---
title: nf-core
---

# nf-core Templates

Templates for [nf-core](https://nf-co.re) pipelines. Each template configures a complete Depictio project — data collections, recipes, dashboards, and cross-DC links — from a single `depictio-cli run` command.

| Template | Pipeline | Versions |
|----------|----------|---------- |
| [ampliseq](ampliseq.md) | 16S / ITS / CO1 amplicon sequencing | 2.14.0, 2.16.0, 2.18.0 |
| [viralrecon](viralrecon.md) | Viral assembly and variant calling | 3.0.0 |
| [variantbenchmarking](variantbenchmarking.md) | Variant caller benchmarking against truth sets | 1.4.0 |
| [differentialabundance](differentialabundance.md) | DESeq2 differential expression | 2.0.0 |
| [funcscan](funcscan.md) | Functional screening of assembled contigs | 4.0.0 |

!!! tip "You do not have to name the template <small>(v1.10.0+)</small>"
    A pipeline can trigger the ingestion itself when it completes, and the
    template is resolved from the pipeline's own name and version. One command
    per machine, then nothing to add to any `nextflow run`:

    ```bash
    depictio-cli config nextflow --install
    ```

    See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).
