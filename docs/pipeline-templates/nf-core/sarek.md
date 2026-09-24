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
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
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

- :material-chart-box-outline: **MultiQC**: read quality, alignment and recalibration, the pooled variant-call QC and the annotation summaries
- :material-chart-bell-curve: **Cohort QC**: coverage per contig and per capture target, a locus browser, and an X against Y sex check
- :material-dna: **Variant yield**: each caller's own statistics side by side, its mutation spectra, what its filters removed
- :material-set-merge: **Caller concordance**: which callsets agree, allele fraction against depth, and where the calls fall
- :material-chart-donut: **Consequences**: SnpEff's composition, recomputed per call with a variant record beside the scatter
- :material-dna: **Genes**: the per-gene burden across callsets and the coding variants along the protein

A `Run at a glance` strip (SNPs called, indels per callset, samples by status,
median Ts/Tv), the collapsed `Sample sheet` and the `Sample filters` (sample,
tumour or normal status) are pinned to every tab, with a collapsed `QC
thresholds` group (a Ts/Tv floor) pinned to the bottom.

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
    depictio run \
      --template nf-core/sarek/latest \
      --data-root /path/to/sarek_results
    ```

    `--data-root` is the only thing you have to pass. The sample hub is built
    from the CSV manifests sarek writes under `csv/` (patient, sex, status and
    the callers run per sample), so the launch samplesheet is not needed. If the
    run was aligned to another assembly than hg38, name it so the locus tracks
    draw the right axis and gene lane:

    ```bash
    depictio run \
      --template nf-core/sarek/latest \
      --data-root /path/to/sarek_results \
      --var GENOME=hg19
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `GENOME` | `hg38` | UCSC name of the assembly (hg38, hg19, mm10): the axis and gene lane of every locus track |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/sarek -r 3.10.0 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
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

Six tabs, read as a funnel: the report, how deeply the targets were covered, how
much each caller called, which callers agree, what the calls do to the
transcript, and which genes carry them. Each tab below carries the **same icon
and colour the dashboard gives it**.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Are the reads, the alignments and the pooled calls sound, before any caller is compared?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/sarek/multiqc_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    The run's native MultiQC report, no reprocess needed: FastQC and fastp on
    the reads, then mapping, duplication, BQSR calibration, mosdepth coverage
    and insert size. The variant-call QC section is what bcftools and VCFtools
    see with every caller pooled, and the annotation section holds the SnpEff
    and VEP summaries. A tab-local `Glance scope` narrows the pinned strip to
    one caller.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and `Status` on the sample hub, persistent and
        pinned to the top of every tab, a `Ts/Tv ratio` range in the collapsed
        *QC thresholds* group pinned to the bottom, and a `Variant caller`
        picker in the tab-local *Glance scope*.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Sample hub*, collapsed and pinned to every tab |
        | MultiQC general statistics | *General statistics* |
        | Read quality | 4 MultiQC panels |
        | Alignment and recalibration | 5 MultiQC panels |
        | Variant-call QC | 4 MultiQC panels |
        | Annotation | 4 MultiQC panels |

=== ":material-chart-bell-curve:{ .mc-blue } Cohort QC"

    *Were the targets covered deeply enough for a call to mean anything?*

    [![Cohort QC dashboard](../../images/pipeline-templates/nf-core/sarek/cohort_qc_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/cohort_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    Coverage bounds every call, so it comes first: target depth per contig,
    depth per capture target, targets under 20x and the X to Y ratio. `One
    locus, three tracks` is a locus browser: a depth navigator binned to 1 Mb
    windows drives, through its locus field or brush, the per-target depth, the
    calls over the gene lane and the annotated VCFs range-read from their files.
    mosdepth's whole-contig and capture-target scopes are then compared per
    contig, and an X against Y depth scatter gives a heuristic sex check.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Contig or targets` picker on mosdepth's summary, in the
        tab-local *Coverage scope*.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | One locus, three tracks | *Depth navigator, 1 Mb windows*, *Depth per capture target*, *Calls over the genes*, *The annotated VCFs, read from the files* |
        | Depth per contig | *Mean depth per contig*, *Per-contig coverage summary* |
        | Sex check | *X depth against Y depth*, *X and Y coverage per sample* |

=== ":material-dna:{ .mc-violet } Variant yield"

    *How much did each caller call, and what did its own filters throw away?*

    [![Variant yield dashboard](../../images/pipeline-templates/nf-core/sarek/variant_yield_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/variant_yield_light.png){ .tpl-shot target="_blank" rel="noopener" }

    Each caller's own bcftools stats and VCFtools reports, caller against
    caller: SNP and indel counts, the substitution and indel spectra as shares
    of each callset, and a parallel-coordinates profile that puts eight QC
    numbers per callset on one plot. The FILTER partitions show what each caller
    discarded, and Ts/Tv against a rising quality floor shows where its quality
    score stops separating variants from noise. The remaining bcftools blocks
    sit behind a block picker.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller` and `FILTER value` in the tab-local *Caller
        scope*, and a `bcftools block` picker in *Distribution scope*.

        | Section | What it holds |
        |---|---|
        | Caller yield | 4 cards |
        | SNPs and indels by caller | *SNPs called per caller*, *Indels called per caller* |
        | Mutation spectra | *Substitution spectrum*, *Indel length spectrum* |
        | Callset QC profile | *Callset QC profile* |
        | Filters and what they cost | *Calls per FILTER partition*, *FILTER breakdown per caller* |
        | Quality calibration | *Ts/Tv against the quality floor* |
        | Distributions | *The chosen distribution, caller by caller*, *bcftools stats distributions* |
        | Variant tables | *Per-caller variant counts*, *Per-caller Ts/Tv*, collapsed |

=== ":material-set-merge:{ .mc-teal } Caller concordance"

    *Which calls do the callers share, and where do they part ways?*

    [![Caller concordance dashboard](../../images/pipeline-templates/nf-core/sarek/caller_concordance_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/caller_concordance_light.png){ .tpl-shot target="_blank" rel="noopener" }

    Two UpSet plots ask the same question twice: exact PASS calls shared between
    callsets, then genes hit by a coding variant. Allele fraction against depth,
    as a density and as a histogram per caller, is the plane a germline callset
    is read on. A rainfall plot of inter-call distances shows where calls
    cluster along the genome, and selecting a call on it narrows the call table.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Caller`, `Variant type`, `Contig` and a `Depth at the
        call` range on the called VCFs, in the tab-local *Call scope*.

        | Section | What it holds |
        |---|---|
        | Concordance at a glance | 4 cards |
        | Which callsets agree | *PASS calls shared between callsets*, *Genes hit by a coding variant, shared between callers* |
        | Depth sensitivity | *Allele fraction against depth, as a density*, *Allele-fraction distribution per caller* |
        | Calls along the genome | *Rainfall, distance to the previous call* |
        | Call table | *Variant calls*, collapsed |

=== ":material-chart-donut:{ .mc-orange } Consequences"

    *What do the calls do to the transcript?*

    [![Consequences dashboard](../../images/pipeline-templates/nf-core/sarek/consequences_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/consequences_light.png){ .tpl-shot target="_blank" rel="noopener" }

    SnpEff's published composition, section by section and caller by caller,
    next to the same composition recomputed from the annotated calls. The allele
    fraction against depth scatter, coloured by impact, drives a linked
    **Variant record** beside it, which folds to a slim rail until a call is
    picked and then links its gene to Ensembl.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `SnpEff section` and `Caller` in the tab-local
        *Composition scope*, and `Impact class` and `Consequence` on the
        annotated calls in *Impact scope*.

        | Section | What it holds |
        |---|---|
        | Consequences at a glance | 4 cards |
        | What kind of variants | *The chosen section, caller by caller*, *SnpEff composition sections* |
        | Impact per call | *Allele fraction against depth, coloured by impact*, *Variant record* |
        | Annotated calls | *Annotated variant calls*, collapsed |

=== ":material-dna:{ .mc-pink } Genes"

    *Which genes carry the variant burden, callset by callset?*

    [![Genes dashboard](../../images/pipeline-templates/nf-core/sarek/genes_light.png){ loading=lazy }](../../images/pipeline-templates/nf-core/sarek/genes_light.png){ .tpl-shot target="_blank" rel="noopener" }

    The per-gene burden SnpEff writes, as a clustered gene by callset heatmap of
    coding-variant counts, then a protein lollipop of the coding variants at
    their amino-acid position. A row picked in the per-gene table drives the
    lollipop. A high burden on long, repetitive genes is a mappability signal
    before it is a biological one.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Biotype` and `Caller` on the per-gene table, in the
        tab-local *Gene scope*, and `Impact class` on the lollipop in *Protein
        scope*.

        | Section | What it holds |
        |---|---|
        | Genes at a glance | 4 cards |
        | Burden across callsets | *Variant burden, gene against callset* |
        | Along the protein | *Coding variants along the protein*, *Coding variants with a protein position* |
        | Gene table | *Per-gene variant burden*, collapsed |

Tables and point views select on their entity column: the sample sheet on
`sample_id`, the per-caller tables on `caller`, the call tables and the rainfall
plot on the variant, and the per-gene table on the gene. A pick narrows every
tile on the tab that reads the same collection or one linked from it.

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
depictio run --template nf-core/sarek/latest --data-root results/
```

See [nf-co.re/sarek/usage](https://nf-co.re/sarek/3.10.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
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
depictio run --template nf-core/sarek/latest --data-root /tmp/sarek_test
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it Experimental.</span>
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
