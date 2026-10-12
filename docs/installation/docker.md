---
icon: simple/docker
---

# Docker Compose Installation

## :material-rocket-launch: Quick Start

**Prerequisites**: [Docker](https://docs.docker.com/get-docker/) 20.10+ and [Docker Compose](https://docs.docker.com/compose/install/) V2.

### Step 1 — Download the compose file

```bash
curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml
```

### Step 2 — Start

```bash
docker compose up -d
```

All services start automatically: MongoDB, Redis, the S3 store (SeaweedFS), backend, viewer, and Celery worker.

!!! warning "Upgrading an install from before v1.12.0?"
    The bundled S3 store is SeaweedFS instead of MinIO since v1.12.0, and it starts
    empty: copy your data over first. See
    [Upgrading to v1.12.0: MinIO → SeaweedFS](upgrade/v1.12.0-seaweedfs.md#docker-compose).

### Step 3 — Open

| Service | URL | Credentials |
|---------|-----|-------------|
| Depictio | <http://localhost:5080> | _(single-user mode, no login)_ |
| API docs | <http://localhost:8058/docs> | — |

The S3 store is reachable only inside the Compose network, under the `s3` host name
(`minio` still works as an alias), with the credentials `minio` / `minio123` unless you
set your own.

!!! success "That's it!"
    Depictio starts in **single-user mode** by default — no login, no configuration needed.

!!! warning "Exposing to the network?"
    Single-user mode disables credential enforcement. Before sharing or deploying beyond localhost, switch to multi-user mode and set strong credentials — see [Custom credentials](#custom-credentials-env-file) below.

---

## :material-cog-outline: Advanced Configuration

Everything in this section is **optional**. The Quick Start defaults work for most users.

### Single-user vs Multi-user mode

Depictio ships in **single-user mode** by default: no login, no accounts, one admin user.

| Mode | `DEPICTIO_AUTH_SINGLE_USER_MODE` | `DEPICTIO_AUTH_PUBLIC_MODE` | Use case |
|------|----------------------------------|-----------------------------|---------:|
| **Single-user** _(default)_ | `true` | `false` | Local development, personal use |
| **Multi-user** | `false` | `false` | Team deployment with login |
| **Public (read-only)** | `false` | `true` | Shared dashboards, no auth required |

Switch to multi-user mode and set strong credentials in your `.env`:

```bash
DEPICTIO_AUTH_SINGLE_USER_MODE=false

# Required in multi-user mode — set on first boot
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=changeme

# S3 password must be ≥ 8 chars and not a known default
DEPICTIO_S3_ROOT_PASSWORD=$(openssl rand -base64 12)
```

Users can then register accounts and log in via the Depictio UI.

!!! info "Bootstrap is idempotent"
    The admin account is created only when no non-anonymous admin exists in MongoDB. Changing the bootstrap vars after first boot has no effect.

!!! warning "Expose to the network?"
    If making Depictio accessible beyond `localhost`, disable single-user mode and change the S3 credentials.

### Custom Credentials (.env file)

To change the S3 credentials or pin a specific version, copy the example file:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Application version (default: latest)
DEPICTIO_VERSION=latest

# Admin account — REQUIRED on first boot (all modes)
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=change-me-strong-password-here

# S3 credentials — REQUIRED in multi-user mode, ≥ 8 chars (enforced at startup from v1.0.0-b1)
# Named DEPICTIO_MINIO_* before v1.12.0; the old names still work
DEPICTIO_S3_ROOT_USER=myadmin
DEPICTIO_S3_ROOT_PASSWORD=change-me-strong-password-here
```

!!! info "Bootstrap is idempotent"
    The admin account is created only on first boot (when no non-anonymous admin exists in MongoDB). Restarting the container or changing the bootstrap vars afterwards has no effect — use the admin UI to manage credentials.

!!! tip "Full reference"
    - **Complete env file**: `.env.complete.example` — all 160+ variables with defaults
    - **Configuration Guide**: [Configuration](configuration.md) — common use cases
    - **Full Reference**: [Environment Reference](env-reference.md) — all variables

### External S3 { #external-s3 }

If you already have S3-compatible storage (AWS, NetApp, Ceph, your own MinIO, …), use the compose file without the bundled store:

```bash
docker compose -f docker-compose/docker-compose.no-minio.yaml up -d
```

Configure your `.env` to point to your existing instance:

```bash
DEPICTIO_S3_ROOT_USER=your-access-key
DEPICTIO_S3_ROOT_PASSWORD=your-secret-key
DEPICTIO_S3_PUBLIC_URL=https://your-s3-host.example.com
DEPICTIO_S3_EXTERNAL_SERVICE=true
# Optional overrides
DEPICTIO_S3_EXTERNAL_HOST=your-s3-host.example.com
DEPICTIO_S3_EXTERNAL_PORT=9000
DEPICTIO_S3_EXTERNAL_PROTOCOL=https
```

!!! note "Network Configuration"
    Set `DEPICTIO_S3_EXTERNAL_SERVICE=true` when the store is outside the Docker Compose network.

!!! note "The bucket does not have to exist"
    From **v1.6.0** the server creates `DEPICTIO_S3_BUCKET` at startup when it is
    missing, then verifies it; an existing bucket is left untouched. See
    [Required S3 permissions](env-reference.md#required-s3-permissions).

!!! info "S3-Compatible Storage"
    Depictio talks to the store through the S3 API (boto3, s3fs, delta-rs), with no MinIO-specific client. AWS S3, DigitalOcean Spaces, Backblaze B2, and others may work but have not been officially tested.

### Port Configuration

Default ports:

| Service | Default port |
|---------|-------------|
| Frontend (React viewer) | 5080 |
| Backend API | 8058, on `127.0.0.1` |
| MongoDB | 27018, inside the Compose network |
| S3 API (SeaweedFS) | 9000, inside the Compose network |

The development stack (`docker-compose.dev.yaml`) also publishes the S3 API and the
SeaweedFS admin UI on `127.0.0.1`. Move them in `.env` with `S3_PORT` (default `9000`)
and `S3_CONSOLE_PORT` (default `9001`), named `MINIO_PORT` and `MINIO_CONSOLE_PORT`
before v1.12.0, which still work.

### Development Mode

Enable debug logging and hot-reload:

```bash
DEPICTIO_DEV_MODE=true docker compose up -d
```

Or set `DEPICTIO_DEV_MODE=true` in your `.env` file.

### Background Callbacks (Celery)

Depictio uses Celery for asynchronous processing. The `depictio-celery-worker` container always starts automatically — it is **required** for the dashboard editor (design mode).

```bash
# Configure view-mode behaviour in .env
DEPICTIO_CELERY_ENABLED=true   # false = synchronous view mode (simpler for debugging)
```

| Mode | `DEPICTIO_CELERY_ENABLED` | Behaviour |
|------|--------------------------|-----------|
| Design mode (editor) | always on | Non-blocking figure preview — required |
| View mode | `true` | Async data loading — recommended for production |
| View mode | `false` | Synchronous — simpler for development |

!!! info "Kubernetes/Helm"
    Background callbacks are also supported in Kubernetes via the Helm chart (`celery.enabled: true` by default). See the [Kubernetes installation guide](kubernetes/).

### Ingestion worker <small>(v1.15.0+)</small> { #ingestion-worker }

`depictio-ingestion-worker` is a second Celery worker for long ingestion tasks: profiling
a table after the CLI has written it, and an ingestion started from a project page. It
runs the same image as `depictio-celery-worker` but reads only the `ingestion` queue, so
a 20-minute table read never holds up the dashboard editor. It is behind a Compose
profile, so `docker compose up -d` alone does not start it:

```bash
docker compose --profile ingestion up -d
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_INGESTION_WORKER_CONCURRENCY` | `2` | Tasks run at once. Each holds a table's columns in memory, so memory runs out before CPU does |

Each worker process takes one task at a time and is replaced after 10 tasks. The worker
stays idle until one of the two features below is turned on. Both are off by default,
and only this Compose file has the worker: the Helm chart and `depictio local up` do not
start one.

!!! warning "Set `DEPICTIO_VERSION` before starting the profile"
    In the v1.15.0 `docker-compose.yaml`, this service defaults to the `1.14.0` image
    while the others default to `1.15.0`. That image ignores the queue setting, reads the
    dashboard queue instead of `ingestion`, and never reports healthy. Set
    `DEPICTIO_VERSION=1.15.0` in `.env`.

Start the worker before turning either feature on. With nothing reading the `ingestion`
queue, jobs stay pending.

#### Offloading the table profile { #async-upsert }

After the CLI writes a Delta table, the server reads it back to profile its columns. On
a large table that takes longer than an HTTP request should. With offloading on, the
server records the new table version at once and hands the profiling to the ingestion
worker. A CLI run with `--async-upsert` then waits for that job instead of a response.

```bash
# .env
DEPICTIO_JOBS_ENABLED=true
DEPICTIO_INGESTION_ASYNC_DELTATABLE_UPSERT=true
```

```bash
depictio ingest results/ --server ~/.depictio/CLI.yaml --async-upsert
```

The CLI waits at most `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` for each job (`3600`; `0`
waits without limit). Without both settings, or against an older server, the server
ignores `--async-upsert` and profiles the table within the request. MultiQC collections
are never offloaded.

#### Starting an ingestion from the browser { #browser-trigger }

This turns on [**Run ingestion**](../features/dashboards.md#run-ingestion) on project
pages. The server then scans and processes the data itself, so it has to see the files:
`depictio-backend` checks that the data locations exist, and
`depictio-ingestion-worker` reads them.

```bash
# .env
DEPICTIO_JOBS_ENABLED=true
DEPICTIO_INGESTION_BROWSER_TRIGGER=true
DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS=/data/runs
```

`DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS` takes a comma-separated or JSON list of
directories. Every data location, single-file path and image directory of a project
must resolve inside one of them, following symlinks, and so must every file the scan
registers. It is checked when the button is pressed, again when the worker starts, and on
the registered files before they are read. Any signed-in user can create a project and
name any path in it, so this list is what keeps an ingestion away from other groups' runs
and from the server's own files. Empty, it refuses every ingestion.

Mount the data at the same path in both containers, for example read-only from a
`docker-compose.override.yaml` next to `docker-compose.yaml`:

```yaml
services:
  depictio-backend:
    volumes:
      - /srv/sequencing/runs:/data/runs:ro
  depictio-ingestion-worker:
    volumes:
      - /srv/sequencing/runs:/data/runs:ro
```

The projects then name their data under `/data/runs`, the path inside the containers.

On the server, the scan skips any symlink that points outside the directory it walks, so
it cannot be led out of the allowed directories. A results directory that Nextflow filled
with links into `work/` (`publishDir mode: 'symlink'`) therefore yields no files: publish
copies instead, or ingest it with the CLI, which reads a symlinked file wherever it
points.

#### Request timeouts

Since v1.15.0 the API server lets a request run for 300 seconds instead of 120, as long
as the CLI waits for the server to profile a written table. Before, a slow profile was
cut off and the CLI saw a dropped connection rather than an error. The bundled viewer's
nginx allows 3600 seconds on API requests. A reverse proxy in front of Depictio should
allow at least 300 seconds, or the CLI should use `--async-upsert`.

---

## :material-wrench: Managing Services

| Action | Command |
|--------|---------|
| Stop (preserve data) | `docker compose stop` |
| Stop and remove containers | `docker compose down` |
| Stop, remove containers **and data** | `docker compose down -v` |
| View all logs | `docker compose logs -f` |
| View one service | `docker compose logs -f depictio-backend` |
| Check status | `docker compose ps` |

---

## :material-bug: Troubleshooting

### A container fails to start

```bash
docker compose logs <service_name>
```

Common causes: port conflict, volume permission error, MongoDB connection failure.

### Cannot connect to services

1. Check containers are running: `docker compose ps`
2. Confirm you are using the correct ports
3. Check for firewall rules blocking the connection

### Data persistence

MongoDB, Redis and the S3 store keep their data in named Docker volumes (`mongo_data`, `redis_data` and `seaweedfs_data`). They persist across `docker compose down`, and `docker compose down -v` deletes them. Before v1.12.0 the store was MinIO, in a `minio_data` volume that SeaweedFS does not read: see [Upgrading to v1.12.0](upgrade/v1.12.0-seaweedfs.md).

---

## Next Steps

- [Get started with Depictio](../usage/get_started.md)
- [Create your first dashboard](../usage/guides/dashboard_creation.md)
- [Ingest data with the CLI](../depictio-cli/usage.md)
