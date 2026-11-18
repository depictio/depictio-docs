---
title: CLI
icon: material/console
description: The depictio command for ingestion, dashboard YAML, templates and a local server.
---

# :material-console: CLI

The `depictio` command, from `pip install depictio`, ingests pipeline results, moves dashboards to and from YAML and runs a local server. `depictio-cli`, its former name, still works.

## :material-rocket-launch: Set up

<div class="grid cards dp-teal" markdown>

-   :material-download:{ .lg .middle } **Install the CLI**

    ---

    Install it, and tell it which server to use.

    [:octicons-arrow-right-24: CLI installation](../installation/cli.md)

-   :material-file-document-outline:{ .lg .middle } **Minimal YAML config**

    ---

    The smallest project file: one workflow, one table collection.

    [:octicons-arrow-right-24: Minimal config](minimal_config.md)

-   :material-book-open-variant:{ .lg .middle } **Command reference**

    ---

    Every command, with its options and examples.

    [:octicons-arrow-right-24: Usage](usage.md)

</div>

## :material-console: Common commands

<div class="grid cards" markdown>

-   :material-database-import:{ .lg .middle .dp-purple } **`depictio ingest`**

    ---

    Ingest pipeline results into a Depictio server.

    [:octicons-arrow-right-24: Ingest](usage.md#ingest-command)

-   :material-eye-refresh:{ .lg .middle .dp-violet } **`depictio watch`**

    ---

    Run `ingest` again whenever the data changes.

    [:octicons-arrow-right-24: Watch](usage.md#watch-command)

-   :material-laptop:{ .lg .middle .dp-yellow } **`depictio local`**

    ---

    Run a complete Depictio server on this machine, without Docker.

    [:octicons-arrow-right-24: Python package](../installation/local.md)

-   :material-file-code:{ .lg .middle .dp-blue } **`depictio dashboard`**

    ---

    Validate, import and export dashboard YAML files.

    [:octicons-arrow-right-24: Dashboard commands](usage.md#dashboard-commands)

-   :material-layers-outline:{ .lg .middle .dp-orange } **`depictio template`**

    ---

    Export a project as a template, or compose one from results.

    [:octicons-arrow-right-24: Template commands](usage.md#template-commands)

-   :material-backup-restore:{ .lg .middle .dp-red } **`backup` and `migrate`**

    ---

    Back up the server database, or move projects between instances.

    [:octicons-arrow-right-24: Backup commands](usage.md#backup-commands)

</div>

## :material-cog-sync: Automate

<div class="grid cards" markdown>

-   :simple-nextflow:{ .lg .middle .dp-green } **Nextflow trigger**

    ---

    Let a pipeline ingest its own results when it completes.

    [:octicons-arrow-right-24: Nextflow trigger](nextflow-trigger.md)

-   :material-chef-hat:{ .lg .middle .dp-pink } **Recipes**

    ---

    Python transforms that turn pipeline outputs into tables.

    [:octicons-arrow-right-24: Recipes](../usage/projects/recipes.md)

-   :material-package-variant-closed:{ .lg .middle .dp-orange } **Templates**

    ---

    A supported pipeline's project and dashboards in one command.

    [:octicons-arrow-right-24: Templates](../usage/projects/templates.md)

</div>

New to the CLI? Install it, then run `depictio` with no command for a quick start.
