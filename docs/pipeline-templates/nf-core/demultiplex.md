---
title: Demultiplexing QC
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/demultiplex" target="_blank" title="nf-core/demultiplex on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/demultiplex/master/docs/images/nf-core-demultiplex_logo_dark.png" alt="nf-core/demultiplex">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/demultiplex/master/docs/images/nf-core-demultiplex_logo_light.png" alt="nf-core/demultiplex">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Demultiplexing QC</h1>
    <p class="template-subtitle">Sequencing-facility run sign-off: CheckQC verdicts, run health per lane and read, demultiplexing balance, undetermined reads and index swaps, and per-library read QC, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/demultiplex" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/demultiplex" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.8.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="1.8.0" selected>1.8.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The demultiplex template reads an nf-core/demultiplex run in the order a
sequencing facility signs a run off:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: what CheckQC and the Falco and fastp read QC flagged in the MultiQC report, and whether the instrument delivered on every lane, read and cycle
- :material-scale-balance: **Demultiplexing**: how evenly each lane's reads were shared between the libraries, what no index matched and whether it is an index swap, and which libraries stand out on read QC within their group

The persistent `Sample filters` (the design group, then the library) sit in the
left panel and narrow every library tab through the project links; Run health
reads lanes, so it keeps its own lane, read and cycle filters instead.

!!! info "bcl2fastq by default, BCL Convert on request"
    The two demultiplexers write different reports: bcl2fastq a
    `Stats/Stats.json`, BCL Convert `Reports/Demultiplex_Stats.csv`,
    `Quality_Metrics.csv` and `Top_Unknown_Barcodes.csv`. The template reads
    bcl2fastq by default; `--var IS_BCLCONVERT=true` repoints the same four
    collections at BCL Convert recipes that write the same columns, so every tile
    renders unchanged. BCL Convert reports no raw cluster count, so the
    pass-filter rate stays empty on that route.

!!! note "Lanes and reads are rows, design comes from a file"
    Every run-level collection is one row per lane (and per read), so a one-lane
    benchtop run and a multi-lane production flowcell ingest through the same
    template. Design factors are never parsed out of library names: they come
    from an optional `METADATA_FILE`, and without it every library falls in a
    single group and every tile still renders.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/demultiplex_results \
      --template nf-core/demultiplex/latest
    ```

    The results directory is the only thing you have to pass. To group libraries by a
    design factor, add a metadata TSV whose first column is the library name as
    written in the sample sheet:

    ```bash
    depictio ingest /path/to/demultiplex_results \
      --template nf-core/demultiplex/latest \
      --var METADATA_FILE=/path/to/library_metadata.tsv \
      --var GROUP_COL=organism
    ```

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/demultiplex -r 1.8.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the MultiQC report, the demultiplexer statistics of every
flowcell and lane, the CheckQC report, the fastp JSON of every library and,
when present, an Illumina InterOp summary table. A pipeline-local `libraries`
recipe joins them into one row per library, the hub of the sample filters.
47 of its 60 tiles carry a `use:` catalog reference, so a tile says where its
panel comes from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="1.8.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/demultiplex-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a
funnel from what the checks flagged to how each library reads, in the order a
facility signs a run off. Each tab below carries the **same icon and colour the
dashboard gives it**, so the page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Run health |
| Demultiplexing | Library balance, Undetermined reads, Library QC |

Each child tab opens with a short intro and, except on MultiQC, a strip of four
cards, then at most three open sections; tables and conditional detail follow,
collapsed. The design comes from the optional `METADATA_FILE`: without it the
`libraries` hub carries one group, "All libraries", and every tile still renders.
The persistent *Sample filters* (the group, then the library, both on the hub)
sit in the left panel and narrow every library tab through the project links.
Run health reads lanes, which no library link reaches, so they are kept off that
tab. The *Sample sheet* is pinned, collapsed, to the bottom of every child tab
except Run health.

=== ":material-compass-outline: Overview"

    *A sequencing run split into its libraries, from lanes to per-library read QC.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/demultiplex/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/demultiplex/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how the two
    filter levels work, *The run* lists the demultiplexer (from `params.json`), the
    libraries, the lanes and the yield, and *Pipeline* walks the five steps from
    run folder to libraries (convert, split, leftovers, read QC, check), each
    linked to the setting or tool version behind it and to its tab. The findings
    are live values: they follow the filters, and a route that lacks their data
    drops them.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the group and the library):
        each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: libraries by group, bases at Q30 on the weakest lane, the smallest library against an even share, the Undetermined share of the worst lane |
        | Findings | Live result rows, then 4 figures: the base quality per cycle, reads against index purity, the library QC scatter and the most frequent unknown barcodes |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *What did CheckQC and the read QC tools flag?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/demultiplex/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/demultiplex/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: the two CheckQC panels (libraries under the read
    threshold, the Undetermined share against its limit) and the general
    statistics, then Falco read counts, per-read quality and adapter content with
    the fastp insert sizes. Start with CheckQC: a library far below an even share
    of reads fails there first. The Falco status checks and the remaining Falco and
    fastp panels are collapsed. The bcl2fastq panels, fastp Filtered Reads and
    fastp Sequence Quality are left out: the other tabs read the same numbers from
    the reports themselves.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Library or FASTQ file` on `multiqc_data`, as MultiQC names
        it, and a `Reads, % of an even share` range on the `libraries` hub, which
        links into the report.

        | Section | What it holds |
        |---|---|
        | CheckQC verdicts | 3 MultiQC panels |
        | Read QC after demultiplexing | 4 MultiQC panels |
        | More MultiQC panels (collapsed) | 10 MultiQC panels |

=== ":material-stethoscope:{ .mc-teal } Run health"

    **Data & QC** · *Did the instrument deliver on every lane, read and cycle?*

    [![Run health dashboard](../../images/pipeline-templates/nf-core/demultiplex/run_health_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/run_health_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Run health dashboard](../../images/pipeline-templates/nf-core/demultiplex/run_health_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/run_health_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Clusters passing filter (then those assigned to a library), the lowest
    pass-filter rate on a gauge, the share of bases at Q30 in the weakest read and
    the yield split by read. Then every lane by Undetermined share and Q30, sized by
    yield (a lane low and to the right lost reads to both), beside the lane by read
    quality dot plot, and the base quality at every cycle, one curve per lane and
    read with its 10th to 90th percentile band. A lane or read that drops alone
    points at the flowcell or the chemistry, not at the libraries. The Sequencing
    Analysis Viewer metrics and the lane table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Lane` on `lane_summary`, `Read` on `read_quality` and a
        `Cycle` range on `cycle_quality`. The sample filters do not reach this tab.

        | Section | What it holds |
        |---|---|
        | Run health at a glance | 4 cards |
        | Lanes and reads | 2 advanced visualizations: the lane scatter and the lane by read dot plot |
        | Quality along the run | 1 advanced visualization |
        | Sequencing Analysis Viewer metrics (collapsed) | 4 cards, 2 advanced visualizations: the PhiX error rate per lane and read, phasing against prephasing |
        | Lane detail (collapsed) | *Lane summary* |

    !!! tip "The SAV section needs an InterOp summary table"
        Error rate, phasing and cluster density live in the InterOp binaries,
        which Depictio does not parse. demultiplex 1.8.0 does not run
        `interop_summary`, so on a stock run the collapsed section stays empty.
        Run `interop_summary --csv=1 <run folder>` and drop the output anywhere
        under the run (any `.csv` whose name contains `interop_summary`): the
        section then shows the worst PhiX error rate, the lowest share of clusters
        passing filter, the densest lane and the worst phasing, then the error
        rate per lane and read and phasing against prephasing.

=== ":material-scale-balance:{ .mc-indigo } Library balance"

    **Demultiplexing** · *How evenly were each lane's reads shared between the libraries?*

    [![Library balance dashboard](../../images/pipeline-templates/nf-core/demultiplex/library_balance_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/library_balance_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Library balance dashboard](../../images/pipeline-templates/nf-core/demultiplex/library_balance_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/library_balance_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Reads assigned to libraries (with the share the three largest hold), the median
    share of the lane per library, the smallest library against the mean library of
    the least even lane (a gauge, 100 is the mean) and the worst perfect index
    match. Then the composition of each lane (the eight largest libraries named,
    the rest pooled, Undetermined kept) beside the run, lane, library sunburst, then
    every library's share of its lane and its reads against index purity. A library
    with few reads and a high perfect-match share was under-pooled; one with few
    reads and a low perfect-match share lost reads to index errors. The reads per
    library and lane, Undetermined rows included, are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Lane` on `lane_summary`, and `Share of the lane (%)` and
        `Perfect index match (%)` ranges on `demux_stats`.

        | Section | What it holds |
        |---|---|
        | Balance at a glance | 4 cards |
        | Lane composition | 2 advanced visualizations: the libraries per lane and the run, lane, library sunburst |
        | Library balance | *Share of the lane per library*, 1 advanced visualization (reads against index purity) |
        | Per-lane library counts (collapsed) | *Reads per library and lane* |

=== ":material-alert-outline:{ .mc-orange } Undetermined reads"

    **Demultiplexing** · *What did no index match, and is it an index swap?*

    [![Undetermined reads dashboard](../../images/pipeline-templates/nf-core/demultiplex/undetermined_reads_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/undetermined_reads_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Undetermined reads dashboard](../../images/pipeline-templates/nf-core/demultiplex/undetermined_reads_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/undetermined_reads_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The Undetermined share of the worst lane on a gauge, the Undetermined reads
    ranked by lane, the reads in the top unknown barcodes split by class and the
    share of a lane's Undetermined reads carried by its most frequent barcode. Then
    the fifteen most frequent unknown barcodes over the lanes in view, coloured by
    class. Each unassigned index pair is split into its i7 and i5 and checked
    against the libraries of the same lane: *Both indexes in use* is the
    index-hopping or swap signature, *Only i7 in use* or *Only i5 in use* often a
    mistyped index, *Neither index in use* a library missing from the sample sheet
    or a contamination, *Poly-G or N index* a failed index read. The unknown
    barcode table and the CheckQC findings (one row per finding, a pass row for
    each silent check) are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Lane` on `lane_summary`, and `Barcode class` and a `Rank in
        its lane` range on `unknown_barcodes`.

        | Section | What it holds |
        |---|---|
        | Undetermined at a glance | 4 cards |
        | Top unknown barcodes | *Most frequent unknown barcodes* |
        | Barcode and verdict tables (collapsed) | *Unknown barcodes*, *CheckQC findings* |

    !!! info "No unknown barcodes, no barcode tiles"
        bcl2fastq keeps the top unknown barcodes of each lane, and the recipes keep
        the 100 most frequent per lane. A report without them skips
        `unknown_barcodes`: its cards, figure, table and filters go, and the lane
        cards of the tab remain.

=== ":material-test-tube:{ .mc-grape } Library QC"

    **Demultiplexing** · *Which libraries stand out on read QC within their group?*

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/demultiplex/library_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/library_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/demultiplex/library_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/demultiplex/library_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The reads fastp was given (then those it kept), the median duplication ranked
    by group, the median share of reads with an adapter and the median share of
    bases at Q30 after filtering. Then duplication against base quality, one point
    per library sized by reads and coloured by group, beside the library card,
    which stays a thin rail until a library is lassoed in the scatter or picked in
    the fastp table. Below, every numeric library metric compared between two
    groups or two saved selections: with a few libraries per group the test is a
    screen, not a verdict. The fastp table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Duplication (%)` and `GC content (%)` ranges on the
        `libraries` hub.

        | Section | What it holds |
        |---|---|
        | Library QC at a glance | 4 cards |
        | Libraries against each other | 2 advanced visualizations: the duplication against base quality scatter and the library card |
        | Design groups compared | 1 advanced visualization |
        | fastp table (collapsed) | *fastp read QC* |

    !!! info "One group without a metadata file"
        Without `METADATA_FILE` the hub carries a single group, "All libraries":
        the group breakdowns show one bar, and the comparison has nothing to
        compare until two selections are saved.

Tables and points select on their entity column: the lane table and the lane
health and phasing scatters on `lane_label`; the sample sheet, the per-lane
library table, the index purity and library QC scatters and the fastp table on
`sample`; the unknown barcode table on `barcode`. A pick narrows the other tiles
of its collection and follows the project links to the collections they reach.
The library card on Library QC follows the scatter beside it. The per-cycle
quality profile and the CheckQC findings table do not select: their collections
have no outgoing link. The SAV collection has no incoming link either, so the
lane filters do not narrow it.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/demultiplex, it does not run the
pipeline. Run the pipeline first:

```bash
nextflow run nf-core/demultiplex -r 1.8.0 \
  --input samplesheet.csv \
  --demultiplexer bcl2fastq \
  --outdir results -profile docker
```

Then point Depictio at the results, adding `--var IS_BCLCONVERT=true` for a
`--demultiplexer bclconvert` run:

```bash
depictio ingest results/ --template nf-core/demultiplex/latest
```

See [nf-co.re/demultiplex/usage](https://nf-co.re/demultiplex/1.8.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory of one pipeline run. Depictio scans
recursively and matches on file name, so the flowcell and lane folder names can
differ from the tree below.

```text
<DATA_ROOT>/
├── <flowcell>/
│   ├── L<lane>/
│   │   ├── Stats/Stats.json                   # bcl2fastq statistics (default route)
│   │   ├── Reports/                           # or BCL Convert: Demultiplex_Stats.csv, Quality_Metrics.csv,
│   │   │                                      #   Top_Unknown_Barcodes.csv (IS_BCLCONVERT)
│   │   ├── checkqc_report.json                # CheckQC verdicts (optional)
│   │   └── *.fastp.json                       # fastp read QC, one per library (optional)
│   └── *interop_summary*.csv                  # optional, from interop_summary --csv=1
├── multiqc/multiqc_data/
│   └── multiqc.parquet                        # bcl2fastq, CheckQC, fastp, Falco
└── pipeline_info/
    ├── params_*.json
    └── *software*versions*.yml
```

`METADATA_FILE` is optional and can live anywhere: a TSV whose first column is
the library name, every other column a design factor. `GROUP_COL` picks the one
the tiles group by, the first annotation column otherwise.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 1.8.0 release
(`results-daade37c4a75a4c1709ccf12434deb3424141319`, `test_full` profile: one
MiSeq flowcell, one lane, paired-end dual-index, demultiplexed with bcl2fastq),
and the screenshots above come from it, with the vendored
`input/library_metadata.tsv` grouping the libraries by organism. That run is a
useful stress case: several libraries got almost no reads and a large share of
the lane went to Undetermined, mostly swapped combinations of indexes in use.
The BCL Convert route and the SAV section were checked on MultiQC test-data
reports only. `megatest.yaml` lists the tables-only subset the template needs:

```bash
bash depictio/projects/nf-core/demultiplex/1.8.0/download_test_data.sh /tmp/demultiplex_test
depictio ingest /tmp/demultiplex_test --template nf-core/demultiplex/latest \
  --var METADATA_FILE=depictio/projects/nf-core/demultiplex/1.8.0/input/library_metadata.tsv
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/demultiplex](https://nf-co.re/demultiplex): official pipeline documentation
- [nf-co.re/demultiplex/1.8.0/results](https://nf-co.re/demultiplex/1.8.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/demultiplex releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
