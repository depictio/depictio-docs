---
title: Nanopore RNA-seq
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/nanoseq" target="_blank" title="nf-core/nanoseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/nanoseq/master/docs/images/nf-core-nanoseq_logo_dark.png" alt="nf-core/nanoseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/nanoseq/master/docs/images/nf-core-nanoseq_logo_light.png" alt="nf-core/nanoseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Nanopore RNA-seq</h1>
    <p class="template-subtitle">Nanopore long-read QC, minimap2 alignment and Bambu gene and transcript quantification, with the DESeq2 and DEXSeq results the pipeline computes on top of them.</p>
    <p class="template-links">
      <a href="https://nf-co.re/nanoseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/nanoseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="3.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.0.0" selected>3.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The nanoseq template follows a Nanopore RNA-seq run from the basecalled reads to
the genes and isoforms that differ between conditions:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC and samtools panels from the reprocessed MultiQC report, NanoStat's length and quality per library with the Nx and quality ladders, and what minimap2 placed with its identity, depth and indel spectrum
- :material-dna: **Expression**: what Bambu counted and whether the libraries group by condition or by preparation, the genes DESeq2 calls between the conditions, and the transcripts DEXSeq finds shifting their share of their gene

The persistent `Sample filters` (condition, library, library preparation,
flow-cell run, source replicate) sit in the left panel, and the template's links
carry a pick to NanoStat, the samtools distributions, the melted Bambu counts and
the MultiQC panels alike. The DESeq2 and DEXSeq results carry no sample column,
so the filters do not narrow them.

!!! warning "nanoseq 3.0.0 writes no MultiQC parquet"
    The release ships MultiQC 1.11, which writes `multiqc_data.json` only, and
    Depictio reads `multiqc.parquet` (MultiQC 1.31 and later). Reprocess the
    run's own tool outputs once before ingesting; the parquet lands in
    `multiqc/multiqc_data/`, where the template looks for it:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src <outdir> --dest <outdir>
    ```

!!! info "The design is a variable"
    nanoseq names every sample `<group>_R<replicate>`, and the template recovers
    only those two fields from the name. The condition and the three
    confounders the dashboard offers beside it (library preparation, source
    replicate, flow-cell run) come from an optional design table passed as
    `METADATA_FILE`. Without it, the condition is the samplesheet group and the
    confounders read `unknown`.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/nanoseq_results \
      --template nf-core/nanoseq/latest
    ```

    The results directory is the only thing you have to pass. The hub of the dashboard
    is the samplesheet the run validated, `pipeline_info/samplesheet.valid.csv`,
    one row per library. To bring your own design, add the table and name the
    factor the run compares:

    ```bash
    depictio ingest /path/to/nanoseq_results \
      --template nf-core/nanoseq/latest \
      --var METADATA_FILE=/path/to/sample_metadata.tsv \
      --var GROUP_COL=condition
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | none | Optional design table (TSV), one row per sample (or samplesheet group), one column per factor |
    | `METADATA_ID_COL` | first column | The design table's id column |
    | `GROUP_COL` | first factor column | The factor carried as `condition`; columns named `protocol`, `source_replicate` and `run_id` feed the three confounder filters |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/nanoseq -r 3.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. The MultiQC reprocess above still applies to a 3.0.0 run. See
    [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the validated samplesheet, the reprocessed MultiQC report,
NanoStat's summaries, the `samtools stats` files of the minimap2 alignments,
Bambu's gene and transcript matrices and the DESeq2 and DEXSeq result tables.
Bambu publishes feature by sample matrices, so catalog recipes melt them into
one row per sample and feature; that is what lets the sample picker reach the
counts. When Bambu's row labels are GTF attribute strings, the recipes extract
the `ENSG` or `ENST` id and promote the biotype to its own filterable column.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="3.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/nanoseq-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in two groups, read as a
funnel from the raw reads to the genes and isoforms that differ between
conditions. Each tab below carries the **same icon and colour the dashboard gives
it**, so the page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Reads, Alignment |
| Expression | Quantification, Gene expression, Isoform usage |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. The persistent *Sample
filters* (condition, library, then the library preparation, flow-cell run and
source replicate) sit in the left panel and narrow every tab with a sample column
through the sample hub. DESeq2 and DEXSeq compare the conditions once over the
whole run: their result tables carry no sample column, so the sample filters do
not narrow the Gene expression tab or the DEXSeq tiles of Isoform usage. The
*Sample sheet*, the library design table, is pinned, collapsed, to the bottom of
every child tab.

=== ":material-compass-outline: Overview"

    *Nanopore long reads, from QC to the genes and isoforms that differ.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/nanoseq/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/nanoseq/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run's provenance: nanoseq writes no `params.json`, so
    the dialog holds the software versions. *About this dashboard* says how the two
    filter levels work, *The run* lists facts read from the data (libraries,
    conditions, library preparations, reads), and *Pipeline* walks the five steps
    from QC to isoforms, each linked to the version of its tool and its tab. The
    findings are live values: they follow the filters. The DESeq2 row counts one
    call per tested annotation entry, as the key figure and the volcano do; the
    Gene expression tab counts the distinct genes.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the condition and the
        library): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: libraries by condition, read length N50, reads placed, DESeq2 calls up and down |
        | Findings | Live result rows, then 4 figures: length against quality per library, the library PCA, the DESeq2 volcano and the DEXSeq volcano |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did every library sequence and align as expected?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/nanoseq/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/nanoseq/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the reprocessed report. Open: general statistics,
    FastQC sequence counts and quality histograms, samtools flagstat and the
    mapped reads per contig. The other FastQC panels, then the samtools
    percentages and XY counts, are collapsed. The NanoStat panels are left out:
    the Reads tab draws the NanoStat summary and its quality ladder from the data,
    and the Alignment tab the samtools summary.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Library`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | 5 MultiQC panels |
        | FastQC details (collapsed) | 6 MultiQC panels |
        | samtools details (collapsed) | 2 MultiQC panels |

=== ":material-waves:{ .mc-cyan } Reads"

    **Data & QC** · *How long and how good are the reads of each library?*

    [![Reads dashboard](../../images/pipeline-templates/nf-core/nanoseq/reads_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/reads_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Reads dashboard](../../images/pipeline-templates/nf-core/nanoseq/reads_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/reads_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    NanoPlot's summary of each library's raw reads. The reads basecalled, the
    median read length N50, the median mean read quality (libraries against Q10,
    failing under Q7) and the median share of reads at Q10 or above. Then mean
    read length against mean quality, one point per library sized by its yield
    (nanoseq publishes no per-read table), with the record of the clicked library
    beside it. The two ladders sit side by side: the Nx ladder recomputed from the
    samtools read-length histogram, N50 marked, and the share of reads above each
    Phred floor, Q10 marked. The NanoStat and per-floor tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Mean read quality at least` floor and a `Read length
        N50` range on `nanostats`.

        | Section | What it holds |
        |---|---|
        | Reads at a glance | 4 cards |
        | Length and quality | 2 advanced visualizations: length against quality and the *Library record* |
        | Ladders | 2 advanced visualizations: the Nx ladder and the reads above each quality floor |
        | Read tables (collapsed) | *NanoStat summary*, *Yield per quality floor* |

=== ":material-chart-bar:{ .mc-indigo } Alignment"

    **Data & QC** · *How much of each library aligned, and how accurately?*

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/nanoseq/alignment_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/alignment_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/nanoseq/alignment_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/alignment_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    minimap2 alignments as `samtools stats` reads them, one summary per library.
    The median share of reads placed, the median per-base identity (100 minus the
    mismatch rate per aligned base), the reads mapped and the supplementary
    alignments, the long-read signal of chimeras. Then the coverage depth
    distribution, one curve per library, and the indel length spectrum beside the
    aligned read lengths. The indel spectrum has no legend, as two curves per
    library pass eight entries: hover a curve for its name. The distributions
    table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Library` picker on `samtools_stats_sections`.

        | Section | What it holds |
        |---|---|
        | Alignment at a glance | 4 cards |
        | Coverage | 1 advanced visualization |
        | Indels and read lengths | 2 advanced visualizations: the indel length spectrum and the aligned read lengths |
        | Alignment table (collapsed) | *Alignment distributions* |

=== ":material-dna:{ .mc-violet } Quantification"

    **Expression** · *Do the libraries group by condition, or by preparation?*

    [![Quantification dashboard](../../images/pipeline-templates/nf-core/nanoseq/quantification_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/quantification_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Quantification dashboard](../../images/pipeline-templates/nf-core/nanoseq/quantification_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/quantification_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Bambu's counts per library. The reads assigned by condition, the median genes
    detected, the median protein-coding share and the median share of the 50 top
    genes. Then the PCA on log CPM over the 500 most variable genes and the
    Spearman correlation heatmap, full width with library ids on both axes. The
    libraries should group by condition; a split by preparation or flow-cell run
    is a confounder. Collapsed: the 100 most variable genes, row-standardised;
    depth against complexity, the libraries by preparation and by flow-cell run
    and the gene expression per library; then the tables.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Gene biotype` and a `log2(CPM + 1)` range on
        `bambu_counts_gene_long`; the biotype also narrows the variable-gene
        heatmap.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Sample structure | 1 advanced visualization (PCA) |
        | Sample correlation | 1 advanced visualization (heatmap) |
        | Most variable genes (collapsed) | 1 advanced visualization (heatmap) |
        | Libraries and counts (collapsed) | 1 advanced visualization (depth against complexity), 2 cards, *Gene expression per library* |
        | Quantification tables (collapsed) | *Per-library readings*, *Correlation matrix*, *Gene counts per library* |

=== ":material-scale-balance:{ .mc-grape } Gene expression"

    **Expression** · *Which genes differ between the two conditions?*

    [![Gene expression dashboard](../../images/pipeline-templates/nf-core/nanoseq/gene_expression_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/gene_expression_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Gene expression dashboard](../../images/pipeline-templates/nf-core/nanoseq/gene_expression_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/gene_expression_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    DESeq2 on Bambu's gene counts, once over the whole run, so the sample filters
    do not narrow this tab. The significant genes, ranked up and down, the median
    log2 fold change of the up calls and of the down calls, each on its own card
    so neither cancels the other, and the strongest significance against the 5%
    FDR. Then one tile with three views of the same rows, switched from its View
    control: the volcano, an MA plot from the mean expression and a QQ plot of the
    raw p-values, without point labels (the labels are Ensembl ids). The twenty
    largest fold changes follow, signed. The 200 best-measured rows are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Adjusted p-value`, `log2 fold change` and `log2 mean
        expression` ranges and `Gene biotype`, all on `deseq2_results`. There is
        no direction filter: it would empty one of the two direction cards.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Volcano | 1 advanced visualization with volcano, MA and QQ views |
        | Largest effects | 1 advanced visualization |
        | Best-measured genes (collapsed) | *Best-measured DESeq2 rows* |

=== ":material-chart-timeline-variant:{ .mc-pink } Isoform usage"

    **Expression** · *Which transcripts change their share of their gene?*

    [![Isoform usage dashboard](../../images/pipeline-templates/nf-core/nanoseq/isoform_usage_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/isoform_usage_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Isoform usage dashboard](../../images/pipeline-templates/nf-core/nanoseq/isoform_usage_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nanoseq/isoform_usage_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    DEXSeq on Bambu's transcript counts: whether a transcript is used more or less
    relative to its gene's other transcripts, once over the whole run. The
    transcripts tested against a 5% gene-level q-value, the median usage gain and
    the median usage loss, each on its own card, and the reads on isoforms by
    condition. Then the change in usage against the gene-level q-value, with a QQ
    view and no MA view (DEXSeq writes no mean intensity), and the per-library
    transcript shares of the top DEXSeq genes, each bar summing to 100% of its
    gene's reads. The transcript expression per library, the isoform structures
    and the tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Gene biotype` and a `log2(CPM + 1)` range on
        `bambu_counts_transcript_long`.

        | Section | What it holds |
        |---|---|
        | Usage at a glance | 4 cards |
        | Usage volcano | 1 advanced visualization with volcano and QQ views |
        | Usage per library | *Transcript usage per library, top DEXSeq genes* |
        | Isoform expression (collapsed) | *Transcript expression per library* |
        | Isoform structures (collapsed) | 1 advanced visualization |
        | Isoform tables (collapsed) | *DEXSeq usage results*, *Transcript counts per library* |

    !!! info "The isoform structures need Bambu's extended annotation"
        The isoform lane view reads `bambu/extended_annotations.gtf`, which a
        quantification-only run does not write; without it the view is dropped.
        nanoseq publishes no splice-junction table, so there is no sashimi view.

Every per-library plot (length against quality, the ladders, the coverage, indel
and read-length curves, the PCA, depth against complexity) and every per-library
table selects on the library, which the sample hub links to every sample-keyed
collection, so a pick narrows the rest of the tab. The length against quality
scatter drives the library record card, which waits for a pick. The DEXSeq usage
table selects on `feature_id`, which narrows the other tiles of `dexseq_results`.
The gene and transcript count tables and the DESeq2 table do not select: their
feature ids link to no other collection.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/nanoseq, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/nanoseq -r 3.0.0 \
  --input samplesheet.csv \
  --protocol cDNA \
  --quantification_method bambu \
  --outdir results -profile docker
```

Then regenerate the MultiQC report as a parquet and point Depictio at the
results:

```bash
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/
depictio ingest results/ --template nf-core/nanoseq/latest
```

DESeq2 and DEXSeq need at least two conditions in the samplesheet; a run with
one condition leaves the Gene expression and Isoform usage tabs empty. See
[nf-co.re/nanoseq/usage](https://nf-co.re/nanoseq/3.0.0/docs/usage) for full
pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so the DESeq2 and DEXSeq tables are found
under `bambu/` or `stringtie2/` alike.

```text
<DATA_ROOT>/
├── pipeline_info/
│   ├── samplesheet.valid.csv            # the hub: one row per library
│   └── software_versions.yml
├── multiqc/multiqc_data/
│   └── multiqc.parquet                  # written by the reprocess step
├── fastqc/*.zip                         # raw MultiQC inputs
├── nanoplot/fastq/<sample>/
│   └── *NanoStats.txt                   # length and quality summary
├── minimap2/samtools_stats/
│   └── *.bam.{stats,flagstat,idxstats}
├── bambu/
│   ├── counts_gene.txt                  # feature x sample matrices
│   ├── counts_transcript.txt
│   ├── extended_annotations.gtf         # optional: isoform lanes
│   ├── deseq2/deseq2.results.txt
│   └── dexseq/dexseq.results.txt
└── input/sample_metadata.tsv            # optional: METADATA_FILE, anywhere you like
```

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 3.0.0 release,
`results-1e60482a2c4621234393a6eef8e9a104309c20ae`: the SG-NEx A549 and K562
cell lines, direct cDNA and cDNA libraries, three replicates each. That run
writes no pycoQC, fusion or variant-calling outputs, so the template reads none.
Its design table is vendored in the template as `input/sample_metadata.tsv`,
and the screenshots above come from that run:

```bash
bash depictio/projects/nf-core/nanoseq/3.0.0/download_test_data.sh /tmp/nanoseq_test
python -m depictio.dev_scripts.multiqc_reprocess --src /tmp/nanoseq_test --dest /tmp/nanoseq_test
mkdir -p /tmp/nanoseq_test/input
cp depictio/projects/nf-core/nanoseq/3.0.0/input/sample_metadata.tsv /tmp/nanoseq_test/input/
depictio ingest /tmp/nanoseq_test --template nf-core/nanoseq/latest \
  --var METADATA_FILE=/tmp/nanoseq_test/input/sample_metadata.tsv
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/nanoseq](https://nf-co.re/nanoseq): official pipeline documentation
- [nf-co.re/nanoseq/3.0.0/results](https://nf-co.re/nanoseq/3.0.0/results): AWS test results
- [Template System Reference](../../usage/projects/templates.md): YAML format, variables, conditionals
- [Recipes](../../usage/projects/recipes.md): how to read, test, and write recipes

---

## :material-account-group-outline: Authorship

<div class="tpl-credits">
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-code-braces"></i> Developers</span>
    <span class="tpl-credit-note">Wrote the template, its recipes and its dashboards.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-eye-check-outline"></i> Reviewers</span>
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it Experimental.</span>
    <span class="tpl-person"><i class="mdi mdi-account-plus-outline"></i> Open</span>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/nanoseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
