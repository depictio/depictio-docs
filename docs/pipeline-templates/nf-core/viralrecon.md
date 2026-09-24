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
reads to variant calls, one tab per step:

- :material-chart-box-outline: **MultiQC**: FastQC, fastp, Kraken2, bowtie2 and mosdepth, then iVar, snpEff, bcftools and QUAST, straight from the report
- :material-chart-areaspline: **Coverage & Depth**: where the mosdepth depth sits along the genome and across the amplicons
- :material-virus: **Lineage & Clustering**: Pangolin lineages and Nextclade clades, the flow from QC verdict to call, and a variant-profile PCA
- :material-stethoscope: **Sample QC**: breadth, mapping and variant yield per sample, with a sample record beside the coverage scatter
- :material-dna: **Variants**: every iVar call along the genome, by gene and effect, and which mutations travel together

A `Run at a glance` strip and the collapsed `Sample sheet` are pinned to the top
of every tab, the `Sample filters` group with them and the `QC thresholds` group
to the bottom, so the sample list and its floors follow you from tab to tab.

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
    depictio run \
      --template nf-core/viralrecon/latest \
      --data-root /path/to/runs
    ```

    `--data-root` is the only thing you have to pass. The template reads a
    `sequencing-runs` layout, so point it at the **parent** of one or more
    `run_*` directories, each holding one viralrecon `--outdir`. Every run found
    there is aggregated into the same collections.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/viralrecon -r 3.0.0 -profile docker \
      --outdir runs/run_1 --depictio_data_root runs
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
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
layout and drops `summary_metrics`, `variants_long` and the views built on the
variant calls, since an ARTIC run writes no `variants_long_table.csv`.

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

Five tabs, read as a funnel: did the run sequence and align well, where does the
depth sit, what was each sample typed as, which samples to trust, and what the
calls are. Each tab below carries the **same icon and colour the dashboard gives
it**, so the page and the app read alike. `summary_metrics` (one row per sample)
is the source of every project link, so a filter or a pick on `sample` reaches
every per-sample collection on every tab.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Did the run sequence, align and call cleanly, straight from the report?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The pinned `Run at a glance` strip opens every tab with four numbers:
    samples, median reads mapped, median genome breadth at 10x and lineages.
    Under it, the collapsed `Sample sheet` holds the `summary_metrics` table,
    whose ticked rows narrow every tab. The tab itself is MultiQC only: the
    panels worth reading first, then two collapsed sections with the read,
    alignment, variant and assembly panels, including the nf-core variant summary
    that stands in when a route prunes `summary_metrics`.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and `Lineage` in `Sample filters`, persistent and
        pinned to the top of every tab; `Genome covered at 10x (%)`, `Median
        depth`, `Reads mapped (%)` and `Variants called` ranges in a collapsed
        `QC thresholds` group pinned to the bottom, all on `summary_metrics`. A
        collapsed `MultiQC report` group keeps a `Sample ID` list read from the
        report itself.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Summary metrics*, pinned to every tab and collapsed |
        | QC overview | *MultiQC general statistics* and 4 MultiQC panels |
        | Read & alignment details | 6 MultiQC panels (FastQC, Kraken2, samtools, mosdepth, cutadapt) |
        | Variant & assembly details | 7 MultiQC panels (iVar, snpEff, bcftools, QUAST, nf-core variant summary) |

=== ":material-chart-areaspline:{ .mc-teal } Coverage & Depth"

    *Where does the depth actually sit, along the genome and across the amplicons?*

    [![Coverage & Depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage & Depth dashboard](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Four cards summarise the depth: amplicons tracked, the median amplicon and
    genome depth, and how many amplicon measurements fall under the 20x default
    floor. Below, the per-position genome track (linear axis, one sub-track per
    sample, so dropouts read as gaps), the per-amplicon track on a log axis and
    the clustered amplicon heatmap, where a primer that fails across samples
    reads as a column.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Genome depth` range on `mosdepth_genome_coverage`, and
        an `Amplicon` picker and an `Amplicon depth` range on
        `mosdepth_amplicon_coverage`, local to this tab in `Coverage scope`.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | Coverage tracks | *Genome coverage track per sample*, *Amplicon coverage track*, *Amplicon coverage heatmap (clustered)* |
        | Coverage tables | *Amplicon coverage table*, collapsed, rows select on `sample` |

=== ":material-virus:{ .mc-red } Lineage & Clustering"

    *What was each sample typed as, and do the lineage and clade calls agree?*

    [![Lineage & Clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Lineage & Clustering dashboard](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Pangolin lineage and Nextclade clade counts sit side by side, then a Sankey
    carries each sample from its QC verdict to its lineage to its clade. The
    variant-profile PCA, coloured by lineage, is a selection source: lasso a
    cluster and the samples in it filter the linked panels. In the collapsed
    typing tables, a linked *Lineage record* card sits beside the Pangolin
    table: it folds to a slim rail until a row is ticked, then shows that
    sample's full call, scorpio notes included.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Lineage` and `Pangolin QC` on `pangolin_lineages`,
        `Clade` and `Nextclade QC` on `nextclade_results`, in `Typing`.

        | Section | What it holds |
        |---|---|
        | Typing at a glance | 4 cards |
        | Lineage distribution | *Pangolin lineage distribution*, *Nextclade clade distribution* |
        | Classification flow | *Classification flow: QC verdict, lineage, clade*, *Variant-profile PCA embedding (coloured by lineage)* |
        | Typing tables | *Pangolin lineage assignments* with its linked *Lineage record*, *Nextclade clade assignments*, collapsed |

=== ":material-stethoscope:{ .mc-indigo } Sample QC"

    *Which samples can you trust, and is a divergent one real or under-sequenced?*

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Sample QC dashboard](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Four median cards (breadth at 1x, variants per sample, reads mapped and
    missing consensus bases) open the tab. The two diagnostic scatters, coverage
    against variant count and Nextclade substitutions against deletions,
    separate divergent samples from under-sequenced ones, and both select on
    `sample`. The linked *Sample record* sits beside the coverage scatter: it
    folds to a slim rail until a point is lassoed there, in the Nextclade
    scatter or in the Sample sheet, then shows that sample's alignment, breadth
    and calls. Genome breadth at 1x and 10x per sample closes the tab, with the
    80% default floor dashed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `SNPs called` and `Indels called` ranges on
        `summary_metrics` and a `Missing bases` range on `nextclade_results`, in
        `Variant yield`.

        | Section | What it holds |
        |---|---|
        | QC at a glance | 4 cards |
        | Diagnostics | *Median coverage vs total variants* with its linked *Sample record*, *Nextclade substitutions vs deletions* |
        | Per-sample coverage | *Genome breadth per sample at 1x and 10x* |

=== ":material-dna:{ .mc-orange } Variants"

    *What are the calls, where do they land, and which mutations travel together?*

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralrecon/variants_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Four cards size the call set, then the allele frequency of every call along
    the genome, with the default consensus threshold drawn as the score line,
    and one lollipop track per gene. The allele-frequency histogram and the read
    support scatter show how well supported the calls are; the frequency track
    and the read support scatter both select on `sample`. Calls per gene and
    functional class and per sample follow, and the tab closes on a sample by
    gene mutation matrix and an UpSet of the mutations shared across lineages.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Gene`, `Variant Effect` and `Functional class` pickers
        and `Allele Frequency` and `Read depth` ranges on `variants_long`, in
        `Variant filters`, plus a `Mutation Type` picker in a collapsed
        `Oncoplot scope` group that reaches the mutation matrix only.

        | Section | What it holds |
        |---|---|
        | Variant burden | 4 cards, *Variant frequencies along the genome*, *Variant tracks per gene (lollipop)* |
        | Allele frequency | *Allele frequency distribution*, *Read support per call* |
        | Effect breakdown | *Variant counts by gene & functional class*, *Variants per sample* |
        | Co-occurrence | *Sample × gene mutation matrix*, *Mutations shared across lineages (UpSet)* |
        | Variant table | *Variants table*, collapsed, rows select on `sample` |

    !!! note "No variant tabs on a nanopore run"
        The `IS_NANOPORE` route drops `variants_long` and every view built on
        it, so the Variants tab and the variant-profile PCA disappear, and
        `summary_metrics` goes with them. The coverage and typing tabs keep
        working off the `artic_minion/` layout.

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
depictio run --template nf-core/viralrecon/latest \
  --data-root runs/
```

A later run written to `runs/run_2` is aggregated into the same collections on
the next ingest. A nanopore ARTIC run (`--platform nanopore`) needs no extra
flag: Depictio reads `platform: nanopore` from the run's `params.json` and sets
`IS_NANOPORE` itself.

See [nf-co.re/viralrecon/usage](https://nf-co.re/viralrecon/3.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the `run_*` directories. Depictio
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
depictio run \
  --template nf-core/viralrecon/latest \
  --data-root /tmp/viralrecon_test
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
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
