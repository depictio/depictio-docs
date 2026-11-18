#!/usr/bin/env python3
"""The system figures of the Architecture page and the Features overview.

    uv run python dev/diagrams/architecture.py

Writes into ``docs/images/architecture/``:

- ``system_{light,dark}``: what runs and what talks to what, on Features and
  Architecture;
- ``tasks_{light,dark}``: how the API hands work to the Celery workers;
- ``realtime_{light,dark}``: how an upsert reaches the open dashboards, on
  Architecture and the Real-time events guide.

Read from depictio v1.21.0. Services and ports: ``docker-compose.yaml`` (mongo,
redis, s3 = SeaweedFS ``weed mini``, depictio-backend :8058, depictio-viewer
:5080, depictio-celery-worker, and depictio-ingestion-worker behind the
``ingestion`` profile) and the Helm chart (``templates/deployments.yaml``, the
same services without the ingestion worker). The viewer is nginx serving the
built SPA and proxying ``/depictio/api/`` and ``/static/`` to the backend
(``docker-images/nginx.conf.template``); it has no state of its own. The CLI
writes Delta tables to S3 itself and registers them with ``/deltatables/upsert``.
Celery: ``depictio/api/celery_app.py`` (default queue ``celery``; ``task_routes``
send ``finalize_upsert`` and ``ingestion.run_project`` to ``ingestion``) and
``celery_dispatch.py`` (the API polls the result; code-mode renders always go to
the worker). Redis databases: cache 0, broker 1, results 2, events 3
(``settings_models.py``). Screenshots: ``screenshot_service.py`` opens
``settings.viewer.internal_url`` with Playwright and writes to the volume the
backend serves. Real time: ``services/events/`` (``connection_manager``,
``publish.py`` on ``depictio:events:*``, ``mongodb_watcher.py``).
"""

from __future__ import annotations

from pathlib import Path

from brand import card, chip, edge, ink, lines, new, panel, path_arrow, solid, tint
from concepts import rrect
from sketch import Sketch, Theme, write_themed

OUT = Path(__file__).resolve().parents[2] / "docs" / "images" / "architecture"


def label(s: Sketch, x: float, y: float, text: str, *, anchor: str = "middle", size: float = 12.5) -> None:
    s.text(x, y, text, size=size, anchor=anchor, colour=s.theme.dim)


def chips(s: Sketch, x: float, y: float, items: tuple[tuple[str, float, str], ...]) -> None:
    for text, w, ico in items:
        chip(s, x, y, w, text, "grey", ico=ico, dashed=True)
        x += w + 10


def system(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 816, "System architecture", "depictio v1.21.0: what runs, what talks to what, and what is optional (dashed)")
    arrow = t.dim

    # -- outside the deployment ---------------------------------------------
    card(s, 30, 92, 250, 100, "violet", "web", "Browser", ("the React viewer: sign-in,", "dashboards, the editor"))
    card(s, 330, 92, 300, 100, "teal", "console", "`depictio` CLI", ("ingest, run, watch, with a CLI token;", "writes its Delta tables to S3 itself"))
    card(s, 680, 92, 250, 100, "purple", "shield-account-outline", "Identity provider", ("OpenID Connect sign-in;", "the API redeems the code"), dashed=True)

    # -- the deployment -------------------------------------------------------
    rrect(s, 14, 212, 932, 442, fill="none", stroke=t.muted, r=16, width=1.2)
    label(s, 930, 644, "one deployment: Docker Compose, Helm, `depictio local up` or the all-in-one image", anchor="end", size=13)

    # The viewer: nginx, the SPA, a proxy.
    panel(s, 30, 252, 200, 160, "violet", "depictio-viewer", "monitor-dashboard")
    lines(s, 46, 318, ("nginx, port 5080", "serves the built SPA", "proxies the API and", "screenshots"))
    s.text(46, 400, "no state of its own", size=13, anchor="start", colour=ink(t, "violet"))

    # The API.
    panel(s, 300, 252, 320, 160, "blue", "depictio-backend", "api", tag="FastAPI, :8058")
    lines(s, 316, 318, (
        "sign-in, permissions, every query",
        "WebSocket for live updates, if on",
        "catalog, backups, migrations",
        "serves the screenshots",
    ))

    # The workers: two queues, the second one optional.
    panel(s, 680, 252, 250, 236, "orange", "Celery workers", "cog-sync-outline")
    rrect(s, 692, 306, 226, 104, fill=tint(t, "orange"), stroke=edge(t, "orange"), r=10, width=1.2)
    lines(s, 704, 328, ("queue `celery`, always on", "previews, code figures,", "advanced viz, MultiQC,", "screenshots (Playwright)"), first_bold=True, size=13.5, step=19)
    rrect(s, 692, 420, 226, 56, fill="none", stroke=edge(t, "orange"), r=10, width=1.2, dash=True)
    lines(s, 704, 442, ("queue `ingestion`, optional", "its own worker, for big tables"), first_bold=True, size=13.5, step=19)

    # -- the stores -----------------------------------------------------------
    sy = 528
    card(s, 30, sy, 270, 100, "green", "database-outline", "MongoDB", ("projects, dashboards, users,", "tokens, versions, comments"))
    card(s, 330, sy, 300, 100, "yellow", "bucket-outline", "S3: SeaweedFS, or yours", ("Delta tables, MultiQC reports,", "indexed track files"))
    card(s, 660, sy, 270, 100, "red", "memory", "Redis", ("db 0 cache, 1 task queue,", "2 task results, 3 live events"))

    # -- what talks to what ---------------------------------------------------
    s.arrow(130, 192, 130, 252, colour=arrow)
    label(s, 140, 236, "HTTPS", anchor="start")
    s.arrow(460, 192, 460, 252, colour=arrow)
    label(s, 470, 236, "REST, CLI token", anchor="start")
    # The CLI writes its tables to S3 itself, then registers them.
    path_arrow(s, [(630, 160), (664, 160), (664, 572), (630, 572)], colour=solid(t, "yellow"), dashed=True)
    # SSO: the browser is sent to the provider, the API redeems the code.
    s.arrow(705, 192, 604, 252, colour=solid(t, "purple"), dashed=True)
    label(s, 690, 236, "SSO", anchor="end")

    s.arrow(230, 312, 300, 312, colour=arrow)
    label(s, 265, 302, "proxy")
    label(s, 265, 330, "REST, WS")
    s.arrow(620, 312, 680, 312, colour=arrow)
    label(s, 642, 302, "tasks")

    # Everything stateful sits behind the API and the workers; the viewer has none.
    by = 506
    s.line(165, by, 805, by, colour=arrow, width=1.6)
    s.line(460, 412, 460, by, colour=arrow, width=1.6)
    s.line(805, 488, 805, by, colour=arrow, width=1.6)
    s.arrow(165, by, 165, sy, colour=arrow)
    s.arrow(460, by, 460, sy, colour=arrow)
    s.arrow(805, by, 805, sy, colour=arrow)
    label(s, 175, 498, "the API and the workers read and write all three", anchor="start")

    # -- leaving the deployment -----------------------------------------------
    s.text(30, 694, "Calls out, from the API and the workers", size=15, anchor="start", weight="bold")
    s.text(332, 694, "each one optional or switchable", size=13, anchor="start", colour=t.dim)
    chips(s, 30, 708, (("remote data, allow-listed", 196, "earth"), ("genome tracks, allow-listed", 206, "earth"), ("another instance: Send to", 200, "swap-horizontal")))
    chips(s, 30, 746, (("release check on GitHub", 186, "earth"), ("anonymous telemetry", 166, "earth"), ("protein structures, off by default", 246, "earth")))
    label(s, 30, 800, "The browser reaches the viewer only, except genome tracks of indexed files, read from S3 through presigned URLs.", anchor="start", size=13)
    return s


def tasks(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 492, "Work handed to the workers", "the API runs cheap work itself, and queues the rest on Redis")
    arrow = t.dim

    panel(s, 30, 100, 230, 176, "blue", "depictio-backend", "api")
    lines(s, 46, 166, ("cheap work: runs it itself", "the rest: queues a task,", "then polls for the result,", "or moves on"), size=13.5, step=20)

    panel(s, 330, 100, 290, 176, "red", "Redis", "memory")
    rrect(s, 344, 156, 262, 34, fill=tint(t, "red"), stroke=edge(t, "red"), r=8, width=1.2)
    s.text(358, 178, "db 1: queue `celery`", size=13.5, anchor="start")
    rrect(s, 344, 198, 262, 34, fill="none", stroke=edge(t, "red"), r=8, width=1.2, dash=True)
    s.text(358, 220, "db 1: queue `ingestion`", size=13.5, anchor="start")
    s.text(358, 260, "db 2: task results", size=13.5, anchor="start")

    panel(s, 690, 100, 240, 176, "orange", "Celery workers", "cog-sync-outline")
    rrect(s, 702, 156, 216, 34, fill=tint(t, "orange"), stroke=edge(t, "orange"), r=8, width=1.2)
    s.text(716, 178, "`depictio-celery-worker`", size=13.5, anchor="start")
    rrect(s, 702, 198, 216, 34, fill="none", stroke=edge(t, "orange"), r=8, width=1.2, dash=True)
    s.text(716, 220, "`depictio-ingestion-worker`", size=13.5, anchor="start")
    s.text(716, 260, "writes its result", size=13.5, anchor="start", colour=t.dim)

    s.arrow(260, 173, 344, 173, colour=arrow)
    label(s, 302, 164, "queue")
    s.arrow(606, 173, 702, 173, colour=arrow)
    s.arrow(606, 215, 702, 215, colour=arrow, dashed=True)
    s.arrow(702, 255, 606, 255, colour=arrow)
    label(s, 654, 246, "result")
    s.arrow(330, 255, 260, 255, colour=arrow, dashed=True)
    label(s, 295, 246, "polls")

    # What goes through, by how the API waits for it.
    y, h, w = 312, 156, 290
    card(s, 30, y, w, h, "blue", "refresh", "Awaited", (
        "same request, answered when done:",
        "figure previews in the editor",
        "code figures, always",
        "renders of tables of 50 MB or more",
        "advanced viz computations",
    ), size=13.5)
    card(s, 335, y, w, h, "orange", "camera-outline", "Fire and forget", (
        "nothing waits for these:",
        "dashboard screenshots, after a save",
        "MultiQC prerender and prewarm",
        "refresh of a remote data source",
    ), size=13.5)
    card(s, 640, y, w, h, "teal", "database-import-outline", "A job, on `ingestion`", (
        "with `DEPICTIO_JOBS_ENABLED`:",
        "finishing a big upsert, if offloaded",
        "an ingestion run from the browser",
        "progress at `/jobs`",
    ), size=13.5, dashed=True)
    return s


def realtime(theme: Theme) -> Sketch:
    t = theme
    s = new(t, 960, 500, "Live updates", "an upsert reaches every open dashboard that reads the collection, with no polling")
    arrow = t.dim

    # Top row: the write, the API, the fan-out.
    card(s, 30, 100, 260, 120, "teal", "console", "A producer", (
        "`depictio ingest`, or an",
        "instrument or pipeline that",
        "POSTs `/deltatables/upsert`",
    ), size=13.5)
    card(s, 350, 100, 260, 120, "blue", "api", "The API", (
        "re-reads the Delta table, bumps",
        "its version, drops cached frames",
        "(or the ingestion worker does)",
    ), size=13.5)
    card(s, 670, 100, 260, 120, "red", "memory", "Redis pub/sub, db 3", (
        "`depictio:events:*`",
        "reaches every API process",
        "and every replica",
    ), size=13.5)
    s.arrow(290, 160, 350, 160, colour=arrow)
    label(s, 320, 150, "upsert")
    s.arrow(610, 160, 670, 160, colour=arrow)
    label(s, 640, 150, "publish")

    # Bottom row, read right to left: a change stream, each API process, the dashboards.
    card(s, 670, 290, 260, 120, "green", "database-outline", "MongoDB change stream", (
        "edits to `data_collections`;",
        "needs a replica set",
    ), size=13.5, dashed=True)
    card(s, 350, 290, 260, 120, "blue", "lightning-bolt", "Each API process", (
        "sends `data_collection_updated`",
        "to every socket it holds; each",
        "dashboard checks the collection",
    ), size=13.5)
    card(s, 30, 290, 250, 120, "violet", "monitor-dashboard", "Open dashboards", (
        "one that reads it refetches,",
        "new rows lit; with auto-refresh",
        "off, a dot until you refresh",
    ), size=13.5)
    s.arrow(760, 220, 560, 290, colour=arrow)
    label(s, 690, 262, "fan-out", anchor="start")
    s.arrow(670, 350, 610, 350, colour=arrow, dashed=True)
    s.arrow(350, 350, 280, 350, colour=arrow)
    label(s, 315, 340, "WebSocket", size=12)

    lines(s, 30, 448, (
        "On when the server sets `DEPICTIO_EVENTS_ENABLED=true` and the project's YAML has `realtime: enabled: true`.",
        "A socket signs in with the access token, `/depictio/api/v1/events/ws`, and needs viewer access to the dashboard.",
    ), size=13, step=20)
    return s


if __name__ == "__main__":
    write_themed(system, OUT, "system")
    write_themed(tasks, OUT, "tasks")
    write_themed(realtime, OUT, "realtime")
