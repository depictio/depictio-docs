#!/usr/bin/env python3
"""The figures on the Protein tiles page.

    uv run python dev/diagrams/protein_tiles.py

Writes ``docs/images/guides/protein-tiles/schema_residue_linking_{light,dark}``
and ``schema_structure_resolver_{light,dark}``, each as SVG and PNG. The page
embeds the PNG with ``#only-light`` / ``#only-dark``, because an ``<img>`` SVG
cannot see the page's Virgil font. The jitter is seeded, so re-running without
editing this file leaves the working tree clean.
"""

from __future__ import annotations

import math
from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "protein-tiles"

LEFT = 46
RIGHT = 1254


def _tile(s: Sketch, theme: Theme, x: float, y: float, w: float, h: float, title: str, kind: str) -> None:
    """One protein tile as a thumbnail, with the picked range banded across it.

    Every tile draws the same band at the same offset, because that is the claim:
    one range, shown by all of them. The thin column to the right is the hover.
    """
    s.rect(Box(x, y, w, h, "white", ""))
    pic_top, pic_h = y + 16, h - 66
    band_x, band_w, hover_x = x + 0.34 * w, 0.22 * w, x + 0.78 * w
    s._parts.append(
        f'<rect x="{band_x:.1f}" y="{pic_top:.1f}" width="{band_w:.1f}" height="{pic_h:.1f}" '
        f'fill="{theme.fill("blue")}" stroke="{theme.accent}" stroke-width="1.4" stroke-dasharray="5 4" rx="3"/>'
    )
    s._parts.append(
        f'<rect x="{hover_x:.1f}" y="{pic_top:.1f}" width="9" height="{pic_h:.1f}" '
        f'fill="{theme.fill("yellow")}" stroke="{theme.muted}" stroke-width="1.2" rx="2"/>'
    )
    left, right, mid = x + 16, x + w - 16, pic_top + pic_h / 2
    ink = theme.ink
    if kind == "3d":
        pts = [(left + i * (right - left) / 24, mid + 16 * math.sin(i * 0.9) + 8 * math.sin(i * 0.37)) for i in range(25)]
        s.polyline(pts, colour=ink, width=2.0, amount=0.5)
        s.circle(band_x + band_w / 2, mid, 9, colour=theme.accent, width=2.0)
    elif kind == "alignment":
        for r, ln in enumerate((1.0, 0.92, 0.84, 0.96, 0.7)):
            yy = pic_top + 10 + r * (pic_h - 20) / 4
            s.line(left, yy, left + ln * (right - left), yy, colour=ink, width=2.0, amount=0.6, passes=1)
    elif kind == "track":
        n = 11
        cw = (right - left) / n
        for i in range(n):
            s.rect(Box(left + i * cw, mid - 14, cw, 28, "none", ""), colour=theme.dim)
    elif kind == "pae":
        n = 5
        cw, ch = (right - left) / n, (pic_h - 8) / n
        for i in range(n):
            for j in range(n):
                if abs(i - j) <= 1:
                    s._parts.append(
                        f'<rect x="{left + i * cw + 1:.1f}" y="{pic_top + 4 + j * ch + 1:.1f}" width="{cw - 2:.1f}" '
                        f'height="{ch - 2:.1f}" fill="{theme.muted}" opacity="0.7"/>'
                    )
        s.rect(Box(left, pic_top + 4, right - left, pic_h - 8, "none", ""), colour=theme.dim)
    elif kind == "lollipop":
        base = pic_top + pic_h - 8
        s.line(left, base, right, base, colour=ink, width=1.8, amount=0.6, passes=1)
        for fx, fh in ((0.08, 0.35), (0.3, 0.8), (0.42, 0.55), (0.58, 0.9), (0.86, 0.45)):
            px, py = left + fx * (right - left), base - fh * (pic_h - 26)
            s.line(px, base, px, py, colour=ink, width=1.6, amount=0.3, passes=1)
            s.circle(px, py, 5, colour=ink, width=1.6)
    s.text(x + w / 2, y + h - 18, title, size=16, weight="bold")


def residue_linking(theme: Theme) -> Sketch:
    """Tiles share one residue range; a pick leaves for the server as a filter, a hover never does.

    The browser is drawn as a dashed zone because that is the line the hover does
    not cross: everything in it is shared by the tiles, and only the pick goes out.
    """
    s = Sketch(1300, 740, theme=theme)
    s.heading(
        LEFT,
        56,
        "Protein tiles are linked by residue",
        "a pick is a filter that leaves the browser, a hover only marks the residue in every tile",
    )

    zone = Box(LEFT, 118, 1208, 300, "none", "")
    s.rect(zone, colour=theme.muted, dashed=True)
    s.text(LEFT + 22, zone.bottom - 18, "in the browser", size=15, colour=theme.dim, anchor="start")

    w, gap, top, h = 200, 24, 176, 168
    x0 = LEFT + (1208 - (5 * w + 4 * gap)) / 2
    tiles = ("3D structure", "Alignment", "Sequence track", "PAE matrix", "Lollipop")
    kinds = ("3d", "alignment", "track", "pae", "lollipop")
    for i, (title, kind) in enumerate(zip(tiles, kinds)):
        _tile(s, theme, x0 + i * (w + gap), top, w, h, title, kind)

    # The hover: a dashed line over the tiles, one arrow into each.
    hover_y = 146
    hxs = [x0 + i * (w + gap) + 0.78 * w + 4.5 for i in range(5)]
    s.line(hxs[0], hover_y, hxs[-1], hover_y, colour=theme.dim, amount=1.0, dashed=True)
    for hx in hxs:
        s.arrow(hx, hover_y, hx, top - 4, dashed=True, colour=theme.dim)
    s.text(x0, hover_y - 8, "a hover: one residue, marked in every tile, never sent to the server", size=15, colour=theme.dim, anchor="start")

    # The pick: out of the browser, as a filter, into every table.
    pick_x = x0 + 2 * (w + gap) + 0.34 * w + 0.11 * w
    filt = Box(pick_x - 150, 478, 300, 96, "blue", "A filter", ("`entity` and a `position` range", "`chain` on a complex"))
    s.box(filt)
    s.arrow(pick_x, top + h + 4, pick_x, filt.y - 6, colour=theme.accent)
    s.text(pick_x - 16, (zone.bottom + filt.y) / 2 + 6, "a pick: a click or a brush, the last one wins", size=15, colour=theme.accent, anchor="end")

    tables = [
        Box(900, 448, 354, 62, "pink", "Residue table", ()),
        Box(900, 536, 354, 62, "pink", "Variants", ()),
        Box(900, 624, 354, 62, "pink", "Domains", ()),
    ]
    for t in tables:
        s.rect(t)
        s.glyph("table", t.x + 38, t.cy, size=30)
        s.text(t.x + 78, t.cy + 6, t.title, size=18, weight="bold", anchor="start")
        s.arrow(filt.right + 6, filt.cy, t.x - 8, t.cy, dashed=True, colour=theme.accent)
    s.text(
        (filt.right + tables[0].x) / 2,
        tables[2].bottom + 22,
        "every table with those columns narrows",
        size=15,
        colour=theme.accent,
    )
    s.text(filt.cx, filt.bottom + 44, "cards and option lists ignore it", size=15, colour=theme.dim)
    return s


def structure_resolver(theme: Theme) -> Sketch:
    """Where the 3D model comes from: the run's file, or the resolver chain.

    The chain reads left to right, first hit wins, and the switch that gates it
    sits on the box that enters it.
    """
    s = Sketch(1300, 420, theme=theme)
    s.heading(
        LEFT,
        56,
        "Where the 3D model comes from",
        "the run's own file, or a model the resolver fetches when a server turns it on",
    )

    row1, row2, height = 130, 270, 100

    file_src = Box(
        LEFT, row1, 270, height, "orange", "`structure_source: file`",
        ("a `pdb` or `mmcif` file", "per protein, from the run"),
    )
    collection = Box(
        400, row1, 400, height, "white", "An indexed-file collection",
        ("fetched through a presigned URL", "no outbound call from the server"),
    )
    resolve_src = Box(
        LEFT, row2, 270, height, "pink", "`structure_source: resolve`",
        ("off until the server", "turns the resolver on"),
    )
    s.box(file_src)
    s.box(collection, icon="folder")
    s.box(resolve_src)
    s.arrow(file_src.right + 6, file_src.cy, collection.x - 6, file_src.cy)

    width, gap, x = 188, 36, 394
    chain = []
    for fill, title, lines in (
        ("grey", "Bucket cache", ("a model fetched", "before")),
        ("blue", "AlphaFold DB", ("by UniProt", "accession")),
        ("blue", "UniProt", ("gene and taxon", "to an accession")),
        ("blue", "ESMFold", ("folds a sequence", "of at most 400 aa")),
    ):
        b = Box(x, row2, width, height, fill, title, lines)
        s.box(b)
        chain.append(b)
        x += width + gap

    s.arrow(resolve_src.right + 6, resolve_src.cy, chain[0].x - 6, resolve_src.cy)
    for a, b in zip(chain, chain[1:]):
        s.arrow(a.right + 4, a.cy, b.x - 4, b.cy)

    s.text(
        (chain[0].x + chain[-1].right) / 2,
        row2 + height + 40,
        "first hit wins, only these three services are called, and the tile names the one it used",
        size=15,
        colour=theme.dim,
    )
    return s


if __name__ == "__main__":
    write_themed(residue_linking, OUT, "schema_residue_linking")
    write_themed(structure_resolver, OUT, "schema_structure_resolver")
