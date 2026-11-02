"""Derive the home page's composed images from the component screenshots.

dev/capture_components.py writes single shots to docs/images/landing/components/.
This script builds, light and dark:

    python dev/make_thumbs.py

- two card grids (four cards each) from the single-card shots, in components/,
  which the component showcase's Card panel shows;
- four tiny thumbnails for the "advanced visualizations" KPI tile, in
  docs/images/landing/thumbs/.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

DOCS = Path(__file__).resolve().parent.parent / "docs"
IMAGES = DOCS / "images"
SHOTS = IMAGES / "landing" / "components"
THUMBS = IMAGES / "landing" / "thumbs"
AV = IMAGES / "guides" / "advanced-visualizations"

THUMB_QUALITY = 75
FULL_QUALITY = 80
THEMES = ("light", "dark")

# Card shots side by side, two per row.
CARD_GRIDS = {
    "card_grid_a": ["card_species", "card_mass", "card_season", "card_flipper"],
    "card_grid_b": ["card_bills", "card_island", "card_sex", "card_individuals"],
}

# The advanced-visualizations KPI tile: tiny shots from that page.
KPI = ("volcano", "sunburst", "genome_chord", "oncoplot")
KPI_WIDTH = 320


def save(im: Image.Image, path: Path, width: int | None, quality: int) -> None:
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", quality=quality, method=6)
    print(f"{path.relative_to(DOCS)}  {im.width}x{im.height}  {path.stat().st_size / 1024:.1f} KB")


def grid(names: list[str], theme: str, gap: int = 24) -> Image.Image:
    ims = [Image.open(SHOTS / f"{n}_{theme}.webp").convert("RGB") for n in names]
    w, h = ims[0].size
    # The page colour, from outside the card's rounded corner.
    out = Image.new("RGB", (2 * w + gap, 2 * h + gap), ims[0].getpixel((1, 1)))
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    return out


def main() -> None:
    for theme in THEMES:
        for name, cards in CARD_GRIDS.items():
            save(grid(cards, theme), SHOTS / f"{name}_{theme}.webp", None, FULL_QUALITY)
        for kind in KPI:
            im = Image.open(AV / f"{kind}_{theme}.webp").convert("RGB")
            save(im, THUMBS / f"kpi_{kind}_{theme}.webp", KPI_WIDTH, THUMB_QUALITY)


if __name__ == "__main__":
    main()
