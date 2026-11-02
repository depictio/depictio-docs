---
title: Stable reference genes
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/stableexpression" target="_blank" title="nf-core/stableexpression on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/stableexpression/master/docs/images/nf-core-stableexpression_logo_dark.png" alt="nf-core/stableexpression">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/stableexpression/master/docs/images/nf-core-stableexpression_logo_light.png" alt="nf-core/stableexpression">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Stable reference genes</h1>
    <p class="template-subtitle">The public datasets that reached the merged matrix, how their gene ids map to Ensembl, then the most stable genes at each expression level and what makes each candidate stable.</p>
    <p class="template-links">
      <a href="https://nf-co.re/stableexpression" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/stableexpression" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.1.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.1.0" selected>1.1.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The stableexpression template follows an nf-core/stableexpression run from the
public expression datasets of one species to the genes that hold steadiest across
them, the reference genes a qPCR assay can normalise against:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-database-outline: **Datasets**: which datasets reached the merged matrix, and how many samples each step kept
- :material-tag-outline: **ID mapping**: the fate of each dataset's gene ids
- :material-trophy-outline: **Ranking**: the most stable genes of each expression section, with their stability score
- :material-scale-balance: **Candidates**: the parts of the score and the agreement of Normfinder and geNorm
- :material-layers-outline: **Sections**: scores, variation and mean expression across the sections

The persistent `Sample filters` (group, dataset, sample) sit in the collapsed left
panel. They narrow the dataset tabs and the per-sample values of the Ranking tab,
and never move a stability score, which is a statistic of the whole cohort.

!!! info "No MultiQC tab"
    A 1.1.0 run writes a MultiQC report of custom content only, and a Plotly Dash
    app. The pinned test run published neither, so the template declares no
    MultiQC collection and has no MultiQC tab.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/stableexpression_results \
      --template nf-core/stableexpression/latest
    ```

    stableexpression takes a species, not a samplesheet, so there is nothing to
    supply: the design is `merged_data/whole_design.csv`, written by the run.
    `METADATA_FILE` can point to an annotated copy with extra columns (tissue,
    treatment), and `GROUP_COL` (default `platform`) can name any of them. For a run
    with `--skip_id_mapping`, pass `--var NO_ID_MAPPING=true`.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/stableexpression -r 1.1.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the merged design, the per-dataset design files and
statistics, the error and warning tables of the ID mapping, the gene summary with
the stability measures, and the merged gene by sample matrix before imputation.
The ID mapping collection is optional.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="1.1.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/stableexpression-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a
funnel from the datasets in the merged matrix to the genes that hold steadiest in
it. Each tab below carries the **same icon and colour the dashboard gives it**.

| Group | Tabs |
|---|---|
| Data & QC | Datasets, ID mapping |
| Stability | Ranking, Candidates, Sections |

=== ":material-compass-outline: Overview"

    *The most stable genes across public expression data.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/stableexpression/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/stableexpression/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A hero links the run parameters. *The run* gives the species, the datasets merged,
    the samples analysed, the genes in the matrix and the sections and candidates per
    section, and *Pipeline* walks five steps (download, map, filter, score, rank). Four
    key figures: datasets, samples analysed, genes and the best stability score. The
    group and dataset filters narrow the first two; the gene cards are cohort-wide.

=== ":material-database-outline:{ .mc-blue } Datasets"

    **Data & QC** · *Which datasets reached the merged matrix, and with how many samples?*

    [![Datasets dashboard](../../images/pipeline-templates/nf-core/stableexpression/datasets_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/datasets_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Datasets dashboard](../../images/pipeline-templates/nf-core/stableexpression/datasets_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/datasets_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Datasets and samples through the steps (download, ID mapping, zero filter,
    missing-value filter), the samples after each step by platform, and the share of the
    genes each dataset misses, one strip per array design. The dataset table with its
    record card is collapsed. Filters: outcome and samples kept.

=== ":material-tag-outline:{ .mc-cyan } ID mapping"

    **Data & QC** · *How many gene ids of each dataset map to an Ensembl gene?*

    [![ID mapping dashboard](../../images/pipeline-templates/nf-core/stableexpression/id_mapping_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/id_mapping_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![ID mapping dashboard](../../images/pipeline-templates/nf-core/stableexpression/id_mapping_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/id_mapping_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One stacked bar per dataset of the fate of its gene ids, grouped by platform and
    sorted by the share kept, then the fate per platform. Filters: fate and dataset
    outcome. A run with `--skip_id_mapping` drops this tab.

=== ":material-trophy-outline:{ .mc-grape } Ranking"

    **Stability** · *Which genes are the most stable at each expression level?*

    [![Ranking dashboard](../../images/pipeline-templates/nf-core/stableexpression/ranking_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/ranking_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Ranking dashboard](../../images/pipeline-templates/nf-core/stableexpression/ranking_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/ranking_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The best genes of each section as boxes of normalised expression with their
    stability score, lower being steadier. Top N and a section filter set what is
    ranked. Below, the same leaders as violins from the per-sample values, the one gene
    tile the sample filters redraw. Filters: section, score and measured share.

=== ":material-scale-balance:{ .mc-violet } Candidates"

    **Stability** · *What makes a candidate stable, measure by measure?*

    [![Candidates dashboard](../../images/pipeline-templates/nf-core/stableexpression/candidates_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/candidates_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Candidates dashboard](../../images/pipeline-templates/nf-core/stableexpression/candidates_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/candidates_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Each section's score split into its five parts, then Normfinder rank against geNorm
    M rank within the section, one point per candidate. The candidate table with its
    record card is collapsed. Filters: section, expression level and measured share.

=== ":material-layers-outline:{ .mc-indigo } Sections"

    **Stability** · *How does stability change with expression level?*

    [![Sections dashboard](../../images/pipeline-templates/nf-core/stableexpression/sections_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/sections_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Sections dashboard](../../images/pipeline-templates/nf-core/stableexpression/sections_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/stableexpression/sections_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The candidates' scores per section, every gene's coefficient of variation per
    section (candidates beside the rest) and every gene by mean expression against
    variation. Filters: expression level, candidacy and platforms.

The dataset table selects on `dataset`, which reaches the funnel and the ID mapping.
The ranking, the candidate table and the scatters select on `gene_id`, which
reaches the per-sample values.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/stableexpression, it does not run the pipeline.
Run the pipeline first, with the species to study:

```bash
nextflow run nf-core/stableexpression -r 1.1.0 \
  --species homo_sapiens \
  -profile docker --outdir results
```

Then point Depictio at the results:

```bash
depictio ingest results/ --template nf-core/stableexpression/latest
```

See [nf-co.re/stableexpression/usage](https://nf-co.re/stableexpression/1.1.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── reporting/all_genes_summary.csv            # every gene: statistics, section, measures, score, rank
├── merged_data/
│   ├── whole_design.csv                       # the hub: one row per sample (METADATA_FILE)
│   └── all_counts.parquet                     # the merged matrix before imputation
├── datasets/<platform>/<normalisation>/<dataset>/<dataset>.design.csv
├── statistics/*.csv                           # ID mapping, filter, zero, null and skewness tables
├── errors/renaming_failure_reasons.tsv
├── warnings/renaming_warning_reasons.tsv
└── pipeline_info/
```

The per-step dataset matrices under `datasets/` and the imputed matrix are not read.

---

## :material-flask-outline: Validation runs

The 1.1.0 release prefix of the AWS megatests holds `pipeline_info/` only, so the
template was validated against
`s3://nf-core-awsmegatests/stableexpression/results-d6b1654c4784332cbad71f1d928cc8b75a77272f/`,
a complete test_full run (Homo sapiens) written by a development build
(`v1.0.0-gd6b1654`), which published neither the MultiQC report nor the Dash app.
`megatest.yaml` lists the tables-only subset the template needs (about 358 MB, the
merged matrix being most of it):

```bash
bash depictio/projects/nf-core/stableexpression/1.1.0/download_test_data.sh /tmp/stableexpression_test
depictio ingest /tmp/stableexpression_test --template nf-core/stableexpression/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/stableexpression](https://nf-co.re/stableexpression): official pipeline documentation
- [nf-co.re/stableexpression/1.1.0/results](https://nf-co.re/stableexpression/1.1.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/stableexpression releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
