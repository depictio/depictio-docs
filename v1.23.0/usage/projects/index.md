# Projects

A project holds your data collections, the dashboards built on them, and who may use them. It starts from its data, grows with each new run, and can move to another instance.

## Start a project

**New project**, then **Add data**: Depictio reads the files and preselects one of three levels (v1.21.0+).

- **Flat tables**

  ______________________________________________________________________

  One collection per table file. No workflow, no dashboards yet.

  **Choose this when** you have a few CSV, TSV or Parquet files, or a sample sheet to edit.

  [Create a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#read-levels)

- **Custom workflows**

  ______________________________________________________________________

  Collections you define in the Project Builder, read from each run folder.

  **Choose this when** the pipeline is your own and no template reads it.

  [Project Builder](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#project-builder)

- **Pipeline template**

  ______________________________________________________________________

  A recognised pipeline read with its template, recipes and dashboards included.

  **Choose this when** you ran a supported pipeline, such as an nf-core one.

  [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md)

- **Import a project**

  ______________________________________________________________________

  An exported or sent project, with its data and dashboards.

  **Choose this when** the project already exists somewhere else.

  [Project migration](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/#web-ui)

## In this section

- **[Guide](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md)**

  ______________________________________________________________________

  Create a project, add runs and tables, edit a table, permissions

- **[Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md)**

  ______________________________________________________________________

  Read data in place from S3 or a URL, refresh it, share a project as a template

- **[Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md)**

  ______________________________________________________________________

  A supported pipeline's project and dashboards in one command

- **[Composed dashboards](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md)**

  ______________________________________________________________________

  A dashboard built from what the tools catalog recognises, when no template fits

- **[YAML examples](https://depictio.github.io/depictio-docs/latest/usage/projects/yaml-examples/index.md)**

  ______________________________________________________________________

  Annotated project files, from one table to a pipeline with links

- **[Full reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md)**

  ______________________________________________________________________

  Every field of the project YAML

- **[Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md)**

  ______________________________________________________________________

  Python transforms that turn pipeline outputs into tables
