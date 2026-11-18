#!/usr/bin/env python3
"""The figure on the Interactive Selection Filtering page.

    uv run python dev/diagrams/selection_filtering.py

Writes ``docs/images/features/selection-filtering/selection-flow_{light,dark}.{svg,png}``.

The dashboard is the image demo of depictio v1.21.0
(``depictio/projects/test/image_demo``): ``category-filter`` (MultiSelect on
``category``), ``quality-scatter-by-category`` (``selection_enabled``,
``selection_column: sample_id``), ``samples-table`` (``row_selection_column:
sample_id``), ``sample-gallery`` and the ``total-samples`` card, all on
``sample_images``, whose ten rows are drawn as they are in ``images_data.csv``.

Each of them writes one entry into the dashboard's filter list, an
``InteractiveFilter`` (``index``, ``value``, ``source``; react-core ``api.ts``):
no ``source`` for an interactive component, ``scatter_selection`` for a figure,
``table_selection`` for a table. Every component's data request carries the
list, and the server ANDs the entries (``process_metadata_and_filter`` and the
``&=`` after it in ``deltatables_utils.py``).
"""

from __future__ import annotations

from pathlib import Path

from component_types import key, type_badge, type_icon
from concepts import edge, icon, ink, raw, rrect, shadow_defs, solid, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "features" / "selection-filtering"

# sample_images, from images_data.csv: (sample_id, category, quality_score).
DATA = (
    ("S001", "A", 0.95), ("S002", "A", 0.87), ("S003", "B", 0.92), ("S004", "B", 0.78), ("S005", "A", 0.89),
    ("S006", "C", 0.94), ("S007", "C", 0.81), ("S008", "B", 0.96), ("S009", "A", 0.73), ("S010", "C", 0.88),
)
CATS = {"B": "#228be6", "C": "#12b886"}  # the figure colours by category; any two colours
LASSO = {"S003", "S006", "S008"}
TICKED = {"S006", "S008"}


def card_frame(s: Sketch, kind: str, x: float, y: float, w: float, h: float, title: str) -> None:
    t = s.theme
    k = key(kind)
    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{white(t)}" stroke="{edge(t, k)}" stroke-width="1.6"/></g>')
    type_badge(s, kind, x + 20, y + 20, 22)
    s.text(x + 38, y + 26, f"`{title}`", size=13, anchor="start", weight="bold", colour=ink(t, k))


def entry(s: Sketch, x: float, y: float, w: float, kind: str, index: str, value: str, source: str) -> None:
    """One InteractiveFilter in the list: who wrote it, the values, the source."""
    t = s.theme
    rrect(s, x, y, w, 76, fill=white(t), stroke=t.muted, r=8, width=1.2)
    rrect(s, x, y, 6, 76, fill=solid(t, key(kind)), r=3, width=0)
    type_icon(s, kind, x + 24, y + 20, 15)
    s.text(x + 38, y + 25, f"`{index}`", size=12, anchor="start", colour=t.dim)
    s.text(x + 16, y + 48, f"value: `{value}`", size=13, anchor="start")
    s.text(x + 16, y + 68, "source: " + (f"`{source}`" if source else "none"), size=13, anchor="start", colour=ink(t, "you") if source else t.dim)


def selection_flow(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(960, 648, theme=t)
    shadow_defs(s)
    s.heading(30, 46, "A selection is one more filter", "the image demo, on `sample_images`: three tiles write to one list, and every tile reads it")
    for cx, label in ((180, "You pick"), (485, "The dashboard's filters"), (800, "Every tile narrows")):
        s.text(cx, 112, label, size=16, weight="bold", colour=t.dim)

    # 1. An interactive component.
    x, w = 30, 300
    card_frame(s, "interactive", x, 128, w, 84, "category-filter")
    rrect(s, x + 14, 166, w - 28, 34, fill=white(t), stroke=solid(t, "you"), r=8, width=1.4)
    for i, c in enumerate(("B", "C")):
        rrect(s, x + 20 + i * 46, 171, 40, 24, fill=solid(t, "you"), r=12, width=0)
        s.text(x + 40 + i * 46, 188, c, size=14, weight="bold", colour="#ffffff" if t.name == "light" else t.bg)

    # 2. A figure: lasso the best-scoring samples of B and C.
    y = 228
    card_frame(s, "figure", x, y, w, 170, "quality-scatter-by-category")
    px0, px1, py0, py1 = x + 50, x + w - 30, y + 150, y + 46
    s.line(px0, py0, px1, py0, colour=t.muted, width=1.1, passes=1)
    s.line(px0, py0, px0, py1, colour=t.muted, width=1.1, passes=1)
    xs = {"B": px0 + (px1 - px0) * 0.3, "C": px0 + (px1 - px0) * 0.72}
    for c, cx in xs.items():
        s.text(cx, py0 + 16, c, size=13, colour=t.dim)
    def py(q: float) -> float:
        return py0 - 8 - (q - 0.75) / 0.23 * (py0 - py1 - 16)
    raw(s, f'<ellipse cx="{(xs["B"] + xs["C"]) / 2:.1f}" cy="{py(0.94):.1f}" rx="{(xs["C"] - xs["B"]) / 2 + 30:.1f}" ry="20" fill="{solid(t, "you")}" fill-opacity="0.10" stroke="{solid(t, "you")}" stroke-width="1.8" stroke-dasharray="6 4"/>')
    for sid, c, q in DATA:
        if c in xs:
            raw(s, f'<circle cx="{xs[c]:.1f}" cy="{py(q):.1f}" r="5.5" fill="{CATS[c]}" fill-opacity="{1 if sid in LASSO else 0.45}"/>')
    icon(s, "selection-drag", x + w - 26, y + 60, 18, solid(t, "you"))

    # 3. A table: tick two rows.
    y = 414
    card_frame(s, "table", x, y, w, 150, "samples-table")
    rrect(s, x + 1.5, y + 40, w - 3, 24, fill=t.fill("grey"), r=0, width=0)
    for cx, head in ((44, "sample_id"), (150, "category"), (230, "quality")):
        s.text(x + cx, y + 57, f"`{head}`", size=12, anchor="start", colour=t.dim)
    for i, sid in enumerate(sorted(LASSO)):
        _sid, c, q = next(d for d in DATA if d[0] == sid)
        ry = y + 64 + i * 27
        on = sid in TICKED
        if on:
            rrect(s, x + 1.5, ry, w - 3, 27, fill=solid(t, "you"), r=0, width=0, opacity=0.13)
        icon(s, "checkbox-marked" if on else "checkbox-blank-outline", x + 24, ry + 14, 16, solid(t, "you") if on else t.muted)
        for cx, cell in ((44, sid), (150, c), (230, f"{q:.2f}")):
            s.text(x + cx, ry + 19, f"`{cell}`", size=13, anchor="start")

    # The list.
    lx, lw = 360, 250
    rrect(s, lx, 128, lw, 436, fill=t.fill("you"), stroke=edge(t, "you"), r=12, width=1.6)
    icon(s, "filter-variant", lx + 22, 152, 18, solid(t, "you"))
    s.text(lx + 40, 158, "One list, three entries", size=15, anchor="start", weight="bold", colour=ink(t, "you"))
    entry(s, lx + 14, 176, lw - 28, "interactive", "category-filter", "B, C", "")
    entry(s, lx + 14, 290, lw - 28, "figure", "quality-scatter-by…", "S003, S006, S008", "scatter_selection")
    entry(s, lx + 14, 418, lw - 28, "table", "samples-table", "S006, S008", "table_selection")
    s.text(lx + lw / 2, 530, "all three must hold:", size=14, colour=t.dim)
    s.text(lx + lw / 2, 551, "`S006` and `S008`", size=15, weight="bold", colour=ink(t, "you"))
    for y0, y1 in ((170, 214), (313, 328), (489, 456)):
        s.arrow(x + w + 4, y0, lx - 4, y1, colour=solid(t, "you"))

    # The tiles that read it.
    gx, gw = 660, 270
    card_frame(s, "image", gx, 128, gw, 210, "sample-gallery")
    for i, sid in enumerate(sorted(TICKED)):
        tx = gx + 22 + i * 120
        rrect(s, tx, 172, 106, 106, fill=t.fill(key("image")), stroke=edge(t, key("image")), r=8, width=1.3)
        icon(s, "image-area", tx + 53, 220, 40, solid(t, key("image")))
        s.text(tx + 53, 300, f"`sample_{sid[1:]}.png`", size=12, colour=t.dim)
    s.text(gx + gw / 2, 326, "two of the ten images", size=14, colour=t.dim)

    card_frame(s, "card", gx, 358, gw, 110, "total-samples")
    s.text(gx + 22, 440, "`2`", size=42, anchor="start", weight="bold", colour=ink(t, key("card")))
    s.text(gx + 60, 436, "(Count) of `sample_id`", size=13, anchor="start", colour=t.dim)

    rrect(s, gx, 488, gw, 76, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.2, dash=True)
    s.text(gx + gw / 2, 518, "and every other tile on", size=14, colour=t.dim)
    s.text(gx + gw / 2, 540, "`sample_images`, or linked to it", size=14, colour=t.dim)
    for y1 in (233, 413, 526):
        s.arrow(lx + lw + 4, 346, gx - 4, y1, colour=solid(t, "you"))

    s.text(30, 604, "Also selections: a lasso or click on a map (`map_selection`), a picked thumbnail (`image_selection`),", size=14, anchor="start", colour=t.dim)
    s.text(30, 626, "a brushed region or track (`genome_selection`, `jbrowse_selection`), and the selecting advanced visualizations.", size=14, anchor="start", colour=t.dim)
    return s


if __name__ == "__main__":
    write_themed(selection_flow, OUT, "selection-flow")
