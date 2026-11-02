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

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "protein-tiles"

LEFT = 46
RIGHT = 1254


def residue_linking(theme: Theme) -> Sketch:
    """One gesture, two outcomes: a pick is sent as a filter, a hover stays local.

    The two rows are parallel on purpose, because the contrast is the point: the
    same tiles, one path that goes through the server's filters and one that
    never leaves the browser. The strip underneath is the protein itself, so
    the range a pick filters and the single residue a hover marks are seen as
    the same axis the tiles share.
    """
    s = Sketch(1300, 640, theme=theme)
    s.heading(
        LEFT,
        56,
        "Protein tiles are linked by residue",
        "a pick filters every table on its residues, a hover only marks them",
    )

    col1, col2, col3 = (LEFT, 250), (380, 420), (880, RIGHT - 880)
    y1, h1 = 130, 128
    y2, h2 = y1 + h1 + 34, 100

    gesture_pick = Box(col1[0], y1, col1[1], h1, "violet", "Click or brush", ("in any protein tile:", "3D, alignment, logo,", "PAE matrix, lollipop"))
    pick = Box(
        col2[0], y1, col2[1], h1, "blue", "A pick is a filter",
        ("`entity`, a `position` range,", "and `chain` on a complex", "the last gesture wins"),
    )
    follow = Box(
        col3[0], y1, col3[1], h1, "green", "Tables narrow, tiles show it",
        ("every table with those columns", "3D rings and zooms, alignment shades", "cards and option lists ignore it"),
    )
    gesture_hover = Box(col1[0], y2, col1[1], h2, "violet", "Pointer", ("over a residue", "in any protein tile"))
    hover = Box(
        col2[0], y2, col2[1], h2, "yellow", "A hover is a highlight",
        ("published in the browser, once per frame", "never sent to the server"),
    )
    marked = Box(col3[0], y2, col3[1], h2, "grey", "Every protein tile marks it", ("nothing is fetched again",))
    for b in (gesture_pick, pick, follow, gesture_hover, hover, marked):
        s.box(b)

    for a, b in ((gesture_pick, pick), (pick, follow)):
        s.arrow(a.right + 6, a.cy, b.x - 6, b.cy)
    for a, b in ((gesture_hover, hover), (hover, marked)):
        s.arrow(a.right + 6, a.cy, b.x - 6, b.cy, dashed=True)

    # -- the shared axis --------------------------------------------------------
    s.line(LEFT, 420, RIGHT, 420, colour=theme.muted, amount=1.0, passes=1, dashed=True)
    s.text(LEFT, 464, "The residue axis every tile shares", size=21, anchor="start")

    cells, size, top = 40, 30, 490
    pick_from, pick_to, hover_at = 13, 21, 31
    for i in range(cells):
        fill = "blue" if pick_from <= i <= pick_to else "yellow" if i == hover_at else "white"
        s.rect(Box(LEFT + i * size, top, size, 34, fill, ""))

    band_x1, band_x2 = LEFT + pick_from * size, LEFT + (pick_to + 1) * size
    s.line(band_x1, top + 52, band_x2, top + 52, colour=theme.dim, amount=1.2)
    s.line(band_x1, top + 46, band_x1, top + 58, colour=theme.dim, amount=0.6, passes=1)
    s.line(band_x2, top + 46, band_x2, top + 58, colour=theme.dim, amount=0.6, passes=1)
    s.text((band_x1 + band_x2) / 2, top + 84, "a pick: a range, sent as a filter", size=15, colour=theme.dim)

    hx = LEFT + hover_at * size + size / 2
    s.arrow(hx, top + 82, hx, top + 42, dashed=True)
    s.text(hx, top + 104, "a hover: one residue, kept local", size=15, colour=theme.dim)
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
    s.box(collection)
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
