#!/usr/bin/env python3
"""The figure on the Cross-DC Filtering page.

    uv run python dev/diagrams/cross_dc_filtering.py

Writes ``docs/images/guides/cross-dc-links/cross-dc-flow_{light,dark}.{svg,png}``.

The example is the nf-core/ampliseq template's own links and test data: the
``metadata`` table links on ``sample`` to ``multiqc_data`` (``sample_mapping``
onto ``sample_name``) and to ``taxonomy_rel_abundance`` (``direct`` onto
``sample``). Picking ``Sediment`` keeps three samples; the resolver turns them
into what each target calls them. The mechanism is ``extend_filters_via_links``
in ``depictio/api/v1/filter_links.py``: links are walked from source to target
only, up to ``MAX_LINK_HOPS`` (3) links, and a value set that resolves to
nothing becomes an empty match rather than no filter.
"""

from __future__ import annotations

from pathlib import Path

from concepts import chip, edge, icon, ink, link_line, panel, raw, rrect, shadow_defs, solid, table_panel, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "cross-dc-links"


def step(s: Sketch, x: float, y: float, n: str, label: str) -> None:
    t = s.theme
    raw(s, f'<circle cx="{x + 13:.1f}" cy="{y - 6:.1f}" r="13" fill="{solid(t, "you")}"/>')
    s.text(x + 13, y - 1, n, size=14, weight="bold", colour="#ffffff" if t.name == "light" else t.bg)
    s.text(x + 34, y, label, size=17, anchor="start", colour=t.ink)


def resolver(s: Sketch, x: float, y: float, w: float, name: str, lines: tuple[str, ...]) -> None:
    """A link, drawn as a grey card with the link icon and the resolver's name."""
    t = s.theme
    h = 40 + 21 * len(lines)
    rrect(s, x, y, w, h, fill=t.fill("link"), stroke=edge(t, "link"), r=12, width=1.6)
    icon(s, "link-variant", x + 22, y + 21, 18, solid(t, "link"))
    s.text(x + 40, y + 26, f"`{name}`", size=15, anchor="start", colour=ink(t, "link"), weight="bold")
    for i, line in enumerate(lines):
        s.text(x + 14, y + 52 + i * 21, line, size=14, anchor="start", colour=t.dim)


def cross_dc_flow(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(960, 800, theme=t, clean=False)
    shadow_defs(s)
    s.heading(30, 50, "A filter travels along the links", "nf-core/ampliseq: pick a habitat on `metadata`, and its samples narrow two other collections")

    step(s, 30, 120, "1", "Filter the source")
    step(s, 366, 120, "2", "Links resolve")
    step(s, 572, 120, "3", "The targets narrow")

    # 1. The filter, then the source collection with the rows it keeps.
    rrect(s, 30, 140, 300, 44, fill=white(t), stroke=edge(t, "you"), r=10, width=1.4)
    icon(s, "filter-variant", 52, 162, 18, solid(t, "you"))
    s.text(72, 168, "`habitat`", size=15, anchor="start")
    chip(s, 200, 147, 116, "Sediment", "you", filled=True)
    s.arrow(180, 186, 180, 200, colour=solid(t, "you"))
    table_panel(
        s, 30, 204, 300, "metadata", ("sample", "habitat"),
        [
            ("SRR10070141", "Groundwater"),
            ("SRR10070149", "Sediment"),
            ("SRR10070150", "Sediment"),
            ("SRR10070151", "Sediment"),
            ("SRR10102392", "Soil"),
        ],
        (150, 130), picked={1, 2, 3}, note="dashed: the link column, `sample`", mark_col=0,
    )

    # 2. One card per link, with what its resolver does to the three samples.
    resolver(s, 366, 186, 178, "sample_mapping", ("each sample, plus", "its MultiQC names", "onto `sample_name`"))
    resolver(s, 366, 478, 178, "direct", ("the same three ids", "onto `sample`"))
    link_line(s, 336, 330, 360, 250)
    link_line(s, 336, 380, 360, 500)

    # 3a. MultiQC: the canonical id expands to every variant the report recorded.
    px, py, pw, ph = 572, 140, 370, 212
    panel(s, px, py, pw, ph, "collection", "multiqc_data", ico="table")
    rrect(s, px + 16, py + 10, 26, 26, fill=t.fill("collection"), r=4, width=0)
    s.glyph("multiqc", px + 28, py + 23, size=22)
    s.text(px + 18, py + 76, "`sample_name` kept:", size=14, anchor="start", colour=t.dim)
    for i, sid in enumerate(("SRR10070149", "SRR10070150", "SRR10070151")):
        y = py + 104 + i * 28
        rrect(s, px + 14, y - 19, pw - 28, 26, fill=solid(t, "you"), r=6, width=0, opacity=0.13)
        s.text(px + 22, y, f"`{sid}`, `{sid}_1`, `{sid}_2`", size=14, anchor="start")
    s.text(px + pw / 2, py + ph - 16, "every MultiQC plot shows only these nine", size=14, colour=ink(t, "you"), weight="bold")
    s.arrow(548, 250, 566, 250, colour=solid(t, "link"))

    # 3b. A table: the same ids, so the rows of the other samples drop out.
    table_panel(
        s, 572, 404, 370, "taxonomy_rel_abundance", ("sample", "Phylum", "rel_abundance"),
        [
            ("SRR10070141", "Proteobacteria", "0.65"),
            ("SRR10070149", "Proteobacteria", "0.39"),
            ("SRR10070149", "Acidobacteria", "0.12"),
            ("SRR10070150", "Proteobacteria", "0.40"),
            ("SRR10070151", "Proteobacteria", "0.42"),
        ],
        (114, 126, 100), picked={1, 2, 3, 4}, note="the rows of the other samples drop out",
    )
    s.arrow(548, 512, 566, 512, colour=solid(t, "link"))

    # Direction, under the source: the declared way only.
    dx, dy = 30, 530
    s.text(dx, dy, "One way only", size=17, anchor="start", weight="bold")
    s.text(dx, dy + 22, "a link is declared from a source to a target", size=14, anchor="start", colour=t.dim)
    rows = (("`metadata`", "a target", True), ("a target", "`metadata`", False))
    for i, (a, b, ok) in enumerate(rows):
        y = dy + 46 + i * 46
        for x, label in ((dx, a), (dx + 190, b)):
            rrect(s, x, y, 110, 32, fill=t.fill("collection"), stroke=edge(t, "collection"), r=8, width=1.3)
            s.text(x + 55, y + 21, label, size=14, colour=ink(t, "collection"))
        s.arrow(dx + 118, y + 16, dx + 182, y + 16, colour=solid(t, "good" if ok else "bad"), dashed=not ok)
        if not ok:
            s.cross(dx + 150, y + 16, size=8, colour=solid(t, "bad"))

    # Two rules that hold for every link.
    by = 700
    rrect(s, 30, by, 912, 74, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.2)
    icon(s, "link-variant", 56, by + 26, 18, t.dim)
    s.text(76, by + 31, "Chains count: with A to B to C declared, a filter on A reaches C, up to 3 links away.", size=14, anchor="start")
    icon(s, "filter-variant", 56, by + 52, 18, t.dim)
    s.text(76, by + 57, "No match is an answer: a tile whose values resolve to nothing is empty, never unfiltered.", size=14, anchor="start")
    return s


if __name__ == "__main__":
    write_themed(cross_dc_flow, OUT, "cross-dc-flow")
