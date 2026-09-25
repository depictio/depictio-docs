---
title: AIRR Repertoire Analysis
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/airrflow" target="_blank" title="nf-core/airrflow on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_dark.png" alt="nf-core/airrflow">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_light.png" alt="nf-core/airrflow">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">AIRR Repertoire Analysis</h1>
    <p class="template-subtitle">B and T cell receptor repertoire analysis: the pRESTO and Change-O sequence funnel, V gene usage, and the Immcantation enchantR clonal report next to the pipeline's own MultiQC.</p>
    <p class="template-links">
      <a href="https://nf-co.re/airrflow" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/airrflow" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="5.1.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="5.1.0" selected>5.1.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The airrflow template covers the reporting half of a standard nf-core/airrflow run, from the raw reads through to the clones:

- :material-chart-box-outline: **Read quality**: fastp trimming and both FastQC runs, read from the pipeline's own MultiQC parquet
- :material-chart-areaspline: **Sequence funnel**: every read followed to the step it stopped at, across pRESTO and Change-O
- :material-dna: **Repertoire composition**: V gene usage at family and gene resolution, the CDR3 spectratype and V-J pairing per donor
- :material-chart-bell-curve: **Clonal analysis**: clones against depth, Hill diversity profiles and rank abundance with bootstrap bands, clonal homeostasis
- :material-set-all: **Sharing between samples**: the pairwise shared-clone matrix and the higher-order intersections behind it
- :material-table: **Cohort and reference tables**: the cohort cards and the AIRR samplesheet pinned to the top of every tab, the repertoire summary to the bottom

!!! info "No external metadata file"
    Everything the template reads comes from the run itself: the validated
    samplesheet the pipeline writes to `pipeline_info/samplesheet.valid.tsv` is
    the hub data collection, so there is nothing to prepare. The one column to
    name is the condition, `GROUP_COL`, which defaults to `treatment`, the
    column airrflow's samplesheet schema documents for it. 5.1.1 has no AWS
    megatest run, so 5.1.0 is the newest release the template could be validated
    against; it binds against both.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/airrflow/latest \
      --data-root /path/to/airrflow_results
    ```

    `--data-root` is the only thing you have to pass. The samplesheet is picked
    up from `{DATA_ROOT}/pipeline_info/samplesheet.valid.tsv`; pass
    `--var SAMPLESHEET_FILE=...` to point somewhere else.

    The condition filter reads the samplesheet column named by `GROUP_COL`
    (default `treatment`, labelled `Condition`). A samplesheet that keeps the
    condition in another free column names it, and can relabel it:

    ```bash
    depictio run \
      --template nf-core/airrflow/latest \
      --data-root /path/to/airrflow_results \
      --var GROUP_COL=intervention \
      --var GROUP_COL_DISPLAY=Intervention
    ```

    | Variable | Default | Meaning |
    |---|---|---|
    | `DATA_ROOT` | required | Root of the airrflow output directory |
    | `SAMPLESHEET_FILE` | `{DATA_ROOT}/pipeline_info/samplesheet.valid.tsv` | The validated samplesheet, the hub data collection |
    | `GROUP_COL` | `treatment` | Samplesheet column holding the condition; must exist in the samplesheet |
    | `GROUP_COL_DISPLAY` | `Condition` | Reader-facing label of that column in filter titles |
    | `SKIP_CLONAL_ANALYSIS`, `SKIP_REPORT`, `SKIP_THRESHOLD_REPORT`, `SKIP_MULTIQC`, `ASSEMBLED_MODE` | unset | Mirror the run's route flags; see *Conditional routes* below |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/airrflow -r 5.1.0 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the MultiQC parquet, the two sequence-count logs, the V usage
tables from the repertoire comparison report, and the enchantR clonal analysis
tables (diversity, clone sizes, pairwise overlap, distance threshold). Most tiles
are catalog renders bound to `enchantr`, airrflow's own R package rather than an
nf-core module, so the tile chrome names where each panel comes from.

The route flags in the *Conditional routes* table are not read back from
`params.json` yet, so a run started with `--skip_clonal_analysis`,
`--skip_report`, `--skip_report_threshold`, `--skip_multiqc` or
`--mode assembled` needs the matching `--var SKIP_...=true` (or
`--var ASSEMBLED_MODE=true`). Omitting one still
ingests: the affected collections are optional and simply come up empty.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="5.1.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/airrflow-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Four tabs, read as a funnel: are the reads good, how many survive, what
repertoire do the survivors make, and how is that repertoire structured. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike. `Sample filters` is persistent and pinned to the top of every
tab, and one pick there reaches every other collection through the template's
[cross-DC links](#cross-dc-links). `Cohort at a glance` and a collapsed
`Sample sheet` are pinned to the top of every tab, `Reference tables` to the
bottom, so the cohort a tile is computed from is always in view.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *fastp and FastQC, straight from the pipeline's MultiQC report.*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/airrflow/multiqc_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/airrflow/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    Eleven MultiQC panels in three sections: read yield before and after
    trimming, per-base and per-read quality, then GC, length, duplication and
    adapter content, the last collapsed. airrflow runs FastQC twice, on the raw
    reads and again after assembly, so MultiQC labels the second run `fastqc-1`
    and its series carry an `_ASSEMBLED` suffix. Amplicon libraries are expected
    to look duplicated and to sit in a narrow GC and length band, so most FastQC
    warnings here are normal.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample`, `Subject`, `Condition` (the `GROUP_COL` column)
        and `Sex` on `samplesheet`, persistent and pinned to the top of every tab,
        plus a `Report sample` selector on `multiqc_data` in a collapsed *Read QC
        scope* group, needed because the MultiQC sample ids carry the
        `_ASSEMBLED` suffix.

        | Section | What it holds |
        |---|---|
        | Cohort at a glance | 4 cards (samples, subjects, subject age, target loci), pinned to every tab |
        | Sample sheet | *AIRR samplesheet*, collapsed, pinned to every tab |
        | Read QC at a glance | 3 MultiQC panels |
        | Base quality | 3 MultiQC panels |
        | Read content | 5 MultiQC panels, collapsed |
        | Reference tables | *Repertoire summary*, collapsed, pinned to every tab |

        Picking rows in either pinned table filters the dashboard by
        `sample_id`, like the persistent filters do.

=== ":material-chart-areaspline:{ .mc-indigo } Sequence processing"

    *How many reads survive each pRESTO and Change-O step, and where the rest go.*

    [![Sequence processing dashboard](../../images/pipeline-templates/nf-core/airrflow/sequence_processing_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/airrflow/sequence_processing_light.png){ .tpl-shot target="_blank" rel="noopener" }

    The signature panel is a Sankey following every read of every sample to the
    step it stopped at. Three of those steps collapse reads rather than discard
    them, since UMI consensus, deduplication and the representative filter each
    fold many reads onto one sequence, so a low retention is expected and it is
    the spread across samples that matters. Below it the funnel is redrawn one
    line per sample on a log axis: a line that drops away from the rest at one
    step is the sample to look at.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Input reads` and `Retention` ranges on `sequence_counts`
        in a collapsed *Processing scope* group, over the persistent sample
        filters.

        | Section | What it holds |
        |---|---|
        | Funnel at a glance | 4 cards |
        | Where the reads go | *Read fates through the pipeline* |
        | Per sample | *Sequences remaining at each step*, *Retention per sample* |
        | Sequence counts table | *Sequence processing counts*, collapsed |

=== ":material-dna:{ .mc-pink } Repertoire"

    *Which V and J genes and which CDR3 lengths build each repertoire.*

    [![Repertoire dashboard](../../images/pipeline-templates/nf-core/airrflow/repertoire_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/airrflow/repertoire_light.png){ .tpl-shot target="_blank" rel="noopener" }

    V usage is a stacked composition switchable between family and gene
    resolution, beside a clustered sample by V gene heatmap, column standardised
    so rare genes stay visible. The CDR3 spectratype is the classic clonality
    readout: a polyclonal repertoire draws a smooth bell per sample, and one
    length towering over its neighbours is an expanded clone. The V-J pairing
    heatmap closes the tab, one row per donor and V gene and one column per J
    gene, counted per donor because clones are defined per donor.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `V family` on `v_gene_usage` in a collapsed *V gene
        resolution* group, and a `CDR3 length (aa)` range on `cdr3_spectratype`
        in a collapsed *CDR3 length* group.

        | Section | What it holds |
        |---|---|
        | Repertoire at a glance | 4 cards |
        | V gene usage | *V gene composition*, *V gene usage heatmap* |
        | CDR3 spectratype | *Spectratype per sample* |
        | V-J pairing | *V by J pairing* |

    !!! tip "Spectratype and V-J pairing need the AIRR table"
        Both read the `*__repertoire-pass.tsv` rearrangement table enchantR's
        repertoire analysis starts from, keeping only the handful of columns they
        need. The two collections are optional: a run with
        `--skip_clonal_analysis`, or a copy of the output without that table,
        drops the two sections and keeps the rest of the tab.

=== ":material-chart-bell-curve:{ .mc-teal } Clonal analysis"

    *How clonal and how diverse each repertoire is, and which clones samples share.*

    [![Clonal analysis dashboard](../../images/pipeline-templates/nf-core/airrflow/clonal_analysis_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/airrflow/clonal_analysis_light.png){ .tpl-shot target="_blank" rel="noopener" }

    The shazam distance threshold and its sensitivity sit on the card row,
    because clones are called by nearest-neighbour distance and every number on
    the tab rests on the threshold fitted per subject. Clone counts scale with
    sequencing depth, so the tab opens on clones against depth: a repertoire that
    is simply deeper sits along the diagonal, a genuinely more clonal one below
    it. The Hill profile draws one curve per repertoire against the order q with
    alakazam's bootstrap band, and the rank-abundance curve carries its band too.
    The last section pairs the shared-clone heatmap with an UpSet of the
    intersections a pairwise view cannot show.

    Clones versus depth, Richness against evenness and the rank-abundance curve
    are selection sources: lasso samples on any of them and the rest of the tab
    narrows to those samples.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Clones` range on `repertoire_summary`, `Diversity order`
        on `diversity_orders`, `Size class` and `Clone rank` on `clone_sizes`, in
        a collapsed *Clonal scope* group, plus `Samples per clone` on
        `clone_sets` in a collapsed *Sharing scope* group.

        | Section | What it holds |
        |---|---|
        | Clonal analysis at a glance | 6 cards |
        | Clones and depth | *Clones versus depth*, *Richness against evenness* |
        | Diversity profiles | *Diversity profile with confidence ribbons*, *Diversity at one named order, ranked* |
        | Clone abundance | *Rank abundance with bootstrap confidence*, *Clonal homeostasis* |
        | Sharing between samples | *Shared clones per sample pair*, *Clone set intersections* |
        | Clonal tables | *Clonal distance threshold*, *Clonal overlap matrix*, collapsed |

!!! tip "Two things that look wrong and are not"
    The overlap heatmap's diagonal is written as 0, since a sample's overlap with
    itself dwarfs any real sharing and flattens the colour scale; cross-subject
    cells read zero too, because airrflow defines clones within a subject. And a
    sample too shallow for enchantR to fit diversity numbers is dropped from
    `clonal_diversity.tsv`, so its diversity cards are null while its clone counts
    stand.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/airrflow, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/airrflow -r 5.1.0 \
  --input samplesheet.tsv \
  --mode fastq \
  --library_generation_method specific_pcr_umi \
  --cprimers CPrimers.fasta \
  --vprimers VPrimers.fasta \
  --umi_length 12 \
  --outdir results -profile docker
```

Then point Depictio at the results:

```bash
depictio run --template nf-core/airrflow/latest \
  --data-root results/
```

See [nf-co.re/airrflow/usage](https://nf-co.re/airrflow/5.1.0/docs/usage)
for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so the layout below only has to be present
somewhere under the root. Nothing outside the run is needed.

```text
<DATA_ROOT>/
├── pipeline_info/
│   ├── samplesheet.valid.tsv                       # hub DC, --var SAMPLESHEET_FILE
│   ├── params.json
│   └── software_versions.yml
├── multiqc/
│   └── multiqc_data/
│       └── multiqc.parquet                         # fastp + both FastQC runs
├── parsed_logs/
│   └── Table_sequences_process.tsv                 # pRESTO half of the funnel
├── repertoire_comparison/
│   ├── Sequence_numbers_summary/
│   │   └── Table_sequences_assembled.tsv           # Change-O half of the funnel
│   └── V_family/
│       ├── V_family_distribution_data.tsv
│       └── V_gene_distribution_by_sequence_data.tsv
└── clonal_analysis/
    ├── find_threshold/all_reps_dist_report/tables/
    │   └── all_reps_threshold-summary.tsv          # shazam threshold per subject
    └── repertoire_analysis/repertoire_analysis_report/
        ├── repertoires/
        │   └── *__repertoire-pass.tsv              # AIRR table: spectratype, V-J pairing
        └── tables/
            ├── clonal_abundance.tsv                # rank abundance with bootstrap band
            ├── clonal_diversity.tsv
            ├── clonal_overlap.tsv
            ├── clone_sizes_table.tsv
            └── num_clones_table.tsv
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/airrflow/5.1.0/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs:

```bash
bash depictio/projects/nf-core/airrflow/5.1.0/download_test_data.sh \
  /tmp/airrflow_test
```

The run is
`s3://nf-core-awsmegatests/airrflow/results-e69d49e3f23f11a3391755b5fb7aa4283c0a2471/`
(the 5.1.0 release tag): a ten-sample, two-subject multiple sclerosis B cell
study of cervical lymph node and brain lesion tissue, run in the default
`--mode fastq` UMI route. The manifest fetches fifteen keys, about 330 MB,
nearly all of it the AIRR rearrangement table behind the spectratype and the
V-J grid;
`post_fetch_help` in `megatest.yaml` prints the dry-run and full-run commands
once the download finishes.

Then run Depictio against it:

```bash
depictio run \
  --template nf-core/airrflow/latest \
  --data-root /tmp/airrflow_test
```

---

## :material-link-variant: Additional resources

- [nf-co.re/airrflow](https://nf-co.re/airrflow): official pipeline documentation
- [nf-co.re/airrflow/5.1.0/results](https://nf-co.re/airrflow/5.1.0/results): AWS test results
- [Immcantation](https://immcantation.readthedocs.io): enchantR, alakazam and shazam, the toolset behind the repertoire panels
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
    <span class="tpl-credit-note">Keep it working as nf-core/airrflow releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
