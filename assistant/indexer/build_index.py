#!/usr/bin/env python3
"""Build the assistant's retrieval index from the docs tree.

    uv run python assistant/indexer/build_index.py --dry-run
    uv run mkdocs build && uv run python assistant/indexer/build_index.py --verify
    uv run python assistant/indexer/build_index.py --upsert

`--verify` is the important one, and it runs in CI: it diffs every anchor this
script generates against the ids in the built HTML. A citation whose anchor
doesn't resolve is worse than no citation, and nothing else would catch it.

Embeddings come from Workers AI and the index is Cloudflare Vectorize, so the
only credential needed here is a Cloudflare token — the OpenRouter key lives on
the worker and is never seen by CI.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chunker import Chunk, chunk_page  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

EMBED_MODEL = "@cf/baai/bge-m3"
EMBED_DIMS = 1024
EMBED_BATCH = 32
UPSERT_BATCH = 500
INDEX_NAME = "depictio-docs"
# A run that would delete more than this share of the index is refused: it means
# the chunker broke, not that the docs shrank.
MAX_DELETE_SHARE = 0.30

API = "https://api.cloudflare.com/client/v4"


# -- mkdocs.yml ---------------------------------------------------------------


class _LaxLoader(yaml.SafeLoader):
    """mkdocs.yml carries python/name tags for the emoji extensions."""


_LaxLoader.add_multi_constructor("", lambda loader, suffix, node: None)
_LaxLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", lambda *_: None)


def nav_breadcrumbs(mkdocs_yml: Path) -> dict[str, str]:
    """`features/components.md` -> `Features > Dashboard & Components > Components`."""
    cfg = yaml.load(mkdocs_yml.read_text(encoding="utf-8"), Loader=_LaxLoader) or {}
    out: dict[str, str] = {}

    def walk(node, trail: list[str]) -> None:
        if isinstance(node, str):
            out[node] = " > ".join(trail)
        elif isinstance(node, list):
            for item in node:
                walk(item, trail)
        elif isinstance(node, dict):
            for label, value in node.items():
                walk(value, trail + ([label] if isinstance(label, str) else []))

    walk(cfg.get("nav", []), [])
    return out


# -- collection ---------------------------------------------------------------


def load_config() -> dict:
    return yaml.safe_load((HERE / "config.yaml").read_text(encoding="utf-8"))


def should_skip(rel: str, cfg: dict) -> bool:
    if rel in cfg.get("skip_exact", []):
        return True
    return any(rel.startswith(p) for p in cfg.get("skip_prefixes", []))


def collect(cfg: dict) -> tuple[list[Chunk], list[str]]:
    docs = ROOT / cfg["docs_dir"]
    crumbs = nav_breadcrumbs(ROOT / "mkdocs.yml")
    overrides = cfg.get("overrides") or {}

    chunks: list[Chunk] = []
    skipped: list[str] = []
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(docs).as_posix()
        if should_skip(rel, cfg):
            skipped.append(rel)
            continue
        rule = overrides.get(rel, {})
        chunks += chunk_page(
            rel,
            path.read_text(encoding="utf-8"),
            breadcrumb=crumbs.get(rel, ""),
            max_depth=rule.get("max_depth", 4),
            drop_headings=tuple(rule.get("drop_headings", ())),
        )

    for path in sorted((HERE / "seed").glob("*.md")):
        chunks += seed_chunks(path)
    return chunks, skipped


def seed_chunks(path: Path) -> list[Chunk]:
    """Hand-written context for what the docs tree cannot supply.

    The landing page is raw HTML with nothing citable, and "open an issue" has
    no page of its own — but the system prompt tells the model to say it, so it
    needs a real source to point at rather than a URL it made up.
    """
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    if raw.startswith("---\n"):
        _, front, raw = raw.split("---\n", 2)
        meta = yaml.safe_load(front) or {}

    produced = chunk_page(f"_seed/{path.stem}.md", raw, breadcrumb=meta.get("breadcrumb", "Depictio"))
    # A seed chunk cites a page it did not come from, so its anchor is dropped:
    # `--verify` cannot check an anchor that was never generated from a heading.
    return [
        Chunk(**{**asdict(c), "url": meta.get("url", ""), "anchor": "", "section": "seed"})
        for c in produced
    ]


# -- verify -------------------------------------------------------------------

ID_RE = re.compile(r'<h[1-4][^>]*\sid="([^"]+)"', re.I)


def verify(chunks: list[Chunk], site: Path) -> int:
    """Every generated anchor must exist in the built HTML."""
    if not site.is_dir():
        print(f"!! {site} not found — run `mkdocs build` first", file=sys.stderr)
        return 1

    cache: dict[str, set[str] | None] = {}
    missing = []
    for c in chunks:
        if not c.anchor or c.section == "seed":
            continue
        if c.url not in cache:
            page = site / c.url / "index.html"
            cache[c.url] = set(ID_RE.findall(page.read_text(encoding="utf-8"))) if page.is_file() else None
        ids = cache[c.url]
        if ids is None:
            missing.append((c.url, c.anchor, "page not built"))
        elif c.anchor not in ids:
            missing.append((c.url, c.anchor, "anchor absent"))

    checked = sum(1 for c in chunks if c.anchor and c.section != "seed")
    if missing:
        print(f"FAIL  {len(missing)}/{checked} anchors do not resolve:", file=sys.stderr)
        for url, anchor, why in missing[:40]:
            print(f"  {url}#{anchor}  ({why})", file=sys.stderr)
        if len(missing) > 40:
            print(f"  … and {len(missing) - 40} more", file=sys.stderr)
        return 1
    print(f"OK    {checked} anchors resolve against {site}")
    return 0


# -- cloudflare ---------------------------------------------------------------


def cf_session():
    import requests

    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not account or not token:
        sys.exit("!! CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set")
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    return s, f"{API}/accounts/{account}"


def embed(session, base: str, texts: list[str]) -> list[list[float]]:
    out: list[list[float]] = []
    batch = EMBED_BATCH
    i = 0
    while i < len(texts):
        window = texts[i : i + batch]
        r = session.post(f"{base}/ai/run/{EMBED_MODEL}", json={"text": window}, timeout=120)
        if r.status_code == 400 and batch > 4:
            # The maximum array length is undocumented; halve and retry rather
            # than guess it.
            batch //= 2
            continue
        r.raise_for_status()
        out += r.json()["result"]["data"]
        i += len(window)
        print(f"    embedded {i}/{len(texts)}", end="\r", flush=True)
    print()
    return out


def upsert(session, base: str, vectors: list[dict]) -> None:
    url = f"{base}/vectorize/v2/indexes/{INDEX_NAME}/upsert?unparsable-behavior=error"
    for i in range(0, len(vectors), UPSERT_BATCH):
        window = vectors[i : i + UPSERT_BATCH]
        body = "\n".join(json.dumps(v, separators=(",", ":")) for v in window)
        r = session.post(
            url, data=body.encode("utf-8"), headers={"Content-Type": "application/x-ndjson"}, timeout=180
        )
        r.raise_for_status()
        print(f"    upserted {min(i + UPSERT_BATCH, len(vectors))}/{len(vectors)}", end="\r", flush=True)
    print()


def delete_ids(session, base: str, ids: list[str]) -> None:
    url = f"{base}/vectorize/v2/indexes/{INDEX_NAME}/delete_by_ids"
    for i in range(0, len(ids), UPSERT_BATCH):
        r = session.post(url, json={"ids": ids[i : i + UPSERT_BATCH]}, timeout=120)
        r.raise_for_status()


def kv_ids(session, base: str, namespace: str, value: list[str] | None):
    """Vectorize can neither list ids nor bulk-delete, so the id set lives in KV.

    Without it a removed page's chunks would linger in the index forever, still
    retrievable and still cited.
    """
    url = f"{base}/storage/kv/namespaces/{namespace}/values/index:ids"
    if value is None:
        r = session.get(url, timeout=60)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        return r.json()
    r = session.put(url, files={"value": (None, json.dumps(value)), "metadata": (None, "{}")}, timeout=60)
    r.raise_for_status()
    return value


def embed_text(c: Chunk) -> str:
    """Prefix the breadcrumb so a short chunk under a generic heading like
    "Configuration" still carries what it is configuring."""
    return f"{c.breadcrumb}\n\n{c.text}"


def to_vector(c: Chunk, values: list[float]) -> dict:
    return {
        "id": c.id,
        "values": values,
        "metadata": {
            "u": c.url,
            "a": c.anchor,
            "t": c.title,
            "b": c.breadcrumb,
            "s": c.section,
            "p": c.part,
            "x": c.text[:3500],
        },
    }


# -- reporting ----------------------------------------------------------------


def report(chunks: list[Chunk], skipped: list[str]) -> None:
    sizes = sorted(len(c.text) for c in chunks)
    by_section: dict[str, int] = {}
    for c in chunks:
        by_section[c.section] = by_section.get(c.section, 0) + 1

    total = sum(sizes)
    print(f"{len(chunks)} chunks, {total / 1000:.0f} kB, {total // max(len(chunks), 1)} chars average")
    if sizes:
        mid = sizes[len(sizes) // 2]
        print(f"  min {sizes[0]}  median {mid}  max {sizes[-1]}")
    print(f"  ~{total // 4 / 1000:.0f}k tokens to embed, {len(chunks) * EMBED_DIMS / 1e6:.2f}M stored dims")
    print("\nby section:")
    for name, n in sorted(by_section.items(), key=lambda kv: -kv[1]):
        print(f"  {n:5}  {name}")
    print(f"\n{len(skipped)} files skipped:")
    for rel in skipped:
        print(f"  {rel}")


# -- main ---------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="chunk and report, touch nothing")
    ap.add_argument("--verify", nargs="?", const="site", metavar="SITE_DIR", help="check anchors against built HTML")
    ap.add_argument("--upsert", action="store_true", help="embed and push to Vectorize")
    ap.add_argument("--force", action="store_true", help="skip the mass-deletion guard")
    ap.add_argument("--out", type=Path, help="also write the chunks as JSON, for inspection")
    args = ap.parse_args()

    cfg = load_config()
    chunks, skipped = collect(cfg)

    if args.out:
        args.out.write_text(json.dumps([asdict(c) for c in chunks], indent=2), encoding="utf-8")
        print(f"→ {args.out}")

    if args.verify is not None:
        return verify(chunks, ROOT / args.verify)

    if not args.upsert:
        report(chunks, skipped)
        return 0

    session, base = cf_session()
    namespace = os.environ.get("CLOUDFLARE_KV_NAMESPACE_ID")
    if not namespace:
        sys.exit("!! CLOUDFLARE_KV_NAMESPACE_ID must be set to track the index id set")

    previous = set(kv_ids(session, base, namespace, None))
    current = {c.id for c in chunks}
    stale = sorted(previous - current)

    if previous and len(stale) / len(previous) > MAX_DELETE_SHARE and not args.force:
        sys.exit(
            f"!! refusing to delete {len(stale)}/{len(previous)} vectors "
            f"({len(stale) / len(previous):.0%}). Re-run with --force if this is intended."
        )

    print(f"embedding {len(chunks)} chunks with {EMBED_MODEL}")
    values = embed(session, base, [embed_text(c) for c in chunks])
    print(f"upserting {len(chunks)} vectors")
    upsert(session, base, [to_vector(c, v) for c, v in zip(chunks, values)])
    if stale:
        print(f"deleting {len(stale)} stale vectors")
        delete_ids(session, base, stale)
    kv_ids(session, base, namespace, sorted(current))

    summary = ROOT / "assistant" / ".last-run-summary.md"
    summary.write_text(
        f"- {len(chunks)} chunks indexed ({EMBED_MODEL}, {EMBED_DIMS} dims)\n"
        f"- {len(current - previous)} added, {len(stale)} removed\n"
        f"- {len(skipped)} files skipped\n",
        encoding="utf-8",
    )
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
