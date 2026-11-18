#!/usr/bin/env python3
"""Dump the depictio CLI command tree to JSON, for render.py.

Runs where depictio is installed (a release image, or a venv): it imports the
Typer app, walks its Click tree and records every command and option. The docs
build never imports depictio; it only reads the JSON this writes.

    python scripts/cli-reference/dump.py -o docs/depictio-cli/cli-reference.json
    python scripts/cli-reference/dump.py -o - > cli-reference.json

Exits non-zero when the tree looks wrong (too few commands or options), so a
release job never commits a broken reference.
"""

from __future__ import annotations

import argparse
import html
import inspect
import json
import os
import re
import sys
from pathlib import Path

SCHEMA = 1
# Floors for the sanity check. v1.21.0 has 46 visible commands and 175 visible options.
MIN_COMMANDS = 35
MIN_OPTIONS = 120

# Rich markup Typer would draw ([bold], [/], [link=...]), not literal brackets
# such as [OPTIONS] or [default: 4].
_RICH_TAG = re.compile(
    r"\[/?(?:bold|b|italic|i|dim|underline|u|code|link(?:=[^\]]*)?|"
    r"(?:bold |dim )?(?:red|green|yellow|blue|magenta|cyan|white|black)|/)\]"
)


def clean(text: str | None) -> str:
    """Help text as a reader sees it: entities unescaped, Click's \\b markers and
    Rich tags dropped, indentation and trailing spaces removed."""
    if not text:
        return ""
    text = html.unescape(inspect.cleandoc(text))
    text = text.replace("\b\n", "").replace("\b", "")
    text = _RICH_TAG.sub("", text)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def jsonable(value):
    """A default as JSON: enums by value, paths and others as strings."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    enum_value = getattr(value, "value", None)
    if enum_value is not None and isinstance(enum_value, (str, int, float)):
        return enum_value
    return str(value)


def plain(value):
    """Typer wraps unset settings (rich_help_panel...) in DefaultPlaceholder."""
    if type(value).__name__ == "DefaultPlaceholder":
        value = value.value
    return value if isinstance(value, str) or value is None else str(value)


def param_type(param) -> dict:
    t = param.type
    out = {"name": getattr(t, "name", type(t).__name__).lower()}
    choices = getattr(t, "choices", None)
    if choices:
        out["choices"] = [jsonable(c) for c in choices]
    if getattr(param, "count", False):
        out["name"] = "count"
    return out


def dump_param(param) -> dict:
    is_argument = param.param_type_name == "argument"
    default = param.default
    # Click's sentinel for "no default", and callables (dynamic defaults).
    if callable(default) or type(default).__name__ in ("_Missing", "Sentinel"):
        default = None
    entry = {
        "name": param.name,
        "kind": "argument" if is_argument else "option",
        "opts": list(param.opts),
        "secondary_opts": list(getattr(param, "secondary_opts", []) or []),
        "type": param_type(param),
        "required": bool(param.required),
        "multiple": bool(getattr(param, "multiple", False)) or param.nargs == -1,
        "nargs": param.nargs,
        "default": jsonable(default),
        "metavar": getattr(param, "metavar", None),
        "help": clean(getattr(param, "help", None)),
        "hidden": bool(getattr(param, "hidden", False)),
        "deprecated": bool(getattr(param, "deprecated", False)),
        "envvar": jsonable(getattr(param, "envvar", None)),
        "panel": plain(getattr(param, "rich_help_panel", None)),
    }
    if not is_argument:
        entry["is_flag"] = bool(getattr(param, "is_flag", False))
        entry["count"] = bool(getattr(param, "count", False))
        show_default = getattr(param, "show_default", None)
        entry["show_default"] = show_default if isinstance(show_default, (bool, str)) else None
    return entry


def callback_key(cmd):
    callback = getattr(cmd, "callback", None)
    return inspect.unwrap(callback) if callback else None


def walk(cmd, path: list[str], parent_hidden: bool, out: list[dict]) -> None:
    hidden = parent_hidden or bool(getattr(cmd, "hidden", False))
    is_group = hasattr(cmd, "commands")
    params = [
        dump_param(p)
        for p in cmd.params
        if p.name != "help" and "--help" not in getattr(p, "opts", ())
    ]
    out.append(
        {
            "path": path,
            "name": path[-1] if path else "depictio",
            "group": is_group,
            "help": clean(cmd.help),
            "short_help": clean(cmd.short_help)
            or clean(cmd.help).split("\n\n")[0].replace("\n", " "),
            "epilog": clean(getattr(cmd, "epilog", None)),
            "hidden": hidden,
            "deprecated": bool(getattr(cmd, "deprecated", False)),
            "panel": plain(getattr(cmd, "rich_help_panel", None)),
            "params": params,
            "_callback": callback_key(cmd),
        }
    )
    if is_group:
        # list_commands keeps the order --help shows (the root sorts by panel).
        names = cmd.list_commands(None)
        for name in names:
            walk(cmd.commands[name], [*path, name], hidden, out)


def link_aliases(commands: list[dict]) -> None:
    """A hidden command running the same function as a visible one is its former
    name: record it on both sides."""
    visible = {}
    for c in commands:
        if not c["hidden"] and c["_callback"] is not None and not c["group"]:
            visible.setdefault(c["_callback"], c)
    for c in commands:
        target = visible.get(c["_callback"]) if c["hidden"] else None
        c["alias_of"] = target["path"] if target else None
        if target:
            target.setdefault("aliases", []).append(c["path"])
    for c in commands:
        c.setdefault("aliases", [])
        del c["_callback"]


def version_of_depictio() -> str:
    try:
        from depictio.version import get_version

        return get_version()
    except Exception:  # noqa: BLE001 - any failure falls back to the metadata
        from importlib.metadata import version

        return version("depictio")


def validate(data: dict) -> list[str]:
    errors = []
    visible = [c for c in data["commands"] if not c["hidden"] and c["path"]]
    options = sum(
        1 for c in visible for p in c["params"] if p["kind"] == "option" and not p["hidden"]
    )
    if len(visible) < MIN_COMMANDS:
        errors.append(f"only {len(visible)} visible commands (expected >= {MIN_COMMANDS})")
    if options < MIN_OPTIONS:
        errors.append(f"only {options} visible options (expected >= {MIN_OPTIONS})")
    for required in (["ingest"], ["watch"], ["data", "scan"]):
        if not any(c["path"] == required for c in visible):
            errors.append(f"missing command: depictio {' '.join(required)}")
    if not re.match(r"^\d+\.\d+\.\d+", data["version"]):
        errors.append(f"unexpected version {data['version']!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "-o", "--out", default="docs/depictio-cli/cli-reference.json", help="file, or - for stdout"
    )
    parser.add_argument("--version", help="override the recorded depictio version")
    args = parser.parse_args()

    # Quiet imports, and no telemetry from a docs job.
    os.environ.setdefault("DEPICTIO_TELEMETRY_ENABLED", "false")
    from typer.main import get_command

    from depictio.cli.depictio_cli import app

    root = get_command(app)
    commands: list[dict] = []
    walk(root, [], False, commands)
    link_aliases(commands)
    data = {
        "schema": SCHEMA,
        "program": "depictio",
        "version": (args.version or version_of_depictio()).lstrip("v"),
        "help_options": list(
            (root.context_settings or {}).get("help_option_names", ["--help"])
        ),
        "commands": commands,
    }
    errors = validate(data)
    if errors:
        for e in errors:
            print(f"dump.py: {e}", file=sys.stderr)
        return 1

    text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    if args.out == "-":
        sys.stdout.write(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
    visible = [c for c in commands if not c["hidden"] and c["path"]]
    print(
        f"dump.py: depictio {data['version']}, {len(visible)} commands, "
        f"{sum(len(c['params']) for c in visible)} parameters",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
