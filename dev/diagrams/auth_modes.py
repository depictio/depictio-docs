#!/usr/bin/env python3
"""The figure on the Authentication Modes page.

    uv run python dev/diagrams/auth_modes.py

Writes ``docs/images/guides/authentication-modes/auth-modes_{light,dark}.{svg,png}``.

What a visitor who opens the URL gets in each mode, read from depictio v1.21.0:
``bootstrapSession`` in ``depictio/viewer/src/main.tsx`` (single-user: the admin's
session; public: ``createTemporaryUser``, unless an access code is required;
otherwise the sign-in page), ``_create_temporary_user`` (``temp_user_<id>@depictio.temp``,
24 h by default) and ``canGuestSignIn`` (sign-in offered to a public guest when an
OIDC provider is configured, never in demo mode). Mode colours and icons follow the
app's badges: public teal with a globe, demo violet with a compass.
"""

from __future__ import annotations

from pathlib import Path

from concepts import CONCEPTS, _ink, _mix, edge, icon, ink, person, raw, rrect, shadow_defs, solid, white
from mdi_icons import MDI
from sketch import DARK, LIGHT, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "authentication-modes"

# Icons the shared set does not carry, from mkdocs-material's bundled MDI.
MDI.update({
    "earth": "M17.9 17.39c-.26-.8-1.01-1.39-1.9-1.39h-1v-3a1 1 0 0 0-1-1H8v-2h2a1 1 0 0 0 1-1V7h2a2 2 0 0 0 2-2v-.41a7.984 7.984 0 0 1 2.9 12.8M11 19.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.22.21-1.79L9 15v1a2 2 0 0 0 2 2m1-16A10 10 0 0 0 2 12a10 10 0 0 0 10 10 10 10 0 0 0 10-10A10 10 0 0 0 12 2",
    "compass-outline": "m7 17 3.2-6.8L17 7l-3.2 6.8zm5-5.9a.9.9 0 0 0-.9.9.9.9 0 0 0 .9.9.9.9 0 0 0 .9-.9.9.9 0 0 0-.9-.9M12 2a10 10 0 0 1 10 10 10 10 0 0 1-10 10A10 10 0 0 1 2 12 10 10 0 0 1 12 2m0 2a8 8 0 0 0-8 8 8 8 0 0 0 8 8 8 8 0 0 0 8-8 8 8 0 0 0-8-8",
    "login": "M11 7 9.6 8.4l2.6 2.6H2v2h10.2l-2.6 2.6L11 17l5-5zm9 12h-8v2h8c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-8v2h8z",
    "account-clock-outline": "M16 14h1.5v2.82l2.44 1.41-.75 1.3L16 17.69zm1-2a5 5 0 0 0-5 5 5 5 0 0 0 5 5 5 5 0 0 0 5-5 5 5 0 0 0-5-5m0-2a7 7 0 0 1 7 7 7 7 0 0 1-7 7c-2.79 0-5.2-1.64-6.33-4H1v-3c0-2.66 5.33-4 8-4 .6 0 1.34.07 2.12.2A6.99 6.99 0 0 1 17 10m-7 7c0-.7.1-1.38.29-2-.42-.07-.86-.1-1.29-.1-2.97 0-6.1 1.46-6.1 2.1v1.1h7.19A7 7 0 0 1 10 17M9 4a4 4 0 0 1 4 4 4 4 0 0 1-4 4 4 4 0 0 1-4-4 4 4 0 0 1 4-4m0 1.9A2.1 2.1 0 0 0 6.9 8 2.1 2.1 0 0 0 9 10.1 2.1 2.1 0 0 0 11.1 8 2.1 2.1 0 0 0 9 5.9",
    "shield-account-outline": "M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5zm0 2.18 7 3.12v4.92c0 1.7-.5 3.43-1.35 4.95C16 14.94 13.26 14.5 12 14.5s-4 .44-5.65 1.67C5.5 14.65 5 12.92 5 11.22V6.3zM12 6a3.5 3.5 0 0 0-3.5 3.5A3.5 3.5 0 0 0 12 13a3.5 3.5 0 0 0 3.5-3.5A3.5 3.5 0 0 0 12 6m0 2a1.5 1.5 0 0 1 1.5 1.5A1.5 1.5 0 0 1 12 11a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 12 8m0 8.5c1.57 0 3.64.61 4.53 1.34C15.29 19.38 13.7 20.55 12 21c-1.7-.45-3.29-1.62-4.53-3.16.9-.73 2.96-1.34 4.53-1.34",
})

# One colour per mode, registered like the concepts: auth in the app's primary
# blue, single-user orange, public teal and demo violet as their badges.
MODES = {"m_auth": "#228be6", "m_single": "#fd7e14", "m_public": "#12b886", "m_demo": "#7950f2"}
for _key, _c in MODES.items():
    CONCEPTS[_key] = _c
    LIGHT.fills[_key] = _mix(_c, "#ffffff", 0.10)
    DARK.fills[_key] = _mix(_c, DARK.bg, 0.22)
    LIGHT.inks[_key] = _ink("light", _key)
    DARK.inks[_key] = _ink("dark", _key)

W, COL, GAP, X0 = 960, 213, 16, 30


def tick(s: Sketch, x: float, y: float, text: str, ok: bool = True) -> None:
    t = s.theme
    if ok:
        icon(s, "check", x + 7, y - 5, 17, solid(t, "good"))
    else:
        s.cross(x + 7, y - 5, size=5, colour=solid(t, "bad"))
    s.text(x + 22, y, text, size=14, anchor="start", colour=t.ink if ok else t.dim)


def auth_modes(theme: Theme) -> Sketch:
    t = theme
    s = Sketch(W, 726, theme=t)
    shadow_defs(s)
    s.heading(X0, 50, "What a visitor gets, mode by mode", "one mode per instance; everyone below has just opened its URL")

    person(s, W / 2, 128, 44, "people")
    s.text(W / 2 + 34, 134, "a visitor", size=15, anchor="start", colour=t.dim)

    cols = (
        ("m_auth", "shield-account-outline", "Auth", "default: nothing to set"),
        ("m_single", "laptop", "Single-user", "`SINGLE_USER_MODE`"),
        ("m_public", "earth", "Public", "`PUBLIC_MODE`"),
        ("m_demo", "compass-outline", "Demo", "`PUBLIC_MODE` + `DEMO_MODE`"),
    )
    door = (
        ("login", "Sign-in page", "password or SSO", False),
        (None, "No sign-in page", "nobody is asked", True),
        ("key-outline", "Access code, if set", "otherwise straight in", True),
        ("key-outline", "Access code, if set", "otherwise straight in", True),
    )
    who = (
        ("account", "Their own account", ("user or admin, with", "a role on each project")),
        ("account", "The admin, for all", ("every visitor shares", "the admin's session")),
        ("account-clock-outline", "A guest account", ("their own `temp_user_…`,", "removed after 24 h")),
        ("account-clock-outline", "A guest account", ("their own `temp_user_…`,", "removed after 24 h")),
    )
    can = (
        (("create projects", True), ("create dashboards", True), ("register, unless", True), ("  it is disabled", None)),
        (("everything an", True), ("  admin can do", None), ("other accounts", False)),
        (("read public dashboards", True), ("duplicate one, the", True), ("  copy expires too", None), ("create projects", False)),
        (("read public dashboards", True), ("duplicate one, the", True), ("  copy expires too", None), ("a sign-in prompt", False)),
    )

    for i, ((key, ico, name, switch), (dico, dtitle, dsub, dashed), (wico, wtitle, wlines), rules) in enumerate(zip(cols, door, who, can)):
        x = X0 + i * (COL + GAP)
        cx = x + COL / 2
        s.arrow(W / 2, 156, cx, 186, colour=t.muted)

        # The mode, and the setting that turns it on.
        rrect(s, x, 192, COL, 74, fill=t.fill(key), stroke=edge(t, key), r=12, width=1.8)
        icon(s, ico, x + 28, 220, 24, solid(t, key))
        s.text(x + 48, 228, name, size=19, anchor="start", weight="bold", colour=ink(t, key))
        s.text(x + 16, 254, switch, size=14, anchor="start", colour=t.dim)
        s.arrow(cx, 272, cx, 294, colour=t.muted)

        # What stands at the door.
        rrect(s, x + 10, 298, COL - 20, 62, fill=white(t), stroke=t.muted, r=10, width=1.3, dash=dashed)
        tx = x + 24
        if dico:
            icon(s, dico, x + 30, 318, 18, t.dim)
            tx = x + 46
        s.text(tx, 324, dtitle, size=15, anchor="start", weight="bold")
        s.text(x + 24, 348, dsub, size=13, anchor="start", colour=t.dim)
        s.arrow(cx, 364, cx, 386, colour=t.muted)

        # Who they are once in.
        f = ' filter="url(#sh)"' if t.name == "light" else ""
        raw(s, f'<g{f}><rect x="{x:.1f}" y="390" width="{COL}" height="108" rx="12" fill="{white(t)}" stroke="{edge(t, key)}" stroke-width="1.8"/></g>')
        raw(s, f'<circle cx="{x + 30:.1f}" cy="418" r="17" fill="{t.fill(key)}" stroke="{edge(t, key)}" stroke-width="1.4"/>')
        icon(s, wico, x + 30, 418, 22, solid(t, key))
        s.text(x + 56, 424, wtitle, size=15, anchor="start", weight="bold", colour=ink(t, key))
        for j, line in enumerate(wlines):
            s.text(x + 16, 460 + j * 21, line, size=14, anchor="start", colour=t.dim)

        # What they can do.
        for j, (text, ok) in enumerate(rules):
            y = 532 + j * 22
            if ok is None:
                s.text(x + 22, y, text.strip(), size=14, anchor="start", colour=t.ink)
            else:
                tick(s, x + 6, y, text, ok)

    # SSO: what an identity provider adds in each mode.
    by = 620
    rrect(s, X0, by, W - 2 * X0, 86, fill=t.fill("grey"), stroke=t.muted, r=12, width=1.2)
    icon(s, "login", X0 + 26, by + 28, 20, t.dim)
    s.text(X0 + 48, by + 34, "With an OpenID Connect provider (SSO)", size=16, anchor="start", weight="bold")
    s.text(X0 + 48, by + 60, "Auth: a sign-in button; a first sign-in creates the account.  Public: a guest can sign in", size=14, anchor="start", colour=t.dim)
    s.text(X0 + 48, by + 79, "to an account of their own.  Demo: no prompts, an admin signs in at `/auth/login`.  Single-user: never asked.", size=14, anchor="start", colour=t.dim)
    return s


if __name__ == "__main__":
    write_themed(auth_modes, OUT, "auth-modes")
