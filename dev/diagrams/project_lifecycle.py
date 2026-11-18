#!/usr/bin/env python3
"""The project lifecycle on the Projects overview page.

    uv run python dev/diagrams/project_lifecycle.py

Writes ``docs/images/guides/project-creation/project-lifecycle_{light,dark}.{svg,png}``.

Four steps read left to right (create, ingest, dashboards, share), then the loop
every new run goes through: Add data, a new data version, and What's new on the
dashboards. Labels are the app's own at v1.21.0 (``Add data``, ``Read in place``,
``Import a project``, ``Send to another instance``, ``Create a template``).

Drawn clean, like the workshop figures: the colours and icons are the ones the
app gives each concept (projects and tables teal, dashboards orange, runs and
versions yellow, what the user does blue). The few helpers below mirror
``concepts.py``, kept local so this figure does not change when that file does.
"""

from __future__ import annotations

from pathlib import Path

from mdi_icons import MDI
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "project-creation"

CONCEPTS: dict[str, str] = {
    "project": "#12b886",  # teal: Projects in the sidebar
    "collection": "#12b886",  # teal: a table data collection
    "dashboard": "#fd7e14",  # orange: Dashboards in the sidebar
    "run": "#fab005",  # yellow: a run folder
    "you": "#228be6",  # blue: the app's primary colour
    "people": "#868e96",  # grey
}


def _mix(a: str, b: str, t: float) -> str:
    pa = [int(a[i : i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02x}" for x, y in zip(pa, pb))


def ink(t: Theme, key: str) -> str:
    c = CONCEPTS[key]
    if t.name == "light":
        return _mix(c, "#000000", 0.62 if c == "#fab005" else 0.8)
    return _mix(c, "#ffffff", 0.78)


def solid(t: Theme, key: str) -> str:
    c = CONCEPTS[key]
    return c if t.name == "light" else _mix(c, "#ffffff", 0.88)


def edge(t: Theme, key: str) -> str:
    c = CONCEPTS[key]
    return _mix(c, "#ffffff", 0.55) if t.name == "light" else _mix(c, t.bg, 0.6)


def tint(t: Theme, key: str) -> str:
    c = CONCEPTS[key]
    return _mix(c, "#ffffff", 0.10) if t.name == "light" else _mix(c, t.bg, 0.22)


def white(t: Theme) -> str:
    return t.fill("white")


def raw(s: Sketch, svg: str) -> None:
    s._parts.append(svg)


def icon(s: Sketch, name: str, cx: float, cy: float, size: float, colour: str) -> None:
    k = size / 24
    raw(s, f'<path transform="translate({cx - 12 * k:.1f},{cy - 12 * k:.1f}) scale({k:.4f})" d="{MDI[name]}" fill="{colour}"/>')


def rrect(s: Sketch, x: float, y: float, w: float, h: float, *, fill: str, stroke: str = "none", r: float = 10, width: float = 1.4, dash: bool = False) -> None:
    d = ' stroke-dasharray="7 5"' if dash else ""
    raw(s, f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}/>')


def panel(s: Sketch, x: float, y: float, w: float, h: float, key: str, title: str, ico: str, *, header: float = 46) -> None:
    """A white card whose header band is tinted in the concept's colour."""
    t = s.theme
    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="{white(t)}" stroke="{edge(t, key)}" stroke-width="1.6"/></g>')
    raw(s, f'<path d="M{x + 1:.1f},{y + header:.1f} V{y + 12:.1f} Q{x + 1:.1f},{y + 1:.1f} {x + 12:.1f},{y + 1:.1f} H{x + w - 12:.1f} Q{x + w - 1:.1f},{y + 1:.1f} {x + w - 1:.1f},{y + 12:.1f} V{y + header:.1f} Z" fill="{tint(t, key)}"/>')
    s.line(x, y + header, x + w, y + header, colour=edge(t, key), width=1.2)
    icon(s, ico, x + 28, y + header / 2, 22, solid(t, key))
    s.text(x + 48, y + header / 2 + 6, title, size=18, anchor="start", weight="bold", colour=ink(t, key))


def badge(s: Sketch, cx: float, cy: float, label: str, key: str) -> None:
    t = s.theme
    raw(s, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="14" fill="{solid(t, key)}"/>')
    s.text(cx, cy + 5, label, size=15, colour="#ffffff" if t.name == "light" else t.bg, weight="bold")


def row(s: Sketch, x: float, y: float, ico: str, key: str, title: str, sub: str = "") -> None:
    """One line of a panel: an icon, a bold label and a dimmed detail under it."""
    t = s.theme
    icon(s, ico, x + 12, y - 5, 20, solid(t, key))
    s.text(x + 32, y, title, size=15, anchor="start", weight="bold")
    if sub:
        s.text(x + 32, y + 20, sub, size=13, anchor="start", colour=t.dim)


def chip(s: Sketch, x: float, y: float, w: float, text: str, key: str) -> None:
    t = s.theme
    rrect(s, x, y, w, 26, fill=tint(t, key), stroke=edge(t, key), r=13, width=1.2)
    s.text(x + w / 2, y + 18, text, size=12.5, colour=ink(t, key))


def card(s: Sketch, x: float, y: float, w: float, h: float, key: str, ico: str, title: str, lines: tuple[str, ...]) -> None:
    """A small card of the lower loop: tinted, with its icon and two lines."""
    t = s.theme
    rrect(s, x, y, w, h, fill=tint(t, key), stroke=edge(t, key), r=12, width=1.4)
    icon(s, ico, x + 26, y + 28, 22, solid(t, key))
    s.text(x + 46, y + 34, title, size=16, anchor="start", weight="bold", colour=ink(t, key))
    for i, line in enumerate(lines):
        s.text(x + 18, y + 62 + i * 20, line, size=13, anchor="start", colour=t.dim)


def lifecycle(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(1440, 660, theme=t, clean=True)
    raw(s, '<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-opacity="0.12"/></filter></defs>')
    s.text(40, 50, "A project's life", size=24, anchor="start", weight="bold")
    s.text(40, 76, "from its data to a shared dashboard, then again with every new run", size=15, anchor="start", colour=t.dim)

    top, h, w = 112, 286, 315
    xs = (40, 385, 730, 1075)

    # 1. Create
    x = xs[0]
    panel(s, x, top, w, h, "project", "Create", "jira")
    badge(s, x, top, "1", "project")
    row(s, x + 14, top + 82, "folder-plus-outline", "you", "New project, Add data", "Upload, or Read in place")
    for cx, cw, label in ((x + 18, 84, "Flat tables"), (x + 108, 118, "Custom workflows"), (x + 232, 70, "Template")):
        chip(s, cx, top + 118, cw, label, "project")
    row(s, x + 14, top + 182, "file-import-outline", "you", "Import a project", "a ZIP, or one sent to this instance")
    row(s, x + 14, top + 240, "console", "you", "`depictio ingest`", "a YAML, or `--template`")

    # 2. Ingest
    x = xs[1]
    panel(s, x, top, w, h, "collection", "Ingest", "table")
    badge(s, x, top, "2", "collection")
    row(s, x + 14, top + 82, "folder-play-outline", "run", "Runs of a pipeline", "read in place: a folder, `s3://`, a URL")
    row(s, x + 14, top + 140, "table", "collection", "Data collections", "one table per kind of file")
    row(s, x + 14, top + 198, "link-variant", "people", "Links", "filter one table, the others follow")
    row(s, x + 14, top + 256, "pencil-outline", "you", "Edit a table", "a sample sheet, cell by cell")

    # 3. Dashboards
    x = xs[2]
    panel(s, x, top, w, h, "dashboard", "Dashboards", "view-dashboard")
    badge(s, x, top, "3", "dashboard")
    row(s, x + 14, top + 82, "view-dashboard", "dashboard", "The template's dashboards", "imported with the project")
    row(s, x + 14, top + 140, "chart-scatter-plot", "dashboard", "Or your own", "figures, tables, cards, maps")
    row(s, x + 14, top + 198, "filter-variant", "you", "Filters", "reach every linked table")
    row(s, x + 14, top + 256, "comment-outline", "people", "Comments and versions", "kept with each dashboard")

    # 4. Share
    x = xs[3]
    panel(s, x, top, w + 5, h, "you", "Share", "account-multiple-outline")
    badge(s, x, top, "4", "you")
    row(s, x + 14, top + 82, "lock-outline", "you", "Permissions", "Owner, Editor, Viewer; or a group")
    row(s, x + 14, top + 140, "web", "you", "Public", "anyone can open it, read-only")
    row(s, x + 14, top + 198, "swap-horizontal", "you", "Send to another instance", "the project, its data and dashboards")
    row(s, x + 14, top + 256, "file-export-outline", "you", "Export as a ZIP, Create a template", "to import it, or run it on other data")

    mid = top + h / 2
    for a, b in zip(xs, xs[1:]):
        s.arrow(a + w + 4, mid, b - 6, mid, colour=t.muted)

    # 5. Every new run: the loop under steps 1 to 3.
    fy, fh = 440, 196
    rrect(s, 26, fy, 1033, fh, fill="none", stroke=edge(t, "run"), r=14, width=1.5, dash=True)
    badge(s, 26, fy, "5", "run")
    s.text(64, fy + 30, "Every new run", size=17, anchor="start", weight="bold", colour=ink(t, "run"))
    s.text(196, fy + 30, "the same project, its dashboards kept", size=14, anchor="start", colour=t.dim)

    cy, ch, cw = fy + 54, 118, w
    cxs = xs[:3]
    card(s, cxs[0], cy, cw, ch, "run", "folder-play-outline", "Add data, Add run",
         ("another run of the same pipeline,", "or `depictio ingest --attach-run`", "samples already there are held back"))
    card(s, cxs[1], cy, cw, ch, "run", "history", "A new data version",
         ("each ingestion or table edit;", "Past versions, Restore", "Data refresh re-reads a remote source"))
    card(s, cxs[2], cy, cw, ch, "dashboard", "clock-outline", "What's new",
         ("what changed since your last visit:", "new samples marked on the figures,", "edits and comments listed"))
    for a, b in zip(cxs, cxs[1:]):
        s.arrow(a + cw + 4, cy + ch / 2, b - 6, cy + ch / 2, colour=solid(t, "run"))

    # The loop closes on the dashboards: What's new is read there.
    s.arrow(cxs[2] + cw / 2 + 40, cy - 4, cxs[2] + cw / 2 + 40, top + h + 6, colour=solid(t, "dashboard"))
    # Ingesting the run is what writes the new version.
    s.arrow(xs[1] + w - 60, top + h + 6, xs[1] + w - 60, cy - 4, colour=solid(t, "collection"))

    # Elsewhere: what Share sends or exports arrives as Import a project.
    bx, by, bw, bh = 1075, 470, 320, 136
    rrect(s, bx, by, bw, bh, fill=white(t), stroke=t.muted, r=12, width=1.4, dash=True)
    s.glyph("depictio", bx + 28, by + 30, size=24)
    s.text(bx + 48, by + 36, "Another instance", size=16, anchor="start", weight="bold")
    for i, line in enumerate(("Import a project: the ZIP,", "or Receive a project with a code;", "a template runs on its own data")):
        s.text(bx + 18, by + 66 + i * 20, line, size=13, anchor="start", colour=t.dim)
    s.arrow(bx + bw / 2, top + h + 6, bx + bw / 2, by - 6, colour=solid(t, "you"), dashed=True)
    return s


if __name__ == "__main__":
    write_themed(lifecycle, OUT, "project-lifecycle")
