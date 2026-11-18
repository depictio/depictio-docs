# CLI

The `depictio` command, from `pip install depictio`, ingests pipeline results, moves dashboards to and from YAML and runs a local server. `depictio-cli`, its former name, still works.

## Start here

- **Install and configure**

  ______________________________________________________________________

  Install it, and save the file that names your server.

  [Install and configure](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md)

- **Common tasks**

  ______________________________________________________________________

  Ingest, add a run, watch a folder, YAML dashboards, backups: one command each.

  [Common tasks](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/index.md)

- **Command reference**

  ______________________________________________________________________

  Every command and option, from its `--help`.

  [Command reference](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md)

## Top commands

- **`depictio ingest`**

  ______________________________________________________________________

  Results folder in, project and dashboards out.

  [Ingest results](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#ingest-results)

- **`depictio watch`**

  ______________________________________________________________________

  Ingest again whenever the data changes.

  [Watch a folder](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#watch-a-folder)

- **`depictio local up`**

  ______________________________________________________________________

  A complete server on this machine, without Docker.

  [Run locally](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#run-a-server-on-this-machine)

- **`depictio dashboard`**

  ______________________________________________________________________

  Export, validate and import dashboard YAML.

  [Dashboards as YAML](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#dashboards-as-yaml)

- **`depictio template`**

  ______________________________________________________________________

  Pick, compose or export a template.

  [Templates](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#use-a-template)

- **`backup` and `migrate`**

  ______________________________________________________________________

  Back up the server, or move a project to another one.

  [Administer](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/#backup-and-restore)

## Automate

- **Nextflow trigger**

  ______________________________________________________________________

  A pipeline ingests its own results when it completes.

  [Nextflow trigger](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/trigger/index.md)

- **Nextflow subworkflow**

  ______________________________________________________________________

  One task in an nf-core pipeline publishes the run, under Docker, Singularity or Apptainer.

  [Nextflow subworkflow](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/subworkflow/index.md)

- **Minimal project YAML**

  ______________________________________________________________________

  The smallest project file, for a pipeline with no template.

  [Minimal project YAML](https://depictio.github.io/depictio-docs/latest/depictio-cli/minimal_config/index.md)
