---
title: Monitoring (Log & Task)
description: Admin-only panel for Celery tasks, ingestion runs, logs, and worker health.
---

# :material-chart-timeline-variant:{ style="color: #009688" } Monitoring: Log & Task

Admin-only panel (**Administration → Log & Task**, `/admin`) exposing a durable MongoDB ledger of background activity: Celery tasks, ingestion runs, application logs, and worker health.

!!! info "Availability"
    Admin-only. Shown in single- and multi-user mode, hidden in public/demo; non-admins get *Forbidden*.

Each pane polls every 8 s; toggle **Auto** to pause. With live updates on, a green **Live** badge appears and the active pane refreshes on each event. The Tasks, Ingestion and Logs panes each have a free-text search box next to their filters.

## Tasks

Celery task history (figures, screenshots, MultiQC, advanced viz, Delta tables) with a **status** badge, duration, and timestamp. Filter by status, kind, or text. Expand a row for the task id, worker, and labelled **Arguments**, **Result**, **Error / Traceback** and **Logs** blocks.

![Log & Task: Tasks pane](../../images/react/admin_monitoring_tasks_light.png#only-light)
![Log & Task: Tasks pane](../../images/react/admin_monitoring_tasks_dark.png#only-dark)

![Log & Task: expanded task detail](../../images/react/admin_monitoring_task_detail_light.png#only-light)
![Log & Task: expanded task detail](../../images/react/admin_monitoring_task_detail_dark.png#only-dark)

## Ingestion

Ingestion runs, newest first: **status**, a `CLI` or `UI` source badge, instance label or hostname, project, and user. Uploads made through the web UI are recorded alongside CLI runs; recording is best-effort and never blocks an upload.

Expand a run for its **provenance** field grid: run id, host, CLI version, the resolved project id, the invoking command line, the CLI and project config paths, and the data root. Long paths are shortened to `head/…/tail`, with the full value in a tooltip and click-to-copy. Below it are two tables:

- **Steps**: every phase the run went through (provisioning, template resolve, server and S3 checks, config validation, project sync, scan, process, joins, dashboard import), each with `success` / `failed` / `skipped` and a detail line such as *3 data collection(s) processed*. The summary line tallies ok / failed / skipped and the wall-clock duration.
- **Data collections**: one row per data collection: tag, type, format, scan mode (`recursive` / `single`), the regex or filename it matched on, the local directories scanned, and the file count when known. These local scan paths are not shown anywhere else in the UI.

![Log & Task: Ingestion pane](../../images/react/admin_monitoring_ingestion_light.png#only-light)
![Log & Task: Ingestion pane](../../images/react/admin_monitoring_ingestion_dark.png#only-dark)

![Log & Task: expanded ingestion run detail](../../images/react/admin_monitoring_ingestion_detail_light.png#only-light)
![Log & Task: expanded ingestion run detail](../../images/react/admin_monitoring_ingestion_detail_dark.png#only-dark)

## Logs

Recent application logs from a capped collection, tagged by **level** and **source** (`api` / `celery`). Filter by level, source, or text; expand a row for the logger, the source `file:line`, and the full message.

!!! tip "Runtime capture floor"
    The **capture floor** selector sets what the server persists, live. Drop it to `DEBUG` while debugging, then raise it back. It differs from the **Level** filter, which only narrows rows already captured. The change is broadcast to Celery workers and is not persisted: a restart falls back to `DEPICTIO_MONITORING_APP_LOG_MIN_LEVEL`.

![Log & Task: Logs pane](../../images/react/admin_monitoring_logs_light.png#only-light)
![Log & Task: Logs pane](../../images/react/admin_monitoring_logs_dark.png#only-dark)

## Health

Celery worker and broker health: status, worker count, active tasks, live-updates state, and worker hostnames.

![Log & Task: Health pane](../../images/react/admin_monitoring_health_light.png#only-light)
![Log & Task: Health pane](../../images/react/admin_monitoring_health_dark.png#only-dark)

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

Set `instance_label` in the CLI YAML; each request then sends `X-Depictio-CLI-Instance` and `X-Depictio-CLI-Host`, and `depictio-cli run` records an ingestion run automatically, so multiple CLIs against one server stay distinguishable. Recording is best-effort and never blocks ingestion.

!!! warning "What leaves the machine"
    Sensitive option values such as `--provisioning-key` are redacted to `***` before the run is reported, but the rest of the invocation and the local paths listed above (CLI and project config, data root, scanned directories) **are visible to server admins** whenever monitoring is enabled.
