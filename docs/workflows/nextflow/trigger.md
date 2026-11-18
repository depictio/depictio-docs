---
title: "Nextflow trigger"
description: "Let a Nextflow pipeline ingest its own results into Depictio when it completes."
---

# <span style="color: #0dc09d;">:simple-nextflow:</span> Nextflow trigger <small>(v1.10.0+)</small>

A `workflow.onComplete` handler, shipped with the CLI, runs `depictio ingest` on a pipeline's output when it finishes. A failed pipeline is never ingested, and a Depictio error only logs a warning: the pipeline's exit status never changes.

!!! tip "From inside the pipeline"
    The trigger needs nothing from the pipeline. To ship Depictio with an nf-core pipeline instead, as one task that leaves a dashboard anyone can reopen, use the [Nextflow subworkflow](subworkflow.md) <small>(v1.22.0+)</small>.

<figure markdown="span">
  [![A pipeline finishes, an onComplete handler runs depictio-cli on the output directory, and Depictio ends up with a project and a dashboard](../images/guides/nextflow-trigger/trigger-flow_light.png#only-light)](../images/guides/nextflow-trigger/trigger-flow_light.png){target=_blank}
  [![A pipeline finishes, an onComplete handler runs depictio-cli on the output directory, and Depictio ends up with a project and a dashboard](../images/guides/nextflow-trigger/trigger-flow_dark.png#only-dark)](../images/guides/nextflow-trigger/trigger-flow_dark.png){target=_blank}
</figure>

## Set it up once

On the machine that runs `nextflow` (on a cluster, the submit node):

```bash
pip install "depictio[multiqc]"     # 1. the CLI
                                    # 2. save your CLI.yaml as ~/.depictio/CLI.yaml
depictio config nextflow --install  # 3. turn the trigger on
depictio config check               #    and check the server answers
```

`--install` copies the handler to `~/.depictio/nextflow.config` and includes it from `~/.nextflow/config` (or `$NXF_HOME/config`). Run it again after upgrading. `--uninstall` removes it; `--default-disabled` makes it opt-in, per run with `--depictio_enabled true`. Without a `CLI.yaml`, the trigger ingests into the [local server](../../installation/local.md).

!!! tip "One run only"
    Skip step 3 and add `-c $(depictio config nextflow)` to `nextflow run`.

## Run your pipeline

```bash
nextflow run nf-core/ampliseq -r 2.16.0 -profile docker --outdir results
```

When it completes, the log ends with a `[depictio]` block and the project and dashboard links. The handler passes the pipeline's `manifest` name and version as `--pipeline-id`, which picks the [bundled template](../../pipeline-templates/nf-core/index.md). Set `--depictio_template` to pin one, `--depictio_data_root` when `--outdir` is not the folder to ingest. The project gets a **Triggered by Nextflow** badge.

## A pipeline with no bundled template

```nextflow
params.depictio_project_config = "${projectDir}/depictio_project.yaml"
params.depictio_dashboard      = "${projectDir}/depictio_dashboard.yaml"
```

The [project YAML](../../usage/projects/guide.md) says what to ingest, the [dashboard YAML](../../features/yaml-sync.md) what to show. Without them, a pipeline with no template stops with exit code 1 in the log: the trigger does not [compose](../../usage/projects/composed-dashboards.md) a dashboard, as `depictio ingest` run by hand does. A runnable example is in [`configs/nextflow/example/`](https://github.com/depictio/depictio/tree/main/depictio/cli/configs/nextflow/example).

<div class="asciinema-cast" data-cast="assets/casts/depictio-nextflow-trigger.cast" data-poster="npt:0:59" data-idle-time-limit="2.5"></div>

## Running it again

The next run of the same pipeline finds its project already there and stops (`exited with code 2`). Choose:

| Add to `nextflow run` | Effect |
| --- | --- |
| `--depictio_project study-B` | A new project for this run |
| `--depictio_attach true` | This run added to the project as another run |
| `--depictio_update true` | The project refreshed at every completion, dashboards kept as edited ([details](../../depictio-cli/usage.md#refreshing-a-project)) |

## On a cluster or in CI

Keep the token out of the file with [`DEPICTIO_CLI_TOKEN`](../../depictio-cli/usage.md#environment-variables). Without Python on the head node, run the CLI image; in `~/.nextflow/config`:

```nextflow title="~/.nextflow/config"
params.depictio_cli_executable = [
    'docker', 'run', '--rm', '--network', 'host',
    '-v', '{DATA_ROOT}:{DATA_ROOT}',
    '-v', "${System.getProperty('user.home')}/.depictio:${System.getProperty('user.home')}/.depictio:ro",
    '-e', 'DEPICTIO_CLI_TOKEN', '-e', 'DEPICTIO_CLI_API_BASE_URL',
    'ghcr.io/depictio/depictio-cli:<version>',
]
```

The handler fills `{DATA_ROOT}`; mount every path at the same place inside. The container has no `CLI.yaml` of its own: set `DEPICTIO_CLI_CONFIG_PATH` or `params.depictio_cli_config`. To ingest as whoever launched the run, set `params.depictio_user` ([provisioning](../../usage/guides/authentication-modes.md#pipeline-provisioning-and-magic-links-v113)).

## Reference

| Parameter | Default | Becomes |
| --- | --- | --- |
| `depictio_enabled` | `true` (`false` with `--default-disabled`) | `false` skips the trigger |
| `depictio_data_root` | `params.outdir` | the folder to ingest |
| `depictio_cli_config` | `$DEPICTIO_CLI_CONFIG_PATH` | `--server` (`local` allowed); unset, the [default server](../../depictio-cli/usage.md#choosing-a-server) |
| `depictio_template` | | `--template` |
| `depictio_project_config` | | `--project-config-path`, wins over the template |
| `depictio_project` | | `--project` |
| `depictio_dashboard` | | `--dashboard`, a path or a list |
| `depictio_attach` | `false` | `--attach-run` |
| `depictio_update` | `false` | `--update-config` |
| `depictio_user` | | `--user` |
| `depictio_cli_executable` | `depictio-cli` | the command, or a list for a container |

Only `depictio_cli_config` and `depictio_cli_executable` belong in `~/.nextflow/config`; set the others per run or in the pipeline's `nextflow.config`.

??? question "Nothing happened"

    Every handler line starts with `[depictio]`, on the console and in `.nextflow.log`.

    | Message | Cause |
    | --- | --- |
    | No `[depictio]` line | The snippet is not included, or `depictio_enabled` is `false` |
    | `Pipeline did not complete successfully` | By design: failed runs are not ingested |
    | `No bundled depictio template matches pipeline` | Set `depictio_project_config`, or pin `depictio_template` |
    | `Could not start the Depictio CLI` | `depictio-cli` is not on the head job's PATH: set `depictio_cli_executable` |
    | `exited with code 2` | The project exists: see [Running it again](#running-it-again) |
    | `exited with code 1` | The ingestion failed; its output is above |
