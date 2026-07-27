#!/usr/bin/env python3
"""The two figures on the Data Model page.

    uv run python dev/diagrams/data_model.py

Writes ``docs/images/data-model/<name>_{light,dark}.{svg,png}``. The jitter is
seeded, so re-running without editing this file leaves the working tree clean.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "data-model"


def project_shape(theme: Theme) -> Sketch:
    """Which relationships are embedding, and which are references.

    Drawn as nesting rather than as arrows, because that is the single thing a
    reader most often gets wrong: workflows and data collections are not their
    own documents, they are fields of the project.
    """
    s = Sketch(1240, 675, theme=theme)
    s.heading(
        46,
        52,
        "The shape of a project",
        "one document in the projects collection holds the whole configuration tree",
    )

    s.box(Box(70, 130, 660, 450, "blue", "Project", ("projects · one document",)))
    s.box(Box(105, 215, 590, 200, "green", "Workflow", ("engine · data_location · runs",)))
    s.box(Box(135, 300, 255, 90, "orange", "DataCollection", ("tag: samplesheet",)))
    s.box(Box(410, 300, 255, 90, "orange", "DataCollection", ("tag: mosdepth",)))

    s.box(
        Box(135, 445, 255, 100, "orange", "DataCollection", ("basic projects:", "no workflow layer")),
        dashed=True,
    )
    s.box(Box(410, 445, 255, 100, "grey", "Embedded config", ("permissions · joins · links",)))

    s.box(Box(850, 215, 310, 130, "violet", "Dashboard", ("dashboards", "components carry dc_id")))
    s.arrow(850, 280, 730, 280)
    s.text(790, 265, "project_id", size=14, colour=theme.dim)

    s.box(Box(850, 420, 310, 120, "violet", "Dashboard (tab)", ("parent_dashboard_id", "tab_order")))
    s.arrow(1005, 420, 1005, 355)
    s.text(1017, 393, "tabs", size=14, colour=theme.dim, anchor="start")

    s.text(
        70,
        625,
        "Nesting is embedding — same document. An arrow is an ObjectId reference between documents.",
        size=14,
        colour=theme.dim,
        anchor="start",
    )
    s.text(
        70,
        648,
        "Dashed: only in basic projects, which skip the workflow layer entirely.",
        size=14,
        colour=theme.dim,
        anchor="start",
    )
    return s


def config_to_data(theme: Theme) -> Sketch:
    """Where the rows actually live, which the object hierarchy alone never says."""
    s = Sketch(1080, 660, theme=theme)
    s.heading(
        46,
        52,
        "From configuration to data",
        "a data collection describes a table; the deltatables entry is where it is",
    )

    s.box(Box(70, 140, 250, 110, "green", "WorkflowRun", ("runs", "one pipeline execution")))
    s.box(Box(400, 140, 250, 110, "yellow", "File", ("files", "location · hash · size")))
    s.arrow(320, 195, 400, 195)
    s.text(360, 180, "scan", size=14, colour=theme.dim)

    s.box(
        Box(400, 320, 250, 120, "orange", "DataCollection", ("embedded in the project", "tag · type · scan"))
    )
    s.arrow(525, 250, 525, 320)
    s.text(537, 290, "aggregate", size=14, colour=theme.dim, anchor="start")

    s.box(
        Box(
            730,
            320,
            280,
            120,
            "blue",
            "DeltaTableAggregated",
            ("deltatables", "location + schema history"),
        )
    )
    s.arrow(650, 380, 730, 380)
    s.text(690, 365, "1:1", size=14, colour=theme.dim)

    # Virgil draws braces as ornaments, so the path template is spelled out.
    s.box(Box(730, 510, 280, 100, "grey", "Delta table", ("in the S3 bucket,", "one per data collection")))
    s.arrow(870, 440, 870, 510)

    for i, line in enumerate(
        (
            "delta_location and last_aggregation are not stored",
            "on the DataCollection. The API joins them in from",
            "deltatables when it serves the project, so they",
            "only ever appear in responses.",
        )
    ):
        s.text(70, 505 + i * 22, line, size=14, colour=theme.dim, anchor="start")

    return s


if __name__ == "__main__":
    write_themed(project_shape, OUT, "project-shape")
    write_themed(config_to_data, OUT, "config-to-data")
