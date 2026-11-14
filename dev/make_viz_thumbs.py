"""Build the Catalog thumbnails of the Advanced visualizations page.

The catalog grid shows small webp crops; the lightbox opens the full screenshot.
Each tile's shape comes from its class in the page (viz-tile--f featured 2x2,
--w wide 2x1, --t tall 1x2, --s 1x1), so the page stays the single source of
truth: change a class, rerun this script.

    python dev/make_viz_thumbs.py

Crops keep the top left of the screenshot (the tile title and y axis), the
same anchor as the grid's object-position. Sources are never upscaled.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "docs/features/advanced-visualizations.md"
IMAGES = ROOT / "docs/images/guides/advanced-visualizations"
THUMBS = IMAGES / "thumbs"

SIZES = {"f": (960, 720), "w": (960, 360), "t": (480, 720), "s": (480, 360)}
QUALITY = 75

TILE_RE = re.compile(
    r'<div class="viz-tile viz-tile--([fwts])" markdown>\n'
    r"\[!\[[^\]]*\]\([^)]*/thumbs/([a-z0-9_]+)_light\.webp"
)


def thumb(src: Path, dst: Path, size: tuple[int, int]) -> None:
    tw, th = size
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target = tw / th
    if w / h > target:  # wider than the tile: keep full height and the left
        cw, ch = round(h * target), h  # edge, where the title and y axis are
        box = (0, 0, cw, ch)
    else:  # taller than the tile: keep full width, crop from the top
        cw, ch = w, round(w / target)
        box = (0, 0, cw, ch)
    im = im.crop(box)
    scale = min(1.0, tw / cw)
    im = im.resize((round(cw * scale), round(ch * scale)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=QUALITY, method=6)


def main() -> None:
    tiles = TILE_RE.findall(PAGE.read_text())
    if not tiles:
        raise SystemExit(f"no viz-tile found in {PAGE}")
    THUMBS.mkdir(exist_ok=True)
    total = 0
    for shape, kind in tiles:
        for theme in ("light", "dark"):
            dst = THUMBS / f"{kind}_{theme}.webp"
            thumb(IMAGES / f"{kind}_{theme}.webp", dst, SIZES[shape])
            total += dst.stat().st_size
    print(f"{len(tiles)} tiles, {2 * len(tiles)} thumbnails, {total / 1024:.0f} KiB in {THUMBS}")


if __name__ == "__main__":
    main()
