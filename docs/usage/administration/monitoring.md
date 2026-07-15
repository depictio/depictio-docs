---
title: Monitoring (Log & Task)
description: Admin-only panel for Celery tasks, ingestion runs, logs, and worker health.
---

# :material-chart-timeline-variant:{ style="color: #009688" } Monitoring — Log & Task

Admin-only panel (**Administration → Log & Task**, `/admin`) exposing a durable MongoDB ledger of background activity: Celery tasks, ingestion runs, application logs, and worker health.

!!! info "Availability"
    Admin-only. Shown in single- and multi-user mode, hidden in public/demo; non-admins get *Forbidden*.

Each pane polls every 8 s — toggle **Auto** to pause. With live updates on, a green **Live** badge appears and the active pane refreshes on each event.

## Tasks

Celery task history — figures, screenshots, MultiQC, advanced viz, Delta tables — with a **status** badge, duration, and timestamp. Filter by status, kind, or text. Expand a row for the task id, worker, arguments, error/traceback, and captured logs.

![Log & Task — Tasks pane](../../images/v0.12/react-beta/admin_monitoring_tasks_light.png#only-light)
![Log & Task — Tasks pane](../../images/v0.12/react-beta/admin_monitoring_tasks_dark.png#only-dark)

![Log & Task — expanded task detail](../../images/v0.12/react-beta/admin_monitoring_task_detail_light.png#only-light)
![Log & Task — expanded task detail](../../images/v0.12/react-beta/admin_monitoring_task_detail_dark.png#only-dark)

## Ingestion

CLI/UI ingestion runs, newest first: **status**, source badge, instance label or hostname, project, and user. Expand for the run id, host, and per-step table.

![Log & Task — Ingestion pane](../../images/v0.12/react-beta/admin_monitoring_ingestion_light.png#only-light)
![Log & Task — Ingestion pane](../../images/v0.12/react-beta/admin_monitoring_ingestion_dark.png#only-dark)

## Logs

Recent application logs from a capped collection, tagged by **level** and **source** (`api` / `celery`). Filter by level, source, or text; expand for the logger and `file:line`.

!!! tip "Runtime capture floor"
    The **capture floor** selector sets what the server persists, live — drop it to `DEBUG` while debugging, then raise it back. Not persisted across restarts.

![Log & Task — Logs pane](../../images/v0.12/react-beta/admin_monitoring_logs_light.png#only-light)
![Log & Task — Logs pane](../../images/v0.12/react-beta/admin_monitoring_logs_dark.png#only-dark)

## Health

Celery worker and broker health: status, worker count, active tasks, live-updates state, and worker hostnames.

![Log & Task — Health pane](../../images/v0.12/react-beta/admin_monitoring_health_light.png#only-light)
![Log & Task — Health pane](../../images/v0.12/react-beta/admin_monitoring_health_dark.png#only-dark)

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEPICTIO_MONITORING_ENABLED` | `true` | Master switch. |
| `DEPICTIO_MONITORING_RETENTION_DAYS` | `14` | TTL for task events. |
| `DEPICTIO_MONITORING_APP_LOG_MIN_LEVEL` | `WARNING` | Default log capture floor. |
| `DEPICTIO_MONITORING_APP_LOG_CAPPED_MB` | `64` | Log collection size cap. |
| `DEPICTIO_MONITORING_LIVE_UPDATES` | `true` | Enables live WebSocket push. |

!!! warning "Live push"
    Requires `DEPICTIO_EVENTS_ENABLED=true`. Without it the panel still works over polling.

## CLI ingestion identity

Set `instance_label` in the CLI YAML; each request then sends `X-Depictio-CLI-Instance` and `X-Depictio-CLI-Host`, and `depictio-cli run` records an ingestion run automatically — so multiple CLIs against one server stay distinguishable. Recording is best-effort and never blocks ingestion.
