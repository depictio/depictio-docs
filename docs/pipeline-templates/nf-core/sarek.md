---
title: Variant calling
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/sarek" target="_blank" title="nf-core/sarek on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_dark.png" alt="nf-core/sarek">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_light.png" alt="nf-core/sarek">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Variant calling</h1>
    <p class="template-subtitle">Germline variant calling compared caller by caller: coverage, bcftools and VCFtools statistics, agreement between callsets, SnpEff consequences and the genes that carry them, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/sarek" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/sarek" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="3.10.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.10.0" selected>3.10.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The sarek template follows a variant-calling run from the reads to the genes the
calls land on, and reads the VCFs themselves, so callers are compared call by
call and gene by gene rather than only by how many calls each made:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: read, mapping and recalibration panels from the pipeline's own MultiQC report, and the depth over the intervals with an X against Y sex check
- :material-set-merge: **Variant calls**: what each caller called and of what kind, how clean each callset looks, and which calls the callers share
- :material-dna: **Annotation**: SnpEff's consequences recomputed per call, the genes that carry the calls, and depth and calls at one region on one axis

The persistent `Sample filters` (status, patient, sample) sit in the left panel,
and a pick there reaches every per-sample collection and the MultiQC panels
through the sample links.

!!! info "Concordance is agreement, not truth"
    Nothing in this template compares a callset against a benchmark truth set:
    "concordance" means agreement between callers and samples. For a truth-set
    benchmark, [nf-core/variantbenchmarking](variantbenchmarking.md) has its own
    template.

!!! note "Structural-variant callers call few SNPs"
    Manta and TIDDIT report a Ts/Tv of 0.0 in bcftools stats, which is the
    caller doing its job. Every Ts/Tv card and filter keeps only `ts_tv > 0`, so
    they do not drag the medians down.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/sarek_results \
      --template nf-core/sarek/latest
    ```

    The results directory is the only thing you have to pass. The sample hub is built
    from the CSV manifests sarek writes under `csv/` (patient, sex, status and
    the callers run per sample), so the launch samplesheet is not needed. If the
    run was aligned to another assembly than hg38, name it so the locus tracks
    draw the right axis and gene lane:

    ```bash
    depictio ingest /path/to/sarek_results \
      --template nf-core/sarek/latest \
      --var GENOME=hg19
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `GENOME` | `hg38` | UCSC name of the assembly (hg38, hg19, mm10): the axis and gene lane of every locus track |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/sarek -r 3.10.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the native MultiQC report, the per-caller bcftools stats and
VCFtools summaries, mosdepth's coverage files, the called VCFs, and SnpEff's
annotated VCFs, CSV statistics and per-gene tables. The caller and the sample
live only in the directory path (`reports/<tool>/<caller>/<sample>/`), so raw
scans carry the path into the table and recipes read both off it. sarek runs
mosdepth on the duplicate-marked and on the recalibrated CRAM; the coverage
recipes keep one pass per sample, so no tile counts a sample twice.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. A run without SnpEff in `--tools`
    drops the Consequences and Genes tabs instead of failing to ingest.

<div class="tpl-version-block" data-version="3.10.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/sarek-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then eight child tabs in three groups, read as a
funnel from the reads to the genes the calls hit and one region of the genome.
Each tab below carries the **same icon and colour the dashboard gives it**, so the
page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Coverage |
| Variant calls | Variant yield, Call quality, Caller concordance |
| Annotation | Consequences, Genes, Locus |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The template has no group column:
the sample hub is built from sarek's CSV manifests and carries the patient, sex,
status and the callers run per sample. A callset is one caller on one sample. The
persistent *Sample filters* (status, patient, sample) sit in the left panel and
narrow every tab through the sample links. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Germline variant calls, from coverage to the genes they hit.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/sarek/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/sarek/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how the two
    filter levels work, *The run* lists the samples, the callsets and the callers
    they come from, the genome and the aligner, and *Pipeline* walks the six steps
    from mapping to annotation, each linked to the parameters that drive it and
    its tab. The findings are live values: they follow the filters, and a run
    without SnpEff drops the HIGH-impact row and the impact figure.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the caller and the sample id):
        each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: variant calls by caller, depth on target, PASS share, Ts/Tv against a 1.8 floor |
        | Findings | Live result rows, then 4 figures: the substitution spectrum, the calls per FILTER value, allele fraction against depth and the impact classes per caller |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did reads, mapping and recalibration work for every sample?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/sarek/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/sarek/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the run's native report. Open: general statistics,
    fastp filtered reads, Samtools percent mapped, MarkDuplicates and the mosdepth
    cumulative coverage. Collapsed: the FastQC panels, the BQSR fit and insert
    sizes, the bcftools and VCFtools panels with every caller pooled, and the
    SnpEff and VEP panels. A library carries a lane and a read suffix in the
    report, so a sample can appear once per read.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | 5 MultiQC panels |
        | Read quality (collapsed) | 3 MultiQC panels |
        | Alignment details (collapsed) | 2 MultiQC panels |
        | Variant-call panels (collapsed) | 4 MultiQC panels |
        | Annotation panels (collapsed) | 4 MultiQC panels |

=== ":material-layers-outline:{ .mc-blue } Coverage"

    **Data & QC** · *How deeply were the intervals covered, sample by sample?*

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/sarek/coverage_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/coverage_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/sarek/coverage_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/coverage_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    mosdepth's depth over the intervals (the capture targets, or the calling
    intervals of a whole genome) and over each contig. The depth on target per
    sample, the median depth of an interval against a 20x floor, the depth across
    contigs and the intervals under 20x, with the contigs that have most. Then the
    mean depth per contig, one bar per sample and contig, with a bar above it that
    switches between the intervals and the whole contig (it opens on the
    intervals), and the X against Y depth scatter, a heuristic sex check. The
    per-contig and sex-check tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Mean depth` range on `mosdepth_summary`. *Depth per
        contig* has its own bar, `Intervals or whole contig`. There is no contig
        or scope picker in the left panel: it would empty the *Depth on target*
        card, which reads mosdepth's `total` row of the intervals.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | Depth per contig | *Mean depth per contig*, with its own filter bar |
        | Sex check | 1 advanced visualization |
        | Coverage tables (collapsed) | *Per-contig coverage summary*, *X and Y coverage per sample* |

=== ":material-chart-bar:{ .mc-violet } Variant yield"

    **Variant calls** · *How much did each caller call, and of what kind?*

    [![Variant yield dashboard](../../images/pipeline-templates/nf-core/sarek/variant_yield_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/variant_yield_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Variant yield dashboard](../../images/pipeline-templates/nf-core/sarek/variant_yield_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/variant_yield_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Each caller's own bcftools stats report. The median records per callset,
    ranked by caller (a structural-variant caller writes orders of magnitude
    fewer), the SNPs and the indels split by caller, and the multiallelic sites.
    Then SNPs and indels per caller, one bar per sample, and the substitution and
    indel length spectra, one bar per caller with its callsets' shares averaged.
    The spectra compare shapes, not yields: a caller whose transversion bars rise
    is the one with the lower Ts/Tv. The bcftools distribution blocks and the
    per-caller count table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` on `bcftools_stats_summary`, and a `bcftools
        block` picker on `bcftools_stats_sections` that chooses the block the
        collapsed distribution draws (it opens on depth).

        | Section | What it holds |
        |---|---|
        | Yield at a glance | 4 cards |
        | Calls per caller | *SNPs per caller*, *Indels per caller* |
        | Mutation spectra | *Substitution spectrum*, *Indel length spectrum* |
        | bcftools distributions (collapsed) | *The chosen block, caller by caller*, *bcftools stats distributions* |
        | Yield table (collapsed) | *Per-caller variant counts* |

=== ":material-check-decagram:{ .mc-cyan } Call quality"

    **Variant calls** · *Do the callsets look like clean germline calls?*

    [![Call quality dashboard](../../images/pipeline-templates/nf-core/sarek/call_quality_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/call_quality_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Call quality dashboard](../../images/pipeline-templates/nf-core/sarek/call_quality_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/call_quality_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    QC numbers computed from each callset's VCF. The median Ts/Tv against a 1.8
    floor, the PASS share, the het to hom ratio and the allele fraction of
    heterozygous calls. Then the callset QC profile, six numbers per callset on
    parallel axes coloured by caller, the calls per FILTER value per caller, with
    PASS in green, and the Ts/Tv above a rising quality floor on a log axis,
    because callers write QUAL on scales a thousand-fold apart. A clean germline
    SNP callset has a Ts/Tv near 2 on a genome, higher on an exome, and its
    heterozygous calls sit near an allele fraction of 0.5. The FILTER breakdown
    and the Ts/Tv per callset are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` and a `Ts/Tv ratio` range on `callset_qc`, and
        `FILTER value` on `vcftools_filter_summary`.

        | Section | What it holds |
        |---|---|
        | Quality at a glance | 4 cards |
        | Callset QC profile | 1 advanced visualization |
        | FILTER partitions | *Calls per FILTER value* |
        | Quality calibration | 1 advanced visualization |
        | Quality tables (collapsed) | *FILTER breakdown per caller*, *Ts/Tv per callset* |

    !!! info "Without VCFtools"
        A run that skipped VCFtools has no FILTER partitions, no quality sweep and
        no `FILTER value` filter here, and the Overview drops its FILTER figure.

=== ":material-set-merge:{ .mc-teal } Caller concordance"

    **Variant calls** · *Which calls do the callers share, and where do they differ?*

    [![Caller concordance dashboard](../../images/pipeline-templates/nf-core/sarek/caller_concordance_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/caller_concordance_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Caller concordance dashboard](../../images/pipeline-templates/nf-core/sarek/caller_concordance_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/caller_concordance_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One row per call, read from the VCFs. The calls ranked by caller, the calls by
    variant type, the allele fraction and the depth at the call. Then the UpSet of
    PASS calls shared between callsets, matched on locus and allele (fixed: the
    pickers on this tab do not narrow it), allele fraction against depth as a
    density beside its histogram per caller (a clean diploid callset forms ridges
    at 0.5 and 1), and the rainfall of the calls along the genome, each at its
    distance to the previous call. The call table is collapsed. Agreement between
    callers is not truth.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller`, `Variant type`, `Contig` and a `Depth at the
        call` range on `vcf_variants`.

        | Section | What it holds |
        |---|---|
        | Concordance at a glance | 4 cards |
        | Shared calls | 1 advanced visualization |
        | Depth sensitivity | 1 advanced visualization, *Allele fraction per caller* |
        | Calls along the genome | 1 advanced visualization |
        | Call table (collapsed) | *Variant calls* |

=== ":material-chart-donut:{ .mc-red } Consequences"

    **Annotation** · *What do the calls do to the transcripts?*

    [![Consequences dashboard](../../images/pipeline-templates/nf-core/sarek/consequences_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/consequences_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Consequences dashboard](../../images/pipeline-templates/nf-core/sarek/consequences_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/consequences_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    SnpEff gives each call its most severe effect on a transcript, in four impact
    classes. The annotated calls by impact class, the HIGH-impact calls by variant
    type, the genes with a HIGH or MODERATE call and the depth at HIGH-impact
    calls. Then SnpEff's own counts for the summary section picked in the left
    panel (opening on impact), caller by caller, and the impact recomputed on the
    calls: the impact classes per caller as shares (MODIFIER left out), and the
    allele fraction against depth scatter coloured by impact, with the record of
    the picked call beside it. The SnpEff summary and the annotated calls are
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` on `snpeff_ann_variants` and `SnpEff section` on
        `snpeff_csv_stats`. *Impact per call* has its own bar, `Impact class`
        and `Consequence`, rather than the left panel, because three cards pin
        an impact class.

        | Section | What it holds |
        |---|---|
        | Consequences at a glance | 4 cards |
        | What kind of variants | *The chosen section, caller by caller* |
        | Impact per call | *Impact classes per caller*, then 2 advanced visualizations: the impact scatter and the *Variant record*, with its own filter bar |
        | Consequence tables (collapsed) | *SnpEff summary sections*, *Annotated variant calls* |

=== ":material-dna:{ .mc-pink } Genes"

    **Annotation** · *Which genes carry the calls, and where on the protein?*

    [![Genes dashboard](../../images/pipeline-templates/nf-core/sarek/genes_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/genes_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genes dashboard](../../images/pipeline-templates/nf-core/sarek/genes_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/genes_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    SnpEff's per-gene counts. The genes with a call by biotype, the HIGH-impact
    variants by caller, the top gene burden (the most HIGH or MODERATE variants on
    one gene, the callers' maxima) and the protein changes by impact class. Then
    the gene by callset burden heatmap, coloured by log(1 + variants) so one long
    gene does not wash out the rest, the UpSet of genes the callers share (fixed),
    and the coding variants along the protein, one lane per gene. A high burden is
    often a long, repetitive or poorly mappable gene before it is a biological
    signal. The per-gene burden and protein position tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Biotype` and `Caller` on `snpeff_genes`, and `Impact
        class` on `snpeff_protein_lollipop`.

        | Section | What it holds |
        |---|---|
        | Genes at a glance | 4 cards |
        | Burden across callsets | 1 advanced visualization |
        | Genes the callers share | 1 advanced visualization |
        | Along the protein | 1 advanced visualization |
        | Gene tables (collapsed) | *Per-gene variant burden*, *Coding variants with a protein position* |

=== ":material-map-marker-outline:{ .mc-indigo } Locus"

    **Annotation** · *What do depth and calls show at one region?*

    [![Locus dashboard](../../images/pipeline-templates/nf-core/sarek/locus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/locus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Locus dashboard](../../images/pipeline-templates/nf-core/sarek/locus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/locus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The locus tab stacks four tracks on one `{GENOME}` axis. The depth navigator,
    the mean depth in 1 Mb windows, drives the others: a typed locus or gene, or a
    brush on its axis, moves the depth per interval, the calls over the gene lane
    (one lane per caller) and the annotated VCFs, range-read from their files
    below 2 Mb. It opens on `chr1:1,000,000-2,000,000`. The four cards (calls by
    caller, depth per interval, allele fraction, depth at the call) are recounted
    on the region in view.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` and `Variant type` on `vcf_variants`, for the call
        track and the cards.

        | Section | What it holds |
        |---|---|
        | Region at a glance | 4 cards |
        | One region, four tracks | 4 advanced visualizations: the depth navigator, the depth per interval, the calls over the genes and the annotated VCFs |

Tables and point views select on their entity column: the sample sheet on
`sample_id`; the contig, sex-check, FILTER and distribution tables and the
sex-check scatter on `sample`; the bcftools and SnpEff summary tables on
`caller`; the rainfall plot, the impact scatter and the call tables on
`variant_key`; the per-gene table on `gene_name`, which reaches the protein
lollipop. A pick narrows the other tiles of its collection and follows the
project links to the collections downstream of it. The variant record on
Consequences shows the call picked in the scatter beside it.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/sarek, it does not run the pipeline.
Run the pipeline first, with the callers you want to compare and SnpEff among
the tools:

```bash
nextflow run nf-core/sarek -r 3.10.0 \
  --input samplesheet.csv \
  --genome GATK.GRCh38 \
  --tools haplotypecaller,deepvariant,strelka,freebayes,manta,snpeff \
  --outdir results -profile docker
```

Then point Depictio at the results. sarek 3.10.0 ships a MultiQC parquet, so no
reprocess step is needed:

```bash
depictio ingest results/ --template nf-core/sarek/latest
```

See [nf-co.re/sarek/usage](https://nf-co.re/sarek/3.10.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name; the caller and sample directories under
`reports/`, `variant_calling/` and `annotation/` are read off the path.

```text
<DATA_ROOT>/
├── csv/*.csv                                  # the hub: sarek's resume manifests
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/multiqc_data/multiqc.parquet       # native, no reprocess
├── reports/
│   ├── bcftools/<caller>/<sample>/*.bcftools_stats.txt
│   ├── vcftools/<caller>/<sample>/*.{TsTv.qual,FILTER.summary}   # optional
│   ├── mosdepth/<sample>/*.{mosdepth.summary.txt,regions.bed.gz}
│   └── snpeff/<caller>/<sample>/*_snpEff.{csv,genes.txt}         # optional
├── variant_calling/<caller>/<sample>/*.vcf.gz # one VCF per sample and caller
└── annotation/<caller>/<sample>/
    └── *_snpEff.ann.vcf.gz{,.tbi}             # optional; the index feeds the locus track
```

gVCFs are not read. The somatic outputs (ASCAT, CNVkit, MSIsensor-pro,
NGSCheckMate) are declared optional so a somatic run ingests, but no tile binds
them yet.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 3.10.0 release,
`results-8ccac7ad37b05dd792447763bf9671b719824587`, on its
`test_full_germline_ncbench_agilent/` profile: one NA12878 exome sequenced at two
depths, five germline callers (DeepVariant, FreeBayes, HaplotypeCaller, Manta,
Strelka) and both annotators. The screenshots above come from that run.
`megatest.yaml` lists the tables-only subset the template needs, plus the
per-caller VCFs and their SnpEff twins:

```bash
bash depictio/projects/nf-core/sarek/3.10.0/download_test_data.sh /tmp/sarek_test
depictio ingest /tmp/sarek_test --template nf-core/sarek/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/sarek](https://nf-co.re/sarek): official pipeline documentation
- [nf-co.re/sarek/3.10.0/results](https://nf-co.re/sarek/3.10.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/sarek releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
