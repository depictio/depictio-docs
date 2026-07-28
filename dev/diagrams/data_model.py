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
    s = Sketch(1320, 960, theme=theme)
    s.heading(
        46,
        52,
        "Two shapes of project",
        "nesting is embedding, in the same document. An arrow is a reference between documents.",
    )

    # -- advanced -----------------------------------------------------------
    s.text(360, 122, "Advanced project", size=19, weight="bold")
    s.text(360, 146, "defined in YAML, ingested by the CLI", size=15, colour=theme.dim)
    s.box(Box(60, 165, 600, 470, "blue", "Project", ("projects, one document",)))

    s.box(
        Box(
            95,
            260,
            530,
            200,
            "green",
            "Workflow",
            ("the pipeline that produced the data:", "nf-core/ampliseq, Snakemake, your own script"),
        )
    )
    s.box(Box(130, 355, 225, 85, "orange", "DataCollection", ("samplesheet",)))
    s.box(Box(370, 355, 225, 85, "orange", "DataCollection", ("mosdepth",)))

    s.box(Box(95, 500, 530, 95, "green", "Workflow", ("a project can define several",)))

    # -- basic --------------------------------------------------------------
    s.text(1000, 122, "Basic project", size=19, weight="bold")
    s.text(1000, 146, "created in the web UI, or with the CLI", size=15, colour=theme.dim)
    s.box(Box(740, 165, 520, 470, "blue", "Project", ("projects, one document",)))

    s.box(Box(775, 285, 215, 85, "orange", "DataCollection", ("samplesheet",)))
    s.box(Box(1010, 285, 215, 85, "orange", "DataCollection", ("metadata",)))

    s.text(1000, 445, "No workflow layer. Data collections", size=15, colour=theme.dim)
    s.text(1000, 469, "sit directly on the project, and there", size=15, colour=theme.dim)
    s.text(1000, 493, "are no runs to scan.", size=15, colour=theme.dim)

    # -- dashboards ---------------------------------------------------------
    s.box(
        Box(
            400,
            730,
            520,
            180,
            "none",
            "Dashboard",
            ("what the user opens:", "one or more tabs of components"),
        ),
        dashed=True,
    )
    s.box(Box(430, 815, 140, 70, "violet", "Main tab", ()))
    s.box(Box(590, 815, 140, 70, "violet", "Tab 2", ()))
    s.box(Box(750, 815, 140, 70, "violet", "Tab 3", ()))

    s.arrow(510, 730, 400, 640)
    s.arrow(810, 730, 940, 640)
    s.text(428, 700, "belongs to", size=14, colour=theme.dim)
    s.text(902, 700, "belongs to", size=14, colour=theme.dim)

    return s


def files_to_data(theme: Theme) -> Sketch:
    """What a scan actually produces, and the fact that it is not always a table.

    The fan on the right is the point of the figure. Drawing only the Delta
    table branch, which is what an earlier version did, quietly implies that
    MultiQC reports, GeoJSON and trees go through the same machinery. They do
    not, and a reader who assumes they do will go looking for a Delta table
    that was never written.
    """
    s = Sketch(1240, 760, theme=theme)
    s.heading(
        46,
        52,
        "How files become dashboard data",
        "one run's output folder, turned into something a dashboard can read",
    )

    s.box(
        Box(
            60,
            130,
            300,
            130,
            "green",
            "Run",
            ("one execution of a workflow:", "an output folder, one or", "more samples processed"),
        ),
        icon="folder",
    )

    s.stack(
        Box(
            490,
            135,
            280,
            125,
            "yellow",
            "Files",
            ("everything the scan matched:", "path, size, checksum"),
        ),
        icon="page",
    )
    s.arrow(360, 195, 470, 195)
    s.text(415, 180, "scan", size=14, colour=theme.dim)

    s.box(
        Box(
            340,
            340,
            430,
            130,
            "orange",
            "DataCollection",
            (
                "every file of one type, from every run,",
                "gathered into the one thing",
                "a dashboard reads",
            ),
        ),
        icon="layers",
    )
    s.arrow(630, 260, 600, 340)
    s.text(645, 305, "grouped by type", size=14, colour=theme.dim, anchor="start")

    s.text(1015, 150, "materialised by type:", size=15, colour=theme.dim)
    types = (
        ("table", "table", ("a Delta table on S3,", "appended run after run")),
        ("image", "image", ("a Delta table of S3 paths;", "the API streams the images")),
        ("multiqc", "multiqc", ("the report's parsed data,", "as Parquet on S3")),
        ("geojson", "map", ("the file itself, copied to S3",)),
        ("phylogeny", "tree", ("the tree, read from wherever", "the scan found it")),
    )
    for i, (title, icon, lines) in enumerate(types):
        y = 175 + i * 108
        s.box(Box(830, y, 370, 90, "blue", title, lines), icon=icon)
        s.arrow(770, 405, 830, y + 45)

    for i, line in enumerate(
        (
            "None of this is written down in the project.",
            "The configuration says what a data collection",
            "is; where it landed is recorded at ingestion",
            "and joined back in when the API serves it.",
        )
    ):
        s.text(60, 540 + i * 24, line, size=15, colour=theme.dim, anchor="start")

    return s


def join_vs_link(theme: Theme) -> Sketch:
    """Two mechanisms that both sound like "connect these two data collections".

    The two halves deliberately do not mirror each other. A join takes two
    tables and returns one; a link takes one selection and reaches an arbitrary
    number of data collections of any type. Drawing both as 2-in-1-out, which is
    what the first version did, hid exactly the difference the figure exists to
    show. The palettes differ for the same reason.
    """
    s = Sketch(1380, 640, theme=theme)
    s.heading(
        46,
        52,
        "Joining and linking",
        "a join merges tables once, at ingestion. A link merges nothing and filters at render time.",
    )

    # -- join ---------------------------------------------------------------
    s.text(350, 122, "Join", size=19, weight="bold")
    s.text(350, 146, "run by the CLI, at ingestion. Tables only.", size=15, colour=theme.dim)

    s.box(Box(70, 190, 250, 95, "green", "samplesheet", ("sample_id, condition",)), icon="table")
    s.box(Box(70, 345, 250, 95, "green", "mosdepth", ("sample_id, coverage",)), icon="table")

    s.box(
        Box(
            410,
            255,
            270,
            120,
            "blue",
            "joined table",
            ("one new data collection,", "written to S3"),
        ),
        icon="table",
    )
    s.arrow(320, 230, 410, 290)
    s.arrow(320, 397, 410, 337)
    s.text(362, 325, "on sample_id", size=14, colour=theme.dim)

    s.text(360, 500, "One data collection from here on.", size=15, colour=theme.dim)
    s.text(360, 524, "The rows are merged on disk.", size=15, colour=theme.dim)

    s.line(700, 120, 700, 570, colour=theme.muted, width=1.4, dashed=True)

    # -- link ---------------------------------------------------------------
    s.text(1030, 122, "Link", size=19, weight="bold")
    s.text(1030, 146, "run by the dashboard, at render time. Any type.", size=15, colour=theme.dim)

    s.box(Box(750, 235, 250, 95, "violet", "samplesheet", ("sample_id, condition",)), icon="table")

    s.box(Box(1060, 180, 280, 70, "pink", "mosdepth table", ()), icon="table")
    s.box(Box(1060, 270, 280, 70, "pink", "MultiQC report", ()), icon="multiqc")
    s.box(Box(1060, 360, 280, 70, "pink", "image gallery", ()), icon="image")
    for y in (215, 305, 395):
        s.arrow(1000, 282, 1060, y, dashed=True, colour=theme.accent)
    s.text(1030, 460, "filters, at query time", size=14, colour=theme.accent)

    s.text(1030, 500, "Nothing is merged. Picking samples on the", size=15, colour=theme.dim)
    s.text(1030, 524, "left narrows everything on the right, whatever", size=15, colour=theme.dim)
    s.text(1030, 548, "kind of data it holds.", size=15, colour=theme.dim)

    return s


if __name__ == "__main__":
    write_themed(project_shape, OUT, "project-shape")
    write_themed(files_to_data, OUT, "files-to-data")
    write_themed(join_vs_link, OUT, "join-vs-link")
