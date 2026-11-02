---
title: Epitope prediction
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/epitopeprediction" target="_blank" title="nf-core/epitopeprediction on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/epitopeprediction/master/docs/images/nf-core-epitopeprediction_logo_dark.png" alt="nf-core/epitopeprediction">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/epitopeprediction/master/docs/images/nf-core-epitopeprediction_logo_light.png" alt="nf-core/epitopeprediction">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Epitope prediction</h1>
    <p class="template-subtitle">MHC binding predicted for the peptides of variants, proteins or peptide tables: which alleles the peptides bind, sample by sample, which peptides bind and where they come from, and how far the prediction tools agree.</p>
    <p class="template-links">
      <a href="https://nf-co.re/epitopeprediction" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/epitopeprediction" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="3.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="3.2.0" selected>3.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The epitopeprediction template follows an nf-core/epitopeprediction run from the
alleles the peptides bind to the peptides that bind and the tools behind the
calls:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, with the binder statistics of every sample and tool
- :material-shield-account-outline: **Neoepitopes**: which alleles the peptides bind, which peptides bind and where they come from, and how far the prediction tools agree

The persistent `Sample filters` (input type, sample and MHC class) sit in the
left panel and narrow every tab. A sample is one of three inputs: a VCF of
somatic variants, a protein FASTA or a peptide table, and the input type is the
default grouping.

!!! info "The samplesheet is not published by the pipeline"
    The hub of the dashboard is the samplesheet the run was started with
    (`sample`, `alleles`, `mhc_class`, `filename`, and for variant input
    `tumor_sample` and `germline_vcf`). It is not part of the published output,
    so copy it under `input/` in the results directory, or pass
    `--var METADATA_FILE=...`.

!!! info "Allele spelling matches nf-core/hlatyping"
    Alleles are normalised to two fields, `HLA-A*02:01`, the spelling the
    [hlatyping](hlatyping.md) template uses. A typed sample's `alleles` list can
    go straight into this pipeline's samplesheet. The two runs are separate
    projects, so a pick in one does not filter the other.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/epitopeprediction_results \
      --template nf-core/epitopeprediction/latest \
      --var METADATA_FILE=/path/to/samplesheet.csv
    ```

    The results directory is the only required value when the samplesheet sits at
    `{DATA_ROOT}/input/samplesheet.csv`.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | `{DATA_ROOT}/input/samplesheet.csv` | the samplesheet the run was started with |
    | `GROUP_COL` | `input_type` | column the dashboard groups and filters samples by; `input_type` (Variants, Proteins or Peptides) is derived from the input file |
    | `GROUP_COL_DISPLAY` | `Input type` | reader-facing label of `GROUP_COL` in filters and cards |
    | `NO_VARIANT_INPUT` | unset | set for a sheet with no VCF: drops the variant peptides and the mutant against wild type pairs |
    | `NO_WILD_TYPE` | unset | set for a run without `--wild_type`: drops the mutant against wild type pairs |
    | `SINGLE_PREDICTOR` | unset | set for a run with one tool per MHC class: drops the tool agreement |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/epitopeprediction -r 3.2.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so put a copy of the samplesheet at
    `results/input/samplesheet.csv` before the run.

---

## :material-book-open-variant: Reference

The template reads the samplesheet, the merged predictions (one table per
sample, in the long shape or with `--wide_format_output`), the candidate
peptides cut from the variants and the MultiQC report. The affinity is the
pipeline's 0 to 1 score converted back to an IC50 in nM, and a binder is the
call of the pipeline, per tool. The per-tool directories repeat the merged
predictions and are not read.

The mutant against wild type pairs, the variant peptides and the tool agreement
are optional collections: an ingest that finds nothing to pair skips them, and
their tiles are pruned even when the variable is not set.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="3.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/epitopeprediction-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then four child tabs in two groups, read from
the binder statistics to the agreement between tools. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read
alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC |
| Neoepitopes | Predictions, Peptides, Predictors |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *MHC binding prediction, from variants, proteins or peptides to the binders.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    *The run* lists the samples, the alleles scored, the tools and the peptide
    lengths, and *Pipeline* walks five steps (peptides, lengths, predict, call,
    compare), each linked to its parameters and its tab. Four key figures: the
    samples, the peptides, the alleles and the predicted binders. The findings are
    live rows (the allele that binds the most peptides, the share of peptides that
    bind, the mutant peptides that bind where their wild type does not, the tool
    agreement) and four figures.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *How many peptides does each tool call a binder?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: the binders, non-binders and unsupported peptides
    per sample and tool, the rank and affinity distributions and the binder length
    distribution. The general statistics and the bcftools panels of the VCF inputs
    are collapsed; a run without variant input has no bcftools panels.

=== ":material-shield-account-outline:{ .mc-blue } Predictions"

    **Neoepitopes** · *Which alleles do the peptides bind, sample by sample?*

    [![Predictions dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/predictions_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/predictions_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Predictions dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/predictions_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/predictions_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The predictions by IC50 band, the binder calls, the alleles scored and the
    median IC50 against the 500 nM binder line. Then the allele by sample dot plot
    (thirty alleles whose median affinity differs most between samples; dot size is
    the binder share, colour the median affinity), the log10 IC50 histogram by tool
    and the predictions per sample by IC50 band. Filters: allele, HLA locus, tool
    and an IC50 range. The tables are collapsed.

=== ":material-dna:{ .mc-violet } Peptides"

    **Neoepitopes** · *Which peptides bind, and which variant or protein do they come from?*

    [![Peptides dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/peptides_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/peptides_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Peptides dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/peptides_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/peptides_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The peptides by binder call, the predicted binders, the alleles per binder and
    the median best IC50. Then the peptides by length stacked by call, and the
    mutant against wild type IC50 of every missense mutant whose wild type was
    predicted: below the diagonal the mutation strengthens binding. The candidate
    peptides cut from the variants and the peptide table, with its record card, are
    collapsed. Filters: binder call, peptide length and origin.

=== ":material-compare-horizontal:{ .mc-grape } Predictors"

    **Neoepitopes** · *How far do the prediction tools agree on the binders?*

    [![Predictors dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/predictors_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/predictors_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Predictors dashboard](../../images/pipeline-templates/nf-core/epitopeprediction/predictors_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/epitopeprediction/predictors_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The binders per tool, the binder share per sample and tool, the peptides a tool
    could not score and the most alleles a tool scored in one sample. Then the
    binder share per sample and tool, IC50 against percentile rank for every
    prediction with a line at 500 nM, and one tool's IC50 against another's for
    the peptides both scored (colour is who calls a binder). Filters: tool and
    agreement. The per-tool and paired-prediction tables are collapsed.

A pick on a sample reaches every collection and the MultiQC panels, and an allele
pick reaches the allele summary, the agreement and the mutant against wild type
pairs through the project links.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/epitopeprediction, it does not run the
pipeline. Run the pipeline first:

```bash
nextflow run nf-core/epitopeprediction -r 3.2.0 \
  --input samplesheet.csv \
  --tools mhcflurry,mhcnuggets \
  --wild_type \
  --outdir results \
  -profile docker
```

The samplesheet is `sample,alleles,mhc_class,filename` (plus `tumor_sample` and
`germline_vcf` for variant input). `--tools` takes one or several predictors,
and `--wild_type` also scores the wild-type peptide of each missense mutant.
Copy the samplesheet under `results/input/`, then point Depictio at the results:

```bash
depictio ingest results/ --template nf-core/epitopeprediction/latest
```

See [nf-co.re/epitopeprediction/usage](https://nf-co.re/epitopeprediction/3.2.0/docs/usage)
for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio
scans recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/samplesheet.csv                       # --var METADATA_FILE (not published by the pipeline)
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/multiqc_data/multiqc.parquet
├── predictions/<sample>.tsv                    # merged predictions, long or wide
└── variant_peptides/<sample>_length_<k>.tsv    # optional; VCF input only
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/epitopeprediction/3.2.0/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs
and copies the vendored samplesheet into `input/`:

```bash
bash depictio/projects/nf-core/epitopeprediction/3.2.0/download_test_data.sh \
  /tmp/epitopeprediction_test
depictio ingest /tmp/epitopeprediction_test \
  --template nf-core/epitopeprediction/latest
```

The run is
`s3://nf-core-awsmegatests/epitopeprediction/results-e637bc7c49e6e05a09f5207501a142ec68d8570b/`,
the 3.2.0 `test_full` run: eleven samples on synthetic data that exercise every
input route (six VCFs, a protein FASTA and four peptide tables, two of them
predicted against every supported allele), with MHCflurry, MHCnuggets and
MHCnuggets II, the wide output format and `--wild_type`. It is a test of the
pipeline, not a cohort.

---

## :material-link-variant: Additional resources

- [nf-co.re/epitopeprediction](https://nf-co.re/epitopeprediction): official pipeline documentation
- [nf-co.re/epitopeprediction/results](https://nf-co.re/epitopeprediction/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/epitopeprediction releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
