---
title: Genome assembly
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/genomeassembler" target="_blank" title="nf-core/genomeassembler on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/genomeassembler/master/docs/images/nf-core-genomeassembler_logo_dark.png" alt="nf-core/genomeassembler">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/genomeassembler/master/docs/images/nf-core-genomeassembler_logo_light.png" alt="nf-core/genomeassembler">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Genome assembly</h1>
    <p class="template-subtitle">Contiguity, Merqury k-mer accuracy and BUSCO gene completeness of every assembly, polishing and scaffolding stage, compared across assembly strategies, with the GenomeScope read profile as the yardstick.</p>
    <p class="template-links">
      <a href="https://nf-co.re/genomeassembler" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/genomeassembler" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
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

The genomeassembler template follows an nf-core/genomeassembler run from its raw
assemblies through polishing and scaffolding, one tab per question, in three
groups:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-flask-outline: **Data & QC**: which samples reached assembly QC and at which stages, and the genome the reads describe before any assembly, from the k-mer spectrum and GenomeScope
- :material-trophy: **Assemblies**: which assembly is best across contiguity, accuracy and genes, and what each polishing and scaffolding step adds to a sample's assembly
- :material-ruler: **Quality**: Nx curves and QUAST for contiguity, Merqury QV, k-mer completeness and copy number for accuracy, and BUSCO for gene completeness

The persistent `Sample filters` (the design group, then the sample id) sit in the
left panel and narrow every per-assembly tab through the samplesheet links;
Genome profile reads per read set and has its own `Read set` filter.

!!! info "No MultiQC report, one row per assessed assembly"
    nf-core/genomeassembler writes no MultiQC report, so there is no MultiQC tab:
    every tile reads the QC tools' own files. The unit of every tile is the
    assessed assembly, which every QC tool names `<sample>_<stage>`: the raw
    assembly, each polishing step (medaka, dorado, pilon) and each scaffolder
    (LINKS, LongStitch, RagTag). A sample whose assembly never reached QC stays
    in the sample sheet as `No assembly QC` and appears in no other tile.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/genomeassembler_results \
      --template nf-core/genomeassembler/latest \
      --var METADATA_FILE=/path/to/samplesheet.csv \
      --var GROUP_COL=strategy
    ```

    The pipeline publishes no copy of its samplesheet, and the samplesheet is the
    design every filter reads. `METADATA_FILE` defaults to `input/samplesheet.csv`
    under the data root, so copying the sheet there is enough. `GROUP_COL`
    (default `strategy`) picks the column the design filter and the colours group
    on: `assembler`, `polish`, `group` or any column you added work too, since
    every per-assembly table carries the samplesheet columns through.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/genomeassembler -r 2.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads, per assessed assembly, the samtools idxstats of the reads
mapped back (every sequence and its length, from which N50, L50, auN and the Nx
curve are computed), Merqury's QV, completeness, per-sequence QV and copy-number
spectrum, the BUSCO batch summary and QUAST's transposed report; and per read
set, the jellyfish histogram and GenomeScope's summary. Every tool collection is
optional, so a run that skipped a tool, or an assembly a tool never reached,
prunes that tool's tiles instead of breaking the import, and a tab left without
data is dropped. 26 of its 57 tiles carry a `use:` catalog reference, so a tile
says where its panel comes from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/genomeassembler-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then seven child tabs in three groups, read as a
funnel from the samples and the genome their reads describe to the contiguity,
accuracy and gene completeness of every assembly. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read
alike.

| Group | Tabs |
|---|---|
| Data & QC | Samples, Genome profile |
| Assemblies | Best assembly, Stages |
| Quality | Contiguity, Accuracy, Gene completeness |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables, details and comparisons follow, collapsed. The
pipeline writes no MultiQC report, so there is no MultiQC tab, and the unit of
every tile is the assessed assembly, `<sample>_<stage>`: one sample contributes
several rows. The persistent *Sample filters* (the group, then the sample id, on
the samplesheet) sit in the left panel and narrow every per-assembly tab through
the samplesheet links; Genome profile reads per read set, which no sample link
reaches. The *Sample sheet* (one row per samplesheet sample, with how far its
assembly QC got) is pinned, collapsed, to the bottom of every child tab. Every QC
collection is optional: a run without Merqury, BUSCO or k-mer profiling loses the
Accuracy, Gene completeness or Genome profile tab, with the Overview rows and
highlights that pointed at it.

=== ":material-compass-outline: Overview"

    *De novo assemblies scored for contiguity, k-mer accuracy and gene completeness.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/genomeassembler/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/genomeassembler/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how the two
    filter levels work, *The run* lists the samples, the assessed assemblies, the
    BUSCO lineage and the k-mer size, and *Pipeline* walks the six steps from reads
    to a scored genome (profile, assemble, polish, scaffold, measure, score), each
    linked to the parameters that drive it and to its tab. The QV card reads
    against QV 40, the Earth BioGenome Project floor. The three assembly cards read
    `assemblies`, which every route writes, so a QC tool the run skipped leaves a
    dash rather than a gap in the row. The findings are live values: they follow
    the filters.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (the group and the sample id), and *Findings* another (the
        group and the stage class): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples by group, N50, consensus QV, BUSCO complete |
        | Findings | Live result rows, then 4 figures: N50 against QV per assembly, the QV along each route, the Nx curves and the BUSCO classes per assembly |
        | How to read this dashboard | The tabs by group, each with its question |

=== ":material-flask-outline:{ .mc-teal } Samples"

    **Data & QC** · *Which samples reached assembly QC, and at which stages?*

    [![Samples dashboard](../../images/pipeline-templates/nf-core/genomeassembler/samples_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/samples_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Samples dashboard](../../images/pipeline-templates/nf-core/genomeassembler/samples_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/samples_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The samples as a ring by QC status, the assessed assemblies split by stage
    class, the distinct stages assessed ranked by stage class, and the mean number
    of QC tools per assembly on a gauge out of four (samtools, Merqury, BUSCO,
    QUAST). Then the assessed stages per sample, one block per assessed assembly
    coloured by stage, a code figure so the count axis steps by one; a group-by
    set in Analysis mode splits it into panels. A sample marked `No assembly QC`
    reached no QC tool and appears on no other tab: the sample sheet below lists
    it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `QC status` on `sample_status`, and `Stage class` and
        `Assembler` on `assemblies`.

        | Section | What it holds |
        |---|---|
        | Samples at a glance | 4 cards |
        | Assessed stages | *Assessed stages per sample* |

=== ":material-chart-bell-curve:{ .mc-orange } Genome profile"

    **Data & QC** · *What genome do the reads describe, before any assembly?*

    [![Genome profile dashboard](../../images/pipeline-templates/nf-core/genomeassembler/genome_profile_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/genome_profile_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genome profile dashboard](../../images/pipeline-templates/nf-core/genomeassembler/genome_profile_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/genome_profile_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    GenomeScope's haploid genome size, heterozygosity, repeat share and the lowest
    model fit over the read sets. Then the jellyfish k-mer spectrum GenomeScope
    fits, one line per read set. The haploid length is the size an assembly should
    approach; a high heterozygosity warns of duplicated haplotigs, and a poor model
    fit means the other estimates are not to be trusted. The GenomeScope table is
    collapsed. Both collections are per read set, not per assembly: the sample
    filters do not reach this tab, and the `Read set` filter does the narrowing.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Read set` on `genomescope_summary`, which links to the
        spectrum.

        | Section | What it holds |
        |---|---|
        | Genome profile at a glance | 4 cards |
        | K-mer spectrum | 1 advanced visualization |
        | Genome profile table (collapsed) | *GenomeScope estimates* |

=== ":material-trophy:{ .mc-indigo } Best assembly"

    **Assemblies** · *Which assembly is best across contiguity, accuracy and genes?*

    [![Best assembly dashboard](../../images/pipeline-templates/nf-core/genomeassembler/best_assembly_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/best_assembly_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Best assembly dashboard](../../images/pipeline-templates/nf-core/genomeassembler/best_assembly_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/best_assembly_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The best N50, QV, share of complete BUSCOs and k-mer completeness over the
    assemblies in view, each with every assembly's spread. Then the parallel
    coordinates over N50, sequence count, length, QV and k-mer completeness,
    coloured by group; brush an axis to keep a range. BUSCO stays off it: the plot
    drops a line that misses an axis, and BUSCO scores fewer assemblies than
    Merqury. Below, N50 against QV coloured by assembler, with the assembly record
    card beside it, which waits for a picked point. The assembly table is
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Stage class`, `Assembler` and a `Consensus QV` range on
        `assemblies`.

        | Section | What it holds |
        |---|---|
        | Best assembly at a glance | 4 cards |
        | Every assembly | 1 advanced visualization |
        | Contiguity against accuracy | 2 advanced visualizations: the N50 against QV scatter and the assembly record card |
        | Assembly table (collapsed) | *Assessed assemblies* |

=== ":material-chart-timeline-variant:{ .mc-grape } Stages"

    **Assemblies** · *What does each polishing and scaffolding step add?*

    [![Stages dashboard](../../images/pipeline-templates/nf-core/genomeassembler/stages_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/stages_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Stages dashboard](../../images/pipeline-templates/nf-core/genomeassembler/stages_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/stages_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A route runs from a sample's raw assembly through polishing to one scaffolder.
    The routes ranked by the stage they end on, the largest QV gain, the largest
    N50 fold change and the lowest share of complete BUSCOs over the steps. Then
    the QV and the N50 fold change along each route, one line per route: a line
    that climbs gained at that step, a flat one changed nothing the metric can
    see. Pick a route on either chart to follow it on both. The comparison of raw
    assemblies against scaffolds, metric by metric (a screen, not a verdict, with
    few assemblies per class), and the route table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Final stage` and `Route` on `stage_steps`.

        | Section | What it holds |
        |---|---|
        | Stages at a glance | 4 cards |
        | QV along each route | 1 advanced visualization |
        | N50 along each route | 1 advanced visualization |
        | Stage comparison (collapsed) | 1 advanced visualization |
        | Route table (collapsed) | *Stage routes* |

=== ":material-ruler:{ .mc-blue } Contiguity"

    **Quality** · *How long and how fragmented is each assembly?*

    [![Contiguity dashboard](../../images/pipeline-templates/nf-core/genomeassembler/contiguity_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/contiguity_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Contiguity dashboard](../../images/pipeline-templates/nf-core/genomeassembler/contiguity_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/contiguity_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median assembled length, N50, L50 and sequence count. Then the Nx curves,
    computed from the samtools idxstats sequence lengths of every assessed
    assembly, so they cover assemblies QUAST never scored: N50 is the point at 50%,
    and a curve that stays high far to the right holds its length in few long
    sequences. Then QUAST's reference-free view, N50 against assembled length
    beside the length kept above each contig length. QUAST against a reference,
    written only when the run had one, and the QUAST tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Stage` and an `N50 (bp)` range on `assemblies`.

        | Section | What it holds |
        |---|---|
        | Contiguity at a glance | 4 cards |
        | Nx curves | 1 advanced visualization |
        | QUAST | 2 advanced visualizations: N50 against assembled length and the length kept above each contig length |
        | QUAST against a reference (collapsed) | 1 advanced visualization |
        | QUAST tables (collapsed) | *QUAST reference-free statistics*, *QUAST against the reference* |

    !!! info "QUAST is optional, the reference too"
        A run without QUAST has no QUAST sections on this tab; a run without a
        reference has no reference view or table. The Nx curves and the strip do
        not depend on QUAST.

=== ":material-check-decagram:{ .mc-cyan } Accuracy"

    **Quality** · *How accurate is each assembly against the read k-mers?*

    [![Accuracy dashboard](../../images/pipeline-templates/nf-core/genomeassembler/accuracy_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/accuracy_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Accuracy dashboard](../../images/pipeline-templates/nf-core/genomeassembler/accuracy_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/accuracy_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median consensus QV, the median k-mer completeness, the sequences Merqury
    scored (a ring, error-free or not) and the median error k-mers per assembly.
    Then QV against k-mer completeness, with a line at Q40 and the points under it
    dimmed, and the copy number of the read k-mers in each assembly. Merqury takes
    the read k-mers as the truth set: assembly k-mers missing from the reads are
    errors (the QV), solid read k-mers missing from the assembly are lost sequence,
    and the copy-number bars show lost, collapsed and duplicated sequence. The
    per-sequence QV scatter and the Merqury table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Consensus QV` range on `merqury_assembly_qv` and
        `Error-free sequence` on `merqury_sequence_qv`.

        | Section | What it holds |
        |---|---|
        | Accuracy at a glance | 4 cards |
        | QV and completeness | 1 advanced visualization |
        | Copy number | 1 advanced visualization |
        | Per-sequence errors (collapsed) | 1 advanced visualization |
        | Accuracy table (collapsed) | *Merqury QV and completeness* |

=== ":material-shield-check-outline:{ .mc-violet } Gene completeness"

    **Quality** · *How many conserved single-copy genes does each assembly hold?*

    [![Gene completeness dashboard](../../images/pipeline-templates/nf-core/genomeassembler/gene_completeness_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/gene_completeness_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Gene completeness dashboard](../../images/pipeline-templates/nf-core/genomeassembler/gene_completeness_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeassembler/gene_completeness_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median share of complete BUSCOs (counting the assemblies at 90% or above),
    the highest duplicated share, and the median fragmented and missing shares,
    each with its spread. Then the BUSCO classes per assembly and complete against
    duplicated BUSCOs. Complete BUSCOs say the gene space is there; duplicated ones
    point to retained haplotigs, fragmented and missing ones to gaps or errors.
    The BUSCO table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `BUSCO lineage` and a `Complete BUSCOs (%)` range on
        `busco_batch_summary`.

        | Section | What it holds |
        |---|---|
        | Genes at a glance | 4 cards |
        | BUSCO classes | 1 advanced visualization |
        | Complete against duplicated | 1 advanced visualization |
        | BUSCO table (collapsed) | *BUSCO batch summary* |

Tables and points select on their entity column: every per-assembly tile (the
Best assembly scatter and table, the QUAST, Merqury and BUSCO scatters and tables,
the Nx curves) on `assembly_id`, the per-sequence QV scatter on `sequence`, the
stage profiles and the route table on `route`, the GenomeScope table on
`read_set` and the pinned sample sheet on `sample`. A pick narrows the other
tiles of its collection and follows the project links to the collections they
reach. The parallel coordinates, the k-mer spectrum, the length ladder, the
copy-number bars and the BUSCO class bars do not select.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/genomeassembler, it does not run the
pipeline. Run the pipeline first; give it a reference (`use_ref` and
`ref_fasta`, see the usage docs) if you want QUAST's reference-based view:

```bash
nextflow run nf-core/genomeassembler -r 2.0.0 \
  --input samplesheet.csv \
  --busco_lineage <lineage>_odb12 \
  --outdir results -profile docker
```

Then copy the samplesheet under `input/` and point Depictio at the results:

```bash
mkdir -p results/input && cp samplesheet.csv results/input/
depictio ingest results/ --template nf-core/genomeassembler/latest
```

See [nf-co.re/genomeassembler/usage](https://nf-co.re/genomeassembler/2.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name. The pipeline writes one directory per
sample, plus one per read `group` that holds the reads-only outputs.

```text
<DATA_ROOT>/
├── input/
│   └── samplesheet.csv                          # the hub (METADATA_FILE default)
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── <sample>/QC/
│   ├── alignments/<sample>_<stage>.idxstats      # sequence lengths: N50, L50, Nx
│   ├── merqury/*.qv, *.completeness.stats, *.spectra-cn.hist
│   ├── BUSCO/*-busco.batch_summary.txt
│   └── QUAST/<sample>_<stage>/transposed_report.tsv
└── <sample or group>/reads/genomescope/
    ├── genomescope/*_genomescope.txt
    └── jellyfish/histo/*_hist.tsv
```

`METADATA_ID_COL` (default `sample`) is the column every output directory is
named after. The assemblies themselves, the BAM files and the BUSCO run
directories are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 2.0.0 release
(`results-a72d47d9cdb50f21b97882dfb2abf4af8f4c74ad`, the full test samplesheet
without medaka), and the screenshots above come from it. That run is partial:
LINKS failed on one sample and the tasks aborted after it, so only half of the
samples reached assembly QC, QUAST and BUSCO ran on a few assemblies, and only
the raw, LINKS and RagTag stages carry data. The polishing stages and Hi-C
scaffolding are wired by name but not yet verified on data. `megatest.yaml`
lists the tables-only subset, and the download script also places the vendored
samplesheet under `input/`:

```bash
bash depictio/projects/nf-core/genomeassembler/2.0.0/download_test_data.sh /tmp/genomeassembler_test
depictio ingest /tmp/genomeassembler_test --template nf-core/genomeassembler/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/genomeassembler](https://nf-co.re/genomeassembler): official pipeline documentation
- [nf-co.re/genomeassembler/2.0.0/results](https://nf-co.re/genomeassembler/2.0.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/genomeassembler releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
