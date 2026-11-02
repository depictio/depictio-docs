"""Rebuild docs/data/landing_stats.json from a depictio checkout.

The landing page's "Depictio in numbers" tiles read every count from that JSON
(hooks/landing_stats.py injects them at build time), so a release only needs:

    git -C ../depictio fetch
    mkdir -p /tmp/dp && git -C ../depictio archive origin/main \
        depictio/catalog depictio/projects depictio/models pyproject.toml \
        | tar -x -C /tmp/dp
    python dev/landing_stats.py /tmp/dp

The argument is the root of a depictio checkout (or of an extracted archive),
the directory that holds depictio/ and pyproject.toml.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent / "docs" / "data" / "landing_stats.json"

# AdvancedVizKind still lists the kinds that became views of another one. They
# are counted through VIEWS below, not as kinds of their own.
LEGACY_ALIASES = {"ma", "qq", "enrichment", "roc_pr_curve"}

# Alternate views a kind switches between, each a visualization of its own on
# the advanced-visualizations page. Kind -> the extra views it adds.
VIEWS = {
    "volcano": ["MA plot", "QQ plot"],
    "manhattan": ["rainfall"],
    "dot_plot": ["enrichment"],
    "pr_benchmark": ["ROC curve"],
    "phylogenetic": ["summary by rank"],
    "domain_architecture": ["architectures"],
}

# Well-known tools on the catalog tile, in this order: a logo where
# dev/fetch_tool_logos.py has one, else the name. Ids that are not in the
# catalog are dropped, so the strip never shows a missing tool.
TOOL_CHIPS = [
    "multiqc", "salmon", "deseq2", "qiime2", "star", "samtools", "pangolin",
    "bcftools", "nextclade", "kallisto", "quast", "busco", "openms", "metaphlan",
    "edger", "macs2", "cooler", "cellranger", "taxpasta", "snpeff", "bowtie2",
    "gtdbtk", "dexseq", "mosdepth", "cellbender", "picard", "mirtop", "deeptools",
    "simpleaf", "arriba", "dbcan", "cnvkit", "cooltools", "nanoplot",
    "damageprofiler", "bismark",
]

# Render order and labels for the stacked bar on the renders tile.
COMPONENT_LABELS = {
    "card": "Card",
    "advanced_viz": "Advanced viz",
    "table": "Table",
    "figure": "Figure",
    "interactive": "Interactive",
    "multiqc": "MultiQC",
}


def version(root: Path) -> str:
    text = (root / "pyproject.toml").read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    if not match:
        sys.exit("no version in pyproject.toml")
    return match.group(1)


def catalog(root: Path) -> dict:
    base = root / "depictio" / "catalog"
    tools = sorted(
        p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    outputs = 0
    renders: Counter[str] = Counter()
    for tool in tools:
        for path in sorted((base / tool).rglob("*.yaml")):
            if path.name == "module.yaml":
                continue
            doc = yaml.safe_load(path.read_text())
            if not isinstance(doc, dict) or "renders_as" not in doc:
                continue
            outputs += 1
            for render in doc.get("renders_as") or []:
                renders[render.get("component", "?")] += 1
    return {"tools": tools, "outputs": outputs, "renders": renders}


def templates(root: Path) -> list[str]:
    base = root / "depictio" / "projects" / "nf-core"
    return sorted(p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))


def viz_kinds(root: Path) -> list[str]:
    text = (root / "depictio" / "models" / "components" / "types.py").read_text()
    match = re.search(r"^AdvancedVizKind\s*=\s*Literal\[(.*?)^\]", text, re.M | re.S)
    if not match:
        sys.exit("AdvancedVizKind not found")
    body = "\n".join(line.split("#", 1)[0] for line in match.group(1).splitlines())
    kinds = list(dict.fromkeys(re.findall(r'"([a-z0-9_]+)"', body)))
    return [k for k in kinds if k not in LEGACY_ALIASES]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("root", type=Path, help="depictio checkout or extracted archive")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    root = args.root.resolve()

    cat = catalog(root)
    kinds = viz_kinds(root)
    missing = sorted(set(VIEWS) - set(kinds))
    if missing:
        sys.exit(f"VIEWS names kinds no longer in AdvancedVizKind: {missing}")
    views = sum(len(v) for v in VIEWS.values())
    pipelines = templates(root)
    renders = cat["renders"]
    unknown = sorted(set(renders) - set(COMPONENT_LABELS))
    if unknown:
        sys.exit(f"add a label for these render components: {unknown}")

    stats = {
        "version": version(root),
        "templates": len(pipelines),
        "tools": len(cat["tools"]),
        "outputs": cat["outputs"],
        "renders": sum(renders.values()),
        "viz": len(kinds) + views,
        "viz_kinds": len(kinds),
        "viz_views": views,
        "renders_by_component": [
            {"id": key, "label": label, "count": renders[key]}
            for key, label in sorted(COMPONENT_LABELS.items(), key=lambda kv: -renders[kv[0]])
            if renders[key]
        ],
        "pipelines": pipelines,
        "tool_chips": [t for t in TOOL_CHIPS if t in cat["tools"]],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(stats, indent=2) + "\n")
    print(
        f"v{stats['version']}: {stats['templates']} templates, {stats['tools']} tools, "
        f"{stats['outputs']} outputs, {stats['renders']} renders, "
        f"{stats['viz']} visualizations ({stats['viz_kinds']} kinds + {views} views) -> {args.out}"
    )


if __name__ == "__main__":
    main()
