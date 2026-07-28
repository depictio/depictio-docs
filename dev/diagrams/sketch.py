#!/usr/bin/env python3
"""A tiny hand-drawn SVG toolkit, shared by the diagrams in this directory.

Ported from the depictio repo's ``dev/diagrams/sketch.py``, which generates the
schema figures shipped in depictio pull requests. Two things are new here:
figures are drawn once and rendered in both the light and the dark palette, and
the PNG pass uses the font this repo already bundles instead of whatever Virgil
happens to be installed on the machine.

The look is Excalidraw's: every stroke is drawn twice along a jittered bezier,
and the text uses Virgil (Excalidraw's font). Jitter comes from a fixed seed, so
re-running a diagram produces a byte-identical file instead of a spurious diff.

Diagrams are generated rather than drawn so they can be corrected in a diff when
the thing they describe changes; a hand-made PNG goes stale silently.
"""

from __future__ import annotations

import asyncio
import functools
import math
import random
import tempfile
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[2]
VIRGIL_TTF = REPO_ROOT / "docs" / "fonts" / "Virgil.ttf"

# Virgil first, so the bundled @font-face wins over any system copy and the PNG
# render is reproducible on a machine that has never opened Excalidraw.
FONT = "Virgil, Virgil GS, Excalifont, Comic Sans MS, Bradley Hand, cursive"

# MultiQC's mark, copied from depictio's bundled
# `api/static_assets/images/logos/multiqc_icon_color.svg` (viewBox 0 0 251 251).
MULTIQC_PATHS = (
    "M46.6601 120.546C49.2801 81.0979 80.9701 49.4901 120.46 47.0102V0.943359C55.5001 "
    "3.50318 3.28008 55.6197 0.580078 120.546H46.6601Z",
    "M120.19 204.85C80.7401 202.23 49.1301 170.543 46.6501 131.055H0.580078C3.14008 "
    "196.011 55.2601 248.227 120.19 250.927V204.85Z",
    "M130.969 47.0202C170.419 49.6401 202.029 81.3279 204.509 120.816H250.579C248.019 "
    "55.8596 195.899 3.64318 130.969 0.943359V47.0202Z",
    "M250.579 204.85C211.129 202.23 179.519 170.543 177.039 131.055H130.969C133.529 "
    "196.011 185.649 248.227 250.579 250.927V204.85Z",
)


@dataclass(frozen=True)
class Theme:
    """A palette. Figures name their fills semantically and are drawn twice."""

    name: str
    bg: str
    ink: str  # strokes and primary text
    dim: str  # secondary text
    accent: str  # the "look here" stroke
    muted: str  # de-emphasised strokes
    fills: dict[str, str]
    # The one colour not ours to choose. MultiQC's mark is brand ink on light
    # backgrounds and reversed to white on dark ones, which is what its own
    # asset set ships; recolouring it to match our stroke would make it a
    # generic glyph rather than a recognisable logo.
    multiqc: str = "#201637"

    def fill(self, key: str) -> str:
        """``"none"`` keeps a box transparent; anything else indexes the palette."""
        return "none" if key == "none" else self.fills[key]


# Excalidraw's own defaults: near-black ink on white, pastel fills.
LIGHT = Theme(
    name="light",
    bg="#ffffff",
    ink="#1e1e1e",
    dim="#5c5c5c",
    accent="#c92a2a",
    muted="#adb5bd",
    fills={
        "blue": "#e7f5ff",
        "yellow": "#fff9db",
        "green": "#ebfbee",
        "violet": "#f3f0ff",
        "orange": "#ffe8cc",
        "pink": "#ffe3e3",
        "grey": "#f1f3f5",
        "white": "#ffffff",
    },
)

# Tuned against mkdocs-material's slate scheme rather than inverted from LIGHT.
# Straight inversion gives fills that glow; these stay close to the page
# background so they read as a tint on a surface, the way the pastels do.
DARK = Theme(
    name="dark",
    bg="#1f2129",
    ink="#e3e3e3",
    dim="#9aa0ac",
    accent="#ff8787",
    muted="#585e6b",
    fills={
        "blue": "#24303d",
        "yellow": "#363020",
        "green": "#23342a",
        "violet": "#2b2938",
        "orange": "#382c22",
        "pink": "#38262b",
        "grey": "#282b33",
        "white": "#24272f",
    },
    multiqc="#ffffff",
)

THEMES = (LIGHT, DARK)


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float
    fill: str  # a Theme.fills key, or "none"
    title: str
    lines: tuple[str, ...] = ()

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h


class Sketch:
    """Accumulates SVG fragments drawn with a hand-drawn wobble."""

    def __init__(self, width: float, height: float, theme: Theme = LIGHT, seed: int = 7) -> None:
        self.width = width
        self.height = height
        self.theme = theme
        self._rng = random.Random(seed)
        self._parts: list[str] = []

    # -- primitives ---------------------------------------------------------

    def _jitter(self, amount: float) -> float:
        return self._rng.uniform(-amount, amount)

    def _wobble(self, x1: float, y1: float, x2: float, y2: float, amount: float) -> str:
        """One stroke as a cubic bezier whose control points wander off the line.

        Bending the curve rather than displacing the endpoints is what keeps a
        rectangle's corners meeting while its edges still bow.
        """
        cx1 = x1 + (x2 - x1) / 3 + self._jitter(amount)
        cy1 = y1 + (y2 - y1) / 3 + self._jitter(amount)
        cx2 = x1 + 2 * (x2 - x1) / 3 + self._jitter(amount)
        cy2 = y1 + 2 * (y2 - y1) / 3 + self._jitter(amount)
        sx, sy = x1 + self._jitter(amount / 2), y1 + self._jitter(amount / 2)
        ex, ey = x2 + self._jitter(amount / 2), y2 + self._jitter(amount / 2)
        return f"M{sx:.1f},{sy:.1f} C{cx1:.1f},{cy1:.1f} {cx2:.1f},{cy2:.1f} {ex:.1f},{ey:.1f}"

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        width: float = 1.7,
        colour: str | None = None,
        amount: float = 2.0,
        dashed: bool = False,
        passes: int = 2,
    ) -> None:
        colour = colour or self.theme.ink
        dash = ' stroke-dasharray="9 7"' if dashed else ""
        for _ in range(passes):
            d = self._wobble(x1, y1, x2, y2, amount)
            self._parts.append(
                f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" '
                f'stroke-linecap="round"{dash}/>'
            )

    def rect(self, box: Box, *, colour: str | None = None, dashed: bool = False) -> None:
        # Fill first, as a plain rounded rect: a wobbling fill edge reads as a
        # smudge, while a wobbling outline on top of it reads as a pen stroke.
        fill = self.theme.fill(box.fill)
        if fill != "none":
            self._parts.append(
                f'<rect x="{box.x:.1f}" y="{box.y:.1f}" width="{box.w:.1f}" '
                f'height="{box.h:.1f}" rx="6" fill="{fill}"/>'
            )
        corners = [
            (box.x, box.y, box.right, box.y),
            (box.right, box.y, box.right, box.bottom),
            (box.right, box.bottom, box.x, box.bottom),
            (box.x, box.bottom, box.x, box.y),
        ]
        for x1, y1, x2, y2 in corners:
            self.line(x1, y1, x2, y2, amount=1.6, colour=colour, dashed=dashed)

    def arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        dashed: bool = False,
        colour: str | None = None,
    ) -> None:
        self.line(x1, y1, x2, y2, dashed=dashed, colour=colour)
        angle = math.atan2(y2 - y1, x2 - x1)
        for sign in (1, -1):
            head = angle + sign * math.radians(28)
            self.line(
                x2,
                y2,
                x2 - 14 * math.cos(head),
                y2 - 14 * math.sin(head),
                amount=1.0,
                colour=colour,
                passes=1,
            )

    def stack(self, box: Box, *, depth: int = 3, offset: float = 9, icon: str | None = None) -> None:
        """A box drawn as a pile, for "many of these" without listing them.

        The sheets behind are drawn first and outline-only, so the front box
        still reads as the labelled one.
        """
        for i in range(depth - 1, 0, -1):
            back = Box(box.x + i * offset, box.y - i * offset, box.w, box.h, box.fill, "")
            self.rect(back, colour=self.theme.muted)
        self.box(box, icon=icon)

    def curve(self, points: list[tuple[float, float]], *, colour: str | None = None) -> None:
        """A multi-segment stroke, for the loops that no straight line can express."""
        colour = colour or self.theme.dim
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            self.line(x1, y1, x2, y2, colour=colour, amount=1.4, width=1.5)

    # -- glyphs -------------------------------------------------------------

    def polyline(
        self,
        points: list[tuple[float, float]],
        *,
        close: bool = False,
        colour: str | None = None,
        width: float = 1.5,
        amount: float = 0.7,
    ) -> None:
        """A single-pass stroke through ``points``, optionally closed.

        Single-pass and low-jitter on purpose: the double stroke that gives a
        box its sketched edge turns into mush at glyph scale.
        """
        pts = [*points, points[0]] if close else points
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self.line(x1, y1, x2, y2, colour=colour, width=width, amount=amount, passes=1)

    def circle(
        self,
        cx: float,
        cy: float,
        r: float,
        *,
        colour: str | None = None,
        width: float = 1.5,
        segments: int = 14,
    ) -> None:
        pts = [
            (cx + r * math.cos(2 * math.pi * i / segments), cy + r * math.sin(2 * math.pi * i / segments))
            for i in range(segments)
        ]
        self.polyline(pts, close=True, colour=colour, width=width, amount=0.35)

    def glyph(self, name: str, cx: float, cy: float, *, size: float = 30, colour: str | None = None) -> None:
        """One line-art mark, centred on ``(cx, cy)`` and drawn in one colour.

        These are deliberately not emoji and not filled: the figures already
        carry meaning in their fills, so a glyph that brought its own palette
        would compete with the box it sits in.
        """
        colour = colour or self.theme.ink
        s = size
        if name == "multiqc":
            self._multiqc_mark(cx, cy, s)
            return

        line = functools.partial(self.line, colour=colour, width=1.5, amount=0.7, passes=1)
        poly = functools.partial(self.polyline, colour=colour)
        ring = functools.partial(self.circle, colour=colour)

        if name == "table":
            x0, x1, y0, y1 = cx - 0.5 * s, cx + 0.5 * s, cy - 0.38 * s, cy + 0.38 * s
            poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True)
            line(x0, y0 + 0.25 * (y1 - y0), x1, y0 + 0.25 * (y1 - y0))
            line(cx, y0, cx, y1)
        elif name == "image":
            x0, x1, y0, y1 = cx - 0.5 * s, cx + 0.5 * s, cy - 0.38 * s, cy + 0.38 * s
            poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True)
            ring(x0 + 0.24 * s, y0 + 0.22 * s, 0.07 * s)
            poly(
                [
                    (x0 + 0.08 * s, y1 - 0.05 * s),
                    (x0 + 0.36 * s, y0 + 0.40 * s),
                    (x0 + 0.58 * s, y1 - 0.20 * s),
                    (x0 + 0.74 * s, y0 + 0.50 * s),
                    (x1 - 0.04 * s, y1 - 0.05 * s),
                ]
            )
        elif name == "map":
            ring(cx, cy - 0.12 * s, 0.27 * s)
            ring(cx, cy - 0.12 * s, 0.10 * s)
            line(cx - 0.21 * s, cy + 0.06 * s, cx, cy + 0.46 * s)
            line(cx + 0.21 * s, cy + 0.06 * s, cx, cy + 0.46 * s)
        elif name == "tree":
            # A cladogram with its three tips spread over the full height. Any
            # tighter and the risers close up into what reads as a bracket.
            line(cx - 0.50 * s, cy + 0.11 * s, cx - 0.32 * s, cy + 0.11 * s)
            line(cx - 0.32 * s, cy - 0.21 * s, cx - 0.32 * s, cy + 0.42 * s)
            line(cx - 0.32 * s, cy + 0.42 * s, cx + 0.50 * s, cy + 0.42 * s)
            line(cx - 0.32 * s, cy - 0.21 * s, cx - 0.05 * s, cy - 0.21 * s)
            line(cx - 0.05 * s, cy - 0.42 * s, cx - 0.05 * s, cy)
            line(cx - 0.05 * s, cy - 0.42 * s, cx + 0.50 * s, cy - 0.42 * s)
            line(cx - 0.05 * s, cy, cx + 0.50 * s, cy)
        elif name == "folder":
            x0, x1, y0, y1 = cx - 0.5 * s, cx + 0.5 * s, cy - 0.36 * s, cy + 0.36 * s
            poly(
                [
                    (x0, y1),
                    (x0, y0),
                    (x0 + 0.34 * s, y0),
                    (x0 + 0.44 * s, y0 + 0.15 * s),
                    (x1, y0 + 0.15 * s),
                    (x1, y1),
                ],
                close=True,
            )
        elif name == "page":
            x0, x1, y0, y1 = cx - 0.36 * s, cx + 0.36 * s, cy - 0.44 * s, cy + 0.44 * s
            fold = 0.26 * s
            poly(
                [(x0, y0), (x1 - fold, y0), (x1, y0 + fold), (x1, y1), (x0, y1)],
                close=True,
            )
            poly([(x1 - fold, y0), (x1 - fold, y0 + fold), (x1, y0 + fold)])
        elif name == "layers":
            for i, dy in enumerate((-0.28, 0.0, 0.28)):
                w = 0.5 - 0.06 * i
                poly(
                    [
                        (cx - w * s, cy + dy * s),
                        (cx, cy + (dy - 0.14) * s),
                        (cx + w * s, cy + dy * s),
                        (cx, cy + (dy + 0.14) * s),
                    ],
                    close=True,
                )
        else:
            raise ValueError(f"unknown glyph: {name}")

    def _multiqc_mark(self, cx: float, cy: float, size: float) -> None:
        """MultiQC's four-quadrant mark, from depictio's own bundled asset.

        Traced verbatim rather than redrawn: a hand-wobbled approximation of a
        logo is a different logo.
        """
        k = size / 251
        self._parts.append(
            f'<g transform="translate({cx - size / 2:.1f},{cy - size / 2:.1f}) scale({k:.5f})" '
            f'fill="{self.theme.multiqc}">'
            + "".join(f'<path d="{d}"/>' for d in MULTIQC_PATHS)
            + "</g>"
        )

    def cross(self, cx: float, cy: float, *, size: float = 11, colour: str | None = None) -> None:
        """The "this does not happen" mark."""
        colour = colour or self.theme.accent
        self.line(cx - size, cy - size, cx + size, cy + size, colour=colour, amount=1.2, passes=1)
        self.line(cx - size, cy + size, cx + size, cy - size, colour=colour, amount=1.2, passes=1)

    def text(
        self,
        x: float,
        y: float,
        content: str,
        *,
        size: float = 16,
        colour: str | None = None,
        anchor: str = "middle",
        weight: str = "normal",
    ) -> None:
        colour = colour or self.theme.ink
        self._parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{colour}" text-anchor="{anchor}" font-weight="{weight}">'
            f"{escape(content)}</text>"
        )

    def box(
        self,
        box: Box,
        *,
        colour: str | None = None,
        dashed: bool = False,
        icon: str | None = None,
    ) -> None:
        self.rect(box, colour=colour, dashed=dashed)
        if icon:
            # Pinned to the title line rather than the box centre, so a box with
            # three lines of body text and one with none put their icon in the
            # same place relative to the name it labels.
            self.glyph(icon, box.x + 38, box.y + 21, size=28)
        self.text(box.cx, box.y + 27, box.title, size=18, weight="bold")
        for i, line in enumerate(box.lines):
            self.text(box.cx, box.y + 51 + i * 21, line, size=14, colour=self.theme.dim)

    def heading(self, x: float, y: float, title: str, subtitle: str = "") -> None:
        self.text(x, y, title, size=25, anchor="start")
        if subtitle:
            self.text(x, y + 26, subtitle, size=15, colour=self.theme.dim, anchor="start")

    def svg(self) -> str:
        body = "\n  ".join(self._parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width:g}" '
            f'height="{self.height:g}" viewBox="0 0 {self.width:g} {self.height:g}">\n'
            f'  <rect width="{self.width:g}" height="{self.height:g}" fill="{self.theme.bg}"/>\n'
            f"  {body}\n</svg>\n"
        )


def _png_host_page(svg: str) -> str:
    """An HTML shell that inlines the SVG and declares the bundled Virgil.

    Loading the .svg directly would leave the render at the mercy of the host's
    installed fonts, and an <img>-embedded SVG cannot see an @font-face at all,
    so the text would fall back to a cursive substitute and overflow its boxes.
    """
    return (
        "<!doctype html><meta charset='utf-8'><style>"
        f"@font-face{{font-family:'Virgil';src:url('{VIRGIL_TTF.as_uri()}') format('truetype');}}"
        "html,body{margin:0;padding:0}svg{display:block}"
        f"</style><body>{svg}</body>"
    )


async def _render_png(svg: str, png_path: Path, width: float, height: float) -> None:
    from playwright.async_api import async_playwright

    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as fh:
        fh.write(_png_host_page(svg))
        host = Path(fh.name)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={"width": int(width), "height": int(height)}, device_scale_factor=2
            )
            await page.goto(host.as_uri())
            await page.wait_for_timeout(400)  # let the handwriting font load
            await page.screenshot(path=str(png_path))
            await browser.close()
    finally:
        host.unlink(missing_ok=True)


def write(sketch: Sketch, out_dir: Path, name: str, *, png: bool = True) -> Path:
    """Write ``<out_dir>/<name>.svg`` (and its PNG), returning the SVG path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / f"{name}.svg"
    svg = sketch.svg()
    svg_path.write_text(svg, encoding="utf-8")
    print(f"→ {svg_path}")
    if png:
        png_path = svg_path.with_suffix(".png")
        asyncio.run(_render_png(svg, png_path, sketch.width, sketch.height))
        print(f"→ {png_path}")
    return svg_path


def write_themed(build, out_dir: Path, name: str, *, png: bool = True) -> None:
    """Render ``build(theme) -> Sketch`` once per palette.

    Emits ``<name>_light.*`` and ``<name>_dark.*``, the naming the docs already
    use for theme-swapped imagery (``#only-light`` / ``#only-dark``).
    """
    for theme in THEMES:
        write(build(theme), out_dir, f"{name}_{theme.name}", png=png)
