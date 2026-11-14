---
title: Viral metagenomics
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/viralmetagenome" target="_blank" title="nf-core/viralmetagenome on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/viralmetagenome/master/docs/images/nf-core-viralmetagenome_logo_dark.png" alt="nf-core/viralmetagenome">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/viralmetagenome/master/docs/images/nf-core-viralmetagenome_logo_light.png" alt="nf-core/viralmetagenome">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Viral metagenomics</h1>
    <p class="template-subtitle">MultiQC and the read funnel, the contigs the assemblers built, each consensus genome against its reference, the depth and breadth of the mappings, and the iVar variant calls.</p>
    <p class="template-links">
      <a href="https://nf-co.re/viralmetagenome" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/viralmetagenome" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="1.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.2.0" selected>1.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The viralmetagenome template follows an nf-core/viralmetagenome run from
metagenomic reads to viral consensus genomes and their variants:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and a link to every tab
- ![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } **MultiQC**: reads, trimming, host removal, mapping, duplicates and coverage from the MultiQC report
- :material-test-tube: **Samples**: how many reads of each sample reach assembly
- :material-puzzle-outline: **Contigs**: the de novo contigs, their taxonomic call and their clusters
- :material-virus: **Consensus**: each genome's identity to its reference, ambiguous bases and CheckV tier
- :material-chart-line: **Mapping**: depth and breadth of coverage per genome
- :material-dna: **Variants**: the iVar calls on a genome view, by allele frequency and depth

The persistent `Sample filters` sit in the collapsed left panel, and the *Sample
sheet* is pinned, collapsed, to the bottom of every child tab.

!!! warning "The MultiQC report must be regenerated"
    viralmetagenome 1.2.0 ships MultiQC 1.27, which writes no parquet, and Depictio
    reads only `multiqc.parquet` (MultiQC 1.31 and later). Rebuild the report from
    the run's own tool outputs before ingesting, or the MultiQC tab stays empty:

    ```bash
    python -m depictio.dev_scripts.multiqc_reprocess --src <outdir> --dest <outdir> --exclude '*_mqc.tsv'
    ```

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/viralmetagenome_results \
      --template nf-core/viralmetagenome/latest \
      --var METADATA_FILE=/path/to/metadata.tsv
    ```

    `METADATA_FILE` is optional: the table given to `--metadata`, which the pipeline
    merges into its samples overview but does not publish. Its sample id is in a
    column named `sample` (or the first column) and every other column is a factor;
    the first factor becomes the group (`GROUP_COL`). Without it the samples carry one
    constant group, and `--var GROUP_COL=<column>` still finds a factor of the
    overview.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/viralmetagenome -r 1.2.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. The MultiQC tab stays empty until the report is regenerated as above. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the pipeline's overview tables (samples, contigs, refinement
steps and constraint mappings), the contig classes and clusters, CheckV, the raw
iVar tables, the mosdepth depth tables and the regenerated MultiQC report. A run
takes the de novo route, the constraint route or both, and every collection a
route does not write is optional: the tiles that read it are pruned.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="1.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/viralmetagenome-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in three groups, read as a
funnel from the reads to the variants. Each tab below carries the **same icon and
colour the dashboard gives it**.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Samples |
| Assembly | Contigs, Consensus, Mapping |
| Variants | Variants |

=== ":material-compass-outline: Overview"

    *Viral genomes from metagenomic reads, to consensus and variants.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A hero, *About* and *The run* cards and a six-step pipeline flow. Four key figures
    (samples, clean read pairs, consensus genomes, breadth at 10X) have their own group
    and sample filter bar. Four findings (contigs, consensus, mapping, variants) each
    link to their tab.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *What does the MultiQC report say about reads and mappings?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    FastQC reads per run, fastp's kept and removed reads, base quality and the Kraken2
    host taxa. Then, one row per mapping, samtools percent mapped, Picard duplicates,
    mosdepth cumulative coverage and the bcftools substitution types.

=== ":material-test-tube:{ .mc-teal } Samples"

    **Data & QC** · *How many reads of each sample reach assembly?*

    [![Samples dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/samples_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/samples_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Samples dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/samples_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/samples_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Four cards: the read funnel, the host share, Q30 bases against Illumina's 80 % floor
    and FastQC's duplicate share. Then the read pairs of every sample at each stage, and
    a sample plane of raw read pairs against the share retained, coloured by the group.
    The per-stage table is collapsed.

=== ":material-puzzle-outline:{ .mc-violet } Contigs"

    **Assembly** · *Which contigs did the assembly build, and what are they?*

    [![Contigs dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/contigs_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/contigs_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Contigs dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/contigs_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/contigs_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards for the contigs by taxonomic call, the assembled bases by length band, the
    reads on contigs by cluster role and the clusters refined or filtered out. Then
    every contig by length and the reads that map back to it, and the read depth share
    of the clusters per sample. The tab exists only on the de novo route.

=== ":material-virus:{ .mc-grape } Consensus"

    **Assembly** · *How close to a reference and how complete is each genome?*

    [![Consensus dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/consensus_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/consensus_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Consensus dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/consensus_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/consensus_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards for the genomes by route, the ambiguous bases (5 % N passes, 20 % warns), the
    identity to the closest reference and the CheckV tier. Then every genome by
    ambiguous bases and identity, coloured by route, with the record of the picked one,
    and the ambiguous bases of each de novo consensus along its refinement.

=== ":material-chart-line:{ .mc-blue } Mapping"

    **Assembly** · *How deep and how evenly do the reads cover each genome?*

    [![Mapping dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/mapping_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/mapping_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Mapping dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/mapping_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/mapping_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards for the reads mapped, the mean depth, the breadth at 10X (90 % passes, 50 %
    warns) and the duplicate pairs. Then the depth along each genome in bins (log), and
    the depth against the breadth per genome beside the cumulative coverage curves.

=== ":material-dna:{ .mc-red } Variants"

    **Variants** · *Which variants does each genome carry, and how fixed are they?*

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/variants_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/variants_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Variants dashboard](../../images/pipeline-templates/nf-core/viralmetagenome/variants_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/viralmetagenome/variants_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cards for the passing calls by allele frequency band (fixed at 0.9 or more, major
    from 0.5, minor below), the minor calls kept or filtered, the call depth and the
    genomes carrying a passing call. Then every call on a genome view, one lane per
    genome, and the allele frequency against the depth.

Tables are collapsed at the bottom of their tab.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/viralmetagenome, it does not run the pipeline.
Run the pipeline first, with a metadata table if you want a design group:

```bash
nextflow run nf-core/viralmetagenome -r 1.2.0 \
  --input samplesheet.csv --metadata metadata.tsv \
  -profile docker --outdir results
```

Then rebuild the MultiQC report and point Depictio at the results:

```bash
python -m depictio.dev_scripts.multiqc_reprocess --src results/ --dest results/ --exclude '*_mqc.tsv'
depictio ingest results/ --template nf-core/viralmetagenome/latest \
  --var METADATA_FILE=metadata.tsv
```

See [nf-co.re/viralmetagenome/usage](https://nf-co.re/viralmetagenome/1.2.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name. Every published file name carries the run's
`--global_prefix`, so the template matches on the suffix and reads a run whatever
its prefix.

```text
<DATA_ROOT>/
├── overview-tables/
│   └── *{samples,contigs,mapping}_overview.tsv     # the pipeline's own merge of its MultiQC sections
├── assembly/
│   ├── assemblers/<assembler>/idxstats/*.idxstats
│   └── polishing/                                  # contig classes, clusters
├── consensus/quality_control/checkv/<sample>/<genome>/quality_summary.tsv
├── variants/
│   ├── ivar/<sample>/*.tsv
│   └── mapping-info/metrics/mosdepth/<sample>/     # per-base depth, cumulative coverage
├── multiqc/multiqc_data/multiqc.parquet            # written by multiqc_reprocess
└── pipeline_info/software_versions.yml
```

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 1.2.0 release,
`s3://nf-core-awsmegatests/viralmetagenome/results-74064a43f4b00c163c22bcfc9cf1d84a2a69e988/`:
four paired-end metagenomic libraries of one virus, assembled with MEGAHIT,
clustered with CD-HIT-EST, refined for one iteration and called with iVar, then
mapped against a constraint sheet of three references. The metadata table is not
part of the published run: it is vendored with the template under `input/`, with
a `specimen` column as the group. CheckV ran on its minimal test database, so
every consensus reads `Not-determined`. `megatest.yaml` lists the subset the
template needs (about 20 MB):

```bash
DEST=/tmp/viralmetagenome_test
bash depictio/projects/nf-core/viralmetagenome/1.2.0/download_test_data.sh "$DEST"
python -m depictio.dev_scripts.multiqc_reprocess --src "$DEST" --dest "$DEST" --exclude '*_mqc.tsv'
depictio ingest "$DEST" --template nf-core/viralmetagenome/latest \
  --var METADATA_FILE="$DEST/input/metadata.tsv" --var GROUP_COL=specimen
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/viralmetagenome](https://nf-co.re/viralmetagenome): official pipeline documentation
- [nf-co.re/viralmetagenome/1.2.0/results](https://nf-co.re/viralmetagenome/1.2.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/viralmetagenome releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
