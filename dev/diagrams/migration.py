#!/usr/bin/env python3
"""The figure on the Project Migration page.

    uv run python dev/diagrams/migration.py

Writes ``docs/images/guides/migration/<name>_{light,dark}.{svg,png}``.
The jitter is seeded, so re-running without editing this file leaves the working
tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "migration"


def migration_paths(theme: Theme) -> Sketch:
    """Three rows, one per way to move a project, read left to right.

    Each row is source, what travels, target. The three targets end in the same
    scoped upsert, which is said once under the last column rather than three
    times, and the S3 difference between the CLI and the browser (copied bucket
    to bucket, or carried inside the ZIP) sits in the middle column, where it is
    the only thing that changes.
    """
    s = Sketch(1300, 610, theme=theme)
    s.heading(
        46,
        56,
        "Three ways to move a project",
        "each one ends in the same scoped upsert: nothing else on the target is touched",
    )

    cols = ((46, 300), (450, 400), (1000, 254))  # (x, width) of source, payload, target
    heads = ("Source instance", "What travels", "Target instance")
    for (x, w), head in zip(cols, heads):
        s.text(x + w / 2, 142, head, size=17, colour=theme.dim)

    rows = (
        (
            Box(cols[0][0], 170, cols[0][1], 96, "violet", "`depictio migrate`", ("from a shell, with the CLI",)),
            Box(
                cols[1][0], 170, cols[1][1], 96, "yellow", "ZIP without the data",
                ("`bundle.json` and its metadata", "files copied bucket to bucket"),
            ),
            Box(cols[2][0], 170, cols[2][1], 96, "green", "Import API", ("upsert, then the S3 copy",)),
            None,
        ),
        (
            Box(
                cols[0][0], 306, cols[0][1], 96, "blue", "Export as ZIP",
                ("Project settings, in the browser", "the ZIP is downloaded"),
            ),
            Box(
                cols[1][0], 306, cols[1][1], 96, "yellow", "ZIP with the data",
                ("`bundle.json`, its metadata", "and the files under `s3_data`"),
            ),
            Box(
                cols[2][0], 306, cols[2][1], 96, "green", "Import a project",
                ("From a ZIP file", "files restored, then upsert"),
            ),
            None,
        ),
        (
            Box(
                cols[0][0], 442, cols[0][1], 96, "blue", "Send",
                ("Project settings, by the owner", "with the URL and the code"),
            ),
            Box(
                cols[1][0], 442, cols[1][1], 96, "orange", "Instance to instance",
                ("the project, then its files", "no file to carry"),
            ),
            Box(
                cols[2][0], 442, cols[2][1], 96, "green", "Receive a project",
                ("an admin creates the code", "optionally read-only"),
            ),
            "v1.21.0+",
        ),
    )

    for source, payload, target, badge in rows:
        for b in (source, payload, target):
            s.box(b)
        s.glyph("depictio", source.x + 30, source.y + 21, size=24)
        s.glyph("depictio", target.x + 30, target.y + 21, size=24)
        s.glyph("folder" if payload.fill == "yellow" else "layers", payload.x + 32, payload.y + 21, size=24)
        mid = source.cy
        s.arrow(source.right + 8, mid, payload.x - 8, mid)
        s.arrow(payload.right + 8, mid, target.x - 8, mid)
        if badge:
            s.text(source.x + source.w - 10, source.y - 10, badge, size=14, colour=theme.accent, anchor="end")

    # The invite code goes the other way: issued on the target, pasted on the source.
    send, receive = rows[2][0], rows[2][2]
    y = send.bottom + 34
    s.line(receive.cx, receive.bottom + 6, receive.cx, y, colour=theme.dim, dashed=True, width=1.4)
    s.line(receive.cx, y, send.cx, y, colour=theme.dim, dashed=True, width=1.4)
    s.arrow(send.cx, y, send.cx, send.bottom + 8, dashed=True, colour=theme.dim)
    s.text((send.cx + receive.cx) / 2, y + 24, "the invite code, issued on the target", size=15, colour=theme.dim)

    return s


if __name__ == "__main__":
    write_themed(migration_paths, OUT, "migration-paths")
