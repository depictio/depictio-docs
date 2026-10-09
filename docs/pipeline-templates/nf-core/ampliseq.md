---
title: Amplicon Sequencing
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/ampliseq" target="_blank" title="nf-core/ampliseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_dark.png" alt="nf-core/ampliseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Amplicon Sequencing</h1>
    <p class="template-subtitle">Amplicon sequencing analysis workflow using DADA2 and QIIME2: 16S, ITS, CO1, 18S and other amplicons across Illumina, PacBio, IonTorrent.</p>
    <p class="template-links">
      <a href="https://nf-co.re/ampliseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/ampliseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-reviewed template-banner-badge" data-tooltip="Reviewed: tested, CI passes, and reviewed by the Depictio team or community."><i class="mdi mdi-check-circle-outline"></i> Reviewed</span>
</div>

<div class="tpl-version-pick" data-latest="2.18.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.18.0" selected>2.18.0</option>
    <option value="2.16.0">2.16.0</option>
    <option value="2.14.0">2.14.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The ampliseq template follows a standard nf-core/ampliseq run from reads to
differential taxa, one tab per step:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-bar: **MultiQC quality control**: FastQC read quality and Cutadapt trimming
- :material-chart-bell-curve: **Diversity**: alpha diversity with rarefaction curves, and the PCoA on Bray-Curtis distances (requires metadata)
- :material-bacteria: **Taxa**: composition per group and per sample, the sunburst, the taxa groups share, and the phylogenetic tree
- :material-chart-scatter-plot: **Differential abundance**: ANCOM-BC volcano with MA and QQ views, per contrast (requires metadata + `--ancombc`)

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/ampliseq_results \
      --template nf-core/ampliseq/latest
    ```

    The results directory is the only thing you have to pass. The samplesheet is picked up
    from `input/`, and `pipeline_info/params.json` fills in the metadata file the
    run was given (`--metadata`) and the route flags: multi-region, `--skip_qiime`,
    `--skip_taxonomy`, `--skip_alpha_rarefaction`, `--skip_ancom`, and the depth of
    the Phylum rank in the taxonomy database.

=== "Choose the grouping column"

    ```bash
    depictio ingest /path/to/ampliseq_results \
      --template nf-core/ampliseq/latest \
      --var METADATA_FILE=/path/to/Metadata.tsv \
      --var GROUP_COL=habitat
    ```

    `GROUP_COL` is the metadata column every grouped tile, the group filter and
    the ANCOM-BC contrast read. It defaults to the first annotation column of the
    metadata file, so pass it when the factor you care about is another one.
    `METADATA_ID_COL` names the sample-ID column (the first column by default),
    and `SAMPLESHEET_FILE` or `TREE_FILE` override the auto-detected samplesheet
    and Newick tree.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/ampliseq -r 2.18.0 -profile docker --outdir results
    ```

    No ingestion command and no template named: the pipeline ingests its own
    output directory when it finishes and picks this template from its own name
    and version. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

Running without `METADATA_FILE` prunes the metadata-dependent collections
(see the *Conditional routes* table); the multi-region, `--skip_qiime`,
`--skip_taxonomy`, `--skip_alpha_rarefaction` and `--skip_ancom` routes are
auto-detected from the run's `params.json`.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound to
    pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are re-packed so
    there are no empty rows. One template therefore covers 16S/ITS, single- vs.
    multi-region (SIDLE), and `skip_qiime` runs without edits.

<div class="tpl-version-block" data-version="2.18.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/ampliseq-latest.md"

</div>

<div class="tpl-version-block" data-version="2.16.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/ampliseq-2.16.0.md"

</div>

<div class="tpl-version-block" data-version="2.14.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/ampliseq-2.14.0.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then seven child tabs in three groups, read as a
funnel from the run to the taxa that differ between groups. Each tab below carries
the **same icon and colour the dashboard gives it**, so the page and the app read
alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC |
| Diversity | Alpha Diversity, Ordination & Clustering |
| Taxa | Community & Diversity, Differential Abundance, Phylogeny, SIDLE |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and details follow, collapsed. The persistent *Sample
filters* (your grouping column, then the sample id) sit in the left panel and narrow
every tab through cross-DC links on the metadata `sample` column, see
[Cross-DC links](#cross-dc-links). The *Sample sheet* is pinned, collapsed, to the
bottom of every child tab.

Where a tab names *your grouping column*, that is whichever metadata column the
run was resolved against; the dashboard substitutes its real name everywhere.

=== ":material-compass-outline: Overview"

    *Amplicon communities, from reads to the taxa that differ between groups.*

    <!-- screenshot pending v2 -->

    A short hero links the run parameters. *About this dashboard* says how to move
    through the tabs, *The run* lists the samples, primers, reference taxonomy and
    removed taxa, and *Pipeline* walks the six steps from trimming to the
    differential test, each linked to its parameters and its tab. The findings are
    live values: they follow the filters, and a route that lacks their data drops
    them.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (your grouping column and the sample id), and so does
        *Findings* (your grouping column and the kingdom): each narrows its own
        section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples, phyla, median Shannon diversity, reads kept |
        | Findings | Live result rows, then 4 figures: phylum composition per group, the ANCOM-BC volcano, the PCoA and a tree of the eight largest phyla |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did sequencing and primer trimming work for every sample?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only: general statistics, Cutadapt filtered reads, FastQC
    sequence counts and quality histograms open, the other FastQC and Cutadapt
    panels collapsed. Its sample filter reads the MultiQC report, so the tab works
    on a run without metadata.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | QC overview | 4 MultiQC panels |
        | QC details (collapsed) | 9 MultiQC panels |

=== ":material-chart-bell-curve:{ .mc-grape } Alpha Diversity"

    **Diversity** · *How diverse is each sample, and was it sequenced deeply enough?*

    [![Alpha Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Alpha Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The median **Shannon** diversity and **Faith PD** with their spread,
    **Observed ASVs** with their distribution and **Evenness** on a 0 to 1 gauge.
    Then the rarefaction curves, one per group with a metric switch, and Shannon
    diversity per group with one point per sample.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a Shannon diversity range on
        `alpha_diversity_multi_canonical`, plus the sample filters.

        | Section | What it holds |
        |---|---|
        | Diversity at a glance | 4 cards |
        | Rarefaction | 1 advanced visualization |
        | Group comparison | *Shannon diversity per group* |
        | Per-sample table (collapsed) | *Alpha diversity per sample* |

=== ":material-chart-scatter-plot-hexbin:{ .mc-pink } Ordination & Clustering"

    **Diversity** · *Which samples have similar communities?*

    [![Ordination & Clustering dashboard](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Ordination & Clustering dashboard](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The samples placed by the PCoA, split by group, and, when the run tested a
    PERMANOVA formula, the share of variation the group explains. Then the PCoA on
    Bray-Curtis beside the distances it was drawn from, and the phyla against the
    samples with both axes clustered. A lasso on the PCoA makes an analysis group.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Phylum` on `complex_heatmap_canonical`, narrowing the rows
        of the heatmap, plus the sample filters.

        | Section | What it holds |
        |---|---|
        | Ordination at a glance | 2 cards |
        | Sample relationships | 2 advanced visualizations |
        | Clustered abundance | 1 advanced visualization |

=== ":material-bacteria-outline:{ .mc-teal } Community & Diversity"

    **Taxa** · *Which taxa make up the samples, and which do groups share?*

    [![Community & Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Community & Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Distinct phyla, classes, orders and families, each split or ranked. Then the
    phylum composition per group and per sample (the eight largest phyla and
    Other), the sunburst hierarchy and the UpSet of the taxa the groups share. A
    `--skip_qiime` run shows its SINTAX tiles in the same places.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Kingdom` and `Phylum` on `taxonomy_rel_abundance`, or on
        `sintax_rel_abundance` for a SINTAX run, plus the sample filters.

        | Section | What it holds |
        |---|---|
        | Community at a glance | 4 cards |
        | Composition | 1 bar + 1 advanced visualization |
        | Taxonomic structure | 1 advanced visualization |
        | Set overlap | 1 advanced visualization |
        | Tables (collapsed) | *Relative abundance per sample and phylum* |

=== ":material-chart-scatter-plot:{ .mc-red } Differential Abundance"

    **Taxa** · *Which taxa differ in abundance between groups?*

    [![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Pick a contrast first. The taxa tested, those significant at 5% FDR, and the
    enriched and depleted calls, each split by contrast. Then the volcano, whose
    View switch reads the same calls as an MA or a QQ plot, and the largest effects
    per contrast. The collapsed *Taxon detail* holds the ANCOM-BC table, with a
    record card for the row you pick.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Contrast`, `Phylum`, `Kingdom` and a log-fold-change
        range, all on `ancombc_results`.

        | Section | What it holds |
        |---|---|
        | Calls at a glance | 4 cards |
        | Volcano and ranked effects | 2 advanced visualizations |
        | Taxon detail (collapsed) | *ANCOM-BC results* + a taxon record card |

=== ":material-family-tree:{ .mc-lime } Phylogeny"

    **Taxa** · *How are the ASVs related, and how deeply are they classified?*

    [![Phylogeny dashboard](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Phylogeny dashboard](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The ASVs, the share classified to genus, the median classifier confidence and
    the distinct genera. The tree opens on its summary, the eight largest phyla
    with their share of the reads per group; its View switch draws every ASV,
    coloured by any rank.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Kingdom` and `Phylum` on
        `phylogenetic_tree_metadata_canonical`, pruning the tree to one clade.

        | Section | What it holds |
        |---|---|
        | Tree at a glance | 4 cards |
        | Tree | 1 advanced visualization |
        | Tip taxonomy (collapsed) | *ASV taxonomy* |

=== ":material-graph-outline:{ .mc-indigo } SIDLE"

    **Taxa** · *What does the community rebuilt across amplicon regions contain?*

    !!! info "Multi-region runs only"
        This tab is bound to `sidle_reconstructed`, which a single-region run never
        writes. On such a run the self-adapting layout drops the tab entirely.

    The reconstructed features, the samples that carry them, the phyla they
    resolve to and the mean number of regions per feature. Then the composition
    per sample, by phylum and by genus, and the reconstruction QC: regions and
    k-mer support per feature.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Phylum` on `sidle_reconstructed`.

        | Section | What it holds |
        |---|---|
        | Reconstruction at a glance | 4 cards |
        | Composition | 2 bars |
        | Reconstruction QC | 1 bar + 1 scatter |
        | Tables (collapsed) | *Reconstructed features per sample*, *Reconstruction support per feature* |

!!! tip "The reference project adds two tabs"
    The Ammer catchment reference dashboard, seeded with the bundled demo data,
    adds two tabs to *Data & QC*: :material-map-marker-outline:{ .mc-blue }
    **Sampling Campaign** (where and when the catchment was sampled) and
    :material-waves:{ .mc-cyan } **Environment (CTD)** (sonde readings per sample,
    and the diversity they go with). Both are bound to metadata columns that only
    that dataset ships.

Tables select rows and the SIDLE k-mer scatter selects points: the pinned
sample sheet on the metadata id column, the alpha-diversity table on
`sample_id`, the two relative-abundance tables on `taxonomy`, the ANCOM-BC table
on `id` (which also drives the *Taxon record*), the tip taxonomy table on
`taxon`, and both SIDLE tables and the scatter on `feature_id`. A pick narrows the
other tiles of the same collection and, through the project links, the
collections downstream of it. The bar and box figures do not select, and the
ordination embedding narrows nothing, since its collection has no outgoing link.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/ampliseq, it does not run the pipeline. Run the pipeline first:

```bash
nextflow run nf-core/ampliseq -r 2.18.0 \
  --input samplesheet.tsv \
  --FW_primer GTGYCAGCMGCCGCGGTAA \
  --RV_primer GGACTACNVGGGTWTCTAAT \
  --metadata Metadata.tsv \
  -profile docker --outdir results
```

Then point Depictio at the results:

```bash
depictio ingest results/ \
  --template nf-core/ampliseq/latest \
  --var GROUP_COL=habitat
```

See [nf-co.re/ampliseq/usage](https://nf-co.re/ampliseq/2.18.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the output directory of one run. Not every file is
required: the template adapts to what is present and to the route flags read
from `params.json`.

```text
<DATA_ROOT>/
├── input/
│   ├── Samplesheet.tsv                            # auto-detected (or --var SAMPLESHEET_FILE)
│   └── Metadata.tsv                               # read from params.json (or --var METADATA_FILE)
├── pipeline_info/
│   ├── params_<timestamp>.json                    # route flags and the metadata path
│   └── software_versions.yml
├── multiqc/multiqc_data/
│   └── multiqc.parquet
├── qiime2/
│   ├── alpha-rarefaction/*.csv                    # requires --metadata
│   ├── diversity/alpha_diversity/
│   │   └── <metric>_vector/metadata.tsv           # shannon, observed_features, faith_pd, evenness
│   ├── barplot/level-<N>.csv                      # N = Phylum depth of the database
│   ├── rel_abundance_tables/rel-table-<N>.tsv     # Phylum down to Genus
│   ├── ancombc/differentials/                     # requires --metadata, skipped by --skip_ancom
│   │   └── Category-<GROUP_COL>-level-<N>/
│   │       └── {lfc,p_val,q_val,se,w}_slice.csv
│   └── phylogenetic_tree/tree.nwk                 # or --var TREE_FILE
├── dada2/ASV_table.tsv                            # --skip_qiime route only
├── sintax/ASV_tax_sintax.*.tsv                    # --skip_qiime route only
└── sidle/                                         # multi-region route only
    ├── reconstructed/reconstructed_merged.tsv
    └── DB/3_reconstructed/reconstruction_summary/metadata.tsv
```

---

## :material-flask-outline: Validation runs

The template is validated against the nf-core AWS megatest of the 2.18.0
release, a 16S run with sample metadata, and the screenshots above come from
the bundled Ammer catchment reference project resolved with
`GROUP_COL=habitat`. `megatest.yaml` lists the tables-only subset of that run
the template needs:

```bash
python scripts/nfcore_megatest.py fetch --pipeline ampliseq --version 2.18.0 --dest /tmp/ampliseq_test
depictio ingest /tmp/ampliseq_test --template nf-core/ampliseq/2.18.0 --var GROUP_COL=habitat
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/ampliseq](https://nf-co.re/ampliseq): official pipeline documentation
- [nf-co.re/ampliseq/2.18.0/results](https://nf-co.re/ampliseq/2.18.0/results): AWS test results
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
    <span class="tpl-credit-note">Ran it on real data and signed off on the status above.</span>
    <a class="tpl-person" href="https://github.com/depictio" target="_blank" rel="noopener">
      <img src="https://github.com/depictio.png?size=80" alt="" loading="lazy"> Depictio team
    </a>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/ampliseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
