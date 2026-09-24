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
| [airrflow](airrflow.md) | B and T cell receptor repertoire (AIRR) | 5.1.0 |
| [rnafusion](rnafusion.md) | Gene-fusion detection from RNA-seq | 4.1.3 |
| [rnaseq](rnaseq.md) | Bulk RNA-seq quantification | 3.26.0 |
| [taxprofiler](taxprofiler.md) | Metagenomic taxonomic profiling | 2.0.1 |
| [chipseq](chipseq.md) | Transcription-factor / histone ChIP-seq | 2.1.0 |
| [atacseq](atacseq.md) | Chromatin accessibility (ATAC-seq) | 2.1.2 |
| [cutandrun](cutandrun.md) | CUT&amp;RUN / CUT&amp;Tag chromatin profiling | 3.1 |
| [eager](eager.md) | Ancient DNA authentication and genotyping | 2.4.5 |
| [hic](hic.md) | Chromosome conformation capture (Hi-C) | 2.0.0 |
| [mag](mag.md) | Metagenome assembly and binning | 5.5.0 |
| [methylseq](methylseq.md) | Bisulfite and enzymatic methylation sequencing | 2.3.0 |
| [nanoseq](nanoseq.md) | Nanopore long-read sequencing | 3.0.0 |
| [sarek](sarek.md) | Germline and somatic variant calling | 3.10.0 |
| [scrnaseq](scrnaseq.md) | Single-cell RNA-seq preprocessing | 4.2.0 |
| [riboseq](riboseq.md) | Ribosome profiling | 2.0.0 |
| [smrnaseq](smrnaseq.md) | Small RNA sequencing | 2.4.1 |
| [genomeassembler](genomeassembler.md) | De novo genome assembly | 2.0.0 |
| [mhcquant](mhcquant.md) | Immunopeptidomics | 3.2.0 |
| [demultiplex](demultiplex.md) | Sequencing run demultiplexing | 1.8.0 |
| [rnasplice](rnasplice.md) | Alternative splicing analysis | 1.0.4 |

!!! tip "You do not have to name the template <small>(v1.10.0+)</small>"
    A pipeline can trigger the ingestion itself when it completes, and the
    template is resolved from the pipeline's own name and version. One command
    per machine, then nothing to add to any `nextflow run`:

    ```bash
    depictio-cli config nextflow --install
    ```

    See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).
