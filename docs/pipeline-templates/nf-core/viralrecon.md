---
title: Viral Genome Reconstruction
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/viralrecon" target="_blank" title="nf-core/viralrecon on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_dark.png" alt="nf-core/viralrecon">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_light.png" alt="nf-core/viralrecon">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Viral Genome Reconstruction</h1>
    <p class="template-subtitle">Amplicon coverage, Pangolin and Nextclade typing, per-sample QC and iVar variant calls for viral genomes, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/viralrecon" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/viralrecon" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-reviewed template-banner-badge" data-tooltip="Reviewed: tested, CI passes, and reviewed by the Depictio team or community."><i class="mdi mdi-check-circle-outline"></i> Reviewed</span>
</div>

<div class="tpl-version-pick" data-latest="3.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.0.0" selected>3.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The viralrecon template follows a standard nf-core/viralrecon amplicon run from
reads to variant calls and lineage, one tab or tab group per step:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-bar: **Data & QC**: the MultiQC report, per-sample alignment and consensus QC, and mosdepth coverage per window and per amplicon
- :material-dna: **Variants**: every call with its snpEff effect, its allele frequency and its read support (iVar on Illumina runs)
- :material-virus: **Lineage & Clustering**: Pangolin lineages and Nextclade clades with their QC verdicts, and the samples grouped by the mutations they share

!!! info "Works beyond SARS-CoV-2"
    The pipeline supports any viral genome in nf-core's reference-genomes
    config. This template was validated on SARS-CoV-2 ARTIC amplicon data, but
    the recipes and dashboard carry over to other viruses with the same iVar
    variant calling and Pangolin and Nextclade typing layout. The dashboard texts
    name no virus, primer scheme or reference.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/runs \
      --template nf-core/viralrecon/latest
    ```

    The results directory is the only thing you have to pass. The template reads a
    `sequencing-runs` layout, so point it at the **parent** of one or more
    `run_*` directories, each holding one viralrecon `--outdir`. Every run found
    there is aggregated into the same collections.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/viralrecon -r 3.0.0 -profile docker \
      --outdir runs/run_1 --depictio_data_root runs
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output, and the template is picked from the pipeline's own name and version.
    Write the run into a `run_*` directory and point `--depictio_data_root` at
    its parent. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

| Variable | Required | What it does |
|---|---|---|
| `DATA_ROOT` | yes | Parent of the `run_*` directories holding the viralrecon output (`multiqc/`, `variants/`). |
| `IS_NANOPORE` | no | Set automatically when the run's `params.json` records `platform: nanopore`. Repoints the coverage and typing collections at the `artic_minion/` layout and drops the Illumina-only collections. |

!!! tip "Override the auto-derived value"
    `IS_NANOPORE` is read from `pipeline_info/params*.json` and logged at
    resolution time. Pass `--var IS_NANOPORE=true` to force the nanopore route,
    for example when a `DATA_ROOT` aggregates runs whose parameters were not
    kept. See the routes in the [Reference](#reference).

!!! tip "Aggregated data collections"
    The viralrecon DCs use `metatype: "Aggregated"`. They are built
    by recipes that fan multiple per-sample files into a single delta
    table via `glob_pattern`. See [Recipes](../../usage/projects/recipes.md#glob_pattern-per-sample-inputs)
    for the underlying mechanism.

---

## :material-book-open-variant: Reference

Recipe DCs fan per-sample files into one delta table via `glob_pattern`. The
`IS_NANOPORE` route repoints the coverage and typing DCs at the `artic_minion/`
layout and drops `variants_long` and the views built on the variant calls, since an
ARTIC run writes no `variants_long_table.csv`. `summary_metrics` stays, read from the
ARTIC summary CSV with its share of reads mapped left empty.

### Direct vs derived data collections

The template exposes two kinds of data collection, and the **Origin** column of the
reference table below flags each one explicitly, so you can tell real measurements
from views at a glance:

| Origin | What it is | Examples |
|---|---|---|
| <span class="gtd-badge gtd-direct">direct</span> | A real pipeline output, scanned straight off disk or lightly cleaned by a recipe that reads the raw files. This *is* the data. | `variants_long`, `pangolin_lineages`, `nextclade_results`, `mosdepth_amplicon_coverage` |
| <span class="gtd-badge gtd-derived">derived</span> | A *reshape* of one or more direct collections into the exact column layout an advanced visualization needs: a view, not new measurement (its recipe reads another collection via `dc_ref`). | `oncoplot_canonical`, `complex_heatmap_canonical`, `coverage_track_canonical`, `sankey_canonical`, `upset_canonical`, `variant_feature_matrix_canonical` |

Each derived collection names its source recipe in the reference table's
*Reads* column.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound to
    pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped, and the rest are re-packed with no empty rows. One
    template therefore covers both the Illumina and nanopore/ARTIC routes without edits.

<div class="tpl-version-block" data-version="3.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/viralrecon-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a funnel
from the reads to the lineage of each consensus genome. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Sample QC, Coverage & Depth |
| Genomes | Variants, Lineage & Clustering |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. The run summary,
`summary_metrics`, is the source of every cross-DC link, so a filter on it reaches
every tab. The persistent *Sample filters* (lineage, then sample id) and *QC
thresholds* (genome at 10x, median depth, reads mapped, variants called) sit in the
left panel and narrow every tab. The *Sample sheet*, the run summary table, is
pinned, collapsed, to the bottom of every child tab.

!!! info "Nanopore (ARTIC) runs"
    A nanopore run keeps the Overview's Key figures, the persistent filters and the
    Sample sheet: the run summary is read from the ARTIC summary CSV, which has every
    column but the share of reads mapped, left empty. Coverage, lineage and clade are
    read from `artic_minion/`. The ARTIC route writes no variant long table, so the
    Variants tab, the PCA and the UpSet drop, and so do the Overview's missense row
    and its allele frequency figure.

=== ":material-compass-outline: Overview"

    *Viral genomes, from reads to variants, consensus and lineage.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/viralrecon/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/viralrecon/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how to move
    through the tabs, *The run* lists the samples, platform and protocol, reference,
    primer scheme and callers, and *Pipeline* walks the six steps from trimming to
    typing, each linked to its parameters and its tab. The findings are live values:
    they follow the filters, and a route that lacks their data drops them.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and *Findings*
        each have a filter bar (sample id and a genome-at-10x range) that narrows
        that section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards on the run summary: samples, median depth, genome at 10x, variants per sample |
        | Findings | Live result rows, then 4 figures: depth against genome at 10x, depth per amplicon, allele frequency along the genome, and the flow from QC verdict to lineage and clade |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did reads trim, align and cover the genome in every sample?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only: general statistics, the samples that failed mapping, fastp
    filtered reads, Bowtie 2 alignments and the mosdepth cumulative coverage open.
    The read and alignment panels and the variant and assembly panels follow,
    collapsed. Its sample filter reads the MultiQC report.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | 5 MultiQC panels |
        | Read & alignment details (collapsed) | 6 MultiQC panels |
        | Variant & assembly details (collapsed) | 7 MultiQC panels |

=== ":material-stethoscope:{ .mc-indigo } Sample QC"

    **Data & QC** · *Did each sample yield a well-covered, trustworthy consensus genome?*

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median **Reads mapped** against the 1,000-read floor, the share of reads
    mapped, the **Median depth** and the **Genome at 10x**. Then median depth against
    genome covered at 10x, one point per sample, beside a record card for the sample
    you pick, the Nextclade substitutions against deletions per consensus genome, and
    the genome covered at 1x and 10x per sample.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · SNPs and indels called on `summary_metrics`, and missing bases
        on `nextclade_results`, all as ranges, plus the sample filters.

        | Section | What it holds |
        |---|---|
        | QC at a glance | 4 cards |
        | Diagnostics | *Median depth against genome covered at 10x* + a sample record card, *Substitutions against deletions (Nextclade)* |
        | Breadth per sample | *Genome covered at 1x and 10x per sample* |

=== ":material-chart-areaspline:{ .mc-teal } Coverage & Depth"

    **Data & QC** · *Where along the genome does each sample lose depth?*

    [![Coverage & Depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage & Depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median depth per 200 bp window, the windows under 10x, the median amplicon
    depth and the amplicons under 10x in at least one sample; 10x is the depth under
    which the consensus masks a position. Then the genome track, one lane per sample,
    the amplicon track and the clustered amplicon heatmap. A run without a primer
    scheme keeps only the window cards and the genome track.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · window depth on `mosdepth_genome_coverage`, and the amplicon
        and amplicon depth on `mosdepth_amplicon_coverage`.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | Along the genome | 1 advanced visualization |
        | Per amplicon | 2 advanced visualizations |
        | Amplicon table (collapsed) | *Depth per sample and amplicon* |

=== ":material-dna:{ .mc-grape } Variants"

    **Genomes** · *Which mutations does each sample carry, and how well supported?*

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The calls by functional class, the distinct mutations, the median allele
    frequency against the 0.75 consensus cut-off and the median read depth. Then the
    allele frequency of every call along the genome, the allele frequency histogram
    beside the read support scatter, and the mutation matrix per sample and gene. The
    per-gene lollipops, the calls per gene and per sample, and the variant table are
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Gene`, `Effect`, `Functional class`, allele frequency and
        read depth on `variants_long`, plus a collapsed *Matrix filter* on the
        mutation type that narrows the mutation matrix only.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Along the genome | 1 advanced visualization |
        | Support | *Allele frequency of the calls*, *Read support per call* |
        | Co-occurrence | 1 advanced visualization (mutation matrix) |
        | Genes and effects (collapsed) | 1 advanced visualization + *Calls per gene*, *Calls per sample* |
        | Variant table (collapsed) | *Variant calls* |

=== ":material-virus:{ .mc-red } Lineage & Clustering"

    **Genomes** · *Which lineage and clade is each sample, and do they agree?*

    [![Lineage & Clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Lineage & Clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The distinct Pangolin lineages, the distinct Nextclade clades, the median
    Nextclade QC score and the median missing bases. Then the flow from Pangolin QC
    verdict to lineage to clade, the PCA of the samples by the mutations they share,
    and the UpSet of the mutations shared across lineages. A lasso on the PCA makes
    an analysis group.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Lineage`, `Clade`, and the Pangolin and Nextclade QC
        verdicts.

        | Section | What it holds |
        |---|---|
        | Typing at a glance | 4 cards |
        | Classification flow | 1 advanced visualization |
        | Variant profiles | 2 advanced visualizations (PCA, UpSet) |
        | Calls per lineage and clade (collapsed) | *Samples per lineage*, *Samples per clade* |
        | Typing tables (collapsed) | *Pangolin lineage calls* + a lineage record card, *Nextclade clade calls* |

Every per-sample table (run summary, amplicon depth, Pangolin, Nextclade, variant
calls) selects rows on `sample`, and the depth against breadth scatter, the Nextclade
scatter, the allele frequency track, the read support scatter and the PCA select points
on it. `summary_metrics` links `sample` to every per-sample collection, so a pick
narrows the rest of the tab. The record cards wait for a pick, and a lasso on the PCA
becomes an analysis group.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/viralrecon, it does not run the
pipeline. Run the pipeline first, using the iVar variant caller the template
targets, and write it into a `run_*` directory:

```bash
nextflow run nf-core/viralrecon -r 3.0.0 \
  --input samplesheet.csv \
  --platform illumina \
  --protocol amplicon \
  --variant_caller ivar \
  --outdir runs/run_1 \
  -profile docker
```

Then point Depictio at the parent of the run directories:

```bash
depictio ingest runs/ \
  --template nf-core/viralrecon/latest
```

A later run written to `runs/run_2` is aggregated into the same collections on
the next ingest. A nanopore ARTIC run (`--platform nanopore`) needs no extra
flag: Depictio reads `platform: nanopore` from the run's `params.json` and sets
`IS_NANOPORE` itself.

See [nf-co.re/viralrecon/usage](https://nf-co.re/viralrecon/3.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the `run_*` directories. Depictio
scans each run recursively and matches on file name. Not all files are
required: optional collections that a run did not write (no Pangolin output
with `--skip_pangolin`, for example) are skipped, and the dashboard hides the
components bound to them.

The tree below shows the **Illumina** layout. On `IS_NANOPORE` the coverage and
typing collections are read from `artic_minion/` instead.

```text
<DATA_ROOT>/
└── run_1/                                        # one viralrecon --outdir per run_* directory
    ├── pipeline_info/params*.json                # read to set IS_NANOPORE
    ├── multiqc/
    │   ├── multiqc_data/
    │   │   └── multiqc.parquet
    │   └── summary_variants_metrics_mqc.csv      # the hub: one row per sample
    └── variants/
        └── ivar/                                 # artic_minion/ on IS_NANOPORE
            ├── consensus/
            │   └── bcftools/
            │       ├── pangolin/*.pangolin.csv   # Pangolin lineage, one file per sample
            │       └── nextclade/*.csv           # Nextclade clade, one file per sample
            ├── variants_long_table.csv           # iVar variant calls
            └── *.mosdepth.{coverage,heatmap}.tsv # amplicon and genome coverage
```

---

## :material-flask-outline: Validation runs

The nf-core AWS megatests do not publish the aggregated files this template
reads (`multiqc.parquet`, `variants_long_table.csv`, the Pangolin and Nextclade
reports, `summary_variants_metrics_mqc.csv`). The repository therefore ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh),
which runs nf-core/viralrecon with its `test_illumina` profile into a
`sequencing-runs` layout (Nextflow 24.10 or later, and Docker or Singularity):

```bash
bash depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh /tmp/viralrecon_test
```

The run lands in `/tmp/viralrecon_test/run_1`, so ingest its parent:

```bash
depictio ingest /tmp/viralrecon_test \
  --template nf-core/viralrecon/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/viralrecon](https://nf-co.re/viralrecon): official pipeline documentation
- [nf-co.re/viralrecon/3.0.0/results](https://nf-co.re/viralrecon/3.0.0/results): AWS test results
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
    <span class="tpl-credit-note">Ran it on real data and signed off on the status above.</span>
    <a class="tpl-person" href="https://github.com/depictio" target="_blank" rel="noopener">
      <img src="https://github.com/depictio.png?size=80" alt="" loading="lazy"> Depictio team
    </a>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/viralrecon releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
