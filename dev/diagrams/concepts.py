#!/usr/bin/env python3
"""Depictio's concepts in the app's own colours and icons, shared by the figures.

A figure that shows a project, a data collection or a dashboard draws it with
the colour and the icon the app gives it, so a reader recognises on screen what
they saw in a figure. Red and green are not concepts: red marks what does not
happen, green what is created or allowed.

    uv run python dev/diagrams/concepts.py   # the legend, on Data Model and the workshop Reference
"""

from __future__ import annotations

from pathlib import Path

from mdi_icons import MDI, VIEW
from sketch import DARK, LIGHT, Sketch, Theme, write_themed

# The app's colours, read from the depictio viewer, as Mantine 7 shade 6:
# Projects teal and Dashboards orange (chrome/AppSidebar.tsx); a table data
# collection teal (projects/dcTypeIcon.tsx: image pink, map and tree grape);
# versions yellow (versions/*: pinned, data version, preview); a run folder
# yellow (projects/fromRun); the primary colour, blue, for what the user does.
# Links have no colour of their own in the app, so they stay in neutral grey.
CONCEPTS: dict[str, str] = {
    "project": "#12b886",  # teal
    "collection": "#12b886",  # teal: a table data collection
    "link": "#868e96",  # grey: no colour of its own in the app
    "dashboard": "#fd7e14",  # orange
    "run": "#fab005",  # yellow
    "version": "#fab005",  # yellow
    "you": "#228be6",  # blue: the app's primary colour, on its buttons
    "people": "#868e96",  # grey: other users
    "good": "#40c057",  # green: created, allowed
    "bad": "#fa5252",  # red: does not happen
}
# The icons the app draws for each (Iconify names in the viewer).
ICONS: dict[str, str] = {
    "project": "jira",  # sidebar Projects: mdi:jira
    "dashboard": "view-dashboard",  # sidebar Dashboards: material-symbols:dashboard, same glyph
    "collection": "table",  # dcTypeIcon: mdi:table
    "link": "link-variant",  # Cross-DC links: mdi:link-variant
    "run": "folder-play-outline",  # Runs tab: mdi:folder-play-outline
    "version": "history",
    "you": "account",
}
# Chart colours inside the miniature dashboards: the figures' own colourway.
DATA = ("#228be6", "#12b886", "#fd7e14", "#be4bdb")


def _mix(a: str, b: str, t: float) -> str:
    """``t`` of colour ``a`` over colour ``b``."""
    pa = [int(a[i : i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02x}" for x, y in zip(pa, pb))


def _ink(theme_name: str, key: str) -> str:
    c = CONCEPTS[key]
    if theme_name == "light":
        return _mix(c, "#000000", 0.62 if c == "#fab005" else 0.8)
    return _mix(c, "#ffffff", 0.78)


# Tints become fill keys of both palettes, so `Box(..., "project", ...)` works,
# and inks the outline of such a box (see Sketch.box).
for _key, _c in CONCEPTS.items():
    LIGHT.fills[_key] = _mix(_c, "#ffffff", 0.10)
    DARK.fills[_key] = _mix(_c, DARK.bg, 0.22)
    LIGHT.inks[_key] = _ink("light", _key)
    DARK.inks[_key] = _ink("dark", _key)


def ink(theme: Theme, key: str) -> str:
    """The concept's stroke and text colour, darkened on white, lifted on slate."""
    return _ink(theme.name, key)


def solid(theme: Theme, key: str) -> str:
    c = CONCEPTS[key]
    return c if theme.name == "light" else _mix(c, "#ffffff", 0.88)


def edge(theme: Theme, key: str) -> str:
    """A light outline in the concept's colour, for cards that should not shout."""
    c = CONCEPTS[key]
    return _mix(c, "#ffffff", 0.55) if theme.name == "light" else _mix(c, theme.bg, 0.6)


def raw(s: Sketch, svg: str) -> None:
    s._parts.append(svg)


def white(t: Theme) -> str:
    return t.fill("white")


def fg_on(t: Theme) -> str:
    """Text on a filled button."""
    return "#ffffff" if t.name == "light" else t.bg


# -- primitives -----------------------------------------------------------------


def icon(s: Sketch, name: str, cx: float, cy: float, size: float, colour: str) -> None:
    """One mdi icon, the same glyph the app draws."""
    vw, vh = VIEW.get(name, (24, 24))
    k = size / max(vw, vh)
    ox, oy = cx - vw * k / 2, cy - vh * k / 2
    raw(s, f'<path transform="translate({ox:.1f},{oy:.1f}) scale({k:.4f})" d="{MDI[name]}" fill="{colour}"/>')


def rrect(s: Sketch, x: float, y: float, w: float, h: float, *, fill: str, stroke: str = "none", r: float = 10, width: float = 1.4, dash: bool = False, opacity: float = 1) -> None:
    d = ' stroke-dasharray="7 5"' if dash else ""
    o = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    raw(s, f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{width}"{d}/>')


def shadow_defs(s: Sketch) -> None:
    raw(s, '<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-opacity="0.12"/></filter></defs>')


def panel(s: Sketch, x: float, y: float, w: float, h: float, key: str, title: str, *, ico: str | None = None, header: float = 46, sub: str = "", shadow: bool = True) -> None:
    """A white card with a header band tinted in the concept's colour."""
    t = s.theme
    f = ' filter="url(#sh)"' if shadow and t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{white(t)}" stroke="{edge(t, key)}" stroke-width="1.6"/></g>')
    raw(s, f'<path d="M{x + 1:.1f},{y + header:.1f} V{y + 12:.1f} Q{x + 1:.1f},{y + 1:.1f} {x + 12:.1f},{y + 1:.1f} H{x + w - 12:.1f} Q{x + w - 1:.1f},{y + 1:.1f} {x + w - 1:.1f},{y + 12:.1f} V{y + header:.1f} Z" fill="{t.fill(key)}"/>')
    s.line(x, y + header, x + w, y + header, colour=edge(t, key), width=1.2)
    tx = x + 16
    if ico or key in ICONS:
        icon(s, ico or ICONS[key], x + 28, y + header / 2, 22, solid(t, key))
        tx = x + 48
    s.text(tx, y + header / 2 + 6, title, size=17, anchor="start", weight="bold", colour=ink(t, key))
    if sub:
        s.text(x + w - 16, y + header / 2 + 5, sub, size=13, anchor="end", colour=t.dim)


def badge(s: Sketch, cx: float, cy: float, label: str, key: str) -> None:
    """A numbered disc in a concept's colour, like the annotated screenshots."""
    raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="14" fill="{solid(s.theme, key)}"/>')
    s.text(cx, cy + 5, label, size=15, colour=fg_on(s.theme), weight="bold")


def button(s: Sketch, x: float, y: float, w: float, text: str, kind: str = "you", *, h: float = 34, ico: str | None = None, ring: bool = False) -> None:
    """A filled app button: kind is a concept key (you = primary blue, people = grey, good = green)."""
    t = s.theme
    rrect(s, x, y, w, h, fill=solid(t, kind), r=8, width=0)
    if ico:
        icon(s, ico, x + 20, y + h / 2, 18, fg_on(t))
        s.text(x + 34 + (w - 34) / 2, y + h / 2 + 5, text, size=14, weight="bold", colour=fg_on(t))
    else:
        s.text(x + w / 2, y + h / 2 + 5, text, size=14, weight="bold", colour=fg_on(t))
    if ring:
        rrect(s, x - 5, y - 5, w + 10, h + 10, fill="none", stroke=solid(t, "you"), r=12, width=2.5)


def chip(s: Sketch, x: float, y: float, w: float, text: str, key: str, *, filled: bool = False, ico: str | None = None) -> None:
    """A rounded pill, the way filters, groups and tabs look in the app."""
    t = s.theme
    rrect(s, x, y, w, 30, fill=solid(t, key) if filled else t.fill(key), stroke="none" if filled else edge(t, key), r=15, width=1.3)
    fg = fg_on(t) if filled else ink(t, key)
    if ico:
        icon(s, ico, x + 18, y + 15, 16, fg)
        s.text(x + 28 + (w - 28) / 2, y + 20, text, size=14, colour=fg, weight="bold" if filled else "normal")
    else:
        s.text(x + w / 2, y + 20, text, size=14, colour=fg, weight="bold" if filled else "normal")


def icon_button(s: Sketch, cx: float, cy: float, name: str, *, key: str | None = None, ring: bool = False, size: float = 32) -> None:
    """An icon-only button; ring draws the attention halo used in the screenshots."""
    t = s.theme
    colour = solid(t, key) if key else t.dim
    h = size / 2
    rrect(s, cx - h, cy - h, size, size, fill=t.fill(key) if key else white(t), stroke=edge(t, key) if key else t.muted, r=8, width=1.2)
    icon(s, name, cx, cy, size * 0.56, colour)
    if ring:
        rrect(s, cx - h - 6, cy - h - 6, size + 12, size + 12, fill="none", stroke=solid(t, "you"), r=12, width=3)


def window(s: Sketch, x: float, y: float, w: float, h: float, title: str = "") -> None:
    """An app window: frame, title bar, three dots."""
    t = s.theme
    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{white(t)}" stroke="{t.muted}" stroke-width="1.3"/></g>')
    raw(s, f'<path d="M{x + 1:.1f},{y + 34:.1f} V{y + 12:.1f} Q{x + 1:.1f},{y + 1:.1f} {x + 12:.1f},{y + 1:.1f} H{x + w - 12:.1f} Q{x + w - 1:.1f},{y + 1:.1f} {x + w - 1:.1f},{y + 12:.1f} V{y + 34:.1f} Z" fill="{t.fill("grey")}"/>')
    s.line(x, y + 34, x + w, y + 34, colour=t.muted, width=1)
    for i, c in enumerate(("#ff6b6b", "#fcc419", "#51cf66")):
        raw(s, f'<circle cx="{x + 18 + i * 16:.1f}" cy="{y + 17:.1f}" r="5" fill="{c}"/>')
    if title:
        s.text(x + w / 2, y + 23, title, size=13, colour=t.dim)


def tiles(s: Sketch, x: float, y: float, w: float, h: float, *, value: str = "57", label: str = "Phyla", dim: set[int] | None = None, select_box: bool = False) -> None:
    """A dashboard's body in miniature: a card, a bar chart, a scatter."""
    t = s.theme
    pal = DATA if t.name == "light" else tuple(_mix(c, "#ffffff", 0.88) for c in DATA)
    lw = w * 0.42
    ch = h * 0.38
    rrect(s, x, y, lw, ch, fill=white(t), stroke=t.muted, r=8, width=1)
    if h > 130:
        s.text(x + 12, y + 20, label, size=12, anchor="start", colour=t.dim)
        s.text(x + 12, y + ch - 12, value, size=24, anchor="start", weight="bold")
    else:
        s.text(x + lw / 2, y + ch / 2 + 6, value, size=16, weight="bold")
    by, bh = y + ch + 8, h - ch - 8
    rrect(s, x, by, lw, bh, fill=white(t), stroke=t.muted, r=8, width=1)
    for i, v in enumerate((0.55, 0.85, 0.4, 0.7)):
        bw = lw / 9
        hh = (bh - 18) * v
        rrect(s, x + bw * (1 + 2 * i), by + bh - 9 - hh, bw, hh, fill=pal[i], r=2, width=0)
    sx, sw = x + lw + 8, w - lw - 8
    rrect(s, sx, y, sw, h, fill=white(t), stroke=t.muted, r=8, width=1)
    pts = ((0.2, 0.7), (0.3, 0.55), (0.42, 0.62), (0.5, 0.4), (0.62, 0.48), (0.7, 0.3), (0.8, 0.36), (0.35, 0.8), (0.75, 0.6), (0.58, 0.72), (0.25, 0.42))
    for i, (px, py) in enumerate(pts):
        op = 0.22 if dim and i in dim else 1
        raw(s, f'<circle cx="{sx + sw * px:.1f}" cy="{y + h * py:.1f}" r="{4.5 if h > 130 else 3.5}" fill="{pal[i % 3]}" fill-opacity="{op}"/>')
    if select_box:
        raw(s, f'<rect x="{sx + sw * 0.44:.1f}" y="{y + h * 0.22:.1f}" width="{sw * 0.42:.1f}" height="{h * 0.33:.1f}" fill="{solid(t, "you")}" fill-opacity="0.10" stroke="{solid(t, "you")}" stroke-width="2" stroke-dasharray="6 4"/>')


def dashboard(
    s: Sketch, x: float, y: float, w: float, h: float, title: str, *, tabs: tuple[str, ...] = ("Overview", "Community & Diversity", "…"),
    active: int = 1, value: str = "57", label: str = "Phyla", dim: set[int] | None = None, select_box: bool = False, search: bool = True, search_ring: bool = False, sub: str = "",
) -> None:
    """A dashboard as the app shows it: orange header with its icon, a tab strip, tiles."""
    t = s.theme
    panel(s, x, y, w, h, "dashboard", title, sub=sub)
    if search:
        icon_button(s, x + w - 26, y + 23, "magnify", ring=search_ring, size=28)
    ty = y + 46
    cx = x + 14
    for i, tab in enumerate(tabs):
        tw = 10 + len(tab) * 6.9
        s.text(cx + tw / 2, ty + 23, tab, size=13, colour=ink(t, "dashboard") if i == active else t.dim, weight="bold" if i == active else "normal")
        if i == active:
            s.line(cx, ty + 33, cx + tw, ty + 33, colour=solid(t, "dashboard"), width=3)
        cx += tw + 8
    s.line(x + 1, ty + 34, x + w - 1, ty + 34, colour=t.fill("grey"), width=1.4)
    tiles(s, x + 14, ty + 46, w - 28, h - 46 - 60, value=value, label=label, dim=dim, select_box=select_box)


def table_panel(
    s: Sketch, x: float, y: float, w: float, title: str, header: tuple[str, ...], body: list[tuple[str, ...]], widths: tuple[float, ...],
    *, picked: set[int] | None = None, note: str = "", key: str = "collection", mark_col: int | None = None,
) -> float:
    """A data collection as a small table. Picked rows tinted blue (your selection),
    the others dimmed; ``mark_col`` outlines one column (the link column). Returns the bottom."""
    t = s.theme
    h = 46 + 34 + 32 * len(body) + (36 if note else 8)
    panel(s, x, y, w, h, key, title)
    hy = y + 47
    rrect(s, x + 1.5, hy, w - 3, 33, fill=t.fill("grey"), r=0, width=0)
    cx = x + 18
    for cell, cw in zip(header, widths):
        s.text(cx, hy + 22, f"`{cell}`", size=14, anchor="start", colour=t.dim)
        cx += cw
    for i, row in enumerate(body):
        ry = hy + 33 + 32 * i
        on = picked is not None and i in picked
        if on:
            rrect(s, x + 1.5, ry, w - 3, 32, fill=solid(t, "you"), r=0, width=0, opacity=0.13)
        s.line(x + 1, ry + 32, x + w - 1, ry + 32, colour=t.fill("grey"), width=1)
        colour = t.ink if (on or not picked) else t.muted
        cx = x + 18
        for cell, cw in zip(row, widths):
            if cell:
                s.text(cx, ry + 21, cell if cell == "…" else f"`{cell}`", size=14, anchor="start", colour=colour)
            cx += cw
    if mark_col is not None:
        cx = x + 8 + sum(widths[:mark_col])
        rrect(s, cx, hy + 2, widths[mark_col] - 4, 33 + 32 * len(body) - 4, fill="none", stroke=solid(t, "link"), r=6, width=1.6, dash=True)
    if note:
        s.text(x + w / 2, y + h - 13, note, size=13, colour=t.dim)
    return y + h


def dc_row(s: Sketch, x: float, y: float, w: float, name: str, *, ico: str = "table") -> None:
    """A data collection as a row of the project's list."""
    t = s.theme
    rrect(s, x, y, w, 40, fill=white(t), stroke=edge(t, "collection"), r=8, width=1.3)
    if ico == "multiqc":
        s.glyph("multiqc", x + 22, y + 20, size=18)
    else:
        icon(s, ico, x + 22, y + 20, 18, solid(t, "collection"))
    s.text(x + 42, y + 25, f"`{name}`", size=14, anchor="start")


def link_line(s: Sketch, x1: float, y1: float, x2: float, y2: float, *, mid_icon: bool = False, at: float = 0.5) -> None:
    """A link: grey dashed connector, with the link icon on it."""
    t = s.theme
    s.arrow(x1, y1, x2, y2, dashed=True, colour=solid(t, "link"))
    if mid_icon:
        mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
        raw(s, f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="15" fill="{white(t)}" stroke="{solid(t, "link")}" stroke-width="1.4"/>')
        icon(s, "link-variant", mx, my, 18, solid(t, "link"))


def person(s: Sketch, cx: float, cy: float, size: float, key: str = "you", label: str = "") -> None:
    t = s.theme
    raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size / 2:.1f}" fill="{t.fill(key)}" stroke="{edge(t, key)}" stroke-width="1.4"/>')
    icon(s, "account", cx, cy + size * 0.03, size * 0.64, solid(t, key))
    if label:
        s.text(cx, cy + size / 2 + 20, label, size=14, colour=ink(t, key))


def bubble(s: Sketch, x: float, y: float, w: float, h: float, lines: tuple[str, ...], key: str = "you") -> None:
    """A comment: a speech bubble with its tail at the bottom left."""
    t = s.theme
    raw(
        s,
        f'<path d="M{x + 12:.1f},{y:.1f} H{x + w - 12:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + 12:.1f} V{y + h - 12:.1f} '
        f'Q{x + w:.1f},{y + h:.1f} {x + w - 12:.1f},{y + h:.1f} H{x + 40:.1f} L{x + 18:.1f},{y + h + 16:.1f} L{x + 24:.1f},{y + h:.1f} '
        f'H{x + 12:.1f} Q{x:.1f},{y + h:.1f} {x:.1f},{y + h - 12:.1f} V{y + 12:.1f} Q{x:.1f},{y:.1f} {x + 12:.1f},{y:.1f} Z" '
        f'fill="{white(t)}" stroke="{edge(t, key)}" stroke-width="1.6"/>',
    )
    icon(s, "comment-outline", x + 22, y + 24, 18, solid(t, key))
    for i, l in enumerate(lines):
        s.text(x + 40, y + 29 + i * 22, l, size=14, anchor="start", colour=t.ink if i == 0 else t.dim)


def folder(s: Sketch, x: float, y: float, w: float, h: float, title: str, lines: tuple[str, ...] = (), key: str = "run", logo: str = "") -> None:
    """A run folder: a card with the run icon, in the run colour. ``logo``, a
    base64 SVG, replaces the icon with the pipeline's own mark (nf-core)."""
    t = s.theme
    rrect(s, x, y, w, h, fill=t.fill(key), stroke=edge(t, key), r=10, width=1.6)
    if logo:
        raw(s, f'<image href="data:image/svg+xml;base64,{logo}" x="{x + 16:.1f}" y="{y + 12:.1f}" width="20" height="31" preserveAspectRatio="xMidYMid meet"/>')
    else:
        icon(s, "folder-play-outline", x + 26, y + 27, 22, solid(t, key))
    s.text(x + 46, y + 33, title, size=16, anchor="start", weight="bold", colour=ink(t, key))
    for i, l in enumerate(lines):
        s.text(x + 46, y + 56 + i * 20, l, size=13, anchor="start", colour=t.dim)


def version_dot(s: Sketch, cx: float, cy: float, label: str, *, on: bool = False, r: float = 15) -> None:
    t = s.theme
    raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{solid(t, "version") if on else white(t)}" stroke="{solid(t, "version")}" stroke-width="2"/>')
    if label:
        s.text(cx, cy + 5, label, size=13, weight="bold", colour=("#000000" if t.name == "light" else t.bg) if on else ink(t, "version"))


def note(s: Sketch, x: float, y: float, lines: tuple[str, ...], *, key: str | None = None, anchor: str = "start") -> None:
    """Annotation text; the first line in a concept's colour and bold when ``key`` is set."""
    t = s.theme
    for i, l in enumerate(lines):
        s.text(x, y + i * 21, l, size=14, anchor=anchor, colour=(ink(t, key) if key and i == 0 else t.dim), weight="bold" if key and i == 0 else "normal")


def legend(theme: Theme) -> Sketch:
    """The key: each concept with the app's colour and icon."""
    s = Sketch(1380, 230, theme=theme, clean=True)
    shadow_defs(s)
    s.heading(46, 50, "Depictio's words, in the app's colours and icons", "Projects teal and Dashboards orange, as in the sidebar; a table data collection teal; versions yellow; links have no colour")
    items = (
        ("project", "Project"),
        ("run", "Run"),
        ("collection", "Data collection"),
        ("link", "Link"),
        ("dashboard", "Dashboard"),
        ("version", "Version"),
        ("you", "You"),
    )
    for i, (key, name) in enumerate(items):
        x = 46 + i * 190
        rrect(s, x, 110, 170, 92, fill=theme.fill(key), stroke=edge(theme, key), r=12, width=1.6)
        icon(s, ICONS[key], x + 85, 143, 32, solid(theme, key))
        s.text(x + 85, 188, name, size=16, colour=ink(theme, key), weight="bold")
    return s


if __name__ == "__main__":
    write_themed(legend, Path(__file__).resolve().parents[2] / "docs" / "images" / "data-model", "concepts")
