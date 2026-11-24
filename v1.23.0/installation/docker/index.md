# Docker Compose Installation

## Quick Start

**Prerequisites**: [Docker](https://docs.docker.com/get-docker/) 20.10+ and [Docker Compose](https://docs.docker.com/compose/install/) V2.

### Step 1 — Download the compose file

```
curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml
```

### Step 2 — Start

```
docker compose up -d
```

All services start automatically: MongoDB, Redis, the S3 store (SeaweedFS), backend, viewer, and Celery worker.

Upgrading an install from before v1.12.0?

The bundled S3 store is SeaweedFS instead of MinIO since v1.12.0, and it starts empty: copy your data over first. See [Upgrading to v1.12.0: MinIO → SeaweedFS](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/#docker-compose).

### Step 3 — Open

| Service  | URL                          | Credentials                    |
| -------- | ---------------------------- | ------------------------------ |
| Depictio | <http://localhost:5080>      | *(single-user mode, no login)* |
| API docs | <http://localhost:8058/docs> | —                              |

The S3 store is reachable only inside the Compose network, under the `s3` host name (`minio` still works as an alias), with the credentials `minio` / `minio123` unless you set your own.

That's it!

Depictio starts in **single-user mode** by default — no login, no configuration needed.

Exposing to the network?

Single-user mode disables credential enforcement. Before sharing or deploying beyond localhost, switch to multi-user mode and set strong credentials — see [Custom credentials](#custom-credentials-env-file) below.

______________________________________________________________________

## Advanced Configuration

Everything in this section is **optional**. The Quick Start defaults work for most users.

### Single-user vs Multi-user mode

Depictio ships in **single-user mode** by default: no login, no accounts, one admin user.

| Mode                        | `DEPICTIO_AUTH_SINGLE_USER_MODE` | `DEPICTIO_AUTH_PUBLIC_MODE` | Use case                            |
| --------------------------- | -------------------------------- | --------------------------- | ----------------------------------- |
| **Single-user** *(default)* | `true`                           | `false`                     | Local development, personal use     |
| **Multi-user**              | `false`                          | `false`                     | Team deployment with login          |
| **Public (read-only)**      | `false`                          | `true`                      | Shared dashboards, no auth required |

Switch to multi-user mode and set strong credentials in your `.env`:

```
DEPICTIO_AUTH_SINGLE_USER_MODE=false

# Required in multi-user mode, read on first boot
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=$(openssl rand -base64 24)

# S3 password must be ≥ 8 chars and not a known default
DEPICTIO_S3_ROOT_PASSWORD=$(openssl rand -base64 12)
```

Users can then register accounts and log in via the Depictio UI.

Bootstrap is idempotent

The admin account is created only when no non-anonymous admin exists in MongoDB. Changing the bootstrap vars after first boot has no effect.

Expose to the network?

If making Depictio accessible beyond `localhost`, disable single-user mode and change the S3 credentials.

### Custom Credentials (.env file)

To change the S3 credentials or pin a specific version, copy the example file:

```
cp .env.example .env
```

Edit `.env`:

```
# Image tag. Unset: the release the compose file pins; `next` follows main
DEPICTIO_VERSION=1.21.0

# First admin: required in multi-user mode on an empty database (single-user mode seeds its own)
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.com
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=change-me-strong-password-here

# S3 credentials: in multi-user mode at least 8 chars and not a known default
# Named DEPICTIO_MINIO_* before v1.12.0; the old names still work
DEPICTIO_S3_ROOT_USER=myadmin
DEPICTIO_S3_ROOT_PASSWORD=change-me-strong-password-here
```

Bootstrap is idempotent

The admin account is created only on first boot (when no non-anonymous admin exists in MongoDB). Restarting the container or changing the bootstrap vars afterwards has no effect: use the admin UI to manage credentials.

Full reference

- [Configuration](https://depictio.github.io/depictio-docs/latest/installation/configuration/index.md): what to set first, then by topic
- [Environment Reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/index.md): every variable, with its default

### External S3

If you already have S3-compatible storage (AWS, NetApp, Ceph, your own MinIO, …), use the compose file without the bundled store:

```
docker compose -f docker-compose/docker-compose.no-minio.yaml up -d
```

Configure your `.env` to point to your existing instance:

```
DEPICTIO_S3_ROOT_USER=your-access-key
DEPICTIO_S3_ROOT_PASSWORD=your-secret-key
DEPICTIO_S3_PUBLIC_URL=https://your-s3-host.example.com
DEPICTIO_S3_EXTERNAL_SERVICE=true
# Optional overrides
DEPICTIO_S3_EXTERNAL_HOST=your-s3-host.example.com
DEPICTIO_S3_EXTERNAL_PORT=9000
DEPICTIO_S3_EXTERNAL_PROTOCOL=https
```

Network Configuration

Set `DEPICTIO_S3_EXTERNAL_SERVICE=true` when the store is outside the Docker Compose network.

The bucket does not have to exist

From **v1.6.0** the server creates `DEPICTIO_S3_BUCKET` at startup when it is missing, then verifies it; an existing bucket is left untouched. See [Required S3 permissions](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#required-s3-permissions).

S3-Compatible Storage

Depictio talks to the store through the S3 API (boto3, s3fs, delta-rs), with no MinIO-specific client. AWS S3, DigitalOcean Spaces, Backblaze B2, and others may work but have not been officially tested.

### Port Configuration

Default ports:

| Service                 | Default port                      |
| ----------------------- | --------------------------------- |
| Frontend (React viewer) | 5080                              |
| Backend API             | 8058, on `127.0.0.1`              |
| MongoDB                 | 27018, inside the Compose network |
| S3 API (SeaweedFS)      | 9000, inside the Compose network  |

The development stack (`docker-compose.dev.yaml`) also publishes the S3 API and the SeaweedFS admin UI on `127.0.0.1`. Move them in `.env` with `S3_PORT` (default `9000`) and `S3_CONSOLE_PORT` (default `9001`), named `MINIO_PORT` and `MINIO_CONSOLE_PORT` before v1.12.0, which still work.

### Development Mode

Reload the API and restart the worker on code changes (telemetry and the walkthrough are off too):

```
DEPICTIO_DEV_MODE=true docker compose up -d
```

Or set `DEPICTIO_DEV_MODE=true` in your `.env` file.

### Celery worker

The `depictio-celery-worker` container always starts: figure previews in the editor, large renders and dashboard thumbnails run on it. Size it in `.env` with `DEPICTIO_CELERY_WORKERS` (default `4` processes); each process holds its own data, so memory sets the limit. When renders are offloaded is set by the `DEPICTIO_CELERY_OFFLOAD_*` variables: see [Celery Task Queue](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#celery-task-queue).

### Ingestion worker (v1.15.0+)

`depictio-ingestion-worker` is a second Celery worker for long ingestion tasks: profiling a table after the CLI has written it, and an ingestion started from a project page. It runs the same image as `depictio-celery-worker` but reads only the `ingestion` queue, so a 20-minute table read never holds up the dashboard editor. It is behind a Compose profile, so `docker compose up -d` alone does not start it:

```
docker compose --profile ingestion up -d
```

| Variable                                | Default | Description                                                                                   |
| --------------------------------------- | ------- | --------------------------------------------------------------------------------------------- |
| `DEPICTIO_INGESTION_WORKER_CONCURRENCY` | `2`     | Tasks run at once. Each holds a table's columns in memory, so memory runs out before CPU does |

Each worker process takes one task at a time and is replaced after 10 tasks. The worker stays idle until one of the two features below is turned on. Both are off by default, and only this Compose file has the worker: the Helm chart and `depictio local up` do not start one.

Set `DEPICTIO_VERSION` before starting the profile

In the v1.15.0 `docker-compose.yaml`, this service defaults to the `1.14.0` image while the others default to `1.15.0`. That image ignores the queue setting, reads the dashboard queue instead of `ingestion`, and never reports healthy. Set `DEPICTIO_VERSION=1.15.0` in `.env`.

Start the worker before turning either feature on. With nothing reading the `ingestion` queue, jobs stay pending.

The server-side ingestions of remote data (v1.16.0+), a project created [from a run folder](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#from-a-run-folder) and a [**Data refresh**](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#refreshing-the-data), run on `depictio-celery-worker` instead: they need neither this worker nor `DEPICTIO_JOBS_ENABLED`.

#### Offloading the table profile

After the CLI writes a Delta table, the server reads it back to profile its columns. On a large table that takes longer than an HTTP request should. With offloading on, the server records the new table version at once and hands the profiling to the ingestion worker. A CLI run with `--async-upsert` then waits for that job instead of a response.

```
# .env
DEPICTIO_JOBS_ENABLED=true
DEPICTIO_INGESTION_ASYNC_DELTATABLE_UPSERT=true
```

```
depictio ingest results/ --server ~/.depictio/CLI.yaml --async-upsert
```

The CLI waits at most `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` for each job (`3600`; `0` waits without limit). Without both settings, or against an older server, the server ignores `--async-upsert` and profiles the table within the request. MultiQC collections are never offloaded.

#### Starting an ingestion from the browser

This turns on [**Run ingestion**](https://depictio.github.io/depictio-docs/latest/features/dashboards/#run-ingestion) on project pages. The server then scans and processes the data itself, so it has to see the files: `depictio-backend` checks that the data locations exist, and `depictio-ingestion-worker` reads them.

```
# .env
DEPICTIO_JOBS_ENABLED=true
DEPICTIO_INGESTION_BROWSER_TRIGGER=true
DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS=/data/runs
```

`DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS` takes a comma-separated or JSON list of directories. Every data location, single-file path and image directory of a project must resolve inside one of them, following symlinks, and so must every file the scan registers. It is checked when the button is pressed, again when the worker starts, and on the registered files before they are read. Any signed-in user can create a project and name any path in it, so this list is what keeps an ingestion away from other groups' runs and from the server's own files. Empty, it refuses every ingestion.

Mount the data at the same path in both containers, for example read-only from a `docker-compose.override.yaml` next to `docker-compose.yaml`:

```
services:
  depictio-backend:
    volumes:
      - /srv/sequencing/runs:/data/runs:ro
  depictio-ingestion-worker:
    volumes:
      - /srv/sequencing/runs:/data/runs:ro
```

The projects then name their data under `/data/runs`, the path inside the containers.

On the server, the scan skips any symlink that points outside the directory it walks, so it cannot be led out of the allowed directories. A results directory that Nextflow filled with links into `work/` (`publishDir mode: 'symlink'`) therefore yields no files: publish copies instead, or ingest it with the CLI, which reads a symlinked file wherever it points.

#### Request timeouts

Since v1.15.0 the API server lets a request run for 300 seconds instead of 120, as long as the CLI waits for the server to profile a written table. Before, a slow profile was cut off and the CLI saw a dropped connection rather than an error. The bundled viewer's nginx allows 3600 seconds on API requests. A reverse proxy in front of Depictio should allow at least 300 seconds, or the CLI should use `--async-upsert`.

______________________________________________________________________

## Managing Services

| Action                               | Command                                   |
| ------------------------------------ | ----------------------------------------- |
| Stop (preserve data)                 | `docker compose stop`                     |
| Stop and remove containers           | `docker compose down`                     |
| Stop, remove containers **and data** | `docker compose down -v`                  |
| View all logs                        | `docker compose logs -f`                  |
| View one service                     | `docker compose logs -f depictio-backend` |
| Check status                         | `docker compose ps`                       |

______________________________________________________________________

## Troubleshooting

### A container fails to start

```
docker compose logs <service_name>
```

Common causes: port conflict, volume permission error, MongoDB connection failure.

### Cannot connect to services

1. Check containers are running: `docker compose ps`
1. Confirm you are using the correct ports
1. Check for firewall rules blocking the connection

### Data persistence

MongoDB, Redis and the S3 store keep their data in named Docker volumes (`mongo_data`, `redis_data` and `seaweedfs_data`). They persist across `docker compose down`, and `docker compose down -v` deletes them. Before v1.12.0 the store was MinIO, in a `minio_data` volume that SeaweedFS does not read: see [Upgrading to v1.12.0](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/index.md).

______________________________________________________________________

## Next Steps

- [Get started with Depictio](https://depictio.github.io/depictio-docs/latest/usage/get_started/index.md)
- [Create your first dashboard](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md)
- [Ingest data with the CLI](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md)
