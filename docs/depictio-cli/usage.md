---
title: Command reference
description: Every depictio command and option, from its --help.
---

# :material-book-open-variant: Command reference

Every command and option of `depictio` v1.21.0; `depictio <command> -h` prints the same. For step-by-step use, see [Common tasks](tasks.md).

## Overview { #quick-reference }

| Command | Does |
| --- | --- |
| [`local`](#local-commands) `up` · `open` · `status` · `down` · `wipe` · `export` | A server on this machine, without Docker |
| [`ingest`](#ingest-command) | Results in, project and dashboards out |
| [`watch`](#watch-command) | `ingest` again whenever files change |
| [`project-builder`](#project-builder) | Describe a folder no template fits, in the browser |
| [`config`](#config-commands) `show` · `check` · `sync` · `nextflow` | Setup checks, project sync, Nextflow hook |
| [`data`](#data-commands) `scan` · `process` · `join` · `push-images` · `versions` · `vacuum` | One ingestion step at a time; Delta history |
| [`dashboard`](#dashboard-commands) `validate` · `import` · `export` | Dashboards as YAML |
| [`template`](#template-commands) `export` · `compose` | A template from a project or a results folder |
| [`manifest`](#manifest-commands) `from-table` | A data manifest from a samplesheet |
| [`catalog`](#catalog-commands) `list` · `info` · `preview` · `gallery` | The tools catalog |
| [`backup`](#backup-commands) `create` · `list` · `validate` · `restore` | Database backups (admins) |
| [`migrate`](#migrate-commands) | A project to another instance (admins) |
| `commands` · `version` | Every command in one table; the version |

`depictio` alone prints a quick start. `depictio-cli` is the same command.

## Global options { #global-options }

They go before the command: `depictio -vv ingest results/`.

| Option | Meaning |
| --- | --- |
| `-v`, `--verbose` | Logs: `-v` INFO, `-vv` DEBUG |
| `--log-level LEVEL` | Logs from `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL` up |
| `-V`, `--version` | Print the version |
| `-h`, `--help` | Help of any command |
| `--install-completion`, `--show-completion` | Shell completion |

## Which server a command uses { #choosing-a-server }

Every command that talks to a server takes `--server`: `local` for the server [`local up`](#local-commands) runs, or a CLI configuration file. Without it, the command uses, in order:

1. `$DEPICTIO_CLI_CONFIG_PATH` (a file, or `local`);
2. `~/.depictio/CLI.yaml`, if it exists;
3. the local server, unless `DEPICTIO_CLI_TOKEN` or `DEPICTIO_CLI_API_BASE_URL` is set.

The rule never checks whether a local server runs. Each command first prints the server it reaches.

### Environment variables { #environment-variables }

| Variable | Effect |
| --- | --- |
| `DEPICTIO_CLI_CONFIG_PATH` | Configuration used without `--server` |
| `DEPICTIO_CLI_TOKEN` | Replaces the file's token |
| `DEPICTIO_CLI_API_BASE_URL` | Replaces the file's `api_base_url` |

The last two never apply to `--server local` or `migrate --to-server`.

## `ingest` { #ingest-command }

<span id="run-command"></span>

```bash
depictio ingest [OPTIONS] [DATA_DIR]
```

Checks the server and S3, validates the project (or resolves the template), syncs it, scans, processes the tables, runs the joins and imports the dashboards the project lacks. Without `--template` or `--project-config-path`, the template is detected from `DATA_DIR`; a local folder no template fits is [composed from the catalog](../usage/projects/composed-dashboards.md). Formerly `run`.

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `DATA_DIR` | path | | Results folder, or an `s3://` prefix |
| `--template` | text | detected | Template id (`nf-core/ampliseq/2.16.0`, `.../latest`) or folder |
| `--project-config-path` | path | | [Project YAML](minimal_config.md) instead of a template |
| `--project` | text | the template's | Project name, also to find it on a refresh |
| `--update-config` | flag | off | [Refresh](#refreshing-a-project) an existing project |
| `--attach-run` | flag | off | Add `DATA_DIR` to it as another run |
| `--reset-dashboards` | flag | off | Re-import the template's dashboards over edited ones |
| `--var KEY=VALUE` | text | | Template variable, repeatable |
| `--dry-run` | flag | off | Validate, list steps and matched files; write nothing |
| `--skip STEP` | text | | [Steps](#skipping-steps) to leave out |
| `--result-json FILE` | path | | Write the [outcome](#result-json) as JSON |

??? note "Sources, dashboards and scope"

    | Option | Type | Default | Meaning |
    | --- | --- | --- | --- |
    | `--manifest` | URL, path | | A [manifest](../usage/projects/remote-data.md#the-data-manifest-contract) in place of `DATA_DIR` |
    | `--bind TAG=LOCATION` | text | | One data collection's folder, glob, file, URL or `s3://` prefix. Repeatable |
    | `--compose` | flag | off | Compose even when a template fits |
    | `--include-unknown` | flag | off | Composing: add files the catalog does not know |
    | `--include GLOB` | text | | Composing: add the unknown files matching it |
    | `--provenance-file` | path | | Extra file for the run provenance. Repeatable |
    | `--drop-missing-runs` | flag | off | Refresh: drop attached runs missing here. Not with `--attach-run` |
    | `--dashboard` | path | | Dashboard YAML instead of the template's. Repeatable |
    | `--dashboard-name` | text | | Main dashboard title; renames it on a refresh |
    | `--workflow-name` | text | | Only this workflow |
    | `--data-collection-tag` | text | | Only this data collection |
    | `--continue-on-error` | flag | off | Go on past a failed step; still exits 1 |

??? note "Writing tables"

    | Option | Type | Default | Meaning |
    | --- | --- | --- | --- |
    | `--write-mode` | text | `overwrite` | Or `replace-runs`: rewrite only this batch's runs. See [Data versions](../features/versioning.md#how-new-data-versions-are-written) |
    | `--incremental-write` | flag | off | With `replace-runs`, only the runs that changed |
    | `--repartition` | flag | off | Let `replace-runs` partition an existing table |
    | `--per-run` | flag | off | Every recipe once per run, cross-sample ones too |
    | `--skip-unchanged` | flag | off | Leave tables whose files did not change |
    | `--sync-changed` | flag | off | Re-upload only changed files |

??? note "Automation, performance, debugging"

    | Option | Type | Default | Meaning |
    | --- | --- | --- | --- |
    | `--pipeline-id` | text | | `<name>/<version>` picking a template; the [Nextflow trigger](nextflow-trigger.md) passes it |
    | `--triggered-by` | text | `manual` | Shown in the [ingestion report](../features/dashboards.md#triggered-by) |
    | `--user` | text | | Create or get this user, ingest as them, print a login link |
    | `--provisioning-key` | text | `$DEPICTIO_AUTH_PROVISIONING_API_KEY` | Secret for `--user`, see [provisioning](../usage/guides/authentication-modes.md#pipeline-provisioning-and-magic-links-v113) |
    | `--streaming` | flag | off | Stream the Delta write. Experimental |
    | `--async-upsert` | flag | off | Profile tables [in the background](../installation/docker.md#async-upsert) |
    | `--concurrency` | int | `4` | Parallel HTTP requests |
    | `--upload-chunk-size` | int | `1000` | Files per upload request |
    | `--state-cache / --no-state-cache` | flag | on | Skip unchanged runs when rescanning |
    | `--preview-recipes` | flag | off | Show recipe inputs and outputs |
    | `--rich-tables` | flag | off | Detailed summary |

    Variables: `DEPICTIO_INGEST_STREAMING_WRITE` (as `--streaming`), `DEPICTIO_INGEST_DC_WORKERS` (collections in parallel, 1 to 4), `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` (`--async-upsert` wait, 3600).

### Skipping steps { #skipping-steps }

`--skip` takes `server-check`, `s3-check`, `sync`, `scan`, `process` (images too), `join` and `dashboards`, comma-separated or repeated. An unknown name is an error.

### Refreshing a project { #refreshing-a-project }

If the project exists, `ingest` changes nothing and exits 2. Say what you meant:

| Option | What happens |
| --- | --- |
| `--update-config` | Configuration updated, every run rescanned, tables rebuilt, dashboards kept as edited and missing template ones added. Creates an absent project, so scripts can always pass it |
| `--attach-run` | `DATA_DIR` added as another run, tables rebuilt, dashboards kept |
| `--reset-dashboards` | As `--update-config`, then the template's dashboards replace the edited ones, titles kept |

- Workflows and collections the project file does not name, such as ones added in the web UI, are kept.
- Dashboards are matched by the file they came from, not their title, and gain the template tabs they lack. Subtitle, icons and tab order edited in the viewer are reset.
- Runs of `DATA_DIR` and of attached folders are kept, others removed. An attached folder missing here stops the refresh (exit 1) unless `--drop-missing-runs`.

### Result file { #result-json }

`--result-json FILE` writes `status` (`success`, `partial` or `exists`), `project` (`name`, `id`, `url`), `dashboards` in import order with their `status` (`created`, `kept`, `replaced`), `template_id`, and `composed` (`template_dir`, `tabs`, `unrecognised`) for a composed template. A failed step writes no file.

### Exit codes { #exit-codes }

| Code | Meaning |
| --- | --- |
| `0` | Every step completed |
| `1` | A step failed (even under `--continue-on-error`), unusable configuration, attached run missing, or nothing to compose |
| `2` | Nothing done: no template found, project exists, `--attach-run` project absent, or usage error |

## `watch` { #watch-command }

```bash
depictio watch [OPTIONS] [DATA_DIR]
```

`ingest` on a loop. The first cycle refreshes as `--update-config`; later ones rewrite what moved. Cycles skip the server checks and dashboards, so `ingest` once first. Ctrl-C finishes the cycle, then exits. A lock under `~/.depictio/state/` (`DEPICTIO_CLI_STATE_DIR`) allows one watcher or ingestion per project. Watchers show in the [Watchers pane](../usage/administration/monitoring.md#watchers).

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `DATA_DIR`, `--template`, `--project-config-path`, `--project`, `--var` | | | As for `ingest` |
| `--mode` | text | `incremental` | Or `full`: re-upload everything each cycle |
| `--full-every` | int | | A full cycle every N |
| `--write-mode` | text | `overwrite` | Or `replace-runs` |
| `--incremental-write` | flag | off | With `replace-runs`, only changed runs |
| `--backend` | text | `auto` | `native`, `polling` or `both`; `auto` polls on network filesystems |
| `--interval` | float | `300` | Seconds between polls |
| `--debounce` | float | `30` | Seconds of quiet before a cycle |
| `--max-delay` | float | `300` | Ceiling on the debounce |
| `--settle` | float | `5` | Seconds a file must stay unchanged |
| `--drop-missing-runs` | flag | off | Drop attached runs missing here |
| `--concurrency` | int | `4` | Parallel HTTP requests |
| `--once` / `--max-runs N` | | | Stop after one or N cycles |
| `--dry-run` | flag | off | Report without writing |

File events need the `watch` extra; without it, it only polls. An `s3://` `DATA_DIR` is ingested once, then the watcher exits 1: refresh remote data [from the server](../usage/projects/remote-data.md#refreshing-the-data).

### Running a watcher as a service { #running-a-watcher-as-a-service }

The repository ships [`deploy/depictio-watch@.service`](https://github.com/depictio/depictio/blob/main/deploy/depictio-watch@.service), a systemd unit reading `/etc/depictio/<project>.env`, and [`deploy/docker-compose.watcher.yaml`](https://github.com/depictio/depictio/blob/main/deploy/docker-compose.watcher.yaml), configured from [`deploy/.env.example`](https://github.com/depictio/depictio/blob/main/deploy/.env.example). Both need `DEPICTIO_CLI_CONFIG` and `DEPICTIO_PROJECT_CONFIG` (Compose also `DEPICTIO_DATA_ROOT`); `DEPICTIO_WATCH_*` variables set the options.

```bash
sudo systemctl enable --now depictio-watch@myproject
docker compose -f deploy/docker-compose.watcher.yaml up -d
```

## `local` { #local-commands }

A complete server on this machine, without Docker. Guide: [Python package](../installation/local.md).

| Command | Options |
| --- | --- |
| `local up` | `--examples` (`iris,penguins`, `iris`, `penguins`, `none`), `--port` (the previous one, else 8058 or a free one), `--open / --no-open` (on), `--screenshots / --no-screenshots` (off), `--data-root-allow PATH` (repeatable) |
| `local open` · `status` · `down` | Open the viewer; show what runs; stop it |
| `local wipe` | Delete all local data. `--yes` skips the prompt |
| `local export` | `--out` (`depictio-docker`): a Docker Compose folder with the data |

## `project-builder` { #project-builder }

```bash
depictio project-builder [DIRECTORY]
```

Describe data collections in the browser for a folder no template fits; it writes a template bundle for `ingest --template`. Options: `--out` (`<dir>/.depictio/template`), `--host` (`127.0.0.1`), `--port` (`8129`), `--no-open`. Needs the `builder` or `local` extra. See [Project Builder](../usage/projects/guide.md#project-builder).

## `config` { #config-commands }

| Command | Options | Does |
| --- | --- | --- |
| `config show` | `--project-name` | Print the configuration in use, and that project |
| `config check` | `--project-config-path` | Check server and S3; validate the file if given |
| `config sync` | `--project-config-path`, `--update` | Register a project file; `--update` an existing one |

### `config nextflow` { #config-nextflow }

Prints the path of the Nextflow `onComplete` snippet; see [Nextflow trigger](nextflow-trigger.md). `--print` prints the snippet, `--install` / `--uninstall` turn it on or off for every pipeline here, and `--default-disabled` (with `--install`) makes it opt-in per run.

## `data` { #data-commands }

One ingestion step at a time, for the project file in `--project-config-path`.

### `data scan`

Registers the files each data collection matches.

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `--workflow-name`, `--data-collection-tag` | text | | Limit the scan |
| `--rescan-folders` | flag | off | Rescan every run |
| `--sync-files` / `--sync-changed` | flag | off | Re-upload every / only changed file |
| `--dry-run` | flag | off | Report without writing |
| `--state-cache / --no-state-cache` | flag | on | Skip unchanged runs |
| `--concurrency` | int | `4` | Parallel requests |
| `--upload-chunk-size` | int | `1000` | Files per request |
| `--legacy-scan-depth` | flag | off | Ignore `max_depth` and `ignore`. Deprecated |
| `--rich-tables` | flag | off | Detailed tables |

### `data process`

Builds the Delta tables from scanned files. Options: `--overwrite` (an existing workflow), `--write-mode`, `--repartition`, `--async-upsert`, `--preview-recipes`, `--rich-tables`, as for [`ingest`](#ingest-command).

### `data join`

Runs the project file's joins; for cross-table filtering, prefer [links](../features/cross-dc-filtering.md). Options: `-j`, `--join-name`, `-p`, `--preview` (no save), `--overwrite`, `--no-auto-process`, `--rich-tables`.

### `data push-images`

```bash
depictio data push-images SOURCE_DIRECTORY S3_DESTINATION
```

Uploads an image collection's files to its `s3_base_folder`, keeping the layout; `ingest` does it for `local_images_path`. Options: `-r / -R` recursive (on), `-e`, `--extensions .png,.jpg`, `-n`, `--dry-run`, `--overwrite`, `-c`, `--concurrency` (`8`).

### `data versions` { #data-versions }

```bash
depictio data versions DATA_COLLECTION_TAG [--limit 20] [--json]
```

A table's Delta commits with write mode, trigger, rows, files and runs: the [Dataset history](../features/versioning.md#dataset-history) in a terminal.

### `data vacuum` { #data-vacuum }

```bash
depictio data vacuum DATA_COLLECTION_TAG [--retention-hours 168] [--apply]
```

Deletes the Delta files no commit newer than the retention needs; without `--apply`, only reports. A [dashboard version](../features/versioning.md#data-versions) pinned to a vacuumed commit loses its data.

## `dashboard` { #dashboard-commands }

Format and workflow: [Dashboard YAML](../features/yaml-sync.md).

| Command | Options | Does |
| --- | --- | --- |
| `dashboard validate FILE` | `--offline` | Schema, then columns on the server if one is set |
| `dashboard import FILE` | `-p`, `--project ID`, `--overwrite`, `--dry-run`, `--offline` | Import; `--overwrite` replaces the same title |
| `dashboard export ID` | `-o`, `--output` (`dashboard.yaml`) | Write it to YAML |

## `template` { #template-commands }

### `template export` { #template-export }

```bash
depictio template export PROJECT_ID -t my-lab/rnaseq-qc/1
```

Writes the project and its dashboards to `<output-dir>/<template-id>/`, ready for `ingest --template`. See [Export a project as a template](../usage/projects/templates.md#export-a-project-as-a-template).

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `-t`, `--template-id` | text | required | Template id |
| `-o`, `--output-dir` | path | `.` | Where to write |
| `--version` | text | `1.0.0` | Template version |
| `--description` | text | | Description |
| `--data-dir` | text | recorded root | Prefix turned into `{DATA_ROOT}`; `""` for none |

### `template compose` { #template-compose }

```bash
depictio template compose DATA_ROOT [-o DIR]
```

Offline: writes the template `ingest` would [compose](../usage/projects/composed-dashboards.md#template-compose) and lists what it left out. Options: `-o`, `--output` (under `~/.depictio/composed/` or `DEPICTIO_COMPOSE_HOME`), `--include-unknown`, `--include GLOB`, `--project`, `--verbose`.

## `manifest` { #manifest-commands }

### `manifest from-table` { #manifest-from-table }

```bash
depictio manifest from-table TABLE --base-url s3://my-bucket/run42
```

Turns a wide samplesheet (CSV or TSV) into a [manifest](../usage/projects/remote-data.md#the-data-manifest-contract), each file column a `type`. Options: `-o`, `--out` (`manifest.json`; another extension writes CSV), `--id-col` and `--file-cols` (detected), `--run-col`, `--base-url` (prefix for relative paths, required for local ones).

## `catalog` { #catalog-commands }

`catalog list` lists tools and outputs, `catalog info TOOL_ID` details one tool, `catalog preview OUTPUT_ID` and `catalog gallery` show one output or all in the browser (`-o`, `--out FILE`, `--port`, `-t`, `--theme dark`, `--no-open`). Online: the [Tools catalog](../catalog/index.md).

<div class="asciinema-cast" data-cast="assets/casts/depictio-catalog.cast" data-poster="npt:0:25" data-idle-time-limit="2.5"></div>

## `backup` { #backup-commands }

Admins only. Guide: [Backup and restore](../usage/administration/backup.md).

| Command | Options |
| --- | --- |
| `backup create` | `--include-s3-data`, `--s3-backup-prefix` (`backup`), `--dry-run` |
| `backup list` | |
| `backup validate ID` | |
| `backup restore ID` | `--dry-run`, `--collections a,b`, `--force` (no prompt), `--allow-unverified` (no checksum), `--skip-validation` |

## `migrate` { #migrate-commands }

```bash
depictio migrate --project "My Project" --to-server ~/.depictio/CLI_remote.yaml --dry-run
```

Copies a project from `--server` to `--to-server` (`~/.depictio/CLI_remote.yaml`), deleting nothing. Admin on both. `--mode`: `all` (default), `metadata` (shared S3), `dashboard` or `files`. `--dry-run` previews, `--overwrite` replaces the project on the target. Guide: [Project migration](../usage/administration/migrate.md).

## Former names and maintainer commands { #recipe-commands }

??? note "Former names, still accepted"

    | Former | Now |
    | --- | --- |
    | `run` | `ingest` |
    | `images push` (and `images list-bucket`) | `data push-images` |
    | `local export-compose` | `local export` |
    | `--CLI-config-path`; `-c/--config`, `--api` | `--server` |
    | `--target-config` | `migrate --to-server` |
    | `--data-root` | `ingest DATA_DIR`; `template export --data-dir` |
    | `--project-name`, `--overwrite` (ingest) | `--project`, `--update-config` |
    | `--skip-server-check` and other `--skip-*` | `--skip STEP` |
    | `-vl/--verbose-level` | `--log-level` |

??? note "`depictio dev`: maintainer tools"

    Out of `--help`: `dev recipe list | info | run NAME -d DATA_DIR` to test a [recipe](../usage/projects/recipes.md), `dev catalog`, `dev link` and `dev backup check-coverage`.
