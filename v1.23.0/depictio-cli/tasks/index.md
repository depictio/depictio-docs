# Common tasks

One command per task. Every option is in the [Command reference](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md). First [install the CLI](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md) and save your `~/.depictio/CLI.yaml`, or run a [local server](#run-a-server-on-this-machine).

## Get data in

### Ingest a pipeline's results

```
depictio ingest results/
```

Builds a project and its dashboards from a results folder. The template comes from the run's provenance (pipeline name and version); a folder no [template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/index.md) fits gets a dashboard [composed from the catalog](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md). Add `--dry-run` to preview what each data collection finds, without writing.

### Pick the template yourself

```
depictio ingest results/ --template nf-core/ampliseq/latest \
  --var SAMPLESHEET_FILE=samplesheet.tsv
```

```
depictio template compose results/ -o my_template/
depictio ingest results/ --template my_template/
```

```
depictio template export PROJECT_ID -t my-lab/rnaseq-qc/1
depictio ingest other_results/ --template ./my-lab/rnaseq-qc/1
```

`--template` takes a bundled id (pin a version, or `latest`) or a template folder. See [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md). `SAMPLESHEET_FILE` takes a CSV or TSV sheet, or a YAML or JSON list of records, read exactly as the same CSV (v1.22.0+).

### Check a template against a run

```
depictio template check --run results/
```

Lists each template variable and what sets it: the run's params, its outputs, or `--var`; and which rules hold and which conditionals fire for this run. Offline. `--fetch-schema` checks the rules against the release's `nextflow_schema.json`, `--against 3.27.0` what the next release breaks. See [`template check`](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#template-check) (v1.22.0+).

### A pipeline with no template

```
depictio ingest --project-config-path project.yaml
```

```
depictio project-builder results/
```

Describe the data collections in a [project YAML](https://depictio.github.io/depictio-docs/latest/depictio-cli/minimal_config/index.md), or let the [Project Builder](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#project-builder) write a template bundle you then pass to `ingest --template`.

### Data on S3 or behind URLs

```
depictio ingest s3://my-bucket/ampliseq/run42
```

```
depictio manifest from-table samplesheet.csv --base-url s3://my-bucket/run42
depictio ingest --template generic/manifest-tables/1 --manifest manifest.json
```

```
depictio ingest --template ./my-lab/rnaseq-qc/1 \
  --bind samples=s3://my-bucket/run42/*.samples.csv
```

The data stays where it is. `manifest from-table` also reads a YAML or JSON samplesheet (v1.22.0+). See [Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md).

## Keep it up to date

### Add a run, or refresh

```
depictio ingest run2/ --attach-run --project "My study"
```

```
depictio ingest results/ --update-config
```

```
depictio ingest results/ --reset-dashboards
```

Ingesting a project that exists stops with exit code 2. `--attach-run` adds the folder as another run; `--update-config` rescans and rebuilds the tables. Both keep the dashboards as edited in the viewer. Details: [Refreshing a project](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#refreshing-a-project).

### Watch a folder

```
depictio watch results/ --write-mode replace-runs --incremental-write
```

Ingests again whenever files change, rewriting only the runs that moved. Install `depictio[watch]` for file events, or it polls every 5 minutes. To keep it running, use the [systemd unit or container](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#running-a-watcher-as-a-service).

### Let Nextflow ingest its results

```
depictio config nextflow --install
```

Once per machine: every pipeline then ingests its `--outdir` when it completes. See [Nextflow trigger](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/trigger/index.md). To ship it inside an nf-core pipeline instead, use the [Nextflow subworkflow](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/subworkflow/index.md).

## Run locally

### Run a server on this machine

```
depictio local up
depictio ingest results/ --server local
```

Starts a full server without Docker (`pip install "depictio[local]"`) with example dashboards, and opens it. Without a `~/.depictio/CLI.yaml`, every command uses it by default. `local down` stops it. See [Python package](https://depictio.github.io/depictio-docs/latest/installation/local/index.md).

## Dashboards as YAML

### Export, edit, import

```
depictio dashboard export DASHBOARD_ID -o dash.yaml
depictio dashboard validate dash.yaml
depictio dashboard import dash.yaml --overwrite
```

`--overwrite` replaces the dashboard with the same title in the project. Keep the YAML in git and import it on any instance. See [Dashboard YAML](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md).

## Administer

### Back up and restore

```
depictio backup create --include-s3-data
depictio backup list
depictio backup restore 20240115_143052 --dry-run
```

Admins only. Drop `--dry-run` to restore; it asks for confirmation. See [Backup and restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md).

### Move a project to another instance

```
depictio migrate --project "My Project" --to-server ~/.depictio/CLI_remote.yaml --dry-run
```

Copies the project from the default server to the one in `CLI_remote.yaml`, never deleting on the target. Drop `--dry-run` to run it; `--mode metadata` when both share S3. See [Project migration](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/index.md).

## Script it

```
depictio ingest results/ --update-config --result-json result.json
```

`--result-json` writes the project and dashboard links; the [exit code](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#exit-codes) says what happened. On CI, set `DEPICTIO_CLI_TOKEN` and `DEPICTIO_CLI_API_BASE_URL` to keep the token [out of the file](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#environment-variables), or run the [container image](https://depictio.github.io/depictio-docs/latest/installation/cli/#container-image).
