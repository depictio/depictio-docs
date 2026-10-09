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
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
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

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC, fastp, STAR and Picard, out of the MultiQC report
- :material-set-merge: **Fusion calls**: fusion-report's ranked consensus and caller agreement, each caller's read support, and Arriba's breakpoints on the genome
- :material-check-decagram: **Follow-up**: FusionInspector re-quantification and fusion allelic ratios, the Pfam domains each fusion protein keeps, and CTAT-splicing junctions

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
    depictio ingest /path/to/rnafusion_results \
      --template nf-core/rnafusion/latest
    ```

    The results directory is the only thing you have to pass. The samplesheet is looked
    for at `{DATA_ROOT}/input/samplesheet.csv`; pass
    `--var SAMPLESHEET_FILE=...` to point somewhere else.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/rnafusion -r 4.1.3 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
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

One dashboard: the **Overview**, then seven child tabs in three groups, read as a
funnel from the reads to the proteins the fusions would make. Each tab below
carries the **same icon and colour the dashboard gives it**, so the page and the
app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC |
| Fusion calls | Caller Agreement, Caller Evidence, Breakpoints |
| Follow-up | Validation, Protein Domains, Splice Junctions |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. Two persistent filter
sections sit in the left panel. *Sample filters* (the sample, then the
strandedness) narrow every tab. *Fusion filters* (the fusion, then the caller
agreement) reach every caller table through the links on the fusion name;
MultiQC and Splice Junctions carry no fusion, so they are left off those two
tabs. The *Sample sheet* is pinned, collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Gene fusions, from the reads to the callers that agree and the proteins they would make.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/rnafusion/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/rnafusion/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how to move
    through the tabs, *The run* lists the samples, the genome and GENCODE release,
    the callers and the caller cut-off, and *Pipeline* walks the six steps from
    alignment to splicing, each linked to its parameters and its tab. The findings
    are live values: they follow the filters, and a run that skipped a step drops
    the rows that read it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have a filter bar (the sample and the caller agreement)
        that narrows that section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples, fusion calls, read support, validated calls |
        | Findings | Live result rows, then 4 figures: the caller UpSet, the breakpoint chord, the fusion allelic ratio scatter and the fusion protein structure |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the reads survive trimming and align to transcripts?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/rnafusion/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/rnafusion/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. The general statistics, the raw read quality beside the
    reads fastp kept, then STAR's alignment scores beside Picard's transcript
    region assignment. The post-trim read quality, insert size, gene body coverage
    and STAR gene counts are collapsed. Its sample filter reads the MultiQC report.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | *General statistics* |
        | Reads | 2 MultiQC panels |
        | Alignment | 2 MultiQC panels |
        | QC details (collapsed) | 4 MultiQC panels |

=== ":material-set-merge:{ .mc-violet } Caller Agreement"

    **Fusion calls** · *Which fusions did the callers agree on, and how are they ranked?*

    [![Caller Agreement dashboard](../../images/pipeline-templates/nf-core/rnafusion/caller_agreement_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/caller_agreement_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Caller Agreement dashboard](../../images/pipeline-templates/nf-core/rnafusion/caller_agreement_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/caller_agreement_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The distinct fusions ranked by 5' partner, the calls split by how many callers
    agree, the median Fusion Indication Index and the calls a knowledge base
    already lists. Then the UpSet of the fusions each combination of callers
    found, and the fusions fusion-report ranks highest, as bars of their index.
    The consensus table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Fusion Indication Index`, `Rank in the sample` and
        `Knowledge bases listing it` ranges, `Knowledge bases` and
        `5' partner gene`, all on `fusion_consensus`.

        | Section | What it holds |
        |---|---|
        | Agreement at a glance | 4 cards |
        | Caller concordance | 1 advanced visualization |
        | Ranked fusions | *Fusions by the index, highest first* |
        | Consensus table (collapsed) | *fusion-report consensus* |

=== ":material-chart-scatter-plot:{ .mc-teal } Caller Evidence"

    **Fusion calls** · *How much read support did each caller find for each fusion?*

    [![Caller Evidence dashboard](../../images/pipeline-templates/nf-core/rnafusion/caller_evidence_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/caller_evidence_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Caller Evidence dashboard](../../images/pipeline-templates/nf-core/rnafusion/caller_evidence_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/caller_evidence_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The caller reports by caller, their median read support, the total support per
    caller and the share of a fusion's reads one caller accounts for. Then the dot
    plot of read support per fusion and caller, and Arriba against STAR-Fusion on
    log axes, one point per fusion and sample. Each caller's own dot plot, on its
    own terms, and the caller tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller`, plus `Supporting reads` and `Caller share`
        ranges, all on `caller_evidence`.

        | Section | What it holds |
        |---|---|
        | Evidence at a glance | 4 cards |
        | Support across callers | 1 advanced visualization |
        | Arriba against STAR-Fusion | *Arriba against STAR-Fusion* |
        | Per caller detail (collapsed) | 3 advanced visualizations, one per caller |
        | Caller tables (collapsed) | *Per-caller evidence*, *Arriba calls*, *STAR-Fusion calls*, *FusionCatcher calls* |

=== ":material-vector-link:{ .mc-cyan } Breakpoints"

    **Fusion calls** · *Where on the genome do the two fusion partners sit?*

    [![Breakpoints dashboard](../../images/pipeline-templates/nf-core/rnafusion/breakpoints_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/breakpoints_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Breakpoints dashboard](../../images/pipeline-templates/nf-core/rnafusion/breakpoints_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/breakpoints_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Arriba's calls as loci. Its calls by event class, the calls between
    chromosomes by confidence, the share of the local reads that support a call
    and the split reads. Then the flow from the contig of the 5' partner to that
    of the 3' partner beside the chord ring of the same calls, and the read
    support by event class and by breakpoint site.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Partner contigs`, `Event class` and `Arriba confidence` on
        `arriba_fusions`. They narrow the Arriba calls, not the chord, which the
        sample and fusion filters reach.

        | Section | What it holds |
        |---|---|
        | Breakpoints at a glance | 4 cards |
        | Partner contigs | 2 advanced visualizations |
        | Event classes | *Read support by event class*, *Read support by breakpoint site* |

=== ":material-check-decagram:{ .mc-grape } Validation"

    **Follow-up** · *Which calls hold up when the reads are re-aligned?*

    [![Validation dashboard](../../images/pipeline-templates/nf-core/rnafusion/validation_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/validation_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Validation dashboard](../../images/pipeline-templates/nf-core/rnafusion/validation_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/validation_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    FusionInspector's re-quantified calls. The validated fusions by predicted
    protein, the median fragments per million against STAR-Fusion's default
    floor, the share of the support that crosses the junction and the re-aligned
    support. Then the abundance by predicted protein, and the 5' against the 3'
    fusion allelic ratio on log axes beside the record of the call you pick: a
    call supported on one side only falls off the diagonal.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Predicted protein` and a `Fragments per million` range on
        `fusioninspector_fusions`.

        | Section | What it holds |
        |---|---|
        | Validation at a glance | 4 cards |
        | Validated abundance | 1 advanced visualization |
        | Allelic ratio | *Fusion allelic ratio, both sides* + a validated call record card |
        | Validated rows (collapsed) | *FusionInspector validation* |

=== ":material-shape-outline:{ .mc-pink } Protein Domains"

    **Follow-up** · *Which protein domains would each fusion protein keep?*

    [![Protein Domains dashboard](../../images/pipeline-templates/nf-core/rnafusion/protein_domains_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/protein_domains_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Protein Domains dashboard](../../images/pipeline-templates/nf-core/rnafusion/protein_domains_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/protein_domains_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The Pfam domains of both partners. The domain hits by partner side, the hits
    the breakpoint cuts through, the domain length and the hit strength. Then the
    fusion protein structure, the fusions with the most domains drawn as their
    partners end to end, and the lollipop of every domain at its start position. A
    domain name ending in `PARTIAL` is one the breakpoint cuts through.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Partner side` and `Predicted protein` on
        `fusion_protein_domains`.

        | Section | What it holds |
        |---|---|
        | Domains at a glance | 4 cards |
        | Fusion protein structure | 1 advanced visualization |
        | Domain positions | 1 advanced visualization |
        | Domain table (collapsed) | *Pfam domains* |

=== ":material-waves:{ .mc-blue } Splice Junctions"

    **Follow-up** · *Which splice junctions do the reads support, and how strongly?*

    [![Splice Junctions dashboard](../../images/pipeline-templates/nf-core/rnafusion/splice_junctions_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/splice_junctions_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Splice Junctions dashboard](../../images/pipeline-templates/nf-core/rnafusion/splice_junctions_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnafusion/splice_junctions_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    CTAT-splicing's junctions. The distinct junctions ranked by gene, the unique
    read support, the reads summed over every junction by chromosome and the
    intron length. Then the Manhattan of junction support along the genome and
    the junction arcs over the busiest loci.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Chromosome` and a `Unique read support` range on
        `splice_junctions`.

        | Section | What it holds |
        |---|---|
        | Junctions at a glance | 4 cards |
        | Junction landscape | 1 advanced visualization |
        | Junction arcs | 1 advanced visualization |
        | Junction table (collapsed) | *Splice junctions* |

!!! tip "Splice junctions are keyed on the intron"
    CTAT-splicing scores the introns of a gene, so a fusion name has nothing to
    match against. The fusion filters stay off the Splice Junctions tab on
    purpose: the sample filters and the tab's own junction filters narrow it.

Fusions select on `fusion`: the ranked fusion bars, the *Arriba against
STAR-Fusion* and allelic-ratio scatters, and the consensus, evidence, caller,
FusionInspector and Pfam tables. The sample sheet selects on `sample`, and the
junction Manhattan and junction table select on `gene`, which stays inside the
Splice Junctions tab. A pick narrows every tile that reads the same collection or
one linked from it. The partner chords, the flow, the UpSet and the dot plots do
not select.

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
depictio ingest results/ \
  --template nf-core/rnafusion/latest
```

See [nf-co.re/rnafusion/usage](https://nf-co.re/rnafusion/4.1.3/docs/usage)
for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
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
depictio ingest "$DEST" --template nf-core/rnafusion/latest
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it a Draft.</span>
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
