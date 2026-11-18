#!/usr/bin/env python3
"""Render the depictio command reference page from the JSON dump.py writes.

Standard library only: the docs build and the pre-commit hook run it without
depictio installed. The same JSON always gives the same bytes.

    python scripts/cli-reference/render.py            # write docs/depictio-cli/usage.md
    python scripts/cli-reference/render.py --check    # exit 1 if usage.md is stale

What the --help text cannot say lives here (icons, colours, guide links, the
anchors other pages link to) or in the hand-written notes under
docs/depictio-cli/_notes/, which the page includes with pymdownx.snippets.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "docs/depictio-cli/cli-reference.json"
PAGE_PATH = ROOT / "docs/depictio-cli/usage.md"
NOTES_DIR = ROOT / "docs/depictio-cli/_notes"
# Snippet paths are relative to the snippets base_path, docs/.
NOTES_SNIPPET = "depictio-cli/_notes/{}.md"

MIN_COMMANDS = 35
MIN_OPTIONS = 120
# Options tables split into --help panels from this many parameters on.
PANEL_MIN = 12

# Top-level commands: icon (Material), accent (cards.css .dp-*), guide links.
# Order is the CLI's own (its --help panels); anything new lands at the end.
GROUPS: dict[str, dict] = {
    "local": {"icon": "laptop", "accent": "yellow",
              "guide": [("Python package", "../installation/local.md")]},
    "ingest": {"icon": "database-import", "accent": "purple",
               "guide": [("Common tasks", "tasks.md#ingest-results"),
                         ("Composed dashboards", "../usage/projects/composed-dashboards.md")]},
    "watch": {"icon": "eye-refresh", "accent": "violet",
              "guide": [("Watch a folder", "tasks.md#watch-a-folder"),
                        ("Watchers pane", "../usage/administration/monitoring.md#watchers")]},
    "config": {"icon": "tune-variant", "accent": "green",
               "guide": [("Install and configure", "../installation/cli.md")]},
    "data": {"icon": "database-cog", "accent": "teal",
             "guide": [("Data versions", "../features/versioning.md")]},
    "dashboard": {"icon": "view-dashboard-edit", "accent": "blue",
                  "guide": [("Dashboard YAML", "../features/yaml-sync.md")]},
    "template": {"icon": "layers-outline", "accent": "orange",
                 "guide": [("Templates", "../usage/projects/templates.md")]},
    "project-builder": {"icon": "hammer-wrench", "accent": "pink",
                        "guide": [("Project Builder", "../usage/projects/guide.md#project-builder")]},
    "manifest": {"icon": "file-table-outline", "accent": "violet",
                 "guide": [("Remote data and manifests",
                            "../usage/projects/remote-data.md#the-data-manifest-contract")]},
    "migrate": {"icon": "swap-horizontal-bold", "accent": "red",
                "guide": [("Project migration", "../usage/administration/migrate.md")]},
    "backup": {"icon": "backup-restore", "accent": "red",
               "guide": [("Backup and restore", "../usage/administration/backup.md")]},
    "catalog": {"icon": "bookshelf", "accent": "blue",
                "guide": [("Tools catalog", "../catalog/index.md")]},
}
# Small top-level commands, gathered in one section rather than one each.
MISC = ("commands", "version")
MISC_SECTION = ("Other commands", "other-commands", "console-line", "purple")
DEFAULT_GROUP = {"icon": "console-line", "accent": "purple", "guide": []}

# Guide links for subcommands, by command path.
SEE_ALSO: dict[str, list[tuple[str, str]]] = {
    "config nextflow": [("Nextflow trigger", "nextflow-trigger.md")],
    "data join": [("Cross-DC filtering", "../features/cross-dc-filtering.md")],
    "data versions": [("Dataset history", "../features/versioning.md#dataset-history")],
    "data vacuum": [("Data versions", "../features/versioning.md#data-versions")],
    "template export": [("Export a project as a template",
                         "../usage/projects/templates.md#export-a-project-as-a-template")],
    "template compose": [("Composed dashboards",
                          "../usage/projects/composed-dashboards.md#template-compose")],
}

# Hand-written notes, included after a command's options (a path) or after the
# global options ("").
NOTES = {"": "servers", "ingest": "ingest", "watch": "watch", "catalog": "catalog"}

# Anchors other pages link to, kept as aliases of the generated ids.
ANCHOR_ALIASES = {
    "ingest-command": "ingest",
    "run-command": "ingest",
    "watch-command": "watch",
    "local-commands": "local",
    "config-commands": "config",
    "data-commands": "data",
    "dashboard-commands": "dashboard",
    "template-commands": "template",
    "manifest-commands": "manifest",
    "catalog-commands": "catalog",
    "backup-commands": "backup",
    "migrate-commands": "migrate",
    "skipping-steps": "ingest-skip",
    "recipe-commands": "former-names",
}

# Former option names, out of --help: what replaced them. Keys are an option,
# or "command path option" when it depends on the command.
RENAMED = {
    "--CLI-config-path": "`--server`",
    "--config": "`--server`",
    "--api": "`--server`",
    "--target-config": "`--to-server`",
    "--verbose-level": "`--log-level`",
    "ingest --project-name": "`--project`",
    "ingest --data-root": "`DATA_DIR`",
    "ingest --overwrite": "`--update-config`",
    "ingest --rescan-folders": "`--update-config`",
    "ingest --sync-files": "`--update-config`",
    "ingest --legacy-scan-depth": "nothing; to be removed",
    "ingest --skip-*": "`--skip STEP`",
    "run --*": "as for `ingest`",
    "template export --data-root": "`--data-dir`",
    "local up --*": "`ingest --server local`",
}

TYPE_NAMES = {
    "str": "text", "text": "text", "string": "text", "path": "path", "file": "file",
    "filename": "file", "int": "integer", "integer": "integer", "int range": "integer",
    "integer range": "integer", "float": "number", "float range": "number",
    "boolean": "flag", "bool": "flag", "count": "count", "uuid": "uuid", "choice": "choice",
}

BANNER = (
    "<!-- GENERATED by scripts/cli-reference/render.py from cli-reference.json. Do not edit:\n"
    "     see scripts/cli-reference/README.md to refresh it. -->"
)


# --- Text -------------------------------------------------------------------

_CODE_SPAN = re.compile(r"(`+)(.+?)\1", re.S)
_CODEISH = re.compile(
    # --flag, -v, -vl/--verbose-level, and a value in capitals: --skip STEP, --var K=V
    r"(?<![\w`/.-])(--?[A-Za-z][\w-]*(?:/--?[A-Za-z][\w-]*)?"
    r"(?: [A-Z][A-Z_]*=[^\s,;)`]+| [A-Z][A-Z_]{2,}\b(?![.,]?\w))?)"
    r"|(\{[A-Z_]+\})"  # {DATA_ROOT}
    r"|(<[^<>\n`]{1,40}>)"  # <results dir>
    r"|(\$[A-Z][A-Z0-9_]+)"  # $DEPICTIO_CLI_CONFIG_PATH
    r"|((?<![\w`])~/[^\s,;)`]*[^\s,;).`])"  # ~/.depictio/CLI.yaml
    r"|((?<![\w`])(?:s3|https?)://[^\s,;)`']*[^\s,;).`'])"  # s3://bucket/run42
    r"|(?<![\w`])'([^'\s]+)'(?!\w)"  # 'local', 'stats/*.tsv'
)


def inline(text: str, cell: bool = False) -> str:
    """Prose from --help as Markdown: option names, placeholders, variables and
    paths in code; *, < and (in tables) | escaped elsewhere. The docs use no
    em dash, so one in the help becomes a comma."""
    text = text.replace(" \u2014 ", ", ").replace("\u2014", ", ")
    out = []
    pos = 0
    for m in _CODE_SPAN.finditer(text):
        out.append(_prose(text[pos:m.start()], cell))
        out.append(m.group(0).replace("|", "\\|") if cell else m.group(0))
        pos = m.end()
    out.append(_prose(text[pos:], cell))
    return "".join(out)


def _prose(text: str, cell: bool) -> str:
    out = []
    pos = 0
    for m in _CODEISH.finditer(text):
        out.append(_escape(text[pos:m.start()], cell))
        token = m.group(7) or m.group(0)  # a quoted token loses its quotes
        out.append(f"`{token}`")
        pos = m.end()
    out.append(_escape(text[pos:], cell))
    return "".join(out)


def _escape(text: str, cell: bool) -> str:
    text = text.replace("*", "\\*").replace("<", "&lt;")
    return text.replace("|", "\\|") if cell else text


def one_line(text: str) -> str:
    return " ".join(text.split())


_LIST_ITEM = re.compile(r"^(\d+\.|-)\s+")
_KEY_VALUE = re.compile(r"^(\S+)\s*:\s+(.*)$")
_DOC_SECTION = re.compile(r"^(Args|Arguments|Returns|Raises):\s*$")


def help_blocks(text: str) -> list[str]:
    """The help of a command as Markdown blocks: paragraphs, lists, code and a
    warning admonition, from Click's plain text."""
    lines = text.splitlines()
    # Docstring sections Typer leaves in the help (Args: ...) repeat the options.
    kept, skipping = [], False
    for line in lines:
        if _DOC_SECTION.match(line):
            skipping = True
            continue
        if skipping and (not line.strip() or line[:1].isspace()):
            continue
        skipping = False
        kept.append(line)
    lines = kept

    blocks: list[str] = []
    para: list[str] = []
    indented: list[str] = []

    def flush_para():
        if para:
            blocks.extend(_text_block(para))
            para.clear()

    def flush_indented():
        while indented and not indented[-1].strip():
            indented.pop()
        if indented:
            blocks.append(_indented_block(indented))
            indented.clear()

    for i, line in enumerate(lines):
        if not line.strip():
            if indented:
                # A blank line inside an example block, if more of it follows.
                rest = next((l for l in lines[i + 1:] if l.strip()), "")
                if rest[:1].isspace():
                    indented.append("")
                    continue
                flush_indented()
            flush_para()
            continue
        if line[:1].isspace():
            if para and not indented and _LIST_ITEM.match(para[-1].lstrip()) or (
                para and not indented and _LIST_ITEM.match(para[0])
            ):
                para.append(line.strip())  # continuation of a list item
                continue
            flush_para()
            indented.append(line)
            continue
        flush_indented()
        para.append(line)
    flush_indented()
    flush_para()
    return blocks


def _text_block(lines: list[str]) -> list[str]:
    """Lines of one paragraph: an intro, then list items if any."""
    intro: list[str] = []
    items: list[list[str]] = []
    for line in lines:
        m = _LIST_ITEM.match(line)
        if m:
            items.append([line])
        elif items:
            items[-1].append(line.strip())
        else:
            intro.append(line)
    out = []
    if intro:
        text = one_line(" ".join(intro))
        m = re.match(r"^(WARNING|Warning|NOTE|Note):\s*(.*)$", text)
        if m:
            kind = "warning" if m.group(1).lower() == "warning" else "note"
            out.append(f"!!! {kind}\n\n    {inline(m.group(2))}")
        else:
            # "Then add data with: depictio ingest <results dir> --server local"
            m = re.match(r"^(.*:\s)(depictio\s[^`]+)$", text)
            out.append(inline(m.group(1)) + f"`{m.group(2)}`" if m else inline(text))
    if items:
        rendered = []
        for item in items:
            marker = _LIST_ITEM.match(item[0]).group(1)
            body = one_line(" ".join([item[0][len(_LIST_ITEM.match(item[0]).group(0)):]] + item[1:]))
            rendered.append(f"{'-' if marker == '-' else marker} {inline(body)}")
        out.append("\n".join(rendered))
    return out


def _indented_block(lines: list[str]) -> str:
    nonblank = [l for l in lines if l.strip()]
    indent = min(len(l) - len(l.lstrip()) for l in nonblank)
    body = [l[indent:] for l in lines]
    stripped = [l.strip() for l in nonblank]
    if all(_LIST_ITEM.match(l) for l in stripped):
        return "\n".join(inline(one_line(l)) for l in stripped)
    if all(_KEY_VALUE.match(l) for l in stripped):
        rows = []
        for l in stripped:
            key, value = _KEY_VALUE.match(l).groups()
            rows.append(f"- `{key}`: {inline(one_line(value))}")
        return "\n".join(rows)
    return "```bash\n" + "\n".join(body) + "\n```"


# --- Commands and options ---------------------------------------------------


def cmd_id(path: list[str]) -> str:
    return "-".join(path) if path else "depictio"


def visible_params(cmd: dict) -> list[dict]:
    return [p for p in cmd["params"] if not p["hidden"]]


def type_label(p: dict) -> str:
    t = p["type"]
    if p.get("count"):
        return "count"
    if p.get("is_flag"):
        return "flag"
    return TYPE_NAMES.get(t["name"], t["name"])


def default_label(p: dict) -> str:
    d = p["default"]
    if p.get("show_default") is False:
        return ""
    if p.get("is_flag"):
        if p["secondary_opts"]:
            return "on" if d else "off"
        return "on" if d else ""
    if p.get("count") or d in (None, "", [], ()):
        return ""
    if isinstance(d, float) and d.is_integer():
        d = int(d)
    if isinstance(d, list):
        d = ",".join(str(x) for x in d)
    return f"`{d}`"


def flag_html(opts: list[str], anchor: str | None = None) -> str:
    # Long names first, as --help shows them.
    ordered = sorted(opts, key=lambda o: (not o.startswith("--"), opts.index(o)))
    pills = []
    for i, o in enumerate(ordered):
        attr = f' id="{anchor}"' if anchor and i == 0 else ""
        short = "" if o.startswith("--") else " dp-short"
        pills.append(f'<code class="dp-flag{short}"{attr}>{html.escape(o)}</code>')
    return " ".join(pills)


def option_row(cmd: dict, p: dict, ids: set[str]) -> str:
    cid = cmd_id(cmd["path"])
    badges = []
    if p["kind"] == "argument":
        name = p["metavar"] or p["name"].upper()
        anchor = f"{cid}-{p['name'].replace('_', '-')}"
        first = f'<code class="dp-arg" id="{anchor}">{html.escape(name)}</code>'
        if p["required"]:
            badges.append('<span class="dp-badge dp-req">required</span>')
    else:
        long = next((o for o in p["opts"] if o.startswith("--")), p["opts"][0])
        anchor = f"{cid}-{long.lstrip('-')}"
        first = flag_html(p["opts"], anchor)
        if p["secondary_opts"]:
            first += ' <span class="dp-sep">/</span> ' + flag_html(p["secondary_opts"])
        if p["required"]:
            badges.append('<span class="dp-badge dp-req">required</span>')
    if p.get("deprecated"):
        badges.append('<span class="dp-badge dp-dep">deprecated</span>')
    if anchor in ids:
        raise SystemExit(f"render.py: duplicate anchor #{anchor}")
    ids.add(anchor)

    choices = p["type"].get("choices")
    if choices:
        chips = " ".join(f'<code class="dp-choice">{html.escape(str(c))}</code>' for c in choices)
        kind = f'<span class="dp-choices">{chips}</span>'
    else:
        label = type_label(p)
        metavar = p["metavar"] if p["kind"] == "option" else None
        if metavar and label not in ("flag", "count"):
            label = metavar
        kind = f'<span class="dp-type">{html.escape(label.strip("<>").lower() if metavar else label)}</span>'
    if p["multiple"]:
        kind += ' <span class="dp-type dp-multi">repeatable</span>'

    desc = one_line(p["help"])
    if p["opts"][:1] == ["--server"] and desc.startswith("Server to use:"):
        desc = inline(desc.split(" Default:")[0].replace("Server to use: ", "").rstrip("."), True)
        desc = desc[:1].upper() + desc[1:] + ". See [Which server a command uses](#choosing-a-server)."
    else:
        desc = inline(desc, True)
    envvars = p["envvar"] if isinstance(p["envvar"], list) else [p["envvar"]] if p["envvar"] else []
    for env in envvars:
        desc += f' <span class="dp-env">env <code>{html.escape(env)}</code></span>'
    spans = "".join(f'<span id="{a}"></span>' for a in aliases_for(anchor))
    cell = spans + first + ("<br>" + " ".join(badges) if badges else "")
    return f"| {cell} | {kind} | {default_label(p)} | {desc} |"


def options_table(cmd: dict, ids: set[str]) -> list[str]:
    params = visible_params(cmd)
    if not params:
        return []
    # A long list is split into the panels --help shows (ingest's), unpanelled
    # options and arguments first; a short one stays one table.
    panels: dict[str | None, list[dict]] = {}
    for p in params:
        key = None if p["kind"] == "argument" or len(params) <= PANEL_MIN else p["panel"]
        panels.setdefault(key, []).append(p)
    out = []
    head = "| Option | Type | Default | Description |\n| --- | --- | --- | --- |"
    for panel, rows in panels.items():
        if panel and len(panels) > 1:
            out.append(f"**{panel}**\n{{ .dp-cli-panel }}")
        out.append(head + "\n" + "\n".join(option_row(cmd, p, ids) for p in rows))
    return out


def signature(cmd: dict) -> str:
    parts = ["depictio", *cmd["path"]]
    params = visible_params(cmd)
    for p in params:
        if p["kind"] == "option" and p["required"]:
            mv = p["metavar"] or p["name"].upper()
            parts.append(f"{p['opts'][0]} {mv}")
    if any(p["kind"] == "option" and not p["required"] for p in params):
        parts.append("[OPTIONS]")
    for p in params:
        if p["kind"] == "argument":
            name = p["metavar"] or p["name"].upper()
            name += "..." if p["multiple"] else ""
            parts.append(name if p["required"] else f"[{name}]")
    if cmd["group"]:
        parts.append("COMMAND [ARGS]...")
    return " ".join(parts)


def guide_line(links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    joined = " · ".join(f"[{label}]({url})" for label, url in links)
    return f":material-book-open-page-variant: {joined}\n{{ .dp-cli-see }}"


def note(key: str) -> list[str]:
    name = NOTES.get(key)
    if not name:
        return []
    if not (NOTES_DIR / f"{name}.md").is_file():
        raise SystemExit(f"render.py: missing note {NOTES_DIR / name}.md")
    return [f'--8<-- "{NOTES_SNIPPET.format(name)}"']


def aliases_for(target: str) -> list[str]:
    return sorted(a for a, t in ANCHOR_ALIASES.items() if t == target)


def heading(level: int, text: str, anchor: str, classes: str = "") -> str:
    spans = "".join(f'<span id="{a}"></span>' for a in aliases_for(anchor))
    attrs = f"#{anchor}" + (f" {classes}" if classes else "")
    # After the icon: doc-sections.js copies a heading's leading icon into the TOC.
    icon, sep, rest = text.partition(": ")
    if sep and icon.startswith(":material-"):
        return f"{'#' * level} {icon}: {spans}{rest} {{ {attrs} }}"
    return f"{'#' * level} {spans}{text} {{ {attrs} }}"


def command_body(cmd: dict, accent: str, ids: set[str]) -> list[str]:
    out = [f"``` {{ .text .dp-cli-sig .dp-{accent} }}\n{signature(cmd)}\n```"]
    if cmd["aliases"]:
        former = ", ".join(f"`depictio {' '.join(a)}`" for a in cmd["aliases"])
        out.append(f"Also {former}, its former name.\n{{ .dp-cli-also }}")
    out.extend(help_blocks(cmd["help"]))
    out.extend(options_table(cmd, ids))
    return out


def render(data: dict) -> str:
    commands = data["commands"]
    by_path = {" ".join(c["path"]): c for c in commands}
    root = by_path[""]
    top = [c for c in commands if len(c["path"]) == 1 and not c["hidden"]]
    ids: set[str] = set()
    version = data["version"]

    out = [
        "---\ntitle: Command reference\n"
        f"description: Every depictio {version} command and option, generated from its --help.\n---",
        BANNER,
        "# :material-book-open-variant: Command reference { .dp-cli-title }",
        f"Every command and option of `depictio` {version}, generated from its `--help`; "
        "`depictio <command> -h` prints the same. `depictio` alone prints a quick start, and "
        "`depictio-cli` is the same command. For step-by-step use, see [Common tasks](tasks.md). "
        "Scripts and AI agents can read the same reference as JSON: "
        "[`cli-reference.json`](cli-reference.json){ download }.",
    ]

    # Overview grid, one card per top-level command.
    out.append(heading(2, "Overview", "quick-reference"))
    cards = []
    for c in top:
        name = c["name"]
        if name in MISC:
            continue
        g = GROUPS.get(name, DEFAULT_GROUP)
        subs = [s["name"] for s in commands
                if s["path"][:1] == [name] and len(s["path"]) == 2 and not s["hidden"]]
        card = [
            f"-   :material-{g['icon']}:{{ .lg .middle .dp-{g['accent']} }} "
            f"**[`{name}`](#{cmd_id(c['path'])})**",
            "",
            "    ---",
            "",
            f"    {inline(one_line(c['short_help']))}",
        ]
        if subs:
            card += ["", "    " + " ".join(f"`{s}`" for s in subs)]
        cards.append("\n".join(card))
    out.append('<div class="grid cards dp-cli-overview" markdown>\n\n' + "\n\n".join(cards) + "\n\n</div>")
    misc = [c for c in top if c["name"] in MISC]
    if misc:
        names = " and ".join(f"[`{c['name']}`](#{cmd_id(c['path'])})" for c in misc)
        out.append(f"Also {names}.")

    # Global options.
    out.append(heading(2, "Global options", "global-options"))
    out.append(f"They go before the command: `depictio -vv ingest results/`.")
    out.extend(options_table(root, ids))
    helps = data.get("help_options") or ["--help"]
    out.append(f"{' and '.join(f'`{h}`' for h in sorted(helps, key=len))} show any command's help.")
    out.extend(note(""))

    # One section per top-level command, in the CLI's order.
    for c in top:
        if c["name"] in MISC:
            continue
        g = GROUPS.get(c["name"], DEFAULT_GROUP)
        cid = cmd_id(c["path"])
        ids.add(cid)
        title = f":material-{g['icon']}: `{c['name']}`"
        out.append(heading(2, title, cid, f".dp-cli-group .dp-{g['accent']}"))
        if c["group"]:
            out.append(f"{inline(one_line(c['short_help']))}\n{{ .dp-cli-lede }}")
            if g["guide"]:
                out.append(guide_line(g["guide"]))
            for s in commands:
                if s["path"][:1] != c["path"] or len(s["path"]) != 2 or s["hidden"]:
                    continue
                sid = cmd_id(s["path"])
                ids.add(sid)
                out.append(heading(3, f"`{' '.join(s['path'])}`", sid, f".dp-cli-cmd .dp-{g['accent']}"))
                out.extend(command_body(s, g["accent"], ids))
                out.append(guide_line(SEE_ALSO.get(" ".join(s["path"]), [])))
                out.extend(note(" ".join(s["path"])))
        else:
            out.extend(command_body(c, g["accent"], ids))
            if g["guide"]:
                out.append(guide_line(g["guide"]))
        out.extend(note(c["name"]))

    if misc:
        label, anchor, icon, accent = MISC_SECTION
        out.append(heading(2, f":material-{icon}: {label}", anchor, f".dp-cli-group .dp-{accent}"))
        for c in misc:
            cid = cmd_id(c["path"])
            ids.add(cid)
            out.append(heading(3, f"`{c['name']}`", cid, f".dp-cli-cmd .dp-{accent}"))
            out.extend(command_body(c, accent, ids))

    out.extend(former_names(commands))
    text = "\n\n".join(block for block in out if block).rstrip() + "\n"
    check_anchors(ids)
    return text


def renamed_to(path: str, opt: str) -> str:
    for key in (f"{path} {opt}", opt):
        if key in RENAMED:
            return RENAMED[key]
    for key, value in RENAMED.items():
        prefix, _, pattern = key.rpartition(" ")
        if pattern.endswith("*") and opt.startswith(pattern[:-1]) and prefix in ("", path):
            return value
    return ""


def former_names(commands: list[dict]) -> list[str]:
    rows: dict[tuple[str, str], list[str]] = {}
    for c in commands:
        if c.get("alias_of"):
            rows.setdefault((f"`{' '.join(c['path'])}`", f"`{' '.join(c['alias_of'])}`"), [])
    for c in commands:
        path = " ".join(c["path"])
        if c["hidden"] and not c.get("alias_of") and path != "run":
            continue
        if c.get("alias_of"):
            continue
        for p in c["params"]:
            if not p["hidden"] or p["kind"] != "option":
                continue
            former = ", ".join(p["opts"] + p["secondary_opts"])
            now = renamed_to(path, p["opts"][0]) or renamed_to(path, p["opts"][-1])
            where = rows.setdefault((f"`{former}`", now), [])
            where.append(f"`{path or 'depictio'}`")
    table = ["| Former | Now | In |", "| --- | --- | --- |"]
    for (former, now), where in sorted(rows.items(), key=lambda kv: (kv[0][0].lower(), kv[0][1])):
        table.append(f"| {former} | {now} | {', '.join(sorted(set(where)))} |")
    hidden_rows = []
    for c in commands:
        if not c["hidden"] or c.get("alias_of") or c["group"]:
            continue
        does = re.split(r"(?<=\.)\s", one_line(c["short_help"]))[0]
        hidden_rows.append(f"| `depictio {' '.join(c['path'])}` | {inline(does, True)} |")
    out = [heading(2, "Former names and maintainer commands", "former-names")]
    out.append(
        '??? note "Former names, still accepted"\n\n'
        "    They are out of `--help` and print what replaced them.\n\n"
        + "\n".join(f"    {row}" for row in table)
    )
    if hidden_rows:
        out.append(
            '??? note "Maintainer commands, out of `--help`"\n\n'
            "    For catalog authoring, recipe tests and CI. They may change without notice.\n\n"
            "    | Command | Does |\n    | --- | --- |\n"
            + "\n".join(f"    {row}" for row in hidden_rows)
        )
    return out


def check_anchors(ids: set[str]) -> None:
    missing = [f"#{a} -> #{t}" for a, t in ANCHOR_ALIASES.items() if t not in ids | {"former-names"}]
    if missing:
        raise SystemExit("render.py: alias targets missing: " + ", ".join(missing))


def validate(data: dict, text: str) -> list[str]:
    errors = []
    if data.get("schema") != 1:
        errors.append(f"unknown schema {data.get('schema')!r}")
    visible = [c for c in data["commands"] if c["path"] and not c["hidden"]]
    options = sum(1 for c in visible for p in c["params"] if p["kind"] == "option" and not p["hidden"])
    if len(visible) < MIN_COMMANDS:
        errors.append(f"only {len(visible)} commands (expected >= {MIN_COMMANDS})")
    if options < MIN_OPTIONS:
        errors.append(f"only {options} options (expected >= {MIN_OPTIONS})")
    for c in visible:
        if not c["group"] and f"{{ #{cmd_id(c['path'])}" not in text:
            errors.append(f"depictio {' '.join(c['path'])} has no section")
    if "—" in text:
        errors.append("an em dash slipped into the page")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", type=Path, default=JSON_PATH)
    parser.add_argument("--out", type=Path, default=PAGE_PATH)
    parser.add_argument("--check", action="store_true", help="fail if --out differs, write nothing")
    args = parser.parse_args()

    data = json.loads(args.json.read_text(encoding="utf-8"))
    text = render(data)
    errors = validate(data, text)
    if errors:
        for e in errors:
            print(f"render.py: {e}", file=sys.stderr)
        return 1
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.exists() else ""
        if current != text:
            print(
                f"render.py: {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}"
                " is out of date with its JSON or was edited by hand.\n"
                "  Run: python scripts/cli-reference/render.py",
                file=sys.stderr,
            )
            return 1
        return 0
    args.out.write_text(text, encoding="utf-8")
    visible = [c for c in data["commands"] if c["path"] and not c["hidden"]]
    print(f"render.py: wrote {args.out.name}, {len(visible)} commands, depictio {data['version']}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
