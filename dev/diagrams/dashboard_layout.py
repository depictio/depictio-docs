#!/usr/bin/env python3
"""The three-panel layout on the Dashboards page.

    uv run python dev/diagrams/dashboard_layout.py

Writes ``docs/images/features/dashboards/three-panels_{light,dark}.{svg,png}``.

The dashboard is the iris demo of depictio v1.21.0
(``depictio/projects/init/iris/dashboards``), on its child tab *Iris Petal
Analysis*, in the Classic look. That tab declares the filter sections
*Measurements* and *Scoped views* (folded) and the grid sections *Petal
geometry* and *Variety separation*; the *Variety* filter section and the *Raw
Data* grid section are declared ``persistent`` on the Overview tab, the first
pinned to the top of the left panel, the second to the bottom of the grid.
Two filters are set: Variety = Versicolor and Petal length 4.0 to 5.1 cm. The
card values and the scatter's 39 points are what ``iris.csv`` gives under them.
Iris has no map, so the map dock is drawn empty.
"""

from __future__ import annotations

from pathlib import Path

from component_types import key, type_badge, type_icon
from concepts import edge, icon, ink, raw, rrect, shadow_defs, solid, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "features" / "dashboards"

# (petal.length, petal.width) of the Versicolor flowers with a petal of 4.0 to 5.1 cm.
POINTS = (
    (4.7, 1.4), (4.5, 1.5), (4.9, 1.5), (4.0, 1.3), (4.6, 1.5), (4.5, 1.3), (4.7, 1.6), (4.6, 1.3),
    (4.2, 1.5), (4.0, 1.0), (4.7, 1.4), (4.4, 1.4), (4.5, 1.5), (4.1, 1.0), (4.5, 1.5), (4.8, 1.8),
    (4.0, 1.3), (4.9, 1.5), (4.7, 1.2), (4.3, 1.3), (4.4, 1.4), (4.8, 1.4), (5.0, 1.7), (4.5, 1.5),
    (5.1, 1.6), (4.5, 1.5), (4.5, 1.6), (4.7, 1.5), (4.4, 1.3), (4.1, 1.3), (4.0, 1.3), (4.4, 1.2),
    (4.6, 1.4), (4.0, 1.2), (4.2, 1.3), (4.2, 1.2), (4.2, 1.3), (4.3, 1.3), (4.1, 1.3),
)

W, H = 960, 690
FX, FY, FW, FH = 30, 112, 900, 552  # the dashboard frame
SB, LP = 112, 250  # sidebar and left panel widths


def section(s: Sketch, x: float, y: float, w: float, name: str, *, folded: bool = False, pinned: bool = False, ico: str | None = None, note: str = "") -> None:
    """A section header: chevron, name, and the pin of a section shown on every tab."""
    t = s.theme
    icon(s, "chevron-right" if folded else "chevron-down", x + 8, y - 5, 18, t.dim)
    tx = x + 22
    if ico:
        icon(s, ico, x + 30, y - 5, 16, t.dim)
        tx = x + 44
    s.text(tx, y, name, size=15, anchor="start", weight="bold")
    if pinned:
        icon(s, "pin", x + w - 12, y - 5, 17, solid(t, "you"))
    if note:
        s.text(x + w - (28 if pinned else 6), y, note, size=12, anchor="end", colour=t.dim)


def card(s: Sketch, x: float, y: float, w: float, title: str, value: str, caption: str) -> None:
    t = s.theme
    rrect(s, x, y, w, 82, fill=white(t), stroke=edge(t, key("card")), r=8, width=1.3)
    if len(title) < 15:
        type_icon(s, "card", x + w - 16, y + 17, 14)
    s.text(x + 10, y + 22, title, size=12 if len(title) < 15 else 11, anchor="start", colour=t.dim)
    s.text(x + 10, y + 54, value, size=24, anchor="start", weight="bold", colour=ink(t, key("card")))
    s.text(x + 10, y + 73, caption, size=11, anchor="start", colour=t.dim)


def slider(s: Sketch, x: float, y: float, w: float, label: str, lo: float | None = None, hi: float | None = None, values: str = "") -> None:
    """A RangeSlider: a track, and the picked span in blue when one is set."""
    t = s.theme
    s.text(x, y, label, size=13, anchor="start")
    if values:
        s.text(x + w, y, values, size=12, anchor="end", colour=ink(t, "you"))
    ty = y + 18
    rrect(s, x, ty - 2, w, 4, fill=t.fill("grey"), stroke=t.muted, r=2, width=0.8)
    a, b = (lo, hi) if lo is not None else (0.0, 1.0)
    rrect(s, x + w * a, ty - 2.5, w * (b - a), 5, fill=solid(t, "you") if lo is not None else t.muted, r=2.5, width=0)
    for f in (a, b):
        raw(s, f'<circle cx="{x + w * f:.1f}" cy="{ty:.1f}" r="6" fill="{white(t)}" stroke="{solid(t, "you") if lo is not None else t.muted}" stroke-width="2"/>')


def three_panels(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(W, H, theme=t)
    shadow_defs(s)
    s.heading(FX, 46, "Three panels", "the iris demo's Iris Petal Analysis tab, Classic look, with two filters set")

    # Captions above the frame, one per panel.
    for cx, label in ((FX + SB / 2, "Sidebar"), (FX + SB + LP / 2, "Left panel: filters"), (FX + SB + LP + (FW - SB - LP) / 2, "Right panel: components")):
        s.text(cx, FY - 10, label, size=14, colour=t.dim, weight="bold")

    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="12" fill="{white(t)}" stroke="{t.muted}" stroke-width="1.3"/></g>')

    # Header bar.
    hy = FY + 44
    raw(s, f'<path d="M{FX + 1},{hy} V{FY + 12} Q{FX + 1},{FY + 1} {FX + 12},{FY + 1} H{FX + FW - 12} Q{FX + FW - 1},{FY + 1} {FX + FW - 1},{FY + 12} V{hy} Z" fill="{t.fill("grey")}"/>')
    s.line(FX, hy, FX + FW, hy, colour=t.muted, width=1)
    s.glyph("depictio", FX + 26, FY + 22, size=24)
    s.text(FX + SB + 14, FY + 29, "Iris Petal Analysis", size=17, anchor="start", weight="bold")
    s.text(FX + FW - 16, FY + 28, "Header bar", size=13, anchor="end", colour=t.dim)

    # Sidebar: the tab family.
    x1, x2 = FX + SB, FX + SB + LP
    s.line(x1, hy, x1, FY + FH, colour=t.muted, width=1)
    s.line(x2, hy, x2, FY + FH, colour=t.muted, width=1)
    s.text(FX + 14, hy + 28, "Tabs", size=12, anchor="start", colour=t.dim, weight="bold")
    # Each tab with its `tab_icon` and `tab_icon_color` (violet, grape).
    tabs = (("Overview", None, "flower-outline", "#7950f2", False), ("Iris Petal", "Analysis", "leaf", "#be4bdb", True))
    for i, (a, b, ico, colour, on) in enumerate(tabs):
        ty = hy + 46 + i * 62
        if on:
            rrect(s, FX + 7, ty - 10, SB - 14, 54, fill=t.fill("you"), stroke=edge(t, "you"), r=8, width=1.2)
        icon(s, ico, FX + 22, ty + 7, 17, colour)
        style = {"colour": ink(t, "you") if on else t.ink, "weight": "bold" if on else "normal"}
        s.text(FX + 35, ty + 12, a, size=13, anchor="start", **style)
        if b:
            s.text(FX + 35, ty + 31, b, size=13, anchor="start", **style)

    # Left panel: summary, sections, map dock.
    lx, lw = x1 + 12, LP - 24
    rrect(s, lx, hy + 14, lw, 32, fill=t.fill("you"), stroke=edge(t, "you"), r=8, width=1.2)
    icon(s, "filter-variant", lx + 18, hy + 30, 17, solid(t, "you"))
    s.text(lx + 34, hy + 35, "2 active", size=14, anchor="start", weight="bold", colour=ink(t, "you"))
    icon(s, "chevron-down", lx + lw - 14, hy + 30, 18, solid(t, "you"))

    y = hy + 82
    section(s, lx, y, lw, "Variety", pinned=True, note="every tab")
    s.text(lx + 4, y + 26, "Variety", size=13, anchor="start")
    type_icon(s, "interactive", lx + lw - 10, y + 21, 15)
    rrect(s, lx, y + 34, lw, 34, fill=white(t), stroke=solid(t, "you"), r=8, width=1.4)
    rrect(s, lx + 6, y + 39, 98, 24, fill=solid(t, "you"), r=12, width=0)
    s.text(lx + 55, y + 56, "Versicolor", size=13, weight="bold", colour="#ffffff" if t.name == "light" else t.bg)

    y += 100
    section(s, lx, y, lw, "Measurements")
    s.text(lx + 4, y + 24, "Petal", size=12, anchor="start", colour=t.dim, weight="bold")
    slider(s, lx + 4, y + 46, lw - 12, "Petal length (cm)", 0.50, 0.69, "4.0 to 5.1")
    slider(s, lx + 4, y + 90, lw - 12, "Petal width (cm)")
    s.text(lx + 4, y + 134, "Sepal: two more sliders", size=12, anchor="start", colour=t.dim)

    y += 172
    section(s, lx, y, lw, "Scoped views", folded=True, note="folded")

    # The map dock: a map lifted out of the grid sits here; iris has none.
    dy = y + 22
    s.line(x1 + 1, dy, x2 - 1, dy, colour=t.muted, width=1)
    rrect(s, lx, dy + 12, lw, FY + FH - dy - 24, fill=t.fill(key("map")), stroke=edge(t, key("map")), r=10, width=1.4, dash=True)
    type_icon(s, "map", lx + 20, dy + 34, 18)
    s.text(lx + 36, dy + 40, "Map dock", size=14, anchor="start", weight="bold", colour=ink(t, key("map")))
    rrect(s, lx + lw - 42, dy + 24, 32, 22, fill=solid(t, key("map")), r=11, width=0)
    s.text(lx + lw - 26, dy + 40, "3", size=13, weight="bold", colour="#ffffff" if t.name == "light" else t.bg)
    s.text(lx + lw / 2, dy + 74, "where a map lifted out of the grid", size=11, colour=t.dim)
    s.text(lx + lw / 2, dy + 92, "docks; the badge counts the values", size=11, colour=t.dim)
    s.text(lx + lw / 2, dy + 110, "it filters on (iris has no map)", size=11, colour=t.dim)

    # Right panel: grid sections.
    rx, rw = x2 + 14, FX + FW - x2 - 28
    y = hy + 30
    section(s, rx, y, rw, "Petal geometry", ico="ruler")
    cw = (rw - 30) / 4
    for i, (title, value, cap) in enumerate((
        ("Petal Length", "4.5", "(Median)"),
        ("Petal Width", "1.4", "(Median)"),
        ("Sepal Length", "6.1", "(Median)"),
        ("Petal width values", "8", "(Nunique)"),
    )):
        card(s, rx + i * (cw + 10), y + 14, cw, title, value, cap)

    # The figure, with the 39 flowers the two filters leave.
    fy = y + 108
    fh = 150
    rrect(s, rx, fy, rw, fh, fill=white(t), stroke=edge(t, key("figure")), r=8, width=1.3)
    type_badge(s, "figure", rx + 18, fy + 18, 20)
    s.text(rx + 36, fy + 23, "Petal Length vs Width", size=13, anchor="start", weight="bold", colour=ink(t, key("figure")))
    px0, px1, py0, py1 = rx + 46, rx + rw - 24, fy + fh - 26, fy + 40
    s.line(px0, py0, px1, py0, colour=t.muted, width=1.2, passes=1)
    s.line(px0, py0, px0, py1, colour=t.muted, width=1.2, passes=1)
    s.text((px0 + px1) / 2, fy + fh - 8, "`petal.length`", size=12, colour=t.dim)
    dot = "#fd7e14" if t.name == "light" else "#ffa94d"
    op = 0.55 if t.name == "light" else 0.8
    for pl, pw in POINTS:
        cx = px0 + 10 + (pl - 4.0) / 1.1 * (px1 - px0 - 20)
        cy = py0 - 8 - (pw - 1.0) / 0.8 * (py0 - py1 - 16)
        raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2" fill="{dot}" fill-opacity="{op}"/>')

    y = fy + fh + 34
    section(s, rx, y, rw, "Variety separation", folded=True, ico="chart-scatter-plot", note="folded: its header keeps the cards' values")

    y += 38
    section(s, rx, y, rw, "Raw Data", pinned=True, ico="table", note="from Overview, pinned to the bottom")
    ty = y + 14
    th = FY + FH - ty - 12
    rrect(s, rx, ty, rw, th, fill=white(t), stroke=edge(t, key("table")), r=8, width=1.3)
    type_badge(s, "table", rx + 18, ty + 18, 20)
    s.text(rx + 36, ty + 23, "Iris Dataset", size=13, anchor="start", weight="bold", colour=ink(t, key("table")))
    s.text(rx + rw - 12, ty + 23, "shared, read-only", size=12, anchor="end", colour=t.dim)
    cols = ("sepal.length", "sepal.width", "petal.length", "petal.width", "variety")
    rows = (("7", "3.2", "4.7", "1.4", "Versicolor"), ("6.4", "3.2", "4.5", "1.5", "Versicolor"))
    cwid = rw / 5
    rrect(s, rx + 1.5, ty + 34, rw - 3, 24, fill=t.fill("grey"), r=0, width=0)
    for j, c in enumerate(cols):
        s.text(rx + 12 + j * cwid, ty + 51, f"`{c}`", size=12, anchor="start", colour=t.dim)
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            s.text(rx + 12 + j * cwid, ty + 76 + i * 22, f"`{c}`", size=12, anchor="start")
    return s


if __name__ == "__main__":
    write_themed(three_panels, OUT, "three-panels")
