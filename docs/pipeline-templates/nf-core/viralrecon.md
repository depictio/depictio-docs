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
    <p class="template-subtitle">Assembly and intrahost/low-frequency variant calling for viral samples — SARS-CoV-2 + other viral genomes via the reference-genomes config.</p>
    <p class="template-links">
      <a href="https://nf-co.re/viralrecon" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/viralrecon" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-reviewed template-banner-badge" data-tooltip="Reviewed — tested, CI passes, and reviewed by the Depictio team or community."><i class="mdi mdi-check-circle-outline"></i> Reviewed</span>
</div>

<div class="tpl-version-pick" data-latest="3.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.0.0" selected>3.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The viralrecon template covers the main outputs of a standard nf-core/viralrecon run:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-bar: **Data & QC**: the MultiQC report, per-sample alignment and consensus QC, and mosdepth coverage per window and per amplicon
- :material-dna: **Variants**: every call with its snpEff effect, its allele frequency and its read support (iVar on Illumina runs)
- :material-virus: **Lineage & Clustering**: Pangolin lineages and Nextclade clades with their QC verdicts, and the samples grouped by the mutations they share

!!! info "Works beyond SARS-CoV-2"
    The pipeline supports any viral genome in nf-core's reference-genomes
    config. This template was validated on SARS-CoV-2 / ARTIC amplicon data,
    but the recipe / dashboard structure carries over to other viruses with
    the same iVar variant-calling + Pangolin / Nextclade lineage layout.

---

## :material-rocket-launch-outline: Quick start

The results directory is the only thing you have to pass. The template's routing variables
(`PLATFORM`, `PROTOCOL`, `VARIANT_CALLER`, and the `SKIP_*` flags) mirror nf-core's own
parameters and are **auto-derived from the run's `params.json`** — so the *same command*
works for an Illumina or a nanopore run:

```bash
depictio ingest /path/to/viralrecon_results \
  --template nf-core/viralrecon/3.0.0
```

A nanopore run (whose `params.json` records `platform: nanopore`) is detected
automatically: the coverage, lineage and clade collections are repointed at the
`artic_minion/` layout, and the run summary is read from the ARTIC summary CSV, so
the Overview keeps its Key figures. The ARTIC route writes no variant long table, so
the variant collections are dropped.

!!! tip "Override the auto-derived values"
    The derivation reads `pipeline_info/params*.json`. Pass `--var NAME=value` to
    override any of it — e.g. `--var PLATFORM=nanopore` when a `DATA_ROOT` aggregates
    mixed-platform runs, or `--var SKIP_PANGOLIN=true` to force-drop a collection. Each
    auto-derived value is logged at resolution time. See the full list and routes in the
    [Reference](#reference).

!!! tip "Or let the pipeline do it <small>(v1.10.0+)</small>"
    Run `depictio config nextflow --install` once on the machine that runs
    `nextflow`. This template reads a folder of `run_*` directories, so write the
    run into one and have the pipeline ingest their parent:

    ```bash
    nextflow run nf-core/viralrecon -r 3.0.0 -profile docker \
      --outdir runs/run_1 --depictio_data_root runs
    ```

    The template is picked from the pipeline's own name and version. See
    [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

!!! tip "Aggregated data collections"
    The viralrecon DCs use `metatype: "Aggregated"`. They are built
    by recipes that fan multiple per-sample files into a single delta
    table via `glob_pattern`. See [Recipes](../../usage/projects/recipes.md#glob_pattern-per-sample-inputs)
    for the underlying mechanism.

---

## :material-book-open-variant: Reference

Recipe DCs fan per-sample files into one delta table via `glob_pattern`. The
`PLATFORM=nanopore` route repoints the coverage, lineage and clade DCs at the
`artic_minion/` layout and drops `variants_long` and the views built on it;
`summary_metrics` stays, read from the ARTIC summary CSV with its share of reads
mapped left empty.

### Direct vs derived data collections

The template exposes two kinds of data collection, and the **Origin** column of the
reference table below flags each one explicitly — so you can tell real measurements
from views at a glance:

| Origin | What it is | Examples |
|---|---|---|
| <span class="gtd-badge gtd-direct">direct</span> | A real pipeline output — scanned straight off disk, or lightly cleaned by a recipe that reads the raw files. This *is* the data. | `variants_long`, `pangolin_lineages`, `nextclade_results`, `mosdepth_amplicon_coverage` |
| <span class="gtd-badge gtd-derived">derived</span> | A *reshape* of one or more direct collections into the exact column layout an advanced visualization needs — a view, not new measurement (its recipe reads another collection via `dc_ref`). | `variant_oncoplot`, `amplicon_coverage_matrix`, `genome_coverage_track`, `classification_sankey`, `mutation_upset`, `variant_pca_matrix` |

Derived collections used to carry a `_canonical` suffix; they were renamed to
say what they *produce* (e.g. `variant_feature_matrix_canonical` →
`variant_pca_matrix`). Each one names its source recipe in the reference table's
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

    <!-- screenshot pending v2 -->

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

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    <!-- screenshot pending v2 -->

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

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    <!-- screenshot pending v2 -->

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

    [![Coverage and depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage and depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    <!-- screenshot pending v2 -->

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

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    <!-- screenshot pending v2 -->

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

    [![Lineage and clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Lineage and clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    <!-- screenshot pending v2 -->

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

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/viralrecon — it does not run the pipeline. Run the pipeline first, using the iVar variant caller the template targets:

```bash
nextflow run nf-core/viralrecon -r 3.0.0 \
  --input samplesheet.csv \
  --platform illumina \
  --protocol amplicon \
  --variant_caller ivar \
  -profile docker
```

Then point Depictio at the results:

```bash
depictio ingest results/ \
  --template nf-core/viralrecon/3.0.0
```

A nanopore/ARTIC run (`nextflow … --platform nanopore`) needs no extra flags —
Depictio reads `platform: nanopore` from the run's `params.json` and switches to the
`artic_minion/` layout automatically.

See [nf-co.re/viralrecon/usage](https://nf-co.re/viralrecon/3.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory containing your viralrecon outputs. This can be a single run's `results/` folder or a parent directory containing multiple runs: Depictio scans recursively. Not all files are required; the template adapts to what's present and to the sequencing platform / caller / skip flags it reads from the run's `params.json` (override any with `--var`).

The tree below shows the **Illumina** layout. On `PLATFORM=nanopore` the coverage,
lineage and clade collections are read from `artic_minion/` instead, and no variant
calls are read.

```text
<DATA_ROOT>/
├── multiqc/
│   ├── multiqc_data/
│   │   └── multiqc.parquet
│   └── summary_variants_metrics_mqc.csv
└── variants/
    └── ivar/                                   # Illumina layout (artic_minion/ on PLATFORM=nanopore)
        ├── consensus/
        │   └── bcftools/
        │       ├── pangolin/*.pangolin.csv     # Pangolin lineage, one file per sample
        │       └── nextclade/*.csv             # Nextclade clade, one file per sample
        ├── variants_long_table.csv             # Illumina variant calls (none read on nanopore)
        └── *.mosdepth.{coverage,heatmap}.tsv   # amplicon / genome coverage
```

---

## :material-flask-outline: Test data

A small test fixture is available for local development without re-running
the full pipeline. The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh)
which fetches a real viralrecon run from nf-core's AWS megatest bucket:

```bash
bash depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh \
  --target /tmp/viralrecon_test
```

This pulls a published run from
`s3://nf-core-awsmegatests/viralrecon/results-395079f1d24dce731ac22e03d7a5e71f110103fc/`
and validates that all expected file patterns are present.

Once the download finishes, run depictio against it:

```bash
depictio ingest /tmp/viralrecon_test/run_1 \
  --template nf-core/viralrecon/3.0.0
```

!!! note "Alternative: run nf-core/viralrecon locally"
    The script can also re-run nf-core/viralrecon end-to-end if you'd
    rather regenerate the fixture from scratch:

    ```bash
    nextflow run nf-core/viralrecon -r 3.0.0 \
      -profile test_illumina,docker \
      --variant_caller ivar \
      --outdir /tmp/viralrecon_test/run_1
    ```

---

## :material-link-variant: Additional resources

- [nf-co.re/viralrecon](https://nf-co.re/viralrecon) — official pipeline documentation
- [nf-co.re/viralrecon/3.0.0/results](https://nf-co.re/viralrecon/3.0.0/results) — AWS test results
- [Template System Reference](../../usage/projects/templates.md) — YAML format, variables, conditionals
- [Recipes](../../usage/projects/recipes.md) — how to read, test, and write recipes

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
