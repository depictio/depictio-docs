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

- :material-chart-box-outline: **MultiQC**: FastQC read quality and Cutadapt primer trimming, straight from the report
- :material-chart-bell-curve: **Alpha Diversity**: rarefaction curves, then observed features, Faith PD, evenness and Shannon per group
- :material-bacteria-outline: **Community & Diversity**: what the samples are made of, ranked, stacked per sample, as a sunburst hierarchy, and shared between groups
- :material-chart-scatter-plot-hexbin: **Ordination & Clustering**: a PCoA on Bray-Curtis, the distance matrix behind it and a clustered phylum by sample heatmap
- :material-chart-scatter-plot: **Differential Abundance**: ANCOM-BC volcano and ranked effects per contrast, with a record card for the taxon picked
- :material-family-tree: **Phylogeny**: the QIIME2 tree with each tip coloured by its taxonomy

A seventh tab, **Reconstructed Community (SIDLE)**, only appears on multi-region
runs. `Sample filters`, `Run at a glance` and `Sample sheet` are pinned to the top
of every tab, so the sample and group picks and the four run-size cards follow
you from tab to tab.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/ampliseq/latest \
      --data-root /path/to/ampliseq_results
    ```

    `--data-root` is the only thing you have to pass. The samplesheet is picked up
    from `input/`, and `pipeline_info/params.json` fills in the metadata file the
    run was given (`--metadata`) and the route flags: multi-region, `--skip_qiime`,
    `--skip_taxonomy`, `--skip_alpha_rarefaction`, `--skip_ancom`, and the depth of
    the Phylum rank in the taxonomy database.

=== "Choose the grouping column"

    ```bash
    depictio run \
      --template nf-core/ampliseq/latest \
      --data-root /path/to/ampliseq_results \
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
    depictio-cli config nextflow --install     # once per machine
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

Seven tabs, read as a funnel: are the reads good, how diverse is each sample,
what are the communities made of, how do the samples relate, which taxa differ
between groups, and where those taxa sit on the tree. Each tab below carries the
**same icon and colour the dashboard gives it**, so the page and the app read
alike. The persistent `Sample filters` (sample ID and your grouping column, both
on the metadata collection) reach every tab through the cross-DC links on the
metadata sample column, see [Cross-DC links](#cross-dc-links); the tabs carry no
sample or group filter of their own.

Where a tab names *your grouping column*, that is whichever metadata column the
run was resolved against; the dashboard substitutes its real name everywhere.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Are the reads good, and did the primers come off?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Thirteen MultiQC panels: Cutadapt filtered reads, the FastQC sequence counts
    and quality histograms up front, the other FastQC and Cutadapt panels in a
    collapsed section. There is no per-sequence GC panel, because amplicon reads
    sit in a narrow GC band and it reads as a flat line.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample ID` and your grouping column on `metadata`,
        persistent and pinned to the top of every tab, plus a collapsed *MultiQC
        report* section with a `Sample ID (MultiQC)` list read from the report
        itself, which keeps the tab filterable on a run without `--metadata`.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | QC overview | 4 MultiQC panels |
        | QC details | 9 MultiQC panels |
        | Sample sheet | *Sample sheet*, pinned to every tab |

=== ":material-chart-bell-curve:{ .mc-orange } Alpha Diversity"

    *Did sequencing reach saturation, and how rich is each sample?*

    [![Alpha Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Alpha Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The cards summarise observed features, Faith PD and evenness as a median
    with their spread, next to the deepest rarefaction depth. The rarefaction
    curves come next, with the metric switch in the tile header, then the same
    indices compared between groups.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Shannon index` range on `alpha_diversity_multi_canonical`,
        which carries the surviving samples to the rarefaction curves.

        | Section | What it holds |
        |---|---|
        | Diversity at a glance | 4 cards |
        | Rarefaction | *Rarefaction curves (multi-metric)* |
        | Per-group comparison | *Alpha diversity by group (per metric)* |
        | Per-sample table | *Per-sample alpha diversity (one row per sample)* |

=== ":material-bacteria-outline:{ .mc-teal } Community & Diversity"

    *What are the samples made of, and which taxa do the groups share?*

    [![Community & Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Community & Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/community_diversity_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The 15 most abundant phyla by mean relative abundance per group open the tab,
    followed by the stacked per-sample composition with a rank switch in the
    header. The sunburst reads the same abundances as a hierarchy, and the UpSet
    shows which taxa are shared between groups and which are exclusive. The
    SINTAX tiles only fill on `--skip_qiime` runs.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Kingdom`, `Phylum` and a relative-abundance range on
        `taxonomy_rel_abundance`, plus a collapsed *SINTAX scope* with its own
        `Kingdom` and `Phylum` pair for the SINTAX tiles.

        | Section | What it holds |
        |---|---|
        | Composition | *Mean Relative Abundance by group*, *Stacked taxonomy (advanced)* |
        | Taxonomic structure | *Taxonomic hierarchy (sunburst)* |
        | Set overlap | *Taxa shared across groups (UpSet)* |
        | SINTAX classifier | 1 bar, *Taxonomy Relative Abundance (sintax)* |
        | Tables | *Taxonomy Relative Abundance* |

=== ":material-chart-scatter-plot-hexbin:{ .mc-pink } Ordination & Clustering"

    *Do the samples cluster by group, and which phyla drive it?*

    [![Ordination & Clustering dashboard](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Ordination & Clustering dashboard](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/ordination_clustering_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The PCoA embeds each sample in two dimensions from Bray-Curtis distances, and
    the distance matrix beside it shows the pairs it was computed from, where a
    sample unlike every other shows up as a bright row. Below, the phylum by
    sample heatmap clusters both axes. The PCoA takes a lasso, which keeps the
    picked samples as a selection.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Phylum` on `complex_heatmap_canonical`, which narrows the
        heatmap rows.

        | Section | What it holds |
        |---|---|
        | Sample relationships | *Sample ordination (PCoA, Bray-Curtis)*, *Sample distances (Bray-Curtis)* |
        | Clustered abundance | *Taxonomy heatmap (clustered)* |

=== ":material-chart-scatter-plot:{ .mc-red } Differential Abundance"

    *Which taxa differ between groups, and by how much?*

    [![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/differential_abundance_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Pick a contrast first: every number on the tab is conditional on it. The cards
    count the taxa tested, those significant at a 5% FDR and those enriched, above
    the volcano and the ranked differential-abundance bars. `Taxon detail` holds
    the full ANCOM-BC table with a linked record card beside it, which folds to a
    slim rail until a row is picked and then opens on that taxon's test and
    lineage.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Contrast`, `Phylum` and `Kingdom` in a *Call scope* group,
        plus `W Statistic Range` and `Log-Fold Change Range` in a *Thresholds*
        group, all on `ancombc_results`.

        | Section | What it holds |
        |---|---|
        | Summary | 4 cards |
        | Volcano & ranked effects | *Volcano (advanced viz)*, *Differential-abundance bars (per contrast)* |
        | Taxon detail | *ANCOM-BC differential abundance results*, *Taxon record* |

    !!! note "No MA plot"
        `ancombc_results` carries no mean abundance, and the contrast filter does
        not reach the MA collection, so an MA tile would ignore the contrast every
        other number on the tab depends on.

=== ":material-family-tree:{ .mc-lime } Phylogeny"

    *Where do the taxa sit on the tree, and how confidently are they classified?*

    [![Phylogeny dashboard](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Phylogeny dashboard](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The cards count the ASVs, the share classified down to genus, the mean
    classifier confidence and the unique genera. The tree follows, pruned to the
    clade picked in the filters and coloured by any rank, with the full lineage of
    each tip in a collapsed table.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Kingdom` and `Phylum` on
        `phylogenetic_tree_metadata_canonical`.

        | Section | What it holds |
        |---|---|
        | Tree at a glance | 4 cards |
        | Tree | *ASV phylogenetic tree* |
        | Tip taxonomy | *ASV taxonomy table* |

=== ":material-graph-outline:{ .mc-indigo } Reconstructed Community (SIDLE)"

    *What community did SIDLE rebuild across regions, and on how much evidence?*

    !!! info "Multi-region runs only"
        This tab is bound to `sidle_reconstructed`, which a single-region run never
        writes. On such a run the self-adapting layout drops the tab entirely.

    Cards for the reconstructed features, samples, phyla and the mean number of
    regions per feature, then the per-sample composition by phylum and by the most
    abundant genera. The QC section plots how many regions and k-mers support each
    feature: select points on the k-mer scatter to filter both tables below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Phylum` on `sidle_reconstructed`.

        | Section | What it holds |
        |---|---|
        | Reconstruction at a glance | 4 cards |
        | Composition | *Relative composition by phylum (per sample)*, *Genus-level composition (per sample)* |
        | Reconstruction QC | *Cross-region support (features by regions mapped)*, *K-mer support vs region coverage* |
        | Tables | *Reconstructed features (per-sample counts)*, *Reconstruction confidence (regions mapped, kmer support)* |

!!! tip "Cross-selection"
    Every table selects rows, and a pick becomes a dashboard filter that narrows
    the other tiles of the same collection and, through the project links, the
    collections downstream of it: the pinned sample sheet, the alpha-diversity
    table, both relative-abundance tables, the ANCOM-BC table, the tip taxonomy
    table and both SIDLE tables. The bar and box figures do not select.

!!! tip "The reference dataset adds two more"
    The Ammer catchment reference dashboard, seeded with the bundled demo data,
    carries two further tabs on top of these seven:
    :material-map-marker-outline:{ .mc-blue } **Sampling Campaign** (where and when
    the catchment was sampled) and :material-waves:{ .mc-cyan } **Environment (CTD)**
    (sonde readings per sample, and the diversity they go with). Both are bound to
    metadata columns that only that dataset ships.

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
depictio run --template nf-core/ampliseq/latest \
  --data-root results/ \
  --var GROUP_COL=habitat
```

See [nf-co.re/ampliseq/usage](https://nf-co.re/ampliseq/2.18.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the output directory of one run. Not every file is
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
depictio run --template nf-core/ampliseq/2.18.0 --data-root /tmp/ampliseq_test --var GROUP_COL=habitat
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
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
