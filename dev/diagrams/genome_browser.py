#!/usr/bin/env python3
"""The figure on the Genome browser page: GenomeSpy lanes and the JBrowse view on one tab.

    uv run python dev/diagrams/genome_browser.py

Writes ``docs/images/guides/genome-browser/schema_genomespy_jbrowse_{light,dark}``
as SVG and PNG. The page embeds the PNG with ``#only-light`` / ``#only-dark``,
because an ``<img>`` SVG cannot see the page's Virgil font. The jitter is
seeded, so re-running without editing this file leaves the working tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "genome-browser"

LEFT = 46
PANEL_W = 500
PANEL_Y, PANEL_H = 140, 262
RIGHT_X = 1300 - LEFT - PANEL_W

# Call positions (0 to 1 along the chromosome) and heights per lane: a fixed
# pattern, so the same peaks line up across the replicates of one antibody.
LANES = (
    ((0.07, 0.3), (0.31, 0.9), (0.52, 0.4), (0.83, 0.6)),
    ((0.1, 0.2), (0.31, 0.7), (0.6, 0.3), (0.9, 0.35)),
    ((0.05, 0.5), (0.18, 0.35), (0.31, 1.0), (0.46, 0.45), (0.7, 0.55), (0.93, 0.3)),
    ((0.12, 0.4), (0.31, 0.8), (0.44, 0.3), (0.74, 0.65)),
)
BAND = (0.27, 0.35)  # the browser's window, as a share of the lane
BRUSH = (0.66, 0.8)  # a region picked on the lanes


def _navigator(s: Sketch, theme: Theme) -> None:
    s.rect(Box(LEFT, PANEL_Y, PANEL_W, PANEL_H, "white", ""))
    left, right = LEFT + 24, LEFT + PANEL_W - 20
    span = right - left
    lane_h, gap, top = 44, 10, PANEL_Y + 16
    bottom = top + len(LANES) * (lane_h + gap) - gap
    # The browser's window, a dashed band on every lane, and a region brushed on
    # them: drawn first so the calls stay on top.
    bx0, bx1 = left + BAND[0] * span, left + BAND[1] * span
    s._parts.append(
        f'<rect x="{bx0:.1f}" y="{top - 6:.1f}" width="{bx1 - bx0:.1f}" height="{bottom - top + 12:.1f}" '
        f'fill="{theme.fill("blue")}" stroke="{theme.accent}" stroke-width="1.4" stroke-dasharray="5 4" rx="3" opacity="0.85"/>'
    )
    rx0, rx1 = left + BRUSH[0] * span, left + BRUSH[1] * span
    s._parts.append(
        f'<rect x="{rx0:.1f}" y="{top - 6:.1f}" width="{rx1 - rx0:.1f}" height="{bottom - top + 12:.1f}" '
        f'fill="{theme.fill("yellow")}" stroke="{theme.muted}" stroke-width="1.4" rx="3" opacity="0.8"/>'
    )
    for i, calls in enumerate(LANES):
        y = top + i * (lane_h + gap)
        s.line(left, y + lane_h, right, y + lane_h, colour=theme.muted, width=1.4, amount=0.5, passes=1)
        for at, height in calls:
            x = left + at * span
            s.line(x, y + lane_h, x, y + lane_h - height * (lane_h - 6), colour=theme.ink, width=2.4, amount=0.2, passes=1)
    s.text(left + (BAND[0] + BAND[1]) / 2 * span, bottom + 26, "browser view", size=13, colour=theme.dim)
    s.text(left + (BRUSH[0] + BRUSH[1]) / 2 * span, bottom + 26, "brushed", size=13, colour=theme.dim)
    s.text(LEFT, PANEL_Y - 14, "Navigator", size=19, weight="bold", anchor="start")
    s.text(LEFT + 112, PANEL_Y - 14, "GenomeSpy lanes, one per library", size=15, colour=theme.dim, anchor="start")


def _browser(s: Sketch, theme: Theme) -> None:
    s.rect(Box(RIGHT_X, PANEL_Y, PANEL_W, PANEL_H, "white", ""))
    left, right = RIGHT_X + 24, RIGHT_X + PANEL_W - 20
    span = right - left
    ruler = PANEL_Y + 26
    s.line(left, ruler, right, ruler, colour=theme.ink, width=1.6, amount=0.4, passes=1)
    for i in range(7):
        x = left + i * span / 6
        s.line(x, ruler, x, ruler + 7, colour=theme.ink, width=1.4, amount=0.2, passes=1)
    # Coverage, peaks, a variant row and genes: the track kinds the page lists.
    cov = PANEL_Y + 96
    pts = [(left + i * span / 40, cov - 26 * max(0.08, 1.0 - abs(i - 14) / 6.0) - 8 * ((i * 7) % 3) / 2) for i in range(41)]
    s.polyline(pts, colour=theme.ink, width=2.0, amount=0.4)
    s.line(left, cov, right, cov, colour=theme.muted, width=1.3, amount=0.4, passes=1)
    peaks = PANEL_Y + 126
    for at, width in ((0.32, 0.11), (0.62, 0.07)):
        s._parts.append(
            f'<rect x="{left + at * span:.1f}" y="{peaks:.1f}" width="{width * span:.1f}" height="14" '
            f'fill="{theme.fill("blue")}" stroke="{theme.ink}" stroke-width="1.4" rx="2"/>'
        )
    var = PANEL_Y + 168
    for at in (0.2, 0.34, 0.37, 0.58, 0.8):
        x = left + at * span
        s.line(x, var - 9, x, var + 9, colour=theme.ink, width=2.2, amount=0.2, passes=1)
    genes = PANEL_Y + 204
    for at, width in ((0.1, 0.22), (0.5, 0.3)):
        x0, x1 = left + at * span, left + (at + width) * span
        s.line(x0, genes, x1, genes, colour=theme.ink, width=1.6, amount=0.3, passes=1)
        for k in range(3):
            xe = x0 + (0.1 + 0.3 * k) * (x1 - x0)
            s._parts.append(
                f'<rect x="{xe:.1f}" y="{genes - 8:.1f}" width="14" height="16" fill="{theme.ink}" rx="1"/>'
            )
    s.text(RIGHT_X, PANEL_Y - 14, "Genome browser", size=19, weight="bold", anchor="start")
    s.text(RIGHT_X + 168, PANEL_Y - 14, "JBrowse 2, the tracks of one region", size=15, colour=theme.dim, anchor="start")


def genomespy_jbrowse(theme: Theme) -> Sketch:
    """The lanes overview the calls and pick a region; the browser shows that region's tracks.

    The two sit on one tab, side by side, and each drives the other. The
    dashboard around them filters both, so it sits underneath with its own arrows.
    """
    s = Sketch(1300, 590, theme=theme)
    s.heading(
        LEFT,
        56,
        "GenomeSpy and JBrowse on one tab",
        "the lanes overview every library's calls, the browser shows the tracks of one region",
    )
    _navigator(s, theme)
    _browser(s, theme)

    mid_l, mid_r = LEFT + PANEL_W, RIGHT_X
    cx = (mid_l + mid_r) / 2
    # Lanes to browser: a brush, or the browser opens on the pick.
    s.arrow(mid_l + 12, PANEL_Y + 78, mid_r - 12, PANEL_Y + 78, colour=theme.accent)
    s.text(cx, PANEL_Y + 52, "brush a region:", size=15, colour=theme.accent)
    s.text(cx, PANEL_Y + 106, "the browser opens on it", size=15, colour=theme.accent)
    # Browser to lanes: its window, drawn as a band.
    s.arrow(mid_r - 12, PANEL_Y + 172, mid_l + 12, PANEL_Y + 172, dashed=True, colour=theme.dim)
    s.text(cx, PANEL_Y + 150, "the browser's window", size=15, colour=theme.dim)
    s.text(cx, PANEL_Y + 198, "drawn as a band", size=15, colour=theme.dim)

    # The dashboard around them.
    bar = Box(LEFT, 500, 1208, 70, "grey", "The rest of the dashboard", ("filters, tables and cards",))
    s.box(bar)
    top = PANEL_Y + PANEL_H
    s.arrow(940, top + 6, 940, bar.y - 6, colour=theme.dim, dashed=True)
    s.text(930, (top + bar.y) / 2 + 5, "a click on a feature filters on its sample", size=15, colour=theme.dim, anchor="end")
    s.arrow(1080, bar.y - 6, 1080, top + 6, colour=theme.dim, dashed=True)
    s.text(1090, (top + bar.y) / 2 + 5, "a picked row moves it", size=15, colour=theme.dim, anchor="start")
    s.arrow(300, bar.y - 6, 300, top + 6, colour=theme.dim, dashed=True)
    s.text(310, (top + bar.y) / 2 + 5, "the lanes keep that sample", size=15, colour=theme.dim, anchor="start")
    return s


if __name__ == "__main__":
    write_themed(genomespy_jbrowse, OUT, "schema_genomespy_jbrowse")
