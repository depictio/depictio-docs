---
title: Ribosome profiling
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/riboseq" target="_blank" title="nf-core/riboseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/riboseq/master/docs/images/nf-core-riboseq_logo_dark.png" alt="nf-core/riboseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/riboseq/master/docs/images/nf-core-riboseq_logo_light.png" alt="nf-core/riboseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Ribosome profiling</h1>
    <p class="template-subtitle">riboWaltz periodicity QC, the Salmon sample space of both assays, anota2seq translational regulation, translational efficiency per gene and Ribo-TISH against RiboCode ORF calls, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/riboseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/riboseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="2.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.0.0" selected>2.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The riboseq template follows an nf-core/riboseq run from paired Ribo-seq and
RNA-seq libraries to translated ORFs:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, riboWaltz periodicity of the footprints, and the Salmon sample space of both assays
- :material-scale-balance: **Translation**: translational efficiency per gene, pooled over the run, and anota2seq translational regulation per contrast
- :material-set-merge: **ORFs**: ORF classes per library, and where Ribo-TISH, RiboCode and the annotation agree

The persistent `Sample filters` (the design group, the library and the assay)
sit in the left panel and narrow every tab that reads per-library data.

!!! info "Two assays in one sample sheet"
    A riboseq run mixes total mRNA libraries (`type: rnaseq`) and ribosome
    footprint libraries (`type: riboseq`). The MultiQC and Sample space tabs read
    both; the riboWaltz, Ribo-TISH and RiboCode panels read the footprint
    libraries only, and anota2seq pairs the two per contrast. The `Assay` filter
    splits them on every tab that reads per-library data.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/riboseq_results \
      --template nf-core/riboseq/latest \
      --var METADATA_FILE=/path/to/design.tsv
    ```

    The hub of the dashboard is the sample sheet the run was started with. It is
    not part of the published output, so copy it under `input/` in the data root,
    where `SAMPLESHEET_FILE` is auto-detected, or pass `--var
    SAMPLESHEET_FILE=...`. `METADATA_FILE` is optional: a design table whose first
    column is the sample id and whose first annotation column becomes the group
    filter. Without it the design table and the group filter are dropped and every
    other panel renders from the sample sheet.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/riboseq -r 2.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the sample sheet, the MultiQC report, the Salmon merged gene
matrices, the riboWaltz QC tables, the anota2seq results per contrast, the
in-frame P-site counts and the Ribo-TISH and RiboCode ORF calls. Every
collection past the sample sheet, MultiQC and Salmon is optional, so a run that
skipped riboWaltz, the contrasts or an ORF caller still imports. 45 of its 65
tiles carry a `use:` catalog reference, so a tile says where its panel comes
from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/riboseq-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in three groups, read as a
funnel from the reads to the ORFs being translated. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read
alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Ribo-seq QC, Sample space |
| Translation | Translational efficiency, Translational regulation |
| ORFs | ORF discovery |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. The persistent *Sample
filters* (the design group, the library and the assay) sit in the left panel and
narrow every tab that reads per-library data; Translational efficiency and
Translational regulation are pooled over the run and do not follow them. The
*Sample sheet* section (the sample sheet and the optional design table) is pinned,
collapsed, to the bottom of every child tab. Without a `METADATA_FILE` the design
table and the group filters go; the library and assay filters remain.

=== ":material-compass-outline: Overview"

    *Ribosome footprints and mRNA, from read QC to the ORFs being translated.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/riboseq/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/riboseq/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says what the
    dashboard shows and how the two filter levels work, *The run* lists the
    libraries, the contrasts, the rRNA removal tool, the aligners and the
    efficiency method, and *Pipeline* walks the six steps from cleaning to ORFs,
    each linked to its settings and its tab. The findings are live values: they
    follow the filters, except the efficiency and ORF rows, which are pooled over
    the run. No key figure reads anota2seq, so a run without `--contrasts` keeps
    four cards; regulation is a findings row and a figure.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (the design group and the library), *Findings* another (the
        design group and the contrast): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: libraries by assay, frame-0 share of CDS P-sites, genes expressed, ORFs by class |
        | Findings | Live result rows, then 4 figures: the P-sites around the start codon, the efficiency plane, the fold-change plane and the caller UpSet |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the reads survive trimming, rRNA removal and alignment?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/riboseq/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/riboseq/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only. Open: FastQC sequence counts and adapter content on the
    raw reads, then counts and read lengths after rRNA removal; the SortMeRNA rRNA
    share beside the STAR summary; Ribo-TISH's reading-frame proportions and
    footprint lengths. Footprints are short, so Ribo-seq libraries show heavy
    adapter content and a large rRNA share: compare them with each other, not with
    RNA-seq. The Salmon fragment lengths, the raw per-base quality, the read
    lengths after trimming, the FastQC status after rRNA removal and the samtools
    mapping rate are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID`, read from the MultiQC report, and `Read layout`
        on the sample sheet, so both work on a run without a design table.

        | Section | What it holds |
        |---|---|
        | Read quality | 4 MultiQC panels |
        | rRNA and alignment | 2 MultiQC panels |
        | Footprint quality | 2 MultiQC panels |
        | QC details (collapsed) | 5 MultiQC panels |

=== ":material-waves:{ .mc-grape } Ribo-seq QC"

    **Data & QC** · *Do the footprints come from translating ribosomes?*

    [![Ribo-seq QC dashboard](../../images/pipeline-templates/nf-core/riboseq/ribo_seq_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/ribo_seq_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Ribo-seq QC dashboard](../../images/pipeline-templates/nf-core/riboseq/ribo_seq_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/ribo_seq_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The P-sites riboWaltz assigned, the median frame-0 share in the CDS, the
    lowest frame margin against a 20-point threshold and the median CDS share of
    P-sites. Then the P-sites per reading frame (the CDS first, a UTR one switch
    away), the P-sites around the start and the stop codon, and the phasing plane
    beside the footprint length profiles. The frame-0 share is taken on frame 0
    itself, not on the dominant frame, so a mis-set P-site offset shows as a low
    value. The region composition, the library table with its record card and the
    region table against the length expectation are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Frame 0 in CDS (%)` and `P-sites in CDS (%)` ranges on
        `ribowaltz_summary`, which links to every other riboWaltz view.

        | Section | What it holds |
        |---|---|
        | Periodicity at a glance | 4 cards |
        | Reading frame | 1 advanced visualization |
        | Metagene profiles | 2 advanced visualizations |
        | Libraries | 2 advanced visualizations: the phasing plane and the footprint length profiles |
        | Library detail (collapsed) | 1 advanced visualization, *Ribo-seq library quality* + a library record card, *P-site regions against the length expectation* |

    !!! tip "Only with riboWaltz"
        A run with `--skip_ribowaltz` writes no riboWaltz tables: the tab is
        dropped, and with it the frame-0 card, the frame-0 row and the start-codon
        figure on the Overview.

=== ":material-chart-scatter-plot:{ .mc-cyan } Sample space"

    **Data & QC** · *Do the libraries separate by assay first, then by design?*

    [![Sample space dashboard](../../images/pipeline-templates/nf-core/riboseq/sample_space_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/sample_space_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Sample space dashboard](../../images/pipeline-templates/nf-core/riboseq/sample_space_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/sample_space_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The libraries placed, split by the sheet's leading factor (the assay on a
    riboseq sheet), the median genes detected, and the median genes expressed and
    median TPM per library with their spread. Then a PCA on the Salmon TPMs of
    every library, Ribo-seq and RNA-seq together, coloured by the leading factor;
    any other sheet column is one switch away. The first component usually splits
    the two assays; read the next ones for the design groups within each. A lasso
    filters the linked panels. The PCA table with the library record beside it is
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Genes expressed` range on `sample_pca`.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Sample space | 1 advanced visualization |
        | Library rows (collapsed) | *Library PCA and expression summary* + a library record card |

=== ":material-chart-line:{ .mc-teal } Translational efficiency"

    **Translation** · *Which genes carry more ribosomes than their mRNA level predicts?*

    [![Translational efficiency dashboard](../../images/pipeline-templates/nf-core/riboseq/translational_efficiency_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/translational_efficiency_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Translational efficiency dashboard](../../images/pipeline-templates/nf-core/riboseq/translational_efficiency_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/translational_efficiency_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Translational efficiency is log2 of Ribo-seq CPM over RNA-seq CPM, computed by
    a template recipe from the in-frame P-site count matrix and pooled over every
    library of the run, so it needs no contrast. The genes both assays reach, the
    median log2 efficiency and the median Ribo-seq and RNA-seq abundance. Then the
    plane of Ribo-seq against RNA-seq abundance, one point per gene coloured by
    efficiency, with the diagonal of equal efficiency: genes above it carry more
    ribosomes than their mRNA level predicts. The plane has no point labels; hover
    names a gene. The per-gene table with the gene record beside it is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Translational efficiency (log2)` range and `Gene` on
        `translational_efficiency`.

        | Section | What it holds |
        |---|---|
        | Efficiency at a glance | 4 cards |
        | Efficiency plane | 1 advanced visualization |
        | Gene detail (collapsed) | *Translational efficiency per gene* + a gene record card |

=== ":material-scale-balance:{ .mc-indigo } Translational regulation"

    **Translation** · *Which genes change translation between conditions, and through which mode?*

    [![Translational regulation dashboard](../../images/pipeline-templates/nf-core/riboseq/translational_regulation_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/translational_regulation_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Translational regulation dashboard](../../images/pipeline-templates/nf-core/riboseq/translational_regulation_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/translational_regulation_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Pick a contrast first: every number on the tab depends on it. The regulated
    calls by mode, the translation calls by direction, the median translation
    effect and the smallest translation adjusted p against anota2seq's cut-off of
    0.15. Then the fold-change plane, ribosome-bound against total mRNA change,
    coloured by mode: on the diagonal the mRNA level drives the change, off it
    translation does. Below, the translation volcano beside a volcano of any one
    of the four anota2seq analyses, each with a View switch to its QQ plot. The
    regulation table and its gene record, across the four analyses, are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Contrast`, `Regulatory mode` and `Gene` on
        `anota2seq_regulation`, and an `anota2seq analysis` picker on
        `anota2seq_results` for the second volcano.

        | Section | What it holds |
        |---|---|
        | Regulation at a glance | 4 cards |
        | Fold-change plane | 1 advanced visualization |
        | Significance | 2 advanced visualizations |
        | Gene detail (collapsed) | *Regulatory mode per gene* + a gene record card |

    !!! tip "Only with contrasts"
        anota2seq runs only when the pipeline got `--contrasts`. Without it the
        regulation collections are not written and the tab is dropped, with the
        contrast filter, the regulation row and the fold-change figure on the
        Overview.

=== ":material-set-merge:{ .mc-pink } ORF discovery"

    **ORFs** · *Which ORFs are translated, and do Ribo-TISH and RiboCode agree?*

    [![ORF discovery dashboard](../../images/pipeline-templates/nf-core/riboseq/orf_discovery_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/orf_discovery_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![ORF discovery dashboard](../../images/pipeline-templates/nf-core/riboseq/orf_discovery_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/riboseq/orf_discovery_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The pooled ORFs split by class, the ORFs Ribo-TISH and the ORFs RiboCode
    report (each spread by the libraries reporting an ORF) and the median protein
    length. Then the ORF classes per library, one caller at a time, and the UpSet
    of Ribo-TISH, RiboCode and the annotated CDS. The callers are compared on the
    genomic stop codon (`chrom:strand:stop`), so alternative start sites of one ORF
    collapse onto one row; ORFs outside the annotated CDS that both callers report
    are the best supported new candidates. The pooled table with the ORF record
    beside it, then each caller's calls per library, are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `ORF class`, `Gene` and a `Protein length (aa)` range on
        `orf_overlap`.

        | Section | What it holds |
        |---|---|
        | ORFs at a glance | 4 cards |
        | ORF classes per library | 1 advanced visualization |
        | Caller agreement | 1 advanced visualization |
        | ORF detail (collapsed) | *ORFs pooled over libraries* + an ORF record card |
        | Calls per library (collapsed) | *Ribo-TISH calls per library*, *RiboCode calls per library* |

    !!! tip "One caller skipped"
        The four cards read the pooled table, so with `--skip_ribotish` or
        `--skip_ribocode` the skipped caller keeps its card and reads 0, and only
        its per-library table goes. The tab is dropped only when both callers are
        skipped.

Tables select rows, and the phasing plane, the PCA and the efficiency and
fold-change planes select points: the sample sheet, the riboWaltz tables and the
phasing plane on `sample`, the design table on its id column, the PCA and its
table on `sample_id`, the efficiency and regulation planes and tables on
`gene_id`, the pooled ORF table on `orf_id`. A pick narrows the other tiles of its
collection and follows the project links to the collections downstream of it.
Each record card sits beside the table that drives it, in its collapsed section,
and waits for a picked row or point.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/riboseq, it does not run the pipeline.
Run the pipeline first, with a contrasts file if you want the Translational
regulation tab:

```bash
nextflow run nf-core/riboseq -r 2.0.0 \
  --input samplesheet.csv \
  --contrasts contrasts.csv \
  --fasta genome.fa.gz --gtf genes.gtf.gz \
  --outdir results -profile docker
```

Then copy the sample sheet under `input/` and point Depictio at the results:

```bash
mkdir -p results/input && cp samplesheet.csv results/input/
depictio ingest results/ --template nf-core/riboseq/latest \
  --var METADATA_FILE=design.tsv
```

See [nf-co.re/riboseq/usage](https://nf-co.re/riboseq/2.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so the aligner directory can differ from
the tree below.

```text
<DATA_ROOT>/
├── input/
│   └── samplesheet.csv                          # the hub: sample, strandedness, type, design columns
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/star/multiqc_report_data/
│   └── multiqc.parquet                          # or multiqc/multiqc_data/
├── quantification/
│   ├── salmon/salmon.merged.gene_{counts,tpm}.tsv
│   └── inframe_psite/gene_counts.tsv            # optional, translational efficiency
├── psites/ribowaltz/ribowaltz_qc/*.tsv          # optional, --skip_ribowaltz drops it
├── translational_efficiency/anota2seq/
│   └── *.anota2seq.results.tsv                  # optional, needs --contrasts
└── orf_predictions/
    ├── ribotish/*_pred.txt                      # optional, --skip_ribotish drops it
    └── ribocode/*_collapsed.txt                 # optional, --skip_ribocode drops it
```

`METADATA_FILE`, when given, is read from wherever it points; its id column is
`METADATA_ID_COL` (default: the first column) and the group filter reads
`GROUP_COL` (default: the first annotation column). BAM files, bigWigs and the
RiboCode P-site stores are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 2.0.0 release
(`results-11d66a3b8ae1f41f9c385af36bd431c35bf015ab`), paired Ribo-seq and RNA-seq
libraries from a two-condition design with one contrast, and the screenshots
above come from it. The sample sheet, contrasts and a design table are not part
of the published run: they are vendored with the template under `input/`.
`megatest.yaml` lists the tables-only subset the template needs:

```bash
bash depictio/projects/nf-core/riboseq/2.0.0/download_test_data.sh /tmp/riboseq_test
mkdir -p /tmp/riboseq_test/input
cp depictio/projects/nf-core/riboseq/2.0.0/input/*.*sv /tmp/riboseq_test/input/
depictio ingest /tmp/riboseq_test --template nf-core/riboseq/latest \
  --var METADATA_FILE=/tmp/riboseq_test/input/metadata.tsv
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/riboseq](https://nf-co.re/riboseq): official pipeline documentation
- [nf-co.re/riboseq/2.0.0/results](https://nf-co.re/riboseq/2.0.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/riboseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
