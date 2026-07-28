#!/usr/bin/env python3
"""The figures on the Data Model page.

    uv run python dev/diagrams/data_model.py

Writes ``docs/images/data-model/<name>_{light,dark}.{svg,png}``. The jitter is
seeded, so re-running without editing this file leaves the working tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "data-model"


def project_shape(theme: Theme) -> Sketch:
    """The two project shapes, side by side, plus where a dashboard attaches.

    Drawn as two panels because the workflow layer being optional is the single
    thing a reader most often gets wrong, and a dashed box inside one figure was
    never going to say "this whole level does not exist here".
    """
    s = Sketch(1320, 930, theme=theme)
    s.heading(
        46,
        52,
        "Two shapes of project",
        "nesting is embedding, in the same document. An arrow is a reference between documents.",
    )

    # -- advanced -----------------------------------------------------------
    s.text(360, 128, "Advanced project", size=19, weight="bold")
    s.box(Box(60, 145, 600, 465, "blue", "Project", ("projects, one document",)))

    s.box(
        Box(
            95,
            240,
            530,
            200,
            "green",
            "Workflow",
            ("the pipeline definition:", "nf-core/ampliseq, a Snakemake catalog entry"),
        )
    )
    s.box(Box(125, 335, 235, 85, "orange", "DataCollection", ("samplesheet",)))
    s.box(Box(390, 335, 235, 85, "orange", "DataCollection", ("mosdepth",)))

    s.box(Box(95, 480, 530, 95, "green", "Workflow", ("a project can define several",)))

    # -- basic --------------------------------------------------------------
    s.text(1000, 128, "Basic project", size=19, weight="bold")
    s.box(Box(740, 145, 520, 465, "blue", "Project", ("projects, one document",)))

    s.box(Box(775, 265, 215, 85, "orange", "DataCollection", ("samplesheet",)))
    s.box(Box(1010, 265, 215, 85, "orange", "DataCollection", ("metadata",)))

    s.text(1000, 420, "No workflow layer. Data collections", size=15, colour=theme.dim)
    s.text(1000, 442, "sit directly on the project, and there", size=15, colour=theme.dim)
    s.text(1000, 464, "are no runs to scan.", size=15, colour=theme.dim)

    # -- dashboards ---------------------------------------------------------
    s.box(
        Box(
            400,
            700,
            520,
            180,
            "none",
            "Dashboard",
            ("what the user opens: one document per tab,", "tied together by parent_dashboard_id"),
        ),
        dashed=True,
    )
    s.box(Box(430, 785, 140, 70, "violet", "Main tab", ()))
    s.box(Box(590, 785, 140, 70, "violet", "Tab 2", ()))
    s.box(Box(750, 785, 140, 70, "violet", "Tab 3", ()))

    s.arrow(510, 700, 400, 615)
    s.arrow(810, 700, 940, 615)
    s.text(430, 668, "project_id", size=14, colour=theme.dim)
    s.text(900, 668, "project_id", size=14, colour=theme.dim)

    return s


def config_to_data(theme: Theme) -> Sketch:
    """Where the rows actually live, which the object hierarchy alone never says."""
    s = Sketch(1200, 800, theme=theme)
    s.heading(
        46,
        52,
        "From configuration to data",
        "how the output of a run becomes one table a dashboard can read",
    )

    s.box(
        Box(
            70,
            170,
            300,
            140,
            "green",
            "Run",
            ("one execution of the workflow:", "an output folder, one or", "more samples processed"),
        )
    )

    s.stack(
        Box(
            500,
            170,
            270,
            140,
            "yellow",
            "Files",
            ("one record per file:", "location, hash, size"),
        )
    )
    s.arrow(370, 235, 490, 235)
    s.text(430, 220, "scan", size=14, colour=theme.dim)

    s.box(
        Box(
            460,
            420,
            310,
            145,
            "orange",
            "DataCollection",
            ("every file of one type,", "across every run,", "as a single table"),
        )
    )
    s.arrow(615, 320, 615, 420)
    s.text(627, 380, "aggregate", size=14, colour=theme.dim, anchor="start")

    s.box(
        Box(
            870,
            420,
            290,
            145,
            "grey",
            "deltatables entry",
            ("where that table is,", "plus the schema of", "every aggregation run"),
        )
    )
    s.arrow(770, 490, 870, 490)
    s.text(820, 475, "1:1", size=14, colour=theme.dim)

    s.box(
        Box(
            870,
            645,
            290,
            110,
            "blue",
            "Delta table",
            ("the rows themselves, on S3,", "in Delta Lake format"),
        )
    )
    s.arrow(1015, 565, 1015, 645)

    for i, line in enumerate(
        (
            "A data collection says what a table is.",
            "It never says where it is: delta_location",
            "and last_aggregation are joined in from",
            "the deltatables entry when the API serves",
            "the project, so they show up in responses",
            "and nowhere in the stored configuration.",
        )
    ):
        s.text(70, 440 + i * 24, line, size=15, colour=theme.dim, anchor="start")

    return s


def join_vs_link(theme: Theme) -> Sketch:
    """Two mechanisms that both sound like "connect these two tables"."""
    s = Sketch(1300, 560, theme=theme)
    s.heading(
        46,
        52,
        "Joining and linking",
        "a join makes one table; a link keeps two and passes filters between them",
    )

    # -- join ---------------------------------------------------------------
    s.text(330, 135, "Join", size=19, weight="bold")
    s.box(Box(70, 165, 230, 95, "orange", "samplesheet", ("sample_id, condition",)))
    s.box(Box(70, 320, 230, 95, "orange", "mosdepth", ("sample_id, coverage",)))

    s.box(
        Box(
            420,
            230,
            250,
            120,
            "green",
            "joined table",
            ("source: joined", "written at ingestion"),
        )
    )
    s.arrow(300, 205, 420, 265)
    s.arrow(300, 372, 420, 320)
    s.text(360, 300, "on sample_id", size=14, colour=theme.dim)

    s.text(370, 450, "One data collection from here on.", size=15, colour=theme.dim)
    s.text(370, 474, "The rows are merged on disk.", size=15, colour=theme.dim)

    s.line(700, 130, 700, 520, colour=theme.muted, width=1.4, dashed=True)

    # -- link ---------------------------------------------------------------
    s.text(1000, 135, "Link", size=19, weight="bold")
    s.box(Box(880, 165, 240, 95, "orange", "samplesheet", ("sample_id, condition",)))
    s.box(Box(880, 320, 240, 95, "orange", "mosdepth", ("sample_id, coverage",)))

    s.arrow(1000, 260, 1000, 320, dashed=True, colour=theme.accent)
    s.text(1012, 296, "filter, at query time", size=14, colour=theme.accent, anchor="start")

    s.text(1000, 450, "Both tables stay as they are. Selecting", size=15, colour=theme.dim)
    s.text(1000, 474, "two conditions on the left narrows the", size=15, colour=theme.dim)
    s.text(1000, 498, "right to the samples they resolve to.", size=15, colour=theme.dim)

    return s


if __name__ == "__main__":
    write_themed(project_shape, OUT, "project-shape")
    write_themed(config_to_data, OUT, "config-to-data")
    write_themed(join_vs_link, OUT, "join-vs-link")
