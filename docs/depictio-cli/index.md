---
title: CLI
icon: material/console
description: The depictio command for ingestion, dashboard YAML, templates and a local server.
---

# :material-console: CLI

The `depictio` command, from `pip install depictio`, ingests pipeline results, moves dashboards to and from YAML and runs a local server. `depictio-cli`, its former name, still works.

## :material-rocket-launch: Start here

<div class="grid cards dp-teal" markdown>

-   :material-download:{ .lg .middle } **Install and configure**

    ---

    Install it, and save the file that names your server.

    [:octicons-arrow-right-24: Install and configure](../installation/cli.md)

-   :material-format-list-checks:{ .lg .middle } **Common tasks**

    ---

    Ingest, add a run, watch a folder, YAML dashboards, backups: one command each.

    [:octicons-arrow-right-24: Common tasks](tasks.md)

-   :material-book-open-variant:{ .lg .middle } **Command reference**

    ---

    Every command and option, from its `--help`.

    [:octicons-arrow-right-24: Command reference](usage.md)

</div>

## :material-console: Top commands

<div class="grid cards" markdown>

-   :material-database-import:{ .lg .middle .dp-purple } **`depictio ingest`**

    ---

    Results folder in, project and dashboards out.

    [:octicons-arrow-right-24: Ingest results](tasks.md#ingest-results)

-   :material-eye-refresh:{ .lg .middle .dp-violet } **`depictio watch`**

    ---

    Ingest again whenever the data changes.

    [:octicons-arrow-right-24: Watch a folder](tasks.md#watch-a-folder)

-   :material-laptop:{ .lg .middle .dp-yellow } **`depictio local up`**

    ---

    A complete server on this machine, without Docker.

    [:octicons-arrow-right-24: Run locally](tasks.md#run-a-server-on-this-machine)

-   :material-file-code:{ .lg .middle .dp-blue } **`depictio dashboard`**

    ---

    Export, validate and import dashboard YAML.

    [:octicons-arrow-right-24: Dashboards as YAML](tasks.md#dashboards-as-yaml)

-   :material-layers-outline:{ .lg .middle .dp-orange } **`depictio template`**

    ---

    Pick, compose or export a template.

    [:octicons-arrow-right-24: Templates](tasks.md#use-a-template)

-   :material-backup-restore:{ .lg .middle .dp-red } **`backup` and `migrate`**

    ---

    Back up the server, or move a project to another one.

    [:octicons-arrow-right-24: Administer](tasks.md#backup-and-restore)

</div>

## :material-cog-sync: Automate

<div class="grid cards" markdown>

-   :simple-nextflow:{ .lg .middle .dp-green } **Nextflow trigger**

    ---

    A pipeline ingests its own results when it completes.

    [:octicons-arrow-right-24: Nextflow trigger](nextflow-trigger.md)

-   :material-file-document-outline:{ .lg .middle .dp-pink } **Minimal project YAML**

    ---

    The smallest project file, for a pipeline with no template.

    [:octicons-arrow-right-24: Minimal project YAML](minimal_config.md)

-   :material-package-variant-closed:{ .lg .middle .dp-orange } **Templates**

    ---

    How a supported pipeline becomes a project and dashboards.

    [:octicons-arrow-right-24: Templates](../usage/projects/templates.md)

</div>
