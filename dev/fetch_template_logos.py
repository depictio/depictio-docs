"""Download the nf-core template logos the home page's templates tile shows.

Each template page's banner links its pipeline's logo on GitHub. The home page
must not hotlink 32 of them, so this fetches each once, trims it, scales it to
HEIGHT px and saves light and dark webp copies:

    python dev/fetch_template_logos.py

Writes docs/images/landing/logos/templates/<pipeline>_{light,dark}.webp and
sizes.json (each logo's size and source).
nf-core's _logo_light.png is drawn for light backgrounds, _logo_dark.png for
dark ones.
"""

from __future__ import annotations

import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

DOCS = Path(__file__).resolve().parent.parent / "docs"
PAGES = DOCS / "pipeline-templates" / "nf-core"
OUT = DOCS / "images" / "landing" / "logos" / "templates"
HEIGHT = 56  # shown at 28 CSS px, so crisp on 2x screens
COLOURS = 48  # flat logos: a small palette, then lossless, is ~1 KB each
LOGO = re.compile(r'src="(https://raw\.githubusercontent\.com/nf-core/[^"]+_logo_light\.png)"')


def fetch(url: str) -> Image.Image:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGBA")


def save(im: Image.Image, path: Path) -> int:
    box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if box:
        im = im.crop(box)
    im = im.resize((round(im.width * HEIGHT / im.height), HEIGHT), Image.LANCZOS)
    im = im.quantize(COLOURS, method=Image.FASTOCTREE).convert("RGBA")
    im.save(path, "WEBP", lossless=True, method=6)
    print(f"{path.relative_to(DOCS)}  {im.width}x{im.height}  {path.stat().st_size / 1024:.1f} KB")
    return im.width


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pages = sorted(p for p in PAGES.glob("*.md") if p.name != "index.md")
    sizes = {}
    for page in pages:
        match = LOGO.search(page.read_text())
        if not match:
            sys.exit(f"no logo in the banner of {page}")
        light = match.group(1)
        dark = light.replace("_logo_light.png", "_logo_dark.png")
        widths = [save(fetch(url), OUT / f"{page.stem}_{theme}.webp") for theme, url in (("light", light), ("dark", dark))]
        # One width for both, so the two copies swap without a shift.
        sizes[page.stem] = {"width": max(widths), "height": HEIGHT, "source": light}
    # Read by hooks/landing_stats.py for the img width/height.
    (OUT / "sizes.json").write_text(json.dumps(sizes, indent=2) + "\n")


if __name__ == "__main__":
    main()
