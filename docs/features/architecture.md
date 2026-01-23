---
title: "Architecture"
icon: material/sitemap
description: "Technical overview of Depictio's microservices architecture."
---

# :material-sitemap: Architecture

Depictio is built on a modern microservices architecture that provides flexibility, scalability, and maintainability.

<p align="center">
  <img src="../../images/modularity/main.png" alt="Depictio architecture" width=800>
</p>

## :material-view-module: Microservices Overview

Depictio's architecture consists of six main components organized by category:

### :material-server: Core Services

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-api: **Backend** | FastAPI | RESTful API, authentication, business logic |
| :material-view-dashboard: **Frontend** | Plotly Dash | Interactive dashboards |

### :material-database: Data Layer

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-database-outline: **Database** | MongoDB | Metadata, users, configurations |
| :material-cloud-upload: **Storage** | MinIO/S3 | Data files, Delta Lake tables |

### :material-server-network: Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| :material-memory: **Cache/Broker** | Redis | Caching, session storage, Celery task broker |
| :material-cog-refresh: **Worker** | Celery (Optional) | Background task processing |

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
- :material-workflow: Workflow definitions and run information
- :material-view-dashboard-edit: Dashboard layouts, structure, and content
- :material-table-of-contents: Data collection metadata

### :material-cloud-upload: MinIO S3 Storage (Optional)

MinIO provides S3-compatible object storage for:

- :material-delta: Processed data ready for visualization (Delta Lake format)
- :material-dna: Genome-browser compatible data
- :material-file-multiple: Large file assets

### :material-memory: Redis Cache/Broker

Redis serves dual purposes in Depictio:

- :material-cached: **Caching**: DataFrame caching and session storage for improved performance
- :material-message-fast: **Task Broker**: Message broker and result backend for Celery background tasks

### :material-view-dashboard: Plotly Dash Frontend

The frontend is built with Plotly Dash (React), providing:

- :material-chart-scatter-plot: Interactive data visualization components
- :material-sync: Real-time data updates
- :material-drag: Draggable and customizable dashboard layouts
- :material-api: Integration with the backend API

---

## :material-apps: Multi-App Architecture (v0.6.0+)

Starting with version 0.6.0, Depictio uses a **multi-app architecture** that separates the frontend into three independent Dash applications:

```text
┌─────────────────────────────────────────────────────────────────┐
│                     Flask Dispatcher                             │
│                   (flask_dispatcher.py)                          │
└───────────────┬───────────────┬───────────────┬─────────────────┘
                │               │               │
    ┌───────────▼───────┐ ┌─────▼─────┐ ┌───────▼───────────┐
    │   Management App  │ │ Viewer App│ │    Editor App     │
    │        /          │ │ /dashboard│ │  /dashboard-edit  │
    │                   │ │           │ │                   │
    │ • Authentication  │ │ • Read-   │ │ • Dashboard       │
    │ • Dashboard list  │ │   only    │ │   editing         │
    │ • Projects page   │ │   viewing │ │ • Component       │
    │ • Admin panel     │ │ • Data    │ │   creation        │
    │                   │ │   updates │ │ • Design mode     │
    └───────────────────┘ └───────────┘ └───────────────────┘
```

### :material-format-list-group: App Responsibilities

| App | URL Pattern | Purpose |
|-----|-------------|---------|
| :material-cog: **Management** | `/`, `/auth`, `/dashboards`, `/projects`, `/admin` | Authentication, listing, project management |
| :material-eye: **Viewer** | `/dashboard/{id}` | Read-only dashboard viewing |
| :material-pencil: **Editor** | `/dashboard-edit/{id}` | Dashboard editing and component creation |

### :material-star: Benefits

1. :material-call-split: **Callback Isolation**: Each app has its own callback registry, preventing conflicts
2. :material-speedometer: **Performance**: Reduced callback overhead per app
3. :material-shield-lock: **Security**: Editor functionality isolated from viewer mode
4. :material-trending-up: **Scalability**: Apps can be optimized independently

---

## :material-cog-refresh: Background Processing (v0.6.0+)

Depictio supports **background task processing** using Celery and Redis for computations that would otherwise block the UI.

```text
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Dash App   │────▶│  Celery Worker  │────▶│    Redis    │
│  (Editor)   │     │                 │     │  (Broker)   │
└─────────────┘     └─────────────────┘     └─────────────┘
```

The Dash application submits tasks to Celery workers, which use Redis as both a message broker (for task queuing) and result backend (for storing task results).

### :material-help-circle: When Background Processing is Used

| Context | Background Processing |
|---------|----------------------|
| :material-pencil: Editor (design mode) | Always required |
| :material-eye: Viewer app | Optional (`DEPICTIO_CELERY_ENABLED`) |
| :material-cog: Management app | Never (no heavy computations) |

### :material-cog-outline: Configuration

To enable background processing:

1. **Set the environment variable** in your `.env` file or Docker Compose configuration:

```bash
DEPICTIO_CELERY_ENABLED=true
```

2. **Restart the full Docker Compose stack** to apply the change:

```bash
docker compose down && docker compose up -d
```

!!! note "Full Restart Required"
    After changing `DEPICTIO_CELERY_ENABLED`, you must restart the entire Docker Compose stack for the change to take effect across all services.

### :material-variable: Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CELERY_ENABLED` | `false` | Enable background callbacks |
| `DEPICTIO_CELERY_BROKER_HOST` | `redis` | Redis broker hostname |
| `DEPICTIO_CELERY_BROKER_PORT` | `6379` | Redis broker port |
| `DEPICTIO_CELERY_BROKER_DB` | `1` | Redis database for Celery broker |
| `DEPICTIO_CELERY_RESULT_BACKEND_DB` | `2` | Redis database for Celery results |

---

## :material-arrow-decision: Data Flow

```text
┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────┐
│  CLI    │────▶│  FastAPI    │────▶│  MongoDB    │◀────│  Dash   │
│         │     │  Backend    │     │             │     │  UI     │
└─────────┘     └──────┬──────┘     └─────────────┘     └────┬────┘
                       │                                      │
                       ▼                                      │
                ┌─────────────┐                               │
                │   MinIO     │◀──────────────────────────────┘
                │  (Delta)    │
                └─────────────┘
```

1. :material-console: **CLI** ingests data, validates, stores in Delta format, registers in MongoDB
2. :material-api: **API** serves metadata and data access endpoints
3. :material-view-dashboard: **Dash UI** renders interactive visualizations, calls API for data

---

## :material-book-open-page-variant: Related Documentation

- :material-view-dashboard-variant: [Dashboards](dashboards.md) - Dashboard modes, tabs, and layouts
- :material-puzzle: [Components](components.md) - Available component types
- :material-developer-board: [Modularity](../developer/modularity.md) - Code structure and API design
- :material-shield-check: [Security](security.md) - Security features and code restrictions
