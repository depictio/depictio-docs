---
title: "Local Server (no Docker)"
icon: material/laptop
description: "Run the full Depictio server on your own machine without Docker, then open the dashboard of your own pipeline results."
---

# Local Server (no Docker) <small>(v1.12.0+)</small>

`depictio local up` starts a complete Depictio server on your machine: the same
API, worker and viewer as the Docker and Kubernetes deployments, with MongoDB,
Redis and SeaweedFS (the S3 store) run as plain processes on `127.0.0.1`. It can
ingest a pipeline template in the same command, so you go from a results
directory to its dashboard without Docker, a cluster or a shared instance.

Use it to review a template on your own results, or to try Depictio on a laptop.
For a team, a demo or production, use [Docker Compose](docker.md) or
[Kubernetes](kubernetes.md).

![The same server, run in containers or as local processes](../images/installation/local/schema_same_code_docs.png)

---

## :material-rocket-launch: Quick Start

**Prerequisites**: [uv](https://docs.astral.sh/uv/getting-started/installation/),
and until the `depictio` package is published on PyPI, a clone of the repository
with [pnpm](https://pnpm.io/installation) to build the viewer.

### Step 1: Get the code and build the viewer

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
pnpm install --frozen-lockfile
(cd depictio/viewer && pnpm run build)
```

Without the viewer build the API starts, but dashboards do not render; `up` warns
about it.

### Step 2: Start the server

```bash
uv run --python 3.12 --extra local depictio local up
```

The first run downloads MongoDB, Redis and SeaweedFS from conda-forge into
`~/.depictio/local/env` (about 710 MB, once). The Iris and Penguins example
projects are seeded, and the browser opens on `http://127.0.0.1:8058/dashboards`.

!!! info "Once `depictio` is on PyPI"
    No clone and no build: the package carries the viewer, and one command
    replaces both steps.

    ```bash
    uvx --python 3.12 --from "depictio[local]" depictio local up
    ```

### Step 3: Open the dashboard of your own results

Pass a [template](../usage/projects/templates.md) and the pipeline output
directory:

```bash
uv run --extra local depictio local up \
  --template nf-core/ampliseq/latest \
  --data-root path/to/results
```

`up` starts the services, then runs `depictio run` against them with a CLI
configuration it generates, and prints the dashboard URL. Template variables go
through `--var`, as with [`depictio-cli run`](../depictio-cli/usage.md#run-command).
nf-core results do not contain the samplesheet: when the template cannot find it
under `input/`, pass it explicitly.

```bash
uv run --extra local depictio local up \
  --template nf-core/rnaseq/latest \
  --data-root path/to/results \
  --var SAMPLESHEET_FILE=samplesheet.csv
```

---

## :material-console: Commands

| Command | Effect |
|---------|--------|
| `depictio local up` | Start the services, seed examples or ingest a template, open the browser |
| `depictio local status` | Show which processes are running, the URL and the log directory |
| `depictio local down` | Stop every process; the data is kept for the next `up` |
| `depictio local wipe` | Stop and delete all data. The downloaded binaries are kept. `--yes` skips the prompt |
| `depictio local export-compose` | Copy the data into a directory that Docker Compose runs, see [Move to Docker Compose](#move-to-docker-compose) |

### `up` options

| Option | Default | Description |
|--------|---------|-------------|
| `--template` | | Template to ingest, e.g. `nf-core/rnaseq/latest`. Goes with `--data-root` |
| `--data-root` | | Pipeline results directory to ingest |
| `--project-name` | | Name of the ingested project |
| `--var KEY=VALUE` | | Template variable, repeatable. Relative paths are resolved from the current directory |
| `--examples` | `iris,penguins`, or `none` with `--template` | Example projects to seed: comma-separated names, `all` or `none` |
| `--port` | `8058`, or a free one | Port of the API and the viewer |
| `--open` / `--no-open` | `--open` | Open the dashboards page in a browser |
| `--screenshots` / `--no-screenshots` | off | Dashboard thumbnails through Playwright. Installs Chromium (about 150 MB) if needed |

Running `up` while the server is already up only ingests the new template.

---

## :material-cog-outline: How it differs from Docker

Only configuration differs, and only through the usual `DEPICTIO_*` variables:
every service is pointed at `127.0.0.1`.

| | Docker Compose | Local server |
|---|---|---|
| MongoDB, Redis, S3 | containers | `mongod`, `redis-server` and `weed mini` from conda-forge, fetched by [py-rattler](https://github.com/conda/rattler) |
| API | 4 workers | 1 uvicorn worker |
| Celery worker | container | 2 slots: `prefork` on Linux, `threads` on macOS |
| Viewer | its own container | served by the API, on the same port |
| Authentication | single-user, multi-user or public | single-user |
| Dashboard thumbnails | on | off unless `--screenshots` |

Ports are picked on `127.0.0.1`: the defaults (API `8058`, MongoDB `27018`, Redis
`6379`, S3 `9000`) when they are free, any free port otherwise, so a local server
runs next to the Docker development stack. Secrets are generated on the first run
and stored owner-only.

Everything lives under `~/.depictio/local`, or `DEPICTIO_LOCAL_HOME` if set:

| Path | Content |
|------|---------|
| `env/` | MongoDB, Redis and SeaweedFS binaries |
| `mongo/`, `redis/`, `s3/` | Service data, kept between runs |
| `logs/` | One log per service: `api.log`, `worker.log`, `mongo.log`, `redis.log`, `s3.log` |
| `cli/` | CLI configuration for this instance, to run `depictio-cli` against it |
| `secrets.json` | Generated S3 and admin passwords |

---

## :material-docker: Move to Docker Compose

A local server can be handed over to [Docker Compose](docker.md) with its
projects, dashboards and table data, for instance once a review turns into a
shared instance.

```bash
uv run --extra local depictio local down
uv run --extra local depictio local export-compose --out depictio-docker
cd depictio-docker
docker compose up -d
```

The dashboards are then on `http://localhost:5080`. `export-compose` copies the
MongoDB and SeaweedFS data and the signing keys into the directory, so the local
server stays usable and the two never share files. It also writes:

| File | Content |
|------|---------|
| `.env` | The local server's S3 and admin credentials |
| `docker-compose.override.yaml` | The same MongoDB and SeaweedFS versions as the local server, on the copied data |
| `docker-compose.yaml` | Copied from a clone of the repository; otherwise the command prints the `curl` to fetch it |

The token in `~/.depictio/local/cli` stays valid against the Docker stack, since
it was signed with the copied keys. The raw pipeline files are not copied, only
the tables built from them: to ingest again, use the Docker setup's own CLI
configuration, with the pipeline directories reachable from the containers.

---

## :material-monitor: Platforms

| Platform | Status |
|----------|--------|
| Linux x86_64 | Supported, tested in CI |
| Linux arm64 | Supported, tested in CI |
| macOS arm64 (Apple silicon) | Supported, tested in CI |
| macOS x86_64 (Intel) | Supported, not tested in CI |
| Windows | Not supported: use [WSL2](https://learn.microsoft.com/windows/wsl/) or [Docker Compose](docker.md) |

Only Python 3.12 is tested, hence `--python 3.12` in the commands.

On macOS the Celery worker runs in threads: a forked worker process that opens a
Delta table crashes there, because the libraries it loads are not safe to use
after `fork()`. Celery time limits and `max-tasks-per-child` do not apply to a
threads pool.

MongoDB 5 and later needs AVX on x86_64 and ARMv8.2-A on arm64, which rules out
some older machines such as the Raspberry Pi 4. `up` reports it when `mongod`
stops on an illegal instruction.

---

## :material-help-circle-outline: Troubleshooting

#### A service exited during startup

`up` stops the services it started and names the log to read, under
`~/.depictio/local/logs`.

#### SeaweedFS does not start

`weed mini` keeps its internal ports: 9333, 9340, 8888 and 23646, plus the same
ports + 10000 for gRPC. If one is taken, stop what holds it; the S3 port itself
is picked freely.

#### Dashboards stay blank

The viewer was not built before `up`. Build it (step 1), then run `depictio local down`
and `depictio local up` again.

#### Start from scratch

`depictio local wipe --yes` deletes every project, dashboard and file of the
local server. The next `up` seeds it again.

## Next Steps

- [Pipeline templates](../usage/projects/templates.md)
- [CLI usage](../depictio-cli/usage.md), with the configuration in `~/.depictio/local/cli`
- [Docker Compose](docker.md), to share an instance with a team
