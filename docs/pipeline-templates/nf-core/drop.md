---
title: RNA outlier detection
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/drop" target="_blank" title="nf-core/drop on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/drop/master/docs/images/nf-core-drop_logo_dark.png" alt="nf-core/drop">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/drop/master/docs/images/nf-core-drop_logo_light.png" alt="nf-core/drop">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">RNA outlier detection</h1>
    <p class="template-subtitle">RNA-seq outliers for rare-disease diagnosis: the genes that stand out in a sample from aberrant expression, aberrant splicing and mono-allelic expression, ranked by how many analyses agree, and located on the genome.</p>
    <p class="template-links">
      <a href="https://nf-co.re/drop" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/drop" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="1.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.0.0" selected>1.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The drop template follows an nf-core/drop run from the sample sheet to the genes
that stand out in a patient's RNA:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-account-search-outline: **Candidates**: each sample's genes ranked by how many analyses call them, with the evidence of each
- :material-chart-bell-curve: **Expression**: OUTRIDER aberrant expression, as a volcano and the samples and genes with the most hits
- :material-content-cut: **Splicing**: FRASER aberrant splicing, as a volcano and what the hit junctions do
- :material-set-split: **Mono-allelic**: heterozygous variants read from one allele only
- :material-map-search-outline: **Locus**: the called genes on the genome, with a browser on the reads and genotypes


<div class="tpl-showcase">
  <div class="tpl-showcase-bar">
    <span class="tpl-showcase-live"></span>
    <span class="tpl-showcase-label">Live showcase</span>
    <span class="tpl-showcase-meta">nf-core/drop, nf-core test data</span>

    <a class="tpl-showcase-open" href="https://showcases.depictio.embl.org/dashboard/6ae7927543b7dac81c0fb760" target="_blank" rel="noopener"><i class="mdi mdi-open-in-new"></i> Open</a>
  </div>
  <iframe class="tpl-showcase-frame" src="https://showcases.depictio.embl.org/dashboard/6ae7927543b7dac81c0fb760" loading="lazy" title="nf-core/drop showcase dashboard" allowfullscreen></iframe>
</div>

The persistent `Sample filters` (group, sample) and `Gene filters` (gene symbol) sit
in the left panel and narrow every tab through the project links.

!!! info "A small run calls nothing"
    OUTRIDER and FRASER need about 30 samples per group. Below that every
    adjusted p-value tends to 1 and zero calls is the expected answer. The
    tables therefore also carry a **nominal** status (raw p-value of 0.05 or
    less, not called): a lead to check in the reads, never a finding.

!!! tip "Give the volcanoes a cloud"
    A default run writes only the rows that pass the cut-offs, so a volcano
    shows its hits and nothing behind them. Run the pipeline with
    `--ae_padj_cutoff 1 --ae_z_score_cutoff 0 --as_padj_cutoff 1 --as_delta_psi_cutoff 0`
    to keep every tested gene and junction. A default run still works.


---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/drop_results \
      --template nf-core/drop/latest
    ```

    The results directory is the only thing you have to pass, with one
    exception: drop does not publish the sample sheet it ran on. The template
    looks for it at `{DATA_ROOT}/input/samplesheet.tsv`; copy it there, or point
    to it:

    ```bash
    depictio ingest /path/to/drop_results \
      --template nf-core/drop/latest \
      --var SAMPLESHEET=/path/to/samplesheet.tsv
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `SAMPLESHEET` | `input/samplesheet.tsv` | the sample sheet given to `--input` |
    | `GROUP_COL` | `drop_group` | column the dashboard groups and filters samples by |
    | `GENOME` | `hg38` | UCSC assembly the browser and the locus links open on |
    | `TRACKS_URI` | unset | `s3://` or `https://` folder that relative BAM and VCF paths of the sheet are read under, in place |
    | `AE_PADJ`, `AS_PADJ`, `MAE_PADJ` | `0.05`, `0.1`, `0.05` | adjusted p-value cut-offs of an OUTRIDER, FRASER and mono-allelic call |

    Further cut-offs (`AE_MIN_Z`, `AS_MIN_DPSI`, `MAE_MIN_RATIO`, `NOMINAL_P`,
    `BACKGROUND_ROWS`, `CANDIDATES_PER_SAMPLE`) are listed in the reference below.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/drop -r 1.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so put a copy of the sample sheet at
    `results/input/samplesheet.tsv` before the run.


---

## :material-book-open-variant: Reference

The template reads the OUTRIDER, FRASER and mono-allelic result tables, the gene
name mapping that gives expression calls a position, the sample sheet and the run
parameters. Each analysis is optional (`--ae_skip`, `--as_skip`, `--mae_skip`):
the collections of a skipped one are pruned with their tiles, and a tab left
without data is dropped. DROP renders its report from R rather than MultiQC
modules, so the template has no MultiQC tab; the same answers are rebuilt from the
result tables.

A sample can belong to several DROP groups. The sample hub keeps the most specific
one (the group the fewest samples share) as `drop_group`. OUTRIDER and FRASER write
only the rows that pass their cut-offs, so the expression and splicing recipes keep
a row when it is called, when its adjusted p-value is 0.5 or less, or when it is one
of the `BACKGROUND_ROWS` (300) most significant of its sample. The calls are read
before that trim and do not change with it, but the kept rows are not a fair sample
of the tests, so the dashboard draws no QQ view for these two analyses.

| Cut-off variable | Default | Role |
|---|---|---|
| `AE_MIN_Z` | `0` | minimum absolute z-score of an OUTRIDER call |
| `AS_MIN_DPSI` | `0.3` | minimum absolute delta PSI of a FRASER call |
| `MAE_MIN_RATIO` | `0.8` | minimum allele share of a mono-allelic call |
| `NOMINAL_P` | `0.05` | raw p-value at or below which a row is a nominal hit |
| `BACKGROUND_ROWS` | `300` | background rows kept per sample by the expression and splicing tables |
| `CANDIDATES_PER_SAMPLE` | `25` | best-supported genes per sample kept in the triage list besides the called ones |

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. The per-sample table is always built, so
    the Overview key figures survive any combination of analyses.

<div class="tpl-version-block" data-version="1.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/drop-latest.md"

</div>


---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a
funnel from the run to the genes that stand out in a sample. Each tab below
carries the **same icon and colour the dashboard gives it**, so the page and the
app read alike.

| Group | Tabs |
|---|---|
| Triage | Candidates |
| Analyses | Expression, Splicing, Mono-allelic, Locus |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *RNA outliers, from the reads to the genes that stand out.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/drop/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/drop/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards for the run (samples, groups, the OUTRIDER and FRASER implementations) and a
    six-step *Pipeline* (group, count, expression, splicing, alleles, locate), each
    linked to its parameters and its tab. Four key figures: the cohort size, the
    outliers called, the heaviest sample and the calls on a phenotype gene. The
    findings are live values that follow the filters, with the nominal hits beside the
    calls, then the hits in each sample and the three volcanoes.

=== ":material-account-search-outline:{ .mc-red } Candidates"

    **Triage** · *Which genes stand out in a sample, and in how many analyses?*

    [![Candidates dashboard](../../images/pipeline-templates/nf-core/drop/candidates_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/candidates_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Candidates dashboard](../../images/pipeline-templates/nf-core/drop/candidates_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/candidates_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A ranked list of the genes of the picked sample, the strongest evidence first
    (the analyses that call each gene, the support, the phenotype match), beside a
    record card for the picked gene. Below, a gene by analysis grid of the cohort's
    best-supported genes: a gene lit in one column only has one analysis behind it.
    Filters: how many analyses call the gene, and the phenotype match.

=== ":material-chart-bell-curve:{ .mc-blue } Expression"

    **Analyses** · *Which genes are expressed far from what the cohort predicts?*

    [![Expression dashboard](../../images/pipeline-templates/nf-core/drop/expression_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/expression_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Expression dashboard](../../images/pipeline-templates/nf-core/drop/expression_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/expression_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The OUTRIDER volcano of fold change against the raw p-value, coloured by status
    (called, nominal only, not significant), then the samples with the most hits and the
    genes hit in the most samples, which are more often technical. The result table and
    its record card are collapsed. Filters: call direction and absolute z-score.

=== ":material-content-cut:{ .mc-orange } Splicing"

    **Analyses** · *Which junctions are used far more or less than in the cohort?*

    [![Splicing dashboard](../../images/pipeline-templates/nf-core/drop/splicing_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/splicing_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Splicing dashboard](../../images/pipeline-templates/nf-core/drop/splicing_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/splicing_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The FRASER volcano of delta PSI against the raw p-value, the samples with the most
    hits, and what the hit junctions do (an intron used less or more, an exon extended
    or shortened), for the genes called and for every hit at the raw p-value. The
    junction table is collapsed. Filters: call direction, absolute delta PSI and
    splicing metric.

=== ":material-set-split:{ .mc-teal } Mono-allelic"

    **Analyses** · *Which variants are read from one allele only?*

    [![Mono-allelic dashboard](../../images/pipeline-templates/nf-core/drop/mono_allelic_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/mono_allelic_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Mono-allelic dashboard](../../images/pipeline-templates/nf-core/drop/mono_allelic_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/mono_allelic_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The volcano of the allelic ratio against the raw p-value, full width. The variant
    table and its record card are collapsed. Only samples with a DNA genotype take part,
    so a cohort without one drops the tab. Filters: call and alternative allele share.

=== ":material-map-search-outline:{ .mc-indigo } Locus"

    **Analyses** · *Where on the genome do the called genes sit, and what do the reads show?*

    [![Locus dashboard](../../images/pipeline-templates/nf-core/drop/locus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/locus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Locus dashboard](../../images/pipeline-templates/nf-core/drop/locus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/drop/locus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One navigator carries the genes of every sample's triage list on a genome axis, one
    lane per sample coloured by group, linked to a genome browser with the alignments
    (with splice-junction arcs) and genotypes of the samples in view. A brush, a pan or a
    typed locus moves the browser, and the cards recount on the region. The volcanoes of
    the three analysis tabs open genes in this browser.

Tables select rows: on `sample` in the sample sheet and on `call_id` in the triage
list and the three call tables. A pick narrows the other tiles of its collection
and follows the project links to the rest.


---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/drop, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/drop -r 1.0.0 \
  --input samplesheet.tsv \
  --outdir results \
  -profile docker
```

Then point Depictio at the results, naming the sample sheet the pipeline did not
publish:

```bash
depictio ingest results/ \
  --template nf-core/drop/latest \
  --var SAMPLESHEET=samplesheet.tsv
```

See [nf-co.re/drop/usage](https://nf-co.re/drop/1.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/
│   └── samplesheet.tsv                         # --var SAMPLESHEET (not published by the pipeline)
├── pipeline_info/params_*.json
└── processed_results/
    ├── aberrant_expression/<annotation>/outrider/<group>/OUTRIDER_results.tsv
    ├── aberrant_splicing/results/<annotation>/fraser/<group>/results.tsv
    └── mae/
        ├── <group>/MAE_results_all_<annotation>.tsv.gz
        └── gene_name_mapping_<annotation>.tsv  # optional: gives expression calls a locus
```

The Locus tab reads the alignments (`RNA_BAM_FILE`) and genotypes (`DNA_VCF_FILE`)
that the sample sheet points at, not pipeline outputs. Paths under `DATA_ROOT` are
uploaded at ingestion; `https://` and `s3://` paths are read in place.

---

## :material-flask-outline: Validation runs

The AWS megatest bucket publishes no result tables for drop, so the template was
validated on the real DROP outputs of the pipeline's own small test run, published
in the nf-core/test-datasets `drop` branch.
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/drop/1.0.0/download_test_data.sh)
lays them out the way the pipeline writes them (about 55 MB) and copies the
vendored sample sheet into `input/`:

```bash
bash depictio/projects/nf-core/drop/1.0.0/download_test_data.sh /tmp/drop_test
depictio ingest /tmp/drop_test --template nf-core/drop/latest
```

That run is degenerate on purpose (ten samples, no significant call), so it
exercises the recipes and the layout rather than the statistics.

---

## :material-link-variant: Additional resources

- [nf-co.re/drop](https://nf-co.re/drop): official pipeline documentation
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it from Reviewed.</span>
    <span class="tpl-person"><i class="mdi mdi-account-plus-outline"></i> Open</span>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/drop releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
