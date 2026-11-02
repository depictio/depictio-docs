---
title: RNA-seq variant calling
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/rnavar" target="_blank" title="nf-core/rnavar on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnavar/master/docs/images/nf-core-rnavar_logo_dark.png" alt="nf-core/rnavar">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnavar/master/docs/images/nf-core-rnavar_logo_light.png" alt="nf-core/rnavar">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">RNA-seq variant calling</h1>
    <p class="template-subtitle">Germline variants called from RNA-seq: how the reads aligned, spliced and covered the genome, how many calls each sample yields and how clean they are, what they change in the genes, and whether replicates share them, with a genome browser on the reads.</p>
    <p class="template-links">
      <a href="https://nf-co.re/rnavar" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/rnavar" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.3.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.3.0" selected>1.3.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The rnavar template follows an nf-core/rnavar run from the alignment to where
the calls fall on the genome:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, how the reads aligned, spliced and deduplicated, and how deep and where they cover the genome
- :material-dna: **Variants**: the callset per sample, what the calls change in the genes (snpEff route), and a genome view of the variants replicates share, over the reads

<div class="tpl-showcase">
  <div class="tpl-showcase-bar">
    <span class="tpl-showcase-live"></span>
    <span class="tpl-showcase-label">Live showcase</span>
    <span class="tpl-showcase-meta">nf-core/rnavar, nf-core test data</span>

    <a class="tpl-showcase-open" href="https://showcases.depictio.embl.org/dashboard/6ae793c0a64daa3df60fb764" target="_blank" rel="noopener"><i class="mdi mdi-open-in-new"></i> Open</a>
  </div>
  <iframe class="tpl-showcase-frame" src="https://showcases.depictio.embl.org/dashboard/6ae793c0a64daa3df60fb764" loading="lazy" title="nf-core/rnavar showcase dashboard" allowfullscreen></iframe>
</div>

The persistent `Sample filters` (the design group and the sample) sit in the left
panel and narrow every tab through the sample hub.

!!! info "The design table is optional"
    rnavar does not publish its samplesheet, and the samplesheet has no design
    column, so the design is a table you pass (`METADATA_FILE`: the sample id in a
    `sample` column, every other column a factor). Without it the group filter,
    the group colours and the replicate agreement fall away, and every tile keeps
    working on one constant group.

!!! info "The BAMs are never ingested as tables"
    The alignments (14 to 21 GB each on the test run) are opened only by the
    genome browser, in place (`TRACKS_URI`) or uploaded. The numbers come from
    STAR's, Picard's and samtools' reports, the VCFs and the MultiQC report.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/rnavar_results \
      --template nf-core/rnavar/latest \
      --var METADATA_FILE=/path/to/design.tsv
    ```

    The results directory is the only required value. `METADATA_FILE` is the
    optional design table above.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | unset | design table; without it the group filter, colours and splits fall away |
    | `GROUP_COL` | first factor column of the design table | column the dashboard groups and filters samples by |
    | `GENOME` | `hg38` | UCSC name of the assembly, which lays out the Genome tab axis and gene lane; rnavar's `--genome GRCh38` is chr-prefixed, so `hg38` fits, and `none` drops the gene lane only |
    | `TRACKS_URI` | unset | `s3://` or `https://` folder holding the run's results: the browser then reads the VCFs and BAMs in place; unset, the files under the results directory are uploaded |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/rnavar -r 1.3.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so the run has no design table.

---

## :material-book-open-variant: Reference

The template reads STAR's final log and splice junctions, Picard MarkDuplicates,
samtools stats and idxstats, the HaplotypeCaller VCFs, the snpEff output when the
run annotated, and the native MultiQC report (no regeneration needed). rnavar
writes each sample's calls twice, as called and after VariantFiltration:
the template reads the filtered VCF, or the unfiltered one when the run skipped
filtration, so no call is counted twice.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. Without `--tools snpeff` the Annotation
    tab, its pipeline step and its tile in the tab list go.

<div class="tpl-version-block" data-version="1.3.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/rnavar-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in two groups, read as a
funnel from the reads to where the calls fall on the genome. Each tab below
carries the **same icon and colour the dashboard gives it**, so the page and the
app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Alignment, Coverage |
| Variants | Callset, Annotation, Genome |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Germline variant calling from RNA-seq, from the alignment to the annotated calls.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/rnavar/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/rnavar/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    *The run* reads the genome, aligner, calling confidence, filter thresholds and
    annotation tools from the run parameters, and *Pipeline* walks six steps (Align,
    Mark, Call, Filter, Annotate, Report), each linked to its settings and its tab.
    Four key figures: PASS variants, replicate agreement (a Ts/Tv card without a
    design table), the T to C share of the PASS SNVs and the calls failing a
    filter. The findings are live rows plus three figures: unique mapping and
    duplication per sample, the substitution spectrum and the sample-by-sample
    genotype concordance.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *What does the MultiQC report say about the alignments?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/rnavar/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/rnavar/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only: the general statistics, then STAR's alignment scores and
    summary, Picard MarkDuplicates, and samtools reads per contig and XY counts.

=== ":material-align-horizontal-left:{ .mc-blue } Alignment"

    **Data & QC** · *How well did the reads align, splice and deduplicate?*

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/rnavar/alignment_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/alignment_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/rnavar/alignment_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/alignment_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The input reads, the uniquely mapped share, duplication and the mismatch rate,
    each with a line on what a bad value means. Then unique mapping and duplication
    per sample as a sorted dot plot, the weakest sample on top, next to the record
    of the picked sample, and the splice junctions per sample by intron motif,
    novel first. The tables are collapsed.

=== ":material-layers-outline:{ .mc-cyan } Coverage"

    **Data & QC** · *How deep do the reads cover the genome, and where?*

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/rnavar/coverage_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/coverage_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/rnavar/coverage_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/coverage_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The covered bases at 10x, the mapped reads, the mitochondrial reads (a
    threshold at 5%) and the reads on alt and unplaced contigs. Then the depth
    histogram of every sample on log axes and the mapped reads by contig class.
    The contig table is collapsed.

=== ":material-magnify-scan:{ .mc-teal } Callset"

    **Variants** · *How many calls does each sample yield, and how clean are they?*

    [![Callset dashboard](../../images/pipeline-templates/nf-core/rnavar/callset_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/callset_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Callset dashboard](../../images/pipeline-templates/nf-core/rnavar/callset_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/callset_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    PASS calls, Ts/Tv, the het/hom ratio and the calls by FILTER value, the first
    two against a working range. Then the genotype concordance of every pair of
    samples, where replicates should sit together, the substitution spectrum per
    sample (T to C carries the A-to-I editing signal) and Ts/Tv and het/hom per
    sample with that range shaded. The allele-fraction distributions and the tables
    are collapsed; a FILTER value picked on the left narrows the calls.

=== ":material-tag-outline:{ .mc-grape } Annotation"

    **Variants** · *What do the calls change in the genes they hit?*

    Only when the run annotated with `--tools snpeff`. The annotated calls by
    impact, the genes hit by biotype, the HIGH impact calls and the coding allele
    fraction. Then the impact classes per sample and the twelve commonest
    consequence terms, coloured by impact. A gene picked in the collapsed gene
    table narrows the call table.

=== ":material-map-marker-outline:{ .mc-indigo } Genome"

    **Variants** · *Are PASS variants shared between replicates, and do the reads support them?*

    [![Genome dashboard](../../images/pipeline-templates/nf-core/rnavar/genome_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/genome_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genome dashboard](../../images/pipeline-templates/nf-core/rnavar/genome_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/rnavar/genome_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards on the sites replicates share and on the region in view. A navigator
    draws one lane per design group, each window its distinct PASS variants per
    megabase; a brush or a typed locus sets the region for the cards, the call
    table and the [genome browser](../../features/genome-browser.md), which shows
    the replicates' VCFs and, under them, their BAMs with splice-junction arcs. It
    opens on the best-supported shared variant, and a stepper walks the shared
    sites. The UCSC tracks are hg38 only.

A pick on a sample or a design group reaches every per-sample collection and the
MultiQC panels through the project links.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/rnavar, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/rnavar -r 1.3.0 \
  --input samplesheet.csv \
  --genome GRCh38 \
  --outdir results \
  -profile docker
```

Add `--tools snpeff` for the Annotation tab. Then point Depictio at the results:

```bash
depictio ingest results/ \
  --template nf-core/rnavar/latest \
  --var METADATA_FILE=design.tsv
```

See [nf-co.re/rnavar/usage](https://nf-co.re/rnavar/1.3.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio
scans recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/sample_metadata.tsv                   # --var METADATA_FILE (optional design table)
├── pipeline_info/
├── reports/
│   ├── star/<s>/<s>.Log.final.out
│   ├── star/<s>/<s>.SJ.out.tab
│   ├── picard/<s>/<s>.md.metrics.txt
│   ├── samtools/<s>/<s>.md.{stats,idxstats}
│   ├── snpeff/<s>/*_snpEff.{csv,genes.txt}     # only with --tools snpeff
│   └── multiqc/multiqc_data/multiqc.parquet
├── variant_calling/<s>/<s>.haplotypecaller[.filtered].vcf.gz[.tbi]
├── annotation/<s>/*_snpEff.ann.vcf.gz          # only with --tools snpeff
└── preprocessing/<s>/<s>.md.bam[.bai]          # opened by the genome browser only
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/rnavar/1.3.0/download_test_data.sh),
which fetches the tables-only subset of nf-core's AWS megatest run that the
template needs (no BAMs) and copies the vendored design table into `input/`:

```bash
bash depictio/projects/nf-core/rnavar/1.3.0/download_test_data.sh \
  /tmp/rnavar_test
depictio ingest /tmp/rnavar_test \
  --template nf-core/rnavar/latest \
  --var METADATA_FILE=/tmp/rnavar_test/input/sample_metadata.tsv
```

The run is
`s3://nf-core-awsmegatests/rnavar/results-5e72bcb5520e00422750c978d4153b38f1fd7312/`,
a complete `test_full` run of the 1.3.0 development version: eight samples from
cell lines with replicates, with the HaplotypeCaller VCFs and a MultiQC report.
The 1.3.0 release run is a truncated sync with no variant calls, so it is not
used. That run used no `--tools`, so the Annotation tab was checked on snpEff
output from the same subworkflow in a sarek megatest.

---

## :material-link-variant: Additional resources

- [nf-co.re/rnavar](https://nf-co.re/rnavar): official pipeline documentation
- [nf-co.re/rnavar/results](https://nf-co.re/rnavar/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/rnavar releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
