---
title: RNA Fusion Detection
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/rnafusion" target="_blank" title="nf-core/rnafusion on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnafusion/master/docs/images/nf-core-rnafusion_logo_dark.png" alt="nf-core/rnafusion">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnafusion/master/docs/images/nf-core-rnafusion_logo_light.png" alt="nf-core/rnafusion">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">RNA Fusion Detection</h1>
    <p class="template-subtitle">Gene fusions called from RNA-seq reads: the fusion-report consensus of three callers, each caller's own evidence, FusionInspector validation and the CTAT-splicing junction landscape.</p>
    <p class="template-links">
      <a href="https://nf-co.re/rnafusion" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/rnafusion" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="4.1.3">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="4.1.3" selected>4.1.3</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The rnafusion template follows the pipeline's own funnel, from read quality
through to the protein a fusion would produce:

- :material-chart-box-outline: **MultiQC**: FastQC either side of trimming, fastp, STAR and Picard, out of the MultiQC report
- :material-set-merge: **Fusion calls**: fusion-report's ranked calls, the UpSet of caller agreement, and the contigs the two partners came from
- :material-chart-scatter-plot: **Evidence**: Arriba, STAR-Fusion and FusionCatcher read support, side by side and each on its own terms
- :material-dna: **FusionInspector and splicing**: re-quantified calls with a linked record, the Pfam domains each partner brings, and the CTAT-splicing junction landscape

`Run at a glance` and `Sample sheet` are pinned to the top of every tab and the
fusion-report consensus to the bottom, so the run size, the samples and the
calls every tab is filtered by follow you from tab to tab.

!!! info "One row is one fusion in one sample"
    rnafusion writes one file per tool per sample and none of those files carries
    a sample column. Every recipe the template binds reads the sample off the file
    name instead, so every fusion and splicing table carries `sample` and the
    samplesheet links to all of them: on a cohort run, the sample filter narrows
    every tab. The fusion name stays the key a fusion selection fans out on,
    across the consensus, the three callers and the FusionInspector tables.

!!! note "Route flags are not auto-detected"
    rnafusion's `--tools` selection is not read back from `params.json`, so a run
    that skipped a step needs the matching variable: `SKIP_ARRIBA`,
    `SKIP_STARFUSION`, `SKIP_FUSIONCATCHER`, `SKIP_FUSIONINSPECTOR`,
    `SKIP_CTATSPLICING` or `SKIP_QC`. Each prunes the matching data collections
    and the tiles that read them.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/rnafusion/latest \
      --data-root /path/to/rnafusion_results
    ```

    `--data-root` is the only thing you have to pass. The samplesheet is looked
    for at `{DATA_ROOT}/input/samplesheet.csv`; pass
    `--var SAMPLESHEET_FILE=...` to point somewhere else.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/rnafusion -r 4.1.3 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the fusion-report consensus, the three caller tables behind
it, the FusionInspector abridged table (both the validated calls and the Pfam
domains come from that one file) and the CTAT-splicing intron scores, through
six catalog tools: `fusionreport`, `arriba`, `starfusion`, `fusioncatcher`,
`fusioninspector` and `ctatsplicing`.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="4.1.3" markdown>

--8<-- "pipeline-templates/nf-core/_generated/rnafusion-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Four tabs, read as a funnel: can the reads support a call at all, what was
called, how strong is each caller's evidence, and does the call survive
re-alignment. Each tab below carries the **same icon and colour the dashboard
gives it**. Two filter groups are persistent and pinned to the top of every tab,
`Sample scope` and `Fusion scope`, and a third, `Reference scope`, follows you
from tab to tab without being pinned.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Read and alignment QC before any fusion is trusted.*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/rnafusion/multiqc_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    A fusion call rests on reads that crossed a breakpoint, so a library that
    never aligned well cannot support one. The MultiQC general statistics table
    opens the tab, then the raw and post-trim FastQC panels either side of
    fastp, STAR's alignment scores and Picard's transcript region assignment.
    Insert size, gene body coverage and the STAR gene counts are folded in a
    collapsed `Library metrics` section. rnafusion runs FastQC twice, so the
    second pass is anchored as `fastqc-1` and carries a `_trimmed` suffix the
    samplesheet does not know: picking a sample in the persistent filter empties
    the trimmed panels.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and `Strandedness` on `samplesheet` in *Sample
        scope*, plus `Fusion`, `Caller agreement` and a `Fusion Indication Index`
        range on `fusion_consensus` in *Fusion scope*, both persistent and pinned
        to the top of every tab. *Reference scope* adds `5' partner gene` and
        `Knowledge bases hit` on `fusion_consensus`, persistent but not pinned.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards (fusions called, samples, callers reporting, distinct 5' partners), pinned to the top of every tab |
        | Sample sheet | *Sample sheet*, pinned to the top of every tab |
        | General statistics | *General statistics* |
        | Read quality | *Raw read quality*, *Reads kept by fastp*, *Trimmed read quality* |
        | Alignment | *STAR alignment scores*, *Where the bases landed* |
        | Library metrics | *Insert size distribution*, *Coverage along the gene body*, *STAR gene-count assignment* |
        | Reference tables | *fusion-report consensus*, pinned to the bottom of every tab |

=== ":material-set-merge:{ .mc-indigo } Fusion calls"

    *What the run called, how much agreement is behind each call, and where the two halves came from.*

    [![Fusion calls dashboard](../../images/pipeline-templates/nf-core/rnafusion/fusion_calls_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/fusion_calls_light.png){ .tpl-shot target="_blank" rel="noopener" }

    Four cards open the tab: the Fusion Indication Index, caller agreement,
    knowledge-base support and known fusions. The UpSet below reads every caller
    flag the run wrote as a set, so each bar is the fusions found by exactly that
    combination of callers and unanimous calls separate from single-caller ones
    at a glance. The lollipop plots each fusion at its fusion-report rank, sized
    by the index. `Partner chromosomes` then reads the Arriba breakpoints as a
    flow from the 5' partner's contig to the 3' partner's, and as chords on a
    chromosome ring coloured by structural class: a band that stays on one
    contig is a local rearrangement, one that crosses is a translocation.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Rank` and `Knowledge bases` ranges on `fusion_consensus`
        and `Partner contigs` on the Arriba calls, in a *Consensus scope* group,
        on top of the persistent filters.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Caller concordance | *Caller concordance* (UpSet), *Ranked fusions* (lollipop) |
        | Partner chromosomes | *Partner contigs, 5' to 3'* (Sankey), *Breakpoint partners on the genome* (chords) |

=== ":material-chart-scatter-plot:{ .mc-teal } Evidence"

    *The same fusions seen through each caller's own read counts.*

    [![Evidence dashboard](../../images/pipeline-templates/nf-core/rnafusion/evidence_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/evidence_light.png){ .tpl-shot target="_blank" rel="noopener" }

    The shared dot plot is one dot per fusion and caller, coloured by log10 read
    support and sized by that caller's share of the total, so an empty column
    means the caller never reported the fusion. The scatter below faces the
    two split-read callers, with FusionCatcher as the marker size: a fusion off
    the diagonal is one they weigh differently, and a lasso on it filters the
    dashboard by fusion.

    The collapsed `Per caller detail` section gives each caller its own view
    rather than a shared one, because the callers report genuinely different
    evidence quantities and collapsing them would mean inventing a common
    scale: Arriba by event type, breakpoint site and confidence class,
    STAR-Fusion by splice type, FusionCatcher by predicted effect. The caller
    tables at the foot of the tab are row-selectable on the fusion.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` and `Arriba confidence`, plus `Supporting reads`
        and `Caller share` ranges on `caller_evidence`, in an *Evidence scope*
        group.

        | Section | What it holds |
        |---|---|
        | Support across callers | 4 cards, *Read support per fusion and caller*, *Arriba against STAR-Fusion* |
        | Per caller detail | *Arriba event types*, *Arriba breakpoint sites*, *Arriba confidence and support*, *STAR-Fusion splice type and abundance*, *FusionCatcher predicted effect and support* |
        | Caller tables | *Per-caller evidence*, *Arriba calls*, *STAR-Fusion calls*, *FusionCatcher calls* |

=== ":material-dna:{ .mc-grape } FusionInspector and splicing"

    *What survives re-alignment, the fusion protein, and the junctions around it.*

    [![FusionInspector and splicing dashboard](../../images/pipeline-templates/nf-core/rnafusion/fusioninspector_and_splicing_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/fusioninspector_and_splicing_light.png){ .tpl-shot target="_blank" rel="noopener" }

    FusionInspector re-quantifies the calls against a fusion contig reference.
    The allelic-ratio scatter plots the 5' side against the 3' side on log axes:
    a call supported on one side only falls off the diagonal, the classic
    signature of a mapping artefact rather than a real fusion transcript. Beside
    it, a linked *Validated call record* folds to a slim rail until a point on
    the scatter or a row of the validated table is picked, then shows that
    call's breakpoints, read support, allelic ratios and predicted protein.

    The fusion protein structure draws each fusion as its two partners end to
    end with the breakpoint marked, one bar per Pfam domain along the partner
    that contributes it; a `PARTIAL` suffix means the breakpoint cuts through
    it. The collapsed `Splice junctions` section closes the tab with the
    CTAT-splicing landscape: support along the genome, arcs over the busiest
    loci, and a junction table whose row selection narrows both.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Predicted protein` and a `Fragments per million` range on
        `fusioninspector_fusions` in a *Validation scope* group; `Chromosome`
        and a `Unique read support` range on `splice_junctions` in a *Splicing
        scope* group.

        | Section | What it holds |
        |---|---|
        | Validated calls | 4 cards, *Validated abundance by predicted protein*, *Fusion allelic ratio, both sides* with the linked *Validated call record* |
        | Fusion protein domains | *Fusion protein structure*, *Domain positions per fusion*, *Pfam domains* |
        | Validated rows | *FusionInspector validation* |
        | Splice junctions | 4 cards, *Junction support along the genome*, *Junction arcs over the busiest loci*, *Splice junctions* |

!!! tip "Splice junctions follow the sample, not the fusion"
    CTAT-splicing scores every junction in the genes the callers touched, so the
    landscape is keyed on the junction and a fusion name has nothing to match
    against. `splice_junctions` is left out of the fusion links on purpose: the
    junction tiles keep their values when a fusion is picked, while the sample
    filter and the *Splicing scope* group narrow them.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/rnafusion, it does not run the
pipeline. Build the references once, then run the pipeline:

```bash
nextflow run nf-core/rnafusion -r 4.1.3 \
  --input samplesheet.csv \
  --genomes_base /path/to/references \
  --tools arriba,starfusion,fusioncatcher,ctatsplicing \
  --outdir results \
  -profile docker
```

Then point Depictio at the results:

```bash
depictio run --template nf-core/rnafusion/latest \
  --data-root results/
```

See [nf-co.re/rnafusion/usage](https://nf-co.re/rnafusion/4.1.3/docs/usage)
for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name. The samplesheet is the one file rnafusion
does not publish: put it under `input/`, or pass `--var SAMPLESHEET_FILE=...`.

```text
<DATA_ROOT>/
├── input/
│   └── samplesheet.csv                                     # --var SAMPLESHEET_FILE, not published by the run
├── pipeline_info/
│   ├── params_<timestamp>.json                             # run parameters and provenance
│   └── *software_versions.yml
├── multiqc/
│   └── multiqc_data/
│       └── multiqc.parquet                                 # FastQC, fastp, STAR, Picard
├── fusionreport/
│   └── <sample>/
│       └── <sample>.fusions.csv                            # the consensus, hub of the dashboard
├── arriba/
│   └── <sample>.arriba.fusions.tsv
├── starfusion/
│   └── <sample>.starfusion.abridged.tsv
├── fusioncatcher/
│   └── <sample>.fusion-genes.txt
├── fusioninspector/
│   └── <sample>/
│       └── <sample>.FusionInspector.fusions.abridged.tsv   # validated calls and Pfam domains
└── ctatsplicing/
    ├── <sample>.introns
    └── <sample>.cancer.introns                             # optional, header-only when nothing matched
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/rnafusion/4.1.3/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs,
20 files and about 3.9 MB. The run is
`s3://nf-core-awsmegatests/rnafusion/results-76ad76e7c39b2ba9edc35aa3602e3dc454d842ec/`:
the pipeline's own test profile, a single library spiked with twelve well known
cancer fusions. Its samplesheet is not part of the results, so fetch the one
`params.json` points at:

```bash
DEST=/tmp/rnafusion_test
bash depictio/projects/nf-core/rnafusion/4.1.3/download_test_data.sh "$DEST"
mkdir -p "$DEST/input" && curl -fsSL -o "$DEST/input/samplesheet.csv" \
  https://raw.githubusercontent.com/nf-core/test-datasets/rnafusion/testdata/human/samplesheet_valid.csv
depictio run --template nf-core/rnafusion/latest --data-root "$DEST"
```

!!! warning "One synthetic sample"
    The reference run is a single library, so every quality-control panel has one
    series and the sample filter can only select all or nothing. The fusions are
    synthetic: twelve calls score 1.0 and the rest 0.167, so the index reads as
    two plateaux rather than a ranking. The fusion tabs compare callers, not
    samples, so they read normally.

---

## :material-link-variant: Additional resources

- [nf-co.re/rnafusion](https://nf-co.re/rnafusion): official pipeline documentation
- [nf-co.re/rnafusion/4.1.3/results](https://nf-co.re/rnafusion/4.1.3/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/rnafusion releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
