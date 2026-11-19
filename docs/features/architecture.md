---
title: "Architecture"
icon: material/sitemap
description: "Technical overview of Depictio's microservices architecture."
---

# :material-sitemap: Architecture

Depictio is built on a modern microservices architecture that provides flexibility, scalability, and maintainability.

[![Depictio v1.21.0: the browser reaches the viewer (nginx), which proxies the FastAPI backend; the CLI calls the API and writes Delta tables to S3; an optional identity provider handles SSO. The API and the Celery workers (queue celery, and an optional ingestion queue) read and write MongoDB, the S3 store (SeaweedFS or yours) and Redis. Outbound calls are all optional](../images/architecture/system_light.png#only-light)](../images/architecture/system_light.png){target=_blank}
[![Depictio v1.21.0: the browser reaches the viewer (nginx), which proxies the FastAPI backend; the CLI calls the API and writes Delta tables to S3; an optional identity provider handles SSO. The API and the Celery workers (queue celery, and an optional ingestion queue) read and write MongoDB, the S3 store (SeaweedFS or yours) and Redis. Outbound calls are all optional](../images/architecture/system_dark.png#only-dark)](../images/architecture/system_dark.png){target=_blank}

The figure draws the default: the browser reads indexed files (genome tracks, 3D structures)
from S3 through presigned URLs. With `DEPICTIO_S3_BROWSER_ACCESS=proxy` <small>(v1.22.0+)</small>
they go through the API instead (see [Data Flow](#data-flow)).

## :material-view-module: Microservices Overview

Depictio's architecture consists of six main components organized by category:

### :material-server: Core Services

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-api: **Backend** | FastAPI | RESTful API, authentication, business logic |
| :material-react: **Frontend** | React + Vite + Mantine | Vite SPA served by nginx, which also proxies the API; no state of its own |

### :material-database: Data Layer

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-database-outline: **Database** | MongoDB | Metadata, users, configurations |
| :material-cloud-upload: **Storage** | S3 (SeaweedFS when bundled) | Data files, Delta Lake tables |

### :material-server-network: Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-memory: **Cache/Broker** | Redis | DataFrame cache, Celery queue and results, live events |
| :material-cog-refresh: **Worker** | Celery | Previews, code figures, screenshots, MultiQC; always on. A second worker for ingestion is optional |

---

### :material-api: FastAPI Backend

The backend service is built with FastAPI, a modern, high-performance web framework:

- :material-routes: RESTful API endpoints for all platform functionality
- :material-key: JWT-based authentication and authorization
- :material-lightning-bolt: Asynchronous request handling for improved performance
- :material-check-decagram: Pydantic models for data validation and serialization
- :material-database-sync: Beanie ODM for MongoDB integration

### :material-database-outline: MongoDB Database

MongoDB serves as the primary database, storing:

- :material-account-multiple: User accounts and authentication information
- :material-folder-cog: Project metadata and configurations
- :material-sitemap: Workflow definitions and run information
- :material-view-dashboard-edit: Dashboard layouts, structure, and content
- :material-table-of-contents: Data collection metadata

### :material-cloud-upload: S3 Storage

S3-compatible object storage holds:

- :material-delta: Processed data ready for visualization (Delta Lake format)
- :material-dna: Genome-browser compatible data
- :material-file-multiple: Large file assets

Docker Compose and the Helm chart bundle [SeaweedFS](https://github.com/seaweedfs/seaweedfs)
as the store since v1.12.0 (MinIO before). Any S3 endpoint can replace it: see
[External S3](../installation/docker.md#external-s3).

### :material-memory: Redis Cache/Broker

Redis serves three purposes in Depictio, each on its own database:

- :material-cached: **Caching** (db 0): DataFrames read from Delta tables, and the per-address limit on sign-in attempts
- :material-message-fast: **Task Broker** (db 1 and 2): message broker and result backend for Celery background tasks
- :material-lightning-bolt: **Live events** (db 3): the pub/sub channel of [real-time events](#real-time-events-v114)

Sessions are not kept in Redis: tokens live in MongoDB, and the browser keeps its own copy.

### :material-react: Frontend — React viewer

The frontend is a Vite + Mantine **React SPA** (`depictio/viewer/`, shared `packages/depictio-react-core/`), graduating onto canonical URLs in **v1.0.0**. It provides:

- :material-chart-scatter-plot: Interactive data visualization components
- :material-sync: Real-time data updates
- :material-drag: Draggable and customizable dashboard layouts
- :material-api: Integration with the backend API

The legacy Plotly Dash frontend was removed in v0.13.12. See the [changelog](../changelog/README.md) for the full migration history.

---

## :material-apps: React SPA Surfaces (v1.0.0+)

The React viewer (`depictio/viewer/`) is a single Vite SPA served by nginx with a fallback rewrite. It exposes three logical surfaces against the same FastAPI backend:

| Surface | URL Pattern | Purpose |
|---------|-------------|---------|
| :material-cog: **Management** | `/dashboards`, `/projects`, `/admin` | Dashboard listing, project management, admin panel |
| :material-eye: **Viewer** | `/dashboard/{id}` | Read-only dashboard viewing |
| :material-pencil: **Editor** | `/dashboard-edit/{id}` | Dashboard editing and component creation |

During the v0.12–v0.13 series the same surfaces ran at `/*-beta` paths alongside the legacy Dash frontend. Dash was removed in v0.13.12; the `*-beta` suffix paths redirect to canonical in v1.0.0.

---

## :material-cog-refresh: Background Processing (v0.6.0+)

Depictio supports **background task processing** using Celery and Redis for computations that would otherwise block the UI.

[![The API runs cheap work itself and queues the rest on Redis db 1, queue celery or the optional queue ingestion; a worker writes its result to db 2, which the API polls. Awaited: previews, code figures, renders of large tables, advanced viz. Fire and forget: screenshots, MultiQC prerender, remote data refresh. A job on ingestion: a big upsert or an ingestion run from the browser](../images/architecture/tasks_light.png#only-light)](../images/architecture/tasks_light.png){target=_blank}
[![The API runs cheap work itself and queues the rest on Redis db 1, queue celery or the optional queue ingestion; a worker writes its result to db 2, which the API polls. Awaited: previews, code figures, renders of large tables, advanced viz. Fire and forget: screenshots, MultiQC prerender, remote data refresh. A job on ingestion: a big upsert or an ingestion run from the browser](../images/architecture/tasks_dark.png#only-dark)](../images/architecture/tasks_dark.png){target=_blank}

### :material-help-circle: When Background Processing is Used

The worker always runs; there is nothing to turn on.

| Work | Runs on the worker |
|------|--------------------|
| :material-pencil: Figure previews in the editor | By default (`DEPICTIO_CELERY_OFFLOAD_PREVIEW`) |
| :material-eye: Dashboard renders | When the source table is 50 MB or more, or always with `DEPICTIO_CELERY_OFFLOAD_RENDERING` |
| :material-code-braces: Code figures | Always, to keep user code off the API |
| :material-camera: Dashboard thumbnails | Always |
| :material-database-import: Offloaded ingestion | On the separate [ingestion worker](../installation/docker.md#ingestion-worker) |

### :material-variable: Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CELERY_WORKERS` | `4` | Worker processes, set on the worker container |
| `DEPICTIO_CELERY_BROKER_HOST` | `redis` | Redis broker hostname |
| `DEPICTIO_CELERY_BROKER_PORT` | `6379` | Redis broker port |
| `DEPICTIO_CELERY_BROKER_DB` | `1` | Redis database for Celery broker |
| `DEPICTIO_CELERY_RESULT_BACKEND_DB` | `2` | Redis database for Celery results |

All of them, including the offload thresholds: [Celery Task Queue](../installation/env-reference.md#celery-task-queue).

---

## :material-lightning-bolt: Real-time Events (v1.1.4+)

Depictio can push **live dashboard updates over WebSocket** when the data behind a dashboard changes, so viewers refresh without polling. The subsystem is disabled by default (`DEPICTIO_EVENTS_ENABLED`) and opt-in per project.

[![A producer upserts a data collection; the API (or the ingestion worker) re-reads the Delta table and publishes on Redis db 3, which reaches every API process; each sends data_collection_updated over WebSocket, and an open dashboard that reads the collection refetches. An optional MongoDB change stream feeds the same broadcast](../images/architecture/realtime_light.png#only-light)](../images/architecture/realtime_light.png){target=_blank}
[![A producer upserts a data collection; the API (or the ingestion worker) re-reads the Delta table and publishes on Redis db 3, which reaches every API process; each sends data_collection_updated over WebSocket, and an open dashboard that reads the collection refetches. An optional MongoDB change stream feeds the same broadcast](../images/architecture/realtime_dark.png#only-dark)](../images/architecture/realtime_dark.png){target=_blank}

Moving parts:

- :material-server-network: **Event service + connection manager** (FastAPI): track WebSocket subscriptions per dashboard and broadcast `data_collection_updated` events.
- :material-memory: **Redis pub/sub**: fans events out across API workers and replicas, on a dedicated Redis DB (default `3`, separate from cache and Celery).
- :material-database-sync: **MongoDB change streams** (optional, requires a replica set): detect data-collection changes at the database layer.
- :material-transit-connection-variant: **WebSocket channel** `/depictio/api/v1/events/ws`: JWT-authenticated via a `token` query parameter and permission-checked at viewer level; the React viewer subscribes per dashboard and drives the live indicator.

Activation requires both the server flag and a `realtime` block in the project's `project.yaml`.

See the [Real-time events guide](../usage/guides/realtime-events.md) for setup, and the [environment reference](../installation/env-reference.md#real-time-events) for the full `DEPICTIO_EVENTS_*` list.

---

## :material-arrow-decision: Data Flow

The figure at the top of this page draws it:

1. :material-console: **CLI** reads the run's files, writes the Delta tables to S3 itself, then registers them through the API (`/deltatables/upsert`), which records the metadata in MongoDB. *Add data* in the web UI does the same on the server.
2. :material-api: **API** answers every figure, table and card: it reads the Delta tables from S3, with the frames cached in Redis.
3. :material-react: **React viewer** only talks to the API, through its nginx proxy. It never reaches MongoDB, Redis or S3, except for indexed files (genome tracks, 3D structures), read from S3 through presigned URLs. With [`DEPICTIO_S3_BROWSER_ACCESS=proxy`](../installation/env-reference.md#s3-browser-access) <small>(v1.22.0+)</small> the API streams those too, for an S3 store browsers cannot reach.

---

## :material-book-open-page-variant: Related Documentation

- :material-view-dashboard-variant: [Dashboards](dashboards.md) - Dashboard modes, tabs, and layouts
- :material-puzzle: [Components](components.md) - Available component types
- :material-database-outline: [Data Model](data-model.md) - Domain objects and relationship model
- :material-shield-check: [Security](security.md) - Security features and code restrictions
- :material-lightning-bolt: [Real-time events](../usage/guides/realtime-events.md) - Enabling live WebSocket dashboard refresh
