# Depictio CLI Usage

<!-- prettier-ignore -->
!!! note "Note about the CLI"
    `depictio` is the command line interface of Depictio. It ingests pipeline results into a Depictio server, from the project configuration to the dashboards, and manages projects, dashboards and backups on that server. `depictio-cli` is the same command under its former name, kept for existing scripts.

## 📚 Table of Contents

- [Installation](#installation)
- [Quick Reference](#quick-reference)
- [Global Options](#global-options)
- [Which server a command uses](#choosing-a-server)
- [🚀 Commands](#commands)
  - [📥 Ingest Command](#ingest-command)
  - [👀 Watch Command](#watch-command)
  - [💻 Local Server Commands](#local-commands)
  - [📋 Config Commands](#config-commands)
  - [📊 Data Commands](#data-commands)
  - [📈 Dashboard Commands](#dashboard-commands)
  - [🗂️ Catalog Commands](#catalog-commands)
  - [💾 Backup Commands](#backup-commands)
  - [🔄 Migrate Commands](#migrate-commands)
  - [🧑‍🍳 Recipe Commands](#recipe-commands)
- [🛠️ Common Use Cases](#common-use-cases)

## Installation

```bash
pip install depictio
```

See the [installation guide](../installation/cli.md) for the other install options, such as the `[multiqc]` extra and the container image.

## Quick Reference

Running `depictio` with no command prints a quick start. `depictio --help` lists the commands grouped by purpose: **Get started**, **Projects and data**, **Administration** and **Reference**. `depictio commands` shows every command and subcommand in one table.

| Command                       | Description                                                   | Access Level   |
| ----------------------------- | ------------------------------------------------------------- | -------------- |
| `local up`                    | Start a complete Depictio server on this machine              | All users      |
| `local open` / `status` / `down` / `wipe` / `export` | Manage that local server             | All users      |
| `ingest <results dir>`        | Ingest pipeline results, from validation to dashboards        | All users      |
| `watch <results dir>`         | Ingest pipeline results, then again whenever they change      | All users      |
| `config show`                 | Show the CLI configuration in use                             | All users      |
| `config check`                | Check the server and its S3 storage, or validate a project file | All users    |
| `config sync`                 | Validate a project configuration and sync it to the server    | All users      |
| `config nextflow`             | Print or install the Nextflow trigger                         | All users      |
| `data scan`                   | Scan project files                                            | All users      |
| `data process`                | Process data collections                                      | All users      |
| `data join`                   | Run the table joins the project configuration defines         | All users      |
| `data push-images`            | Upload a directory of images for an image data collection     | All users      |
| `data versions`               | List the Delta commits of a data collection                   | All users      |
| `data vacuum`                 | Remove the Delta files no retained commit needs               | All users      |
| `dashboard validate`          | Validate a dashboard YAML file                                | All users      |
| `dashboard import`            | Import a dashboard YAML file to the server                    | All users      |
| `dashboard export`            | Export a dashboard to a YAML file                             | All users      |
| `catalog list` / `info` / `preview` / `gallery` | Browse the tools catalog                    | All users      |
| `backup create`               | Create a backup                                               | **Admin only** |
| `backup list`                 | List available backups                                        | **Admin only** |
| `backup validate`             | Validate a backup against the models                          | **Admin only** |
| `backup restore`              | Restore from a backup                                         | **Admin only** |
| `migrate`                     | Migrate a project to another instance                         | **Admin only** |
| `commands`                    | Show every command and subcommand                             | All users      |
| `version`                     | Show the installed version                                    | All users      |

??? info "Former command names, still accepted (v1.12.0+)"

    These names still work, out of the help, and print the name to use now.

    | Former name | Now |
    | ----------- | --- |
    | `depictio run` | `depictio ingest` |
    | `depictio images push` | `depictio data push-images` |
    | `depictio local export-compose` | `depictio local export` |
    | `--CLI-config-path` (every command) | `--server` |
    | `-c/--config`, with `--api` (dashboard commands) | `--server` |
    | `--target-config` (migrate) | `--to-server` |
    | `--data-root` (ingest) | the results directory, as the argument |
    | `--project-name` (ingest) | `--project` |
    | `--skip-server-check`, `--skip-s3-check`, `--skip-sync`, `--skip-scan`, `--skip-process`, `--skip-join`, `--skip-dashboard-import` | `--skip STEP`, see [Skipping steps](#skipping-steps) |
    | `-vl/--verbose-level` | `--log-level` |

## Global Options

Global options go before the command: `depictio -vv ingest results/`.

| Option        | Short | Type     | Default | Description                                                                 |
| ------------- | ----- | -------- | ------- | --------------------------------------------------------------------------- |
| `--verbose`   | `-v`  | count    |         | Show logs: `-v` for INFO, `-vv` for DEBUG                                   |
| `--log-level` |       | `string` |         | Show logs from this level up: `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. No `-v` needed. Formerly `-vl/--verbose-level` |
| `--version`   | `-V`  | `flag`   |         | Show the version and exit                                                   |
| `--help`      | `-h`  | `flag`   |         | Show the help of any command                                                |

## Which server a command uses <small>(v1.12.0+)</small> { #choosing-a-server }

Every command that talks to a server takes `--server`:

- `--server local` uses the server that [`depictio local up`](../installation/local.md) runs on this machine.
- `--server <file>` uses a CLI configuration file, such as the `CLI.yaml` downloaded from the [CLI agents page](../usage/get_started.md#create-a-cli-configuration) of a Depictio instance.

Without `--server`, a command uses, in this order:

1. the file that `$DEPICTIO_CLI_CONFIG_PATH` names (the variable also takes `local`);
2. else `~/.depictio/CLI.yaml`, when that file exists;
3. else the local server.

This is a fixed rule on files and variables: the CLI does not check whether a local server is running, so a command reaches the same server whether one runs or not. When `DEPICTIO_CLI_TOKEN` or `DEPICTIO_CLI_API_BASE_URL` is set, step 3 does not apply: the command is meant for a remote server, and it reports the missing `~/.depictio/CLI.yaml` instead.

Each command starts by naming the server it reaches and the file it read. When it reaches a server from `~/.depictio/CLI.yaml` or `$DEPICTIO_CLI_CONFIG_PATH` while a local server is running, it says so:

```text
A local server is running too (http://127.0.0.1:8058): add --server local to use it
```

`depictio migrate` reads from `--server` and writes to `--to-server`, which takes the same values. Its default is `~/.depictio/CLI_remote.yaml`, with no fallback to the local server.

The options used before `--server` still work, out of the help, and print a notice: `--CLI-config-path` on every command, `-c/--config` with `--api` on the dashboard commands, and `--target-config` on `migrate`.

### Environment variables <small>(v1.10.0+)</small> { #environment-variables }

These variables override parts of a CLI configuration file, so the token can stay out of the file, for example on a CI runner.

| Variable | Effect |
| -------- | ------ |
| `DEPICTIO_CLI_CONFIG_PATH` | The configuration to use when `--server` is not given: a file, or `local` |
| `DEPICTIO_CLI_TOKEN` | Replaces the token from the file |
| `DEPICTIO_CLI_API_BASE_URL` | Replaces `api_base_url` from the file |

`DEPICTIO_CLI_TOKEN` and `DEPICTIO_CLI_API_BASE_URL` never apply to `--server local`, whose configuration is complete as `depictio local up` wrote it. For `depictio migrate`, they apply to `--server` only, not to `--to-server`.

## 🚀 Commands

### 📥 Ingest Command { #ingest-command }

<span id="run-command"></span>

Ingest pipeline results into a Depictio server, from validation to dashboards. Formerly `run`, which still works and says it is now `ingest`.

```bash
depictio ingest [OPTIONS] [DATA_DIR]
```

**Quick Start:**

```bash
# The template is detected from the results directory
depictio ingest results/

# After a new run: refresh the project, its dashboards kept as edited in the viewer
depictio ingest results/ --update-config
```

The template is detected from the run's own provenance, such as the pipeline name and version a Nextflow run records. Pass `--template <id>` to choose one, or `--project-config-path <project.yaml>` for a pipeline Depictio ships no template for.

Without a template for the run's exact release, the CLI takes the highest shipped version that is not newer than the run, or the lowest one when the run predates them all. When that template was built for another major release of the pipeline, the CLI warns: outputs move between major releases, so data collections that find no files are skipped and the tabs built on them are dropped.

Here the template is detected from nf-core/taxprofiler results, previewed with `--dry-run`, then ingested into the local server:

<div class="asciinema-cast" data-cast="assets/casts/depictio-ingest-detect.cast" data-poster="npt:0:51" data-idle-time-limit="2.5"></div>

**Pipeline Steps:**

1. ✅ Check that the server answers
2. ✅ Check the S3 storage configuration
3. ✅ Validate the project configuration, or resolve the template
4. ✅ Sync the project configuration to the server
5. ✅ Scan the data files
6. ✅ Process the data collections, uploading the images of a collection that sets `local_images_path`
7. ✅ Run the table joins the project configuration defines
8. ✅ Import the dashboards the project lacks, from the template or from `--dashboard`

`depictio ingest --help` shows the essential options first. The others sit in panels, which the tables below follow.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `DATA_DIR` | `path` | | The results directory to ingest, as the argument. Without `--template` or `--project-config-path`, the template is detected from it. Formerly `--data-root` |
| `--server` | `string` | see [Which server a command uses](#choosing-a-server) | `local`, or a CLI configuration file. Formerly `--CLI-config-path` |
| `--template` | `string` | detected | Template ID. Pin a version (`nf-core/ampliseq/2.16.0`), or use `nf-core/ampliseq/latest`, or just `nf-core/ampliseq`, for the newest shipped version (v1.5.2+). Not with `--project-config-path` |
| `--project-config-path` | `string` | | Project YAML, for a pipeline Depictio ships no template for. Not with `--template` |
| `--update-config` | `flag` | `false` | Refresh a project that exists, see [Refreshing a project](#refreshing-a-project). `--overwrite` is the same option |
| `--var` | `KEY=VALUE` | | Template variable, repeatable |
| `--dry-run` | `flag` | `false` | Validate the project configuration locally and list the steps that would run, without contacting the server. From v1.13.2 it also lists how many files each data collection would match |

Since **v1.6.0**, resolving a template also picks up any [recipe seed](../usage/projects/templates.md#recipe-seeds) committed beside the data: a `source: transformed` data collection with a `{DATA_ROOT}/{dc_tag}.tsv` next to it is scanned from that file instead of re-running its recipe against raw pipeline inputs the bundled projects do not ship. See [Templates](../usage/projects/templates.md) for full documentation.

??? info "🗂️ Project and runs"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--project` | `string` | the template's | Project name. Replaces the name the template gives, or the `name` in the `--project-config-path` file. `--attach-run` and `--update-config` find the project by it. Formerly `--project-name` |
    | `--attach-run` | `flag` | `false` | Add the results directory to an existing project as **another run**, see [Refreshing a project](#refreshing-a-project) (v1.10.0+) |
    | `--drop-missing-runs` | `flag` | `false` | On a refresh, remove the runs of a location added with `--attach-run` that is not on this machine. Without it, such a refresh stops before changing anything. Cannot be combined with `--attach-run` (v1.13.1+) |
    | `--provenance-file` | `path` | | Extra recap file (JSON, YAML or two-column key/value TSV) listed in the project's [run provenance](../usage/projects/templates.md#run-provenance) under *User provided*. Repeatable (v1.8.3+) |

??? info "📈 Dashboards"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--dashboard` | `path` | | Dashboard YAML to import instead of the template's own. Repeatable. Since **v1.10.0** it also works without a template |
    | `--dashboard-name` | `string` | | Title of the main dashboard. Without it, a new dashboard takes the title in its YAML and a refresh keeps the current one, even if renamed in the viewer. With it, a refresh renames the main dashboard and leaves its contents as they are. Tabs keep their titles |
    | `--reset-dashboards` | `flag` | `false` | Import the template's dashboards (or `--dashboard`'s) over the ones the project has: the layout and components edited in the viewer are lost, the titles are kept. Implies `--update-config`. With `--project-config-path`, it needs `--dashboard` or `--template`, since a project file brings no dashboards of its own |

??? info "⚙️ Scope and steps"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--workflow-name` | `string` | | Scan and process only this workflow (its tag) |
    | `--data-collection-tag` | `string` | | Scan and process only this data collection |
    | `--skip` | `STEP` | | Steps to skip, see [Skipping steps](#skipping-steps) |
    | `--continue-on-error` | `flag` | `false` | Carry on when a step fails. The command still exits with code 1 at the end |
    | `--sync-changed` | `flag` | `false` | Re-upload only the files whose size or modification time moved since the last scan. Narrower than `--update-config`, which re-uploads every file |
    | `--write-mode` | `string` | `overwrite` | How step 6 writes a table. `overwrite` rewrites it whole. `replace-runs` partitions it by run and rewrites only the runs in this batch, leaving the others untouched. See [Data versions](../features/versioning.md#how-new-data-versions-are-written) |
    | `--incremental-write` | `flag` | `false` | With `--write-mode replace-runs`, rewrite only the runs that changed instead of rebuilding the whole table. Falls back to a full rebuild whenever that cannot be done safely (run removed, table not partitioned by run, column type changed) |
    | `--skip-unchanged` | `flag` | `false` | Leave a data collection's table untouched when the scan found no new, changed or removed file for it. Off by default, so that ingesting again always rebuilds a project that drifted |
    | `--repartition` | `flag` | `false` | Let `--write-mode replace-runs` partition by run a table that is not yet. This rewrites every row, so it is never done implicitly, and never by the watcher |

    Since v1.15.0 the scan honours each data collection's `max_depth` and `ignore`, and
    prints a warning naming the collections that set them, since it may now register
    fewer files than before. `ingest` also takes `--legacy-scan-depth`, left out of its help, to ignore
    them for one more release. See [Limiting a recursive scan](../usage/projects/yaml-examples.md#scan-bounds).

??? info "🔑 Automation"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--pipeline-id` | `string` | | Which pipeline produced this data, as `<name>/<version>`. Resolves a bundled template when neither `--template` nor `--project-config-path` is given, and is ignored otherwise, so an explicit choice always wins. The [Nextflow trigger](nextflow-trigger.md) fills it from the pipeline's `manifest` block (v1.10.0+) |
    | `--triggered-by` | `string` | `manual` | What invoked this ingestion, recorded on the project and shown as a badge in its [ingestion report](../features/dashboards.md#triggered-by) (v1.10.0+) |
    | `--user` | `string` | | Email of a user to provision and run as. Requires `--provisioning-key` (v1.1.3+) |
    | `--provisioning-key` | `string` | | Shared provisioning secret. Reads `DEPICTIO_AUTH_PROVISIONING_API_KEY` from the environment if the flag is omitted |

    With `--user`, the CLI runs a pipeline **on behalf of a user who has no account yet**: it creates-or-gets the account, runs the whole ingestion as them, and prints a passwordless login link straight to the dashboard it imported.

    ```bash
    depictio ingest /path/to/results \
      --template nf-core/ampliseq/latest \
      --user alice@example.org \
      --provisioning-key "$DEPICTIO_AUTH_PROVISIONING_API_KEY"
    ```

    The key is a **server-side secret**: the instance must be started with the
    matching `DEPICTIO_AUTH_PROVISIONING_API_KEY`, otherwise the provisioning
    endpoints stay disabled and the run is rejected. The CLI redacts the value
    from its own logs. See
    [Pipeline provisioning](../usage/guides/authentication-modes.md#pipeline-provisioning-and-magic-links-v113).

??? info "⚡ Performance and debugging"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--streaming` | `flag` | `false` | Stream the Delta write instead of materialising the whole table in memory. Lowers peak RSS on large ingests. Experimental, falls back to the standard write on any failure (v1.3.0+) |
    | `--preview-recipes` | `flag` | `false` | Show recipe input sources and transformed output before writing to Delta Lake |
    | `--rich-tables` | `flag` | `false` | Show a detailed summary of the run |
    | `--concurrency` | `int` | `4` | Parallel HTTP requests for file uploads and cleanup deletes |
    | `--upload-chunk-size` | `int` | `1000` | Files per `/files/upsert_batch` request |
    | `--state-cache` / `--no-state-cache` | `flag` | `--state-cache` | Skip the runs whose file tree is unchanged since the last successful scan, from a local cache. Only applies when rescanning |
    | `--async-upsert` | `flag` | `false` | Ask the server to profile each written table in the background, and poll until it finishes, instead of holding one long request open. A server without offloading enabled ignores it and answers inline. See [Offloading the table profile](../installation/docker.md#async-upsert) |

    | Variable | Default | Description |
    |----------|---------|-------------|
    | `DEPICTIO_INGEST_STREAMING_WRITE` | unset | Same as `--streaming`, as an environment toggle. |
    | `DEPICTIO_INGEST_DC_WORKERS` | `1` | Ingest this many data collections concurrently. Clamped to 4 and to the number of data collections, so an over-large value degrades to the cap. An unparseable value logs a warning and falls back to sequential. |
    | `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` | `3600` | With `--async-upsert`, the longest wait for one server job, in seconds. `0` waits without limit. (v1.15.0+) |

#### Skipping steps { #skipping-steps }

`--skip` takes step names, comma-separated or repeated: `server-check`, `s3-check`, `sync`, `scan`, `process`, `join` and `dashboards`. An unknown name is a usage error that lists the known ones, so a typo never runs the step it meant to skip. Skipping `process` skips the image upload too, and `--skip dashboards` cannot be combined with `--reset-dashboards`.

```bash
depictio ingest results/ --skip server-check,s3-check
```

`--skip` replaces seven flags, which still work and print a notice: `--skip-server-check`, `--skip-s3-check`, `--skip-sync`, `--skip-scan`, `--skip-process`, `--skip-join` and `--skip-dashboard-import` (now `--skip dashboards`).

#### Refreshing a project <small>(v1.12.0+)</small> { #refreshing-a-project }

If the project already exists, `ingest` changes nothing, says how to go on, and exits with code 2. Say which one you meant:

| You want | Option | What happens |
| --- | --- | --- |
| To refresh the project with new data | `--update-config` | The configuration is updated, every run is rescanned and the tables are rebuilt. The project's dashboards are kept as they are, edits made in the viewer included, and the template's dashboards it lacks are added |
| One project, many runs | `--attach-run` | The results directory is added to the project as another run, and the tables are rebuilt from every run. The dashboards are kept, as with `--update-config` |
| To start the dashboards over | `--reset-dashboards` | The template's dashboards (or `--dashboard`'s) are imported over the project's: the layout and components edited in the viewer are lost, the titles are kept. Implies `--update-config` |

`--overwrite` is the same option as `--update-config`. `--rescan-folders` and `--sync-files`, which used to go with it, are part of every refresh now.

A project not on the server yet is created by `--update-config`, so a script can pass it every time.

Here a third run is added to a project ingested from a project YAML: a dry run, then the refresh, which keeps its dashboard:

<div class="asciinema-cast" data-cast="assets/casts/depictio-ingest-refresh.cast" data-poster="npt:0:48" data-idle-time-limit="2.5"></div>

**Dashboards.** Dashboards are matched by their origin, the template file or the `--dashboard` file they came from, not by their title. Renaming a dashboard in the viewer no longer makes the next refresh import a second copy, and the new title is kept. The summary at the end of the run lists each dashboard as `created`, `kept` or `replaced`, with its link.

A `--dashboard` file inside the template or the project file's folder is matched by its path there. One from anywhere else is matched by its absolute path (v1.13.1+, by its file name before), so moving that file makes the next refresh create a new dashboard.

**Tabs** <small>(v1.13.1+)</small>. A multi-tab dashboard that a refresh keeps gains the template tabs it lacks, after its existing tabs. The summary says how many, as in `kept (2 tabs added)`. A tab deleted in the viewer comes back on the next refresh.

!!! note "What a refresh does not keep yet"
    A kept dashboard keeps its layout, components and title, but a refresh still resets the subtitle, the icons and the tab order edited in the viewer.

**Run locations** <small>(v1.13.1+)</small>. `--attach-run` records its directory on the server. A refresh keeps the runs of the results directory you give, or of the locations the project file lists, plus the runs of those recorded directories. The runs of any other location are removed, with a warning for each location.

So a results directory that moved replaces the old one, and a location removed from the project file is removed from the project.

Attaching a directory that is already one of the project's locations records it, so a later refresh keeps it. A project ingested before attached runs were recorded has no record: a refresh removes its extra locations, unless you attach them again first. In v1.12.0, a refresh kept every location the project had.

**Missing locations** <small>(v1.13.1+)</small>. If a location added with `--attach-run` is not on the machine that runs the refresh, the refresh stops with exit code 1 before it changes anything. Pass `--drop-missing-runs` to remove those runs from the project on purpose.

**Flat workflows** <small>(v1.13.1+)</small>. A workflow whose `data_location.structure` is `flat` names each run after its directory. Two of its locations whose directories have the same name would be one run, so they are refused: rename one of the directories, or ingest it into another project.

**Single-file collections.** A data collection with `scan.mode: single` (a samplesheet, a metadata table, a tree) keeps reading the run that created the project.

#### Exit codes

| Code | Meaning |
| ---- | ------- |
| `0` | Every step completed |
| `1` | A step failed, including under `--continue-on-error`, the CLI configuration could not be used, or a refresh stopped on a missing run location |
| `2` | Nothing to do as asked: no template detected and none given, the project already exists without `--update-config` or `--attach-run`, the project `--attach-run` names does not exist, or a usage error |

Here the first step fails, as no server answers, and its message says how to start one:

<div class="asciinema-cast" data-cast="assets/casts/depictio-ingest-error.cast" data-poster="npt:0:13" data-idle-time-limit="2.5"></div>

**Examples:**

=== "Template detected"

    ```bash
    # The template comes from the run's own provenance
    depictio ingest /data/my_ampliseq_run
    ```

=== "Pinned template"

    ```bash
    # Set up a complete ampliseq project from raw pipeline output
    depictio ingest /data/my_ampliseq_run \
      --template nf-core/ampliseq/latest \
      --var SAMPLESHEET_FILE=/data/samplesheet.tsv
    ```

=== "Project YAML"

    ```bash
    # A pipeline with no bundled template
    depictio ingest --project-config-path ./config.yaml
    ```

=== "Local server"

    ```bash
    # The server `depictio local up` runs on this machine
    depictio ingest /data/my_ampliseq_run --server local
    ```

=== "Dry Run"

    ```bash
    # Validate the configuration and preview the scan, without contacting the server
    depictio ingest /data/my_ampliseq_run --dry-run
    ```

    From v1.13.2 the dry run prints a table of the files each data collection would match,
    counted by the scanner itself. A derived collection shows `n/a (no scan)`, and a
    collection that would match nothing is named in a warning.

=== "Debugging"

    ```bash
    # DEBUG logs, carry on past a failed step, skip the server checks
    depictio -vv ingest --project-config-path ./config.yaml \
      --continue-on-error \
      --skip server-check,s3-check \
      --rich-tables
    ```

### 👀 Watch Command { #watch-command }

`depictio ingest` on a loop: ingest the results directory, then again whenever its files
change. Each cycle writes new [data versions](../features/versioning.md#data-versions) of
the tables it touches.

```bash
depictio watch [OPTIONS] [DATA_DIR]
```

```bash
# Rewrite only the runs that changed, on each cycle
depictio watch results/ --write-mode replace-runs --incremental-write
```

The project is chosen as `ingest` chooses it, from `DATA_DIR`, `--template` or
`--project-config-path`. The first cycle runs at once and refreshes the project as
`ingest --update-config` does, which brings it up to date with whatever changed while
nothing watched. The later cycles rescan and rewrite what moved. No cycle checks the
server and S3 or imports dashboards: run `depictio ingest` once first if the project
should have its dashboards.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `DATA_DIR` | `path` | | Directory of the pipeline results to watch. Without `--template` or `--project-config-path`, the template is detected from it |
| `--server` | `string` | see [Which server a command uses](#choosing-a-server) | `local`, or a CLI configuration file |
| `--template` | `string` | detected | Template to build the project from, as for `ingest`. Not with `--project-config-path` |
| `--project-config-path` | `string` | | Project YAML, for a pipeline Depictio ships no template for. Not with `--template` |
| `--project` | `string` | | Project name. Replaces the name the template gives, or the `name` in the project file |
| `--var` | `KEY=VALUE` | | Template variable, repeatable |
| `--mode` | `string` | `incremental` | `incremental` re-uploads only the files that changed. `full` re-uploads and rewrites everything on every cycle |
| `--full-every` | `int` | | Run a full cycle every N incremental ones |
| `--backend` | `string` | `auto` | `native` (filesystem events only), `polling` (a periodic walk), `both`, or `auto`: `both` on local disk, `polling` on a network filesystem, where events do not see writes made from another host |
| `--interval` | `float` | `300` | Seconds between polling walks, also the backstop for lost events |
| `--debounce` | `float` | `30` | Seconds of quiet before a cycle starts |
| `--max-delay` | `float` | `300` | Ceiling on the debounce, so a tree written continuously still gets ingested |
| `--settle` | `float` | `5` | Seconds a file must keep the same size and modification time before it is ingested |
| `--write-mode` | `string` | `overwrite` | How each cycle writes a table, as for `ingest`: `overwrite` or `replace-runs` |
| `--incremental-write` | `flag` | `false` | With `--write-mode replace-runs`, rewrite only the runs that changed. Ignored, with a warning, with `overwrite` |
| `--drop-missing-runs` | `flag` | `false` | Remove the runs of a location added with `ingest --attach-run` that is not on this host. Without it, such a project stops the first cycle |
| `--concurrency` | `int` | `4` | Parallel HTTP requests during each cycle |
| `--once` | `flag` | `false` | Run a single cycle and exit with its status |
| `--max-runs` | `int` | | Stop after this many cycles, the first included |
| `--dry-run` | `flag` | `false` | Report each cycle's changes without writing to the server |

With `--mode incremental` and the default `--write-mode overwrite`, the watcher warns at
start-up: a collection whose files moved still has its whole table rewritten.
`--write-mode replace-runs --incremental-write` rewrites only the runs that changed. An
incremental cycle leaves alone the collections whose files did not move, as long as the
previous cycle succeeded; after a failure, and on every full cycle, every table is
rebuilt.

`auto` picks polling alone as soon as one watched location is on NFS, SMB/CIFS, Lustre,
GPFS, BeeGFS, GlusterFS, Ceph, AFS, 9p or a FUSE mount. A location of the project that does not exist on this machine is skipped with
a warning, and the watcher stops if none is left.

**Stopping.** Ctrl-C or SIGTERM lets the cycle in progress finish, then exits, so the
watcher is safe to run under systemd or as a container.

**One per project.** A watcher holds a lock under `~/.depictio/state/`, per server and
project, next to the scan-state cache (`DEPICTIO_CLI_STATE_DIR` moves both).
`depictio ingest` takes the same lock before its first write, so a second watcher or
ingestion on the same project stops at once with an error that names the lock file.

**In the admin panel.** A watcher registers with the server, sends a heartbeat every
minute, and asks every 5 seconds whether someone pressed **Run now** on its card in the
[Watchers pane](../usage/administration/monitoring.md#watchers). It reaches out to the
server and never the reverse, so it works from a machine the server cannot reach, such
as an HPC login node. Its runs show **Watch**, or **UI** for one started by **Run now**,
as their trigger. On a server with `DEPICTIO_MONITORING_ENABLED=false`, the watcher
carries on without reporting.

#### Running a watcher as a service { #running-a-watcher-as-a-service }

The depictio repository ships two ways to keep a watcher running, both configured through
environment variables:

- [`deploy/depictio-watch@.service`](https://github.com/depictio/depictio/blob/main/deploy/depictio-watch@.service),
  a systemd template unit: one instance per project, each reading
  `/etc/depictio/<instance>.env`;
- [`deploy/docker-compose.watcher.yaml`](https://github.com/depictio/depictio/blob/main/deploy/docker-compose.watcher.yaml),
  a container running the `depictio-cli` image, configured by a `.env` next to it
  (start from [`deploy/.env.example`](https://github.com/depictio/depictio/blob/main/deploy/.env.example)).

=== "systemd"

    ```bash
    sudo cp deploy/depictio-watch@.service /etc/systemd/system/
    sudo systemctl edit depictio-watch@.service    # set User=, the account it runs as
    sudo install -d /etc/depictio
    sudoedit /etc/depictio/myproject.env
    sudo systemctl enable --now depictio-watch@myproject
    journalctl -u depictio-watch@myproject -f
    ```

=== "Docker Compose"

    ```bash
    cp deploy/.env.example deploy/.env    # then fill it in
    docker compose -f deploy/docker-compose.watcher.yaml up -d
    docker compose -f deploy/docker-compose.watcher.yaml logs -f
    ```

    For several projects, run it once per project with its own `COMPOSE_PROJECT_NAME`
    and `--env-file`.

| Variable | systemd | Docker Compose |
|----------|---------|----------------|
| `DEPICTIO_CLI_CONFIG` | Required: the CLI configuration | Required |
| `DEPICTIO_PROJECT_CONFIG` | Required: the project YAML | Required |
| `DEPICTIO_DATA_ROOT` | | Required: the data root on the host, mounted read-only |
| `DEPICTIO_DATA_ROOT_MOUNT` | | `/data`. Must match the paths in the project YAML |
| `DEPICTIO_WATCH_MODE` | `incremental` | `incremental` |
| `DEPICTIO_WATCH_WRITE_MODE` | `overwrite` | `replace-runs` |
| `DEPICTIO_WATCH_INCREMENTAL_WRITE` | `0`. `1` adds `--incremental-write` | Not a variable: uncomment `--incremental-write` in the compose file |
| `DEPICTIO_WATCH_BACKEND` | `auto` | `polling`, since file events do not cross a bind mount reliably |
| `DEPICTIO_WATCH_INTERVAL` | `300` | `300` |
| `DEPICTIO_WATCH_DEBOUNCE` | `30` | `30` |
| `DEPICTIO_WATCH_SETTLE` | `5` | `5` |
| `DEPICTIO_CLI_BIN` | `/usr/local/bin/depictio` | |
| `DEPICTIO_CLI_IMAGE` | | `ghcr.io/depictio/depictio-cli:latest` |
| `WATCHER_NAME` | | `depictio-watcher`, the container name |

Both give a stopping watcher 15 minutes to finish its cycle. The unit keeps the lock and
the scan-state cache in `/var/lib/depictio-watch`, and the compose file in a named volume,
so a restart does not rescan everything.

### 💻 Local Server Commands <small>(v1.12.0+)</small> { #local-commands }

`depictio local` runs a complete Depictio server on this machine, without Docker, and manages it: `up`, `open`, `down`, `status`, `wipe` and `export`. It manages the server only: data goes in with `depictio ingest`, which reaches the local server with `--server local`, or by default when no other server is configured (see [Which server a command uses](#choosing-a-server)).

```bash
depictio local up
depictio ingest results/ --server local
```

See [Python package installation](../installation/local.md) for every command and option.

### 📋 Config Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio config`"
    All commands in this section are part of the `config` command family. Use them to check the CLI setup, sync project configurations, and hook Depictio into Nextflow.

#### `config show`

Show the CLI configuration in use.

```bash
depictio config show [OPTIONS]
```

| Parameter        | Type     | Default | Description                                                         |
| ---------------- | -------- | ------- | ------------------------------------------------------------------- |
| `--server`       | `string` | see [above](#choosing-a-server) | `local`, or a CLI configuration file    |
| `--project-name` | `string` |         | Also show this project's metadata as registered on the server       |

```bash
depictio config show --project-name my-project
```

---

#### `config check`

Run the preflight checks. Without `--project-config-path`, it checks that the server answers and that its S3 storage is reachable. With `--project-config-path`, it validates that project configuration, which also runs the S3 storage check it depends on.

```bash
depictio config check [OPTIONS]
```

| Parameter               | Type     | Default | Description                                  |
| ----------------------- | -------- | ------- | -------------------------------------------- |
| `--server`              | `string` | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string` |         | Project configuration file to validate       |

```bash
# The server and its storage
depictio config check

# A project configuration
depictio config check --project-config-path ./config.yaml
```

---

#### `config sync`

Validate a project configuration and sync it to the server.

```bash
depictio config sync [OPTIONS]
```

| Parameter               | Type      | Default | Description                                     |
| ----------------------- | --------- | ------- | ----------------------------------------------- |
| `--server`              | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string`  |         | Project configuration file                      |
| `--update`              | `boolean` | `false` | Update the project configuration on the server  |

```bash
depictio config sync --project-config-path ./config.yaml --update
```

---

#### `config nextflow` <small>(v1.10.0+)</small> { #config-nextflow }

Print or install the `workflow.onComplete` snippet that lets a Nextflow pipeline
ingest its own results when it finishes. Full guide:
[Nextflow trigger](nextflow-trigger.md).

```bash
depictio config nextflow [OPTIONS]
```

| Parameter     | Type   | Default | Description                                                                                  |
| ------------- | ------ | ------- | -------------------------------------------------------------------------------------------- |
| `--print`     | `flag` | `false` | Write the snippet's contents to stdout instead of its path                                    |
| `--install`   | `flag` | `false` | Enable the trigger for every pipeline on this machine, once                                   |
| `--uninstall` | `flag` | `false` | Undo `--install`, leaving any other Nextflow settings alone                                   |
| `--default-enabled` / `--default-disabled` | `flag` | `--default-enabled` | With `--install`: whether a pipeline that sets no `--depictio_enabled` triggers Depictio, or stays opt-in |

With no flag it prints the path of the bundled snippet, which is what makes the
`$(...)` form below work.

```bash
# one pipeline, one run
nextflow run nf-core/ampliseq -profile docker --outdir results \
  -c $(depictio config nextflow)

# every pipeline on this machine, once
depictio config nextflow --install
nextflow run nf-core/ampliseq -profile docker --outdir results
```

### 📊 Data Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio data`"
    All commands in this section are part of the `data` command family. They run one ingestion step at a time, which `depictio ingest` otherwise runs in order.

#### `data scan`

Scan the project's data folders for the files its data collections match, and register them on the server. The project configuration must already be synced.

```bash
depictio data scan [OPTIONS]
```

| Parameter               | Type      | Default | Description                            |
| ----------------------- | --------- | ------- | -------------------------------------- |
| `--server`              | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string`  |         | Project configuration file             |
| `--workflow-name`       | `string`  |         | Workflow to scan                       |
| `--data-collection-tag` | `string`  |         | Data collection to scan                |
| `--rescan-folders`      | `boolean` | `false` | Reprocess all runs for the data collection |
| `--sync-files`          | `boolean` | `false` | Update files for the data collection   |
| `--sync-changed`        | `boolean` | `false` | Re-upload only the files whose metadata moved since the last scan. Narrower than `--sync-files`, which re-uploads every registered file |
| `--dry-run`             | `boolean` | `false` | Report what would be registered or removed, without writing to the server |
| `--legacy-scan-depth`   | `boolean` | `false` | Ignore each data collection's scan `max_depth` and `ignore`, as releases before v1.15.0 did. Deprecated, and to be removed. See [Limiting a recursive scan](../usage/projects/yaml-examples.md#scan-bounds) |
| `--state-cache` / `--no-state-cache` | `boolean` | `--state-cache` | Skip the runs whose file tree is unchanged since the last successful scan, from a local cache. Only applies when rescanning |
| `--concurrency`         | `int`     | `4`     | Parallel HTTP requests for file uploads and cleanup deletes |
| `--upload-chunk-size`   | `int`     | `1000`  | Files per `/files/upsert_batch` request |
| `--rich-tables`         | `boolean` | `false` | Display rich tables in the output      |

```bash
depictio data scan --project-config-path ./config.yaml --workflow-name my-workflow
```

---

#### `data process`

Build each data collection's Delta table from the files `depictio data scan` found.

```bash
depictio data process [OPTIONS]
```

| Parameter               | Type      | Default | Description                      |
| ----------------------- | --------- | ------- | -------------------------------- |
| `--server`              | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string`  |         | Project configuration file       |
| `--overwrite`           | `boolean` | `false` | Overwrite existing tables        |
| `--write-mode`          | `string`  | `overwrite` | `overwrite` rewrites the whole table. `replace-runs` partitions it by run and rewrites only the runs in this batch, leaving the others untouched |
| `--repartition`         | `boolean` | `false` | Let `--write-mode replace-runs` partition by run a table that is not yet. This rewrites every row |
| `--async-upsert`        | `boolean` | `false` | Ask the server to profile the written table in the background and poll until it finishes. Servers without offloading enabled ignore it. See [Offloading the table profile](../installation/docker.md#async-upsert) |
| `--rich-tables`         | `boolean` | `false` | Display rich tables in the output |
| `--preview-recipes`     | `boolean` | `false` | Show recipe input sources and transformed output without writing to Delta Lake |

```bash
depictio data process --project-config-path ./config.yaml --overwrite
```

---

#### `data join`

Run the table joins defined in the project configuration, on the client side, and optionally persist the results as Delta tables.

<!-- prettier-ignore -->
!!! note "Links vs Joins"
    For interactive cross-DC filtering, use **links** (configured in YAML, resolved at runtime). Use **joins** only when you need a pre-computed combined dataset stored as a Delta table. See [Cross-DC Filtering](../features/cross-dc-filtering.md).

```bash
depictio data join [OPTIONS]
```

| Parameter               | Short | Type      | Default | Description                                     |
| ----------------------- | ----- | --------- | ------- | ----------------------------------------------- |
| `--server`              |       | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` |       | `string`  |         | Project configuration file                      |
| `--join-name`           | `-j`  | `string`  |         | Join to process (all when not given)            |
| `--preview`             | `-p`  | `boolean` | `false` | Preview join results without persisting         |
| `--overwrite`           |       | `boolean` | `false` | Overwrite existing joined tables                |
| `--no-auto-process`     |       | `boolean` | `false` | Do not process missing source data collections  |

```bash
# Preview all joins
depictio data join --project-config-path ./config.yaml --preview

# Execute a specific join
depictio data join --project-config-path ./config.yaml --join-name my_join
```

---

#### `data push-images` <small>(v1.12.0+)</small>

Upload a directory of images to S3 storage, for an image data collection. Formerly `images push`, which still works. `depictio ingest` does this itself for a collection that sets `local_images_path`, and checks the upload.

```bash
depictio data push-images <source_directory> <s3_destination> [OPTIONS]
```

The directory structure is kept, relative to the source directory, and images already in storage are skipped unless `--overwrite`. Upload to the collection's `s3_base_folder`: its `image_column` paths are relative to it.

| Parameter          | Short | Type      | Default | Description                                    |
| ------------------ | ----- | --------- | ------- | ---------------------------------------------- |
| `source_directory` |       | `path`    | **required** | Directory holding the images              |
| `s3_destination`   |       | `string`  | **required** | S3 destination, e.g. `s3://bucket/path/to/images/` |
| `--recursive` / `--no-recursive` | `-r` / `-R` | `flag` | `--recursive` | Include subdirectories |
| `--extensions`     | `-e`  | `string`  |         | Comma-separated extensions to upload, e.g. `.png,.jpg` |
| `--dry-run`        | `-n`  | `flag`    | `false` | Show what would be uploaded                    |
| `--overwrite`      |       | `flag`    | `false` | Overwrite existing files in S3                 |
| `--concurrency`    | `-c`  | `int`     | `8`     | Number of parallel uploads                     |
| `--server`         |       | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |

```bash
depictio data push-images ./data/images s3://my-bucket/project/images/ --dry-run
```

---

#### `data versions` { #data-versions }

List the Delta commits of a data collection, with what Depictio recorded on each. The same
history is on the project page, see [Dataset history](../features/versioning.md#dataset-history).

```bash
depictio data versions <data_collection_tag> [OPTIONS]
```

| Parameter               | Type      | Default | Description                                  |
| ----------------------- | --------- | ------- | -------------------------------------------- |
| `data_collection_tag`   | `string`  | **required** | Data collection whose Delta history to list |
| `--server`              | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string`  |         | Project configuration file                   |
| `--limit`               | `int`     | `20`    | Number of commits to show                    |
| `--json`                | `boolean` | `false` | Emit machine-readable JSON                   |

Each row gives the `version`, its `timestamp` and Delta `operation`, then what Depictio
recorded: the `write_mode`, the `trigger`, `rows_added`, `files_added`, the number of
`runs`, and the `ingestion_run` that wrote it. The command reads the table's commit log on
S3 directly, with the storage settings of the CLI configuration.

Depictio stores that record on the commit itself, under `depictio.` keys:
`data_collection_id`, `data_collection_tag` and `write_mode` always, and when known
`ingestion_run_id`, `project_id`, `trigger`, `cli_version`, `user_email`, `file_count`,
`row_count`, `run_count` and `run_tags` (the first 50).

```bash
depictio data versions my_table --project-config-path ./config.yaml --limit 5
```

---

#### `data vacuum` { #data-vacuum }

Remove the Delta files that no retained commit needs. Every ingestion leaves the previous
commit's files behind, so a table's footprint on S3 grows until it is vacuumed, and
nothing in Depictio vacuums on its own.

```bash
depictio data vacuum <data_collection_tag> [OPTIONS]
```

| Parameter               | Type      | Default | Description                                  |
| ----------------------- | --------- | ------- | -------------------------------------------- |
| `data_collection_tag`   | `string`  | **required** | Data collection whose stale Delta files to remove |
| `--server`              | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--project-config-path` | `string`  |         | Project configuration file                   |
| `--retention-hours`     | `int`     | `168`   | Keep the files that commits newer than this need. Going below the default breaks readers that are mid-query |
| `--apply`               | `boolean` | `false` | Delete. Without it, the command only reports what it would remove |

<!-- prettier-ignore -->
!!! warning "Vacuumed commits can no longer be read"
    A commit older than `--retention-hours` loses the files it needs. A
    [dashboard version](../features/versioning.md#data-versions) pinned to it, a preview of
    that version, and **At version** on the project page then have nothing to read.

```bash
# See what would go, then delete it
depictio data vacuum my_table --project-config-path ./config.yaml
depictio data vacuum my_table --project-config-path ./config.yaml --apply
```

### 📈 Dashboard Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio dashboard`"
    All commands in this section are part of the `dashboard` command family. Use them to manage dashboard YAML files: validate, import to server, and export from server.

Manage dashboard YAML files for the [Dashboard YAML Management](../features/yaml-sync.md) feature. Each command reaches the server [`--server`](#choosing-a-server) names, or the default one. `--server` replaces the former `-c/--config` and `--api` options, which still work.

| Command    | Description                  | Server Required          |
| ---------- | ---------------------------- | ------------------------ |
| `validate` | Validate a YAML file         | No, used when configured |
| `import`   | Import YAML to server        | Yes (unless `--dry-run`) |
| `export`   | Export dashboard to YAML     | Yes                      |

#### `dashboard validate`

Validate a dashboard YAML file in two passes: schema and domain constraints (always), then the columns and types against the server's data collections. Without `--server`, the second pass uses the default server when one is configured, reports its findings as warnings only, and is skipped when no server is configured.

```bash
depictio dashboard validate <yaml_file> [OPTIONS]
```

| Parameter           | Type      | Default      | Description                                                       |
| ------------------- | --------- | ------------ | ----------------------------------------------------------------- |
| `yaml_file`         | `path`    | **required** | Path to YAML dashboard file                                       |
| `--server`          | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file: the server to check the columns against |
| `--offline`         | `boolean` | `false`      | Skip the server schema check                                      |

For detailed logs, put `-v` before the command: `depictio -v dashboard validate ...`.

```bash
# Schema + domain, then the default server if one is configured
depictio dashboard validate my_dashboard.yaml

# Full validation against the local server
depictio dashboard validate my_dashboard.yaml --server local

# Schema + domain only
depictio dashboard validate my_dashboard.yaml --offline
```

**Example Output (Success):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
  <span style="color: #2e7d32;">✓ Schema + domain OK</span>
  Pass 2: server schema validation
  <span style="color: #2e7d32;">✓ Server schema OK</span>

<span style="color: #2e7d32;">✓ Validation passed</span>
</pre>
</div>

**Example Output (Failure, per-component error table):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
<span style="color: #c62828;">✗ Schema/domain validation failed</span>
                         Validation Errors
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component     ┃ Field     ┃ Message                                            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ pie-chart     │ -         │ Invalid visu_type 'pie' for mode='ui'.             │
│               │           │ Valid values: scatter, line, bar, box, histogram   │
└───────────────┴───────────┴────────────────────────────────────────────────────┘
</pre>
</div>

---

#### `dashboard import`

Import a dashboard YAML file to the server. The project is determined from the `--project` option, else from the YAML `project_tag` field.

```bash
depictio dashboard import <yaml_file> [OPTIONS]
```

| Parameter          | Type      | Default      | Description                                                    |
| ------------------ | --------- | ------------ | -------------------------------------------------------------- |
| `yaml_file`        | `path`    | **required** | Path to YAML dashboard file                                    |
| `--server`         | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file        |
| `--project` / `-p` | `string`  |              | Project ID (overrides `project_tag` in YAML)                   |
| `--overwrite`      | `boolean` | `false`      | Update an existing dashboard with the same title               |
| `--dry-run`        | `boolean` | `false`      | Validate schema + domain only, don't import (no server needed) |
| `--offline`        | `boolean` | `false`      | Skip server schema check (column names not verified)           |

```bash
# Validate locally without server (no config needed)
depictio dashboard import dashboard.yaml --dry-run

# Import to the default server
depictio dashboard import dashboard.yaml

# Import to the server a configuration file describes
depictio dashboard import dashboard.yaml --server ~/.depictio/admin_config.yaml

# Update existing dashboard with same title
depictio dashboard import dashboard.yaml --server local --overwrite

# Override project from YAML
depictio dashboard import dashboard.yaml --project 646b0f3c1e4a2d7f8e5b8c9a
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);"><span style="color: #0097a7;">Validating:</span> <span style="color: #c2185b;">dashboard.yaml</span>
  Checks: schema + domain constraints
<span style="color: #2e7d32;">✓ Validation passed</span>
  Title: Iris Dashboard Demo
  Components: 7
  Project: Iris_Dataset_Project (from YAML project_tag)

• Server: <span>http://127.0.0.1:8058</span> (local server, as no ~/.depictio/CLI.yaml exists; configuration ~/.depictio/local/cli/admin_config.yaml)

<span style="color: #0097a7;">Validating column names against server schema...</span>
<span style="color: #2e7d32;">✓ Server schema OK</span>

<span style="color: #0097a7;">Importing dashboard (project: Iris_Dataset_Project)...</span>
<span style="color: #2e7d32;">✓ Dashboard imported successfully!</span>
  Dashboard ID: 6824cb3b89d2b72169309737
  Title: Iris Dashboard Demo
  Project ID: 650a1b2c3d4e5f6a7b8c9d0e

<span style="color: #0097a7;">View at:</span> <span>http://127.0.0.1:8058/dashboard/6824cb3b89d2b72169309737</span>
</pre>
</div>

---

#### `dashboard export`

Export a dashboard from the server to a YAML file.

```bash
depictio dashboard export <dashboard_id> [OPTIONS]
```

| Parameter         | Type     | Default          | Description             |
| ----------------- | -------- | ---------------- | ----------------------- |
| `dashboard_id`    | `string` | **required**     | Dashboard ID to export  |
| `--server`        | `string` | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--output` / `-o` | `path`   | `dashboard.yaml` | Output file path        |

```bash
# Export to default file
depictio dashboard export 6824cb3b89d2b72169309737

# Export to specific file
depictio dashboard export 6824cb3b89d2b72169309737 --server local -o iris_dashboard.yaml
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">• Server: http://127.0.0.1:8058 (local server, as no ~/.depictio/CLI.yaml exists; configuration ~/.depictio/local/cli/admin_config.yaml)
<span style="color: #0097a7;">Exporting dashboard 6824cb3b89d2b72169309737...</span>
<span style="color: #2e7d32;">✓ Dashboard exported to:</span> <span style="color: #c2185b;">iris_dashboard.yaml</span>
</pre>
</div>

---

For more information about dashboard YAML format and workflows, see [Dashboard YAML Management](../features/yaml-sync.md).

---

### 🗂️ Catalog Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio catalog`"
    Browse the bioinformatics tool→viz catalog by rendering its components on their bundled fixture data. Handy for previewing what a tool produces before wiring it into a dashboard. For the live, hosted version see the [Depictio Tools Catalog](../catalog/index.md).

`depictio catalog list` lists every tool and output with its recipe and render targets, and `depictio catalog info <tool>` shows one tool in detail.

Here a profiler is looked up in the list, then shown in detail:

<div class="asciinema-cast" data-cast="assets/casts/depictio-catalog.cast" data-poster="npt:0:25" data-idle-time-limit="2.5"></div>

#### `catalog preview`

Render a single catalog output on its fixture and serve it on a throwaway localhost server (nothing is written to disk). Pass `--out` to export a portable, self-contained HTML file instead.

```bash
# Serve an ephemeral preview (Ctrl-C to stop)
depictio catalog preview <output-id>

# Export a standalone HTML file instead of serving
depictio catalog preview <output-id> --out preview.html
```

#### `catalog gallery`

Same as `preview`, but renders the whole catalog as a browsable gallery.

```bash
depictio catalog gallery
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--out`, `-o` | `path` | `null` | Export the self-contained HTML here instead of serving it |
| `--port` | `int` | `0` | Port for the ephemeral server (`0` = auto) |
| `--theme`, `-t` | `string` | `light` | Theme: `light` or `dark` |
| `--no-open` | `flag` | `false` | Do not open a browser tab automatically |

---

### 💾 Backup Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio backup`"
    All commands in this section are part of the `backup` command family. Use them to backup and restore MongoDB database and S3 data. **Admin access required.**

Backup and restore system data and configurations. Each command takes [`--server`](#choosing-a-server), formerly `--CLI-config-path`.

#### `backup create`

Create a backup of the MongoDB database.

```bash
depictio backup create [OPTIONS]
```

| Parameter            | Type      | Default | Description                          |
| -------------------- | --------- | ------- | ------------------------------------ |
| `--server`           | `string`  | see [above](#choosing-a-server) | `local`, or a CLI configuration file |
| `--dry-run`          | `boolean` | `false` | Validate without creating backup     |
| `--include-s3-data`  | `boolean` | `false` | Include S3 deltatable data in backup |
| `--s3-backup-prefix` | `string`  | `backup` | Prefix for S3 backup location       |

```bash
depictio backup create --include-s3-data
```

---

#### `backup list`

List available backup files on the server.

```bash
depictio backup list [OPTIONS]
```

```bash
depictio backup list
```

---

#### `backup validate`

Validate a backup file against Pydantic models.

```bash
depictio backup validate <backup_id> [OPTIONS]
```

| Parameter   | Type     | Default      | Description                             |
| ----------- | -------- | ------------ | --------------------------------------- |
| `backup_id` | `string` | **required** | Backup ID to validate (YYYYMMDD_HHMMSS) |

```bash
depictio backup validate 20240115_143052
```

---

#### `backup restore`

Restore data from a backup file. **Warning: destructive operation.**

```bash
depictio backup restore <backup_id> [OPTIONS]
```

| Parameter            | Type      | Default      | Description                                                    |
| -------------------- | --------- | ------------ | -------------------------------------------------------------- |
| `backup_id`          | `string`  | **required** | Backup ID to restore (YYYYMMDD_HHMMSS)                         |
| `--dry-run`          | `boolean` | `false`      | Simulate restore without making changes                        |
| `--collections`      | `string`  |              | Comma-separated list of collections                            |
| `--force`            | `boolean` | `false`      | Skip confirmation prompt                                       |
| `--allow-unverified` | `boolean` | `false`      | Allow restoring a legacy backup without a checksum sidecar. Checksum mismatches are never bypassable |
| `--skip-validation`  | `boolean` | `false`      | Skip the server-side validation gate before restore            |

```bash
depictio backup restore 20240115_143052 --dry-run
```

The validation coverage audit, formerly `backup check-coverage`, is a maintainer tool: `depictio dev backup check-coverage`.

### 🔄 Migrate Commands

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    All migrate operations require administrator privileges on both the source and target instances.

#### `migrate`

Migrate a project from one Depictio instance to another: a non-destructive upsert that never wipes existing data on the target.

```bash
depictio migrate --project <name> [OPTIONS]
```

| Parameter     | Type     | Default                       | Description                                        |
| ------------- | -------- | ----------------------------- | -------------------------------------------------- |
| `--project`   | `string` | **required**                  | Project name to migrate                            |
| `--server`    | `string` | see [above](#choosing-a-server) | Source instance: `local`, or a CLI configuration file. Formerly `--CLI-config-path` |
| `--to-server` | `string` | `~/.depictio/CLI_remote.yaml` | Target instance, given the same way as `--server`. Formerly `--target-config` |
| `--mode`      | `string` | `all`                         | Migration scope: `all`, `metadata`, `dashboard`, `files` |
| `--dry-run`   | `flag`   | `False`                       | Preview changes without writing anything           |
| `--overwrite` | `flag`   | `False`                       | Replace the project on the target if it already exists |

`DEPICTIO_CLI_TOKEN` and `DEPICTIO_CLI_API_BASE_URL` apply to `--server` only.

**Migration modes:**

| Mode        | What is migrated                                  | When to use                                         |
| ----------- | ------------------------------------------------- | --------------------------------------------------- |
| `all`       | MongoDB documents + S3 files                      | First-time full migration                           |
| `metadata`  | MongoDB documents only                            | Both instances share the same S3 storage            |
| `dashboard` | Dashboard documents only                          | Project already exists on remote, updating layouts  |
| `files`     | S3 files only                                     | MongoDB already migrated, syncing data files        |

```bash
# Dry-run first (recommended before any migration)
depictio migrate \
  --project "My Project" \
  --server local \
  --to-server ~/.depictio/CLI_remote.yaml \
  --dry-run

# Full migration (MongoDB + S3)
depictio migrate \
  --project "My Project" \
  --server local \
  --to-server ~/.depictio/CLI_remote.yaml

# Metadata-only (shared S3)
depictio migrate \
  --project "My Project" \
  --server ~/.depictio/CLI_local.yaml \
  --to-server ~/.depictio/CLI_remote.yaml \
  --mode metadata

# Dashboard-only update
depictio migrate \
  --project "My Project" \
  --server ~/.depictio/CLI_local.yaml \
  --to-server ~/.depictio/CLI_remote.yaml \
  --mode dashboard
```

### 🧑‍🍳 Recipe Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio dev recipe`"
    The recipe commands are maintainer tools, in the `dev` group that `depictio --help` leaves out. Use them to discover, inspect, and locally test data transformation recipes before running them in a project. For full recipe documentation, see [Recipes](../usage/projects/recipes.md).

#### `dev recipe list`

List all bundled recipes.

```bash
depictio dev recipe list
```

**Output:**

```
                 Available recipes (327)
╭────────────────────────────────────────────────────────╮
│ Recipe                                                 │
├────────────────────────────────────────────────────────┤
│ adapterremoval/settings.py                             │
│ ampcombi/clusters.py                                   │
│ ampcombi/embedding.py                                  │
│ ampcombi/summary.py                                    │
…
```

---

#### `dev recipe info <name>`

Show recipe details: description, sources, and output schema.

```bash
depictio dev recipe info <recipe_name>
```

| Parameter | Short | Type | Default | Description |
|-----------|-------|------|---------|-------------|
| `recipe_name` | | `string` | **required** | Recipe name (e.g. `nf-core/ampliseq/alpha_diversity.py`) |
| `--version` | `-v` | `string` | | Pipeline version, for a version-specific recipe. Uses the shared recipe when omitted |

```bash
depictio dev recipe info nf-core/ampliseq/alpha_diversity.py
```

**Output:**

```
Recipe: nf-core/ampliseq/alpha_diversity.py
Description: Transform QIIME2 alpha diversity vector to per-sample Faith PD table.

When ampliseq is run with --metadata, QIIME2 embeds metadata columns directly
into the faith_pd_vector/metadata.tsv file (e.g. habitat). This recipe handles
both cases: with and without embedded metadata columns.
                                     Sources (1)
╭──────────┬───────────────────────────────────────────────────────────────┬────────╮
│ Source   │ Location                                                      │ Format │
├──────────┼───────────────────────────────────────────────────────────────┼────────┤
│ faith_pd │ qiime2/diversity/alpha_diversity/faith_pd_vector/metadata.tsv │ tsv    │
╰──────────┴───────────────────────────────────────────────────────────────┴────────╯
    Input schema:
faith_pd (2 columns)
╭──────────┬────────╮
│ Column   │ Type   │
├──────────┼────────┤
│ id       │ String │
│ faith_pd │ String │
╰──────────┴────────╯
   Output schema (2
       columns)
╭──────────┬─────────╮
│ Column   │ Type    │
├──────────┼─────────┤
│ sample   │ String  │
│ faith_pd │ Float64 │
╰──────────┴─────────╯
```

Each source that declares an `input_schema` gets an `Input schema: <source> (N columns)` table before the output schema. A non-empty `OPTIONAL_OUTPUT_SCHEMA` adds an `Optional output schema (N columns)` table.

---

#### `dev recipe run <name>`

Execute a recipe against a local data directory, with its validation checkpoints.

```bash
depictio dev recipe run <recipe_name> [OPTIONS]
```

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `recipe_name` | | **required** | Recipe name (e.g. `nf-core/ampliseq/alpha_diversity.py`) |
| `--data-dir` | `-d` | **required** | Root directory with workflow output files |
| `--version` | `-v` | | Pipeline version, for a version-specific recipe |
| `--output` | `-o` | | Save the result to a Parquet file |
| `--head` | `-n` | `20` | Number of rows to display |

```bash
# Run with validation output
depictio dev recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results

# Save output and show first 5 rows
depictio dev recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results \
  --output alpha_diversity.parquet \
  --head 5
```

## 🛠️ Common Use Cases

### <span style="color: #0dc09d;">:simple-nextflow:</span> Let the pipeline run the CLI for you <small>(v1.10.0+)</small> { #nextflow-trigger }

Everything below is a command someone has to remember. A Nextflow pipeline can
run `depictio ingest` itself when it completes, on the output directory it just wrote:

```bash
depictio config nextflow --install     # once per machine
nextflow run nf-core/ampliseq -profile docker --outdir results
```

See [Nextflow trigger](nextflow-trigger.md) for the setup, custom pipelines,
repeated runs and running the CLI from a container.

### 🚀 Quick Start

=== "Local server"

    ```bash
    # 1. Start a server on this machine
    depictio local up

    # 2. Ingest your results into it
    depictio ingest /path/to/results --server local
    ```

=== "Complete Setup"

    ```bash
    # 1. Validate your project configuration
    depictio config check --project-config-path ./config.yaml

    # 2. Run the complete workflow
    depictio ingest --project-config-path ./config.yaml
    ```

=== "Step by Step"

    ```bash
    # 1. Check the server and its storage
    depictio config check

    # 2. Validate and sync configuration
    depictio config check --project-config-path ./config.yaml
    depictio config sync --project-config-path ./config.yaml

    # 3. Scan and process data
    depictio data scan --project-config-path ./config.yaml
    depictio data process --project-config-path ./config.yaml
    ```

### 🔧 Development Workflow

=== "Testing Changes"

    ```bash
    # Preview changes without execution
    depictio ingest --project-config-path ./config.yaml --dry-run

    # Test with specific workflow
    depictio ingest --project-config-path ./config.yaml --workflow-name test-workflow
    ```

=== "Debugging"

    ```bash
    # DEBUG logs, and carry on past a failed step
    depictio -vv ingest --project-config-path ./config.yaml --continue-on-error

    # Skip problematic steps
    depictio ingest --project-config-path ./config.yaml --skip server-check,s3-check
    ```

### 💾 Backup Operations

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    All backup operations require administrator privileges.

=== "Create Backup"

    ```bash
    # Create database backup
    depictio backup create

    # Include S3 deltatable data
    depictio backup create --include-s3-data
    ```

=== "Restore Backup"

    ```bash
    # List available backups
    depictio backup list

    # Preview restore
    depictio backup restore 20240115_143052 --dry-run

    # Restore specific backup
    depictio backup restore 20240115_143052 --force
    ```

### 📊 Data Management

=== "Rescan Data"

    ```bash
    # Rescan all folders
    depictio data scan --project-config-path ./config.yaml --rescan-folders

    # Sync file updates
    depictio data scan --project-config-path ./config.yaml --sync-files
    ```

=== "Process Updates"

    ```bash
    # Overwrite existing tables
    depictio data process --project-config-path ./config.yaml --overwrite

    # Refresh the whole project, its dashboards kept as edited
    depictio ingest --project-config-path ./config.yaml --update-config
    ```

### 🔄 Project Migration

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    Migration requires administrator privileges on both source and target instances.

=== "First-time Migration"

    ```bash
    # 1. Dry-run to preview what will be migrated
    depictio migrate \
      --project "My Project" \
      --server ~/.depictio/CLI_local.yaml \
      --to-server ~/.depictio/CLI_remote.yaml \
      --dry-run

    # 2. Run full migration (MongoDB docs + S3 files)
    depictio migrate \
      --project "My Project" \
      --server ~/.depictio/CLI_local.yaml \
      --to-server ~/.depictio/CLI_remote.yaml
    ```

=== "Shared S3 Storage"

    ```bash
    # When source and target share the same S3, only migrate MongoDB docs
    depictio migrate \
      --project "My Project" \
      --server ~/.depictio/CLI_local.yaml \
      --to-server ~/.depictio/CLI_remote.yaml \
      --mode metadata
    ```

=== "Dashboard Update"

    ```bash
    # Push updated dashboard layouts to a remote instance
    # (project and data already exist on remote)
    depictio migrate \
      --project "My Project" \
      --server ~/.depictio/CLI_local.yaml \
      --to-server ~/.depictio/CLI_remote.yaml \
      --mode dashboard
    ```

## 📖 Configuration References

- [Minimal YAML Configuration](minimal_config.md)
- [Full Reference Configuration](../usage/projects/reference.md)
