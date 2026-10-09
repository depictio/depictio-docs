---
title: "CUT&RUN / CUT&Tag"
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/cutandrun" target="_blank" title="nf-core/cutandrun on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/cutandrun/master/docs/images/nf-core-cutandrun_logo_dark.png" alt="nf-core/cutandrun">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/cutandrun/master/docs/images/nf-core-cutandrun_logo_light.png" alt="nf-core/cutandrun">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">CUT&amp;RUN / CUT&amp;Tag</h1>
    <p class="template-subtitle">Chromatin profiling from reads to peaks: SEACR and MACS2 over the same fragments, how much the two callers agree, and the consensus peak set each target's replicates reproduce.</p>
    <p class="template-links">
      <a href="https://nf-co.re/cutandrun" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/cutandrun" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="3.2.2">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.2.2" selected>3.2.2</option>
    <option value="3.1">3.1</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The cutandrun template covers the peak-calling chain of a standard run:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report (FastQC, Trim Galore, Bowtie 2 against the target and the spike-in, the deepTools fingerprint), then depth, spike-in scaling, duplication and enrichment per library
- :material-waves: **Chromatin signal**: the nucleosomal fragment ladder, then the SEACR regions, their pile-up and the signal they hold
- :material-scale-balance: **Agreement**: how much SEACR and MACS2 agree, the consensus set each target's replicates reproduce, and both on one genomic region

!!! warning "One MultiQC report per run, chosen by `MULTIQC_REPROCESSED`"
    cutandrun 3.2.2 pins MultiQC 1.19, which writes no parquet, and Depictio
    reads only `multiqc.parquet` (MultiQC 1.31 and later). A run made with a
    newer MultiQC, as the Nextflow trigger runs are, publishes
    `04_reporting/multiqc/multiqc_data/multiqc.parquet` itself, and the template
    binds that one by default. A run on the pinned 1.19 needs its report
    re-generated first:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src DATA_ROOT --dest DATA_ROOT
    ```

    It re-runs the pinned MultiQC 1.35 over the run's own raw tool outputs and
    writes `multiqc/multiqc_data/multiqc.parquet` at the root, next to a
    `REPROCESSED.json` recording both versions; `--dry-run` prints the plan
    first. Ingest such a run with `--var MULTIQC_REPROCESSED=true`, which binds
    the re-generated report instead of the pipeline's. The template never binds
    both: a re-generated report ingested without the variable is not read, and
    the MultiQC tab stays empty.

!!! info "Both callers, or either one"
    Both validation runs called peaks with both callers (`--peakcaller
    seacr,macs2`). SEACR is cutandrun's default and the path the template is
    built on; the MACS2 collections are optional, so a SEACR-only run still
    ingests and the layout drops what is missing; a MACS2-only run drops the SEACR
    tiles the same way. Read **Caller agreement** with care then: with one caller
    the comparison reads as complete disagreement.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/cutandrun_results \
      --template nf-core/cutandrun/latest
    ```

    The results directory is the only thing you have to pass for a run whose own
    MultiQC report is a parquet (MultiQC 1.31 or later): the sample hub is built
    from the run's own `pipeline_info/samplesheet.valid.csv`. For a run aligned to
    another build than hg38, add `--var GENOME=<assembly>`.

=== "A run on the pinned MultiQC 1.19"

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess \
      --src /path/to/cutandrun_results --dest /path/to/cutandrun_results
    depictio ingest /path/to/cutandrun_results \
      --template nf-core/cutandrun/latest \
      --var MULTIQC_REPROCESSED=true
    ```

    The release's own report has no parquet, so it is re-generated first, and the
    variable points the MultiQC collection at the re-generated one.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/cutandrun -r 3.2.2 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the validated samplesheet, the Bowtie 2 logs (target and
spike-in), the SEACR stringent calls, the MACS2 narrow peaks, the per-target
consensus peak counts, the fragment-length histograms and fragment BEDs and the
three deepTools QC tables, on top of the MultiQC parquet. Every collection and
recipe matches on file **name**, so the numbered stage directories cutandrun
publishes are never spelled out. The SEACR scan skips `igv/`, where the pipeline
copies every SEACR bed for its IGV session, so no region is read twice. A caller
that finds nothing for a sample still writes its peak file, at 0 bytes: the ingest
skips it with a warning, and the caller comparison keeps a row with no peaks for
that sample.

cutandrun 3.2.2 still ships no `params.json`, so no variable is set from the run's
parameters. Besides `DATA_ROOT`, `MULTIQC_REPROCESSED` says which MultiQC report
to bind and `GENOME` (default `hg38`) sets the genome axis of the Locus tab.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="3.2.2" markdown>

--8<-- "pipeline-templates/nf-core/_generated/cutandrun-latest.md"

</div>

<div class="tpl-version-block" data-version="3.1" markdown>

--8<-- "pipeline-templates/nf-core/_generated/cutandrun-3.1.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then seven child tabs in three groups, read as a
funnel from the libraries to the peaks a target's replicates reproduce. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Libraries |
| Chromatin signal | Fragments, Peaks |
| Agreement | Caller agreement, Consensus, Locus |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. The persistent *Sample
filters* (target, sample, replicate, role) sit in the left panel and narrow every
tab through the project links. The *Sample sheet* is pinned, collapsed, to the
bottom of every child tab. The template has no grouping variable: `target`, the
samplesheet group, is what every grouped tile reads. The IgG controls are samples
throughout; only the peak collections omit them.

=== ":material-compass-outline: Overview"

    *Chromatin profiling, from fragments to the peaks replicates reproduce.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/cutandrun/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/cutandrun/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters, which for cutandrun 3.2.2 are the
    software versions: the run ships no `params.json`. *About this dashboard* says
    how the two filter levels work, *The run* lists the samples, targets, IgG
    controls and peak callers read from the data, and *Pipeline* walks the six steps
    from trimming to the consensus merge, each linked to its tool versions and its
    tab. The findings are live values: they follow the filters, and a route that
    lacks their data drops them. The Locus tab has no figure here, since it is a
    browser rather than a summary.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (target and sample): each
        narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples, fragment length, peaks, FRiP |
        | Findings | Live result rows, then 4 figures: the fragment-length distribution, the pile-up at the SEACR summits, MACS2 against SEACR per sample and the reproducible share per target |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did reads trim, align and rise above the IgG control?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/cutandrun/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/cutandrun/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: general statistics, FastQC sequence counts and the
    reads kept after trimming, the Bowtie 2 alignments to the target genome beside
    those to the spike-in genome, then the deepTools fingerprint. Percent mapped,
    base quality, GC content, insert sizes and reads per contig are collapsed. A
    re-generated report has no separate spike-in Bowtie 2 module: the import drops
    the spike-in tile, and the target tile, now full width, shows both genomes,
    the spike-in libraries carrying a `.spikein` suffix.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Target alignment rate` and `Spike-in scale factor` ranges
        on `bowtie2_spikein_factors`, carried into the report by a reverse link.

        | Section | What it holds |
        |---|---|
        | QC overview | 3 MultiQC panels |
        | Alignment and spike-in | 2 MultiQC panels (target and spike-in genome) |
        | Enrichment over the control | 1 MultiQC panel (fingerprint) |
        | QC details (collapsed) | 5 MultiQC panels |

=== ":material-flask-outline:{ .mc-cyan } Libraries"

    **Data & QC** · *How deep and duplicated is each library, and is it enriched?*

    [![Libraries dashboard](../../images/pipeline-templates/nf-core/cutandrun/libraries_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/libraries_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Libraries dashboard](../../images/pipeline-templates/nf-core/cutandrun/libraries_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/libraries_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The tables the pipeline publishes beside the report. Read pairs, the spike-in
    scale factor, duplicate reads and the distance from a uniform library. Then the
    scale factor and the duplicate share per library, the fingerprint metrics,
    where targets sit apart from the IgG controls, and the PCA beside the clustered
    correlation matrix of the genome-wide bin counts.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Spike-in scale factor` range on `bowtie2_spikein_factors`
        and a `Coverage concentration` range on `deeptools_fingerprint_metrics`.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Spike-in and duplication | 2 bars |
        | Enrichment over the control | 1 advanced visualization |
        | Sample similarity | 2 advanced visualizations |
        | Depth detail (collapsed) | 2 scatters |
        | Library tables (collapsed) | *Spike-in factors* |

=== ":material-waves:{ .mc-violet } Fragments"

    **Chromatin signal** · *Did the digestion work, and how nucleosomal are the fragments?*

    [![Fragments dashboard](../../images/pipeline-templates/nf-core/cutandrun/fragments_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/fragments_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Fragments dashboard](../../images/pipeline-templates/nf-core/cutandrun/fragments_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/fragments_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The nucleosomal ladder. The median fragment length, the fragments counted, the
    fragments by nucleosome class and the mononucleosome to sub-nucleosome ratio
    per target. Then the fragment-length distribution, one curve per sample with
    the sub-nucleosomal and mononucleosomal windows shaded, beside its cumulative
    twin, and each library split into its four nucleosome classes.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Nucleosome class` on `seacr_fragment_classes` and a
        `Fragment length` range on `seacr_fragment_lengths`.

        | Section | What it holds |
        |---|---|
        | Fragments at a glance | 4 cards |
        | Fragment length | 2 line charts |
        | Nucleosome classes | 1 bar |
        | Fragment tables (collapsed) | *Nucleosome classes* |

=== ":material-chart-bell-curve:{ .mc-indigo } Peaks"

    **Chromatin signal** · *What did each sample call, and how much signal do peaks hold?*

    [![Peaks dashboard](../../images/pipeline-templates/nf-core/cutandrun/peaks_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/peaks_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Peaks dashboard](../../images/pipeline-templates/nf-core/cutandrun/peaks_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/peaks_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    SEACR regions, their width, their coverage per base and the lowest FRiP in
    view. Then the region width beside the mean pile-up on the summits, the
    summit-centred pile-up of each sample's strongest regions, and the fragment
    coverage inside and outside peaks. FRiP is built in base pairs of coverage,
    because SEACR reports no read count. The pile-up tiles need the fragment BEDs
    and drop when a run did not publish them.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Region width`, `Coverage per base` and `Contig` on
        `seacr_peaks`, then `Regions called` and `Median coverage per base` on
        `seacr_peak_summary`.

        | Section | What it holds |
        |---|---|
        | Peaks at a glance | 4 cards |
        | Peak shape | 1 histogram + 1 line chart |
        | Pile-up per region | 1 advanced visualization |
        | Signal in peaks | 1 bar |
        | Peak tables (collapsed) | *SEACR regions*, *MACS2 peaks*, *SEACR summary per sample*, *Signal budget* |

    !!! tip "The pile-up needs the fragment BEDs"
        Both fragment collections are optional. A run or a mirror without the
        `*.frags.cut.bed` files ingests everything else, and the pile-up tiles here,
        the fragment track of the Locus tab and the pile-up figure on the Overview
        drop out.

=== ":material-scale-balance:{ .mc-red } Caller agreement"

    **Agreement** · *Do SEACR and MACS2 call the same peaks on each sample?*

    [![Caller agreement dashboard](../../images/pipeline-templates/nf-core/cutandrun/caller_agreement_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/caller_agreement_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Caller agreement dashboard](../../images/pipeline-templates/nf-core/cutandrun/caller_agreement_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/caller_agreement_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Peaks called by caller, the peak width by caller, the share of one caller's
    peaks the other reproduces and the calls only one caller made. Then MACS2
    against SEACR, one selectable point per sample, beside the calls the other
    caller did not make, and the MACS2 significance along the genome. A sample
    with no MACS2 peaks keeps its row, so it reads as disagreement rather than as
    missing data.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` and a `Share reproduced` range, both on
        `caller_agreement`.

        | Section | What it holds |
        |---|---|
        | Agreement at a glance | 4 cards |
        | Caller against caller | 1 scatter + 1 bar |
        | MACS2 along the genome | 1 advanced visualization |
        | Comparison table (collapsed) | *Caller comparison* |

=== ":material-set-merge:{ .mc-grape } Consensus"

    **Agreement** · *Which peaks do a target's replicates reproduce?*

    [![Consensus dashboard](../../images/pipeline-templates/nf-core/cutandrun/consensus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/consensus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Consensus dashboard](../../images/pipeline-templates/nf-core/cutandrun/consensus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/consensus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Consensus intervals by replicate support, the reproducible ones (two
    replicates or more) by target, the interval width and the coverage per
    interval. Then the UpSet of the replicates calling each interval, the
    reproducible share per target and the interval width by support. The
    `Replicate support` filter keeps every value until you narrow it, so the cards
    include single-replicate intervals.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Replicate support`, and `Interval width` and `Member
        peaks` ranges, all on `seacr_consensus_peaks`.

        | Section | What it holds |
        |---|---|
        | Consensus at a glance | 4 cards |
        | Replicate agreement | 1 advanced visualization (UpSet) |
        | How reproducible | 1 bar + 1 histogram |
        | Consensus table (collapsed) | *Consensus intervals* |

=== ":material-dna:{ .mc-teal } Locus"

    **Agreement** · *Do the callers and the replicates agree on one region?*

    [![Locus dashboard](../../images/pipeline-templates/nf-core/cutandrun/locus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/locus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Locus dashboard](../../images/pipeline-templates/nf-core/cutandrun/locus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cutandrun/locus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One region on one genome axis. The cards count what the region in view holds
    and follow it as the tracks do. The SEACR navigator opens on the first contig
    the calls sit on, so a run aligned to part of the genome opens on data: type a
    locus in its header or brush its axis, and the fragment pile-up, the MACS2
    calls and the consensus intervals over the gene lane follow.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `SEACR coverage per base` on `seacr_peaks`, `MACS2 -log10
        q-value` on `macs2_peaks` and `Replicate support` on
        `seacr_consensus_peaks`.

        | Section | What it holds |
        |---|---|
        | Region at a glance | 4 cards |
        | One region, four tracks | 4 advanced visualizations |

    !!! tip "Pass the assembly for a run not on hg38"
        The navigator fetches only the chromosome of its region from the
        assembly it is given, which defaults to `hg38`. For a run aligned to
        another build, pass `--var GENOME=<assembly>` at ingest, or the tracks
        land on the wrong coordinates.

!!! tip "A broad mark reproduces poorly, and the dashboard says so"
    The replicates of a broad histone mark overlap badly, so a large part of its
    consensus intervals rests on a single replicate. That is a property of the
    data, not of the template.

Tables and point views select on their entity column: the sample sheet on
`sample_id`; the per-sample tables (SEACR summary, fragment classes, spike-in
factors, signal budget, caller comparison), the caller, depth and duplication
scatters and the fingerprint tile on `sample`; the peak and consensus tables, the
MACS2 significance track and the SEACR, MACS2 and consensus tracks of the Locus
tab on `peak_id`. A lasso on a scatter, a brush on a track or a picked table row
becomes a dashboard filter that narrows the other tiles of its collection and
follows the project links to the collections they reach. The deepTools PCA emits
a selection, but its collection has no outgoing link, so it narrows no other
tile.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/cutandrun. Run the pipeline first:

```bash
nextflow run nf-core/cutandrun -r 3.2.2 \
  --input samplesheet.csv \
  --genome GRCh38 \
  --peakcaller seacr,macs2 \
  --outdir results -profile docker
```

Then point Depictio at the results. A run on the release's pinned MultiQC 1.19
needs its report re-generated first, and the variable that binds it:

```bash
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/
depictio ingest results/ --template nf-core/cutandrun/latest \
  --var MULTIQC_REPROCESSED=true
```

A run made with MultiQC 1.31 or later skips both: `depictio ingest results/
--template nf-core/cutandrun/latest` reads the report the pipeline published.

See [nf-co.re/cutandrun/usage](https://nf-co.re/cutandrun/3.2.2/docs/usage) for
full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so the stage numbering below is the
reference run's layout, not a requirement.

```text
<DATA_ROOT>/
├── pipeline_info/
│   ├── samplesheet.valid.csv                          # the sample hub is derived from this
│   └── software_versions.yml                          # provenance, with local_versions.yml
├── 01_prealign/
│   ├── pretrim_fastqc/*_fastqc.zip
│   └── trimgalore/{fastqc/*_fastqc.zip,*_trimming_report.txt}
├── 02_alignment/bowtie2/
│   ├── target/log/*.bowtie2.log
│   ├── spikein/log/*.spikein.bowtie2.log
│   └── target/markdup/*.{stats,flagstat,idxstats}
├── 03_peak_calling/
│   ├── 04_called_peaks/
│   │   ├── seacr/*.seacr.peaks.stringent.bed          # required, the default caller
│   │   └── macs2/*.macs2_peaks.narrowPeak             # optional, plus *.macs2_peaks.xls
│   ├── 05_consensus_peaks/*.consensus.peak_counts.bed # *.seacr.consensus.* in 3.2.2
│   └── 06_fragments_from_bams/
│       ├── *.frags.len.txt
│       └── *.frags.cut.bed                            # optional, for the pile-up tiles
├── 04_reporting/
│   ├── deeptools_qc/
│   │   ├── *.plotFingerprint.qcmetrics.txt
│   │   └── all_target_bams.plot{PCA.tab,Correlation.mat.tab}
│   ├── igv/                                           # copies of the SEACR beds, skipped
│   └── multiqc/multiqc_data/multiqc.parquet           # the run's own, MultiQC 1.31 or later
└── multiqc/multiqc_data/
    └── multiqc.parquet                                # or this one, from multiqc_reprocess
```

A tree may hold both MultiQC parquets: the default binds the run's own under
`04_reporting/`, `--var MULTIQC_REPROCESSED=true` the re-generated one at the
root, and the template never loads the two together.

---

## :material-flask-outline: Validation runs

No AWS megatest is usable for 3.2.2: every cutandrun 3.2.x prefix in the bucket
holds directory markers only. The template was validated on two EMBL HPC runs of
the release instead: `cutandrun322-full`, the `test_full` profile (the megatest
design, two histone marks in two replicates each against IgG controls), and
`cutandrun322-small`, the `test_full_small` profile (the same design on a read
subset against one chromosome, with linear duplicate removal and mitochondrial
filtering on). Both runs wrote MultiQC 1.19, so both were re-generated with
`multiqc_reprocess` and checked with `--var MULTIQC_REPROCESSED=true`; the
pipeline's own MultiQC 1.35 report was checked on the small run only. The small
run was ingested on a local stack, its zero-byte peak file included; the full run
was checked by dry runs and by building every collection without a server.

`megatest.yaml` lists the tables-only subset a 3.2.2 megatest would need, so a
usable S3 run can be pinned later without rewriting it. The 3.1 megatest the
previous template version was built on is still fetched by
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/cutandrun/3.1/download_test_data.sh)
next to the 3.1 template:

```bash
bash depictio/projects/nf-core/cutandrun/3.1/download_test_data.sh /tmp/cutandrun_test
python -m depictio.dev_scripts.multiqc_reprocess \
  --src /tmp/cutandrun_test --dest /tmp/cutandrun_test
depictio ingest /tmp/cutandrun_test --template nf-core/cutandrun/3.1
```

The screenshots above show the 3.1 template on an earlier layout of the
dashboard; the 3.2.2 layout has not been captured yet.

---

## :material-link-variant: Additional resources

- [nf-co.re/cutandrun](https://nf-co.re/cutandrun): official pipeline documentation
- [nf-co.re/cutandrun/3.2.2/docs/output](https://nf-co.re/cutandrun/3.2.2/docs/output): the output files the template reads
- [nf-co.re/cutandrun/3.1/results](https://nf-co.re/cutandrun/3.1/results): AWS test results of the 3.1 release (3.2.x has none)
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
    <span class="tpl-credit-note">Keep it working as nf-core/cutandrun releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
