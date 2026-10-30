#!/usr/bin/env python3
"""The figure on the Protein tiles page.

    uv run python dev/diagrams/protein_tiles.py

Writes ``docs/images/guides/protein-tiles/schema_residue_linking.svg``, one SVG in
the light palette and no PNG: the page embeds the SVG, like the versioning
schemas. The jitter is seeded, so re-running without editing this file leaves the
working tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import LIGHT, Box, Sketch, Theme, write

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "protein-tiles"


def residue_linking(theme: Theme) -> Sketch:
    """Two halves: how tiles stay linked, then where the 3D model comes from.

    The pick and the hover are drawn as two parallel rows because their whole
    point is the contrast: the same gesture source, one goes through the
    server's filters and one never leaves the browser. The resolver is a chain
    read left to right, first hit wins, with the switch that gates it on the
    box that enters it.
    """
    s = Sketch(1300, 800, theme=theme)
    s.heading(
        46,
        56,
        "Protein tiles: one protein, linked by residue",
        "a pick filters every table on its residues, a hover only marks them, "
        "and the 3D model comes from the run or from the resolver",
    )

    # -- linking ---------------------------------------------------------------
    tiles = Box(
        46,
        140,
        270,
        230,
        "violet",
        "Protein tiles",
        (
            "3D structure",
            "alignment, sequence track",
            "HMM logo, domains",
            "secondary structure",
            "PAE matrix, Ramachandran",
            "lollipop, profile",
        ),
    )
    pick = Box(
        420,
        140,
        400,
        100,
        "blue",
        "A pick is a filter",
        ("`entity` + a `position` range, `chain` on a complex", "the last gesture wins"),
    )
    narrowed = Box(
        900,
        140,
        354,
        100,
        "green",
        "Every table narrows",
        ("that has those columns", "cards and option lists ignore it"),
    )
    hover = Box(
        420,
        270,
        400,
        100,
        "yellow",
        "A hover is a highlight",
        ("published in the browser, once per frame", "never sent to the server"),
    )
    marked = Box(900, 270, 354, 100, "grey", "Every protein tile marks it", ("nothing is fetched again",))
    for b in (tiles, pick, narrowed, hover, marked):
        s.box(b)

    s.arrow(tiles.right + 6, pick.cy, pick.x - 6, pick.cy)
    s.text((tiles.right + pick.x) / 2, pick.cy - 12, "click, brush", size=14, colour=theme.dim)
    s.arrow(tiles.right + 6, hover.cy, hover.x - 6, hover.cy, dashed=True)
    s.text((tiles.right + hover.x) / 2, hover.cy - 12, "pointer", size=14, colour=theme.dim)
    s.arrow(pick.right + 6, pick.cy, narrowed.x - 6, pick.cy)
    s.arrow(hover.right + 6, hover.cy, marked.x - 6, hover.cy, dashed=True)

    # -- where the structure comes from -------------------------------------------
    s.line(46, 420, 1254, 420, colour=theme.muted, amount=1.0, passes=1, dashed=True)
    s.text(46, 466, "Where the 3D model comes from", size=21, anchor="start")

    row1 = 500
    row2 = 640
    height = 96

    file_src = Box(
        46, row1, 270, height, "orange", "`structure_source: file`", ("a `pdb` or `mmcif` file", "per protein, from the run")
    )
    collection = Box(
        420,
        row1,
        400,
        height,
        "white",
        "An indexed-file collection",
        ("fetched through a presigned URL", "no outbound call from the server"),
    )
    resolve_src = Box(
        46,
        row2,
        270,
        height,
        "pink",
        "`structure_source: resolve`",
        ("off until the server", "turns the resolver on"),
    )
    for b in (file_src, collection, resolve_src):
        s.box(b)
    s.arrow(file_src.right + 6, file_src.cy, collection.x - 6, file_src.cy)

    width = 188
    gap = 36
    x = 394
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
    write(residue_linking(LIGHT), OUT, "schema_residue_linking", png=False)
