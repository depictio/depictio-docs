#!/usr/bin/env python3
"""Check that every image the published site points at is actually there.

Images and the catalog gallery are published once at the site root rather than
copied into each version (see hooks/shared_images.py), so a page and the file
it wants now live in different places. Nothing at build time notices when the
two disagree: the deploy succeeds and the pages come out with broken images.

This reads the deploy branch through git, so it needs no checkout of what is a
multi-GB branch and no wait for GitHub Pages to publish.

Usage:
  scripts/verify-shared-assets.py --version v1.2.2
  scripts/verify-shared-assets.py --all
"""

from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from collections import defaultdict

# Only references to these are checked. Everything else on a page (stylesheets,
# scripts, cross-page links) is emitted relative by mkdocs and moves with it.
INTERESTING = re.compile(r"(?:^|/)(?:images/|assets/component-catalog-)")
REF_RE = re.compile(rb"""(?:src|href)=["']([^"'>]+)["']""")
ASSET_RE = re.compile(r"\.(?:png|jpe?g|gif|svg|webp|html)$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", action="append", default=[],
                   help="version directory to check; repeatable")
    p.add_argument("--all", action="store_true",
                   help="check every published version")
    p.add_argument("--branch", default="gh-pages")
    p.add_argument("--remote", default="origin")
    p.add_argument("--site-url", default="https://depictio.github.io/depictio-docs/",
                   help="site root that absolute references are written against")
    p.add_argument("--no-fetch", action="store_true",
                   help="use the local ref as-is")
    return p.parse_args()


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def main() -> int:
    args = parse_args()
    if not args.all and not args.version:
        sys.exit("give --version at least once, or --all")

    ref = f"{args.remote}/{args.branch}"
    if not args.no_fetch:
        git("fetch", "-q", args.remote, args.branch)

    site = args.site_url.rstrip("/") + "/"
    tree = {}
    for line in git("ls-tree", "-r", ref).splitlines():
        meta, path = line.split("\t", 1)
        tree[path] = meta.split()[2]

    if args.all:
        scope = None
    else:
        scope = tuple(f"{v.strip('/')}/" for v in args.version)
        for prefix in scope:
            if not any(p.startswith(prefix) for p in tree):
                sys.exit(f"no such version on {ref}: {prefix.rstrip('/')}")

    pages = [(sha, p) for p, sha in tree.items()
             if p.endswith(".html") and (scope is None or p.startswith(scope))]
    print(f"checking {len(pages)} pages on {ref}", flush=True)

    # One blob at a time: feeding every sha up front deadlocks, because the
    # child stops draining stdin once its stdout pipe fills.
    cat = subprocess.Popen(["git", "cat-file", "--batch"],
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert cat.stdin and cat.stdout

    missing: dict[str, list[str]] = defaultdict(list)
    checked = 0
    for sha, path in pages:
        cat.stdin.write(f"{sha}\n".encode())
        cat.stdin.flush()
        size = int(cat.stdout.readline().split()[2])
        data = cat.stdout.read(size)
        cat.stdout.read(1)

        base = posixpath.dirname(path)
        for match in REF_RE.finditer(data):
            url = match.group(1).decode("utf-8", "replace").split("#")[0].split("?")[0]
            if url.startswith(site):
                target = url[len(site):]
            elif url.startswith("/"):
                # Absolute-path form, used by 404.html: /<repo>/<rest>.
                target = url.lstrip("/").split("/", 1)[-1]
            elif "://" in url or url.startswith(("#", "mailto:", "data:")):
                continue
            else:
                target = posixpath.normpath(posixpath.join(base, url))
            if not ASSET_RE.search(target) or not INTERESTING.search(target):
                continue
            checked += 1
            if target not in tree:
                missing[target].append(path)
    cat.stdin.close()
    cat.wait()

    print(f"resolved {checked} references, {len(missing)} targets missing")
    if not missing:
        return 0

    print("\nmissing:", file=sys.stderr)
    for target, sources in sorted(missing.items(), key=lambda kv: -len(kv[1])):
        print(f"  {target}  ({len(sources)} pages, e.g. {sources[0]})", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
