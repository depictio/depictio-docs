#!/usr/bin/env python3
"""The figures on the Security page.

    uv run python dev/diagrams/security.py

Writes into ``docs/images/security/``:

- ``sign-in_{light,dark}``: the three ways to a token, and the checks on every
  request;
- ``access_{light,dark}``: how a user's role on a project and a dashboard is
  resolved;
- ``code-figure_{light,dark}``: what a code-mode figure goes through.

Read from depictio v1.21.0. Sign-in: ``user_endpoints/routes.py`` (``/auth/login``
behind a Redis rate limit, ``/auth/refresh``, ``/generate_agent_config``),
``auth_endpoints/oidc_routes.py`` (code flow with PKCE, a 2-minute single-use
ticket in the URL fragment), ``core_functions._add_token`` (short-lived: 1 h
access, 7 days refresh; long-lived CLI: 1 year) and
``_async_fetch_user_from_token`` (signature with the public key, algorithm
pinned, ``exp`` required, then the token must still be in MongoDB). The viewer
keeps the pair in local storage (``packages/depictio-react-core/src/api.ts``).
Access: ``depictio/api/v1/permissions.py`` (sysadmins pass; highest of direct and
group roles; public means a viewer floor; anonymous users see public documents
only) and ``dashboards_endpoints/routes.py`` (a dashboard's own owners and editors
keep that role). Code figures: ``services/figure/code_executor.py``
(RestrictedPython ``compile_restricted``, guarded globals, ``df.clone()``, the
audit hook) and ``celery_dispatch.should_offload_render`` (code mode always runs
on the worker).
"""

from __future__ import annotations

from pathlib import Path

from brand import badge, card, chip, edge, ink, lines, new, panel, solid, tint
from concepts import icon, raw, rrect, white
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "security"


def label(s: Sketch, x: float, y: float, text: str, *, anchor: str = "middle", size: float = 12.5) -> None:
    s.text(x, y, text, size=size, anchor=anchor, colour=s.theme.dim)


def sign_in(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 520, "Signing in, then every request", "signed tokens, checked on every call, and revoked by deleting them")
    arrow = t.dim

    # Three ways to a token.
    s.text(30, 112, "Three ways in", size=15, anchor="start", weight="bold")
    card(s, 30, 126, 290, 92, "blue", "key-outline", "Password", ("POST `/auth/login`, rate-limited", "per address"), size=13.5)
    card(s, 30, 230, 290, 92, "purple", "shield-account-outline", "Single sign-on", ("OpenID Connect with PKCE, then", "a 2-minute, single-use ticket"), size=13.5, dashed=True)
    card(s, 30, 334, 290, 92, "teal", "console", "CLI token", ("made in Account settings, kept", "in `~/.depictio/CLI.yaml`"), size=13.5)

    # The API signs a pair and records it.
    panel(s, 372, 126, 236, 300, "blue", "The API signs", "key-outline")
    lines(s, 388, 194, ("with its private key, RS256", "by default"), size=13.5)
    lines(s, 388, 254, ("browser session", "access token: 1 hour", "refresh token: 7 days"), first_bold=True, size=13.5)
    lines(s, 388, 330, ("CLI", "1 year"), first_bold=True, size=13.5)
    rrect(s, 384, 372, 212, 40, fill=tint(t, "green"), stroke=edge(t, "green"), r=8, width=1.2)
    icon(s, "database-outline", 402, 392, 17, solid(t, "green"))
    s.text(418, 397, "kept in MongoDB `tokens`", size=13.5, anchor="start", colour=ink(t, "green"))
    for y in (172, 276, 380):
        s.arrow(320, y, 372, y + (276 - y) * 0.25, colour=arrow)

    # Every request.
    panel(s, 660, 126, 270, 300, "violet", "Every request", "shield-check-outline")
    steps = (
        ("1", ("`Authorization: Bearer`", "carries the access token")),
        ("2", ("signature and `exp` checked,", "the algorithm pinned")),
        ("3", ("still in MongoDB? Deleting", "a token revokes it")),
        ("4", ("the user, then their role", "on what they asked for")),
    )
    for i, (n, rows) in enumerate(steps):
        y = 194 + i * 58
        badge(s, 684, y - 5, n, "violet", r=11)
        lines(s, 704, y, rows, size=13.5, step=19, colour=t.ink)
    s.arrow(608, 276, 660, 276, colour=arrow)
    label(s, 634, 266, "token")

    lines(s, 30, 466, (
        "The browser keeps the pair in local storage; as the access token nears expiry, `/auth/refresh` trades the refresh",
        "token for a new one. Single-user mode signs every visitor in as the admin; public mode gives each a guest account.",
    ), size=13.5, step=21)
    return s


def access(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 470, "Who can open what", "one module, `permissions.py`, answers every check")
    arrow = t.dim

    rrect(s, 30, 96, 900, 46, fill=tint(t, "grey"), stroke=edge(t, "grey"), r=12, width=1.3)
    icon(s, "shield-account-outline", 54, 119, 20, solid(t, "grey"))
    s.text(74, 125, "An admin passes every check.", size=15, anchor="start", weight="bold")
    s.text(310, 125, "Everyone else gets a role on each project, then on each dashboard.", size=14, anchor="start", colour=t.dim)

    card(s, 30, 172, 230, 170, "blue", "account", "A user", (
        "their own role, if any:",
        "owner, editor or viewer",
        "",
        "and their groups',",
        "read live from the groups",
    ), size=13.5)
    card(s, 320, 172, 290, 170, "teal", "jira", "Project role", (
        "the highest of their own",
        "and their groups' roles",
        "",
        "a public project: viewer",
        "for anyone, signed in or not",
    ), size=13.5)
    card(s, 670, 172, 260, 170, "orange", "view-dashboard", "Dashboard role", (
        "the project role, unless the",
        "dashboard's own owners or",
        "editors name them: a guest",
        "edits the copy they made",
    ), size=13.5)
    s.arrow(260, 257, 320, 257, colour=arrow)
    s.arrow(610, 257, 670, 257, colour=arrow)

    s.text(30, 384, "Then", size=15, anchor="start", weight="bold")
    chip(s, 80, 366, 200, "owner: share, delete", "teal")
    chip(s, 290, 366, 220, "editor: edit dashboards, data", "teal")
    chip(s, 520, 366, 120, "viewer: read", "teal")
    chip(s, 650, 366, 280, "no role: 404, as if it did not exist", "red", ico="cancel")
    label(s, 30, 432, "A refusal looks like a missing resource, so it tells nothing about what exists. Sign-in-free visitors match", anchor="start", size=13.5)
    label(s, 30, 453, "public projects only. Group membership is read on every check, so a change applies at once.", anchor="start", size=13.5)
    return s


def code_figure(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 458, "A code figure, from text to plot", "checked, compiled restricted, then run on the Celery worker under guards")
    arrow = t.dim

    w, gap, y, h = 200, 33, 100, 120
    steps = (
        ("blue", "code-braces", "Your code", ("`df` to read, `fig` to", "build; preparation", "lines may come first")),
        ("teal", "file-document-check-outline", "Checked", ("its shape: steps, then", "`fig`; and no line", "may reassign `df`")),
        ("purple", "shield-check-outline", "Restricted", ("`compile_restricted`:", "no `import`, no name", "that starts with `_`")),
        ("orange", "cog-sync-outline", "Run on the worker", ("a copy of `df`, with", "`px` `go` `pd` `pl` `np`", "and safe builtins")),
    )
    for i, (key, ico, title, rows) in enumerate(steps):
        x = 30 + i * (w + gap)
        card(s, x, y, w, h, key, ico, title, rows, size=13.5)
        if i:
            s.arrow(x - gap, y + h / 2, x, y + h / 2, colour=arrow)

    # While it runs: the guards and the audit hook.
    py = 252
    rrect(s, 30, py, 900, 140, fill=white(t), stroke=edge(t, "red"), r=12, width=1.5)
    icon(s, "cancel", 54, py + 26, 20, solid(t, "red"))
    s.text(74, py + 32, "While it runs, refused", size=16, anchor="start", weight="bold", colour=ink(t, "red"))
    s.text(266, py + 32, "by the attribute guard, then by an audit hook armed for that run only", size=13.5, anchor="start", colour=t.dim)
    row1 = (("readers and writers: `read_*`, `to_csv`", 290), ("submodules, bar the palettes", 210), ("`eval`, `query`, SQL", 150), ("writing a file", 120))
    row2 = (("starting a process", 140), ("opening a socket", 130), ("reading outside Python's install", 240), ("loading a library", 130), ("new imports", 110))
    x = 50
    for text, cw in row1:
        chip(s, x, py + 52, cw, text, "red")
        x += cw + 10
    x = 50
    for text, cw in row2:
        chip(s, x, py + 92, cw, text, "red")
        x += cw + 10
    label(s, 30, 438, "What it returns must be a Plotly figure named `fig`; anything else, or any refusal, shows as an error in the tile.", anchor="start", size=13.5)
    return s


if __name__ == "__main__":
    write_themed(sign_in, OUT, "sign-in")
    write_themed(access, OUT, "access")
    write_themed(code_figure, OUT, "code-figure")
