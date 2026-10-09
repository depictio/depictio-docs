---
title: Ancient DNA
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/eager" target="_blank" title="nf-core/eager on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/eager/dev/docs/images/nf-core-eager_logo_dark.png" alt="nf-core/eager">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/eager/dev/docs/images/nf-core-eager_logo_light.png" alt="nf-core/eager">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Ancient DNA</h1>
    <p class="template-subtitle">Ancient-DNA QC from trimming and collapsing to endogenous content, the deamination and fragment-length signals that authenticate a library, coverage and genotypes, next to the pipeline's MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/eager" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/eager" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="2.4.5">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.4.5" selected>2.4.5</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The eager template follows an nf-core/eager run from raw lanes to genotypes, one
question per tab, in three groups:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC, AdapterRemoval and bcftools panels from the regenerated MultiQC report, every library on every tool at once, and where each sequenced read stops, from trimming and collapsing to deduplication
- :material-dna: **Ancient DNA**: how much of each extract is the target organism, how many distinct molecules each library holds, and whether the DNA is damaged and short, as ancient DNA is
- :material-waves: **Genome**: depth per contig and the depth distribution, depth and mapping quality at one locus, and the variants called per sample

The persistent `Sample filters` (sample, library, UDG treatment) sit in the left
panel and narrow every tab. Below them, the collapsed `QC thresholds` set
coverage, duplication and endogenous-DNA floors: the collections they read link
back to the library hub, so a floor narrows the hub and, through it, every tab.

!!! warning "The MultiQC report must be regenerated"
    eager 2.4.5 ships MultiQC 1.13, which writes no parquet, and Depictio reads
    only `multiqc.parquet` (MultiQC 1.31 and later). Re-run MultiQC over the
    run's own tool outputs before ingesting, or the MultiQC tab stays empty:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src <outdir> --dest <outdir>
    ```

!!! info "Copy the `--input` TSV under `input/`"
    eager 2.x does not publish the samplesheet it was launched with. The library
    hub and the per-lane table read any `input/*.tsv` under the data root, so copy
    the TSV there (several are concatenated, one per batch).

!!! note "Optional branches appear when the run enabled them"
    Sex.DetERRmine, MTNucRatio, ANGSD nuclear contamination, MaltExtract and
    Kraken are optional collections, each bound to one table in a collapsed
    section: *Off-target screen* on Endogenous DNA, *Contamination* on
    Authentication, *Sex determination* on Coverage. A run that did not enable
    the branch ingests without it, and the import drops its table.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/eager_results \
      --template nf-core/eager/latest
    ```

    The results directory is the only thing you have to pass, once the `--input` TSV is
    copied under `input/` and the MultiQC report regenerated. `SHORT_FRAGMENT_BP`
    (default `70`) sets the short-fragment cut-off the Authentication tab counts:

    ```bash
    depictio ingest /path/to/eager_results \
      --template nf-core/eager/latest \
      --var SHORT_FRAGMENT_BP=50
    ```

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/eager -r 2.4.5 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. The samplesheet copy and the MultiQC regeneration above still
    apply. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the run's `--input` TSV, the regenerated MultiQC report and the
tool tables behind it: AdapterRemoval, samtools flagstat, endorS.py, Picard
MarkDuplicates, preseq, DamageProfiler, Qualimap BamQC and bcftools stats. 63 of
its 89 tiles carry a `use:` catalog reference, so a tile says where its panel
comes from. Every file is matched on its name, never on the per-library directory
around it.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.4.5" markdown>

--8<-- "pipeline-templates/nf-core/_generated/eager-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then nine child tabs in three groups, read as a
funnel from the reads to the genotypes called from an ancient extract. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Libraries, Read fate |
| Ancient DNA | Endogenous DNA, Complexity, Authentication |
| Genome | Coverage, Locus, Genotypes |

Each child tab opens with a short intro and, except on MultiQC, a strip of four
cards, then at most three open sections; tables, record cards and the optional
branches follow, collapsed. The template has no group column: the library hub
(`samples`) is one row per eager library, and the biological sample plays the
group's part. The persistent *Sample filters* (sample, library, UDG treatment)
sit in the left panel and narrow every tab through the project links. The
persistent *QC thresholds*, collapsed below them, filter the Qualimap BamQC
summary (mean coverage, duplication rate) and endorS.py (endogenous DNA); both
collections link back to the hub, so a floor narrows the hub and the hub fans the
surviving libraries out. The *Sample sheet* (the library hub) and *Reference
tables* (the BamQC summary the thresholds read) are pinned, collapsed, to the
bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Ancient DNA, from the reads to authentication, coverage and genotypes.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/eager/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/eager/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run's provenance: eager 2.4.5 writes no `params.json`,
    so the dialog lists the software versions the run recorded. *About this
    dashboard* says how the two filter levels work, *The run* lists facts read
    from the run's tables (libraries and samples, the most common UDG treatment,
    the organism, the lanes and reads sequenced), and *Pipeline* walks the six
    steps from trimming to genotyping, each linked to the version of its tool and
    to its tab. The findings are live values: they follow the filters. Each figure
    draws one point or curve per library, so its legend is hidden and the caption
    says what the colour is.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (sample and library), and *Findings* another (sample and UDG
        treatment): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: libraries by sample, endogenous DNA, C to T at the first base, genome covered at 1X |
        | Findings | Live result rows, then 4 figures: endogenous DNA before against after filtering, the preseq complexity curves, the ancient-DNA plane and the genome fraction curves |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did sequencing and trimming work for every library?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/eager/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/eager/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the regenerated report, and only those no tile
    redraws from a tool table: flagstat, Picard, preseq, DamageProfiler and
    Qualimap are left to their tiles. Open: general statistics (endorS.py's
    endogenous DNA included), FastQC sequence counts and the AdapterRemoval
    collapsed-read length, then per-base quality and GC content. Adapter content
    and duplication levels, and the four bcftools panels (substitution types,
    quality, indel lengths, depths), are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Report sample` on `multiqc_data`, the sample as the report
        names it.

        | Section | What it holds |
        |---|---|
        | QC overview | 3 MultiQC panels |
        | Read quality | 2 MultiQC panels |
        | QC details (collapsed) | 2 MultiQC panels |
        | Variant calling (collapsed) | 4 MultiQC panels |

=== ":material-table-account:{ .mc-teal } Libraries"

    **Data & QC** · *How do the libraries compare on every tool at once?*

    [![Libraries dashboard](../../images/pipeline-templates/nf-core/eager/libraries_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/libraries_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Libraries dashboard](../../images/pipeline-templates/nf-core/eager/libraries_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/libraries_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Libraries split by sample, the reads per lane, the reads sequenced (a funnel to
    the reads AdapterRemoval kept) and the mapping quality. Then the per-library QC
    profile: the pipeline-local `eager/library_qc.py` recipe joins endorS.py,
    Picard, Qualimap and DamageProfiler on the library id, and a
    parallel-coordinates tile draws one line per library across seven axes, each
    rescaled to its range. Brush an axis to narrow the profile. Collapsed: the
    pooled table with the record of the row you pick beside it, and the per-lane
    AdapterRemoval table.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Clonality (%)` range on `eager_library_qc` and `Lane` on
        `eager_lane_stats`.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Library QC profile | 1 advanced visualization |
        | Library detail (collapsed) | *Library QC, pooled* + a library record card |
        | Lanes (collapsed) | *Per-lane trimming and collapsing* |

=== ":material-chart-sankey:{ .mc-grape } Read fate"

    **Data & QC** · *Where does every sequenced read stop?*

    [![Read fate dashboard](../../images/pipeline-templates/nf-core/eager/read_fate_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/read_fate_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Read fate dashboard](../../images/pipeline-templates/nf-core/eager/read_fate_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/read_fate_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Reads sequenced split by trimming outcome, the same reads by final fate (a
    ring), the collapse rate and the discard rate per lane. Then one sankey, five
    stages with the reads that fall out at each, its flows coloured by where they
    end. The pipeline-local `eager/read_fate.py` recipe chains AdapterRemoval,
    samtools flagstat and Picard MarkDuplicates, and the accounting is exact: a
    library's retained reads equal its pre-filter flagstat total, so nothing is
    apportioned. Then the lane yield: reads kept and the discard share per lane,
    and the collapse rate against the retained length. The fate table is
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Final fate` on `eager_read_fate` and `Lane` on
        `eager_lane_stats`. There is no trimming-outcome filter: it would leave
        the strip's first card on one outcome.

        | Section | What it holds |
        |---|---|
        | Reads at a glance | 4 cards |
        | Read fate | 1 advanced visualization |
        | Lane yield | *Reads kept for mapping, per lane*, *Reads discarded, per lane*, 1 advanced visualization (collapse rate against retained length) |
        | Read fate table (collapsed) | *Read fate, as counts* |

=== ":material-dna:{ .mc-green } Endogenous DNA"

    **Ancient DNA** · *How much of each extract is the target organism?*

    [![Endogenous DNA dashboard](../../images/pipeline-templates/nf-core/eager/endogenous_dna_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/endogenous_dna_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Endogenous DNA dashboard](../../images/pipeline-templates/nf-core/eager/endogenous_dna_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/endogenous_dna_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Endogenous DNA before filtering, after filtering (a share of 100%), the points
    lost between them and the reads given to the mapper (a funnel to those mapped,
    from flagstat's pre-filter stage). Then each library's endogenous DNA before
    against after filtering, the on-target signal lost to filtering below the
    diagonal, and the mapped reads per library and stage. A low share is normal
    for ancient extracts, where most DNA is environmental. The off-target screen
    (MaltExtract and Kraken, when the run enabled them) and the endorS.py and
    flagstat tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · an `Endogenous DNA after filtering` range on
        `endorspy_endogenous`. There is no stage filter, for the same reason there
        is no trimming-outcome filter on Read fate.

        | Section | What it holds |
        |---|---|
        | Endogenous DNA at a glance | 4 cards |
        | Before and after filtering | 1 advanced visualization |
        | Alignment | *Mapped reads before and after the filter* |
        | Off-target screen (collapsed) | *MaltExtract authentication overview*, *Kraken classification* |
        | Endogenous tables (collapsed) | *Endogenous DNA per library*, *Flagstat, pre- and post-filter* |

=== ":material-content-duplicate:{ .mc-violet } Complexity"

    **Ancient DNA** · *How many distinct molecules does each library hold?*

    [![Complexity dashboard](../../images/pipeline-templates/nf-core/eager/complexity_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/complexity_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Complexity dashboard](../../images/pipeline-templates/nf-core/eager/complexity_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/complexity_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The Picard duplication rate, the reads checked (a funnel to the unique reads
    kept), the duplicates removed and the unique reads kept. Then the screening
    plane, endogenous DNA against clonality with each point sized by depth, and
    side by side the duplication against the unique reads kept and the preseq
    complexity curves. A library worth sequencing deeper is high in endogenous DNA
    and low in duplicates; a flattened curve means the extract, not the sequencing,
    is the limit. eager's preseq run wrote no bootstrap interval, so the curves
    carry no band. The Picard table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Picard duplication` range on
        `picard_markduplicates_metrics`.

        | Section | What it holds |
        |---|---|
        | Duplication at a glance | 4 cards |
        | Screening plane | 1 advanced visualization |
        | Duplication and depth | 2 advanced visualizations: duplication against what survived it and the library complexity curve |
        | Duplication table (collapsed) | *Duplication metrics per library* |

=== ":material-shield-check-outline:{ .mc-red } Authentication"

    **Ancient DNA** · *Is the DNA damaged and short, as ancient DNA is?*

    [![Authentication dashboard](../../images/pipeline-templates/nf-core/eager/authentication_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/authentication_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Authentication dashboard](../../images/pipeline-templates/nf-core/eager/authentication_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/authentication_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    C to T at the 5 prime end, G to A at the 3 prime end, the mean fragment length
    and the share under the `SHORT_FRAGMENT_BP` cut-off. Then the ancient-DNA
    plane, mean length against terminal deamination, beside the fragment length
    curves, and the misincorporation profile (`C>T`, `G>A` and the pooled
    background by position from each read end). Short and damaged is ancient, long
    and undamaged is modern contamination; UDG-treated libraries keep the damage at
    the terminal base only. DamageProfiler 0.4.9 writes no length-binned damage
    table, so the profile is not split by length. The contamination estimates
    (ANGSD and MTNucRatio, when the run enabled them) and the DamageProfiler
    tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Read end` and a `Distance from the read end` range on
        `damageprofiler_misincorporation`, `Strand` and a `Fragment length` range
        on `damageprofiler_lgdistribution`.

        | Section | What it holds |
        |---|---|
        | Damage at a glance | 4 cards |
        | Length and damage | 2 advanced visualizations: the ancient-DNA plane and the fragment length distribution |
        | Misincorporation | 1 advanced visualization |
        | Contamination (collapsed) | *Nuclear contamination (ANGSD)*, *Mitochondrial to nuclear ratio* |
        | Authentication tables (collapsed) | *Authenticity summary per library*, *Misincorporation table*, *Fragment length table* |

=== ":material-waves:{ .mc-blue } Coverage"

    **Genome** · *How deep and how evenly is the reference covered?*

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/eager/coverage_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/coverage_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Coverage dashboard](../../images/pipeline-templates/nf-core/eager/coverage_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/coverage_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The mean coverage per library, the share of the reference covered at 1X and at
    2X, and the depth of the sequences of 1 Mb or more relative to the library
    mean. Then the relative depth against contig length, the quantity a sex call
    and an organelle ratio are made from: an even library sits on 1, the
    mitochondrion far above it, a sex chromosome near 0.5 or 1. Side by side, the
    depth histogram and the share of the reference covered at least X deep, on a
    log depth axis. There is no per-contig bar: on a reference with hundreds of
    scaffolds its axis cannot be read. The Sex.DetERRmine table (when the run
    enabled it) and the per-contig and genome fraction tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Relative depth` and `Contig length` ranges on
        `qualimap_coverage_per_contig`. There is no depth-threshold filter: the 1X
        and 2X cards would print a dash once it excluded their threshold.

        | Section | What it holds |
        |---|---|
        | Coverage at a glance | 4 cards |
        | Per-contig depth | 1 advanced visualization |
        | Depth distribution | 2 advanced visualizations: the depth histogram and the genome fraction curve |
        | Sex determination (collapsed) | *Sex.DetERRmine* |
        | Coverage tables (collapsed) | *Coverage per contig*, *Genome fraction by depth threshold* |

=== ":material-map-marker-outline:{ .mc-cyan } Locus"

    **Genome** · *How deep and how well mapped is one region?*

    [![Locus dashboard](../../images/pipeline-templates/nf-core/eager/locus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/locus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Locus dashboard](../../images/pipeline-templates/nf-core/eager/locus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/locus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The window depth, the windows in view (those at 1X or deeper against the rest),
    the depth spread within a window and the mapping quality; the four cards read
    the whole reference until a region is picked, then that region. Then the locus
    navigator, Qualimap's windows mapped back onto their contigs, with a track of
    mean mapping quality under it from the pipeline-local
    `eager/mapq_across_reference.py`. A `region` link carries the navigator's
    chromosome and position onto that track, so a brush or a typed locus moves both
    tracks and the strip together. A dip in mapping quality under a depth dip marks
    repeats the mapper could not place. The window table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Window depth (X)` range on
        `qualimap_coverage_across_reference`. There is no chromosome filter: the
        navigator owns the region.

        | Section | What it holds |
        |---|---|
        | Region at a glance | 4 cards |
        | Depth along the reference | 2 advanced visualizations: the locus navigator and the mapping quality track |
        | Window table (collapsed) | *Windowed depth* |

    !!! info "The navigator opens on the first contig"
        No contig name holds across references, so the navigator opens on the
        whole first contig of the data. A non-model reference has no built-in
        assembly: the contig list comes from the data and there is no gene lane.

=== ":material-scale-balance:{ .mc-pink } Genotypes"

    **Genome** · *How many variants did each sample yield, and how clean?*

    [![Genotypes dashboard](../../images/pipeline-templates/nf-core/eager/genotypes_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/genotypes_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genotypes dashboard](../../images/pipeline-templates/nf-core/eager/genotypes_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/eager/genotypes_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    SNPs called split by sample, indels, the Ts to Tv ratio and multiallelic
    sites. The VCF record count is not a card: a VCF that emits reference sites
    counts them as records too. Then SNPs and the Ts to Tv ratio per sample, one
    bar per caller. bcftools reads the biological sample from the VCF header, not
    the library, so the hub carries both ids and links on both. A shallow, damaged
    library calls fewer confident variants than its read count suggests, and
    deamination read as variation inflates the transitions. The bcftools summary
    and Ts/Tv tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Variant caller` on `bcftools_stats_summary`.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Calls per sample | *SNPs called per sample*, *Ts to Tv ratio per sample* |
        | Genotype tables (collapsed) | *Variant counts per sample and caller*, *Transition and transversion counts* |

Tables and points select on their entity column: the pinned sample sheet on
`sample_id` and the BamQC reference table on `sample`; the lane table and the
collapse scatter on `lane_id`; the pooled library table, the read fate table and
every per-library table and scatter of the Ancient DNA and Genome tabs on
`sample`, as do the fragment length and genome fraction profiles. A pick narrows
the other tiles of its collection and follows the project links to the
collections they reach. The complexity curve and depth histogram profiles, the
coverage track, and the raw MaltExtract, Kraken, contamination and
Sex.DetERRmine tables do not select. The screening plane emits a selection, but
its collection has no outgoing link, so it narrows no other tile.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/eager, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/eager -r 2.4.5 \
  --input libraries.tsv \
  --fasta reference.fa \
  -profile docker --outdir results
```

Then copy the TSV beside the results, regenerate the MultiQC report and point
Depictio at them:

```bash
mkdir -p results/input && cp libraries.tsv results/input/
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/
depictio ingest results/ --template nf-core/eager/latest
```

See [nf-co.re/eager/usage](https://nf-co.re/eager/2.4.5/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so a run with `--dedupper dedup` or a
different directory layout lands in the same collections.

```text
<DATA_ROOT>/
├── input/*.tsv                                # the run's --input TSV (required, copied by hand)
├── pipeline_info/software_versions.csv
├── multiqc/multiqc_data/multiqc.parquet       # written by multiqc_reprocess
├── fastqc/{input_fastq,after_clipping}/zips/*_fastqc.zip
├── adapterremoval/output/*.settings
├── samtools/
│   ├── stats/*_flagstat.stats
│   └── filtered_stats/*_postfilterflagstat.stats
├── endorspy/*_endogenous_dna_mqc.json
├── deduplication/<library>/*_rmdup.metrics
├── preseq/*.filtered.preseq
├── damageprofiler/<library>_rmdup/
│   ├── *_freq_misincorporations.txt
│   └── *lgdistribution.txt
├── qualimap/<library>_rmdup_stats/
│   ├── genome_results.txt
│   └── raw_data_qualimapReport/*.txt          # coverage and mapping quality across the reference
├── bcftools/stats/*.vcf.stats
└── (optional branches, anywhere under the root)
    ├── *SexDet*.tsv                           # Sex.DetERRmine
    ├── *.mtnucratio                           # MTNucRatio
    ├── nuclear_contamination.txt              # ANGSD
    ├── heatmap_overview_Wevid.tsv             # MaltExtract (HOPS)
    └── *kraken{_parsed,_merged_report}.{csv,tsv}  # Kraken
```

---

## :material-flask-outline: Validation runs

The template was validated on the nf-core AWS megatest of the 2.4.5 release,
`s3://nf-core-awsmegatests/eager/results-42c9d5f8602e5e88fdcec28f194d2cd4cff61c75/`
(every 2.5.x prefix holds `pipeline_info/` only), and the screenshots above come
from that run. The megatest did not enable sex determination, contamination
estimation or a metagenomic screen, so the import drops those tables. Its
samplesheet is not part of the results; the template ships a reconstructed one
under `input/`:

```bash
DEST=/tmp/eager_test
bash depictio/projects/nf-core/eager/2.4.5/download_test_data.sh "$DEST"
mkdir -p "$DEST/input" && cp depictio/projects/nf-core/eager/2.4.5/input/*.tsv "$DEST/input/"
python -m depictio.dev_scripts.multiqc_reprocess --src "$DEST" --dest "$DEST"
depictio ingest "$DEST" --template nf-core/eager/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/eager](https://nf-co.re/eager): official pipeline documentation
- [nf-co.re/eager/2.4.5/results](https://nf-co.re/eager/2.4.5/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/eager releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
