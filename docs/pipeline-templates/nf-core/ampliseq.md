# nf-core/ampliseq

<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
  <div style="flex-shrink:0;">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_dark.png" alt="nf-core/ampliseq" style="height:56px;">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq" style="height:56px;">
  </div>
  <div style="flex:1;">
    <strong style="font-size:1.1em;">Amplicon sequencing analysis workflow using DADA2 and QIIME2 — 16S, ITS, CO1, 18S and other amplicons across Illumina, PacBio, IonTorrent.</strong><br>
    <span style="color:#666;font-size:0.9em;">nf-core pipeline · <a href="https://nf-co.re/ampliseq" target="_blank">nf-co.re/ampliseq</a></span>
  </div>
  <span class="template-status-reviewed" style="white-space:nowrap;"><i class="mdi mdi-check-circle-outline" style="vertical-align:-1px;"></i> Reviewed</span>
</div>

The ampliseq template covers the main outputs of a standard nf-core/ampliseq run:

- :material-chart-bar: **MultiQC quality control** — FastQC read quality, Cutadapt trimming statistics
- :material-bacteria: **Taxonomy composition** — stacked bar, sunburst, sankey flow, ComplexHeatmap with metadata annotations
- :material-chart-line: **Alpha diversity** — Shannon, Faith PD, Observed features, Evenness; multi-metric rarefaction curves
- :material-set-center: **Beta diversity / ordination** — PCoA embedding (Bray-Curtis), sample-distance heatmap
- :material-chart-scatter-plot: **Differential abundance** — ANCOM-BC volcano, DA barplot, MA plot (requires metadata + `--ancombc`)
- :material-set-center: **Set analysis** — UpSet of taxon presence/absence per habitat
- :material-family-tree: **Phylogeny** — rooted ASV tree with Kingdom/Phylum/Genus tip annotations
- :material-map-marker: **Sampling locations** — geographic scatter map (requires metadata coordinates)

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

## Template variables

| Variable | Required | Auto | Description |
|----------|:--------:|:----:|-------------|
| `DATA_ROOT` | :material-check: | — | Pipeline output root (set via `--data-root`) |
| `SAMPLESHEET_FILE` | :material-check: | — | Path to ampliseq samplesheet CSV |
| `METADATA_FILE` | — | — | Sample metadata TSV. Enables extended mode. |
| `GROUP_COL` | — | :material-check: | Grouping column for facetting. Auto: first annotation column. |
| `GROUP_COL_DISPLAY` | — | :material-check: | Title-cased GROUP_COL for chart labels |
| `ANNOTATION_COLS` | — | :material-check: | All annotation columns from metadata |

---

## Data collections

**Core data collections** — raw QIIME2 / samplesheet inputs:

| Data Collection | Type | Recipe | Base | Extended |
|-----------------|------|--------|:----:|:--------:|
| `multiqc_data` | MultiQC | — | :material-check: | :material-check: |
| `samplesheet` | Table | — | :material-check: | :material-check: |
| `taxonomy_composition` | Table | `qiime2/taxonomy_composition.py` | :material-check: | :material-check: |
| `taxonomy_rel_abundance` | Table | `nf-core/ampliseq/taxonomy_rel_abundance.py` | :material-check: | :material-check: |
| `taxonomy_heatmap` | Table | `qiime2/taxonomy_heatmap.py` | :material-check: | :material-check: |
| `metadata` | Table (Metadata) | — | :material-close: | :material-check: |
| `alpha_rarefaction` | Table | `qiime2/alpha_rarefaction.py` | :material-close: | :material-check: |
| `ancombc_results` | Table | `qiime2/ancombc.py` | :material-close: | :material-check: |

**Advanced-viz canonical DCs** — reformatted to the role-based schema consumed by advanced viz renderers:

| Data Collection | Drives | Recipe |
|-----------------|--------|--------|
| `stacked_taxonomy_canonical` | Stacked taxonomy | `qiime2/stacked_taxonomy_canonical.py` |
| `sunburst_canonical` | Sunburst | `nf-core/ampliseq/sunburst_canonical.py` |
| `sankey_canonical` | Sankey flow | `nf-core/ampliseq/sankey_canonical.py` |
| `upset_canonical` | UpSet (taxon × habitat) | `nf-core/ampliseq/upset_canonical.py` |
| `rarefaction_canonical` | Multi-metric rarefaction | `qiime2/rarefaction_canonical.py` |
| `alpha_diversity_multi_canonical` | Alpha diversity (4 metrics) | `qiime2/alpha_diversity_multi_canonical.py` |
| `embedding_pcoa` | PCoA embedding | `qiime2/embedding_pcoa.py` |
| `complex_heatmap_canonical` | Hierarchical heatmap | `nf-core/ampliseq/complex_heatmap_canonical.py` |
| `bray_curtis_canonical` | Sample-distance heatmap | `nf-core/ampliseq/bray_curtis_canonical.py` |
| `ma_canonical` | MA plot (ANCOM-BC) | `nf-core/ampliseq/ma_canonical.py` |
| `phylogenetic_tree_canonical` | Phylogenetic tree (Newick) | — (scan: `qiime2/phylogenetic_tree/tree.nwk`) |
| `phylogenetic_tree_metadata_canonical` | Tree tip annotations | `nf-core/ampliseq/tree_metadata_canonical.py` |

!!! info "Base vs Extended"

    === "Base"

        No `METADATA_FILE` provided. The template removes metadata-dependent DCs (alpha diversity, rarefaction, ANCOM-BC) and imports a single dashboard with MultiQC + taxonomy composition.

        **Use when:** Quick QC check, no sample metadata available, or testing the pipeline setup.

    === "Extended"

        `METADATA_FILE` provided. All 9 DCs active. Dashboard includes facetted charts by `GROUP_COL`, sampling location map, heatmap with metadata annotations, and ANCOM-BC differential abundance.

        **Use when:** Full analysis with sample grouping, geographic data, and differential abundance.

---

## Dashboard tabs

The ampliseq dashboard ships as a six-tab funnel (MultiQC parent + five
child tabs). Filters propagate across tabs via cross-DC links on the
metadata `sample` column — see [Cross-DC links](#cross-dc-links-7) below.

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

## Cross-DC links (7)

| Source | Column | Target | Description |
|--------|--------|--------|-------------|
| `samplesheet` | `sampleID` | `multiqc_data` | Filter MultiQC by samples |
| `metadata` | `ID` | `alpha_diversity` | Filter diversity by metadata |
| `metadata` | `ID` | `alpha_rarefaction` | Filter rarefaction by metadata |
| `metadata` | `ID` | `taxonomy_composition` | Filter taxonomy by metadata |
| `metadata` | `ID` | `taxonomy_rel_abundance` | Filter rel abundance by metadata |
| `samplesheet` | `sampleID` | `taxonomy_heatmap` | Filter heatmap (base) |
| `metadata` | `ID` | `taxonomy_heatmap` | Filter heatmap (extended) |

Metadata links are auto-pruned when `METADATA_FILE` is absent.

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

## Recipes

**QIIME2 recipes** (under `qiime2/`):

| Recipe | Input | Key transformation |
|--------|-------|--------------------|
| `alpha_rarefaction.py` | `faith_pd.csv` | Wide → long, regex depth/iter extraction |
| `alpha_diversity_multi_canonical.py` | Multiple `faith_pd_vector/metadata.tsv` files | Join Shannon, Faith PD, Observed features, Evenness per sample |
| `rarefaction_canonical.py` | `faith_pd.csv` | Multi-metric long format with `group` from metadata |
| `taxonomy_composition.py` | `barplot/level-2.csv` | Detect taxonomy cols (`;`), melt to long format |
| `taxonomy_heatmap.py` | rel_abundance DC + metadata DC | Pivot to Phylum × sample matrix, embed metadata annotations |
| `stacked_taxonomy_canonical.py` | `barplot/level-2.csv` | Produce `(sample_id, taxon, rank, abundance)` long format |
| `embedding_pcoa.py` | QIIME2 PCoA artefact | Extract Bray-Curtis PCoA axes into `(sample_id, dim_1, dim_2)` |
| `ancombc.py` | 5 ANCOM-BC CSVs via `source_overrides` | Melt 5 slices, join, compute `-log10(q)` and significance flag |

**nf-core/ampliseq recipes** (under `nf-core/ampliseq/`):

| Recipe | Input | Key transformation |
|--------|-------|--------------------|
| `alpha_diversity.py` | `faith_pd_vector/metadata.tsv` | Filter comment rows, rename `id` → `sample`, pass through metadata cols |
| `taxonomy_rel_abundance.py` | `rel-table-2.tsv` + metadata DC | Wide → long, Kingdom/Phylum split, generic metadata join |
| `sunburst_canonical.py` | taxonomy_rel_abundance DC | Aggregate to `(Kingdom, Phylum, taxon, abundance)` hierarchy |
| `sankey_canonical.py` | taxonomy_rel_abundance DC | Normalize per-sample flows to `(Kingdom → Phylum → taxon, abundance)` |
| `upset_canonical.py` | taxonomy_rel_abundance DC | Pivot to binary `taxon × habitat` presence matrix |
| `complex_heatmap_canonical.py` | taxonomy_rel_abundance DC + metadata DC | Phylum × sample matrix, embed Kingdom row annotations |
| `bray_curtis_canonical.py` | taxonomy_rel_abundance DC | Compute symmetric Bray-Curtis distance matrix |
| `ma_canonical.py` | ancombc_results DC | Compute `avg_log_intensity` (mean log10 count) vs ANCOM-BC LFC |
| `tree_metadata_canonical.py` | QIIME2 taxonomy TSV | Map ASV → Kingdom/Phylum/…/Genus for tip annotation overlay |

---

## Additional resources

- [nf-co.re/ampliseq](https://nf-co.re/ampliseq) — official pipeline documentation
- [nf-co.re/ampliseq/2.16.0/results](https://nf-co.re/ampliseq/2.16.0/results) — AWS test results
- [Template System Reference](../../usage/projects/templates.md) — YAML format, variables, conditionals
- [Recipes](../../usage/projects/recipes.md) — how to read, test, and write recipes
