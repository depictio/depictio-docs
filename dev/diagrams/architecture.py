#!/usr/bin/env python3
"""The system architecture figure on the Features overview page.

    uv run python dev/diagrams/architecture.py

Writes ``docs/images/architecture/system_{light,dark}.{svg,png}``. Six services,
matching the component table the page prints underneath it, so the two cannot
drift apart without one of them looking obviously wrong.
"""

from __future__ import annotations

from pathlib import Path

from sketch import Box, Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "architecture"


def system(theme: Theme) -> Sketch:
    s = Sketch(1200, 660, theme=theme)
    s.heading(46, 52, "System architecture", "six services, and what talks to what")

    viewer = Box(
        60, 185, 250, 125, "violet", "React viewer", ("dashboards, in", "the browser")
    )
    api = Box(410, 185, 250, 125, "blue", "FastAPI", ("the API: auth, queries,", "data serving"))
    mongo = Box(
        810, 60, 260, 105, "green", "MongoDB", ("projects, dashboards,", "users, runs, files")
    )
    storage = Box(
        810, 200, 260, 105, "yellow", "MinIO / S3", ("Delta tables, images,", "screenshots")
    )
    redis = Box(810, 340, 260, 105, "pink", "Redis", ("cache, and the Celery", "broker"))
    celery = Box(
        410, 470, 250, 125, "orange", "Celery workers", ("ingestion, screenshots,", "pre-rendering")
    )

    for box in (viewer, api, mongo, storage, redis, celery):
        s.box(box)

    s.arrow(310, 240, 410, 240)
    s.text(360, 224, "REST", size=14, colour=theme.dim)
    s.arrow(410, 272, 310, 272, dashed=True)
    s.text(360, 300, "WebSocket", size=14, colour=theme.dim)

    s.arrow(660, 218, 810, 130)
    s.arrow(660, 248, 810, 250)
    s.arrow(660, 278, 810, 375)

    s.arrow(535, 310, 535, 470)
    s.text(547, 400, "dispatch", size=14, colour=theme.dim, anchor="start")

    s.arrow(660, 520, 810, 435)
    s.text(760, 500, "queue", size=14, colour=theme.dim)

    s.text(
        60,
        628,
        "The viewer only ever talks to FastAPI. Nothing else is reachable from the browser.",
        size=15,
        colour=theme.dim,
        anchor="start",
    )
    return s


if __name__ == "__main__":
    write_themed(system, OUT, "system")
