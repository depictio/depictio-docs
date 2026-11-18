# Command reference

Every command and option of `depictio` 1.22.0, generated from its `--help`; `depictio <command> -h` prints the same. `depictio` alone prints a quick start, and `depictio-cli` is the same command. For step-by-step use, see [Common tasks](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/index.md). Scripts and AI agents can read the same reference as JSON: [`cli-reference.json`](https://depictio.github.io/depictio-docs/latest/depictio-cli/cli-reference.json).

## Overview

- **[`local`](#local)**

  ______________________________________________________________________

  Run a complete Depictio server on this machine, without Docker.

  `up` `open` `down` `status` `wipe` `export`

- **[`ingest`](#ingest)**

  ______________________________________________________________________

  Ingest pipeline results into a Depictio server, from validation to dashboards. Formerly `run`.

- **[`watch`](#watch)**

  ______________________________________________________________________

  Ingest pipeline results, then again whenever they change: `ingest` on a loop.

- **[`config`](#config)**

  ______________________________________________________________________

  Check the CLI setup, sync project configurations, hook Depictio into Nextflow.

  `show` `nextflow` `check` `sync`

- **[`data`](#data)**

  ______________________________________________________________________

  Run one ingestion step at a time: scan files, process data collections, join tables, upload images.

  `scan` `process` `join` `push-images` `versions` `vacuum`

- **[`dashboard`](#dashboard)**

  ______________________________________________________________________

  Validate, import and export dashboard YAML files.

  `validate` `import` `export`

- **[`template`](#template)**

  ______________________________________________________________________

  Export a project and its dashboards as a template someone else can run on their data, or compose one from what the catalog recognises in a results directory.

  `export` `compose` `check`

- **[`project-builder`](#project-builder)**

  ______________________________________________________________________

  Define a project's data collections from a folder no template fits, in the browser.

- **[`manifest`](#manifest)**

  ______________________________________________________________________

  Write a data manifest from a samplesheet or any table.

  `from-table`

- **[`migrate`](#migrate)**

  ______________________________________________________________________

  Migrate a project from one Depictio instance to another (non-destructive).

- **[`backup`](#backup)**

  ______________________________________________________________________

  Create, list, validate and restore server database backups (admins only).

  `create` `list` `validate` `restore`

- **[`catalog`](#catalog)**

  ______________________________________________________________________

  Browse the supported tools and the dashboard components their outputs become.

  `list` `info` `preview` `gallery`

Also [`commands`](#commands) and [`version`](#version).

## Global options

They go before the command: `depictio -vv ingest results/`.

| Option                 | Type                                        | Default | Description                                                                                                           |
| ---------------------- | ------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| `--verbose` `-v`       | count                                       |         | Show logs: `-v` for INFO, `-vv` for DEBUG                                                                             |
| `--log-level`          | `DEBUG` `INFO` `WARNING` `ERROR` `CRITICAL` |         | Show logs from this level up (DEBUG, INFO, WARNING, ERROR, CRITICAL); no `-v` needed. Formerly `-vl/--verbose-level`. |
| `--version` `-V`       | flag                                        |         | Show the Depictio CLI version and exit                                                                                |
| `--install-completion` | flag                                        |         | Install completion for the current shell.                                                                             |
| `--show-completion`    | flag                                        |         | Show completion for the current shell, to copy it or customize the installation.                                      |

`-h` and `--help` show any command's help.

## Which server a command uses

Every command that talks to a server takes `--server`: `local` for the server [`local up`](#local-up) runs, or a CLI configuration file. Without it, the command uses, in order:

1. `$DEPICTIO_CLI_CONFIG_PATH` (a file, or `local`);
1. `~/.depictio/CLI.yaml`, if it exists;
1. the local server, unless `DEPICTIO_CLI_TOKEN` or `DEPICTIO_CLI_API_BASE_URL` is set.

The rule never checks whether a local server runs. Each command first prints the server it reaches.

### Environment variables

| Variable                    | Effect                                |
| --------------------------- | ------------------------------------- |
| `DEPICTIO_CLI_CONFIG_PATH`  | Configuration used without `--server` |
| `DEPICTIO_CLI_TOKEN`        | Replaces the file's token             |
| `DEPICTIO_CLI_API_BASE_URL` | Replaces the file's `api_base_url`    |

The last two never apply to `--server local` or `migrate --to-server`.

## `local`

Run a complete Depictio server on this machine, without Docker.

[Python package](https://depictio.github.io/depictio-docs/latest/installation/local/index.md)

### `local up`

```
depictio local up [OPTIONS]
```

Start MongoDB, Redis, SeaweedFS, the API and the worker on this machine.

Run from a source checkout, it first builds the viewer when its sources changed since the last build (this needs pnpm).

Then add data with: `depictio ingest <results dir> --server local`

| Option                               | Type            | Default | Description                                                                                    |
| ------------------------------------ | --------------- | ------- | ---------------------------------------------------------------------------------------------- |
| `--examples`                         | text            |         | Example projects to seed on the first run: iris,penguins (the default), iris, penguins or none |
| `--port`                             | integer         |         | API/viewer port, kept for later runs (default: the previous one, else 8058 or a free one)      |
| `--open` / `--no-open`               | flag            | on      | Open the dashboards page in a browser                                                          |
| `--screenshots` / `--no-screenshots` | flag            | off     | Dashboard thumbnails via Playwright; installs Chromium (~150 MB) if needed. Off by default.    |
| `--data-root-allow`                  | path repeatable |         | Also let the web UI read run folders under PATH. Your home folder is always allowed.           |

### `local open`

```
depictio local open
```

Open the dashboards page of the running local server in a browser.

### `local down`

```
depictio local down
```

Stop every process started by `depictio local up`.

### `local status`

```
depictio local status
```

Show which local processes are running and whether the API answers.

Exits with 0 when every process runs and the API answers, 1 otherwise.

### `local wipe`

```
depictio local wipe [OPTIONS]
```

Stop the server and delete all local data (downloaded binaries are kept).

| Option  | Type | Default | Description                 |
| ------- | ---- | ------- | --------------------------- |
| `--yes` | flag |         | Do not ask for confirmation |

### `local export`

```
depictio local export [OPTIONS]
```

Also `depictio local export-compose`, its former name.

Copy the local server's data into a directory Docker Compose runs as is.

A running local server is stopped first, so the copy is consistent. Formerly `export-compose`.

| Option  | Type | Default           | Description                                      |
| ------- | ---- | ----------------- | ------------------------------------------------ |
| `--out` | path | `depictio-docker` | Directory to create for the Docker Compose stack |

## `ingest`

```
depictio ingest [OPTIONS] [DATA_DIR]
```

Also `depictio run`, its former name.

Ingest pipeline results into a Depictio server, from validation to dashboards. Formerly `run`.

Runs these steps in order:

1. Check that the server answers
1. Check the S3 storage configuration
1. Validate the project configuration (or resolve the template)
1. Sync the project configuration to the server
1. Scan the data files
1. Process the data collections, uploading images where local_images_path is set
1. Run the table joins the project configuration defines
1. Import the dashboards the project lacks (from the template, or from `--dashboard`)

Example, the template detected from the results directory:

```
depictio ingest results/
```

Refreshed after a new run, the dashboards kept as edited in the viewer:

```
depictio ingest results/ --update-config
```

A manifest-driven template, the files listed in a manifest instead of a directory:

```
depictio ingest --template generic/manifest-tables/1 --manifest https://data.example.org/run42/manifest.json
```

| Option                  | Type            | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                          |
| ----------------------- | --------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATA_DIR`              | text            |         | Directory of the pipeline results to ingest, or an s3:// prefix holding them (e.g. `s3://my-bucket/pipeline/run42`). Without `--template` or `--project-config-path`, the template is detected from it. Formerly `--data-root`.                                                                                                                                                                                      |
| `--server`              | text            |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server).                                                                                                                                                                                                                                                                                    |
| `--template`            | text            |         | Template to build the project from, e.g. nf-core/ampliseq/2.16.0, or nf-core/ampliseq/latest for the newest shipped version. Default: detected from DATA_DIR, else composed from the catalog. Not with `--project-config-path`.                                                                                                                                                                                      |
| `--project-config-path` | text            |         | Project YAML, for a pipeline Depictio ships no template for. Not with `--template`.                                                                                                                                                                                                                                                                                                                                  |
| `--update-config`       | flag            |         | Refresh a project that exists: its configuration, and its tables with every run rescanned. Its runs become those of DATA_DIR (or of the project file's locations) and those added with `--attach-run`; the runs of any other location are removed. Its dashboards are kept as they are, edits made in the viewer included; the template's dashboards it lacks are added. A project not on the server yet is created. |
| `--var`                 | text repeatable |         | Extra template variable as KEY=VALUE. Repeatable. Example: `--var SAMPLESHEET_FILE=/path/to/samplesheet.csv` `--var METADATA_FILE=/path/to/metadata.tsv`                                                                                                                                                                                                                                                             |
| `--dry-run`             | flag            |         | Validate the project configuration locally and list the steps that would run, without contacting the server                                                                                                                                                                                                                                                                                                          |

**Project and runs**

| Option                | Type            | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------------- | --------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--manifest`          | text            |         | A data manifest, as an https:// URL or a local file, listing the files to ingest as {id, type, url[, run]} entries. In place of DATA_DIR, for a manifest-driven template such as generic/manifest-tables/1 (it sets the template's MANIFEST_URL variable).                                                                                                                                                                        |
| `--project`           | text            |         | Project name. Replaces the name the template gives, or the `name` in the `--project-config-path` file. `--attach-run` and `--update-config` find the project by it. Formerly `--project-name`.                                                                                                                                                                                                                                    |
| `--attach-run`        | flag            |         | Add DATA_DIR to an EXISTING project as one more run, instead of creating a project. The run is recorded as attached, so a later `--update-config` keeps it. The project is found by `--project`, else by the template's own name. Implies `--update-config`, dashboards included. Only the new run's rows are written; a recipe that mixes samples (distances, ordinations, top-N) is recomputed over every run, see `--per-run`. |
| `--drop-missing-runs` | flag            |         | On a refresh, remove the runs of a location added with `--attach-run` that is not on this host. Without it, such a refresh stops before changing anything.                                                                                                                                                                                                                                                                        |
| `--provenance-file`   | text repeatable |         | Extra provenance/recap file (json, yaml, or 2-column tsv of key/value) whose entries are listed in the project's run-provenance report under 'User provided'. Repeatable.                                                                                                                                                                                                                                                         |
| `--bind`              | text repeatable |         | Point one data collection at where its data actually is, as TAG=LOCATION. Repeatable. The scan mode is inferred from the location: a local directory or glob scans locally, a local file is a single file, https:// is a remote file, an s3:// prefix or glob is listed remotely. Example: `--bind` samples=`s3://my-bucket/run42/*.samples.csv`                                                                                  |
| `--compose`           | flag            |         | Compose the template from what the catalog recognises in DATA_DIR, even when a bundled template fits. Without it, composing is the fallback when none does.                                                                                                                                                                                                                                                                       |
| `--include-unknown`   | flag            |         | When composing: also ingest the tabular files the catalog does not recognise, in an 'Other data' tab.                                                                                                                                                                                                                                                                                                                             |
| `--include`           | glob repeatable |         | When composing: ingest the unrecognised files matching this glob, relative to DATA_DIR (e.g. `stats/*.tsv`). Repeatable.                                                                                                                                                                                                                                                                                                          |

**Dashboards**

| Option               | Type            | Default | Description                                                                                                                                                                                                                                                                                          |
| -------------------- | --------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--dashboard`        | text repeatable |         | Dashboard YAML file to import instead of the template's own. Repeatable.                                                                                                                                                                                                                             |
| `--dashboard-name`   | text            |         | Title of the main dashboard. Without it, a new dashboard takes the title in its YAML and a refresh keeps the current one, even if renamed in the viewer. With it, a refresh renames the existing main dashboard and leaves its contents as they are. Child tabs keep their titles and stay attached. |
| `--reset-dashboards` | flag            |         | Import the template's dashboards (or `--dashboard`'s) over the ones the project has: the layout and components edited in the viewer are lost, the titles are kept. Implies `--update-config`, as only a project that exists has dashboards to reset.                                                 |

**Scope and steps**

| Option                  | Type            | Default     | Description                                                                                                                                                                                                                                    |
| ----------------------- | --------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--workflow-name`       | text            |             | Scan and process only this workflow (its tag)                                                                                                                                                                                                  |
| `--data-collection-tag` | text            |             | Scan and process only this data collection                                                                                                                                                                                                     |
| `--skip`                | step repeatable |             | Steps to skip, comma-separated or repeated: server-check, s3-check, sync, scan, process, join, dashboards. Skipping process skips the image upload too. Formerly the `--skip-<step>` flags.                                                    |
| `--continue-on-error`   | flag            |             | Continue execution even if a step fails                                                                                                                                                                                                        |
| `--sync-changed`        | flag            |             | Re-upload only the files whose size or modification time moved since the last scan. Narrower than `--update-config`, which re-uploads every file.                                                                                              |
| `--write-mode`          | text            | `overwrite` | How step 6 writes a table. overwrite: rewrite it whole. replace-runs: partition it by run and rewrite only the runs in this batch, leaving the others untouched.                                                                               |
| `--incremental-write`   | flag            |             | With `--write-mode` replace-runs, rewrite only the runs that changed instead of rebuilding the whole table. Falls back to a full rebuild whenever that cannot be done safely (run removed, table not partitioned by run, column type changed). |
| `--per-run`             | flag            |             | Compute every recipe once per run, including those that mix samples (distances, ordinations, top-N cuts), which are otherwise recomputed over all the project's runs at once. Their per-run outputs are then stacked.                          |
| `--skip-unchanged`      | flag            |             | Leave a data collection's table untouched when the scan found no new, changed or removed file for it. Off by default, so that ingesting again always rebuilds a project that drifted.                                                          |
| `--repartition`         | flag            |             | Let `--write-mode` replace-runs partition by run a table that is not yet. This rewrites every row, so it is never done implicitly, and never by the watcher.                                                                                   |

**Automation**

| Option               | Type | Default  | Description                                                                                                                                                                                                                                                                                                   |
| -------------------- | ---- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--pipeline-id`      | text |          | The pipeline that produced the data, as `<name>/<version>` (e.g. `nf-core/ampliseq/2.16.0`). Without `--template` or `--project-config-path`, the bundled template that matches it is used; otherwise it is ignored. Pipeline triggers fill it in, from a Nextflow pipeline's workflow.manifest for instance. |
| `--triggered-by`     | text | `manual` | What invoked this ingestion, recorded on the project and shown in its ingestion report. Defaults to `manual`; a pipeline's completion trigger passes its engine (e.g. `nextflow`) so an automated project is distinguishable from one someone ingested by hand.                                               |
| `--user`             | text |          | Provision (create-or-get) this user's account and run the pipeline as them, then emit a passwordless login link to their dashboard. Requires `--provisioning-key`.                                                                                                                                            |
| `--provisioning-key` | text |          | Shared provisioning secret used with `--user` (or set DEPICTIO_AUTH_PROVISIONING_API_KEY). env `DEPICTIO_AUTH_PROVISIONING_API_KEY`                                                                                                                                                                           |
| `--result-json`      | file |          | Write how the ingestion ended (status, project and dashboard ids and links) to this file as JSON, for scripts.                                                                                                                                                                                                |

**Performance and debugging**

| Option                               | Type    | Default | Description                                                                                                                                                                                              |
| ------------------------------------ | ------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--streaming`                        | flag    |         | Stream the Delta write instead of materialising the whole table in memory (lower peak RSS on large ingests). Experimental; falls back to the standard write on any failure.                              |
| `--concurrency`                      | integer | `4`     | Parallel HTTP requests for file uploads and cleanup deletes                                                                                                                                              |
| `--upload-chunk-size`                | integer | `1000`  | Files per /files/upsert_batch request                                                                                                                                                                    |
| `--state-cache` / `--no-state-cache` | flag    | on      | Skip the runs whose file tree is unchanged since the last successful scan, from a local cache. Only applies when rescanning.                                                                             |
| `--async-upsert`                     | flag    |         | Ask the server to profile each written table in the background, and poll until it finishes, instead of holding one long request open. A server without offloading enabled ignores it and answers inline. |
| `--preview-recipes`                  | flag    |         | Show recipe input sources and transformed output before writing to Delta Lake                                                                                                                            |
| `--rich-tables`                      | flag    |         | Show detailed summary of the workflow execution                                                                                                                                                          |

[Common tasks](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#ingest-results) · [Composed dashboards](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md)

Variables: `DEPICTIO_INGEST_STREAMING_WRITE` (as `--streaming`), `DEPICTIO_INGEST_DC_WORKERS` (collections in parallel, 1 to 4), `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` (`--async-upsert` wait, 3600).

### Refreshing a project

If the project exists, `ingest` changes nothing and exits 2. Say what you meant:

| Option               | What happens                                                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--update-config`    | Configuration updated, every run rescanned, tables rebuilt, dashboards kept as edited and missing template ones added. Creates an absent project, so scripts can always pass it |
| `--attach-run`       | `DATA_DIR` added as another run, tables rebuilt, dashboards kept                                                                                                                |
| `--reset-dashboards` | As `--update-config`, then the template's dashboards replace the edited ones, titles kept                                                                                       |

- Workflows and collections the project file does not name, such as ones added in the web UI, are kept.
- Dashboards are matched by the file they came from, not their title, and gain the template tabs they lack. Subtitle, icons and tab order edited in the viewer are reset.
- Runs of `DATA_DIR` and of attached folders are kept, others removed. An attached folder missing here stops the refresh (exit 1) unless `--drop-missing-runs`.

### Result file

`--result-json FILE` writes `status` (`success`, `partial` or `exists`), `project` (`name`, `id`, `url`), `dashboards` in import order with their `status` (`created`, `kept`, `replaced`), `template_id`, and `composed` (`template_dir`, `tabs`, `unrecognised`) for a composed template. A failed step writes no file.

### Exit codes

| Code | Meaning                                                                                                               |
| ---- | --------------------------------------------------------------------------------------------------------------------- |
| `0`  | Every step completed                                                                                                  |
| `1`  | A step failed (even under `--continue-on-error`), unusable configuration, attached run missing, or nothing to compose |
| `2`  | Nothing done: no template found, project exists, `--attach-run` project absent, or usage error                        |

## `watch`

```
depictio watch [OPTIONS] [DATA_DIR]
```

Ingest pipeline results, then again whenever they change: `ingest` on a loop.

The first cycle runs at once and refreshes the project as `ingest --update-config` does; the later ones rescan and rewrite what moved. Runs until interrupted: SIGINT or SIGTERM finish the cycle in progress and then exit cleanly, so it is safe to run under systemd or as a container command.

One watcher or ingestion per project at a time: the first cycle takes the project's lock before it writes anything, and the watch holds it until it exits. A second one stops at once and names the lock file.

Example, rewriting only the runs that changed:

```
depictio watch results/ --write-mode replace-runs --incremental-write
```

| Option                  | Type            | Default       | Description                                                                                                                                                                                     |
| ----------------------- | --------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATA_DIR`              | text            |               | Directory of the pipeline results to watch. Without `--template` or `--project-config-path`, the template is detected from it, as `ingest` does.                                                |
| `--server`              | text            |               | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server).                                                               |
| `--template`            | text            |               | Template to build the project from, as for `ingest`. Default: detected from DATA_DIR. Not with `--project-config-path`.                                                                         |
| `--project-config-path` | text            |               | Project YAML, for a pipeline Depictio ships no template for. Not with `--template`.                                                                                                             |
| `--project`             | text            |               | Project name. Replaces the name the template gives, or the `name` in the `--project-config-path` file.                                                                                          |
| `--var`                 | text repeatable |               | Extra template variable as KEY=VALUE. Repeatable.                                                                                                                                               |
| `--mode`                | text            | `incremental` | incremental: re-upload only the files that changed. full: re-upload and rewrite everything on every cycle.                                                                                      |
| `--backend`             | text            | `auto`        | auto (detect), native (filesystem events only), polling (periodic re-walk), or both. auto selects polling on network filesystems, where native events do not see writes made from another host. |
| `--debounce`            | number          | `30`          | Seconds of quiet before a cycle is triggered                                                                                                                                                    |
| `--settle`              | number          | `5`           | Seconds a file must hold the same size and mtime before it is ingested                                                                                                                          |
| `--interval`            | number          | `300`         | Seconds between polling walks (also the backstop for lost events)                                                                                                                               |
| `--max-delay`           | number          | `300`         | Ceiling on debouncing, so a tree written continuously still gets ingested                                                                                                                       |
| `--full-every`          | integer         |               | Run a full cycle every N incremental ones                                                                                                                                                       |
| `--once`                | flag            |               | Run a single cycle and exit with its status                                                                                                                                                     |
| `--max-runs`            | integer         |               | Stop after this many cycles, the first included                                                                                                                                                 |
| `--write-mode`          | text            | `overwrite`   | How each cycle writes a table, as for `ingest`: overwrite or replace-runs                                                                                                                       |
| `--incremental-write`   | flag            |               | With `--write-mode` replace-runs, rewrite only the runs that changed instead of rebuilding the whole table.                                                                                     |
| `--drop-missing-runs`   | flag            |               | Remove the runs of a location added with `ingest --attach-run` that is not on this host. Without it, such a project stops the first cycle.                                                      |
| `--concurrency`         | integer         | `4`           | Parallel HTTP requests during each cycle                                                                                                                                                        |
| `--dry-run`             | flag            |               | Report each cycle's changes without writing to the server                                                                                                                                       |

[Watch a folder](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#watch-a-folder) · [Watchers pane](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/#watchers)

A lock under `~/.depictio/state/` (`DEPICTIO_CLI_STATE_DIR`) allows one watcher or ingestion per project. Watchers show in the [Watchers pane](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/#watchers). File events need the `watch` extra; without it, it only polls. An `s3://` `DATA_DIR` is ingested once, then the watcher exits 1: refresh remote data [from the server](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#refreshing-the-data).

### Running a watcher as a service

The repository ships [`deploy/depictio-watch@.service`](https://github.com/depictio/depictio/blob/main/deploy/depictio-watch@.service), a systemd unit reading `/etc/depictio/<project>.env`, and [`deploy/docker-compose.watcher.yaml`](https://github.com/depictio/depictio/blob/main/deploy/docker-compose.watcher.yaml), configured from [`deploy/.env.example`](https://github.com/depictio/depictio/blob/main/deploy/.env.example). Both need `DEPICTIO_CLI_CONFIG` and `DEPICTIO_PROJECT_CONFIG` (Compose also `DEPICTIO_DATA_ROOT`); `DEPICTIO_WATCH_*` variables set the options.

```
sudo systemctl enable --now depictio-watch@myproject
docker compose -f deploy/docker-compose.watcher.yaml up -d
```

## `config`

Check the CLI setup, sync project configurations, hook Depictio into Nextflow.

[Install and configure](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md)

### `config show`

```
depictio config show [OPTIONS]
```

Show the current Depictio CLI configuration.

With `--project-name`, additionally fetch and print that project's metadata as registered on the server.

| Option           | Type | Default | Description                                                                                                                       |
| ---------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server`       | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-name` | text |         | Also show this project's metadata as registered on the server                                                                     |

### `config nextflow`

```
depictio config nextflow [OPTIONS]
```

Print the path of the bundled Nextflow onComplete snippet.

Meant to be substituted straight into a Nextflow command, which is the whole reason it exists: the snippet lives inside the installed package, and that is not a path anyone should have to type or keep in sync.

```
nextflow run nf-core/ampliseq --outdir results -c $(depictio config nextflow)
```

For an nf-core pipeline that is the entire setup. The snippet reads the pipeline's own manifest and hands it to the CLI as `--pipeline-id`, which resolves the bundled template, so there is nothing else to configure.

Use `--print` to read the snippet, or to copy it somewhere you can edit:

```
depictio config nextflow --print > depictio.config
```

Use `--install` to stop repeating the `-c`, once per machine:

```
depictio config nextflow --install
```

Every later `nextflow run` then triggers Depictio with no extra flag, and `--uninstall` reverses it. Add `--default-disabled` to install it opt-in instead: pipelines then need `--depictio_enabled true` to trigger. Either way, `--depictio_enabled true/false` on a given `nextflow run` always wins.

| Option                                     | Type | Default | Description                                                                                                         |
| ------------------------------------------ | ---- | ------- | ------------------------------------------------------------------------------------------------------------------- |
| `--print`                                  | flag |         | Write the snippet's contents to stdout instead of its path.                                                         |
| `--install`                                | flag |         | Enable the trigger for every pipeline on this machine, once.                                                        |
| `--uninstall`                              | flag |         | Undo `--install`, leaving any other Nextflow settings alone.                                                        |
| `--default-enabled` / `--default-disabled` | flag | on      | With `--install`: whether a pipeline that sets no `--depictio_enabled` triggers Depictio (default) or stays opt-in. |

[Nextflow trigger](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/trigger/index.md)

### `config check`

```
depictio config check [OPTIONS]
```

Run Depictio preflight checks.

Without `--project-config-path`: verify server accessibility and S3 storage (the environment the CLI talks to).

With `--project-config-path`: validate that project configuration (this also exercises the S3 storage check it depends on).

| Option                  | Type | Default | Description                                                                                                                       |
| ----------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server`              | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-config-path` | text |         | Path to the pipeline configuration file                                                                                           |

### `config sync`

```
depictio config sync [OPTIONS]
```

Validate the Depictio project configuration and sync it to the server.

| Option                  | Type | Default | Description                                                                                                                       |
| ----------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server`              | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-config-path` | text |         | Path to the pipeline configuration file                                                                                           |
| `--update`              | flag |         | Update the project configuration on the server                                                                                    |

## `data`

Run one ingestion step at a time: scan files, process data collections, join tables, upload images.

[Data versions](https://depictio.github.io/depictio-docs/latest/features/versioning/index.md)

### `data scan`

```
depictio data scan [OPTIONS]
```

Scan the project's data folders for the files its data collections match.

Registers what it finds on the server; `depictio data process` then turns those files into tables. The project configuration must already be synced.

| Option                               | Type    | Default | Description                                                                                                                               |
| ------------------------------------ | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `--server`                           | text    |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server).         |
| `--project-config-path`              | text    |         | Project configuration file (YAML)                                                                                                         |
| `--workflow-name`                    | text    |         | Name of the workflow to be scanned                                                                                                        |
| `--data-collection-tag`              | text    |         | Data collection tag to be scanned                                                                                                         |
| `--rescan-folders`                   | flag    |         | Reprocess all runs for the data collection                                                                                                |
| `--sync-files`                       | flag    |         | Update files for the data collection                                                                                                      |
| `--sync-changed`                     | flag    |         | Re-upload only files whose metadata hash moved since the last scan. Narrower than `--sync-files`, which re-uploads every registered file. |
| `--legacy-scan-depth`                | flag    |         | Ignore each data collection's scan max_depth/ignore, as releases before 1.2.2 did. Deprecated escape hatch; will be removed.              |
| `--dry-run`                          | flag    |         | Report what would be registered or removed without writing to the server                                                                  |
| `--state-cache` / `--no-state-cache` | flag    | on      | Use the local scan-state cache to skip runs whose file tree is unchanged since the last successful scan. Only applies when rescanning.    |
| `--concurrency`                      | integer | `4`     | Parallel HTTP requests for file uploads and cleanup deletes                                                                               |
| `--upload-chunk-size`                | integer | `1000`  | Files per /files/upsert_batch request                                                                                                     |
| `--rich-tables`                      | flag    |         | Display rich tables in the output                                                                                                         |

### `data process`

```
depictio data process [OPTIONS]
```

Build each data collection's Delta table from the files `depictio data scan` found.

| Option                  | Type | Default     | Description                                                                                                                                                                                                                              |
| ----------------------- | ---- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--server`              | text |             | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server).                                                                                                        |
| `--project-config-path` | text |             | Project configuration file (YAML)                                                                                                                                                                                                        |
| `--overwrite`           | flag |             | Overwrite the workflow if it already exists                                                                                                                                                                                              |
| `--rich-tables`         | flag |             | Display rich tables in the output                                                                                                                                                                                                        |
| `--write-mode`          | text | `overwrite` | overwrite: rewrite the whole table (historical behaviour). replace-runs: partition by run and rewrite only the runs present in this batch, leaving the others untouched.                                                                 |
| `--preview-recipes`     | flag |             | Show recipe input sources and transformed output without writing to Delta Lake                                                                                                                                                           |
| `--repartition`         | flag |             | Allow `--write-mode` replace-runs to adopt run partitioning on a table that does not have it yet. This rewrites every row, so it is never done implicitly, and never by the watcher.                                                     |
| `--async-upsert`        | flag |             | Ask the server to profile the written table in the background and poll until it finishes, instead of holding one long HTTP request open. Ignored by servers without offloading enabled: the upsert then just completes inline as before. |

### `data join`

```
depictio data join [OPTIONS]
```

Execute table joins defined in the project configuration.

This command processes the top-level `joins` configuration in your project YAML, joining data collections on the client side and optionally persisting the results as Delta tables.

Examples:

```
# Preview all joins without persisting
depictio data join --project-config-path project.yaml --preview

# Execute a specific join
depictio data join --project-config-path project.yaml --join-name my_join

# Execute all joins and overwrite existing
depictio data join --project-config-path project.yaml --overwrite
```

| Option                  | Type | Default | Description                                                                                                                       |
| ----------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server`              | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-config-path` | text |         | Project configuration file (YAML)                                                                                                 |
| `--join-name` `-j`      | text |         | Name of a specific join to process (processes all if not specified)                                                               |
| `--preview` `-p`        | flag |         | Preview join results without persisting                                                                                           |
| `--overwrite`           | flag |         | Overwrite existing joined tables                                                                                                  |
| `--no-auto-process`     | flag |         | Don't auto-process missing source data collections                                                                                |
| `--rich-tables`         | flag |         | Display rich tables in the output                                                                                                 |

[Cross-DC filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md)

### `data push-images`

```
depictio data push-images [OPTIONS] SOURCE_DIRECTORY S3_DESTINATION
```

Also `depictio images push`, its former name.

Upload a directory of images to S3 storage, for an image data collection. Formerly `images push`.

The directory structure is kept, relative to the source directory, and images already in storage are skipped unless `--overwrite`. Upload to the collection's s3_base_folder: its image_column paths are relative to it. `depictio ingest` does this itself for a collection that sets local_images_path.

Examples:

```
# Push all images to S3
depictio data push-images ./data/images s3://my-bucket/project/images/

# Dry run to see what would be uploaded
depictio data push-images ./data/images s3://my-bucket/images/ --dry-run

# Push only specific extensions
depictio data push-images ./data/images s3://my-bucket/images/ --extensions ".png,.jpg"
```

| Option                                     | Type    | Default | Description                                                                                                                       |
| ------------------------------------------ | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `SOURCE_DIRECTORY` required                | text    |         | Source directory containing images                                                                                                |
| `S3_DESTINATION` required                  | text    |         | S3 destination path (e.g., `s3://bucket/path/to/images/`)                                                                         |
| `--recursive` `-r` / `--no-recursive` `-R` | flag    | on      | Include subdirectories                                                                                                            |
| `--extensions` `-e`                        | text    |         | Comma-separated list of extensions to upload (e.g., `.png,.jpg`)                                                                  |
| `--dry-run` `-n`                           | flag    |         | Show what would be uploaded without actually uploading                                                                            |
| `--overwrite`                              | flag    |         | Overwrite existing files in S3                                                                                                    |
| `--concurrency` `-c`                       | integer | `8`     | Number of parallel uploads                                                                                                        |
| `--server`                                 | text    |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |

### `data versions`

```
depictio data versions [OPTIONS] DATA_COLLECTION_TAG
```

List the Delta Lake commit history of a data collection.

Every ingestion has always produced a new Delta version; this surfaces the history that was already there, along with depictio's own commit metadata (which run wrote it, what triggered it, which write mode was used).

| Option                         | Type    | Default | Description                                                                                                                       |
| ------------------------------ | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `DATA_COLLECTION_TAG` required | text    |         | Data collection whose Delta history to list                                                                                       |
| `--server`                     | text    |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-config-path`        | text    |         | Project configuration file (YAML)                                                                                                 |
| `--limit`                      | integer | `20`    | Number of commits to show                                                                                                         |
| `--json`                       | flag    |         | Emit machine-readable JSON                                                                                                        |

[Dataset history](https://depictio.github.io/depictio-docs/latest/features/versioning/#dataset-history)

### `data vacuum`

```
depictio data vacuum [OPTIONS] DATA_COLLECTION_TAG
```

Remove Delta files no longer referenced by any retained version.

Nothing in depictio has ever vacuumed, so every re-ingestion has left its predecessor's files behind and a data collection's physical footprint grows without bound. A watcher accelerates that considerably.

Deliberately dry-run by default and never wired into an ingestion path: vacuuming below the retention window pulls files out from under an API worker that is part-way through reading the table.

| Option                         | Type    | Default | Description                                                                                                                       |
| ------------------------------ | ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `DATA_COLLECTION_TAG` required | text    |         | Data collection whose stale Delta files to remove                                                                                 |
| `--server`                     | text    |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project-config-path`        | text    |         | Project configuration file (YAML)                                                                                                 |
| `--retention-hours`            | integer | `168`   | Keep files needed by versions newer than this. Going below the 168h default breaks readers that are mid-query.                    |
| `--apply`                      | flag    |         | Actually delete. Without this the command only reports.                                                                           |

[Data versions](https://depictio.github.io/depictio-docs/latest/features/versioning/#data-versions)

## `dashboard`

Validate, import and export dashboard YAML files.

[Dashboard YAML](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md)

### `dashboard validate`

```
depictio dashboard validate [OPTIONS] YAML_FILE
```

Validate a dashboard YAML file.

Runs two levels of validation:

1. Schema + domain (always): required fields, enum values, cross-field rules (visu_type, mode/code_content, aggregation×column_type, etc.)
1. Server schema (when a server is configured): resolves each component's workflow_tag + data_collection_tag against the server delta table schema, checks that column_name exists, and validates aggregation/interactive_component_type against the inferred column type. Without `--server` it uses the default server (`$DEPICTIO_CLI_CONFIG_PATH`, else `~/.depictio/CLI.yaml`, else the local server), is skipped when that has no configuration, and what it reports is shown as warnings only. Use `--offline` to skip it.

Example:

```
depictio dashboard validate dashboard.yaml --server local
depictio dashboard validate dashboard.yaml --server admin_config.yaml --offline
depictio dashboard validate dashboard.yaml  # offline unless a default server is set up
```

| Option               | Type | Default | Description                                                                                                                        |
| -------------------- | ---- | ------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `YAML_FILE` required | path |         | Path to YAML dashboard file                                                                                                        |
| `--server`           | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server).  |
| `--verbose` `-v`     | flag |         | No effect, kept for the scripts that pass it. For detailed logs, put `-v` before the command: depictio `-v` dashboard validate ... |
| `--offline`          | flag |         | Skip server schema validation (column names, inferred types, aggregation compatibility)                                            |

### `dashboard import`

```
depictio dashboard import [OPTIONS] YAML_FILE
```

Import a dashboard YAML file to the server.

The project is determined in this order:

1. `--project` option (if provided)
1. project_tag field in the YAML file

Imports into the server `--server` names, else the one `$DEPICTIO_CLI_CONFIG_PATH` or `~/.depictio/CLI.yaml` describes, else the local server (none needed for `--dry-run` validation).

Example:

```
# Validate without a server
depictio dashboard import dashboard.yaml --dry-run

# Import into the server `depictio local up` runs
depictio dashboard import dashboard.yaml --server local

# Overwrite existing dashboard with same title
depictio dashboard import dashboard.yaml --server admin_config.yaml --overwrite

# Override with explicit project ID
depictio dashboard import dashboard.yaml --server admin_config.yaml --project 646b0f3c1e4a2d7f8e5b8c9a

# Skip online column validation
depictio dashboard import dashboard.yaml --server admin_config.yaml --offline
```

| Option               | Type | Default | Description                                                                                                                       |
| -------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `YAML_FILE` required | path |         | Path to YAML dashboard file                                                                                                       |
| `--server`           | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--project` `-p`     | text |         | Project ID (overrides project_tag in YAML)                                                                                        |
| `--overwrite`        | flag |         | Overwrite existing dashboard with same title in project                                                                           |
| `--dry-run`          | flag |         | Validate only, don't import                                                                                                       |
| `--offline`          | flag |         | Skip online checks (column name validation against server DC schema)                                                              |

### `dashboard export`

```
depictio dashboard export [OPTIONS] DASHBOARD_ID
```

Export a dashboard from the server to a YAML file.

Downloads the dashboard configuration and saves it as a minimal YAML file suitable for version control and re-import.

Example:

```
depictio dashboard export 6824cb3b89d2b72169309737 --server local
depictio dashboard export 6824cb3b89d2b72169309737 --server admin_config.yaml -o my-dashboard.yaml
```

| Option                  | Type | Default          | Description                                                                                                                       |
| ----------------------- | ---- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `DASHBOARD_ID` required | text |                  | Dashboard ID to export                                                                                                            |
| `--server`              | text |                  | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--output` `-o`         | path | `dashboard.yaml` | Output file path                                                                                                                  |

## `template`

Export a project and its dashboards as a template someone else can run on their data, or compose one from what the catalog recognises in a results directory.

[Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md)

### `template export`

```
depictio template export --template-id TEMPLATE_ID [OPTIONS] PROJECT_ID
```

Export a project + its dashboards as a template bundle.

The inverse of `depictio ingest --template`: the bundle can be ingested on another dataset.

Example:

```
depictio template export 6824cb3b89d2b72169309737 \
  --template-id my-lab/rnaseq-qc/1 --server admin_config.yaml -o depictio/projects
```

| Option                        | Type | Default | Description                                                                                                                       |
| ----------------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `PROJECT_ID` required         | text |         | Project ID to export                                                                                                              |
| `--template-id` `-t` required | text |         | Template id, e.g. `my-lab/rnaseq-qc/1`                                                                                            |
| `--server`                    | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--output-dir` `-o`           | path | `.`     | Directory to unpack the bundle into                                                                                               |
| `--version`                   | text | `1.0.0` | Template version                                                                                                                  |
| `--description`               | text |         | Template description                                                                                                              |
| `--data-dir`                  | text |         | Local path prefix to re-parameterize as `{DATA_ROOT}` in the template                                                             |

[Export a project as a template](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#export-a-project-as-a-template)

### `template compose`

```
depictio template compose [OPTIONS] DATA_ROOT
```

Compose a template from the files the catalog recognises in a results directory.

Offline: nothing is ingested. Prints what was recognised, the tabs and key metrics of the dashboard, what was left out and why, and the tabular files nothing recognised with what each could show. This is what `depictio ingest <dir>` does by itself when no bundled template fits the run.

| Option               | Type            | Default | Description                                                                                                                                                 |
| -------------------- | --------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATA_ROOT` required | path            |         | Results directory to compose a dashboard for                                                                                                                |
| `--output` `-o`      | path            |         | Write the template here, to edit it and ingest with it: `depictio ingest <dir> --template <out>`. Default: where `depictio ingest` keeps composed templates |
| `--include-unknown`  | flag            |         | Also include the tabular files the catalog does not recognise                                                                                               |
| `--include`          | text repeatable |         | Include the unrecognised files matching this glob (relative to the directory); repeatable                                                                   |
| `--project`          | text            |         | Name of the project to create                                                                                                                               |
| `--verbose`          | flag            |         | List everything left out, with the reason                                                                                                                   |

[Composed dashboards](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/#template-compose)

### `template check`

```
depictio template check [OPTIONS] [TEMPLATE]
```

Check a template's variables against a pipeline's parameters.

Lists each variable and what sets it: a `from_params` rule on the run's params, the outputs themselves (auto), or the user (`--var`). With `--schema`/`--fetch-schema`: every param a rule reads must exist in the release, each rule is evaluated on a default run, and the release's skip\_\* params no rule reads are listed. With `--run`/`--params`: which rules hold for that run and which conditionals fire. Offline unless `--fetch-schema`.

Examples:

```
depictio template check nf-core/rnaseq/3.26.0 --fetch-schema
depictio template check --run results/ --var TRACKS_URI=s3://bucket/run
depictio template check ./my-template --schema ../rnaseq/nextflow_schema.json
depictio template check nf-core/rnaseq/3.26.0 --against 3.27.0
```

| Option           | Type            | Default | Description                                                                                                                  |
| ---------------- | --------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `TEMPLATE`       | text            |         | Template id (nf-core/rnaseq/3.26.0, nf-core/rnaseq) or path. Omitted with `--run`: the template `depictio ingest` would pick |
| `--run`          | path            |         | A results directory: its pipeline_info/params\_`<ts>`.json                                                                   |
| `--params`       | path            |         | A params JSON (nf-core's params\_`<ts>`.json)                                                                                |
| `--var`          | text repeatable |         | KEY=VALUE as given to `depictio ingest`; repeatable                                                                          |
| `--schema`       | path            |         | The pipeline's nextflow_schema.json (a local checkout)                                                                       |
| `--fetch-schema` | flag            |         | Fetch the template release's nextflow_schema.json from GitHub (nf-core only)                                                 |
| `--all`          | flag            |         | Every bundled template, one line each                                                                                        |
| `--schema-cache` | path            |         | Keep fetched schemas here                                                                                                    |
| `--against`      | text            |         | A newer release (3.27.0) or its nextflow_schema.json: which rules it breaks or flips, which skip\_\* flags it adds           |
| `--verbose`      | flag            |         | Also list variables no conditional reads                                                                                     |

## `project-builder`

```
depictio project-builder [OPTIONS] [DIRECTORY]
```

Define a project's data collections from a folder no template fits, in the browser.

| Option      | Type    | Default     | Description                                                                                                                          |
| ----------- | ------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `DIRECTORY` | path    | `.`         | The folder to define data collections from                                                                                           |
| `--out`     | path    |             | Folder to write the template bundle to (default: `<dir>`/.depictio/template, or `~/.depictio/builder/`... when `<dir>` is read-only) |
| `--host`    | text    | `127.0.0.1` | Address to serve on (default: this machine only)                                                                                     |
| `--port`    | integer | `8129`      | Port to serve on                                                                                                                     |
| `--no-open` | flag    |             | Do not open a browser                                                                                                                |

[Project Builder](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#project-builder)

## `manifest`

Write a data manifest from a samplesheet or any table.

[Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#the-data-manifest-contract)

### `manifest from-table`

```
depictio manifest from-table [OPTIONS] TABLE
```

Pivot a wide sample table into a Data Manifest.

Example:

```
depictio manifest from-table samplesheet.csv --id-col sample \
  --base-url s3://my-bucket/run42 -o manifest.json
```

| Option           | Type            | Default         | Description                                                                                                                                     |
| ---------------- | --------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `TABLE` required | path            |                 | Wide table to pivot (nf-core samplesheet, CSV/TSV/YAML/JSON)                                                                                    |
| `--out` `-o`     | path            | `manifest.json` | Output manifest (.json or .csv)                                                                                                                 |
| `--id-col`       | text            |                 | Entity id column. Auto-detected (sample/id/name) if omitted.                                                                                    |
| `--file-cols`    | text repeatable |                 | Columns holding file locations, repeatable. Auto-detected if omitted.                                                                           |
| `--run-col`      | text            |                 | Column to use as the manifest `run` grouping                                                                                                    |
| `--base-url`     | text            |                 | Prefix joined to relative paths, e.g. `s3://my-bucket/run42`. Required when the table holds local paths: a manifest entry must be a remote URL. |

## `migrate`

```
depictio migrate --project PROJECT [OPTIONS]
```

Migrate a project from one Depictio instance to another (non-destructive).

The project is read from `--server` and written to `--to-server`. DEPICTIO_CLI_TOKEN and DEPICTIO_CLI_API_BASE_URL apply to `--server` only.

Mode descriptions:

- `all`: MongoDB docs + S3 files (default, full first-time migration)
- `metadata`: MongoDB docs only (both instances share S3 storage)
- `dashboard`: Dashboards only (project already exists on remote)
- `files`: S3 files only (metadata already migrated)

| Option               | Type                                 | Default | Description                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--project` required | text                                 |         | Project name to migrate                                                                                                                                                                                                                   |
| `--server`           | text                                 |         | Server to migrate from. Server to use: `local` for the one `depictio local up` runs, or a CLI configuration file. Default: `$DEPICTIO_CLI_CONFIG_PATH`, else `~/.depictio/CLI.yaml`, else the local server. Formerly `--CLI-config-path`. |
| `--to-server`        | text                                 |         | Server to migrate to, given the same way as `--server`. Default: `~/.depictio/CLI_remote.yaml`. Formerly `--target-config`.                                                                                                               |
| `--mode`             | `all` `metadata` `dashboard` `files` | `all`   | Migration scope, described below.                                                                                                                                                                                                         |
| `--dry-run`          | flag                                 |         | Preview changes without writing anything                                                                                                                                                                                                  |
| `--overwrite`        | flag                                 |         | Replace the project on the target if it already exists                                                                                                                                                                                    |

[Project migration](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/index.md)

## `backup`

Create, list, validate and restore server database backups (admins only).

[Backup and restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md)

### `backup create`

```
depictio backup create [OPTIONS]
```

Create a backup of the Depictio database.

This command creates a full backup of the MongoDB database, excluding:

- Short-lived tokens
- Temporary users and their related resources

Optionally includes S3 deltatable data for complete backups.

Only administrators can perform backup operations.

| Option               | Type | Default  | Description                                                                                                                       |
| -------------------- | ---- | -------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server`           | text |          | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--dry-run`          | flag |          | Perform validation without creating backup                                                                                        |
| `--include-s3-data`  | flag |          | Include S3 deltatable data in backup                                                                                              |
| `--s3-backup-prefix` | text | `backup` | Prefix for S3 backup location                                                                                                     |

### `backup list`

```
depictio backup list [OPTIONS]
```

List available backup files on the server.

| Option     | Type | Default | Description                                                                                                                       |
| ---------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `--server` | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |

### `backup validate`

```
depictio backup validate [OPTIONS] BACKUP_ID
```

Validate a backup file on the server against Pydantic models.

| Option               | Type | Default | Description                                                                                                                       |
| -------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `BACKUP_ID` required | text |         | ID of the backup to validate (format: YYYYMMDD_HHMMSS)                                                                            |
| `--server`           | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |

### `backup restore`

```
depictio backup restore [OPTIONS] BACKUP_ID
```

Restore data from a backup file.

Warning

This is a destructive operation that will replace existing data! Use `--dry-run` to preview what would be restored without making changes.

Before restoring, the server validates the backup against the current Pydantic models and refuses to restore invalid backups unless `--skip-validation` is passed.

| Option                       | Type | Default | Description                                                                                                                       |
| ---------------------------- | ---- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `BACKUP_ID` required         | text |         | ID of the backup to restore (format: YYYYMMDD_HHMMSS)                                                                             |
| `--server`                   | text |         | `local` for the one `depictio local up` runs, or a CLI configuration file. See [Which server a command uses](#choosing-a-server). |
| `--dry-run` / `--no-dry-run` | flag | off     | Simulate restore without making changes                                                                                           |
| `--collections`              | text |         | Comma-separated list of collections to restore                                                                                    |
| `--force`                    | flag |         | Skip confirmation prompt (use with caution!)                                                                                      |
| `--allow-unverified`         | flag |         | Allow restoring a legacy backup without a checksum sidecar. Checksum mismatches are never bypassable.                             |
| `--skip-validation`          | flag |         | Skip the server-side Pydantic validation gate before restore (dangerous!)                                                         |

## `catalog`

Browse the supported tools and the dashboard components their outputs become.

[Tools catalog](https://depictio.github.io/depictio-docs/latest/catalog/index.md)

### `catalog list`

```
depictio catalog list
```

List every tool + output with its recipe and render targets.

### `catalog info`

```
depictio catalog info TOOL_ID
```

Show one tool's identity (clickable URLs) + every output in detail.

| Option             | Type | Default | Description                      |
| ------------------ | ---- | ------- | -------------------------------- |
| `TOOL_ID` required | text |         | Tool id, e.g. qiime2 or pangolin |

### `catalog preview`

```
depictio catalog preview [OPTIONS] OUTPUT_ID
```

Preview an output's components in the browser, on its bundled fixture.

Served on an ephemeral localhost server (Ctrl-C to stop); `--out FILE` exports a portable, self-contained HTML instead.

Renders every renders_as target through the depictio React viewer's real ComponentRenderer (figure/card/table today). The data is computed Dash-free from the output's bundled fixture. Needs the prebuilt bundle (cd depictio/viewer && pnpm run build:catalog-preview).

| Option               | Type    | Default | Description                                               |
| -------------------- | ------- | ------- | --------------------------------------------------------- |
| `OUTPUT_ID` required | text    |         | Output id, e.g. qiime2_alpha_diversity                    |
| `--theme` `-t`       | text    | `light` | Theme: light or dark                                      |
| `--out` `-o`         | text    |         | Export the self-contained HTML here instead of serving it |
| `--port`             | integer | `0`     | Port for the ephemeral server (0 = auto)                  |
| `--no-open`          | flag    |         | Do not open a browser tab                                 |

### `catalog gallery`

```
depictio catalog gallery [OPTIONS]
```

Browse the whole catalog on one page in the browser.

Every tool's outputs, grouped, with component-type badges, fixture chips, search/filter and copyable renders_as, served on an ephemeral localhost server (Ctrl-C to stop).

Clicking an output opens its full live preview (same renderer as catalog preview). Pass `--out FILE` to export a portable, self-contained HTML instead.

Served or exported, the page needs the prebuilt bundle (cd depictio/viewer && pnpm run build:catalog-preview).

| Option         | Type    | Default | Description                                               |
| -------------- | ------- | ------- | --------------------------------------------------------- |
| `--theme` `-t` | text    | `light` | Theme: light or dark                                      |
| `--out` `-o`   | text    |         | Export the self-contained HTML here instead of serving it |
| `--port`       | integer | `0`     | Port for the ephemeral server (0 = auto)                  |
| `--no-open`    | flag    |         | Do not open a browser tab                                 |

## Other commands

### `commands`

```
depictio commands
```

Show every command and subcommand in one table.

Introspects the live command tree, so it always matches what the CLI actually exposes. Maintainer/CI tooling under the hidden `dev` group is omitted (run `depictio dev --help` to see it).

### `version`

```
depictio version
```

Show the installed depictio version.

## Former names and maintainer commands

Former names, still accepted

They are out of `--help` and print what replaced them.

| Former                    | Now                     | In                                                                                                                                                                                                                                            |
| ------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--api`                   | `--server`              | `dashboard export`, `dashboard import`, `dashboard validate`, `template export`                                                                                                                                                               |
| `--CLI-config-path`       | `--server`              | `backup create`, `backup list`, `backup restore`, `backup validate`, `config check`, `config show`, `config sync`, `data join`, `data process`, `data push-images`, `data scan`, `data vacuum`, `data versions`, `ingest`, `migrate`, `watch` |
| `--config, -c`            | `--server`              | `dashboard export`, `dashboard import`, `dashboard validate`, `template export`                                                                                                                                                               |
| `--data-root`             | `--data-dir`            | `template export`                                                                                                                                                                                                                             |
| `--data-root`             | `DATA_DIR`              | `ingest`                                                                                                                                                                                                                                      |
| `--data-root`             | `ingest --server local` | `local up`                                                                                                                                                                                                                                    |
| `--legacy-scan-depth`     | nothing; to be removed  | `ingest`                                                                                                                                                                                                                                      |
| `--overwrite`             | `--update-config`       | `ingest`                                                                                                                                                                                                                                      |
| `--project-name`          | `--project`             | `ingest`                                                                                                                                                                                                                                      |
| `--project-name`          | `ingest --server local` | `local up`                                                                                                                                                                                                                                    |
| `--rescan-folders`        | `--update-config`       | `ingest`                                                                                                                                                                                                                                      |
| `--skip-dashboard-import` | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-join`             | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-process`          | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-s3-check`         | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-scan`             | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-server-check`     | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--skip-sync`             | `--skip STEP`           | `ingest`                                                                                                                                                                                                                                      |
| `--sync-files`            | `--update-config`       | `ingest`                                                                                                                                                                                                                                      |
| `--target-config`         | `--to-server`           | `migrate`                                                                                                                                                                                                                                     |
| `--template`              | `ingest --server local` | `local up`                                                                                                                                                                                                                                    |
| `--var`                   | `ingest --server local` | `local up`                                                                                                                                                                                                                                    |
| `--verbose-level, -vl`    | `--log-level`           | `depictio`                                                                                                                                                                                                                                    |
| `images push`             | `data push-images`      |                                                                                                                                                                                                                                               |
| `local export-compose`    | `local export`          |                                                                                                                                                                                                                                               |
| `run`                     | `ingest`                |                                                                                                                                                                                                                                               |

Maintainer commands, out of `--help`

For catalog authoring, recipe tests and CI. They may change without notice.

| Command                              | Does                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------- |
| `depictio images list-bucket`        | List images in an S3 bucket/prefix.                                                   |
| `depictio dev recipe run`            | Run a recipe against local data with all 5 validation checkpoints.                    |
| `depictio dev recipe list`           | List all available shared recipes.                                                    |
| `depictio dev recipe info`           | Show recipe details: docstring, sources, and output schema.                           |
| `depictio dev catalog columns`       | Print the output columns a recipe produces (to help write `roles`).                   |
| `depictio dev catalog validate`      | Validate the catalog (CI-friendly: non-zero on error).                                |
| `depictio dev catalog match`         | Recognise which catalog outputs are present in a run directory.                       |
| `depictio dev catalog compose`       | Preview the guided dashboard a run would compose (module → viz).                      |
| `depictio dev catalog refresh-index` | Regenerate the vendored existence indices from authoritative sources.                 |
| `depictio dev catalog schema`        | Emit the JSON Schema for a catalog file (regenerate the committed copy).              |
| `depictio dev catalog kinds`         | Emit the advanced_viz kind descriptors (source for tool-studio's kinds.json).         |
| `depictio dev catalog manifest`      | Emit a JSON snapshot of the existing catalog (source for tool-studio's catalog.json). |
| `depictio dev catalog figure-params` | Emit the figure builder's visualization list + per-viz parameter specs.               |
| `depictio dev backup check-coverage` | Check validation coverage for all MongoDB collections.                                |
| `depictio dev link list`             | List all DC links for a project.                                                      |
| `depictio dev link create`           | Create a new DC link for cross-DC filtering.                                          |
| `depictio dev link resolve`          | Test link resolution by resolving filter values from source to target DC.             |
| `depictio dev link delete`           | Delete a DC link.                                                                     |
