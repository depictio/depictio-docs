#!/usr/bin/env python3
"""The concept figures of the workshop's Day 2 lesson (Tutorials > Hands-on workshop, Day 2).

    uv run python dev/diagrams/workshop_cli.py

Writes ``docs/images/tutorials/workshop-cli/diagrams/<name>_{light,dark}.{svg,png}``.

Same clean style, colours and icons as workshop.py (concepts.py). Every number
comes from a rehearsal of the lesson with depictio 1.21.0 (PyPI) against a v1.21.0 server.
"""

from __future__ import annotations

from pathlib import Path

from concepts import (
    badge, button, chip, dashboard, dc_row, edge, folder, icon, ink, link_line, note, panel, raw, rrect, shadow_defs, solid, white,
    window,
)
from sketch import MONO, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "tutorials" / "workshop-cli" / "diagrams"


def new(theme: Theme, w: float, h: float, title: str, subtitle: str) -> Sketch:
    s = Sketch(w, h, theme=theme, clean=True)
    shadow_defs(s)
    s.text(46, 50, title, size=24, anchor="start", weight="bold")
    s.text(46, 76, subtitle, size=15, anchor="start", colour=theme.dim)
    return s


def _esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def term(s: Sketch, x: float, y: float, w: float, lines: tuple[str, ...], *, size: float = 13.5) -> float:
    """A terminal: dark block, ``$`` in green, options in blue. Returns the bottom."""
    step = size * 1.65
    h = 18 + step * len(lines)
    rrect(s, x, y, w, h, fill="#25262b", stroke="#5c5f66", r=8, width=1)
    for i, l in enumerate(lines):
        ty = y + 14 + step * (i + 0.72)
        tx = x + 14
        if l.startswith("$ "):
            raw(s, f'<text x="{tx:.1f}" y="{ty:.1f}" font-family="{MONO}" font-size="{size}" fill="#69db7c">$</text>')
            l = "  " + l[2:]
        spans = "".join(
            f'<tspan fill="{"#74c0fc" if tok.startswith("--") else "#f1f3f5"}">{_esc(tok)}</tspan>' for tok in _tokens(l)
        )
        raw(s, f'<text x="{tx:.1f}" y="{ty:.1f}" font-family="{MONO}" font-size="{size}" xml:space="preserve">{spans}</text>')
    return y + h


def _tokens(line: str) -> list[str]:
    out, cur = [], ""
    for ch in line:
        cur += ch
        if ch == " ":
            out.append(cur)
            cur = ""
    return out + ([cur] if cur else [])


def code_card(s: Sketch, x: float, y: float, w: float, title: str, lines: tuple[tuple[str, str | None], ...], *, size: float = 13.5) -> float:
    """A YAML file: header with its name, monospace lines; a line can be tinted in a concept's colour."""
    t = s.theme
    step = size * 1.75
    h = 46 + 14 + step * len(lines) + 8
    panel(s, x, y, w, h, "people", title, ico="file-code-outline")
    for i, (l, key) in enumerate(lines):
        ly = y + 46 + 10 + step * i
        if key:
            rrect(s, x + 8, ly + 1, w - 16, step - 2, fill=t.fill(key), stroke=edge(t, key), r=5, width=1)
        raw(s, f'<text x="{x + 18:.1f}" y="{ly + step * 0.7:.1f}" font-family="{MONO}" font-size="{size}" fill="{ink(t, key) if key else t.ink}" xml:space="preserve">{_esc(l)}</text>')
    return y + h


def item(s: Sketch, x: float, y: float, ico: str, key: str, text: str, *, size: float = 15) -> None:
    """One line of a panel: the concept's icon, then the text."""
    icon(s, ico, x + 10, y - 5, 19, solid(s.theme, key))
    s.text(x + 28, y, text, size=size, anchor="start")


def cli_flow(theme: Theme) -> Sketch:
    """Day 2: the CLI reads a folder on the laptop, writes the tables to the storage, records the project on the server."""
    t = theme
    s = new(t, 1440, 560, "From your laptop to the server", "the CLI reads your folder, writes the tables to the server's storage and records the project; the browser shows the result")

    window(s, 40, 105, 500, 385, "your laptop")
    folder(s, 62, 160, 220, 112, "penguins-workshop/", ("penguins-1.yaml", "seasons/season_2007/"))
    rrect(s, 298, 160, 220, 112, fill=white(t), stroke=t.muted, r=10, width=1.3)
    icon(s, "key-outline", 322, 187, 20, t.dim)
    s.text(342, 193, "`~/.depictio/CLI.yaml`", size=13, anchor="start", weight="bold")
    for i, l in enumerate(("server address", "your token", "storage access")):
        s.text(318, 222 + i * 19, l, size=13, anchor="start", colour=t.dim)
    term(s, 62, 290, 456, ("$ depictio ingest \\", "    --project-config-path penguins-1.yaml \\", "    --project yourname-penguins \\", "    --dashboard starter.yaml"))
    note(s, 62, 438, ("Your files stay on the laptop:", "the CLI reads them here and sends the tables"), key="you")

    sx = 650
    panel(s, sx, 110, 320, 175, "project", "Depictio server", ico="server-outline")
    for i, (ico, key, txt) in enumerate((
        ("jira", "project", "project `yourname-penguins`"),
        ("folder-play-outline", "run", "run `season_2007`"),
        ("table", "collection", "1 data collection"),
        ("view-dashboard", "dashboard", "dashboard Penguin field survey"),
    )):
        item(s, sx + 16, 182 + i * 26, ico, key, txt)
    panel(s, sx, 330, 320, 150, "collection", "Storage (S3)", ico="database-outline")
    dc_row(s, sx + 16, 392, 288, "physical_features")
    s.text(sx + 160, 460, "one table per data collection", size=13, colour=t.dim)

    s.arrow(540, 245, sx - 6, 200, colour=solid(t, "you"))
    s.arrow(540, 380, sx - 6, 410, colour=solid(t, "you"))
    s.text(590, 211, "API", size=13, colour=ink(t, "you"), weight="bold")
    s.text(590, 385, "S3", size=13, colour=ink(t, "you"), weight="bold")

    dashboard(s, 1060, 140, 345, 300, "Penguin field survey", tabs=("Overview",), active=0, search=False, value="109", label="Birds measured")
    s.arrow(sx + 320, 200, 1054, 250, colour=t.muted)
    s.arrow(sx + 320, 410, 1054, 360, colour=t.muted)
    note(s, 1232, 475, ("in your browser, as on Day 1",), key="dashboard", anchor="middle")
    return s


def ingest_steps(theme: Theme) -> Sketch:
    """Episode 1: what `depictio ingest` does with a run folder, and what --var and --dry-run change."""
    t = theme
    s = new(t, 1440, 560, "What `depictio ingest` does", "four steps, from the folder on your laptop to a dashboard on the server")
    folder(s, 40, 160, 190, 112, "megatest/", ("on your laptop",))
    xs = (282, 567, 852, 1137)
    for i, x in enumerate(xs):
        badge(s, x + 20, 130, str(i + 1), "you")
        s.arrow((xs[i - 1] + 250 + 6) if i else 236, 215, x - 8, 215, colour=t.muted)

    x = xs[0]
    panel(s, x, 150, 250, 270, "people", "Finds the pipeline", ico="folder-search-outline")
    s.text(x + 18, 225, "reads `pipeline_info/`", size=14, anchor="start", colour=t.dim)
    chip(s, x + 18, 245, 214, "nf-core/ampliseq 2.18.0", "people")
    s.text(x + 18, 315, "and the run's sample", size=14, anchor="start", colour=t.dim)
    s.text(x + 18, 336, "metadata", size=14, anchor="start", colour=t.dim)

    x = xs[1]
    panel(s, x, 150, 250, 270, "people", "Picks the template", ico="file-cog-outline")
    s.text(x + 18, 225, "`nf-core/ampliseq/2.18.0`", size=14, anchor="start")
    s.text(x + 18, 262, "group column `GROUP_COL`", size=14, anchor="start", colour=t.dim)
    rrect(s, x + 18, 276, 214, 32, fill=t.fill("bad"), stroke=edge(t, "bad"), r=8, width=1.2)
    s.text(x + 30, 297, "guessed: `name`", size=14, anchor="start", colour=ink(t, "bad"))
    rrect(s, x + 18, 316, 214, 32, fill=t.fill("you"), stroke=solid(t, "you"), r=8, width=1.6)
    s.text(x + 30, 337, "`--var GROUP_COL=habitat`", size=14, anchor="start", colour=ink(t, "you"), weight="bold")

    x = xs[2]
    panel(s, x, 150, 250, 270, "collection", "Writes the tables", ico="table")
    dc_row(s, x + 14, 210, 222, "taxonomy_composition")
    dc_row(s, x + 14, 256, 222, "ancombc_results")
    rrect(s, x + 14, 302, 222, 40, fill="none", stroke=t.muted, r=8, width=1.3, dash=True)
    s.text(x + 125, 327, "2 optional, empty: SIDLE", size=13, colour=t.dim)
    s.text(x + 125, 380, "25 data collections, 21 links", size=14, weight="bold", colour=ink(t, "collection"))

    dashboard(s, xs[3], 150, 250, 270, "nf-core/ampliseq", tabs=("Overview", "Taxonomy", "…"), active=0, search=False, sub="7 tabs")

    rrect(s, 282, 448, 1105, 52, fill=t.fill("people"), stroke=t.muted, r=10, width=1.3, dash=True)
    icon(s, "clipboard-check-outline", 310, 474, 22, t.dim)
    s.text(332, 480, "`--dry-run`: the same four steps, checked on your laptop; nothing is sent to the server", size=15, anchor="start")
    return s


def project_file(theme: Theme) -> Sketch:
    """Episode 2: one project file, two season folders, two runs of one project."""
    t = theme
    s = new(t, 1440, 610, "One project file, two seasons", "`penguins.yaml` adds a table and a link; each season becomes a run of the same project")

    cb = code_card(s, 40, 110, 420, "penguins.yaml", (
        ("name: Penguins field seasons", None),
        ("workflows:", None),
        ("  - name: field_survey", None),
        ("    data_location:", None),
        ("      structure: flat", None),
        ('      locations: ["{SEASON_DIR}"]', "run"),
        ("    data_collections:", None),
        ("      - physical_features", "collection"),
        ("      - demographic_data", "collection"),
        ("links:", None),
        ("  - demographic_data → physical_features", "link"),
        ("    on individual_id", "link"),
    ))
    s.text(250, cb + 24, "abridged: the full file is in the download", size=13, colour=t.dim)

    cx = 520
    for i, (season, birds, last) in enumerate((("season_2007", "109 birds, the folder of episode 1", "    --update-config"), ("season_2008", "114 birds", "    --attach-run"))):
        y = 112 + i * 240
        badge(s, cx + 382, y - 10, str(i + 1), "you")
        folder(s, cx + 22, y - 10, 360, 70, f"seasons/{season}/", (birds,))
        term(s, cx + 22, y + 74, 380, (f"$ SEASON_DIR=seasons/{season} \\", "    depictio ingest … \\", last), size=13)
    link_line(s, 442, 296, cx + 16, 127)
    link_line(s, 442, 296, cx + 16, 367)

    px = 990
    panel(s, px, 110, 410, 440, "project", "yourname-penguins")
    s.text(px + 18, 185, "Runs", size=15, anchor="start", weight="bold", colour=t.dim)
    for i, (run, rows) in enumerate((("season_2007", "109 rows, the first run"), ("season_2008", "+114 rows"))):
        y = 200 + i * 52
        rrect(s, px + 16, y, 378, 42, fill=t.fill("run"), stroke=edge(t, "run"), r=8, width=1.3)
        icon(s, "folder-play-outline", px + 38, y + 21, 18, solid(t, "run"))
        s.text(px + 56, y + 26, f"`{run}`", size=14, anchor="start", weight="bold")
        s.text(px + 192, y + 26, rows, size=13, anchor="start", colour=t.dim)
        if i:
            button(s, px + 300, y + 6, 84, "Compare", h=30)
    s.arrow(cx + 402, 212, px + 10, 221, colour=solid(t, "run"))
    s.arrow(cx + 402, 452, px + 10, 273, colour=solid(t, "run"))
    s.text(px + 18, 345, "Data collections", size=15, anchor="start", weight="bold", colour=t.dim)
    dc_row(s, px + 16, 362, 250, "demographic_data")
    dc_row(s, px + 16, 470, 250, "physical_features")
    link_line(s, px + 141, 404, px + 141, 466, mid_icon=True)
    s.text(px + 172, 441, "`individual_id`", size=14, anchor="start", colour=ink(t, "link"))
    s.text(px + 300, 446, "223 rows", size=13, anchor="start", colour=t.dim)
    s.text(px + 300, 466, "after both", size=13, anchor="start", colour=t.dim)
    return s


def as_code(theme: Theme) -> Sketch:
    """Episode 3: export a dashboard to YAML, edit it, validate it, import it."""
    t = theme
    s = new(t, 1440, 520, "A dashboard as a file", "export it, change it in a text editor, check it, send it back")

    dashboard(s, 40, 130, 250, 250, "Penguin field survey", tabs=("Overview",), active=0, search=False, value="223", label="Birds measured")
    s.arrow(296, 255, 350, 255, colour=solid(t, "you"))
    s.text(323, 243, "`export`", size=14, colour=ink(t, "you"), weight="bold")

    bottom = code_card(s, 356, 110, 450, "dashboard.yaml", (
        ("title: Penguins, two seasons", "you"),
        ("project_tag: yourname-penguins", None),
        ("components:", None),
        ("-   component_type: card  …", None),
        ("-   component_type: figure", None),
        ("    figure_params: {x: flipper_length_mm, …}", None),
        ("-   component_type: figure", "good"),
        ("    title: Bill length vs flipper length", "good"),
        ("    figure_params: {x: bill_length_mm, …}", "good"),
    ), size=13.5)
    note(s, 374, bottom + 26, ("blue: changed · green: added",))

    vx = 850
    s.arrow(810, 255, vx - 6, 255, colour=solid(t, "you"))
    panel(s, vx, 150, 230, 210, "people", "validate", ico="clipboard-check-outline")
    for i, l in enumerate(("Schema + domain OK", "Server schema OK", "Validation passed")):
        icon(s, "check", vx + 28, 214 + i * 30, 18, solid(t, "good"))
        s.text(vx + 46, 219 + i * 30, l, size=14, anchor="start")
    s.text(vx + 18, 322, "with `--server`: the columns", size=13, anchor="start", colour=t.dim)
    s.text(vx + 18, 341, "of cards and filters too", size=13, anchor="start", colour=t.dim)

    s.arrow(vx + 234, 255, 1134, 255, colour=solid(t, "you"))
    s.text(1109, 243, "`import`", size=14, colour=ink(t, "you"), weight="bold")
    dashboard(s, 1140, 130, 270, 250, "Penguins, two seasons", tabs=("Overview",), active=0, search=False, value="223", label="Birds measured")
    note(s, 1275, 410, ("new title: a new dashboard", "same title: add `--overwrite`"), key="good", anchor="middle")
    return s


if __name__ == "__main__":
    write_themed(cli_flow, OUT, "cli-flow")
    write_themed(ingest_steps, OUT, "ingest-steps")
    write_themed(project_file, OUT, "project-file")
    write_themed(as_code, OUT, "as-code")
