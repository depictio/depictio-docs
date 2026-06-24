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
    <p class="template-subtitle">Amplicon sequencing analysis workflow using DADA2 and QIIME2 — 16S, ITS, CO1, 18S and other amplicons across Illumina, PacBio, IonTorrent.</p>
    <p class="template-links">
      <a href="https://nf-co.re/ampliseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/ampliseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-reviewed template-banner-badge" data-tooltip="Reviewed — tested, CI passes, and reviewed by the Depictio team or community."><i class="mdi mdi-check-circle-outline"></i> Reviewed</span>
</div>

The ampliseq template covers the main outputs of a standard nf-core/ampliseq run:

- :material-chart-bar: **MultiQC quality control** — FastQC read quality, Cutadapt trimming statistics
- :material-bacteria: **Taxonomy composition** — phylum-level barplots, sunburst, heatmap with annotations
- :material-chart-line: **Alpha diversity** — Faith's Phylogenetic Diversity, rarefaction curves (requires metadata)
- :material-chart-scatter-plot: **Differential abundance** — ANCOM-BC volcano plots, log-fold change (requires metadata + `--ancombc`)
- :material-map-marker: **Sampling locations** — geographic scatter map from metadata coordinates (requires metadata)

---

## Quick start

=== "Base (no metadata)"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.16.0 \
      --data-root /path/to/ampliseq_results \
      --var SAMPLESHEET_FILE=samplesheet.csv
    ```

    MultiQC + taxonomy dashboards. No diversity or differential abundance.

=== "Extended (with metadata)"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.16.0 \
      --data-root /path/to/ampliseq_results \
      --var SAMPLESHEET_FILE=samplesheet.csv \
      --var METADATA_FILE=Metadata.tsv \
      --var GROUP_COL=habitat
    ```

    Full dashboard: diversity, facetted charts, map, heatmap annotations, ANCOM-BC.

---

## Reference

Running without `METADATA_FILE` prunes the metadata-dependent collections
(see the *Conditional routes* table); the `--skip_qiime` / `--skip_taxonomy`
/ multi-region routes are auto-detected from the run's `params.json`.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound to
    pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are re-packed so
    there are no empty rows. One template therefore covers 16S/ITS, single- vs.
    multi-region (SIDLE), and `skip_qiime` runs without edits.

--8<-- "pipeline-templates/nf-core/_generated/ampliseq-2.16.0.md"

---

## Dashboard tabs

The ampliseq dashboard ships as a six-tab funnel (MultiQC parent + five
child tabs). Filters propagate across tabs via cross-DC links on the
metadata `sample` column — see [Cross-DC links](#cross-dc-links) in the
Reference section.

=== "MultiQC"

    Quality control overview powered by MultiQC.

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png)](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Habitat Type, Sampling Period (DatePicker).

    **Components:**

    - General stats table
    - Cutadapt: filtered reads, trimmed sequence lengths
    - FastQC: sequence counts, quality histograms, GC content, adapter
      content, status checks, Per-sequence quality / GC / N content,
      sequence duplication levels, length distribution

=== "Alpha Diversity"

    Within-sample diversity metrics, rarefaction, and per-habitat
    comparisons. Extended mode only.

    [![Alpha Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png)](../../images/pipeline-templates/nf-core/ampliseq/alpha_diversity_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Habitat.

    **Components:**

    - 4 metric cards: *Total Samples*, *Shannon (distribution)*,
      *Faith PD (distribution)*, *Evenness (distribution)*
    - Rarefaction curves (multi-metric) — advanced viz, filterable by
      habitat / sample via the in-tab DCLink
    - Alpha diversity by habitat (per metric) — facetted boxplot
    - Per-sample alpha diversity data table

=== "Community & Diversity"

    Taxonomy composition + sampling-location map (extended mode).

    [![Community & Diversity dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_light.png)](../../images/pipeline-templates/nf-core/ampliseq/community_light.png){target="_blank" rel="noopener"}

    **Components (base):**

    - Metric cards: total samples, total taxa, kingdoms, unique phyla
    - Sunburst: Kingdom → Phylum hierarchy
    - Mean relative abundance by Phylum (± std)
    - Stacked bar: taxonomic composition per sample
    - ComplexHeatmap: z-score normalized, clustered, with Kingdom row
      annotations
    - Data table: taxonomy relative abundance
    - Filters: Kingdom, Phylum, relative abundance range

    **Additional components (extended):**

    - Facetted bar charts by GROUP_COL
    - Sampling locations scatter map
    - Heatmap with habitat + city column annotations
    - Filters: sampling period (DatePicker), GROUP_COL, sample ID

=== "Differential Abundance"

    ANCOM-BC differential abundance results. Extended mode only.

    [![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_light.png)](../../images/pipeline-templates/nf-core/ampliseq/differential_light.png){target="_blank" rel="noopener"}

    **Components:**

    - Metric cards: total taxa, significant taxa (q<0.05), unique phyla,
      max log-fold change
    - Volcano plot: LFC vs -log10(q-value), facetted by contrast
    - DA barplot: per-contrast log-fold change
    - Top differential taxa bar chart
    - Results data table
    - Filters: contrast, Phylum, Kingdom, W statistic range, LFC range

=== "Ordination & Clustering"

    Beta-diversity / PCoA embedding + ComplexHeatmap on the canonical
    feature matrix. Surfaces clusters and outliers across samples.

    [![Ordination & Clustering dashboard](../../images/pipeline-templates/nf-core/ampliseq/ordination_light.png)](../../images/pipeline-templates/nf-core/ampliseq/ordination_light.png){target="_blank" rel="noopener"}

    **Components:**

    - Embedding (PCoA): 2D sample projection, colour-coded by habitat
    - ComplexHeatmap: clustered z-score heatmap on the canonical feature
      matrix
    - Bray-Curtis sample-distance heatmap

=== "Phylogeny"

    Rooted phylogenetic tree of ASVs with tip metadata overlay.

    [![Phylogeny dashboard](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png)](../../images/pipeline-templates/nf-core/ampliseq/phylogeny_light.png){target="_blank" rel="noopener"}

    **Components:**

    - Phylogenetic tree viewer (Newick) with metadata-annotated tips

---

## Running the pipeline

Depictio reads the **output** of nf-core/ampliseq — it does not run the pipeline. Run the pipeline first:

```bash
nextflow run nf-core/ampliseq \
  --input samplesheet.csv \
  --FW_primer GTGYCAGCMGCCGCGGTAA \
  --RV_primer GGACTACNVGGGTWTCTAAT \
  --metadata Metadata.tsv \
  -profile docker
```

Then point Depictio at the results:

```bash
depictio run --template nf-core/ampliseq/2.16.0 \
  --data-root results/ \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --var METADATA_FILE=Metadata.tsv
```

See [nf-co.re/ampliseq/usage](https://nf-co.re/ampliseq/2.16.0/docs/usage) for full pipeline documentation.

---

## Required data structure

Point `--data-root` to the directory containing your ampliseq outputs. This can be a single run's `results/` folder or a parent directory containing multiple runs — Depictio scans recursively. Not all files are required; the template adapts based on what's present and which `--var` flags you provide.

```text
<DATA_ROOT>/
├── samplesheet.csv                                # --var SAMPLESHEET_FILE
├── Metadata.tsv                                   # --var METADATA_FILE (optional)
└── <run_id>/                                      # One or more pipeline run output folders
    ├── multiqc/
    │   └── multiqc_data/
    │       └── multiqc.parquet
    └── qiime2/
        ├── alpha-rarefaction/                      # ⚠ Requires --metadata
        │   └── faith_pd.csv
        ├── ancombc/differentials/                  # ⚠ Requires --metadata + --ancombc
        │   └── Category-<GROUP_COL>-level-2/
        │       ├── lfc_slice.csv
        │       ├── p_val_slice.csv
        │       ├── q_val_slice.csv
        │       ├── se_slice.csv
        │       └── w_slice.csv
        ├── barplot/
        │   └── level-2.csv
        ├── diversity/alpha_diversity/              # ⚠ Requires --metadata
        │   └── faith_pd_vector/
        │       └── metadata.tsv
        └── rel_abundance_tables/
            └── rel-table-2.tsv
```

---

## Additional resources

- [nf-co.re/ampliseq](https://nf-co.re/ampliseq) — official pipeline documentation
- [nf-co.re/ampliseq/2.16.0/results](https://nf-co.re/ampliseq/2.16.0/results) — AWS test results
- [Template System Reference](../../usage/projects/templates.md) — YAML format, variables, conditionals
- [Recipes](../../usage/projects/recipes.md) — how to read, test, and write recipes
