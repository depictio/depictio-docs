---
title: "API"
icon: material/api
description: "Depictio's REST API: logging in, the endpoint reference, live FastAPI docs and background jobs."
---

# API

The viewer and the CLI both work through Depictio's REST API, under `/depictio/api/v1`. Log in with `POST /auth/login`, then send the token as `Authorization: Bearer <token>`.

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle .dp-blue } **API reference**

    ---

    Every endpoint, generated from the OpenAPI specification.

    [:octicons-arrow-right-24: API reference](reference.md)

-   :material-api:{ .lg .middle .dp-teal } **FastAPI docs**

    ---

    Swagger UI and ReDoc, served live by your own server.

    [:octicons-arrow-right-24: FastAPI docs](fastapi_docs.md)

-   :material-progress-clock:{ .lg .middle .dp-orange } **Jobs**

    ---

    Poll the work the server finishes in the background.

    [:octicons-arrow-right-24: Jobs](#jobs)

</div>

Serving one component to another website? See [Component export](../features/component-export.md#the-api).

## Jobs <small>(v1.15.0+)</small> { #jobs }

Some requests start work that outlives an HTTP request. They answer with a `job_id`, and
the client polls the job until it ends. Paths are under `/depictio/api/v1`. The routes exist only when `DEPICTIO_JOBS_ENABLED`
is true; otherwise `/jobs` answers 404. See [Jobs](../installation/env-reference.md#jobs).

| Method and path | What it does |
|-----------------|--------------|
| `GET /jobs/{job_id}` | One job: `status`, `step`, `detail`, `progress`, `result` or `error`, timestamps, and `poll_after_seconds`, the suggested wait before the next poll |
| `GET /jobs` | Your jobs, newest first. Filters `kind`, `status` and `project_id`; `limit` (1–200, default 50) and `skip`. Admins see everyone's |
| `POST /jobs/{job_id}/cancel` | Cancels a job that has not ended, and asks the worker to stop its task |

A job is `pending`, `running`, `success`, `failed` or `cancelled`. A job that belongs to
someone else answers 404, as a missing one does; admins can read any job. There is no
route to create a job: the endpoint that owns the work creates it, and names its `kind`.

| Kind | Created by |
|------|------------|
| `deltatable.upsert` | `POST /deltatables/upsert` with `async_mode: true`, when [offloading](../installation/docker.md#async-upsert) is on. Without it the response has no `job_id` and the work is done |
| `project.ingest` | `POST /projects/ingestion/trigger/{project_id}`, the [**Run ingestion**](../features/dashboards.md#run-ingestion) button |

The project page uses these routes for its ingestion tab:

| Method and path | What it does |
|-----------------|--------------|
| `GET /projects/ingestion-runs/{project_id}` | The project's ingestion runs, newest first, with `limit` and `skip`. Paths and host details are removed for viewers who cannot edit the project |
| `GET /projects/ingestion/trigger-status/{project_id}` | Whether **Run ingestion** is offered (`enabled`), usable by the caller (`available`), and the `reason` when it is not |
| `POST /projects/ingestion/trigger/{project_id}` | Starts an ingestion; `overwrite` as a query parameter. Returns `job_id`, `run_id` and `already_running` |

`GET /utils/capabilities` lists `jobs`, `deltatables.async_upsert` and
`ingestion.browser_trigger` in its `features` when each is turned on, so a client can
check before relying on them.
