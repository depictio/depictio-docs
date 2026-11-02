---
title: DIA proteomics
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/quantms" target="_blank" title="nf-core/quantms on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/quantms/master/docs/images/nf-core-quantms_logo_dark.png" alt="nf-core/quantms">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/quantms/master/docs/images/nf-core-quantms_logo_light.png" alt="nf-core/quantms">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">DIA proteomics</h1>
    <p class="template-subtitle">Label-free DIA proteomics, from the spectra to the proteins that change: whether the runs were acquired alike, what each run identified, how completely proteins were quantified, whether replicates agree, and which proteins differ between conditions.</p>
    <p class="template-links">
      <a href="https://nf-co.re/quantms" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/quantms" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.1.1">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.1.1" selected>1.1.1</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The quantms template reads the DIA route of an nf-core/quantms run and follows it
from the spectra to the proteins that change between conditions:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-waveform: **Acquisition**: whether the runs were acquired alike, from the mzML spectrum statistics
- :material-magnify-scan: **Identification**: the precursors each run identified and their quality, from DIA-NN
- :material-molecule: **Proteins**: the protein groups quantified, how completely, and how much they vary between runs
- :material-set-merge: **Reproducibility**: whether the runs of a condition agree and the conditions separate
- :material-chart-scatter-plot: **Differential abundance**: the MSstats contrasts, with the volcano and the calibration of the test


<div class="tpl-showcase">
  <div class="tpl-showcase-bar">
    <span class="tpl-showcase-live"></span>
    <span class="tpl-showcase-label">Live showcase</span>
    <span class="tpl-showcase-meta">nf-core/quantms, nf-core test data</span>

    <a class="tpl-showcase-open" href="https://showcases.depictio.embl.org/dashboard/6ae792dd4156ddc555564b18" target="_blank" rel="noopener"><i class="mdi mdi-open-in-new"></i> Open</a>
  </div>
  <iframe class="tpl-showcase-frame" src="https://showcases.depictio.embl.org/dashboard/6ae792dd4156ddc555564b18" loading="lazy" title="nf-core/quantms showcase dashboard" allowfullscreen></iframe>
</div>

The persistent `Sample filters` (condition, run) sit in the left panel and narrow
every tab: the links carry a pick to every run-level table by `run_id` and to the
per-condition tables by condition.

!!! info "DIA only"
    quantms quantifies proteins in three modes: data-dependent acquisition with
    label-free quantification, isobaric labelling and data-independent
    acquisition (DIA). This template reads the DIA route (DIA-NN and MSstats).
    The other two write other tables and need their own template.


---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/quantms_results/mode_dia \
      --template nf-core/quantms/latest
    ```

    The directory to pass is the one holding `diannsummary/`, `msstats/`,
    `mzmlstatistics/`, `sdrfparsing/` and `pipeline_info/`: that of one mode, which
    is `mode_dia/` for the nf-core megatest. The design is read from
    `sdrfparsing/`, so no SDRF is needed; the SDRF only adds its characteristics
    columns (organism, instrument and so on):

    ```bash
    depictio ingest /path/to/quantms_results/mode_dia \
      --template nf-core/quantms/latest \
      --var METADATA_FILE=/path/to/sdrf.tsv
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | `{DATA_ROOT}/input/sdrf.tsv` | the SDRF the run was started with (optional) |
    | `GROUP_COL` | `condition` | column the dashboard groups and filters runs by; leave it at the MSstats condition |
    | `GROUP_COL_DISPLAY` | `Condition` | reader-facing label of `GROUP_COL` in filters and cards |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/quantms -r 1.1.1 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).


---

## :material-book-open-variant: Reference

The template reads the design quantms parsed from the SDRF, the mzML spectrum
statistics, the DIA-NN precursor report and protein-group matrix, and the MSstats
comparisons. Derived collections (the run summary, the protein summary, the
per-condition statistics, the run projection and the replicate pairs) are recipes
over those tables. There is no MultiQC tab: quantms 1.1.1 reports through pmultiqc
custom content, which has no `multiqc.parquet`, so the plots of that report are
rebuilt from the result tables.

A call is an Up or Down protein at an adjusted p-value below 0.05 and an absolute
log2 fold change of at least one, the dashboard's cut-offs (MSstats reports the
adjusted p-value only). The coefficient of variation is taken over the runs of a
condition that quantified the group, and needs at least two. The DIA-NN version of
this release reports no mass error, so Identification has no mass-accuracy view.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. With one condition there is no contrast,
    and Differential abundance shows empty panels.

<div class="tpl-version-block" data-version="1.1.1" markdown>

--8<-- "pipeline-templates/nf-core/_generated/quantms-latest.md"

</div>


---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a
funnel from the spectra to the proteins that change. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | Acquisition, Identification |
| Quantification | Proteins, Reproducibility, Differential abundance |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and record cards follow, collapsed. The *Sample sheet*
and the *Reference tables* (the per-run summary) are pinned, collapsed, to the
bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Label-free DIA proteomics, from the spectra to the proteins that change.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/quantms/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/quantms/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Hero, *About* and run cards (runs, conditions, acquisition method, enzyme,
    tolerances, search database) and a five-step *Pipeline* (acquire, identify,
    quantify, compare runs, test). Four key figures: the runs, the protein groups per
    run, the median variation between replicates (a threshold at 20 %) and the
    significant proteins. The findings follow the filters, then the run projection, the
    variation against abundance, the volcano and the p-value histogram.

=== ":material-waveform:{ .mc-blue } Acquisition"

    **Data & QC** · *Were the runs acquired alike?*

    [![Acquisition dashboard](../../images/pipeline-templates/nf-core/quantms/acquisition_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/acquisition_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Acquisition dashboard](../../images/pipeline-templates/nf-core/quantms/acquisition_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/acquisition_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The MS2 spectra per minute and the median MS2 base-peak intensity per minute, one
    curve per run, and the share of MS2 spectra by the number of peaks they hold. Runs
    of one experiment are expected within about 5 % of the median on the gradient and
    the MS2 rate. The spectra summary is collapsed. Filter: a retention-time window.

=== ":material-magnify-scan:{ .mc-indigo } Identification"

    **Data & QC** · *How many precursors did each run identify, and how clean are they?*

    [![Identification dashboard](../../images/pipeline-templates/nf-core/quantms/identification_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/identification_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Identification dashboard](../../images/pipeline-templates/nf-core/quantms/identification_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/identification_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One per-run quality view, the weakest run on top: the deviation from the median of
    the precursors, the yield per thousand MS2 spectra, the modified share and the
    missed-cleavage share, coloured by condition. Then the gap between observed and
    predicted retention time along the gradient, and the peptide length and DIA-NN
    evidence score per run. The precursor table is collapsed. Filters: modification,
    charge and peptide length.

=== ":material-molecule:{ .mc-violet } Proteins"

    **Quantification** · *Which protein groups were quantified, and how completely?*

    [![Proteins dashboard](../../images/pipeline-templates/nf-core/quantms/proteins_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/proteins_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Proteins dashboard](../../images/pipeline-templates/nf-core/quantms/proteins_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/proteins_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The variation between runs against abundance for every group, with a dashed line at
    a coefficient of variation of 20 % and the most variable groups labelled by gene. The
    groups missed in some runs, by how many runs quantified them, and the protein-group
    table with a record card that links the UniProt entry are collapsed. Filters:
    detection, peptide support and a variation range.

=== ":material-set-merge:{ .mc-cyan } Reproducibility"

    **Quantification** · *Do the runs of a condition agree, and do the conditions separate?*

    [![Reproducibility dashboard](../../images/pipeline-templates/nf-core/quantms/reproducibility_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/reproducibility_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Reproducibility dashboard](../../images/pipeline-templates/nf-core/quantms/reproducibility_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/reproducibility_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The run projection (a lasso filters the linked panels), the difference between two
    runs against their mean for every replicate pair, and the variation within each
    condition as a violin, where under 20 is tight and over 30 noisy. The clustered run
    correlation and the per-condition table are collapsed. Filters: replicate pair and a
    variation range.

=== ":material-chart-scatter-plot:{ .mc-pink } Differential abundance"

    **Quantification** · *Which proteins change between conditions, and can the test tell?*

    [![Differential abundance dashboard](../../images/pipeline-templates/nf-core/quantms/differential_abundance_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/differential_abundance_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Differential abundance dashboard](../../images/pipeline-templates/nf-core/quantms/differential_abundance_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/quantms/differential_abundance_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The proteins called Up and Down in each contrast, the volcano with its MA and QQ
    views (dashed lines at an adjusted p of 0.05 and at log2 fold changes of -1 and 1),
    the p-value histogram and the fold-change histogram. A flat histogram says the test
    is calibrated and no protein changed enough. The MSstats table and its record card
    are collapsed. Filters: contrast, direction, effect size and missing values.

The sample sheet selects on `run_id`, and the protein tables, the variation scatter
and the volcano select on `protein_group`. A pick narrows the other tiles of its
collection and of the collections linked from it. A record card waits for a picked
row or point.


---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/quantms, it does not run the pipeline.
Run the pipeline first, on an SDRF of a DIA experiment:

```bash
nextflow run nf-core/quantms -r 1.1.1 \
  --input sdrf.tsv \
  --outdir results \
  -profile docker
```

See the usage documentation for the DIA options. Then point Depictio at the
directory of the DIA results:

```bash
depictio ingest results/ --template nf-core/quantms/latest
```

See [nf-co.re/quantms/usage](https://nf-co.re/quantms/1.1.1/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the output of one mode. Depictio
scans recursively and matches on file name.

```text
<DATA_ROOT>/                                    # mode_dia/ for the megatest
├── input/
│   └── sdrf.tsv                                # --var METADATA_FILE (optional)
├── pipeline_info/*software*versions*.yml
├── sdrfparsing/
│   ├── *_openms_design.tsv                     # runs, sample, MSstats condition
│   └── *_config.tsv                            # acquisition settings
├── mzmlstatistics/*_mzml_info.tsv
├── diannsummary/
│   ├── diann_report.tsv                        # precursors
│   └── diann_report.pg_matrix.tsv              # protein groups
└── msstats/*_comparisons.csv                   # contrasts (tab separated)
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/quantms/1.1.1/download_test_data.sh),
which fetches the tables of nf-core's AWS megatest run that the template needs and
copies the vendored SDRF into `input/`:

```bash
bash depictio/projects/nf-core/quantms/1.1.1/download_test_data.sh \
  /tmp/quantms_test
depictio ingest /tmp/quantms_test --template nf-core/quantms/latest
```

The run is
`s3://nf-core-awsmegatests/quantms/results-600505011027ab196bb18b1320607468bdae951a/`,
whose `mode_dia/` folder holds four label-free DIA runs of two conditions. It
therefore has a single contrast, and the per-contrast views read one. The other
two modes of that run (`mode_lfq`, `mode_tmt`) are not read.

---

## :material-link-variant: Additional resources

- [nf-co.re/quantms](https://nf-co.re/quantms): official pipeline documentation
- [nf-co.re/quantms/results](https://nf-co.re/quantms/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/quantms releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
