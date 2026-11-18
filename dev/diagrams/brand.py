#!/usr/bin/env python3
"""The app's brand colours and the few card helpers the system figures share.

``architecture.py`` and ``security.py`` draw services, stores and checks rather
than the app's screens, so they colour them with depictio's ``brandColors``
(``packages/depictio-react-core/src/brandColors.ts``: purple, violet, blue, teal, green, yellow,
orange, pink, red) instead of the concept colours of ``concepts.py``. Each colour
is registered as a fill key of both palettes, so ``tint(t, "blue")`` and
``Box(..., "br_blue")`` resolve in light and dark alike. Drawn clean, like the
workshop figures.
"""

from __future__ import annotations

from concepts import _mix, icon, raw, rrect, shadow_defs, white
from mdi_icons import MDI
from sketch import DARK, LIGHT, Sketch, Theme

BRAND: dict[str, str] = {
    "purple": "#9966CC",
    "violet": "#7A5DC7",
    "blue": "#6495ED",
    "teal": "#45B8AC",
    "green": "#8BC34A",
    "yellow": "#F9CB40",
    "orange": "#F68B33",
    "pink": "#E6779F",
    "red": "#E53935",
    "grey": "#868e96",
}
for _name, _c in BRAND.items():
    LIGHT.fills[f"br_{_name}"] = _mix(_c, "#ffffff", 0.12)
    DARK.fills[f"br_{_name}"] = _mix(_c, DARK.bg, 0.22)

# Icons the shared set does not carry, from mkdocs-material's bundled MDI.
MDI.update({
    "api": "M7 7H5a2 2 0 0 0-2 2v8h2v-4h2v4h2V9a2 2 0 0 0-2-2m0 4H5V9h2m7-2h-4v10h2v-4h2a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2m0 4h-2V9h2m6 0v6h1v2h-4v-2h1V9h-1V7h4v2Z",
    "monitor-dashboard": "M21 16V4H3v12zm0-14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-7v2h2v2H8v-2h2v-2H3a2 2 0 0 1-2-2V4c0-1.11.89-2 2-2zM5 6h9v5H5zm10 0h4v2h-4zm4 3v5h-4V9zM5 12h4v2H5zm5 0h4v2h-4z",
    "cog-sync-outline": "M11.7 20h-.4l-.4-2.6c-1.2-.2-2.2-.9-3-1.8l-2.4 1-.8-1.3 2.1-1.6q-.6-1.8 0-3.6L4.7 8.7l.8-1.3 2.4 1q1.2-1.35 3-1.8l.3-2.6h1.5l.4 2.6c1.2.2 2.3.9 3 1.8l2.4-1 .8 1.3-2.1 1.5q.3.9.3 1.8h.5c.5 0 1 .1 1.5.2V12l-.1-1 2.1-1.6c.2-.2.2-.4.1-.6l-2-3.5c-.1-.3-.3-.3-.6-.3l-2.5 1c-.5-.4-1.1-.7-1.7-1l-.4-2.7c.1-.1-.2-.3-.4-.3h-4c-.2 0-.5.2-.5.4l-.4 2.7c-.6.2-1.1.6-1.7.9L5 5c-.3 0-.5 0-.7.3l-2 3.5c-.1.2 0 .4.2.6L4.6 11l-.1 1 .1 1-2.1 1.7c-.2.2-.2.4-.1.6l2 3.5c.1.2.3.2.6.2l2.5-1c.5.4 1.1.7 1.7 1l.4 2.7c0 .2.2.4.5.4h2.5c-.5-.7-.7-1.4-.9-2.1m4.3-7.7V12c0-2.2-1.8-4-4-4s-4 1.8-4 4 1.8 4 4 4c.7-1.7 2.2-3.1 4-3.7m-6-.3c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2m8 2.5V13l-2.2 2.2 2.2 2.2V16c1.4 0 2.5 1.1 2.5 2.5 0 .4-.1.8-.3 1.1l1.1 1.1c1.2-1.8.7-4.3-1.1-5.5-.6-.5-1.4-.7-2.2-.7m0 6.5c-1.4 0-2.5-1.1-2.5-2.5 0-.4.1-.8.3-1.1l-1.1-1.1c-1.2 1.8-.7 4.3 1.1 5.5.7.4 1.4.7 2.2.7V24l2.2-2.2-2.2-2.3z",
    "bucket-outline": "M3 4h18v3h-1l-2.5 14h-11L4 7H3zm14.97 3H6.03l2.12 12h7.7z",
    "memory": "M17 17H7V7h10m4 4V9h-2V7a2 2 0 0 0-2-2h-2V3h-2v2h-2V3H9v2H7c-1.11 0-2 .89-2 2v2H3v2h2v2H3v2h2v2a2 2 0 0 0 2 2h2v2h2v-2h2v2h2v-2h2a2 2 0 0 0 2-2v-2h2v-2h-2v-2m-6 2h-2v-2h2m2-2H9v6h6z",
    "shield-account-outline": "M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5zm0 2.18 7 3.12v4.92c0 1.7-.5 3.43-1.35 4.95C16 14.94 13.26 14.5 12 14.5s-4 .44-5.65 1.67C5.5 14.65 5 12.92 5 11.22V6.3zM12 6a3.5 3.5 0 0 0-3.5 3.5A3.5 3.5 0 0 0 12 13a3.5 3.5 0 0 0 3.5-3.5A3.5 3.5 0 0 0 12 6m0 2a1.5 1.5 0 0 1 1.5 1.5A1.5 1.5 0 0 1 12 11a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 12 8m0 8.5c1.57 0 3.64.61 4.53 1.34C15.29 19.38 13.7 20.55 12 21c-1.7-.45-3.29-1.62-4.53-3.16.9-.73 2.96-1.34 4.53-1.34",
    "earth": "M17.9 17.39c-.26-.8-1.01-1.39-1.9-1.39h-1v-3a1 1 0 0 0-1-1H8v-2h2a1 1 0 0 0 1-1V7h2a2 2 0 0 0 2-2v-.41a7.984 7.984 0 0 1 2.9 12.8M11 19.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.22.21-1.79L9 15v1a2 2 0 0 0 2 2m1-16A10 10 0 0 0 2 12a10 10 0 0 0 10 10 10 10 0 0 0 10-10A10 10 0 0 0 12 2",
    "lightning-bolt": "M11 15H6l7-14v8h5l-7 14z",
    "camera-outline": "M20 4h-3.17L15 2H9L7.17 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2m0 14H4V6h4.05l1.83-2h4.24l1.83 2H20zM12 7a5 5 0 0 0-5 5 5 5 0 0 0 5 5 5 5 0 0 0 5-5 5 5 0 0 0-5-5m0 8a3 3 0 0 1-3-3 3 3 0 0 1 3-3 3 3 0 0 1 3 3 3 3 0 0 1-3 3",
    "database-import-outline": "m8.84 12-4.92 4.92L2.5 15.5 5 13H0v-2h5L2.5 8.5l1.42-1.42zM12 3C8.59 3 5.68 4.07 4.53 5.57L5 6l1.03 1.07C6 7.05 6 7 6 7c0-.5 2.13-2 6-2s6 1.5 6 2-2.13 2-6 2c-2.62 0-4.42-.69-5.32-1.28l3.12 3.12c.7.1 1.44.16 2.2.16 2.39 0 4.53-.53 6-1.36v2.81c-1.3.95-3.58 1.55-6 1.55-.96 0-1.9-.1-2.76-.27l-1.65 1.64c1.32.4 2.82.63 4.41.63 2.28 0 4.39-.45 6-1.23V17c0 .5-2.13 2-6 2s-6-1.5-6-2v-.04L5 18l-.46.43C5.69 19.93 8.6 21 12 21c4.41 0 8-1.79 8-4V7c0-2.21-3.58-4-8-4",
    "login": "M11 7 9.6 8.4l2.6 2.6H2v2h10.2l-2.6 2.6L11 17l5-5zm9 12h-8v2h8c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-8v2h8z",
    "shield-check-outline": "M21 11c0 5.55-3.84 10.74-9 12-5.16-1.26-9-6.45-9-12V5l9-4 9 4zm-9 10c3.75-1 7-5.46 7-9.78V6.3l-7-3.12L5 6.3v4.92C5 15.54 8.25 20 12 21m-2-4-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9",
    "cancel": "M12 2c5.5 0 10 4.5 10 10s-4.5 10-10 10S2 17.5 2 12 6.5 2 12 2m0 2c-1.9 0-3.6.6-4.9 1.7l11.2 11.2c1-1.4 1.7-3.1 1.7-4.9 0-4.4-3.6-8-8-8m4.9 14.3L5.7 7.1C4.6 8.4 4 10.1 4 12c0 4.4 3.6 8 8 8 1.9 0 3.6-.6 4.9-1.7",
    "account-group-outline": "M12 5a3.5 3.5 0 0 0-3.5 3.5A3.5 3.5 0 0 0 12 12a3.5 3.5 0 0 0 3.5-3.5A3.5 3.5 0 0 0 12 5m0 2a1.5 1.5 0 0 1 1.5 1.5A1.5 1.5 0 0 1 12 10a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 12 7M5.5 8A2.5 2.5 0 0 0 3 10.5c0 .94.53 1.75 1.29 2.18.36.2.77.32 1.21.32s.85-.12 1.21-.32c.37-.21.68-.51.91-.87A5.42 5.42 0 0 1 6.5 8.5v-.28c-.3-.14-.64-.22-1-.22m13 0c-.36 0-.7.08-1 .22v.28c0 1.2-.39 2.36-1.12 3.31.12.19.25.34.4.49a2.482 2.482 0 0 0 1.72.7c.44 0 .85-.12 1.21-.32.76-.43 1.29-1.24 1.29-2.18A2.5 2.5 0 0 0 18.5 8M12 14c-2.34 0-7 1.17-7 3.5V19h14v-1.5c0-2.33-4.66-3.5-7-3.5m-7.29.55C2.78 14.78 0 15.76 0 17.5V19h3v-1.93c0-1.01.69-1.85 1.71-2.52m14.58 0c1.02.67 1.71 1.51 1.71 2.52V19h3v-1.5c0-1.74-2.78-2.72-4.71-2.95M12 16c1.53 0 3.24.5 4.23 1H7.77c.99-.5 2.7-1 4.23-1",
    "arrow-decision-outline": "M9.64 13.4C8.63 12.5 7.34 12.03 6 12v3l-4-4 4-4v3c1.67 0 3.3.57 4.63 1.59a8 8 0 0 0-.99 1.81M18 15v-3c-.5 0-4.5.16-4.95 4.2 1.56.55 2.38 2.27 1.83 3.83a3.006 3.006 0 0 1-3.83 1.83c-1.55-.56-2.38-2.27-1.83-3.83.28-.86.98-1.53 1.83-1.83A6.75 6.75 0 0 1 18 10V7l4 4zm-5 4a1 1 0 0 0-1-1 1 1 0 0 0-1 1 1 1 0 0 0 1 1 1 1 0 0 0 1-1m-2-7.88c.58-.66 1.25-1.23 2-1.69V5h3l-4-4-4 4h3z",
    "refresh": "M17.65 6.35A7.96 7.96 0 0 0 12 4a8 8 0 0 0-8 8 8 8 0 0 0 8 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 12 18a6 6 0 0 1-6-6 6 6 0 0 1 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z",
    "cellphone-arrow-down": "M17 1H7a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2m0 18H7V5h10zm-1-6h-3V8h-2v5H8l4 4z",
    "broadcast": "M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2m6 2c0-3.3-2.7-6-6-6s-6 2.7-6 6c0 2.2 1.2 4.1 3 5.2l1-1.7c-1.2-.7-2-2-2-3.4 0-2.2 1.8-4 4-4s4 1.8 4 4c0 1.5-.8 2.8-2 3.4l1 1.7c1.8-1 3-3 3-5.2M12 2C6.5 2 2 6.5 2 12c0 3.7 2 6.9 5 8.6l1-1.7c-2.4-1.4-4-4-4-6.9 0-4.4 3.6-8 8-8s8 3.6 8 8c0 3-1.6 5.5-4 6.9l1 1.7c3-1.7 5-4.9 5-8.6 0-5.5-4.5-10-10-10",
    "access-point-network": "M4.93 3.93A9.97 9.97 0 0 0 2 11c0 2.76 1.12 5.26 2.93 7.07l1.41-1.41A7.94 7.94 0 0 1 4 11c0-2.21.89-4.22 2.34-5.66zm14.14 0-1.41 1.41A7.96 7.96 0 0 1 20 11c0 2.22-.89 4.22-2.34 5.66l1.41 1.41A9.97 9.97 0 0 0 22 11c0-2.76-1.12-5.26-2.93-7.07M7.76 6.76A5.98 5.98 0 0 0 6 11c0 1.65.67 3.15 1.76 4.24l1.41-1.41A4 4 0 0 1 8 11c0-1.11.45-2.11 1.17-2.83zm8.48 0-1.41 1.41A4 4 0 0 1 16 11c0 1.11-.45 2.11-1.17 2.83l1.41 1.41A5.98 5.98 0 0 0 18 11c0-1.65-.67-3.15-1.76-4.24M12 9a2 2 0 0 0-2 2 2 2 0 0 0 2 2 2 2 0 0 0 2-2 2 2 0 0 0-2-2m-1 6v4h-1a1 1 0 0 0-1 1H2v2h7a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1h7v-2h-7a1 1 0 0 0-1-1h-1v-4z",
    "radio-tower": "M12 10a2 2 0 0 1 2 2 2 2 0 0 1-.47 1.29L16.7 22h-2.13L12 14.93 9.43 22H7.3l3.17-8.71A2 2 0 0 1 10 12a2 2 0 0 1 2-2m0-2a4 4 0 0 0-4 4c0 .5.1 1 .28 1.46l-.88 2.4A6.03 6.03 0 0 1 6 12a6 6 0 0 1 6-6 6 6 0 0 1 6 6c0 1.47-.53 2.81-1.4 3.86l-.88-2.4C15.9 13 16 12.5 16 12a4 4 0 0 0-4-4m0-4a8 8 0 0 0-8 8c0 2.36 1 4.5 2.64 5.94l-.72 2A10 10 0 0 1 2 12 10 10 0 0 1 12 2a10 10 0 0 1 10 10c0 3.23-1.54 6.11-3.92 7.94l-.72-2C19 16.5 20 14.36 20 12a8 8 0 0 0-8-8",
    "cloud-upload-outline": "M6.5 20q-2.28 0-3.89-1.57Q1 16.85 1 14.58q0-1.95 1.17-3.48 1.18-1.53 3.08-1.95.63-2.3 2.5-3.72Q9.63 4 12 4q2.93 0 4.96 2.04Q19 8.07 19 11q1.73.2 2.86 1.5 1.14 1.28 1.14 3 0 1.88-1.31 3.19T18.5 20H13q-.82 0-1.41-.59Q11 18.83 11 18v-5.15L9.4 14.4 8 13l4-4 4 4-1.4 1.4-1.6-1.55V18h5.5q1.05 0 1.77-.73.73-.72.73-1.77t-.73-1.77Q19.55 13 18.5 13H17v-2q0-2.07-1.46-3.54Q14.08 6 12 6 9.93 6 8.46 7.46 7 8.93 7 11h-.5q-1.45 0-2.47 1.03Q3 13.05 3 14.5T4.03 17q1.02 1 2.47 1H9v2m3-7",
    "language-python": "M19.14 7.5A2.86 2.86 0 0 1 22 10.36v3.78A2.86 2.86 0 0 1 19.14 17H12c0 .39.32.96.71.96H17v1.68a2.86 2.86 0 0 1-2.86 2.86H9.86A2.86 2.86 0 0 1 7 19.64v-3.75a2.85 2.85 0 0 1 2.86-2.85h5.25a2.85 2.85 0 0 0 2.85-2.86V7.5zm-4.28 11.79c-.4 0-.72.3-.72.89s.32.71.72.71a.71.71 0 0 0 .71-.71c0-.59-.32-.89-.71-.89m-10-1.79A2.86 2.86 0 0 1 2 14.64v-3.78A2.86 2.86 0 0 1 4.86 8H12c0-.39-.32-.96-.71-.96H7V5.36A2.86 2.86 0 0 1 9.86 2.5h4.28A2.86 2.86 0 0 1 17 5.36v3.75a2.85 2.85 0 0 1-2.86 2.85H8.89a2.85 2.85 0 0 0-2.85 2.86v2.68zM9.14 5.71c.4 0 .72-.3.72-.89s-.32-.71-.72-.71c-.39 0-.71.12-.71.71s.32.89.71.89",
    "file-document-check-outline": "m23.5 17-5 5-3.5-3.5 1.5-1.5 2 2 3.5-3.5zM6 2a2 2 0 0 0-2 2v16c0 1.11.89 2 2 2h7.81c-.36-.62-.61-1.3-.73-2H6V4h7v5h5v4.08c.33-.05.67-.08 1-.08.34 0 .67.03 1 .08V8l-6-6M8 12v2h8v-2m-8 4v2h5v-2Z",
})


def _c(key: str) -> str:
    return BRAND[key]


def tint(t: Theme, key: str) -> str:
    return t.fill(f"br_{key}")


def solid(t: Theme, key: str) -> str:
    return _c(key) if t.name == "light" else _mix(_c(key), "#ffffff", 0.88)


def edge(t: Theme, key: str) -> str:
    return _mix(_c(key), "#ffffff", 0.6) if t.name == "light" else _mix(_c(key), t.bg, 0.6)


def ink(t: Theme, key: str) -> str:
    """Text in the colour: darkened on white (yellow and green further), lifted on slate."""
    if t.name == "light":
        return _mix(_c(key), "#000000", 0.5 if key in ("yellow", "green") else 0.68)
    return _mix(_c(key), "#ffffff", 0.78)


def fg_on(t: Theme) -> str:
    return "#ffffff" if t.name == "light" else t.bg


def new(theme: Theme, w: float, h: float, title: str, subtitle: str) -> Sketch:
    """A clean canvas with the workshop's bold title and dimmed subtitle."""
    s = Sketch(w, h, theme=theme, clean=True)
    shadow_defs(s)
    s.text(30, 44, title, size=24, anchor="start", weight="bold")
    s.text(30, 70, subtitle, size=15, anchor="start", colour=theme.dim)
    return s


def panel(s: Sketch, x: float, y: float, w: float, h: float, key: str, title: str, ico: str, *, header: float = 44, dashed: bool = False, tag: str = "") -> None:
    """A white card whose header band is tinted; dashed when the part is optional."""
    t = s.theme
    f = ' filter="url(#sh)"' if t.name == "light" and not dashed else ""
    d = ' stroke-dasharray="7 5"' if dashed else ""
    raw(s, f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{white(t)}" stroke="{edge(t, key)}" stroke-width="1.6"{d}/></g>')
    raw(s, f'<path d="M{x + 1:.1f},{y + header:.1f} V{y + 12:.1f} Q{x + 1:.1f},{y + 1:.1f} {x + 12:.1f},{y + 1:.1f} H{x + w - 12:.1f} Q{x + w - 1:.1f},{y + 1:.1f} {x + w - 1:.1f},{y + 12:.1f} V{y + header:.1f} Z" fill="{tint(t, key)}"/>')
    s.line(x, y + header, x + w, y + header, colour=edge(t, key), width=1.2)
    icon(s, ico, x + 26, y + header / 2, 21, solid(t, key))
    s.text(x + 46, y + header / 2 + 6, title, size=16, anchor="start", weight="bold", colour=ink(t, key))
    if tag:
        s.text(x + w - 14, y + header / 2 + 5, tag, size=12, anchor="end", colour=t.dim)


def card(s: Sketch, x: float, y: float, w: float, h: float, key: str, ico: str, title: str, lines: tuple[str, ...] = (), *, dashed: bool = False, size: float = 14) -> None:
    """A tinted card: icon and bold title on the first line, dimmed lines under it."""
    t = s.theme
    rrect(s, x, y, w, h, fill=tint(t, key), stroke=edge(t, key), r=12, width=1.5, dash=dashed)
    icon(s, ico, x + 24, y + 25, 21, solid(t, key))
    s.text(x + 44, y + 31, title, size=16, anchor="start", weight="bold", colour=ink(t, key))
    for i, line in enumerate(lines):
        s.text(x + 16, y + 56 + i * 20, line, size=size, anchor="start", colour=t.dim)


def lines(s: Sketch, x: float, y: float, rows: tuple[str, ...], *, size: float = 14, step: float = 20, first_bold: bool = False, colour: str | None = None) -> None:
    t = s.theme
    for i, r in enumerate(rows):
        bold = first_bold and i == 0
        s.text(x, y + i * step, r, size=size, anchor="start", colour=t.ink if bold else (colour or t.dim), weight="bold" if bold else "normal")


def badge(s: Sketch, cx: float, cy: float, label: str, key: str, r: float = 12) -> None:
    t = s.theme
    raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{solid(t, key)}"/>')
    s.text(cx, cy + 4.5, label, size=13, colour=fg_on(t), weight="bold")


def chip(s: Sketch, x: float, y: float, w: float, text: str, key: str, *, ico: str | None = None, dashed: bool = False, h: float = 28) -> None:
    t = s.theme
    rrect(s, x, y, w, h, fill=tint(t, key), stroke=edge(t, key), r=h / 2, width=1.2, dash=dashed)
    if ico:
        icon(s, ico, x + 17, y + h / 2, 15, solid(t, key))
        s.text(x + 30, y + h / 2 + 4.5, text, size=13, anchor="start", colour=ink(t, key))
    else:
        s.text(x + w / 2, y + h / 2 + 4.5, text, size=13, colour=ink(t, key))


def path_arrow(s: Sketch, points: list[tuple[float, float]], *, colour: str, dashed: bool = False, width: float = 1.6) -> None:
    """An elbowed connector: straight segments, an arrowhead on the last one."""
    for (x1, y1), (x2, y2) in zip(points[:-2], points[1:-1]):
        s.line(x1, y1, x2, y2, colour=colour, dashed=dashed, width=width)
    (x1, y1), (x2, y2) = points[-2], points[-1]
    s.arrow(x1, y1, x2, y2, colour=colour, dashed=dashed)
