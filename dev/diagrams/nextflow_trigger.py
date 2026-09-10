#!/usr/bin/env python3
"""The figure on the Nextflow trigger page.

    uv run python dev/diagrams/nextflow_trigger.py

Writes ``docs/images/guides/nextflow-trigger/<name>_{light,dark}.{svg,png}``.
The jitter is seeded, so re-running without editing this file leaves the working
tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "guides" / "nextflow-trigger"

# Each box wears the mark of the thing it is, so the row can be read before the
# words are. Brand colours are the marks' own; the checkered flag is not a brand
# and follows the palette.
NEXTFLOW_GREEN = "#0dc09d"
PYTHON_BLUE = {"light": "#3776ab", "dark": "#7aa9d4"}


def trigger_flow(theme: Theme) -> Sketch:
    """One spine, left to right, and the three things a reader has to trust.

    Drawn as a single row rather than a flowchart because the page it sits on is
    deliberately short: anything needing a legend belongs in the prose, not here.
    The guards, the argument list and the CLI's own eight steps are all left out
    for the same reason, and the notes underneath sit each under the box
    they qualify so no leader lines are needed.
    """
    s = Sketch(1300, 372, theme=theme)
    s.heading(
        46,
        56,
        "The pipeline ingests its own results",
        "nothing changes in the command you run, and nothing about Depictio goes in the pipeline",
    )

    top = 168
    height = 100
    mid = top + height / 2

    pipeline = Box(46, top, 250, height, "green", "Your pipeline", ("the last task finishes",))
    handler = Box(
        336,
        top,
        280,
        height,
        "blue",
        "`workflow.onComplete`",
        ("reads `params.outdir`", "and passes it as `--data-root`"),
    )
    cli = Box(
        656,
        top,
        250,
        height,
        "violet",
        "`depictio-cli run`",
        ("resolves the template", "from the pipeline's name"),
    )
    server = Box(946, top, 308, height, "orange", "Depictio", ("a project, and a dashboard",))

    for b in (pipeline, handler, cli, server):
        s.box(b)

    # The marks sit above their box rather than beside the title: three of the
    # four titles are code, and a centred monospace title of that length reaches
    # the corner an inline icon would occupy.
    marks = (
        # The flag is drawn larger: its icon carries more padding inside its own
        # viewBox than the three logos do, so at a shared size it reads smaller.
        (pipeline, "nextflow", NEXTFLOW_GREEN, 30),
        (handler, "flag", theme.ink, 36),
        (cli, "python", PYTHON_BLUE[theme.name], 30),
        (server, "depictio", None, 32),
    )
    for b, mark, mark_colour, mark_size in marks:
        s.glyph(mark, b.cx, top - 28, size=mark_size, colour=mark_colour)

    for a, b in ((pipeline, handler), (handler, cli), (cli, server)):
        s.arrow(a.right + 6, mid, b.x - 6, mid)

    # -- the three things a reader has to trust, each under its own box ------
    note = top + height + 52

    s.text(pipeline.cx, note, "your exit status", size=15, colour=theme.dim)
    s.text(pipeline.cx, note + 22, "is never changed", size=15, colour=theme.dim)

    s.cross(handler.cx - 118, note - 5, size=9)
    s.text(handler.cx + 12, note, "a pipeline that failed", size=15, colour=theme.dim)
    s.text(handler.cx, note + 22, "is never ingested", size=15, colour=theme.dim)

    s.text(cli.cx, note, "your token comes from", size=15, colour=theme.dim)
    s.text(cli.cx, note + 22, "`~/.depictio/CLI.yaml`", size=15, colour=theme.dim)

    s.text(server.cx, note, "the run summary prints", size=15, colour=theme.dim)
    s.text(server.cx, note + 22, "a link to both", size=15, colour=theme.dim)

    return s


if __name__ == "__main__":
    write_themed(trigger_flow, OUT, "trigger-flow")
