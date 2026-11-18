---
title: "Nextflow"
description: "Two ways to send a Nextflow run to Depictio: the onComplete trigger, or the depictio/publish subworkflow."
---

# :simple-nextflow: Nextflow

Two ways to turn a Nextflow run into Depictio dashboards. Both pick the run's [pipeline template](../../pipeline-templates/nf-core/index.md) by themselves.

<div class="grid cards" markdown>

-   :material-flag-checkered:{ .lg .middle .dp-teal } **onComplete trigger**

    ---

    For whoever **runs** pipelines: one config line, then every run is pushed to your Depictio server when it ends.

    [:octicons-arrow-right-24: onComplete trigger](trigger.md)

-   :material-package-variant-closed:{ .lg .middle .dp-purple } **Subworkflow** <small>v1.22.0+</small>

    ---

    For whoever **develops** a pipeline: its last step builds a Depictio folder anyone reopens, no server needed.

    [:octicons-arrow-right-24: Subworkflow](subworkflow.md)

</div>

| | onComplete trigger | Subworkflow (`depictio/publish`) |
|---|---|---|
| Set up by | The person running pipelines, once per machine | The pipeline developer, once per pipeline |
| Runs | Outside the pipeline, when it completes | Inside the pipeline, as its last task |
| Needs | A Depictio server and a CLI token | Docker, Podman, Singularity or Apptainer (or conda) |
| Produces | The run as a project on that server | A self-contained folder in `results/depictio/`, or the run sent to an instance |
| Works with | Any pipeline with a template, or your own project YAML | Any nf-core pipeline with a template |
