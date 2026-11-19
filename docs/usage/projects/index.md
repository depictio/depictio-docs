---
title: Projects
icon: material/folder-multiple
description: Configure and manage Depictio projects.
glightbox: true
---

# :material-folder-multiple: Projects

[![A project's life: create, ingest, dashboards, share, then every new run adds a data version that What's new shows on the dashboards](../../images/guides/project-creation/project-lifecycle_light.png#only-light)](../../images/guides/project-creation/project-lifecycle_light.png){target=_blank}
[![A project's life: create, ingest, dashboards, share, then every new run adds a data version that What's new shows on the dashboards](../../images/guides/project-creation/project-lifecycle_dark.png#only-dark)](../../images/guides/project-creation/project-lifecycle_dark.png){target=_blank}

A project holds your data collections, the dashboards built on them, and who may use them. It starts from its data, grows with each new run, and can move to another instance.

## Start a project { #start-a-project }

**New project**, then **Add data**: Depictio reads the files and preselects one of three levels <small>(v1.21.0+)</small>.

<div class="grid cards" markdown>

-   :material-table:{ .lg .middle .dp-teal } **Flat tables**

    ---

    One collection per table file. No workflow, no dashboards yet.

    **Choose this when** you have a few CSV, TSV or Parquet files, or a sample sheet to edit.

    [:octicons-arrow-right-24: Create a project](guide.md#read-levels)

-   :material-sitemap:{ .lg .middle .dp-blue } **Custom workflows**

    ---

    Collections you define in the Project Builder, read from each run folder.

    **Choose this when** the pipeline is your own and no template reads it.

    [:octicons-arrow-right-24: Project Builder](guide.md#project-builder)

-   :material-package-variant:{ .lg .middle .dp-orange } **Pipeline template**

    ---

    A recognised pipeline read with its template, recipes and dashboards included.

    **Choose this when** you ran a supported pipeline, such as an nf-core one.

    [:octicons-arrow-right-24: Templates](templates.md)

-   :material-package-down:{ .lg .middle .dp-purple } **Import a project**

    ---

    An exported or sent project, with its data and dashboards.

    **Choose this when** the project already exists somewhere else.

    [:octicons-arrow-right-24: Project migration](../administration/migrate.md#web-ui)

</div>

## In this section

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle .dp-teal } **[Guide](guide.md)**

    ---

    Create a project, add runs and tables, edit a table, permissions

-   :material-cloud-download-outline:{ .lg .middle .dp-blue } **[Remote data and manifests](remote-data.md)**

    ---

    Read data in place from S3 or a URL, refresh it, share a project as a template

-   :material-package-variant-closed:{ .lg .middle .dp-orange } **[Templates](templates.md)**

    ---

    A supported pipeline's project and dashboards in one command

-   :material-puzzle-outline:{ .lg .middle .dp-yellow } **[Composed dashboards](composed-dashboards.md)**

    ---

    A dashboard built from what the tools catalog recognises, when no template fits

-   :material-code-braces:{ .lg .middle .dp-violet } **[YAML examples](yaml-examples.md)**

    ---

    Annotated project files, from one table to a pipeline with links

-   :material-file-document-outline:{ .lg .middle .dp-violet } **[Full reference](reference.md)**

    ---

    Every field of the project YAML

-   :material-chef-hat:{ .lg .middle .dp-pink } **[Recipes](recipes.md)**

    ---

    Python transforms that turn pipeline outputs into tables

</div>
