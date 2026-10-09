---
title: Small RNA-seq
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/smrnaseq" target="_blank" title="nf-core/smrnaseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/smrnaseq/master/docs/images/nf-core-smrnaseq_logo_dark.png" alt="nf-core/smrnaseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/smrnaseq/master/docs/images/nf-core-smrnaseq_logo_light.png" alt="nf-core/smrnaseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Small RNA-seq</h1>
    <p class="template-subtitle">miRTrace library composition, mirtop miRNA expression and isomiRs, a two-group screen on the design, and miRDeep2 novel precursors, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/smrnaseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/smrnaseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="2.4.1">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.4.1" selected>2.4.1</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The smrnaseq template follows an nf-core/smrnaseq run from trimmed small RNA
libraries to novel miRNA candidates:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, then what each library is made of, how long its reads are and whether it was sequenced deep enough
- :material-scale-balance: **Expression**: which miRNAs each library carries and which vary most, how the libraries relate, and which miRNAs separate two groups
- :material-shape-outline: **Sequences**: how far the reads stray from the reference miRNA sequences, and the precursors miRDeep2 proposes beyond miRBase

The persistent `Sample filters` (the design group, then the sample) sit in the
left panel and narrow every tab.

!!! info "Expression is aggregated from the mirtop isomiR table"
    The template reads miRNA expression from mirtop's joined isomiR table, one
    row per isomiR with a count column per sample, and aggregates it per miRNA.
    CPM is therefore over miRNA-assigned reads. miRTrace publishes no statistics
    table of its own, so its composition, length and complexity views are read
    back from the plot data MultiQC keeps in its parquet.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/smrnaseq_results \
      --template nf-core/smrnaseq/latest \
      --var METADATA_FILE=/path/to/design.tsv \
      --var GENOME=hg38
    ```

    The pipeline samplesheet carries no design column, so the design comes from
    an optional table: `METADATA_FILE`, sample id in the first column (or in a
    column named `sample`), one column per factor, and `GROUP_COL` defaulting to
    the first factor. Without it the design table, the group filters and the
    group splits are dropped and the figures fall back to one colour. `GENOME` (default `hg38`) is the UCSC
    assembly the novel precursors link out to. A run with `--skip_mirdeep` takes
    `--var SKIP_MIRDEEP=true`, one with `--skip_multiqc` takes
    `--var SKIP_MULTIQC=true`.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/smrnaseq -r 2.4.1 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the MultiQC report, the mirtop joined isomiR table, the
miRDeep2 per-sample results and the optional design table. The sample hub, the
per-miRNA summary, the PCA, the heatmap matrix, the isomiR composition and the
miRDeep2 precursors are recipes over those files. 40 of its 58 tiles carry a
`use:` catalog reference, so a tile says where its panel comes from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.4.1" markdown>

--8<-- "pipeline-templates/nf-core/_generated/smrnaseq-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in three groups, read as a
funnel from the libraries to the miRNAs they hold and the new ones they suggest.
Each tab below carries the **same icon and colour the dashboard gives it**, so the
page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Library QC |
| Expression | miRNA Expression, Group Comparison |
| Sequences | isomiRs, Novel miRNAs |

Each child tab opens with a short intro and a strip of cards (four, two on Group
Comparison), then at most three open sections; tables and details follow,
collapsed. The persistent *Sample filters* (the design group, then the sample) sit
in the left panel and narrow every tab; the group filter reads the design table
and is pruned with it. The per-miRNA and per-precursor summaries aggregate over
libraries, so the sample filters do not reach them. The *Sample sheet* section
(the design table and the library summary) is pinned, collapsed, to the bottom of
every child tab.

=== ":material-compass-outline: Overview"

    *Small RNA libraries, from the reads to the miRNAs they hold and the new ones they suggest.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/smrnaseq/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/smrnaseq/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says what the
    dashboard shows and how the two filter levels work, *The run* lists the
    samples, the genome, the miRTrace species, the read length window and the
    miRNAs with reads, and *Pipeline* walks the six steps from trimming to
    discovery, each linked to its settings and its tab. The findings are live
    values: they follow the filters. A run with `SKIP_MIRDEEP` loses the novel
    card, row and figure, and the Key figures keep three cards.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the design group and the
        sample): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples by group, miRNAs detected, reference reads, novel precursors by star-arm reads |
        | Findings | Live result rows, then 4 figures: the top miRNAs by group, the library PCA, the novel precursor plane and the isomiR composition |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the adapter come off and the reads map?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/smrnaseq/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/smrnaseq/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: fastp's filtered reads beside the read length after
    trimming, miRTrace's read QC beside mirtop's isomiR read counts, then
    samtools' mapping rate, the reads Bowtie placed on the genome for miRDeep2.
    Check that the adapter came off and the trimmed reads pile up near 22 nt
    before reading any count. The distinct isomiR sequences, the raw FastQC
    counts and adapter content, fastp's base quality, the post-trim FastQC status
    (the `fastqc-1` panels), the mean isomiR read counts and samtools' alignment
    statistics are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | Read trimming | 2 MultiQC panels |
        | Small RNA QC | 2 MultiQC panels |
        | Genome mapping | 1 MultiQC panel |
        | QC details (collapsed) | 7 MultiQC panels |

=== ":material-test-tube:{ .mc-teal } Library QC"

    **Data & QC** · *Is each library a small RNA library, and a clean one?*

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/smrnaseq/library_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/library_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/smrnaseq/library_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/library_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    miRTrace's view of every library. The median miRNA share on a bar out of 100,
    the median rRNA share, the reads on miRNAs (the deepest libraries ranked) and
    the most miRNAs a library reaches at full depth. Then the read length profile,
    the miRNA window shaded, beside the complexity curves; the composition bars
    (RNA type, read QC outcome, organism clade); and the per-library measures as
    parallel coordinates. A clean small RNA library peaks at 20 to 24 nt and is
    mostly miRNA. Depth against miRNA share, one point per library coloured by its
    main clade, beside the library record, is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Reads on miRNAs`, `miRNAs detected`, `miRNA reads (%)`,
        `rRNA reads (%)`, `tRNA reads (%)` and `miRNAs in the main clade (%)`
        ranges on `samples`.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Read length and complexity | 2 advanced visualizations |
        | RNA composition | 1 advanced visualization |
        | Library profile | 1 advanced visualization |
        | Library detail (collapsed) | 1 advanced visualization + a library record card |

    !!! tip "miRTrace comes through MultiQC"
        miRTrace's numbers are read back from the MultiQC parquet. A run with
        `--skip_multiqc` takes `--var SKIP_MULTIQC=true`: the MultiQC tab goes,
        and so do the miRTrace cards, the length, complexity and composition
        figures, and the miRNA share row on the Overview.

=== ":material-chart-box-outline:{ .mc-cyan } miRNA Expression"

    **Expression** · *Which miRNAs does each library express, and how much?*

    [![miRNA Expression dashboard](../../images/pipeline-templates/nf-core/smrnaseq/mirna_expression_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/mirna_expression_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![miRNA Expression dashboard](../../images/pipeline-templates/nf-core/smrnaseq/mirna_expression_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/mirna_expression_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    mirtop's counts, scaled to counts per million miRNA reads. The miRNAs with
    reads, the miRNA reads by group, the median miRNAs at 10 CPM or more per
    library and the median number of libraries detecting a miRNA. Then the
    clustered heatmap of the most variable miRNAs, where libraries of one group
    should form a block; the twelve most expressed miRNAs as boxes by group, every
    library a dot; and the mean-variance plane beside the record of the picked
    miRNA, linked to miRBase. A pick on the plane narrows the boxes to that miRNA.
    The miRNA table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `miRNA` picker on `mirtop_mirna_counts`, and `Mean
        log2(CPM + 1)` and `Libraries detecting the miRNA` ranges on
        `mirtop_mirna_summary`.

        | Section | What it holds |
        |---|---|
        | Expression at a glance | 4 cards |
        | Top variable miRNAs | 1 advanced visualization |
        | Expression by group | *Expression of the top miRNAs by group* |
        | miRNA detail | 1 advanced visualization + a miRNA record card |
        | miRNA table (collapsed) | *miRNA summary* |

=== ":material-scale-balance:{ .mc-grape } Group Comparison"

    **Expression** · *Which libraries look alike, and which miRNAs separate two groups?*

    [![Group Comparison dashboard](../../images/pipeline-templates/nf-core/smrnaseq/group_comparison_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/group_comparison_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Group Comparison dashboard](../../images/pipeline-templates/nf-core/smrnaseq/group_comparison_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/group_comparison_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Two cards rather than four: the libraries compared, by group, and their miRNA
    depth, the two things to check before trusting a separation. Then the library
    PCA on log2(CPM + 1), coloured by group, where a lasso saves a set of points
    as a group, and the volcano of a Wilcoxon rank-sum test between two groups,
    corrected for multiple testing. The volcano opens on the first two groups of
    the design column and runs at once. It is a screen: the pipeline publishes no
    model-based test, so read the hits as candidates to confirm with edgeR or
    DESeq2.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `miRNAs at 10 CPM or more` range on `samples` and a `First
        principal component` range on `mirtop_sample_pca`, to drop shallow or
        outlying libraries before comparing.

        | Section | What it holds |
        |---|---|
        | Comparison at a glance | 2 cards |
        | Sample relationships | 1 advanced visualization |
        | Two-group test | 1 advanced visualization |

=== ":material-shape-outline:{ .mc-indigo } isomiRs"

    **Sequences** · *How far do the reads stray from the reference sequence?*

    [![isomiRs dashboard](../../images/pipeline-templates/nf-core/smrnaseq/isomirs_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/isomirs_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![isomiRs dashboard](../../images/pipeline-templates/nf-core/smrnaseq/isomirs_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/isomirs_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    mirtop names every read of a miRNA by how it differs from the reference. The
    median share of a library's miRNA reads on the reference sequence, the median
    isomiRs of an expressed miRNA in a library, the miRNA reads by 3' end and the
    reads with a non-templated 3' addition, the added bases ranked. Then the
    isomiR composition of each library, opening on the 3' end with the 5' end,
    the addition and the nucleotide change a switch away, and the landscape of
    isomiR classes over the 40 most expressed miRNAs. The landscape table is
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `isomiR class` on `mirtop_isomir_landscape` and a `Reads on
        the reference (%)` range on `samples`.

        | Section | What it holds |
        |---|---|
        | isomiRs at a glance | 4 cards |
        | isomiR composition | 1 advanced visualization |
        | isomiR landscape | 1 advanced visualization |
        | isomiR table (collapsed) | *isomiR landscape rows* |

=== ":material-star-outline:{ .mc-red } Novel miRNAs"

    **Sequences** · *Which new miRNAs does miRDeep2 propose, and how credible are they?*

    [![Novel miRNAs dashboard](../../images/pipeline-templates/nf-core/smrnaseq/novel_mirnas_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/novel_mirnas_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Novel miRNAs dashboard](../../images/pipeline-templates/nf-core/smrnaseq/novel_mirnas_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/smrnaseq/novel_mirnas_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The novel precursors merged across libraries, by star-arm reads, the median
    libraries reporting one, the median true-positive estimate and every miRDeep2
    call, novel or known. Then miRDeep2's signal-to-noise and known-recovery
    curves by score cutoff, to set the threshold, and the plane of recurrence
    against the true-positive estimate beside the record of the picked precursor,
    linked to the UCSC browser on `GENOME`. The plane reads the estimate rather
    than the raw score, which is unbounded. The precursor table and every
    per-library call are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Libraries reporting it` and `True-positive estimate (%)`
        ranges and `Star-arm reads` on `mirdeep2_novel_precursors`.

        | Section | What it holds |
        |---|---|
        | Discovery at a glance | 4 cards |
        | Score calibration | 2 advanced visualizations |
        | Precursor detail | 1 advanced visualization + a precursor record card |
        | Precursor tables (collapsed) | *Novel precursors*, *Every miRDeep2 call, per library* |

    !!! tip "Dropped with `--skip_mirdeep`"
        A run without miRDeep2 writes no `result_*.csv`. Pass
        `--var SKIP_MIRDEEP=true` and the four miRDeep2 collections are pruned,
        which drops this tab and the novel card, row and figure on the Overview.

Tables select rows and the planes and curves select points: the library summary,
the read-length and complexity curves, the library plane and the PCA on `sample`,
and the design table on its id column; the mean-variance plane, the miRNA summary
and the isomiR landscape rows on `mirna`; the novel-precursor plane and table on
`precursor_id`. A pick narrows the other tiles of its collection and follows the
project links to the collections downstream of it: a miRNA picked on the plane
narrows the per-library counts behind the boxes and the isomiR landscape. Each
record card follows the plane beside it and waits for a pick.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/smrnaseq, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/smrnaseq -r 2.4.1 \
  --input samplesheet.csv \
  --genome GRCh38 --mirtrace_species hsa \
  --three_prime_adapter <adapter> \
  --outdir results -profile docker
```

Then point Depictio at the results, with a design table if you have one:

```bash
depictio ingest results/ --template nf-core/smrnaseq/latest \
  --var METADATA_FILE=design.tsv --var GENOME=hg38
```

See [nf-co.re/smrnaseq/usage](https://nf-co.re/smrnaseq/2.4.1/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── multiqc/multiqc_data/
│   └── multiqc.parquet                          # fastp, FastQC, miRTrace, mirtop, samtools
├── mirna_quant/mirtop/
│   └── joined_samples_mirtop.tsv                # the source of expression and isomiRs
├── result_*.csv                                 # miRDeep2 per sample (optional, --skip_mirdeep)
└── pipeline_info/
    ├── params_*.json
    └── *software*versions*.yml
```

The design table named by `METADATA_FILE` is read from wherever it points; its
id column is `METADATA_ID_COL` (default: the first column) and `GROUP_COL` picks
the factor the figures group on. The mature and hairpin count matrices and the
edgeR QC tables are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 2.4.1 release
(`results-cb0af579b24cb8d5a3accd87b2f14ea93fe04832`, the pipeline's full test
profile, a two-factor design), and the screenshots above come from it. That run
published the miRDeep2 results at the output root, and no mature or hairpin
matrices, which is why the template reads the mirtop joined table. The design
table is not part of the published run: it is vendored with the template under
`input/`. `megatest.yaml` lists the tables-only subset the template needs:

```bash
bash depictio/projects/nf-core/smrnaseq/2.4.1/download_test_data.sh /tmp/smrnaseq_test
mkdir -p /tmp/smrnaseq_test/input
cp depictio/projects/nf-core/smrnaseq/2.4.1/input/sample_metadata.tsv /tmp/smrnaseq_test/input/
depictio ingest /tmp/smrnaseq_test --template nf-core/smrnaseq/latest \
  --var METADATA_FILE=/tmp/smrnaseq_test/input/sample_metadata.tsv --var GENOME=hg19
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/smrnaseq](https://nf-co.re/smrnaseq): official pipeline documentation
- [nf-co.re/smrnaseq/2.4.1/results](https://nf-co.re/smrnaseq/2.4.1/results): AWS test results
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it a Draft.</span>
    <span class="tpl-person"><i class="mdi mdi-account-plus-outline"></i> Open</span>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/smrnaseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
