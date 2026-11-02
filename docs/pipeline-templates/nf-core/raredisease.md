---
title: Rare disease
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/raredisease" target="_blank" title="nf-core/raredisease on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/raredisease/master/docs/images/nf-core-raredisease_logo_dark.png" alt="nf-core/raredisease">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/raredisease/master/docs/images/nf-core-raredisease_logo_light.png" alt="nf-core/raredisease">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Rare disease</h1>
    <p class="template-subtitle">Rare disease analysis of a family, from the alignment to the ranked variants: alignment and coverage QC, pedigree checks, the callset, the GENMOD-ranked variants and their inheritance models, mitochondrial, repeat and mobile element calls, and a genome browser.</p>
    <p class="template-links">
      <a href="https://nf-co.re/raredisease" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/raredisease" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="3.1.2">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="3.1.2" selected>3.1.2</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The raredisease template follows an nf-core/raredisease run on a family, usually a
trio, from the alignment to the ranked variants:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and a leaderboard of the best-ranked variants, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, the alignment and coverage numbers per sample, and whether the samples are the family the pedigree says
- :material-sort-numeric-descending: **Variants**: the callset per sample, the GENMOD-ranked variants with their inheritance models, and the optional mitochondrial and repeat branches
- :material-map-marker-outline: **Locus**: the ranked variants on the genome, with a browser on the calls and alignments


<div class="tpl-showcase">
  <div class="tpl-showcase-bar">
    <span class="tpl-showcase-live"></span>
    <span class="tpl-showcase-label">Live showcase</span>
    <span class="tpl-showcase-meta">nf-core/raredisease, nf-core test data</span>

    <a class="tpl-showcase-open" href="https://showcases.depictio.embl.org/dashboard/6ae792b09e97ca1af10fb760" target="_blank" rel="noopener"><i class="mdi mdi-open-in-new"></i> Open</a>
  </div>
  <iframe class="tpl-showcase-frame" src="https://showcases.depictio.embl.org/dashboard/6ae792b09e97ca1af10fb760" loading="lazy" title="nf-core/raredisease showcase dashboard" allowfullscreen></iframe>
</div>

A pick on a sample, a role (proband, father, mother, sibling) or a family in the
left panel narrows every per-sample collection, the MultiQC report and the genome
browser's tracks.

!!! info "Roles come from the pedigree"
    The pipeline publishes its pedigree as a `.ped` file, so the group the filters
    use is the **role**, read from it, and the affected status colours the
    pedigree figure. A run without the pedigree keys the sample hub on the QC and
    callset samples, and every role reads *Other*.


---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/raredisease_results \
      --template nf-core/raredisease/latest
    ```

    The results directory is the only required value. The run's reference decides
    the one variable you may need to set:

    ```bash
    depictio ingest /path/to/raredisease_results \
      --template nf-core/raredisease/latest \
      --var GENOME=hg38
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `GENOME` | `hg19` | assembly of the navigator, the karyotype and the browser's tracks: `hg19` is the GRCh37 naming, `hg38` that of GRCh38 |
    | `TRACKS_URI` | unset | `s3://` or `https://` folder holding the run's results: the browser reads the alignments and signal tracks in place instead of uploading them from `DATA_ROOT` |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/raredisease -r 3.1.2 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so a GRCh38 run reads on the `hg19` axis; ingest it
    by hand with `GENOME=hg38` instead.


---

## :material-book-open-variant: Reference

The template reads the pedigree, the Picard and mosdepth QC, the family callset,
the VEP-annotated and GENMOD-ranked VCFs (the clinical set is a subset of the
research set and is flagged, so no variant is counted twice), the optional
mitochondrial, repeat expansion, mobile element and SMN outputs, the MultiQC
report and the run parameters. The alignments, the ranked and repeat VCFs and the
signal tracks are never loaded as tables: the genome browser opens them through
their indexes. peddy, GENS, the germline CNV caller and structural variant calling
are not read.

The callset summary, the substitution spectrum and the FILTER breakdown count the
calls a sample carries (a genotype with an alternate allele), not the sites of the
joint file. A target capture (exome) run fills the hybrid-selection coverage columns
instead of the whole-genome ones, and the tiles that read the latter draw a dash.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. A run that skipped the mitochondrial
    branch loses the Mitochondria tab, one without repeat expansion or mobile
    element calling loses their cards and tables.

<div class="tpl-version-block" data-version="3.1.2" markdown>

--8<-- "pipeline-templates/nf-core/_generated/raredisease-latest.md"

</div>


---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then eight child tabs in two groups, read as a
funnel from the reads to what the calls and alignments show at one locus. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Alignment, Family |
| Variants | Callset, Ranked, Mitochondria, Repeats, Locus |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed.

=== ":material-compass-outline: Overview"

    *Rare disease analysis of a family, from the alignment to the ranked variants.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/raredisease/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/raredisease/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Hero, *About* and run cards (genome, analysis type, aligner, caller, VEP cache,
    skipped tools) and six steps (Align, Call, Rank, Mitochondria, Repeats, Report),
    each with its settings and its tab. Four key figures: the clinical variants by
    inheritance model, the top rank score, the samples by role and the mean coverage.
    The findings are led by the top candidate, then a leaderboard of the eight
    best-ranked variants and the pedigree.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *What does the MultiQC report say about reads and alignments?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/raredisease/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/raredisease/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    General statistics, FastQC counts and fastp filtered reads, then the Picard alignment
    summary, duplicates, insert size and the coverage histogram. Base quality, adapter
    content and the mosdepth curves are collapsed.

=== ":material-align-horizontal-left:{ .mc-blue } Alignment"

    **Data & QC** · *What do the alignment, coverage and call numbers say, sample by sample?*

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/raredisease/alignment_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/alignment_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Alignment dashboard](../../images/pipeline-templates/nf-core/raredisease/alignment_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/alignment_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Reads, aligned share, mean coverage, duplication and the mitochondrial to nuclear
    depth ratio, and one table of the samples with the record of the picked sample beside
    it. The contig depth and the full tables are collapsed.

=== ":material-family-tree:{ .mc-pink } Family"

    **Data & QC** · *Are the samples the family the pedigree says they are?*

    [![Family dashboard](../../images/pipeline-templates/nf-core/raredisease/family_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/family_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Family dashboard](../../images/pipeline-templates/nf-core/raredisease/family_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/family_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The samples by affected status, the parent-child IBS0 share and the sex check. The
    pedigree figure from the sample sheet (squares male, circles female, filled marks
    affected) sits beside the opposite homozygous share of every pair of samples, one bar
    each, coloured by the verdict. The pair table is collapsed.

=== ":material-magnify-scan:{ .mc-teal } Callset"

    **Variants** · *How many calls does each sample yield, and how clean are they?*

    [![Callset dashboard](../../images/pipeline-templates/nf-core/raredisease/callset_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/callset_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Callset dashboard](../../images/pipeline-templates/nf-core/raredisease/callset_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/callset_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    PASS calls, Ts/Tv, het/hom ratio and calls by FILTER value. Ts/Tv and het/hom per
    sample as two sorted bars with the usual range shaded (a click narrows the dashboard
    to that sample), and the substitution spectrum folded onto six classes. Ts/Tv is
    about 2.0 to 2.1 for a genome and 2.8 to 3.0 for an exome. The karyotype of one
    sample and the allele fraction per sample are collapsed.

=== ":material-sort-numeric-descending:{ .mc-grape } Ranked"

    **Variants** · *Which variants rank first, and which inheritance model do they fit?*

    [![Ranked dashboard](../../images/pipeline-templates/nf-core/raredisease/ranked_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/ranked_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Ranked dashboard](../../images/pipeline-templates/nf-core/raredisease/ranked_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/ranked_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The 50 best candidates as a leaderboard, best first, with the gene and protein
    change, the inheritance model and impact as badges and the rank score as a bar.
    Hover for the consequence, frequency, CADD and carriers; a click picks the variant
    for the record beside it and opens the pedigree filled by genotype. Then the rank
    score of the 50 best variants, why the 20 best rank (one segment per GENMOD score
    component) and the genotype of every individual at those variants.

=== ":material-atom:{ .mc-yellow } Mitochondria"

    **Variants** · *How heteroplasmic are the mitochondrial calls, and how rare?*

    [![Mitochondria dashboard](../../images/pipeline-templates/nf-core/raredisease/mitochondria_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/mitochondria_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Mitochondria dashboard](../../images/pipeline-templates/nf-core/raredisease/mitochondria_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/mitochondria_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Optional branch. Calls by heteroplasmy class, median heteroplasmy, impact and depth,
    then heteroplasmy along the mitochondrial genome and against the gnomAD frequency.
    The mitochondrion is not on the navigator's axis, so this tab has no genome view.

=== ":material-repeat:{ .mc-red } Repeats"

    **Variants** · *Do any repeat expansions or mobile element insertions stand out?*

    [![Repeats dashboard](../../images/pipeline-templates/nf-core/raredisease/repeats_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/repeats_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Repeats dashboard](../../images/pipeline-templates/nf-core/raredisease/repeats_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/repeats_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Optional branches. Repeat calls by status, pathogenic-range calls by inheritance,
    mobile element insertions by family and SMN calls. One row per repeat locus, each
    call placed by its repeat count as a multiple of the pathogenic threshold over
    shaded normal, intermediate and pathogenic zones; insertions per sample by element
    family. The tables are collapsed.

=== ":material-map-marker-outline:{ .mc-indigo } Locus"

    **Variants** · *What do the calls and alignments show at one locus?*

    [![Locus dashboard](../../images/pipeline-templates/nf-core/raredisease/locus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/locus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Locus dashboard](../../images/pipeline-templates/nf-core/raredisease/locus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/raredisease/locus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A navigator draws every ranked variant at its position, higher for a higher rank
    score and coloured by the inheritance model it fits, linked to a genome browser. The
    browser opens on the span of the 20 best-ranked variants (else the top-ranked one),
    showing the research VCF, the proband alignment and coverage, the parents'
    alignments and the ClinVar and dbSNP tracks; the rest is in its track menu. A brush
    or a typed locus moves the browser, a rank score slider in the left panel narrows the
    points to the top, and the ranked variants of the region are listed below.

Tables and leaderboards select rows, and a pick narrows the other tiles of its
collection and follows the project links to the rest.


---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/raredisease, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/raredisease -r 3.1.2 \
  --input samplesheet.csv \
  --outdir results \
  -profile docker
```

The mitochondrial, repeat expansion, mobile element and SMN branches are optional,
and the template adapts to the ones that ran. Then point Depictio at the results,
naming the assembly the run used if it is GRCh38:

```bash
depictio ingest results/ \
  --template nf-core/raredisease/latest \
  --var GENOME=hg38
```

See [nf-co.re/raredisease/usage](https://nf-co.re/raredisease/3.1.2/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── pedigree/<family>.ped                                  # family, parents, sex, phenotype
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/multiqc_data/multiqc.parquet
├── alignment/<sample>_sorted_md.metrics.txt               # MarkDuplicates (+ BAM and index for the browser)
├── qc_bam/<sample>_{multiplemetrics,wgsmetrics,hsmetrics,mosdepth.mosdepth}.*
├── call_snv/genome/<family>_snv.vcf.gz                    # joint callset
├── rank_and_filter/<family>_{snv,mt}_ranked_*.vcf.gz      # mt: optional
├── repeat_expansions/<family>_repeat_expansion_stranger.vcf.gz   # optional
├── call_mobile_elements/<family>_mobile_elements.vcf.gz          # optional
└── smncopynumbercaller/out/<family>_smncopynumbercaller.tsv      # optional
```

---

## :material-flask-outline: Validation runs

There is no AWS megatest behind this template, so the repository ships no download
script for it. It was built on a real `test_full` run of nf-core/raredisease 3.1.2
executed on the EMBL cluster: a trio on a reduced GRCh37 reference restricted to one
autosome and the mitochondrion, at about 1.4x mean coverage. Every route the
template reads is present in it.

That depth is far too low for the numbers to mean anything biological: the
relatedness estimate is unreliable, the repeat and SMN calls are mostly *No call*,
and there is no X or Y contig, so the sex check reads *Not tested*. peddy, GENS, the
germline CNV caller and structural variant calling were skipped by the run.

---

## :material-link-variant: Additional resources

- [nf-co.re/raredisease](https://nf-co.re/raredisease): official pipeline documentation
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
    <span class="tpl-credit-note">Keep it working as nf-core/raredisease releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
