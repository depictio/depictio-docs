---
title: Hi-C
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/hic" target="_blank" title="nf-core/hic on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_dark.png" alt="nf-core/hic">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_light.png" alt="nf-core/hic">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Hi-C</h1>
    <p class="template-subtitle">HiC-Pro's valid-pair funnel as filterable numbers, the contact probability curve, the contact matrix with its insulation, domain and compartment tracks at one locus, and the same calls genome-wide, next to the pipeline's MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/hic" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/hic" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="2.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.0.0" selected>2.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The hic template follows an nf-core/hic run from read pairs to chromatin
architecture:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC and HiC-Pro panels from the regenerated MultiQC report, and every read pair followed to the valid contacts
- :material-grid: **Contacts**: how contact probability falls off with distance, and the contact triangle with its domain, insulation and compartment tracks at one locus
- :material-border-all-variant: **Architecture**: TAD domain sizes and the A/B compartment split, genome-wide

The persistent `Sample filters` sit in the left panel, and a pick there reaches the
funnel, the matrix, every track and the P(s) curve through the project links.

!!! warning "The MultiQC report must be regenerated"
    hic 2.0.0 ships MultiQC 1.13, which writes no parquet, and Depictio reads
    only `multiqc.parquet` (MultiQC 1.31 and later). Re-run MultiQC over the
    run's own tool outputs before ingesting, or the MultiQC tab stays empty:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src <outdir> --dest <outdir>
    ```

!!! info "HiC-Pro's numbers are read twice, on purpose"
    The HiC-Pro panels stay on the MultiQC tab, because that is the report a
    reader may already know. A MultiQC panel cannot be filtered or joined, so
    `hicpro/stats/<sample>/*` is also read directly into a funnel row per sample
    and a weighted row per read-pair fate, which is what the Valid pairs tab and
    the Overview's key figures read.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/hic_results \
      --template nf-core/hic/latest \
      --var GENOME=mm10
    ```

    The results directory is the only required value. `GENOME` (default `hg38`) is the
    UCSC name of the assembly the run was mapped to, which lays out the Contact
    maps axis: pass the UCSC spelling (`mm10`, `hg19`), not an iGenomes key such
    as `GRCm38`. The sample hub is the samplesheet the run validated,
    `samplesheet/samplesheet.valid.csv`, collapsed to one row per sample.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/hic -r 2.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. The MultiQC tab stays empty until the report is regenerated as
    above. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the validated samplesheet, the regenerated MultiQC report,
HiC-Pro's statistics, the balanced `cooler dump` contacts and bins, the cooltools
compartment and insulation outputs, and hicexplorer's distance-decay curve. 51 of
its 53 tiles carry a `use:` catalog reference (`hicpro/*`, `cooler/*`,
`cooltools/*`, `hicexplorer/*`, `multiqc/*`), so a tile says where its panel
comes from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/hic-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in three groups, read as a
funnel from the read pairs to the domains and compartments of the genome. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Valid pairs |
| Contacts | Distance decay, Contact maps |
| Architecture | Domains, Compartments |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The template has no group column:
the sample hub carries the sample id and the FASTQ pairs merged into it, and every
collection carries a sample column. The persistent *Sample filters* (the sample)
sit in the left panel and narrow every tab through the project links. The *Sample
sheet* is pinned, collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Chromatin conformation, from read pairs to domains and compartments.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/hic/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/hic/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run's provenance: hic 2.0.0 writes no `params.json`, so
    the dialog holds the software versions. *About this dashboard* says how the two
    filter levels work, *The run* lists facts read from the data (samples, read
    pairs, unique valid pairs, map resolutions), and *Pipeline* walks the six steps
    from mapping to compartments, each linked to the versions of its process and
    its tab. The findings are live values: they follow the filters. Contact maps
    has no figure here, because it is a browser on one region, not a summary.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* and
        *Findings* each have their own filter bar (the sample and a FASTQ-pairs
        range): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: FASTQ pairs, valid-pair rate, decay slope, domain size |
        | Findings | Live result rows, then 4 figures: the read-pair flow, the contact probability curve, the domain size per insulation window and the A and B bins per chromosome |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the reads map, pair and filter down to valid contacts?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/hic/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/hic/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the regenerated report. Open: general statistics,
    FastQC sequence counts and per-base quality, then HiC-Pro's read mapping, read
    pairing, valid-pair filtering (dangling ends, self circles and re-ligations
    dropped) and contact statistics. The other FastQC panels are collapsed. There
    is no trimming module: HiC-Pro's mapping step trims.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `FASTQ pairs merged` range on the sample hub, which links
        into the report.

        | Section | What it holds |
        |---|---|
        | QC overview | 3 MultiQC panels |
        | HiC-Pro processing | 4 MultiQC panels |
        | Read details (collapsed) | 5 MultiQC panels |

=== ":material-filter-variant:{ .mc-teal } Valid pairs"

    **Data & QC** · *Where do the read pairs go, and how many become valid contacts?*

    [![Valid pairs dashboard](../../images/pipeline-templates/nf-core/hic/valid_pairs_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/valid_pairs_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Valid pairs dashboard](../../images/pipeline-templates/nf-core/hic/valid_pairs_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/valid_pairs_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    HiC-Pro's statistics as numbers: the read pairs processed, the median
    valid-pair rate, the median duplicate rate and the read pairs by mapping
    outcome. Then the read-pair flow, HiC-Pro's three decisions weighted by read
    pairs: does the pair map uniquely at both ends, could a real ligation have
    joined its fragments, and is the contact cis or trans. Each loss peels off into
    a `Lost` lane at the step it stopped at. The read-pair fates and the funnel per
    sample are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Mapping fate` and `Contact fate` on `pair_flow`, and a
        `Valid-pair rate` range on `pair_stats`.

        | Section | What it holds |
        |---|---|
        | Pairs at a glance | 4 cards |
        | Where the pairs go | 1 advanced visualization |
        | Pair tables (collapsed) | *Read-pair fates*, *Valid-pair funnel* |

=== ":material-chart-line:{ .mc-cyan } Distance decay"

    **Contacts** · *How fast does contact frequency fall off with genomic distance?*

    [![Distance decay dashboard](../../images/pipeline-templates/nf-core/hic/distance_decay_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/distance_decay_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Distance decay dashboard](../../images/pipeline-templates/nf-core/hic/distance_decay_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/distance_decay_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median log-log slope, the valid pairs split into cis, trans and
    duplicates, the median long-range share of cis contacts and the long-range cis
    contacts. Then P(s), the probability that two loci a distance s apart touch,
    one curve per chromosome plus the pooled curve, with its local slope in a panel
    underneath. It is recomputed from the balanced contact dump, because
    nf-core/hic never runs `cooltools expected-cis`, and its denominator counts
    every bin pair that could have been observed, which keeps the tail from
    flattening. A slope near -1 is the usual interphase range; a bump or a plateau
    points to trans contamination or a rearrangement.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Chromosome` on `distance_profile`. Picking a curve narrows
        the P(s) table to that chromosome.

        | Section | What it holds |
        |---|---|
        | Decay at a glance | 4 cards |
        | Contact probability | 1 advanced visualization |
        | Curve tables (collapsed) | *P(s) bins*, *Distance-decay curve* |

=== ":material-grid:{ .mc-indigo } Contact maps"

    **Contacts** · *What do the contacts, domains and compartments look like at one locus?*

    [![Contact maps dashboard](../../images/pipeline-templates/nf-core/hic/contact_maps_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/contact_maps_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Contact maps dashboard](../../images/pipeline-templates/nf-core/hic/contact_maps_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/contact_maps_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The locus tab stacks four collections on one `{GENOME}` axis. The TAD domain
    track is the navigator: a typed locus or a brush on its axis emits a region
    that `region` links carry to the contact triangle, the insulation score and the
    phased E1 compartment track below it. The triangle reads the finest dumped
    resolution that fits the span, so zooming re-bins it. The four cards (median
    balanced contact, insulation score, domains, A and B bins) are recounted on the
    region in view.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Domain window (bp)`, `Insulation window (bp)` and
        `Compartment resolution (bp)` choose which calls the tracks draw. There is
        no chromosome filter: the locus field is the tab's chromosome.

        | Section | What it holds |
        |---|---|
        | Region at a glance | 4 cards |
        | One region, four tracks | 4 advanced visualizations: the TAD domain navigator, the contact triangle, the insulation score and the E1 track |

=== ":material-border-all-variant:{ .mc-pink } Domains"

    **Architecture** · *How many TAD domains are there, and how large are they?*

    [![Domains dashboard](../../images/pipeline-templates/nf-core/hic/domains_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/domains_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Domains dashboard](../../images/pipeline-templates/nf-core/hic/domains_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/domains_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Genome-wide, no tracks. The median domain size, the domains called, the median
    mappable share of a domain and the insulation bins split into boundaries and
    the rest. Then the domain size per insulation window, one box per window.
    cooltools calls boundaries, not domains, and nf-core/hic 2.x emits no interval
    list, so the domains are derived from runs of boundary bins, and a domain that
    is mostly unmappable is dropped. Each window calls its own set: pick one before
    comparing counts.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Domain window (bp)` on `tad_domains` and `Insulation window
        (bp)` on `tad_insulation`.

        | Section | What it holds |
        |---|---|
        | Domains at a glance | 4 cards |
        | Domain sizes | *Domain size by insulation window* |
        | Domain tables (collapsed) | *TAD domains*, *Insulation bins* |

=== ":material-scale-balance:{ .mc-violet } Compartments"

    **Architecture** · *How does the genome split between the A and B compartments?*

    [![Compartments dashboard](../../images/pipeline-templates/nf-core/hic/compartments_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/compartments_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Compartments dashboard](../../images/pipeline-templates/nf-core/hic/compartments_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/hic/compartments_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Genome-wide, no tracks. The bins with an E1 sign split into A and B, the median
    E1 (two humps when compartments are strong) and the first and second
    eigenvalues. Then the A and B bins per chromosome. nf-core/hic passes no
    phasing track, so E1 is oriented per chromosome and resolution to correlate
    with bin coverage: the better-covered side is A, and the call does not flip
    between resolutions. Pick one resolution before comparing.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Compartment resolution (bp)` and `Compartment` on
        `compartment_eigenvector`.

        | Section | What it holds |
        |---|---|
        | Compartments at a glance | 4 cards |
        | A and B per chromosome | *A and B bins per chromosome* |
        | Compartment tables (collapsed) | *Compartment bins*, *Compartment eigenvalues* |

Tables select rows and the P(s) curve selects a chromosome: the sample sheet on
`sample_id`; the pair fates, the funnel, the P(s) bins and the eigenvalue tables
on `sample`; the P(s) curve on `chrom`. A pick narrows the other tiles of its
collection and follows the project links to the collections they reach. The
domain, insulation and compartment tables do not select: their rows are bins and
domains with no identifier column.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/hic, it does not run the pipeline.
Run the pipeline first, without `--skip_compartments` or `--skip_tads`:

```bash
nextflow run nf-core/hic -r 2.0.0 \
  --input samplesheet.csv \
  --genome GRCm38 --digestion dpnii \
  -profile docker --outdir results
```

Then regenerate the MultiQC report and point Depictio at the results, passing the
UCSC name of the same assembly:

```bash
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/
depictio ingest results/ --template nf-core/hic/latest --var GENOME=mm10
```

See [nf-co.re/hic/usage](https://nf-co.re/hic/2.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name, so a run with a different `--outdir`
layout lands in the same collections.

```text
<DATA_ROOT>/
├── samplesheet/samplesheet.valid.csv          # the hub: one row per FASTQ pair
├── pipeline_info/software_versions.yml
├── multiqc/multiqc_data/multiqc.parquet       # written by multiqc_reprocess
├── fastqc/*.zip                               # raw MultiQC inputs
├── hicpro/stats/<sample>/
│   └── *.{mmapstat,mpairstat,mRSstat,mergestat}
├── contact_maps/
│   ├── *_balanced.txt                         # cooler dump, one per resolution
│   └── cooler_bins_<resolution>.bed
├── compartments/
│   ├── *.cis.vecs.tsv                         # cooltools eigs-cis E1
│   └── *.cis.lam.txt                          # eigenvalues
├── tads/*_balanced_insulation.tsv             # cooltools insulation
└── distance_decay/*_distcount.txt             # hicPlotDistVsCounts
```

---

## :material-flask-outline: Validation runs

The template was validated on the nf-core AWS megatest of the 2.0.0 release,
`s3://nf-core-awsmegatests/hic/results-b4d89cfacf97a5835fba804887cf0fc7e0449e8d/`,
a single mouse ES cell sample merged from three FASTQ pairs, and the screenshots
above come from that run with `GENOME=mm10`. With one sample the sample filter
has one value, but nothing in the template assumes it: every collection carries a
sample column and the links are ready for a cohort.

```bash
DEST=/tmp/hic_test
bash depictio/projects/nf-core/hic/2.0.0/download_test_data.sh "$DEST"
python -m depictio.dev_scripts.multiqc_reprocess --src "$DEST" --dest "$DEST"
depictio ingest "$DEST" --template nf-core/hic/latest --var GENOME=mm10
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/hic](https://nf-co.re/hic): official pipeline documentation
- [nf-co.re/hic/2.0.0/results](https://nf-co.re/hic/2.0.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/hic releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
