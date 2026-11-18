---
icon: material/pipe
title: "Workflow managers"
description: "Get pipeline results into Depictio from the workflow manager that ran them."
---

# :material-pipe: Workflow managers

A workflow manager can hand each run to Depictio when it ends, so results reach dashboards without a manual `depictio ingest`. Nextflow is supported today.

<div class="grid cards" markdown>

-   :simple-nextflow:{ .lg .middle .dp-teal } **Nextflow**

    ---

    Two ways: a trigger on your machine, or a subworkflow shipped inside the pipeline.

    [:octicons-arrow-right-24: Nextflow](nextflow/index.md)

-   :material-console-line:{ .lg .middle .dp-purple } **Any other pipeline**

    ---

    Run `depictio ingest` on the results folder once the run ends.

    [:octicons-arrow-right-24: Common tasks](../depictio-cli/tasks.md)

-   :material-file-cog:{ .lg .middle .dp-blue } **Pipeline templates**

    ---

    What Depictio reads from each supported nf-core pipeline, and its dashboards.

    [:octicons-arrow-right-24: Templates](../pipeline-templates/nf-core/index.md)

</div>
