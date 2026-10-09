---
title: Bisulfite Methylation
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/methylseq" target="_blank" title="nf-core/methylseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/methylseq/master/docs/images/nf-core-methylseq_logo_dark.png" alt="nf-core/methylseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/methylseq/master/docs/images/nf-core-methylseq_logo_light.png" alt="nf-core/methylseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Bisulfite Methylation</h1>
    <p class="template-subtitle">Bismark alignment and conversion QC, coverage, M-bias per context, the binned methylome with its cohort structure, and a window-level comparison between two groups, next to the pipeline's MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/methylseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/methylseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="2.3.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.3.0" selected>2.3.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The methylseq template follows the Bismark route of an nf-core/methylseq run from
the reads to the windows whose methylation differs between groups:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC, Cutadapt, Bismark and Qualimap panels from the regenerated MultiQC report, the libraries that fail the alignment, duplication or conversion floors, and how deep and how evenly the alignments cover the reference
- :material-dna: **Methylome**: whether the extraction needs a read-position trim, whether each methylome is bimodal, whether the libraries group by the design, and the windows that differ between two groups

The persistent `Sample filters` (the design factor, then the sample id) sit in the
left panel and narrow every tab through the project links, and the collapsed
`Sample sheet` is pinned to the bottom of every child tab.

!!! warning "The MultiQC report must be regenerated"
    methylseq 2.3.0 ships MultiQC 1.13, which writes no parquet, and Depictio
    reads only `multiqc.parquet` (MultiQC 1.31 and later). Re-run MultiQC over
    the run's own tool outputs before ingesting, or the MultiQC tab stays empty:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src <outdir> --dest <outdir>
    ```

!!! info "Bismark route only"
    methylseq also publishes `bismark_hisat/` and `bwameth/` routes. This template
    covers the default `bismark/` route; its file patterns match any
    `bismark_<aligner>` suffix, so the sample ids parse the same way on the
    hisat2 route.

!!! note "The design is a table beside the run"
    The methylseq samplesheet carries no design column, and the template never
    parses one out of sample names. Pass a design table with `METADATA_FILE`:
    without it there is no group to filter or colour by, and the window
    comparison is pruned, leaving the Group comparison tab with only the
    per-library lanes of its collapsed locus section.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/methylseq_results \
      --template nf-core/methylseq/latest \
      --var METADATA_FILE=/path/to/design.tsv \
      --var GENOME=hg38
    ```

    The sample hub reads `input/samplesheet_full.csv` under the data root. The
    variables:

    | Variable | Default | What it does |
    |---|---|---|
    | `METADATA_FILE` | none | Design table (TSV): sample id in a `sample` column or the first column, one column per factor |
    | `METADATA_ID_COL` | first column | The design table's sample-id column |
    | `GROUP_COL` | first factor | The factor the dashboards colour and filter by; the comparison tests it when it has two levels, else the first two-level factor |
    | `GROUP_COL_DISPLAY` | title-cased `GROUP_COL` | Label used in titles |
    | `GENOME` | `hg38` | UCSC assembly of the locus tracks (contig axis and region search) |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/methylseq -r 2.3.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. Without a `METADATA_FILE` the window comparison is pruned, and the
    MultiQC tab stays empty until the report is regenerated as above. See
    [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the samplesheet and the design table, the regenerated MultiQC
report, Bismark's alignment, deduplication, splitting and M-bias reports and its
per-CpG bedGraphs, and Qualimap BamQC. 68 of its 74 tiles carry a `use:` catalog
reference (`bismark/*`, `qualimap/*`, `multiqc/*`), and the two comparison tracks
of the locus view name their `viz_kind` explicitly.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.3.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/methylseq-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then seven child tabs in two groups, read as a
funnel from the reads to the windows whose methylation differs between groups.
Each tab below carries the **same icon and colour the dashboard gives it**, so the
page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Run QC, Coverage |
| Methylome | Bias and context, Methylation levels, Cohort structure, Group comparison |

Each child tab opens with a short intro and a strip of two to four cards, then at
most three open sections; tables, details and the locus view follow, collapsed.
The design is a table beside the run (`METADATA_FILE`), and `GROUP_COL` is the
factor every tab colours and filters by. The persistent *Sample filters* (the
group, then the sample id, both on the sample hub) sit in the left panel and
narrow every tab through the project links; each tab's own filters sit under them.
The *Sample sheet* is pinned, collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Bisulfite methylomes, from read QC to the windows that differ between groups.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/methylseq/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/methylseq/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run's provenance: methylseq 2.3.0 writes no
    `params.json`, so the dialog holds the software versions. *About this
    dashboard* says how the two filter levels work, *The run* lists the samples,
    read pairs, pairs aligned and CpG calls, and *Pipeline* walks the five steps
    from trimming to the binned methylome, each linked to the version of its tool
    and its tab. The findings are live values: they follow the filters. Without a
    design table the windows row and the Manhattan drop out.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the group and the sample id):
        each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples, reads aligned, CpG methylation, the lowest conversion |
        | Findings | Live result rows, then 4 figures, one per Methylome tab: the CpG M-bias curves, the per-CpG methylation density, the library PCA and the Manhattan of the tested windows |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the reads trim, align and deduplicate cleanly in every library?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/methylseq/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/methylseq/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the report regenerated with MultiQC 1.35. Open:
    general statistics, FastQC base quality and the reads Cutadapt kept, then
    Bismark's alignment rates, deduplication, cytosine methylation and M-bias. A
    bisulfite library fails the FastQC sequence content and GC checks by design,
    since conversion turns unmethylated cytosines into thymines. The other FastQC
    panels with the trimmed read lengths, and Bismark's strand alignment with the
    four Qualimap BamQC panels, are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | 3 MultiQC panels |
        | Bisulfite alignment | 4 MultiQC panels |
        | Read quality details (collapsed) | 10 MultiQC panels |
        | Strand and coverage details (collapsed) | 5 MultiQC panels |

=== ":material-check-decagram:{ .mc-teal } Run QC"

    **Data & QC** · *Which libraries fail the alignment, duplication or conversion floors?*

    [![Run QC dashboard](../../images/pipeline-templates/nf-core/methylseq/run_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/run_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Run QC dashboard](../../images/pipeline-templates/nf-core/methylseq/run_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/run_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The read pairs Bismark analysed, followed to those aligned and kept; the worst
    mapping efficiency, which passes at 70% since a bisulfite aligner tops out in
    the seventies; the worst duplication (10% passes) and the worst conversion,
    read as `100 - %CHH`. Then the conversion per library, coloured by group, and
    five run-summary metrics on parallel axes: a library that crosses the others on
    conversion is a bisulfite problem, on alignment and duplication a library
    preparation one. Bismark's three report tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Read pairs analysed`, `CpG methylation` and `Conversion
        efficiency` ranges on `bismark_summary_report`, `Mapping efficiency` on
        `bismark_alignment_summary`, and `Duplication rate` and `Alignments kept
        after deduplication` on `bismark_deduplication_summary`.

        | Section | What it holds |
        |---|---|
        | Run QC at a glance | 4 cards |
        | Conversion per library | *Bisulfite conversion per library* |
        | Library QC profile | 1 advanced visualization |
        | Library detail (collapsed) | *Bismark run summary*, *Alignment summary*, *Deduplication summary* |

=== ":material-chart-line:{ .mc-cyan } Coverage"

    **Data & QC** · *How deep and how evenly do the alignments cover the reference?*

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/methylseq/coverage_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/coverage_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/methylseq/coverage_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/coverage_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Qualimap BamQC on the deduplicated alignments. The mean depth, the share of the
    reference covered at least once, Qualimap's duplicate estimate and the mean
    mapping quality on Bowtie 2's 0 to 42 scale. Mean depth counts the bases at
    zero, so on a shallow run judge the breadth. Then the depth along the
    reference, one lane per library, and side by side the bases at each depth and
    the share of the reference covered at least X deep. The depth threshold in that
    section's bar narrows that section only. The BamQC table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Contig` on `qualimap_coverage_across_reference`; the
        `Depth threshold` range sits in the bar of *Depth distribution*.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | Depth along the reference | 1 advanced visualization |
        | Depth distribution | 2 advanced visualizations, under a filter bar |
        | Coverage detail (collapsed) | *Qualimap BamQC summary* |

=== ":material-chart-bell-curve:{ .mc-pink } Bias and context"

    **Methylome** · *Does the methylation extraction need a read-position trim?*

    [![Bias and context dashboard](../../images/pipeline-templates/nf-core/methylseq/bias_and_context_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/bias_and_context_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Bias and context dashboard](../../images/pipeline-templates/nf-core/methylseq/bias_and_context_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/bias_and_context_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    CpG and CHG methylation, the worst CHH methylation against a 2% line (the 98%
    conversion floor on a mammalian genome) and the methylated calls by context.
    Then one M-bias explorer over the six tables of Bismark's M-bias file; the bar
    of its section picks the context and the read, opens on CpG and narrows the
    explorer only. A CpG curve that has not flattened by the end of the read calls
    for an `--ignore` or `--ignore_r2` trim and a re-extraction. The raw M-bias
    positions and the per-context counts are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Read position` range on `bismark_mbias_all_contexts`;
        `Cytosine context` and `Read` sit in the bar of *M-bias*.

        | Section | What it holds |
        |---|---|
        | Context at a glance | 4 cards |
        | M-bias | 1 advanced visualization, under a filter bar |
        | Context detail (collapsed) | *M-bias, every context and read*, *Methylation by context* |

=== ":material-dna:{ .mc-violet } Methylation levels"

    **Methylome** · *Is each methylome bimodal, and are CpG-dense regions unmethylated?*

    [![Methylation levels dashboard](../../images/pipeline-templates/nf-core/methylseq/methylation_levels_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/methylation_levels_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Methylation levels dashboard](../../images/pipeline-templates/nf-core/methylseq/methylation_levels_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/methylation_levels_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Bismark's per-CpG calls, streamed into 2% buckets per library and into 10 kb
    windows. The share of CpGs at 98 to 100%, the share at 0 to 2%, the median
    window methylation and the median window per CpG-density class. Then the
    per-CpG methylation density, one curve per library, and window methylation by
    CpG-density class. A healthy mammalian methylome is bimodal. The CpG-density
    tertiles stand in for a CpG-island annotation, which nf-core/methylseq does not
    ship. Nothing on this tab is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `CpG density class` and a `Window methylation` range on
        `bismark_binned_methylation`.

        | Section | What it holds |
        |---|---|
        | Levels at a glance | 4 cards |
        | Per-CpG methylation | 1 advanced visualization |
        | CpG density | *Methylation by CpG-density class* |

=== ":material-relation-many-to-many:{ .mc-grape } Cohort structure"

    **Methylome** · *Do the libraries group by the design?*

    [![Cohort structure dashboard](../../images/pipeline-templates/nf-core/methylseq/cohort_structure_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/cohort_structure_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Cohort structure dashboard](../../images/pipeline-templates/nf-core/methylseq/cohort_structure_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/cohort_structure_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The library-by-window matrix read three ways. The libraries placed by the PCA,
    as a ring by group, and the 150 most variable windows ranked by contig. Then
    the PCA coloured by group, where a lasso makes an analysis group, and the
    pairwise Pearson correlation, clustered. The heatmap of the 150 windows is
    collapsed, too tall to open by default. A library that lands with the wrong
    block in all three is a swap, a mislabelled sheet or a conversion failure.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Contig` on `bismark_top_variable_windows`.

        | Section | What it holds |
        |---|---|
        | Cohort at a glance | 2 cards |
        | Library relationships | 2 advanced visualizations |
        | Variable windows (collapsed) | 1 advanced visualization |

=== ":material-scale-balance:{ .mc-red } Group comparison"

    **Methylome** · *Which windows differ in methylation between the two groups?*

    [![Group comparison dashboard](../../images/pipeline-templates/nf-core/methylseq/group_comparison_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/group_comparison_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Group comparison dashboard](../../images/pipeline-templates/nf-core/methylseq/group_comparison_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/methylseq/group_comparison_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Every 10 kb window covered in every library is tested between the two levels
    of the design factor, a t-test on arcsine-transformed proportions with
    Benjamini-Hochberg correction, and called at padj below 0.05 with at least ten
    points of difference. The windows tested and called, the median difference and
    the strongest call. Then the Manhattan of every tested window, and the volcano
    (its View switch draws a QQ plot) beside the spread of the differences. The
    locus view, a navigator with two tracks on its region, and the window table are
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Call`, and `Methylation difference` and `Adjusted p`
        ranges, on `bismark_window_group_compare`.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Along the genome | 1 advanced visualization |
        | Effect and significance | 1 advanced visualization + *How the differences spread* |
        | Methylation at a locus (collapsed) | 3 advanced visualizations: the locus navigator, the binned methylation per library and the group difference on the same region |
        | Window detail (collapsed) | *Tested windows* |

    !!! tip "A window screen, not a DMR caller"
        nf-core/methylseq ships no differential-methylation caller. The unit is a
        10 kb window, not a CpG or a called DMR, and with few libraries a side the
        screen is low-powered by construction: read clusters of windows, not a lone
        hit. Without a design table, or without a factor of exactly two levels, the
        comparison is pruned and only the per-library lanes of the locus section
        remain.

A picked row or point becomes a filter that narrows the other tiles of its
collection and follows the project links to the collections they reach. The
pinned sample sheet selects on `sample_id`; the Bismark, Qualimap and M-bias
tables and the per-library profiles on `sample`; the PCA on `sample_id`; the
tested-window table and the two window tracks on `window_id`; the Manhattan on
`chromosome`. The cohort-level collections (correlation, variable windows,
comparison) hold the libraries as columns or test across them, so the sample
filters do not narrow them; their own tab filters do.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/methylseq, it does not run the pipeline.
Run the pipeline first on the default Bismark route:

```bash
nextflow run nf-core/methylseq -r 2.3.0 \
  --input samplesheet_full.csv \
  --genome GRCh38 \
  -profile docker --outdir results
```

Then place the samplesheet and a design table beside the results, regenerate the
MultiQC report and point Depictio at them:

```bash
mkdir -p results/input && cp samplesheet_full.csv design.tsv results/input/
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/
depictio ingest results/ --template nf-core/methylseq/latest \
  --var METADATA_FILE=results/input/design.tsv
```

See [nf-co.re/methylseq/usage](https://nf-co.re/methylseq/2.3.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, never on the `bismark/` prefix.

```text
<DATA_ROOT>/
├── input/
│   ├── samplesheet_full.csv                   # the hub (required)
│   └── design.tsv                             # METADATA_FILE (optional)
├── pipeline_info/software_versions.yml
├── multiqc/multiqc_data/multiqc.parquet       # written by multiqc_reprocess
├── fastqc/*.zip                               # raw MultiQC inputs
├── trimgalore/*.{txt,zip}
├── bismark/
│   ├── alignments/logs/*_bismark_bt2_PE_report.txt
│   ├── deduplicated/logs/*.deduplication_report.txt
│   ├── methylation_calls/
│   │   ├── splitting_report/*_splitting_report.txt
│   │   ├── mbias/*.M-bias.txt
│   │   └── bedGraph/*.bedGraph.gz             # the methylome and the comparison
│   └── summary/                               # bismark2summary
└── qualimap/<sample>/
    ├── genome_results.txt
    └── raw_data_qualimapReport/*.txt
```

---

## :material-flask-outline: Validation runs

The template was validated on the nf-core AWS megatest of the 2.3.0 release,
`s3://nf-core-awsmegatests/methylseq/results-93bc5811603c287c766a0ff7e03b5b41f4483895/bismark/`,
seven paired-end libraries, and the screenshots above come from that run. Its
design table is vendored under the template's `input/`, built once from the
samplesheet:

```bash
DEST=/tmp/methylseq_test
bash depictio/projects/nf-core/methylseq/2.3.0/download_test_data.sh "$DEST"
mkdir -p "$DEST/input" && cp depictio/projects/nf-core/methylseq/2.3.0/input/sample_metadata.tsv "$DEST/input/"
python -m depictio.dev_scripts.multiqc_reprocess --src "$DEST" --dest "$DEST"
depictio ingest "$DEST" --template nf-core/methylseq/latest \
  --var METADATA_FILE="$DEST/input/sample_metadata.tsv"
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/methylseq](https://nf-co.re/methylseq): official pipeline documentation
- [nf-co.re/methylseq/2.3.0/results](https://nf-co.re/methylseq/2.3.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/methylseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
