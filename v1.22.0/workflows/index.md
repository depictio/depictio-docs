# Workflow managers

A workflow manager can hand each run to Depictio when it ends, so results reach dashboards without a manual `depictio ingest`. Nextflow is supported today.

- **Nextflow**

  ______________________________________________________________________

  Two ways: a trigger on your machine, or a subworkflow shipped inside the pipeline.

  [Nextflow](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/index.md)

- **Any other pipeline**

  ______________________________________________________________________

  Run `depictio ingest` on the results folder once the run ends.

  [Common tasks](https://depictio.github.io/depictio-docs/latest/depictio-cli/tasks/index.md)

- **Pipeline templates**

  ______________________________________________________________________

  What Depictio reads from each supported nf-core pipeline, and its dashboards.

  [Templates](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/index.md)
