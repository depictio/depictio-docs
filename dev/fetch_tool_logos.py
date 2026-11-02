"""Download official logos for the catalog tools the home page's catalog tile shows.

Each entry in LOGOS is a catalog tool folder (depictio/catalog/<tool>) and the
logo its own project publishes, on GitHub. A small SVG is kept as is; anything
else is trimmed, scaled to HEIGHT px and saved as webp:

    python dev/fetch_tool_logos.py

Writes docs/images/landing/logos/tools/<tool>.{svg,webp} and sources.json,
which records where each file came from. Tools without an official logo are
shown as a text chip instead.
One file per tool: the page sets every logo on a light pill, so it reads in
both themes.
"""

from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

DOCS = Path(__file__).resolve().parent.parent / "docs"
OUT = DOCS / "images" / "landing" / "logos" / "tools"
HEIGHT = 48  # shown at 24 CSS px
COLOURS = 64
MAX_SVG = 12 * 1024
GH = "https://raw.githubusercontent.com/{}/HEAD/{}"

LOGOS = {
    "multiqc": GH.format("MultiQC/MultiQC", "docs/images/MultiQC_logo.png"),
    "qiime2": GH.format("qiime2/logos", "raster/transparent/qiime2-rect-400.png"),
    "deseq2": GH.format("Bioconductor/BiocStickers", "DESeq2/DESeq2.png"),
    "edger": GH.format("Bioconductor/BiocStickers", "edgeR/edgeR.png"),
    "dexseq": GH.format("Bioconductor/BiocStickers", "DEXSeq/DEXSeq.png"),
    "pangolin": GH.format("cov-lineages/pangolin", "docs/logo.png"),
    "nextclade": GH.format("nextstrain/nextclade", "packages/nextclade-web/src/assets/img/nextclade_logo.svg"),
    "openms": GH.format("OpenMS/OpenMS", "cmake/MacOSX/openms_logo_small_transparent.png"),
    "quast": GH.format("ablab/quast", "quast_libs/html_saver/static/img/quast_logo_black.png"),
    "cooler": GH.format("open2c/cooler", "docs/cooler_logo.png"),
    "cooltools": GH.format("open2c/cooltools", "docs/figs/cooltools-logo-futura.png"),
    "simpleaf": GH.format("COMBINE-lab/simpleaf", "docs/logo.png"),
    "taxpasta": GH.format("taxprofiler/taxpasta", "docs/assets/images/taxpasta-logo-text.png"),
    "gtdbtk": GH.format("Ecogenomics/GTDBTk", "docs/src/_static/GTDBTk.svg"),
    "mirtop": GH.format("miRTop/mirtop", "artwork/logo.png"),
    "dbcan": GH.format("linnabrown/run_dbcan", "docs/_static/img/dbCAN3_logo.png"),
    "damageprofiler": GH.format("Integrative-Transcriptomics/DamageProfiler", "docs/contents/images/logo.png"),
    "cellbender": GH.format("broadinstitute/CellBender", "docs/source/_static/design/logo_250_185.png"),
    "bowtie2": GH.format("BenLangmead/bowtie2", "doc/images/bowtie_logo.png"),
}

# Logos that spell the tool's name; the others get the name printed beside them.
WORDMARKS = {
    "multiqc", "qiime2", "openms", "quast", "cooler", "taxpasta", "gtdbtk",
    "mirtop", "dbcan", "bowtie2",
}


def svg_width(data: bytes) -> int:
    """Width at HEIGHT px, from the SVG's viewBox."""
    import re

    box = re.search(rb'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', data)
    if not box:
        raise SystemExit("SVG without a viewBox")
    return round(float(box.group(1)) * HEIGHT / float(box.group(2)))


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = {}
    for tool, url in LOGOS.items():
        data = fetch(url)
        if url.endswith(".svg") and len(data) <= MAX_SVG:
            path = OUT / f"{tool}.svg"
            path.write_bytes(data.rstrip() + b"\n")  # as end-of-file-fixer wants
            width = svg_width(data)
        else:
            if url.endswith(".svg"):
                raise SystemExit(f"{tool}: SVG over {MAX_SVG} bytes, point LOGOS at a PNG")
            im = Image.open(io.BytesIO(data)).convert("RGBA")
            box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
            if box:
                im = im.crop(box)
            im = im.resize((round(im.width * HEIGHT / im.height), HEIGHT), Image.LANCZOS)
            im = im.quantize(COLOURS, method=Image.FASTOCTREE).convert("RGBA")
            path = OUT / f"{tool}.webp"
            im.save(path, "WEBP", lossless=True, method=6)
            width = im.width
        # width/height at HEIGHT px, so the page can reserve the space.
        sources[tool] = {
            "file": path.name,
            "width": width,
            "height": HEIGHT,
            "wordmark": tool in WORDMARKS,
            "source": url,
        }
        print(f"{path.relative_to(DOCS)}  {path.stat().st_size / 1024:.1f} KB  <- {url}")
    (OUT / "sources.json").write_text(json.dumps(sources, indent=2) + "\n")


if __name__ == "__main__":
    main()
