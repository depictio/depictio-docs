# Nextflow

Two ways to turn a Nextflow run into Depictio dashboards. Both pick the run's [pipeline template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/index.md) by themselves.

- **onComplete trigger**

  ______________________________________________________________________

  For whoever **runs** pipelines: one config line, then every run is pushed to your Depictio server when it ends.

  [onComplete trigger](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/trigger/index.md)

- **Subworkflow** v1.22.0+

  ______________________________________________________________________

  For whoever **develops** a pipeline: its last step builds a Depictio folder anyone reopens, no server needed.

  [Subworkflow](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/subworkflow/index.md)

|            | onComplete trigger                                     | Subworkflow (`depictio/publish`)                                               |
| ---------- | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| Set up by  | The person running pipelines, once per machine         | The pipeline developer, once per pipeline                                      |
| Runs       | Outside the pipeline, when it completes                | Inside the pipeline, as its last task                                          |
| Needs      | A Depictio server and a CLI token                      | Docker, Podman, Singularity or Apptainer (or conda)                            |
| Produces   | The run as a project on that server                    | A self-contained folder in `results/depictio/`, or the run sent to an instance |
| Works with | Any pipeline with a template, or your own project YAML | Any nf-core pipeline with a template                                           |
