#!/usr/bin/env python3
"""The two figures on the Components page.

    uv run python dev/diagrams/components_figures.py

Writes ``docs/images/features/components/card-stat-lists_{light,dark}.*`` and
``docs/images/features/components/cross-dc-components_{light,dark}.*``.

*Card stat lists*: the iris demo's ``card-raw-sepal-length`` (Overview, Raw Data
section of depictio v1.21.0): ``average`` of ``sepal.length`` as the hero value,
``aggregations: [median, std_dev, min, max]`` under it. The three layouts are
``StatList`` in ``packages/depictio-react-core/src/components/card/metrics``
(``vertical``: label left, value right; ``compact``: one row, value under its
label; ``grid``: two columns); the template sets ``compact``. Labels are the
aggregation names with ``_`` turned into spaces, numbers as ``formatCardNumber``
prints them, over the 150 flowers of ``iris.csv`` (sample standard deviation).

*Cross-DC components*: the nf-core/ampliseq 2.16.0 template, with its test data.
The habitat MultiSelect sits on ``metadata``; the template links ``metadata`` to
``taxonomy_rel_abundance`` (``direct``) and to ``multiqc_data``
(``sample_mapping``), and its dashboard shows both as a table and as MultiQC's
general statistics. Samples and rows as on the Cross-DC Filtering figure.
"""

from __future__ import annotations

from pathlib import Path

from component_types import key, type_badge, type_icon
from concepts import edge, icon, ink, link_line, raw, rrect, shadow_defs, solid, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "features" / "components"

INDIGO = {"light": "#4c6ef5", "dark": "#91a7ff"}  # Mantine indigo, the card's title_color
ROWS = (("median", "5.8"), ("std dev", "0.828"), ("min", "4.3"), ("max", "7.9"))


def iris_card(s: Sketch, x: float, y: float, w: float, h: float, layout: str) -> None:
    t = s.theme
    ind = INDIGO[t.name]
    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{white(t)}" stroke="{t.muted}" stroke-width="1.2"/></g>')
    icon(s, "ruler", x + w - 40, y + 46, 44, "#bac8ff" if t.name == "light" else "#364fc7")
    s.text(x + 18, y + 34, "Sepal length", size=16, anchor="start", weight="bold", colour=ind)
    s.text(x + 18, y + 80, "5.84", size=36, anchor="start", weight="bold", colour=ind)
    s.text(x + 18, y + 104, "(Average)", size=13, anchor="start", colour=t.dim)
    sy = y + 122
    s.line(x + 14, sy, x + w - 14, sy, colour=t.fill("grey"), width=1.4, passes=1)
    if layout == "vertical":
        for i, (lab, val) in enumerate(ROWS):
            yy = sy + 28 + i * 25
            s.text(x + 18, yy, lab, size=14, anchor="start", colour=t.dim)
            s.text(x + w - 18, yy, val, size=14, anchor="end", weight="bold")
    elif layout == "compact":
        cw = (w - 24) / 4
        for i, (lab, val) in enumerate(ROWS):
            cx = x + 12 + cw * (i + 0.5)
            s.text(cx, sy + 30, lab, size=13, colour=t.dim)
            s.text(cx, sy + 54, val, size=15, weight="bold")
    else:
        for i, (lab, val) in enumerate(ROWS):
            cx = x + 18 + (i % 2) * (w - 36) / 2
            yy = sy + 26 + (i // 2) * 48
            s.text(cx, yy, lab, size=13, anchor="start", colour=t.dim)
            s.text(cx, yy + 21, val, size=15, anchor="start", weight="bold")


def card_stat_lists(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(960, 432, theme=t)
    shadow_defs(s)
    s.heading(30, 46, "One card, three ways to list its secondary metrics", "iris `Sepal length`: `average` as the hero, `aggregations: [median, std_dev, min, max]` under it")
    w, gap = 290, 25
    for i, (layout, label, sub) in enumerate((
        ("vertical", "`vertical`", "the default: one row each"),
        ("compact", "`compact`", "one strip; what the iris demo sets"),
        ("grid", "`grid`", "two columns, for four to six"),
    )):
        x = 30 + i * (w + gap)
        s.text(x + w / 2, 122, label, size=17, weight="bold", colour=ink(t, key("card")))
        s.text(x + w / 2, 144, sub, size=13, colour=t.dim)
        iris_card(s, x, 162, w, 244, layout)
    return s


SAMPLES = ("SRR10070149", "SRR10070150", "SRR10070151")


def cross_dc_components(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(960, 540, theme=t)
    shadow_defs(s)
    s.heading(30, 46, "One filter, three collections", "nf-core/ampliseq: the habitat filter sits on `metadata`; links carry its samples to a table and to MultiQC")

    # The interactive component, on metadata.
    x, y, w, h = 30, 150, 270, 196
    rrect(s, x, y, w, h, fill=white(t), stroke=edge(t, key("interactive")), r=10, width=1.6)
    type_badge(s, "interactive", x + 24, y + 26, 26)
    s.text(x + 46, y + 32, "Habitat", size=17, anchor="start", weight="bold", colour=ink(t, key("interactive")))
    s.text(x + w - 14, y + 32, "MultiSelect", size=13, anchor="end", colour=t.dim)
    icon(s, "table", x + 24, y + 66, 16, solid(t, "collection"))
    s.text(x + 40, y + 71, "`metadata`, column `habitat`", size=13, anchor="start", colour=t.dim)
    rrect(s, x + 14, y + 88, w - 28, 38, fill=white(t), stroke=solid(t, "you"), r=8, width=1.5)
    rrect(s, x + 20, y + 94, 104, 26, fill=solid(t, "you"), r=13, width=0)
    s.text(x + 72, y + 112, "Sediment", size=14, weight="bold", colour="#ffffff" if t.name == "light" else t.bg)
    s.text(x + 18, y + 152, "keeps 3 samples:", size=13, anchor="start", colour=t.dim)
    s.text(x + 18, y + 174, "`SRR10070149`, `…150`, `…151`", size=13, anchor="start")

    # The links.
    def label(cx: float, cy: float, name: str) -> None:
        rrect(s, cx - 74, cy - 15, 148, 30, fill=t.fill("link"), stroke=edge(t, "link"), r=15, width=1.3)
        icon(s, "link-variant", cx - 54, cy, 16, solid(t, "link"))
        s.text(cx - 38, cy + 5, f"`{name}`", size=13, anchor="start", colour=ink(t, "link"))

    link_line(s, 306, 220, 506, 168)
    link_line(s, 306, 290, 506, 410)
    label(400, 180, "direct")
    label(400, 340, "sample_mapping")

    # The table, on taxonomy_rel_abundance.
    tx, ty, tw = 512, 96, 418
    rrect(s, tx, ty, tw, 222, fill=white(t), stroke=edge(t, key("table")), r=10, width=1.6)
    type_badge(s, "table", tx + 24, ty + 24, 24)
    s.text(tx + 46, ty + 30, "`taxonomy_rel_abundance`", size=15, anchor="start", weight="bold", colour=ink(t, key("table")))
    hy = ty + 46
    rrect(s, tx + 1.5, hy, tw - 3, 26, fill=t.fill("grey"), r=0, width=0)
    cols = (16, 150, 300)
    for cx, head in zip(cols, ("sample", "Phylum", "rel_abundance")):
        s.text(tx + cx, hy + 18, f"`{head}`", size=13, anchor="start", colour=t.dim)
    body = (
        ("SRR10070141", "Proteobacteria", "0.65", False),
        ("SRR10070149", "Proteobacteria", "0.39", True),
        ("SRR10070149", "Acidobacteria", "0.12", True),
        ("SRR10070150", "Proteobacteria", "0.40", True),
    )
    for i, (a, b, c, on) in enumerate(body):
        ry = hy + 26 + i * 27
        if on:
            rrect(s, tx + 1.5, ry, tw - 3, 27, fill=solid(t, "you"), r=0, width=0, opacity=0.13)
        for cx, cell in zip(cols, (a, b, c)):
            s.text(tx + cx, ry + 19, f"`{cell}`", size=13, anchor="start", colour=t.ink if on else t.muted)
    s.text(tx + tw / 2, ty + 208, "the rows of the other samples drop out", size=13, colour=t.dim)

    # MultiQC, on multiqc_data.
    mx, my, mw = 512, 340, 418
    rrect(s, mx, my, mw, 170, fill=white(t), stroke=edge(t, key("multiqc")), r=10, width=1.6)
    type_icon(s, "multiqc", mx + 24, my + 24, 22)
    s.text(mx + 46, my + 30, "MultiQC, general statistics", size=15, anchor="start", weight="bold", colour=ink(t, key("multiqc")))
    s.text(mx + 16, my + 62, "`multiqc_data`, the names the report recorded:", size=13, anchor="start", colour=t.dim)
    for i, sid in enumerate(SAMPLES):
        yy = my + 90 + i * 26
        rrect(s, mx + 12, yy - 18, mw - 24, 24, fill=solid(t, "you"), r=6, width=0, opacity=0.13)
        s.text(mx + 20, yy, f"`{sid}`, `{sid}_1`, `{sid}_2`", size=13, anchor="start")
    return s


if __name__ == "__main__":
    write_themed(card_stat_lists, OUT, "card-stat-lists")
    write_themed(cross_dc_components, OUT, "cross-dc-components")
