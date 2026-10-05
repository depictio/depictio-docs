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
[Kubernetes](kubernetes.md). A local server can later be
[moved to Docker Compose](#move-to-docker-compose) with its data.

![The same server, run in containers or as local processes](../images/installation/local/schema_same_code_docs.png)

---

## :material-rocket-launch: Quick Start

**Prerequisites**: [uv](https://docs.astral.sh/uv/getting-started/installation/),
and until the `depictio` package is published on PyPI, [git](https://git-scm.com/),
[Node.js](https://nodejs.org/) and [pnpm](https://pnpm.io/installation) to build
the viewer from a clone.

### Step 1: Install

`depictio` is not on PyPI yet, so for now it is installed from a clone of the
repository, with the viewer built first:

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
pnpm install --frozen-lockfile
(cd depictio/viewer && pnpm run build)
uv tool install -e ".[local]"
```

`uv tool install` puts the `depictio` command on your `PATH`, in an environment
of its own that holds the server's Python dependencies (about 2 GB). No
`--python` flag is needed: the dependencies install from prebuilt wheels on
Python 3.11 to 3.14. The install is editable, so it runs the code and the viewer
build of the clone. Without the viewer build the API starts, but dashboards do
not render; `up` warns about it.

!!! info "Once `depictio` is published on PyPI"
    The package carries the viewer, so one command replaces the clone and the
    build:

    ```bash
    uv tool install "depictio[local]"
    ```

    Prefer it to `uvx --from "depictio[local]" depictio local up`: `uvx` runs the
    command in a temporary environment and leaves no `depictio` command behind
    for `depictio local status` and `depictio local down`.

### Step 2: Start the server

```bash
depictio local up
```

The first run downloads MongoDB, Redis and SeaweedFS from conda-forge into
`~/.depictio/local/env` (about 710 MB, once). The Iris and Penguins example
projects are seeded, and the browser opens on the dashboards page,
`http://127.0.0.1:8058/dashboards` unless that port was already taken (see
[How it differs from Docker](#how-it-differs-from-docker) for the ports). On a
first run, `up` waits a few seconds for the examples to load ("Loading the
examples") so their dashboards open with data, then ends with a summary:

```text
Depictio is ready: http://127.0.0.1:8058/dashboards
  Examples: iris, penguins
  Data: /home/you/.depictio/local (logs in /home/you/.depictio/local/logs)
  Add data: depictio local up --template <template> --data-root <dir>
  CLI on this server: export DEPICTIO_CLI_CONFIG_PATH=/home/you/.depictio/local/cli/admin_config.yaml
  Stop: depictio local down
```

The `export` line points the [CLI](../depictio-cli/usage.md) at this server for
the rest of the shell session.

Over SSH, or on Linux without a display, no browser is opened: `up` prints the
tunnel to run from your own machine, `ssh -L <port>:127.0.0.1:<port> <host>`,
then the URL to open there.

### Step 3: Open the dashboard of your own results

Pass a [template](../usage/projects/templates.md) and the pipeline output
directory:

```bash
depictio local up \
  --template nf-core/ampliseq/latest \
  --data-root path/to/results
```

`up` starts the services unless they are already running, then runs
`depictio run` against them with a CLI configuration it generates, and prints
the summary. With `--template`, no example project is seeded unless
`--examples` asks for one. Template variables go through `--var`, as with
[`depictio-cli run`](../depictio-cli/usage.md#run-command). nf-core results do
not contain the samplesheet: when the template cannot find it under `input/`,
pass it explicitly.

```bash
depictio local up \
  --template nf-core/rnaseq/latest \
  --data-root path/to/results \
  --var SAMPLESHEET_FILE=samplesheet.csv
```

If the ingestion fails, the command exits with an error and the server keeps
running.

---

## :material-console: Commands

| Command | Effect |
|---------|--------|
| `depictio local up` | Start the services, seed examples or ingest a template, print a summary, open the browser |
| `depictio local status` | Show each process with its port, whether the API answers, and the log directory |
| `depictio local down` | Stop every process; the data and the ports are kept for the next `up`. Says so when nothing is running |
| `depictio local wipe` | Stop the server and delete all local data. The downloaded binaries are kept. `--yes` skips the prompt |
| `depictio local export-compose` | Stop the server and copy its data into a directory that Docker Compose runs, see [Move to Docker Compose](#move-to-docker-compose) |

### `up` options

| Option | Default | Description |
|--------|---------|-------------|
| `--template` | | Template to ingest, e.g. `nf-core/rnaseq/latest`. Goes with `--data-root` |
| `--data-root` | | Pipeline results directory to ingest |
| `--project-name` | | Name of the ingested project |
| `--var KEY=VALUE` | | Template variable, repeatable. Relative paths are resolved from the current directory |
| `--examples` | `iris,penguins`, or `none` with `--template` | Example projects to seed: `iris`, `penguins`, `iris,penguins` or `none` |
| `--port` | the previous run's, else `8058` or a free one | Port of the API and the viewer, kept for later runs. A busy `--port` fails |
| `--open` / `--no-open` | `--open` | Open the dashboards page in a browser |
| `--screenshots` / `--no-screenshots` | off | Dashboard thumbnails through Playwright. Installs Chromium (about 150 MB) if needed |

Running `up` while the server is already up only ingests the new template.
`--port`, `--examples` and `--screenshots` apply when the server starts: a
warning names those it ignores, and running `depictio local down` first makes
them apply. Ctrl-C during startup stops what that run started, and the command
exits with code 130.

---

## :material-cog-outline: How it differs from Docker

Only configuration differs, and only through the usual `DEPICTIO_*` variables:
every service is pointed at `127.0.0.1`.

| | Docker Compose | Local server |
|---|---|---|
| MongoDB, Redis, S3 | containers | `mongod` 8.0.x, `redis-server` 8.x and `weed mini` 4.x from conda-forge, fetched by [py-rattler](https://github.com/conda/rattler) |
| API | 4 workers | 1 uvicorn worker |
| Celery worker | container | 2 slots: `prefork` on Linux, `threads` on macOS |
| Viewer | its own container | served by the API, on the same port |
| Authentication | single-user, multi-user or public | single-user |
| Dashboard thumbnails | on | off unless `--screenshots` |

The conda-forge packages are pinned to the major series of the Compose images
(the 8.0 series for MongoDB), so their minor versions can be newer than the
images'. [`export-compose`](#move-to-docker-compose) runs the exact MongoDB and
SeaweedFS versions of the local server, so the data never moves to an older one.

The first `up` picks its ports on `127.0.0.1`: the defaults (API `8058`, MongoDB
`27018`, Redis `6379`, S3 `9000`) when they are free, any free port otherwise, so
a local server runs next to the Docker development stack. The ports are saved
and reused by later runs, so the dashboards URL stays the same. A saved port
that another program has taken since moves to a free one, with a warning; a
`--port` that is busy fails instead. The CLI configuration follows the ports in
use.

Everything lives under `~/.depictio/local`, or `DEPICTIO_LOCAL_HOME` if set:

| Path | Content |
|------|---------|
| `env/` | MongoDB, Redis and SeaweedFS binaries |
| `mongo/`, `redis/`, `s3/` | Service data, kept between runs |
| `logs/` | One log per service: `api.log`, `worker.log`, `mongo.log`, `redis.log`, `s3.log` |
| `keys/` | Token signing keys |
| `cli/` | CLI configuration for this instance, with its admin token, to run `depictio-cli` against it |
| `secrets.json` | Generated S3 and admin passwords |
| `ports.json` | Ports kept for the next `up` |

The local home, `keys/` and `cli/` are owner-only (`0700`), and `secrets.json` is
created owner-only (`0600`).

!!! warning "Shared machines"
    The local server runs in single-user mode: no login, and whoever reaches its
    port acts as its admin. It listens on `127.0.0.1` only, but on a shared
    machine, such as an HPC login node, every other user of that machine can
    reach it, and the data it serves. The owner-only files do not change that.
    On such a machine, load only data that every user of it may see, or use
    [Docker Compose](docker.md) in multi-user mode.

---

## :material-docker: Move to Docker Compose

A local server can be handed over to [Docker Compose](docker.md) with its
projects, dashboards and table data, for instance once a review turns into a
shared instance.

```bash
depictio local export-compose --out depictio-docker
cd depictio-docker && docker compose up -d
```

`export-compose` stops the local server if it is running, so the copy is
consistent, then copies the MongoDB and SeaweedFS data and the token signing
keys into the directory (`depictio-docker` by default). The two never share
files: `depictio local up` restarts the local server on its own data. The
command ends by printing the one to run next, `cd <dir> && docker compose up -d`,
and the dashboards URL, `http://localhost:5080`.

The directory must be new or empty. Everything that can refuse the export (no
local data, a non-empty directory, no compose file to use) is checked before the
server is stopped. The directory holds:

| File | Content |
|------|---------|
| `docker-compose.yaml` | The compose file that matches the installed code: the clone's own file when `depictio` runs from a clone, otherwise the file of the release tag `v<version>`, downloaded from GitHub. A development or beta build outside a clone matches no published file, and the command stops with a message |
| `docker-compose.override.yaml` | The `mongo` and `chrislusf/seaweedfs` images at the versions the local server ran, on the copied data. On Linux they run as your user, who owns the copied files |
| `.env` | Single-user mode, the local server's S3 and admin credentials and, for a release, `DEPICTIO_VERSION`. Owner-only |
| `data/` | The copied MongoDB and SeaweedFS data, and the key files |

Redis is not carried over, since it holds only cache and queues, and thumbnails
are rendered again. The token in `~/.depictio/local/cli` stays valid against the
Docker stack, since it was signed with the copied keys. The raw pipeline files
are not copied, only the tables built from them: to ingest again, use the Docker
setup's own CLI configuration, with the pipeline directories reachable from the
containers.

---

## :material-monitor: Platforms

| Platform | Status |
|----------|--------|
| Linux x86_64 | Supported, tested in CI |
| Linux arm64 | Supported, tested in CI |
| macOS arm64 (Apple silicon) | Supported, tested in CI |
| macOS x86_64 (Intel) | Not supported: `cryptography`, a server dependency, ships macOS wheels for arm64 only. Use [Docker Compose](docker.md) |
| Windows | Not supported, `up` refuses to start: conda-forge has no `redis-server` for Windows, and the services are managed as POSIX process groups. Use [WSL2](https://learn.microsoft.com/windows/wsl/) or [Docker Compose](docker.md) |

Python 3.11 to 3.14 is supported: the dependencies install from prebuilt wheels
on each. CI runs the stack on Python 3.12, and it has also been run on 3.13 and
3.14.

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

#### A port is already in use

The API, MongoDB, Redis and S3 ports move to free ones by themselves (see
[How it differs from Docker](#how-it-differs-from-docker)); only an explicit
`--port` that is busy stops `up`. SeaweedFS (`weed mini`) also opens internal
ports (master, volume, filer, admin and their gRPC ports): `up` picks them the
same way, at their defaults (9333, 9340, 8888, 23646, and the same + 10000 for
gRPC) when they are free, so two local servers, or a local server and the Docker
development stack, run side by side.

#### On an HPC login node or behind a proxy

An HTTP proxy set in the environment does not break startup: the readiness
checks on `127.0.0.1` bypass `http_proxy` and the other proxy variables, and
SeaweedFS runs without them. The downloads do go through the proxy: MongoDB,
Redis and SeaweedFS from conda-forge on the first run, and the compose file of
`export-compose`. When one fails, a one-line error says so: check the network or
the proxy settings, then run the command again. Over SSH, open the server
through the `ssh -L` tunnel that `up` prints. The other users of a login node
can reach the server too: see the shared machines warning under
[How it differs from Docker](#how-it-differs-from-docker).

#### `DEPICTIO_*` settings are ignored

`up` does not pass the `DEPICTIO_*` variables of your shell to the server, since
they usually target another instance (`DEPICTIO_LOCAL_HOME` is read by
`depictio local` itself). The exception is `DEPICTIO_TELEMETRY_*`:
`DEPICTIO_TELEMETRY_ENABLED=false` (or `DO_NOT_TRACK=1`) turns
[telemetry](../features/telemetry.md) off for the local server too. Likewise,
`DEPICTIO_CLI_*` overrides, such as a token for another server, do not reach the
ingestion.

#### The example dashboards show no data

The examples load in the background on the first run. If the server was stopped
before they finished, they stay incomplete, and `up` then warns that they did
not finish loading. `depictio local wipe`, then `depictio local up`, loads them
again.

#### Dashboards stay blank

The viewer was not built before `up`, which only concerns an install from a
clone. Build it (step 1), then run `depictio local down` and `depictio local up`
again.

#### Start from scratch

`depictio local wipe --yes` deletes every project, dashboard and file of the
local server, with its passwords, keys and saved ports. The downloaded binaries
are kept. The next `up` seeds it again.

## Next Steps

- [Pipeline templates](../usage/projects/templates.md)
- [CLI usage](../depictio-cli/usage.md), after the `export DEPICTIO_CLI_CONFIG_PATH=...` line that `up` prints
- [Docker Compose](docker.md), to share an instance with a team
