---
title: Common tasks
description: Short recipes for the depictio CLI, one command each.
---

# :material-format-list-checks: Common tasks

One command per task. Every option is in the [Command reference](usage.md). First [install the CLI](../installation/cli.md) and save your `~/.depictio/CLI.yaml`, or run a [local server](#run-a-server-on-this-machine).

## Get data in

### Ingest a pipeline's results { #ingest-results }

```bash
depictio ingest results/
```

Builds a project and its dashboards from a results folder. The template comes from the run's provenance (pipeline name and version); a folder no [template](../pipeline-templates/nf-core/index.md) fits gets a dashboard [composed from the catalog](../usage/projects/composed-dashboards.md). Add `--dry-run` to preview what each data collection finds, without writing.

<div class="asciinema-cast" data-cast="assets/casts/depictio-ingest-detect.cast" data-poster="npt:0:51" data-idle-time-limit="2.5"></div>

### Pick the template yourself { #use-a-template }

=== "Bundled template"

    ```bash
    depictio ingest results/ --template nf-core/ampliseq/latest \
      --var SAMPLESHEET_FILE=samplesheet.tsv
    ```

=== "Composed, then edited"

    ```bash
    depictio template compose results/ -o my_template/
    depictio ingest results/ --template my_template/
    ```

=== "From an existing project"

    ```bash
    depictio template export PROJECT_ID -t my-lab/rnaseq-qc/1
    depictio ingest other_results/ --template ./my-lab/rnaseq-qc/1
    ```

`--template` takes a bundled id (pin a version, or `latest`) or a template folder. See [Templates](../usage/projects/templates.md).

### A pipeline with no template { #no-template }

=== "Project YAML"

    ```bash
    depictio ingest --project-config-path project.yaml
    ```

=== "In the browser"

    ```bash
    depictio project-builder results/
    ```

Describe the data collections in a [project YAML](minimal_config.md), or let the [Project Builder](../usage/projects/guide.md#project-builder) write a template bundle you then pass to `ingest --template`.

### Data on S3 or behind URLs { #remote-data }

=== "S3 run folder"

    ```bash
    depictio ingest s3://my-bucket/ampliseq/run42
    ```

=== "Manifest"

    ```bash
    depictio manifest from-table samplesheet.csv --base-url s3://my-bucket/run42
    depictio ingest --template generic/manifest-tables/1 --manifest manifest.json
    ```

=== "Bind one collection"

    ```bash
    depictio ingest --template ./my-lab/rnaseq-qc/1 \
      --bind samples=s3://my-bucket/run42/*.samples.csv
    ```

The data stays where it is. See [Remote data and manifests](../usage/projects/remote-data.md).

## Keep it up to date

### Add a run, or refresh { #add-or-refresh-a-run }

=== "Add a run"

    ```bash
    depictio ingest run2/ --attach-run --project "My study"
    ```

=== "Refresh"

    ```bash
    depictio ingest results/ --update-config
    ```

=== "Start dashboards over"

    ```bash
    depictio ingest results/ --reset-dashboards
    ```

Ingesting a project that exists stops with exit code 2. `--attach-run` adds the folder as another run; `--update-config` rescans and rebuilds the tables. Both keep the dashboards as edited in the viewer. Details: [Refreshing a project](usage.md#refreshing-a-project).

<div class="asciinema-cast" data-cast="assets/casts/depictio-ingest-refresh.cast" data-poster="npt:0:48" data-idle-time-limit="2.5"></div>

### Watch a folder { #watch-a-folder }

```bash
depictio watch results/ --write-mode replace-runs --incremental-write
```

Ingests again whenever files change, rewriting only the runs that moved. Install `depictio[watch]` for file events, or it polls every 5 minutes. To keep it running, use the [systemd unit or container](usage.md#running-a-watcher-as-a-service).

<div class="asciinema-cast" data-cast="assets/casts/depictio-watch.cast" data-poster="npt:0:30" data-idle-time-limit="2.5"></div>

### Let Nextflow ingest its results { #nextflow }

```bash
depictio config nextflow --install
```

Once per machine: every pipeline then ingests its `--outdir` when it completes. See [Nextflow trigger](nextflow-trigger.md).

## Run locally

### Run a server on this machine { #run-a-server-on-this-machine }

```bash
depictio local up
depictio ingest results/ --server local
```

Starts a full server without Docker (`pip install "depictio[local]"`) with example dashboards, and opens it. Without a `~/.depictio/CLI.yaml`, every command uses it by default. `local down` stops it. See [Python package](../installation/local.md).

## Dashboards as YAML

### Export, edit, import { #dashboards-as-yaml }

```bash
depictio dashboard export DASHBOARD_ID -o dash.yaml
depictio dashboard validate dash.yaml
depictio dashboard import dash.yaml --overwrite
```

`--overwrite` replaces the dashboard with the same title in the project. Keep the YAML in git and import it on any instance. See [Dashboard YAML](../features/yaml-sync.md).

## Administer

### Back up and restore { #backup-and-restore }

```bash
depictio backup create --include-s3-data
depictio backup list
depictio backup restore 20240115_143052 --dry-run
```

Admins only. Drop `--dry-run` to restore; it asks for confirmation. See [Backup and restore](../usage/administration/backup.md).

### Move a project to another instance { #migrate-a-project }

```bash
depictio migrate --project "My Project" --to-server ~/.depictio/CLI_remote.yaml --dry-run
```

Copies the project from the default server to the one in `CLI_remote.yaml`, never deleting on the target. Drop `--dry-run` to run it; `--mode metadata` when both share S3. See [Project migration](../usage/administration/migrate.md).

## Script it

```bash
depictio ingest results/ --update-config --result-json result.json
```

`--result-json` writes the project and dashboard links; the [exit code](usage.md#exit-codes) says what happened. On CI, set `DEPICTIO_CLI_TOKEN` and `DEPICTIO_CLI_API_BASE_URL` to keep the token [out of the file](usage.md#environment-variables), or run the [container image](../installation/cli.md#container-image).
