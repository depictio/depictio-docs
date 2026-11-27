#!/usr/bin/env python3
"""The concept figures of the hands-on workshop (Tutorials > Hands-on workshop).

    uv run python dev/diagrams/workshop.py

Writes ``docs/images/tutorials/workshop/diagrams/<name>_{light,dark}.{svg,png}``.

Every figure draws the workshop's own data, so a learner sees in the figure the
names they meet on screen: the nf-core/ampliseq megatest run (12 samples, the
template's data collections and links) and the Palmer Penguins tables
(``individual_id``, the versions of ``physical_features``). Where a number
appears it is one the learner can check in the app.

The figures are drawn clean (straight strokes, sans-serif) because most of
them stand for the app's own screens: the Dashboards list and its menu, the
History panel, the three-step component builder. Labels are the app's
(``Component type / Data source / Design``, ``Next Step``, ``Create
component``, ``Dashboard actions``). Colours and icons come from concepts.py.
"""

from __future__ import annotations

import csv
from pathlib import Path

from concepts import (
    badge,
    button,
    chip,
    dashboard,
    dc_row,
    edge,
    fg_on,
    folder,
    icon,
    icon_button,
    ink,
    link_line,
    note,
    panel,
    person,
    raw,
    rrect,
    shadow_defs,
    solid,
    table_panel,
    version_dot,
    white,
    window,
)
from sketch import MONO, Sketch, Theme, write_themed

DOCS = Path(__file__).resolve().parents[2] / "docs"
OUT = DOCS / "images" / "tutorials" / "workshop" / "diagrams"
DATA = DOCS / "tutorials" / "workshop"


def new(theme: Theme, w: float, h: float, title: str, subtitle: str) -> Sketch:
    s = Sketch(w, h, theme=theme, clean=True)
    shadow_defs(s)
    s.text(46, 50, title, size=24, anchor="start", weight="bold")
    s.text(46, 76, subtitle, size=15, anchor="start", colour=theme.dim)
    return s


def filters_panel(s: Sketch, x: float, y: float, w: float, field: str, value: str, *, section: str = "") -> None:
    """The Filters panel of a dashboard, with one select set."""
    t = s.theme
    h = 196 if section else 172
    panel(s, x, y, w, h, "you", "Filters", ico="filter-variant")
    yy = y + 70
    if section:
        s.text(x + 16, yy, section, size=11, anchor="start", colour=t.dim, weight="bold")
        yy += 24
    s.text(x + 16, yy, field, size=14, anchor="start", weight="bold")
    rrect(s, x + 16, yy + 10, w - 32, 38, fill=white(t), stroke=solid(t, "you"), r=8, width=1.6)
    chip(s, x + 22, yy + 14, 18 + len(value) * 9, value, "you", filled=True)
    s.text(x + 16, yy + 76, "1 filter active", size=13, anchor="start", colour=ink(t, "you"))


def mdi_or_multiqc(s: Sketch, name: str, cx: float, cy: float, size: float, colour: str) -> None:
    if name == "multiqc":
        s.glyph("multiqc", cx, cy, size=size)
    else:
        icon(s, name, cx, cy, size, colour)


def menu_box(s: Sketch, x: float, y: float, w: float, h: float) -> None:
    t = s.theme
    f = ' filter="url(#sh)"' if t.name == "light" else ""
    raw(s, f'<g{f}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{white(t)}" stroke="{t.muted}" stroke-width="1.2"/></g>')


# -- episode 0 --------------------------------------------------------------------


def four_words(theme: Theme) -> Sketch:
    """Episode 0: the four words, drawn on the ampliseq project."""
    t = theme
    s = new(t, 1440, 640, "Project, data collections, links, dashboard", "the nf-core/ampliseq run, as you meet it in episodes 1, 2 and 3")

    panel(s, 40, 105, 900, 500, "project", "Project · today's ampliseq run", sub="23 data collections · 19 links")
    badge(s, 40, 105, "1", "project")

    table_panel(s, 70, 190, 340, "metadata", ("ID", "habitat"), [("SRR10070130", "Riverwater"), ("SRR10102392", "Soil"), ("…", "")], (180, 140), mark_col=0)
    s.text(240, 410, "one row per sample", size=13, colour=t.dim)

    badge(s, 528, 182, "2", "collection")
    s.text(550, 188, "Data collections: tables, a MultiQC report…", size=15, anchor="start", weight="bold", colour=ink(t, "collection"))
    rows = (("alpha_rarefaction", "table"), ("taxonomy_composition", "table"), ("embedding_pcoa", "table"), ("multiqc_data", "multiqc"))
    for i, (name, ico) in enumerate(rows):
        dc_row(s, 520, 210 + i * 54, 390, name, ico=ico)
    s.text(715, 448, "… and 18 more", size=13, colour=t.dim)
    for i in range(4):
        link_line(s, 410, 300, 518, 230 + i * 54, mid_icon=(i == 3), at=0.42)

    badge(s, 82, 478, "3", "link")
    note(s, 104, 484, ("Links: from metadata to the others,", "matching the sample IDs: a filter on", "metadata narrows every collection"), key="link")

    s.arrow(940, 340, 1000, 340, colour=t.muted)
    s.text(970, 328, "read by", size=13, colour=t.dim)
    dashboard(s, 1005, 150, 400, 360, "nf-core/ampliseq", search=False)
    badge(s, 1005, 150, "4", "dashboard")
    note(s, 1205, 545, ("Dashboard: 7 tabs of components", "reading the data collections"), key="dashboard", anchor="middle")
    return s


# -- episode 1 --------------------------------------------------------------------


def filter_flow(theme: Theme) -> Sketch:
    """Episode 1: four ways to pick samples, all on the metadata; the links carry them on."""
    t = theme
    s = new(t, 1440, 580, "Four ways to pick samples",
            "a filter, rows of a table, points of a figure, markers of a map: on the metadata, the links carry the picked samples to the other data collections")

    sources = (
        ("filter-variant", "Filters panel", "Habitat: Soil"),
        ("table", "A table", "rows of Sample sheet"),
        ("chart-scatter-plot", "A figure", "points of a scatter plot"),
        ("map-marker-multiple", "A map", "markers of Sampling sites"),
    )
    x, w, h, gap, top = 40, 300, 84, 14, 112
    mid = (385, 318)
    for i, (ico, title, detail) in enumerate(sources):
        y = top + i * (h + gap)
        rrect(s, x, y, w, h, fill=white(t), stroke=edge(t, "you"), r=12, width=1.4)
        rrect(s, x + 14, y + 18, 48, 48, fill=t.fill("you"), r=10, width=0)
        icon(s, ico, x + 38, y + 42, 26, solid(t, "you"))
        s.text(x + 76, y + 36, title, size=16, anchor="start", weight="bold")
        s.text(x + 76, y + 60, detail, size=13, anchor="start", colour=t.dim)
        s.arrow(x + w + 2, y + h / 2, mid[0] - 4, mid[1], colour=solid(t, "you"))

    bottom = table_panel(
        s, 385, 150, 360, "metadata", ("sample", "habitat"),
        [("SRR10070130", "Riverwater"), ("SRR10070132", "Groundwater"), ("SRR10070149", "Sediment"),
         ("SRR10102392", "Soil"), ("SRR10102393", "Soil"), ("SRR10102394", "Soil")],
        (190, 150), picked={3, 4, 5}, note="12 samples, 3 picked", mark_col=0,
    )

    rows = (("taxonomy_rel_abundance", "table"), ("alpha_diversity_multi_canonical", "table"), ("read_tracking", "table"), ("multiqc_data", "multiqc"))
    for i, (name, ico) in enumerate(rows):
        yy = 150 + i * 66
        dc_row(s, 840, yy, 330, name, ico=ico)
        link_line(s, 745, 318, 838, yy + 20, mid_icon=(i == 1), at=0.45)
    note(s, 1005, 440, ("links, from metadata:", "the 3 samples reach every collection"), key="link", anchor="middle")

    # Where it applies.
    bx, bw = 1200, 210
    rrect(s, bx, 150, bw, 112, fill=t.fill("dashboard"), stroke=edge(t, "dashboard"), r=12, width=1.3)
    icon(s, "pin", bx + 22, 176, 18, solid(t, "dashboard"))
    s.text(bx + 38, 182, "Pinned filter", size=15, anchor="start", weight="bold", colour=ink(t, "dashboard"))
    s.text(bx + 16, 212, "Sample filters section:", size=13, anchor="start", colour=t.dim)
    s.text(bx + 16, 236, "every tab", size=15, anchor="start", weight="bold")
    rrect(s, bx, 282, bw, 112, fill=white(t), stroke=edge(t, "dashboard"), r=12, width=1.3)
    icon(s, "chart-scatter-plot", bx + 22, 308, 18, solid(t, "dashboard"))
    s.text(bx + 38, 314, "Selection", size=15, anchor="start", weight="bold", colour=ink(t, "dashboard"))
    s.text(bx + 16, 344, "table, figure, map:", size=13, anchor="start", colour=t.dim)
    s.text(bx + 16, 368, "its own tab", size=15, anchor="start", weight="bold")
    for yy in (206, 338):
        s.arrow(1172, 300, bx - 4, yy, colour=t.muted)

    note(s, 46, 548, ("The links go one way, from metadata to the others: a selection on a figure of another collection, such as the PCoA, narrows only the components that read that collection.",))
    return s


# nf-core's own mark, as the deck uses it (assets/brand/nf-core_icon.svg).
NFCORE_ICON = __import__("base64").b64encode((Path(__file__).parent / "nf-core-icon.svg").read_bytes()).decode()
# Shiny's hex logo, as Posit ships it in bslib (examples/card/www/shiny-hex.svg).
SHINY_HEX = __import__("base64").b64encode((Path(__file__).parent / "shiny-hex.svg").read_bytes()).decode()


def why_depictio(theme: Theme) -> Sketch:
    """Episode 1: where a pipeline usually stops, and Depictio as the step after it."""
    t = theme
    s = new(t, 1440, 620, "Depictio: the step after the pipeline",
            "one platform, the same for every pipeline, from building the dashboard to sharing it")

    # Usually
    s.text(46, 128, "Usually", size=16, anchor="start", weight="bold", colour=t.dim)
    folder(s, 40, 152, 240, 84, "one pipeline", ("results/",))
    ends = (("folder-outline", "Output files", "opened one by one", ()),
            ("text-box-outline", "A static HTML report", "views fixed when it was written",
             (("multiqc", "MultiQC"), ("quarto", "Quarto"), ("jupyter", "Jupyter"))),
            ("code-braces", "An app coded from scratch", "for one dataset, to maintain and host",
             (("shiny", "Shiny"), ("streamlit", "Streamlit"), ("plotly", "Plotly Dash"))))
    brand = {"quarto": "#39729E", "jupyter": "#F37626", "streamlit": "#FF4B4B",
             "plotly": "#3F4F75" if t.name == "light" else "#A7B4DA"}
    for i, (ico, title, sub, tools) in enumerate(ends):
        x = 370 + i * 360
        rrect(s, x, 142, 300, 104, fill=t.fill("grey"), stroke=t.muted, r=10, width=1.2, dash=True)
        icon(s, ico, x + 30, 168, 24, t.dim)
        s.text(x + 56, 168, title, size=15, anchor="start", weight="bold", colour=t.dim)
        s.text(x + 56, 191, sub, size=13, anchor="start", colour=t.dim)
        if not tools:
            s.text(x + 26, 226, "TSV, CSV, PNG, logs…", size=13, anchor="start", colour=t.dim)
        lx = x + 26
        for logo, name in tools:
            if logo == "shiny":  # Posit's own hex, as bslib ships it
                raw(s, f'<image href="data:image/svg+xml;base64,{SHINY_HEX}" x="{lx - 9:.1f}" y="{210:.1f}" width="18" height="21"/>')
            elif logo == "multiqc":
                s.glyph("multiqc", lx, 221, size=18)
            else:
                s.glyph(logo, lx, 221, size=17, colour=brand[logo])
            s.text(lx + 14, 226, name, size=13, anchor="start")
            lx += 14 + len(name) * 7.4 + 22
        if i:
            s.text(x - 30, 199, ("and/or", "or")[i - 1], size=13, colour=t.dim)
    s.arrow(282, 194, 366, 194, colour=t.muted)
    s.line(40, 272, 1400, 272, colour=t.fill("grey"), width=1.5)
    raw(s, '<g transform="translate(0,30)">')

    # With Depictio
    s.text(46, 288, "With", size=16, anchor="start", weight="bold")
    s.glyph("depictio", 100, 282, size=20)
    s.text(114, 288, "Depictio", size=16, anchor="start", weight="bold")
    for i, name in enumerate(("nf-core/ampliseq", "nf-core/rnaseq", "your own pipeline")):
        y = 304 + i * 84
        folder(s, 40, y, 240, 70, name, ("results/",), logo=NFCORE_ICON if name.startswith("nf-core") else "")
        s.arrow(282, y + 35, 366, 430, colour=t.muted)
    # The platform is Depictio itself, not a project: neutral card, its own logo.
    rrect(s, 370, 300, 400, 260, fill=white(t), stroke=t.muted, r=12, width=1.4)
    raw(s, f'<path d="M371,346 V312 Q371,301 382,301 H758 Q769,301 769,312 V346 Z" fill="{t.fill("grey")}"/>')
    s.line(370, 346, 770, 346, colour=t.muted, width=1.2)
    s.glyph("depictio", 396, 323, size=24)
    s.text(418, 329, "One platform, every pipeline", size=17, anchor="start", weight="bold")
    s.text(755, 329, "while you build", size=13, anchor="end", colour=t.dim)
    rows = (("file-cog-outline", "a template per pipeline version"),
            ("chart-scatter-plot", "components from the Tools catalog"),
            ("pencil-outline", "edit in the interface, in code or YAML"),
            ("history", "every save is a version"))
    for i, (ico, text) in enumerate(rows):
        yy = 378 + i * 46
        rrect(s, 390, yy - 18, 36, 36, fill=t.fill("grey"), r=8, width=0)
        icon(s, ico, 408, yy, 20, t.dim)
        s.text(440, yy + 5, text, size=15, anchor="start")
    s.arrow(772, 430, 806, 430, colour=t.muted)
    dashboard(s, 810, 300, 300, 260, "Your dashboard", tabs=("Overview", "QC", "…"), search=False)
    s.text(1285, 290, "after you share", size=13, colour=t.dim)
    shares = (("account-multiple-outline", "Collaborators", ("who opens, who edits;", "filter, compare, comment"))
              , ("web", "Everyone", ("a public project, or", "one HTML file, no server")))
    for i, (ico, title, lines) in enumerate(shares):
        y = 300 + i * 136
        rrect(s, 1160, y, 250, 124, fill=white(t), stroke=edge(t, "you"), r=12, width=1.3)
        icon(s, ico, 1188, y + 30, 22, solid(t, "you"))
        s.text(1210, y + 36, title, size=16, anchor="start", weight="bold", colour=ink(t, "you"))
        for k, l in enumerate(lines):
            s.text(1180, y + 70 + k * 22, l, size=14, anchor="start", colour=t.dim)
        s.arrow(1112, 430, 1156, y + 62, colour=t.muted)
    raw(s, "</g>")
    return s


def status(s: Sketch, x: float, y: float, ok: bool) -> None:
    t = s.theme
    key, ico, text = ("good", "pencil", "You can change it") if ok else ("bad", "lock-outline", "Read only")
    w = 190 if ok else 130
    rrect(s, x - w, y, w, 34, fill=t.fill(key), stroke=solid(t, key), r=17, width=1.4)
    icon(s, ico, x - w + 22, y + 17, 17, solid(t, key))
    s.text(x - w + 36 + (w - 36) / 2 - 4, y + 22, text, size=14, weight="bold", colour=ink(t, key))


def yours_and_shared(theme: Theme) -> Sketch:
    """Episode 1: what a reader can and cannot change, and where their own view is kept."""
    t = theme
    s = new(t, 1440, 600, "As a reader, what you can change", "on a dashboard shared with you")

    dashboard(s, 40, 110, 520, 330, "nf-core/ampliseq", search=False)
    chip(s, 440, 118, 108, "Reader", "people", ico="eye-outline")

    rows = (
        ("view-dashboard", "dashboard", "Dashboard", "its figures, tables, tabs and layout", "To change it, make your own copy: episode 2"),
        ("table", "collection", "Data", "the project's data collections", "Changed by the project's owners and editors"),
    )
    for k, (ico, key, name, what, sub) in enumerate(rows):
        y = 110 + k * 110
        rrect(s, 610, y, 790, 96, fill=white(t), stroke=t.muted, r=12, width=1.1)
        rrect(s, 632, y + 22, 52, 52, fill=t.fill(key), stroke=edge(t, key), r=10, width=1.3)
        icon(s, ico, 658, y + 48, 28, solid(t, key))
        s.text(706, y + 36, name, size=18, anchor="start", weight="bold", colour=ink(t, key))
        s.text(706, y + 59, what, size=14, anchor="start")
        s.text(706, y + 80, sub, size=13, anchor="start", colour=t.dim)
        status(s, 1380, y + 31, False)

    y = 330
    rrect(s, 610, y, 790, 240, fill=white(t), stroke=solid(t, "good"), r=12, width=1.4)
    rrect(s, 632, y + 22, 52, 52, fill=t.fill("you"), stroke=edge(t, "you"), r=10, width=1.3)
    icon(s, "account", 658, y + 48, 28, solid(t, "you"))
    s.text(706, y + 42, "Your view", size=18, anchor="start", weight="bold", colour=ink(t, "you"))
    s.text(706, y + 64, "changes nothing for anyone else", size=14, anchor="start")
    status(s, 1380, y + 31, True)
    items = (
        ("filter-variant", "Filters, and selections on a figure", "kept for your account, in any browser (Settings › Remember my filters, on by default)"),
        ("account-multiple-outline", "Groups, in Analysis", "kept in this browser only"),
        ("link-variant", "Shown to someone else only by a view link", "Settings › Share this view: whoever opens it gets your filters"),
    )
    for k, (ico, what, where) in enumerate(items):
        yy = y + 100 + k * 46
        icon(s, ico, 718, yy + 4, 20, solid(t, "you"))
        s.text(740, yy, what, size=14, anchor="start", weight="bold")
        s.text(740, yy + 19, where, size=13, anchor="start", colour=t.dim)
    return s


# -- episode 2 --------------------------------------------------------------------


def your_copy(theme: Theme) -> Sketch:
    """Episode 2: duplicate from the Dashboards list, open the copy, Edit."""
    t = theme
    s = new(t, 1440, 540, "Your copy", "Duplicate the shared dashboard: the copy is yours, so you can edit it; the original stays as it is")

    panel(s, 40, 105, 700, 400, "dashboard", "Dashboards")
    rows = (
        ("nf-core/ampliseq (copy)", "you are the owner", True),
        ("nf-core/ampliseq", "shared with you, reader", False),
        ("Palmer Penguins: Three Field Seasons", "shared with you, reader", False),
    )
    for i, (name, sub, new_row) in enumerate(rows):
        y = 165 + i * 70
        rrect(s, 58, y, 664, 58, fill=t.fill("good") if new_row else white(t), stroke=solid(t, "good") if new_row else t.fill("grey"), r=10, width=1.6 if new_row else 1.2)
        icon(s, "view-dashboard", 84, y + 29, 22, solid(t, "dashboard"))
        s.text(108, y + 25, name, size=15, anchor="start", weight="bold")
        s.text(108, y + 45, sub, size=13, anchor="start", colour=ink(t, "good") if new_row else t.dim)
        icon_button(s, 694, y + 29, "dots-vertical", ring=(i == 1), size=30)
    badge(s, 726, 216, "1", "you")
    badge(s, 52, 165, "3", "good")

    mx, my = 500, 290
    menu_box(s, mx, my, 200, 200)
    s.text(mx + 14, my + 22, "Dashboard actions", size=12, anchor="start", colour=t.dim)
    for k, (label, ico) in enumerate((("Open", "view-dashboard"), ("Edit", "pencil"), ("Duplicate", "content-copy"), ("Export JSON", "upload"), ("Delete", None))):
        yy = my + 34 + k * 32
        on = label == "Duplicate"
        if on:
            rrect(s, mx + 6, yy, 188, 30, fill=t.fill("you"), r=6, width=0)
        colour = ink(t, "bad") if label == "Delete" else (ink(t, "you") if on else t.ink)
        if ico:
            icon(s, ico, mx + 24, yy + 15, 16, colour)
        s.text(mx + 42, yy + 20, label, size=14, anchor="start", colour=colour, weight="bold" if on else "normal")
    badge(s, mx + 200, my + 113, "2", "you")

    s.arrow(740, 200, 800, 200, colour=t.muted)
    s.text(770, 186, "open", size=13, colour=t.dim)
    dashboard(s, 805, 105, 595, 330, "nf-core/ampliseq (copy)", search=False)
    tx, ty = 1067, 410
    menu_box(s, tx, ty, 70, 52)
    icon_button(s, tx + 35, ty + 26, "pencil", key="you", ring=True, size=34)
    badge(s, tx + 78, ty - 4, "4", "you")
    note(s, 1102, 500, ("Edit: the pencil, in the bottom toolbar",), key="you", anchor="middle")
    return s


# The builder's type grid: icon and accent per type, from the app's
# componentTypeMeta.ts (COMPONENT_TYPE_VISUALS), in the grid's own order.
TYPES = (
    ("Figure", "graph-box", "#9966CC"),
    ("Card", "formkit:number", "#45B8AC"),
    ("Interactive", "bx:slider-alt", "#8BC34A"),
    ("Table", "octicon:table-24", "#6495ED"),
    ("MultiQC", "multiqc", None),
    ("Image", "image-area", "#E6779F"),
)
FIGURE = TYPES[0]


def type_tile(s: Sketch, cx: float, cy: float, ico: str, colour: str | None, size: float = 36) -> None:
    """The coloured square the type grid draws behind a type's icon."""
    if colour is None:
        s.glyph("multiqc", cx, cy, size=size * 0.9)
        return
    rrect(s, cx - size / 2, cy - size / 2, size, size, fill=colour, r=size * 0.28, width=0)
    icon(s, ico, cx, cy, size * 0.6, "#ffffff")


def selected_badge(s: Sketch, x: float, y: float) -> None:
    """Steps 2 and 3 recall the chosen type in its colour."""
    t = s.theme
    name, ico, colour = FIGURE
    s.text(x, y + 19, "Selected component", size=12, anchor="start", colour=t.dim)
    rrect(s, x + 132, y + 2, 92, 26, fill=colour, r=13, width=0)
    icon(s, ico, x + 150, y + 15, 15, "#ffffff")
    s.text(x + 190, y + 20, name, size=13, weight="bold", colour="#ffffff")


def component_steps(theme: Theme) -> Sketch:
    """Episode 2: the component builder, step by step, with its own labels and colours."""
    t = theme
    s = new(t, 1440, 540, "Every component in three steps", "the builder's own steps: Component type, Data source, Design; then Create component")
    steps = ("Component type", "Data source", "Design")
    xs = (40, 505, 970)
    for k, x in enumerate(xs):
        window(s, x, 105, 430, 390, "")
        badge(s, x, 105, str(k + 1), "you")
        s.text(x + 18, 160, "nf-core/ampliseq (copy)  ›  New component", size=12, anchor="start", colour=t.dim)
        for j, name in enumerate(steps):
            cx = x + 60 + j * 155
            done, cur = j < k, j == k
            raw(s, f'<circle cx="{cx}" cy="192" r="13" fill="{solid(t, "you") if (done or cur) else white(t)}" stroke="{solid(t, "you") if (done or cur) else t.muted}" stroke-width="1.6"/>')
            if done:
                icon(s, "check", cx, 192, 16, fg_on(t))
            else:
                s.text(cx, 197, str(j + 1), size=13, weight="bold", colour=fg_on(t) if cur else t.dim)
            s.text(cx, 225, name, size=12, colour=ink(t, "you") if cur else t.dim, weight="bold" if cur else "normal")
            if j < 2:
                s.line(cx + 18, 192, cx + 137, 192, colour=solid(t, "you") if done else t.muted, width=1.6)
        s.line(x + 1, 240, x + 429, 240, colour=t.fill("grey"), width=1.2)

    # 1 · Component type: the type grid, each type on its coloured tile
    x = xs[0]
    for k, (name, ico, colour) in enumerate(TYPES):
        cx, cy = x + 22 + (k % 3) * 132, 254 + (k // 3) * 86
        on = name == "Figure"
        rrect(s, cx, cy, 122, 76, fill=white(t), stroke="#4dabf7" if on else t.muted, r=10, width=2.4 if on else 1.1)
        type_tile(s, cx + 61, cy + 28, ico, colour, size=34)
        s.text(cx + 61, cy + 64, name, size=13, weight="bold")
    button(s, x + 290, 444, 120, "Next Step", "people")

    # 2 · Data source: the data collection list
    x = xs[1]
    selected_badge(s, x + 22, 250)
    s.text(x + 22, 302, "Data Collection", size=13, anchor="start", weight="bold")
    rrect(s, x + 22, 312, 386, 116, fill=white(t), stroke=t.muted, r=8, width=1.1)
    for k, name in enumerate(("alpha_rarefaction", "ancombc_results", "metadata")):
        yy = 318 + k * 35
        on = name == "ancombc_results"
        if on:
            rrect(s, x + 28, yy, 374, 32, fill=t.fill("you"), r=6, width=0)
        icon(s, "table", x + 46, yy + 16, 16, solid(t, "collection"))
        s.text(x + 62, yy + 21, f"`{name}`", size=13, anchor="start", colour=ink(t, "you") if on else t.ink)
    button(s, x + 290, 444, 120, "Next Step", "people", ring=True)

    # 3 · Design: the form and its preview
    x = xs[2]
    selected_badge(s, x + 22, 250)
    for k, (lab, val) in enumerate((("X axis", "lfc"), ("Y axis", "neg_log10_qval"), ("Color by", "contrast"))):
        yy = 292 + k * 48
        s.text(x + 22, yy + 12, lab, size=12, anchor="start", colour=t.dim, weight="bold")
        rrect(s, x + 22, yy + 18, 180, 26, fill=white(t), stroke=t.muted, r=6, width=1.1)
        s.text(x + 32, yy + 36, f"`{val}`", size=13, anchor="start")
    rrect(s, x + 220, 290, 190, 140, fill=white(t), stroke=t.muted, r=8, width=1.1)
    pal = ("#228be6", "#12b886", "#fd7e14")
    for k in range(27):
        u = (k - 13) / 13
        px = x + 315 + u * 80
        py = 418 - (u * u) * 105 - (k % 3) * 4
        raw(s, f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.6" fill="{pal[k % 3]}"/>')
    button(s, x + 215, 444, 196, "Create component", "good", ico="check", ring=True)

    for x in (470, 935):
        s.arrow(x + 2, 300, x + 31, 300, colour=t.muted)
    note(s, 1185, 525, ("the component lands on the tab you are on",), anchor="middle")
    return s


# -- episodes 3 and 4 -------------------------------------------------------------



def two_ways_in(theme: Theme) -> Sketch:
    """Episodes 3 and 4: read a run folder in place, or upload a run folder in place."""
    t = theme
    s = new(t, 1440, 690, "Two ways to bring data in", "episode 3 reads a run where it is; episode 4 uploads two files")

    s.text(46, 132, "Read in place · episode 3", size=17, anchor="start", weight="bold")
    folder(s, 40, 150, 300, 180, "megatest", ("nf-core/ampliseq 2.18.0, on S3",))
    for k, sub in enumerate(("pipeline_info/", "input/", "qiime2/", "multiqc/")):
        icon(s, "folder-outline", 72, 228 + k * 25, 16, solid(t, "run"))
        s.text(86, 233 + k * 25, f"`{sub}`", size=13, anchor="start")
    s.arrow(340, 240, 465, 240, colour=t.muted)
    s.text(402, 226, "read", size=13, colour=t.dim)
    icon(s, "content-copy", 402, 272, 20, t.muted)
    s.cross(402, 272, size=13, colour=solid(t, "bad"))
    s.text(402, 305, "no copy", size=12, colour=ink(t, "bad"))
    rrect(s, 470, 180, 290, 120, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.2)
    s.glyph("depictio", 504, 214, size=30)
    s.text(530, 221, "Depictio", size=17, anchor="start", weight="bold")
    s.text(490, 256, "detects nf-core/ampliseq 2.18.0", size=13, anchor="start", colour=t.dim)
    s.text(490, 278, "and applies its template", size=13, anchor="start", colour=t.dim)
    s.arrow(760, 240, 815, 240, colour=t.muted)
    for k in range(3):
        rrect(s, 820 + 12 - k * 6, 180 + k * 6 - 12, 170, 100, fill=t.fill("collection") if k == 2 else white(t), stroke=edge(t, "collection"), r=10, width=1.4)
    icon(s, "table", 852, 214, 22, solid(t, "collection"))
    s.text(875, 221, "23", size=20, anchor="start", weight="bold", colour=ink(t, "collection"))
    s.text(843, 252, "data collections", size=13, anchor="start", colour=t.dim)
    rrect(s, 1010, 190, 130, 100, fill=t.fill("link"), stroke=edge(t, "link"), r=10, width=1.4)
    icon(s, "link-variant", 1040, 222, 22, solid(t, "link"))
    s.text(1062, 229, "19", size=20, anchor="start", weight="bold", colour=ink(t, "link"))
    s.text(1030, 260, "links", size=13, anchor="start", colour=t.dim)
    dashboard(s, 1160, 140, 250, 210, "7 tabs", tabs=("Overview", "…"), active=0, search=False)
    s.text(1285, 378, "ready to open", size=13, colour=ink(t, "good"), weight="bold")

    s.line(40, 410, 1400, 410, colour=t.muted, width=1.2, dashed=True)

    s.text(46, 455, "Upload · episode 4", size=17, anchor="start", weight="bold")
    for k, name in enumerate(("demographic_data.csv", "physical_features.csv")):
        y = 480 + k * 72
        rrect(s, 40, y, 300, 56, fill=white(t), stroke=t.muted, r=10, width=1.2)
        icon(s, "text-box-outline", 66, y + 28, 20, t.dim)
        s.text(86, y + 33, f"`{name}`", size=14, anchor="start")
    s.arrow(340, 545, 465, 545, colour=t.muted)
    s.text(402, 531, "drop", size=13, colour=t.dim)
    rrect(s, 470, 470, 290, 150, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.5, dash=True)
    icon(s, "upload", 615, 512, 30, t.dim)
    s.text(615, 556, "Drop files or folders here", size=14, weight="bold")
    s.text(615, 580, "the files are copied into Depictio", size=13, colour=t.dim)
    s.arrow(760, 545, 815, 545, colour=t.muted)
    for k in range(2):
        rrect(s, 820 + 6 - k * 6, 495 + k * 6 - 6, 170, 100, fill=t.fill("collection") if k == 1 else white(t), stroke=edge(t, "collection"), r=10, width=1.4)
    icon(s, "table", 852, 529, 22, solid(t, "collection"))
    s.text(875, 536, "2", size=20, anchor="start", weight="bold", colour=ink(t, "collection"))
    s.text(843, 567, "data collections", size=13, anchor="start", colour=t.dim)
    rrect(s, 1010, 500, 130, 100, fill=white(t), stroke=solid(t, "link"), r=10, width=1.6, dash=True)
    icon(s, "link-variant", 1075, 530, 22, solid(t, "link"))
    s.text(1075, 565, "+ link", size=14, weight="bold", colour=ink(t, "link"))
    s.text(1075, 585, "you add it", size=12, colour=t.dim)
    rrect(s, 1160, 470, 250, 160, fill=white(t), stroke=solid(t, "dashboard"), r=12, width=1.6, dash=True)
    icon(s, "view-dashboard", 1285, 525, 30, solid(t, "dashboard"))
    s.text(1285, 570, "+ dashboard", size=14, weight="bold", colour=ink(t, "dashboard"))
    s.text(1285, 592, "you build it", size=12, colour=t.dim)
    s.text(1210, 668, "your part, in episode 4", size=13, colour=ink(t, "you"), weight="bold")
    return s


def penguin_points() -> list[tuple[float, float, bool]]:
    """bill_length_mm, flipper_length_mm and is-Gentoo for every penguin of episode 4's files."""
    demo = {r["individual_id"]: r["species"] for r in csv.DictReader(open(DATA / "demographic_data.csv"))}
    out = []
    for r in csv.DictReader(open(DATA / "physical_features.csv")):
        try:
            out.append((float(r["bill_length_mm"]), float(r["flipper_length_mm"]), demo.get(r["individual_id"]) == "Gentoo"))
        except ValueError:
            pass
    return out


def penguin_link(theme: Theme) -> Sketch:
    """Episode 4: a filter on the census reaches the measurements through the link."""
    t = theme
    s = new(t, 1440, 520, "The link at work", "a filter on one table narrows a figure drawn from the other")

    pts = penguin_points()
    n, gentoo_n = len(pts), sum(g for _, _, g in pts)
    filters_panel(s, 40, 150, 190, "species", "Gentoo")
    s.arrow(230, 240, 250, 240, colour=solid(t, "you"))
    table_panel(
        s, 255, 110, 330, "demographic_data", ("individual_id", "species"),
        [("adelie_1", "Adelie"), ("chinstrap_1", "Chinstrap"), ("gentoo_1", "Gentoo"), ("gentoo_2", "Gentoo")],
        (165, 140), picked={2, 3}, note=f"{n} penguins", mark_col=0,
    )
    link_line(s, 585, 255, 680, 255, mid_icon=True)
    s.text(632, 300, "`individual_id`", size=13, colour=ink(t, "link"))
    s.text(632, 320, "the link", size=12, colour=t.dim)
    table_panel(
        s, 685, 110, 445, "physical_features", ("individual_id", "bill_length_mm", "flipper_length_mm"),
        [("adelie_1", "39.1", "181"), ("chinstrap_1", "46.5", "192"), ("gentoo_1", "46.1", "211"), ("gentoo_2", "50.0", "230")],
        (130, 145, 150), picked={2, 3}, note="the same ids kept", mark_col=0,
    )
    s.arrow(1130, 240, 1148, 240, colour=t.muted)

    px, py, pw, ph = 1152, 110, 268, 330
    panel(s, px, py, pw, ph, "dashboard", "Figure", ico="graph-box")
    ox, oy, aw, ah = px + 62, py + ph - 62, pw - 80, ph - 46 - 80
    s.line(ox, oy, ox + aw, oy, colour=t.muted, width=1.2)
    s.line(ox, oy, ox, oy - ah, colour=t.muted, width=1.2)
    x0, x1, y0, y1 = 30, 62, 168, 236
    X = lambda v: ox + (v - x0) / (x1 - x0) * aw
    Y = lambda v: oy - (v - y0) / (y1 - y0) * ah
    for v in (35, 45, 55):
        s.line(X(v), oy, X(v), oy + 5, colour=t.muted, width=1)
        s.text(X(v), oy + 19, str(v), size=11, colour=t.dim)
    for v in (180, 200, 220):
        s.line(ox - 5, Y(v), ox, Y(v), colour=t.muted, width=1)
        s.text(ox - 9, Y(v) + 4, str(v), size=11, anchor="end", colour=t.dim)
    for bx, fl, gentoo in sorted(pts, key=lambda p: p[2]):
        fill, op = (solid(t, "you"), 0.85) if gentoo else (t.muted, 0.35)
        raw(s, f'<circle cx="{X(bx):.1f}" cy="{Y(fl):.1f}" r="2.6" fill="{fill}" fill-opacity="{op}"/>')
    s.text(ox + aw / 2, oy + 40, "`bill_length_mm`", size=13, colour=t.dim)
    raw(s, f'<text x="{ox - 40:.1f}" y="{oy - ah / 2:.1f}" transform="rotate(-90 {ox - 40:.1f} {oy - ah / 2:.1f})" font-family="{MONO}" font-size="11.5" fill="{t.dim}" text-anchor="middle">flipper_length_mm</text>')
    s.text(px + pw / 2, py + ph + 26, f"{gentoo_n} Gentoo in colour, others filtered out", size=13, colour=ink(t, "you"), weight="bold")
    note(s, 720, 495, (f"Without the link, the filter would stop at demographic_data: the figure would keep all {n} penguins.",), anchor="middle")
    return s



def penguin_join(theme: Theme) -> Sketch:
    """Episode 3: a join (Add join, or YAML for the CLI) writes a third table, one row per penguin with every column."""
    t = theme
    s = new(t, 1440, 450, "Link or join", "a link keeps the tables apart; a join writes a third table, one row per penguin with every column")
    table_panel(s, 40, 105, 330, "demographic_data", ("individual_id", "species"), [("adelie_1", "Adelie"), ("gentoo_1", "Gentoo")], (190, 120), mark_col=0)
    table_panel(s, 40, 285, 330, "physical_features", ("individual_id", "flipper"), [("adelie_1", "181"), ("gentoo_1", "211")], (190, 120), mark_col=0)
    s.arrow(370, 185, 505, 245, colour=t.muted)
    s.arrow(370, 365, 505, 290, colour=t.muted)
    raw(s, f'<circle cx="455" cy="268" r="17" fill="{white(t)}" stroke="{t.muted}" stroke-width="1.4"/>')
    icon(s, "table-merge-cells", 455, 268, 20, t.dim)
    s.text(440, 312, "join on", size=12, colour=t.dim)
    table_panel(
        s, 510, 175, 520, "joined_penguins", ("individual_id", "species", "flipper"),
        [("adelie_1", "Adelie", "181"), ("gentoo_1", "Gentoo", "211")], (190, 150, 120), mark_col=0,
    )
    note(s, 1070, 190, ("A third data collection,", "one row per penguin, every column.", "The two tables stay as they are;", "the join is rebuilt when one changes.", "", "Made in the browser with Add join,", "or in project.yaml (`joins:`) for the CLI."), key="collection")
    return s


# -- episode 5 --------------------------------------------------------------------


def runs_and_versions(theme: Theme) -> Sketch:
    """Episode 5: seasons arrive as runs; each change of a table is a version."""
    t = theme
    s = new(t, 1440, 680, "Runs and versions", "the prebuilt penguin project, one run per field season")

    icon(s, "folder-play-outline", 58, 168, 22, solid(t, "run"))
    s.text(76, 175, "Runs", size=17, anchor="start", weight="bold", colour=ink(t, "run"))
    icon(s, "table", 58, 418, 22, solid(t, "collection"))
    s.text(76, 425, "physical_features", size=16, anchor="start", weight="bold", colour=ink(t, "collection"))
    s.text(58, 450, "rows, version by version", size=13, anchor="start", colour=t.dim)

    xs = (380, 720, 1200)
    runs = ("season_2007", "season_2008", "season_2009")
    counts = (109, 223, 342)
    base, scale = 560, 0.62
    s.line(270, base, 1300, base, colour=t.muted, width=1.2)
    for k, (x, run, n) in enumerate(zip(xs, runs, counts)):
        hh = n * scale
        if run:
            folder(s, x - 110, 125, 220, 86, run, ("2 files · New",) if run == "season_2009" else ("2 files",))
            s.arrow(x, 211, x, base - hh - 8, colour=solid(t, "run"))
        else:
            s.text(x, base - hh - 16, "a correction", size=13, colour=t.dim)
        rrect(s, x - 60, base - hh, 120, hh, fill=t.fill("collection"), stroke=edge(t, "collection"), r=8, width=1.6)
        if k == 2:
            rrect(s, x - 60, base - hh, 120, 119 * scale, fill=solid(t, "you"), r=8, width=0, opacity=0.25)
            s.text(x, base - hh + 42, "+119", size=16, weight="bold", colour=ink(t, "you"))
        s.text(x, base - 14, f"{n} rows", size=14, weight="bold", colour=ink(t, "collection"))
        version_dot(s, x, base + 32, f"v{k}", on=(k == 1))

    s.line(1030, 110, 1030, 640, colour=solid(t, "you"), dashed=True, width=2)
    person(s, 1030, 610, 40, "you")
    s.text(1004, 615, "your visit", size=14, anchor="end", colour=ink(t, "you"), weight="bold")
    note(s, 1275, 300, ("What's new:", "+119 penguins", "since your visit"), key="you")

    s.curve([(720, 609), (720, 632), (680, 642)], colour=solid(t, "version"))
    note(s, 500, 638, ("Data version → v1:", "the figures before 2009, for you only"), key="version", anchor="middle")
    return s


if __name__ == "__main__":
    for build, name in (
        (four_words, "four-words"),
        (filter_flow, "filter-flow"),
        (why_depictio, "why-depictio"),
        (yours_and_shared, "yours-and-shared"),
        (your_copy, "your-copy"),
        (component_steps, "component-steps"),
        (two_ways_in, "two-ways-in"),
        (penguin_link, "penguin-link"),
        (penguin_join, "penguin-join"),
        (runs_and_versions, "runs-and-versions"),
    ):
        write_themed(build, OUT, name)
