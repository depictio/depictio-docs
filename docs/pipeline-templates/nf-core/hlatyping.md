---
title: HLA typing
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/hlatyping" target="_blank" title="nf-core/hlatyping on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/hlatyping/master/docs/images/nf-core-hlatyping_logo_dark.png" alt="nf-core/hlatyping">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/hlatyping/master/docs/images/nf-core-hlatyping_logo_light.png" alt="nf-core/hlatyping">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">HLA typing</h1>
    <p class="template-subtitle">HLA class I genotypes typed by OptiType: the read quality behind them, the alleles each sample carries at HLA-A, -B and -C, how often each allele occurs across the samples, and how many reads each genotype rests on.</p>
    <p class="template-links">
      <a href="https://nf-co.re/hlatyping" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/hlatyping" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="2.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="2.2.0" selected>2.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The hlatyping template follows an nf-core/hlatyping run from the reads to the
genotypes and the support behind them:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, and how many reads each sample gave and how many typed it
- :material-dna: **HLA**: the alleles each sample carries, how often each allele occurs across the samples, and how many reads each genotype rests on

The persistent `Sample filters` (sequencing type, sample and input format) sit in
the left panel and narrow every tab. The sequencing type (DNA or RNA) is the
default grouping.

!!! info "The samplesheet is not published by the pipeline"
    The hub of the dashboard is the samplesheet the run was started with. It is
    not part of the published output, so copy it under `input/` in the results
    directory, or pass `--var METADATA_FILE=...`. Without a sheet the hub still
    lists every sample OptiType typed, with the sequencing type `Not stated`.

!!! info "Allele spelling matches nf-core/epitopeprediction"
    Alleles are normalised to two fields, `HLA-A*02:01`, the spelling the
    [epitopeprediction](epitopeprediction.md) template uses. The genotype table
    writes each sample's alleles as the `;`-separated list an epitopeprediction
    samplesheet takes, so a typed sample can be predicted against its own
    genotype. The two runs are separate projects, so a pick in one does not
    filter the other.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/hlatyping_results \
      --template nf-core/hlatyping/latest \
      --var METADATA_FILE=/path/to/samplesheet.csv
    ```

    The results directory is the only required value when the samplesheet sits at
    `{DATA_ROOT}/input/samplesheet.csv`.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | `{DATA_ROOT}/input/samplesheet.csv` | the samplesheet the run was started with |
    | `GROUP_COL` | `seq_type` | column the dashboard groups and filters samples by; any column added to the sheet works |
    | `GROUP_COL_DISPLAY` | `Sequencing type` | reader-facing label of `GROUP_COL` in filters and cards |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/hlatyping -r 2.2.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so put a copy of the samplesheet at
    `results/input/samplesheet.csv` before the run.

---

## :material-book-open-variant: Reference

The template reads the samplesheet, OptiType's result table of each sample, the
MultiQC report and the per-read-file FastQC table it was built from. With
`--enumerations` above 1 OptiType also writes sub-optimal solutions; the
genotypes keep the optimum. No variable prunes a route: every 2.2.0 run that
reaches MultiQC writes all five collections. HLA-HD output (`--tools hlahd`) is
not read.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/hlatyping-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read as a
funnel from the reads to the genotypes and the support behind them. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page
and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Reads |
| HLA | Genotypes, Alleles, Typing quality |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *HLA class I typing with OptiType, from the reads to the genotypes.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/hlatyping/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/hlatyping/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    *The run* lists the samples, the distinct alleles, the typing tool, the solver
    and the solutions asked per sample, and *Pipeline* walks five steps (reads, QC,
    map, type, score), each linked to its parameters and its tab. Four key figures:
    the samples, the distinct alleles, the homozygous loci and the median reads
    behind a genotype. The findings are live rows plus four figures: the genotype
    grid, the allele frequency by locus, the reads against the objective and the
    reads per sample.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Are the reads clean enough to type?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/hlatyping/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/hlatyping/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: the general statistics, FastQC's sequence counts,
    mean quality, GC content and duplication levels, and OptiType's allele calls by
    locus. The FastQC status checks, adapter content, overrepresented sequences and
    N content are collapsed. FastQC judges GC content against a whole-genome model,
    so exome, RNA or HLA-enriched reads often fail that module without harm.

=== ":material-file-document-multiple-outline:{ .mc-teal } Reads"

    **Data & QC** · *How many reads did each sample give, and how many typed it?*

    [![Reads dashboard](../../images/pipeline-templates/nf-core/hlatyping/reads_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/reads_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Reads dashboard](../../images/pipeline-templates/nf-core/hlatyping/reads_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/reads_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The read files (a ring by their worst FastQC module), the median reads per
    file, the share of a sample's read pairs its genotype explains and the highest
    duplicate share against FastQC's 20% and 50% lines. Then the reads per sample
    and read, the reads of each file against the reads its genotype explains, the GC
    content by group and the duplicate share per sample. Filters: read of the pair
    and FastQC status.

=== ":material-dna:{ .mc-blue } Genotypes"

    **HLA** · *Which HLA class I alleles does each sample carry?*

    [![Genotypes dashboard](../../images/pipeline-templates/nf-core/hlatyping/genotypes_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/genotypes_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genotypes dashboard](../../images/pipeline-templates/nf-core/hlatyping/genotypes_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/genotypes_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The samples typed, the distinct alleles per sample, the homozygous loci and the
    allele groups. Then the allele grid: one row per sample, one column per locus,
    each cell split into its two haplotypes and coloured by allele group, with the
    objective and the reads as side bars. A click on an allele narrows the
    dashboard to the samples that carry it. The genotype table and every allele call
    are collapsed. Filters: locus, allele and zygosity.

=== ":material-chart-bar:{ .mc-violet } Alleles"

    **HLA** · *How often does each allele occur across the samples?*

    [![Alleles dashboard](../../images/pipeline-templates/nf-core/hlatyping/alleles_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/alleles_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Alleles dashboard](../../images/pipeline-templates/nf-core/hlatyping/alleles_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/alleles_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The distinct alleles, the commonest allele, the allele calls by zygosity and
    the share of calls the three largest allele groups take. Then the allele
    frequency by locus (each sample contributes two calls per locus, so a
    homozygous locus counts its allele twice) and the calls per allele group
    stacked by zygosity. Filters: locus and allele group.

=== ":material-scale-balance:{ .mc-grape } Typing quality"

    **HLA** · *How many reads does each genotype rest on?*

    [![Typing quality dashboard](../../images/pipeline-templates/nf-core/hlatyping/typing_quality_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/typing_quality_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Typing quality dashboard](../../images/pipeline-templates/nf-core/hlatyping/typing_quality_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hlatyping/typing_quality_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median reads behind a genotype, the fewest reads of any sample, the median
    heterozygous loci and the median objective per read. Then the reads against
    the objective, one point per sample coloured by its homozygous loci, and the
    reads per sample. The objective mostly reads the zygosity, not the quality of
    the fit, so judge a genotype by its reads. Filters: a reads range and a
    heterozygous-loci range.

An allele, locus or zygosity pick on the genotypes reaches the per-sample typing
and the read files through the sample, so a pick on an allele shows the samples
that carry it.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/hlatyping, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/hlatyping -r 2.2.0 \
  --input samplesheet.csv \
  --outdir results \
  -profile docker
```

The samplesheet is `sample,fastq_1,fastq_2,bam,seq_type`, with `seq_type` set to
`dna` or `rna`; several rows of one sample are concatenated. Copy it under
`results/input/`, then point Depictio at the results:

```bash
depictio ingest results/ --template nf-core/hlatyping/latest
```

See [nf-co.re/hlatyping/usage](https://nf-co.re/hlatyping/2.2.0/docs/usage) for full pipeline documentation.

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
├── multiqc/multiqc_data/
│   ├── multiqc.parquet
│   └── multiqc_fastqc.txt                      # per-read-file FastQC table
└── optitype/<sample>/<sample>_result.tsv       # OptiType's call, one per sample
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/hlatyping/2.2.0/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs
and copies the vendored samplesheet into `input/`:

```bash
bash depictio/projects/nf-core/hlatyping/2.2.0/download_test_data.sh \
  /tmp/hlatyping_test
depictio ingest /tmp/hlatyping_test \
  --template nf-core/hlatyping/latest
```

The run is
`s3://nf-core-awsmegatests/hlatyping/results-3237d20e7e611d8bbf8c37e637202dfe8a23e996/`,
the 2.2.0 `test_full` run: five samples, a DNA exome (as FASTQ, as the same FASTQ in
two parts and as a BAM) and an RNA sample (as FASTQ and as the same FASTQ in two
parts), typed from two individuals. It tests the pipeline, not a cohort, so the
genotypes repeat by design. The vendored samplesheet is the test-datasets sheet
that run read.

---

## :material-link-variant: Additional resources

- [nf-co.re/hlatyping](https://nf-co.re/hlatyping): official pipeline documentation
- [nf-co.re/hlatyping/results](https://nf-co.re/hlatyping/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/hlatyping releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
