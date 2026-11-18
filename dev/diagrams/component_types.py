#!/usr/bin/env python3
"""Component types in the app's colours and icons, shared by the dashboard figures.

Read from depictio v1.21.0, ``packages/depictio-react-core/src/componentTypeMeta.ts``
(``COMPONENT_TYPE_VISUALS``) and ``brandColors.ts``: a figure is purple with
``mdi:graph-box``, a card teal with ``formkit:number``, an interactive green with
``bx:slider-alt``, a table blue with ``octicon:table-24``, MultiQC its own logo,
an image pink, a map violet, a genome browser yellow, text ``#E91E63`` and an
advanced visualization ``#D6336C``.

Importing this module registers each type as a concept key (``"c_figure"``,
``"c_card"``...), so the helpers of concepts.py (``ink``, ``solid``, ``edge``,
``t.fill``) work on them as they do on a project or a link.
"""

from __future__ import annotations

from concepts import CONCEPTS, _ink, _mix, edge, fg_on, icon, ink, raw, rrect, solid, white
from mdi_icons import MDI
from sketch import DARK, LIGHT, Sketch

# (accent, icon, label), in the order of the builder's type grid.
TYPES: dict[str, tuple[str, str, str]] = {
    "figure": ("#9966CC", "graph-box", "Figure"),
    "card": ("#45B8AC", "formkit:number", "Card"),
    "interactive": ("#8BC34A", "bx:slider-alt", "Interactive"),
    "table": ("#6495ED", "octicon:table-24", "Table"),
    "multiqc": ("#F68B33", "multiqc", "MultiQC"),
    "image": ("#E6779F", "image-area", "Image"),
    "map": ("#7A5DC7", "map-marker-multiple", "Map"),
    "jbrowse": ("#F9CB40", "dna", "Genome browser"),
    "text": ("#E91E63", "text-box-outline", "Text"),
    "advanced_viz": ("#D6336C", "chart-scatter-plot", "Advanced viz"),
}

for _kind, (_c, _ico, _label) in TYPES.items():
    _key = f"c_{_kind}"
    CONCEPTS[_key] = _c
    LIGHT.fills[_key] = _mix(_c, "#ffffff", 0.10)
    DARK.fills[_key] = _mix(_c, DARK.bg, 0.22)
    LIGHT.inks[_key] = _ink("light", _key)
    DARK.inks[_key] = _ink("dark", _key)

# Icons the shared set does not carry, from mkdocs-material's bundled MDI.
MDI.update({
    "ruler": "m1.39 18.36 1.77-1.76L4.58 18l1.06-1.05-1.42-1.41 1.42-1.42 2.47 2.48 1.06-1.06-2.47-2.48 1.41-1.41 1.42 1.41L10.59 12l-1.42-1.41 1.42-1.42 2.47 2.48 1.06-1.06-2.47-2.48 1.41-1.41 1.41 1.41 1.07-1.06-1.42-1.41 1.42-1.42L18 6.7l1.07-1.06-2.47-2.48 1.76-1.77 4.25 4.25L5.64 22.61z",
    "flower-outline": "M8.66 13.07c-1.74 0-3.16-1.41-3.16-3.14 0-.71.26-1.39.69-1.93-.42-.54-.69-1.22-.69-1.93 0-1.73 1.43-3.14 3.16-3.14l.43.03A3.15 3.15 0 0 1 12 1c1.31 0 2.44.81 2.91 1.96l.43-.03c1.73 0 3.16 1.41 3.16 3.14 0 .71-.26 1.39-.69 1.93.42.54.69 1.22.69 1.93 0 1.73-1.43 3.14-3.16 3.14l-.43-.03A3.15 3.15 0 0 1 12 15a3.15 3.15 0 0 1-2.91-1.96zM12 13c.62 0 1.12-.5 1.14-1.1l-.11-1.09c-.32.12-.67.19-1.03.19s-.7-.07-1-.19l-.14 1.09c.02.6.52 1.1 1.14 1.1m3.34-1.93c.63 0 1.16-.51 1.16-1.15 0-.42-.27-.84-.67-1.03l-.88-.42c-.12.74-.51 1.38-1.06 1.83l.81.57c.18.13.4.2.64.2m-.65-5.94-.82.56c.56.45.95 1.09 1.07 1.81l.88-.4c.41-.2.68-.6.68-1.03 0-.63-.53-1.14-1.16-1.14-.23 0-.45.07-.65.2M12 3c-.62 0-1.12.5-1.14 1.1L11 5.19c.3-.12.64-.19 1-.19s.71.07 1.03.19l.11-1.09C13.12 3.5 12.62 3 12 3M8.66 4.93c-.63 0-1.16.51-1.16 1.14 0 .43.27.83.67 1.03l.88.4c.12-.72.51-1.36 1.06-1.81l-.81-.56c-.18-.13-.4-.2-.64-.2M8.17 8.9c-.4.2-.67.6-.67 1.02 0 .63.53 1.14 1.16 1.14.23 0 .45-.06.65-.2l.81-.55c-.56-.45-.95-1.09-1.07-1.81zM12 22a9 9 0 0 1-9-9 9 9 0 0 1 9 9 9 9 0 0 1 9-9 9 9 0 0 1-9 9m2.44-2.44a7.04 7.04 0 0 0 4.12-4.12c-1.9.7-3.41 2.22-4.12 4.12m-9-4.12a7.04 7.04 0 0 0 4.12 4.12c-.7-1.9-2.22-3.41-4.12-4.12",
    "leaf": "M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66.95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75C7 8 17 8 17 8",
    "chevron-down": "M7.41 8.58 12 13.17l4.59-4.59L18 10l-6 6-6-6z",
    "selection-drag": "M14 17h3v-3h2v3h3v2h-3v3h-2v-3h-3zm-2 0v2H9v-2zm-5 0v2H3v-4h2v2zm-4-4v-3h2v3zm0-5V4h4v2H5v2zm6-4h3v2H9zm6 0h4v4h-2V6h-2zm4 6v2h-2v-2z",
    "checkbox-marked": "m10 17-5-5 1.41-1.42L10 14.17l7.59-7.59L19 8m0-5H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2",
    "checkbox-blank-outline": "M19 3H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m0 2v14H5V5z",
    "filter-cog-outline": "m22.77 19.32-1.07-.82c.02-.17.04-.33.04-.5s-.01-.33-.04-.5l1.06-.82a.26.26 0 0 0 .06-.32l-1-1.73c-.06-.13-.19-.13-.32-.13l-1.23.5c-.27-.18-.54-.35-.85-.47l-.19-1.32A.236.236 0 0 0 19 13h-2a.26.26 0 0 0-.26.21l-.19 1.32c-.3.13-.59.29-.85.47l-1.24-.5c-.11 0-.24 0-.31.13l-1 1.73c-.06.11-.04.24.06.32l1.06.82a4.2 4.2 0 0 0 0 1l-1.06.82a.26.26 0 0 0-.06.32l1 1.73c.06.13.19.13.31.13l1.24-.5c.26.18.54.35.85.47l.19 1.32c.02.12.12.21.26.21h2c.11 0 .22-.09.24-.21l.19-1.32c.3-.13.57-.29.84-.47l1.23.5c.13 0 .26 0 .33-.13l1-1.73a.26.26 0 0 0-.06-.32M18 19.5c-.84 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5m-.38-16.28c-.19-.14-.4-.22-.62-.22H3c-.22 0-.43.08-.62.22a1 1 0 0 0-.17 1.4L7 10.75v5.12c-.04.29.06.6.29.83l4.01 4.01c.1.1.2.17.35.22C11.22 20 11 19 11 18c0-1.83.72-3.59 2-4.9v-2.35l4.79-6.13a1 1 0 0 0-.17-1.4M11 10.05v7.53l-2-2v-5.52L5.04 5h9.92z",
})


def key(kind: str) -> str:
    return f"c_{kind}"


def type_icon(s: Sketch, kind: str, cx: float, cy: float, size: float, colour: str | None = None) -> None:
    """The type's icon in its colour; MultiQC draws its logo instead."""
    _c, ico, _label = TYPES[kind]
    if ico == "multiqc":
        s.glyph("multiqc", cx, cy, size=size)
    else:
        icon(s, ico, cx, cy, size, colour or solid(s.theme, key(kind)))


def type_badge(s: Sketch, kind: str, cx: float, cy: float, size: float = 30) -> None:
    """The coloured square the builder's type grid draws behind a type's icon."""
    if kind == "multiqc":
        s.glyph("multiqc", cx, cy, size=size * 0.9)
        return
    rrect(s, cx - size / 2, cy - size / 2, size, size, fill=solid(s.theme, key(kind)), r=size * 0.28, width=0)
    type_icon(s, kind, cx, cy, size * 0.6, fg_on(s.theme))


def tile(s: Sketch, kind: str, x: float, y: float, w: float, h: float, title: str, *, sub: str = "", header: float = 40, shadow: bool = True) -> None:
    """A component on the canvas: a white card whose header carries its type's badge and colour."""
    t = s.theme
    k = key(kind)
    f = ' filter="url(#sh)"' if shadow and t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="{white(t)}" stroke="{edge(t, k)}" stroke-width="1.6"/></g>')
    raw(s, f'<path d="M{x + 1:.1f},{y + header:.1f} V{y + 10:.1f} Q{x + 1:.1f},{y + 1:.1f} {x + 10:.1f},{y + 1:.1f} H{x + w - 10:.1f} Q{x + w - 1:.1f},{y + 1:.1f} {x + w - 1:.1f},{y + 10:.1f} V{y + header:.1f} Z" fill="{t.fill(k)}"/>')
    s.line(x, y + header, x + w, y + header, colour=edge(t, k), width=1.1)
    type_badge(s, kind, x + 22, y + header / 2, 24)
    s.text(x + 42, y + header / 2 + 6, title, size=15, anchor="start", weight="bold", colour=ink(t, k))
    if sub:
        s.text(x + w - 12, y + header / 2 + 5, sub, size=13, anchor="end", colour=t.dim)
