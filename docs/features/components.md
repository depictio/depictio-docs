---
title: "Dashboard Components"
icon: material/view-dashboard
description: "Complete guide to Depictio's dashboard component types and their configuration."
---

# :material-puzzle: Dashboard Components

Depictio provides a variety of component types for building interactive dashboards. This guide covers each component type, when to use it, and how to configure it.

## :material-format-list-bulleted: Component Overview

<div class="grid cards" markdown>

-   :material-chart-scatter-plot:{ .lg .middle } **[Figure](#figure-components)**

    ---

    Charts and plots (scatter, bar, histogram, line, box, pie, and more)

-   :material-table:{ .lg .middle } **[Table](#table-components)**

    ---

    Interactive data tables with filtering and sorting

-   :material-card-text:{ .lg .middle } **[Card](#card-components)**

    ---

    Metric display with aggregations

-   :material-format-header-1:{ .lg .middle } **[Text](#text-components)**

    ---

    Section headers (H1, H2, H3)

-   :material-tune:{ .lg .middle } **[Interactive](#interactive-components)**

    ---

    User input components for filtering (slider, dropdown, date picker)

-   :material-microscope:{ .lg .middle } **[MultiQC](#multiqc-components)**

    ---

    Quality control report visualizations

-   :material-image-multiple:{ .lg .middle } **[Image](#image-components)**

    ---

    Image galleries with S3/MinIO storage integration

-   :material-map-marker-multiple:{ .lg .middle } **[Map](#map-components)**

    ---

    Geospatial map visualization with markers

-   :material-chart-multiline:{ .lg .middle } **[Advanced Visualizations](#advanced-visualizations)**

    ---

    Domain-specific scientific viz (volcano, MA, manhattan, ComplexHeatmap, UpSet, sankey, …) backed by canonical column schemas

</div>

---

## :material-chart-scatter-plot: Figure Components <small>(v0.0.1+)</small> { #figure-components }

Figure components display data visualizations using Plotly charts. They support both **UI Mode** (drag-and-drop configuration) and **Code Mode** (Python code for custom plots).

### Supported Chart Types

**UI Mode** provides a curated selection of chart types through the visual interface:

<!-- TODO: update when more UI types are re-enabled -->

| Category | Chart Types |
|----------|-------------|
| :material-chart-scatter-plot: **Basic Charts** | Scatter, Bar, Line |
| :material-chart-box: **Statistical** | Histogram, Box |
| :material-grid-large: **Matrix** | ComplexHeatmap (via [:material-open-in-new: plotly-complexheatmap](https://github.com/weber8thomas/plotly-complexheatmap){ target="_blank" }) |
<!-- | :material-chart-bell-curve: **Distribution** | Density Heatmap, Density Contour |
| :material-chart-tree: **Hierarchical** | Treemap, Sunburst | -->

<!-- | Category | Chart Types |
|----------|-------------|
| :material-chart-scatter-plot: **Basic Charts** | Scatter, Bar, Line, Area, Pie, Donut |
| :material-chart-box: **Statistical** | Histogram, Box, Violin, Strip |
| :material-chart-bell-curve: **Distribution** | Density Heatmap, Density Contour |
| :material-chart-tree: **Hierarchical** | Treemap, Sunburst | -->

!!! tip "Unlimited Charts with Code Mode :material-code-tags:"
    **Code Mode** supports the entire Plotly library, giving you access to all chart types including 3D plots, maps, financial charts, and more. See the [:material-open-in-new: Plotly Python documentation](https://plotly.com/python/){ target="_blank" } for the complete reference.

### UI Mode

In UI Mode, configure charts through the visual interface:

1. Select a **Data Collection** as your data source
2. Choose the **Chart Type** (scatter, bar, histogram, etc.)
3. Map data columns to **X-axis**, **Y-axis**, and optional **Color** dimension
4. Customize appearance (title, axis labels, colors)

### Code Mode

Code Mode allows custom Python code for advanced visualizations:

```python
import plotly.express as px

# df is your data collection as a pandas DataFrame
fig = px.scatter(
    df,
    x="coverage",
    y="quality_score",
    color="sample_type",
    title="Coverage vs Quality by Sample Type"
)

# Return the figure object
fig
```

!!! warning "Security Note :material-shield-lock:"
    Code Mode uses [RestrictedPython](https://restrictedpython.readthedocs.io/en/latest/) for security. Only approved libraries (pandas, plotly) are available. See [Security](security.md) for details.

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Title | Chart title displayed at top | Auto-generated |
| X-axis label | Label for horizontal axis | Column name |
| Y-axis label | Label for vertical axis | Column name |
| Color | Column for color encoding | None |
| Hover data | Additional columns shown on hover | None |

!!! tip "Clustered heatmaps moved"
    The ComplexHeatmap viz has been renamed and is now part of the Advanced Visualizations section below — see [Hierarchical Heatmap](#hierarchical-heatmap) for the full config, alongside the rest of the domain-specific viz family (volcano, MA, sankey, …).

### Selection Filtering (Scatter Plots)

Scatter plots can act as interactive filters. Enable selection to let users lasso, box-select, or click points to filter other components.

| Option | Description |
|--------|-------------|
| `selection_enabled` | Enable selection filtering (`true`/`false`) |
| `selection_column` | Column to extract from selected points |

See [Interactive Selection Filtering](interactive-selection-filtering.md) for details.

---

## :material-table: Table Components <small>(v0.0.2+)</small> { #table-components }

Table components display data in interactive tables with built-in filtering and sorting.

### Features

| Feature | Description |
|---------|-------------|
| :material-page-next: **Server-Side Pagination** | Efficiently handles large datasets by loading data in pages |
| :material-arrow-vertical-lock: **Server-Side Scrolling** | Virtual scrolling for smooth navigation through large tables |
| :material-sort: **Column Sorting** | Click headers to sort ascending/descending |
| :material-filter: **Column Filtering** | Filter by column values |
| :material-download: **Export** (v0.6.0+) | Download data as CSV |

### Configuration

| Option | Description | Default |
|--------|-------------|---------|
| Data Collection | Source data for the table | Required |
| Visible Columns | Columns to display | All columns |
| Page Size | Rows per page | 10, 25, 50, or 100 |
| Style | Column width, text alignment | Auto |
| Title | Header text above the table | Auto (from DC tag) |
| Description | Subtitle text below the title | None |
| Title Size | Header level: `h1`, `h2`, `h3`, or `sm` | `sm` |
| Title Align | Text alignment: `left`, `center`, or `right` | `left` |

### Row Selection Filtering

Tables can act as interactive filters. Enable row selection to let users click rows to filter other components.

| Option | Description |
|--------|-------------|
| `row_selection_enabled` | Enable row selection filtering (`true`/`false`) |
| `row_selection_column` | Column to extract from selected rows |

See [Interactive Selection Filtering](interactive-selection-filtering.md) for details.

---

## :material-chart-multiline: Advanced Visualizations <small>(v0.13.0+)</small> { #advanced-visualizations }

Advanced Visualizations are a family of domain-specific scientific charts (catalogued below). Unlike the generic [Figure](#figure-components) component, which accepts any numeric columns, each advanced viz declares a **canonical column-role schema**: a volcano plot knows it needs a `feature_id`, an `effect_size`, and a `significance` column — wired to your DC's actual column names through the viz's config.

Two ingredients work together:

- a **per-viz `Config` class** (e.g. `VolcanoConfig`, `MAConfig`) that captures the role → column mapping plus per-viz display defaults (thresholds, top-N, sort order);
- a **`CANONICAL_SCHEMAS` entry** declaring the required and optional roles plus their accepted polars dtypes, used by the dashboard builder to validate the binding and surface errors before the viz renders.

Source of truth in the codebase:

- `depictio/models/components/advanced_viz/configs.py` — per-viz Pydantic configs
- `depictio/models/components/advanced_viz/schemas.py` — `CANONICAL_SCHEMAS` + `validate_binding()`
- `depictio/models/components/types.py` — `AdvancedVizKind` literal enum

### Catalog

Every advanced viz consumes a **tabular DC** (CSV / TSV / Parquet → polars) with the column roles documented per-viz below. The **Accepted input** column lists upstream tools whose output natively has — or trivially reshapes to — those columns. Web renderers that *look* like a viz (Microreact, iTOL, IGV, JBrowse, Krona, EnhancedVolcano, qqman, …) aren't listed here — they're peers, not data sources; we call them out in the per-viz prose where the framing helps.

| Viz | Description | Accepted input (canonical producer) |
|-----|-------------|-------------------------------------|
| :material-chart-scatter-plot: [Volcano](#volcano) | Effect size vs significance scatter for differential analysis. | **DESeq2** results table (`results()` → TSV) |
| :material-chart-bell-curve-cumulative: [MA](#ma) | Mean intensity vs log fold change for DE / proteomics QC. | **DESeq2** results table: `log2(baseMean+1)` (or `log10`) → `avg_log_intensity`, `log2FoldChange` straight |
| :material-view-grid-plus-outline: [DA barplot](#da-barplot) | Ranked signed-LFC bars for differential abundance — single panel or faceted by contrast. | **ANCOM-BC** `output$res` (feature, contrast, lfc, q-value) |
| :material-chart-bubble: [Enrichment](#enrichment) | Pathway / GO-term enrichment dot plot. | **clusterProfiler** GSEA / ORA result (term, NES, padj, gene-count) |
| :material-chart-histogram: [Manhattan](#manhattan) | Genome-wide signal scatter across chromosomes (GWAS). | **PLINK** `.assoc` (chr, pos, p-value) |
| :material-chart-timeline-variant: [Lollipop](#lollipop) | Variant / mutation track along a gene body. | **maftools / vcf2maf** Mutation Annotation Format table — `Hugo_Symbol`, `Start_Position`, `Variant_Classification` (file format, **not** Minor Allele Frequency) |
| :material-chart-areaspline: [Coverage track](#coverage-track) | Read depth / signal along genomic coordinates. | **mosdepth** per-base / by-region BED (chrom, pos, depth) |
| :material-chart-bar-stacked: [Stacked taxonomy](#stacked-taxonomy) | Per-sample relative-abundance composition by taxonomic rank. | **QIIME2** `taxa-collapse` table (sample × taxon abundance) |
| :material-sun-wireless: [Sunburst](#sunburst) | Hierarchical taxonomy / pathway viewer. | **Kraken2** `.kreport` parsed into rank columns + `fraction_total_reads` (Bracken `.bracken` is flat single-rank, needs lineage expansion first) |
| :material-chart-line: [Rarefaction](#rarefaction) | Alpha-diversity vs sequencing-depth saturation curve. | **QIIME2** `alpha-rarefaction` (sample, depth, alpha-metric) |
| :material-family-tree: [Phylogenetic](#phylogenetic) | Newick tree + tip metadata. Renders Microreact-style. | **IQ-TREE** Newick + a tabular tip-metadata TSV |
| :material-circle-multiple-outline: [Dot plot](#dot-plot) | Single-cell marker-gene expression by cluster. | **scanpy** aggregation (`sc.get.aggregate` or `groupby` on `adata.X`) producing `(cluster, gene, mean_expression, frac_expressing)` — `rank_genes_groups.to_df()` alone is DE stats, not the dot-plot schema |
| :material-atom: [Embedding](#embedding) | 2D / 3D sample projection for cluster inspection (precomputed or live PCA / UMAP / t-SNE / PCoA). | **scanpy** `adata.obsm['X_umap']` (sample, dim1, dim2) |
| :material-grid: [Hierarchical Heatmap](#hierarchical-heatmap) | Clustered matrix with dendrograms + annotation tracks. | **DESeq2** `vst()` matrix (sample × gene wide) |
| :material-chart-line-stacked: [QQ](#qq) | p-value distribution QC for inflation / deflation. | **PLINK** `.assoc` (or any p-value column) |
| :material-set-center: [UpSet](#upset) | Set-intersection visualisation, alternative to Venn. | Any binary membership matrix (sample × set) |
| :material-chart-sankey: [Sankey](#sankey) | Categorical flow across N ordered levels. | Any tidy table with ≥2 ordered categorical columns |
| :material-grid-large: [Oncoplot](#oncoplot) | Sample × gene mutation matrix. | **maftools / vcf2maf** Mutation Annotation Format table — `Tumor_Sample_Barcode`, `Hugo_Symbol`, `Variant_Classification` (file format, **not** Minor Allele Frequency) |

!!! info "Reading the schema tables"
    Each viz subsection lists its **required** column roles (must be bound for the viz to render) and **optional** roles (extra colour / size / label dimensions). Types use polars dtype families — `Float` accepts `Float32` / `Float64`, `Int` accepts `Int8`–`Int64` and unsigned widths, `String` accepts `String` / `Utf8`, `Numeric` is `Int` ∪ `Float`. The dashboard builder validates the binding via `validate_binding()` and surfaces dtype mismatches in-place.

### Volcano

Effect size vs significance scatter — classic differential-expression view with threshold lines, point search, and top-N labels.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `feature_id` | ✓ | String | Feature identifier (gene, peak, …) |
| `effect_size` | ✓ | Float | Effect size (e.g. log2FC, lfc) |
| `significance` | ✓ | Float | p-value or padj/q-value |
| `label` | — | String | Hover label override |
| `category` | — | String | Categorical annotation (pathway, cluster…) for point colour |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `significance_is_neg_log10` | bool | `false` | True if `significance_col` already contains -log10(p); else applied client-side |
| `significance_threshold` | float | `0.05` | Cutoff applied to the `significance` column |
| `effect_threshold` | float | `1.0` | Absolute `effect_size` cutoff |
| `top_n_labels` | int (≥0) | `20` | Max features to auto-label |

**Filtering / row tagging**

Every row is classified client-side as **UP**, **DOWN**, or **NS** based on `significance < threshold` combined with `|effect_size| > threshold`. The backend returns raw rows; classification + colouring happens in `VolcanoRenderer.tsx`.


[![Volcano example](../images/guides/advanced-visualizations/volcano_light.webp#only-light)](../images/guides/advanced-visualizations/volcano_light.webp){target=_blank}

[![Volcano example](../images/guides/advanced-visualizations/volcano_dark.webp#only-dark)](../images/guides/advanced-visualizations/volcano_dark.webp){target=_blank}
### MA

Mean log intensity (x) vs log2 fold change (y) — same hits as volcano, classic DE / proteomics layout. Shares the UP / DOWN / NS tier scheme with [Volcano](#volcano).

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `feature_id` | ✓ | String | Feature identifier |
| `avg_log_intensity` | ✓ | Float | Mean log intensity (A in MA, x-axis). For DESeq2: pre-transform `baseMean` with `log2(baseMean + 1)` (or `log10`) — `baseMean` itself is untransformed normalised counts. |
| `log2_fold_change` | ✓ | Float | Log2 fold change (M in MA, y-axis). DESeq2 `log2FoldChange` maps directly. |
| `significance` | — | Float | p / padj column for tier colouring |
| `label` | — | String | Hover label override |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `significance_threshold` | float (0–1) | `0.05` | Cutoff for `significance` |
| `fold_change_threshold` | float (≥0) | `1.0` | Absolute `log2_fold_change` cutoff |
| `top_n_labels` | int (≥0) | `15` | Max features to auto-label |

**Filtering / row tagging**

Mirror of the [Volcano](#volcano) tier scheme — UP / DOWN / NS classification (sig × FC thresholds), client-side in `MARenderer.tsx`.


[![MA example](../images/guides/advanced-visualizations/ma_light.webp#only-light)](../images/guides/advanced-visualizations/ma_light.webp){target=_blank}

[![MA example](../images/guides/advanced-visualizations/ma_dark.webp#only-dark)](../images/guides/advanced-visualizations/ma_dark.webp){target=_blank}
### DA barplot

Ranked signed-LFC horizontal bars for differential abundance — single panel or faceted across contrasts. Same input shape as the upstream tool (ANCOM-BC, ALDEx2, MaAsLin2): one row per `(feature, contrast)` with `lfc` and optional `significance`.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `feature_id` | ✓ | String | Feature / taxon identifier |
| `contrast` | ✓ | String | Contrast name (faceting + single-panel filter) |
| `lfc` | ✓ | Float | Log-fold-change (signed) |
| `significance` | — | Float | FDR-adjusted p-value; significant bars are highlighted when bound |
| `label` | — | String | Display label for bars |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `contrast_view` | str | `"all"` | `"all"` → faceted small-multiples (one panel per contrast); any specific contrast value → single-panel drill-in |
| `significance_threshold` | float (0–1) | `0.05` | Highlight cutoff for `significance` |
| `top_n` | int (≥1) | `15` | Top features by `\|lfc\|` shown per panel |

**Filtering / row tagging**

When `contrast_view == "all"` the renderer **facets by contrast** (one panel per unique value, top-N per panel). When `contrast_view` matches a specific contrast value, the renderer collapses to a **single panel** showing only that contrast — useful when one comparison is the focus.

!!! info "Legacy `viz_kind: ancombc_differentials`"
    Previously this single-panel layout was a separate viz kind named `ancombc_differentials`. It's now merged into DA barplot — `viz_kind: ancombc_differentials` is still accepted at deserialisation and rewritten to `da_barplot` with `contrast_view` defaulted from the persisted config.


[![DA barplot example](../images/guides/advanced-visualizations/da_barplot_light.webp#only-light)](../images/guides/advanced-visualizations/da_barplot_light.webp){target=_blank}

[![DA barplot example](../images/guides/advanced-visualizations/da_barplot_dark.webp#only-dark)](../images/guides/advanced-visualizations/da_barplot_dark.webp){target=_blank}
### Enrichment

GSEA / GO / KEGG / Reactome pathway-enrichment dot plot: term on y, NES on x, dot size = gene-set size, colour = -log10(padj).

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `term` | ✓ | String | Pathway / GO-term name |
| `nes` | ✓ | Float | Normalised enrichment score (signed, x-axis) |
| `padj` | ✓ | Float | FDR-adjusted p-value |
| `gene_count` | ✓ | Numeric | Gene-set size (dot size) |
| `source` | — | String | Ontology / source label (GO_BP, KEGG, Reactome, Hallmark, …) |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `padj_threshold` | float (0–1) | `0.05` | Filter cutoff |
| `top_n` | int (≥1) | `20` | Max pathways shown |

**Filtering / row tagging**

Renderer **filters by source** (MultiSelect) and ranks by |nes|; only the top-N pathways are shown. Dot colour encodes -log10(padj).


[![Enrichment example](../images/guides/advanced-visualizations/enrichment_light.webp#only-light)](../images/guides/advanced-visualizations/enrichment_light.webp){target=_blank}

[![Enrichment example](../images/guides/advanced-visualizations/enrichment_dark.webp#only-dark)](../images/guides/advanced-visualizations/enrichment_dark.webp){target=_blank}
### Manhattan

Generic chr / pos / score plot — works for true GWAS (variants), peak significance (ATAC/ChIP narrowPeak), or viral variant tracks. `score_kind` keeps the y-axis label honest.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `chr` | ✓ | String | Chromosome label |
| `pos` | ✓ | Int | Genomic position (1-based) |
| `score` | ✓ | Float | Y-axis score (e.g. -log10(padj)) |
| `feature` | — | String | Feature / locus id (gene, SNP, peak) |
| `effect` | — | Float | Signed effect for point colouring |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `score_kind` | str | `-log10(padj)` | Y-axis label override |
| `score_threshold` | float \| null | `null` | Horizontal threshold line; null hides it |

**Filtering / row tagging**

Renderer **facets by chromosome** (one subplot per unique `chr` value). The optional `score_threshold` draws a horizontal cutoff line — no explicit per-row tag, but the line gives a visual significance reference.


[![Manhattan example](../images/guides/advanced-visualizations/manhattan_light.webp#only-light)](../images/guides/advanced-visualizations/manhattan_light.webp){target=_blank}

[![Manhattan example](../images/guides/advanced-visualizations/manhattan_dark.webp#only-dark)](../images/guides/advanced-visualizations/manhattan_dark.webp){target=_blank}
### Lollipop

Needle / variant track along a gene — each gene body as a horizontal line, each variant as a vertical stem with a category-coloured marker on top.

**Columns** — straight rename from canonical Mutation Annotation Format (VEP / vcf2maf / maftools — the cancer-mutation file format, not Minor Allele Frequency):

| Role | Required | Type | Description | Mutation Annotation Format column |
|------|:--------:|------|-------------|------------|
| `feature_id` | ✓ | String | Gene / feature the variant is on | `Hugo_Symbol` |
| `position` | ✓ | Int | Position along the feature | `Start_Position` (or `Protein_position` for AA-space tracks) |
| `category` | ✓ | String | Variant consequence category (colour) | `Variant_Classification` |
| `effect` | — | Float | Numeric effect (marker size) | e.g. `VAF`, `t_alt_count / t_depth` |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_subplot_genes` | int (≥1) | `6` | If the gene universe exceeds this, switch to a single-gene picker |

**Filtering / row tagging**

Renderer **facets by feature** (one subplot per gene, or a picker once the universe exceeds `max_subplot_genes`). Markers are **coloured by category** and **sized by effect** when bound.


[![Lollipop example](../images/guides/advanced-visualizations/lollipop_light.webp#only-light)](../images/guides/advanced-visualizations/lollipop_light.webp){target=_blank}

[![Lollipop example](../images/guides/advanced-visualizations/lollipop_dark.webp#only-dark)](../images/guides/advanced-visualizations/lollipop_dark.webp){target=_blank}
### Coverage track

Read depth / signal along a coordinate axis. Universal genomics primitive — covers mosdepth bins, BigWig-derived transcript coverage, peak signal, methylseq depth, contig coverage, sarek QC.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `chromosome` | ✓ | String | Chromosome / contig label |
| `position` | ✓ | Int | Bin centre or single-base position |
| `value` | ✓ | Numeric | Coverage / signal value |
| `end` | — | Int | Bin end — when set with `position`, treated as interval |
| `sample` | — | String | Per-sample faceting (stacked subplots) |
| `category` | — | String | Categorical annotation (gene region, peak class, …) |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `y_scale` | `linear` \| `log` | `linear` | Y-axis scale |
| `smoothing_window` | int (0–200) | `0` | Rolling-mean window in bins (0 disables) |
| `color_by` | `single` \| `category` \| `sample` | `single` | Trace colour assignment mode |
| `show_annotation_lane` | bool | `true` | Render annotation strip when `category` is bound |
| `chromosomes_filter` | list[str] \| null | `null` | Whitelist of chromosomes; null = all |
| `samples_filter` | list[str] \| null | `null` | Whitelist of samples; null = all |

**Filtering / row tagging**

Renderer **facets by chromosome** (subplot per chr) and optionally by **sample** (stacked subplot rows). The `chromosomes_filter` / `samples_filter` whitelists narrow the view further; the category lane colour-segments the trace.


[![Coverage track example](../images/guides/advanced-visualizations/coverage_track_light.webp#only-light)](../images/guides/advanced-visualizations/coverage_track_light.webp){target=_blank}

[![Coverage track example](../images/guides/advanced-visualizations/coverage_track_dark.webp#only-dark)](../images/guides/advanced-visualizations/coverage_track_dark.webp){target=_blank}
### Stacked taxonomy

Per-sample stacked relative-abundance bar with a rank dropdown.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `sample_id` | ✓ | String | Sample identifier |
| `taxon` | ✓ | String | Taxon name |
| `rank` | ✓ | String | Taxonomic rank label |
| `abundance` | ✓ | Numeric | Relative or absolute abundance |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default_rank` | str \| null | `null` | If `rank` carries multiple ranks, default-filter to this one |
| `top_n` | int (≥1) | `20` | Show top-N taxa, lump rest into `Other` |
| `sort_by` | `abundance` \| `alphabetical` | `abundance` | Stack-ordering rule |
| `normalise_to_one` | bool | `true` | Force each sample's bars to sum to 1 (true % composition) |

**Filtering / row tagging**

Renderer **filters by rank** (dropdown sourced from the unique `rank` values). Within the active rank, taxa are sorted by `sort_by`; everything past `top_n` is collapsed into an `Other` slice.


[![Stacked taxonomy example](../images/guides/advanced-visualizations/stacked_taxonomy_light.webp#only-light)](../images/guides/advanced-visualizations/stacked_taxonomy_light.webp){target=_blank}

[![Stacked taxonomy example](../images/guides/advanced-visualizations/stacked_taxonomy_dark.webp#only-dark)](../images/guides/advanced-visualizations/stacked_taxonomy_dark.webp){target=_blank}
### Sunburst

Hierarchical taxonomy / pathway viewer — concentric rings from root to leaf. Unlike most viz, Sunburst uses a multi-column `rank_cols` list rather than the standard single-column `<role>_col` pattern; the `abundance` role is bound via the `abundance_col` setting below.

!!! note "Bracken vs Kraken2 — what to ingest"
    A raw `.bracken` file is **flat for a single target rank** (columns: `name`, `taxonomy_id`, `taxonomy_lvl`, `fraction_total_reads`, …) and does **not** carry explicit Kingdom→Genus rank columns. To bind it to Sunburst, either (a) ingest the Kraken2 `.kreport` instead and pivot the indented lineage into rank columns, or (b) map each Bracken `taxonomy_id` back to the NCBI taxonomy tree (e.g. `taxonkit lineage`, `ete3`) and expand to rank columns before upload. The DC must end up with one column per rank used in `rank_cols` plus one numeric `abundance_col`.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `abundance` | ✓ | Numeric | Leaf abundance weight (bound via `abundance_col`). For Bracken: `fraction_total_reads` or `new_est_reads`. |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `rank_cols` | list[str] (≥2) | _required_ | Hierarchical columns from root to leaf (e.g. `[Kingdom, Phylum, Class, Order, Family, Genus]`) |
| `abundance_col` | str | _required_ | DC column that satisfies the `abundance` role above |

**Filtering / row tagging**

Renderer **hierarchically aggregates** by the `rank_cols` sequence. Intermediate arc sizes are reconstructed via Plotly's `branchvalues='total'`. No per-row tag — aggregation is deterministic and lossless.


[![Sunburst example](../images/guides/advanced-visualizations/sunburst_light.webp#only-light)](../images/guides/advanced-visualizations/sunburst_light.webp){target=_blank}

[![Sunburst example](../images/guides/advanced-visualizations/sunburst_dark.webp#only-dark)](../images/guides/advanced-visualizations/sunburst_dark.webp){target=_blank}
### Rarefaction

Alpha-diversity vs sequencing depth — one line per sample with optional ±SE band and group colouring.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `sample_id` | ✓ | String | Sample identifier |
| `depth` | ✓ | Numeric | Subsampling depth (x-axis) |
| `metric` | ✓ | Numeric | Alpha-diversity metric value (y-axis) |
| `iter` | — | Numeric | Iteration column to aggregate over |
| `group` | — | String | Categorical column for line colour grouping |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_ci` | bool | `true` | Shade ±1 SE band around each sample's curve |

**Filtering / row tagging**

Renderer **aggregates over `iter`** per `(sample_id, depth)` — computes mean ± CI. Optional `group` adds a colour split; otherwise one line per sample. No binary row tag.


[![Rarefaction example](../images/guides/advanced-visualizations/rarefaction_light.webp#only-light)](../images/guides/advanced-visualizations/rarefaction_light.webp){target=_blank}

[![Rarefaction example](../images/guides/advanced-visualizations/rarefaction_dark.webp#only-dark)](../images/guides/advanced-visualizations/rarefaction_dark.webp){target=_blank}
### Phylogenetic

Newick tree + tip metadata (Microreact-style) — 5 layouts, tip search, subtree highlight.

The tree itself comes from a separate DC with `dc_type: phylogeny` (served via `/advanced_viz/phylogeny/{dc_id}/newick`). Tip annotations live in a regular Table DC and are joined to tip labels at render time via `taxon_col`. The schema below validates the **metadata** DC only.

**Columns** (metadata DC)

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `taxon` | ✓ | String | Joins metadata rows to tip labels in the tree |
| `color` | — | Numeric \| String | Tip colouring (categorical or continuous) |
| `label` | — | String | Metadata column shown alongside the tip label (e.g. clade name) |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tree_wf_id` / `tree_dc_id` | str | _required_ | Workflow + DC ids of the phylogeny DC |
| `metadata_wf_id` / `metadata_dc_id` | str \| null | `null` | Optional metadata DC for tip annotations |
| `default_layout` | `rectangular` \| `circular` \| `radial` \| `diagonal` \| `hierarchical` | `rectangular` | Initial tree layout |
| `ladderize` | bool | `true` | Ladderise the tree by default |
| `show_metadata_strip` | bool | `true` | Render Microreact-style metadata strip next to each tip |
| `show_branch_lengths` | bool | `true` | Annotate branches with lengths |
| `show_internal_labels` | bool | `false` | Annotate internal nodes with their labels |


[![Phylogenetic example](../images/guides/advanced-visualizations/phylogenetic_light.webp#only-light)](../images/guides/advanced-visualizations/phylogenetic_light.webp){target=_blank}

[![Phylogenetic example](../images/guides/advanced-visualizations/phylogenetic_dark.webp#only-dark)](../images/guides/advanced-visualizations/phylogenetic_dark.webp){target=_blank}
### Dot plot

scanpy / Seurat marker-gene dot plot — cluster × gene with size = fraction expressing, colour = mean expression. The schema expects a **cluster-aggregated long table** — derive it from `AnnData` via `sc.get.aggregate` (or a manual `groupby` on `adata.X`), not from `rank_genes_groups` (which returns DE statistics, not aggregates).

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `cluster` | ✓ | String | Cluster / group (x-axis) |
| `gene` | ✓ | String | Gene / feature (y-axis) |
| `mean_expression` | ✓ | Float | Mean expression per (cluster, gene) — dot colour |
| `frac_expressing` | ✓ | Float | Fraction of cells with `X > 0` per (cluster, gene) — dot size |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_dot_size` | int (4–60) | `22` | Max marker size in pixels |
| `min_dot_size` | int (0–20) | `2` | Min marker size in pixels |


[![Dot plot example](../images/guides/advanced-visualizations/dot_plot_light.webp#only-light)](../images/guides/advanced-visualizations/dot_plot_light.webp){target=_blank}

[![Dot plot example](../images/guides/advanced-visualizations/dot_plot_dark.webp#only-dark)](../images/guides/advanced-visualizations/dot_plot_dark.webp){target=_blank}
### Embedding

2D / 3D sample embedding (PCA / UMAP / t-SNE / PCoA) — supports a **precomputed** DC (`dim_1`, `dim_2` columns already materialised) or **live-compute** mode (run the reduction on the fly via a Celery task and cache by `(dc, method, params, filters)`).

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `sample_id` | ✓ | String | Sample identifier |
| `dim_1` | ✓ | Float | First embedding dim (precomputed mode) |
| `dim_2` | ✓ | Float | Second embedding dim (precomputed mode) |
| `dim_3` | — | Float | Third dim — enables 3D |
| `cluster` | — | String | Cluster assignment column |
| `color` | — | Numeric \| String | Point colouring (metadata or expression) |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `compute_method` | `pca` \| `umap` \| `tsne` \| `pcoa` \| null | `null` | When set, runs the reduction live on the server; null = precomputed mode |
| `umap_n_neighbors` | int (2–100) | `15` | UMAP `n_neighbors` |
| `umap_min_dist` | float (0–1) | `0.1` | UMAP `min_dist` |
| `tsne_perplexity` | float (2–100) | `30.0` | t-SNE perplexity |
| `tsne_n_iter` | int (250–5000) | `1000` | t-SNE iterations |
| `pcoa_distance` | `bray_curtis` | `bray_curtis` | PCoA distance metric |
| `show_density` | bool | `false` | Overlay density contours |
| `point_size` | int (1–30) | `6` | Marker size |

**Filtering / row tagging**

In **precomputed mode** the renderer just plots the pre-existing coordinates. In **live-compute mode** it dispatches `POST /advanced_viz/compute_embedding`, which runs the chosen reduction on the wide sample × feature matrix and returns coordinates. Results are cached by `(dc_id, method, params, filters)`; tweaking a slider re-dispatches a fresh job.


[![Embedding example](../images/guides/advanced-visualizations/embedding_light.webp#only-light)](../images/guides/advanced-visualizations/embedding_light.webp){target=_blank}

[![Embedding example](../images/guides/advanced-visualizations/embedding_dark.webp#only-dark)](../images/guides/advanced-visualizations/embedding_dark.webp){target=_blank}
### Hierarchical Heatmap

Clustered heatmap with dendrograms + annotation tracks, à la R's [ComplexHeatmap](https://github.com/jokergoo/ComplexHeatmap) / [pheatmap](https://cran.r-project.org/package=pheatmap). Wraps the in-tree [:material-open-in-new: plotly-complexheatmap](https://github.com/weber8thomas/plotly-complexheatmap){ target="_blank" } library; heavy compute (clustering, dendrogram layout) runs in a Celery worker and is cached by `(dc, params hash)`.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `index` | ✓ | String | Row-label column (typically `sample_id`) |

Numeric matrix columns are inferred from the rest of the DC schema at compute time — there's no per-role binding for the value columns.

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `matrix_wf_id` / `matrix_dc_id` | str | _required_ | Workflow + DC ids of the wide matrix DC |
| `index_column` | str | `sample_id` | Row-label column |
| `value_columns` | list[str] \| null | `null` | Subset of numeric columns; null = all numeric |
| `row_annotation_cols` | list[str] | `[]` | Categorical columns rendered as a right-side annotation strip |
| `cluster_rows` / `cluster_cols` | bool | `true` | Enable hierarchical clustering |
| `cluster_method` | `ward` \| `single` \| `complete` \| `average` | `ward` | Linkage method |
| `cluster_metric` | `euclidean` \| `correlation` \| `cosine` | `euclidean` | Distance metric |
| `normalize` | `none` \| `row_z` \| `col_z` \| `log1p` | `none` | Pre-clustering normalisation |
| `colorscale` | str \| null | `null` | Plotly colorscale name override |


[![Hierarchical Heatmap example](../images/guides/advanced-visualizations/complex_heatmap_light.webp#only-light)](../images/guides/advanced-visualizations/complex_heatmap_light.webp){target=_blank}

[![Hierarchical Heatmap example](../images/guides/advanced-visualizations/complex_heatmap_dark.webp#only-dark)](../images/guides/advanced-visualizations/complex_heatmap_dark.webp){target=_blank}
### QQ

Quantile-quantile plot for p-value distributions (GWAS / DE / eQTL QC). Sorts p-values and plots `-log10(observed)` against the theoretical `-log10(expected)` under a uniform null.

**Columns**

| Role | Required | Type | Description |
|------|:--------:|------|-------------|
| `p_value` | ✓ | Float | Raw p-value (0–1) |
| `feature_id` | — | String | Hover-only id |
| `category` | — | String | Stratification column (one trace per stratum) |

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_ci` | bool | `true` | Shade the 95% null CI band |

**Filtering / row tagging**

When `category` is bound, the renderer produces **one trace per stratum** (e.g. genome partitions, ancestry groups). Otherwise a single trace plus the y = x reference line and the optional 95% null CI band.


[![QQ example](../images/guides/advanced-visualizations/qq_light.webp#only-light)](../images/guides/advanced-visualizations/qq_light.webp){target=_blank}

[![QQ example](../images/guides/advanced-visualizations/qq_dark.webp#only-dark)](../images/guides/advanced-visualizations/qq_dark.webp){target=_blank}
### UpSet

Set-intersection visualisation (alternative to Venn diagrams). Wraps the in-tree `plotly-upset` library (vendored under `packages/plotly-upset/`, not yet a standalone public repo); intersection enumeration + sorting runs in a Celery worker and is cached by `(dc, params hash)`. Input DC: a binary table where each row is an element and each `set_col` is a 0/1 membership indicator.

**Columns**

No canonical role-based schema — the renderer enumerates binary columns at compute time. Editor binding validation is a no-op.

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `matrix_wf_id` / `matrix_dc_id` | str | _required_ | Workflow + DC ids of the membership DC |
| `set_columns` | list[str] \| null | `null` | Explicit list of set columns; null = auto-detect binary |
| `sort_by` | `cardinality` \| `degree` \| `degree-cardinality` \| `input` | `cardinality` | Intersection ordering |
| `sort_order` | `descending` \| `ascending` | `descending` | Ordering direction |
| `min_size` | int (≥0) | `1` | Hide intersections smaller than this |
| `max_degree` | int \| null | `null` | Hide intersections involving more than N sets |
| `show_set_sizes` | bool | `true` | Show horizontal set-size bar chart |
| `color_intersections_by` | `none` \| `set` \| `degree` | `none` | Intersection-bar colour mode |

**Filtering / row tagging**

Renderer **filters by intersection size and degree** — `min_size` drops intersections below the threshold, `max_degree` drops intersections involving more sets than the limit.


[![UpSet example](../images/guides/advanced-visualizations/upset_plot_light.webp#only-light)](../images/guides/advanced-visualizations/upset_plot_light.webp){target=_blank}

[![UpSet example](../images/guides/advanced-visualizations/upset_plot_dark.webp#only-dark)](../images/guides/advanced-visualizations/upset_plot_dark.webp){target=_blank}
### Sankey

Categorical-flow diagram across N ordered categorical levels (e.g. `sample → lineage → clade`, `sample → kingdom → phylum → genus`). Server-side aggregation via Celery, client-side colour / opacity tweaks.

**Columns**

No canonical role-based schema — `step_cols` is a multi-column list (≥2 ordered categorical columns). The renderer validates step presence at compute time; the editor enforces `min_length=2`.

**Settings**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `step_cols` | list[str] (≥2, unique) | _required_ | Ordered categorical columns from source to leaf |
| `value_col` | str \| null | `null` | Optional numeric weight; null = each row counts as 1 |
| `sort_mode` | `alphabetical` \| `total_flow` \| `input` | `total_flow` | Node-ordering rule |
| `color_mode` | `source` \| `target` \| `step` | `source` | Link colouring rule |
| `link_opacity` | float (0.05–1) | `0.5` | Link transparency |
| `min_link_value` | float (≥0) | `0.0` | Hide links whose aggregated value is below this threshold |
| `show_node_labels` | bool | `true` | Render node labels |

**Filtering / row tagging**

Renderer **aggregates by the `step_cols` sequence** (via Celery `compute_sankey`) and filters out links whose aggregated value is below `min_link_value`.


[![Sankey example](../images/guides/advanced-visualizations/sankey_light.webp#only-light)](../images/guides/advanced-visualizations/sankey_light.webp){target=_blank}

[![Sankey example](../images/guides/advanced-visualizations/sankey_dark.webp#only-dark)](../images/guides/advanced-visualizations/sankey_dark.webp){target=_blank}
### Oncoplot

Sample × gene mutation matrix with discrete mutation-type colours and per-gene / per-sample frequency strips.

**Columns** — straight rename from canonical Mutation Annotation Format (VEP / vcf2maf / maftools — the cancer-mutation file format, not Minor Allele Frequency):

| Role | Required | Type | Description | Mutation Annotation Format column |
|------|:--------:|------|-------------|------------|
| `sample_id` | ✓ | String | Sample identifier (x-axis) | `Tumor_Sample_Barcode` |
| `gene` | ✓ | String | Gene identifier (y-axis) | `Hugo_Symbol` |
| `mutation_type` | ✓ | String | Categorical mutation type (cell colour) | `Variant_Classification` |

**Settings**

No additional knobs — the layout is fully determined by the column bindings.

**Filtering / row tagging**

Cells are **coloured categorically by `mutation_type`** (NA cells stay blank). Side strips show per-gene and per-sample mutation counts.


[![Oncoplot example](../images/guides/advanced-visualizations/oncoplot_light.webp#only-light)](../images/guides/advanced-visualizations/oncoplot_light.webp){target=_blank}

[![Oncoplot example](../images/guides/advanced-visualizations/oncoplot_dark.webp#only-dark)](../images/guides/advanced-visualizations/oncoplot_dark.webp){target=_blank}

---

## :material-card-text: Card Components <small>(v0.0.1+)</small> { #card-components }

Card components display metrics with aggregations. A card shows a **hero metric** (primary value) and can optionally display **secondary metrics** below it for at-a-glance summaries.

### Aggregation Types

| Aggregation | Description | Example |
|-------------|-------------|---------|
| :material-counter: **count** | Number of rows | Total samples |
| :material-sigma: **sum** | Sum of values | Total reads |
| :material-chart-line-variant: **average** | Average value | Average coverage |
| :material-format-vertical-align-center: **median** | Median value | Median quality score |
| :material-arrow-down: **min** | Minimum value | Minimum mapping rate |
| :material-arrow-up: **max** | Maximum value | Maximum duplication rate |
| :material-tag-multiple: **nunique** | Count of unique values | Unique sample types |
| :material-chart-bell-curve-cumulative: **std_dev** | Standard deviation | Coverage spread |
| :material-chart-bell-curve: **variance** | Variance | Expression variability |
| :material-arrow-expand-horizontal: **range** | Max − Min | Read length range |
| :material-wave: **skewness** | Distribution skew | Quality score symmetry |
| :material-sine-wave: **kurtosis** | Distribution tailedness | Outlier tendency |
| :material-percent: **percentile** | 50th percentile | Median coverage |
| :material-poll: **mode** | Most frequent value | Dominant sample type |

### Configuration

1. Select a **Data Collection**
2. Choose a **Column** to aggregate
3. Select an **Aggregation** type (hero metric)
4. Optionally add **Secondary Metrics** (`aggregations`) for a multi-metric summary
5. Optionally add a **Filter Expression** (`filter_expr`) for conditional aggregation
6. Customize the **Title**, **Icon**, and **Styling**

### Multi-Metric Summary Cards

Cards can display multiple aggregation results in a single component. The primary `aggregation` is shown as the large hero value, and `aggregations` are displayed as compact secondary rows below it.

```text
┌─────────────────────────────────┐
│ Petal Length              [Icon]│
├─────────────────────────────────┤
│           4.5 cm                │
│          (Average)              │
├─────────────────────────────────┤
│ Median:       4.35              │
│ Std Dev:      0.82              │
│ Min:          1.00              │
│ Max:          6.90              │
└─────────────────────────────────┘
```

### Conditional Aggregation (filter_expr)

Cards support a `filter_expr` field — a Polars expression that pre-filters the data **before** computing the aggregation. This enables conditional metrics like "count of samples with coverage > 30x" without creating a separate data collection.

`filter_expr` works **on top of** interactive filters (dual-layer filtering): interactive filters narrow the dataset first, then `filter_expr` applies an additional condition before aggregation.

See [Filter Expressions](filter-expressions.md) for the complete expression reference.

### Styling Options

| Option | Description | Example |
|--------|-------------|---------|
| Title | Metric label | "Total Samples" |
| Description | Subtitle text | "Across all batches" |
| Icon | Iconify icon name | `mdi:chart-line` |
| Icon Color | Icon accent color | `#2196F3` |
| Title Color | Title text color | `#333333` |
| Title Font Size | Title font size | `sm` |
| Value Font Size | Hero value font size | `xl` |

---

## :material-format-header-1: Text Components <small>(v0.2.0+)</small> { #text-components }

Text components display section headers to organize your dashboard.

### Supported Header Levels

| Level | Syntax | Description |
|-------|--------|-------------|
| **H1** | `# Header` | Main section headers |
| **H2** | `## Header` | Sub-section headers |
| **H3** | `### Header` | Minor section headers |

!!! warning "Limited Markdown Support"
    Currently, only H1, H2, and H3 headers are supported. Full markdown rendering (lists, links, bold, italic, code blocks, etc.) is not available in text components.

### Use Cases

- :material-format-title: Dashboard section headers
- :material-view-grid: Visual organization of content
- :material-label: Labeling groups of related components

---

## :material-tune: Interactive Components <small>(v0.0.1+)</small> { #interactive-components }

Interactive components let users filter data across the dashboard. These components affect all linked visualization components.

### Component Types

| Component | Input Type | Best For |
|-----------|------------|----------|
| :material-ray-start-end: **RangeSlider** | Numeric range | Coverage: 0-100x |
| :material-format-list-checks: **MultiSelect** | Multiple choices | Sample types |
| :material-calendar: **DatePicker** | Date range | Run dates |
| :material-toggle-switch: **SegmentedControl** | Single choice | Condition A/B |
| :material-form-textbox: **TextInput** | Free text | Sample ID search |

### RangeSlider

Filter data by numeric range:

| Option | Description |
|--------|-------------|
| Column | Numeric column to filter |
| Min/Max | Range bounds |
| Step | Increment value |
| Default | Initial range values |

### MultiSelect

Filter by selecting multiple values:

| Option | Description |
|--------|-------------|
| Column | Categorical column to filter |
| Options | Available values (auto-populated) |
| Default | Initially selected values |
| Placeholder | Hint text when empty |

### DatePicker

Filter by date range:

| Option | Description |
|--------|-------------|
| Column | Date/datetime column to filter |
| Format | Date display format |
| Default | Initial date range |

### SegmentedControl

Single-selection toggle:

| Option | Description |
|--------|-------------|
| Column | Column to filter |
| Options | Available choices |
| Default | Initially selected option |

### Scoped Filters (filter_expr)

Interactive components support a `filter_expr` field that **pre-filters the underlying data before computing component options**. Instead of showing all possible values, the component shows only values that exist in the filtered subset.

**Example**: A MultiSelect with `filter_expr: "col('petal.length') > 4"` only shows variety options that appear in rows where petal length exceeds 4 cm.

This is useful for:

- :material-filter-variant: **Cascading filters** — show only relevant options based on data conditions
- :material-microscope: **Domain-specific scoping** — e.g., only show taxa above an abundance threshold
- :material-target: **Focused analysis** — restrict a slider's range to a meaningful subset

See [Filter Expressions](filter-expressions.md) for the complete expression reference.

---

## :material-microscope: MultiQC Components <small>(v0.5.0+)</small> { #multiqc-components }

MultiQC components display quality control reports generated by [:material-open-in-new: MultiQC](https://multiqc.info/){ target="_blank" }.

### Features

| Feature | Description |
|---------|-------------|
| :material-application-brackets: **Report Embedding** | Display MultiQC HTML reports inline |
| :material-navigation: **Interactive Navigation** | Navigate between MultiQC sections |
| :material-tools: **Tool Integration** | Support for various QC tools (FastQC, Samtools, STAR, etc.) |

### Configuration

| Option | Description |
|--------|-------------|
| Report Path | Path to MultiQC report HTML file |
| Display Mode | Full report or specific sections |

!!! note "Data Requirements"
    MultiQC components require pre-generated MultiQC reports. The report HTML files should be accessible via the configured data source.

---

## :material-image-multiple: Image Components <small>(v0.7.0+)</small> { #image-components }

Image components display image galleries from S3/MinIO storage, with metadata filtering and thumbnail previews.

### Features

| Feature | Description |
|---------|-------------|
| :material-grid: **Grid Layout** | Configurable column layout for image thumbnails |
| :material-image-search: **Thumbnail Previews** | Auto-generated thumbnails with configurable size |
| :material-filter: **Metadata Filtering** | Filter images using interactive components |
| :material-cloud-download: **S3 Integration** | Serve images directly from S3/MinIO buckets |
| :material-gesture-tap: **Click to Expand** | View full-size images in a modal |

### Configuration

| Option | Description | Default |
|--------|-------------|---------|
| Data Collection | Source table with image metadata | Required |
| Image Column | Column containing image paths | Required |
| S3 Base Folder | S3/MinIO bucket path prefix | Required |
| Thumbnail Size | Thumbnail height in pixels | 150 |
| Columns | Number of columns in grid | 4 |
| Max Images | Maximum images to display | 20 |

### Data Collection Setup

Image components require a **Table-type Data Collection** with:

1. A column containing relative image paths (e.g., `image_path`)
2. Optional metadata columns for filtering (e.g., `category`, `quality_score`)

Example CSV structure:

```csv
sample_id,image_path,category,quality_score
sample_001,images/sample_001.png,A,0.95
sample_002,images/sample_002.png,B,0.87
sample_003,images/sample_003.jpg,A,0.92
```

### Project YAML Configuration

Configure the Image data collection in your `project.yaml`:

```yaml
data_collections:
  - id: "650a1b2c3d4e5f6a7b8c9d10"
    data_collection_tag: "sample_images"
    description: "Sample images with metadata"
    config:
      type: "Image"
      metatype: "Images"
      scan:
        mode: single
        scan_parameters:
          filename: images_data.csv
      dc_specific_properties:
        # Table fields (required for delta table)
        format: "csv"
        columns_description:
          sample_id: "Unique sample identifier"
          image_path: "Relative path to image file"
          category: "Sample category"
          quality_score: "Quality score 0-1"
        # Image-specific fields (mandatory)
        image_column: "image_path"
        # Image display properties (optional)
        s3_base_folder: "s3://bucket-name/images/"
        local_images_path: ./images
        supported_formats: [".png", ".jpg", ".jpeg"]
        thumbnail_size: 150
```

### Dashboard YAML Configuration

Add an image component in your `dashboard_lite.yaml`:

```yaml
components:
  - tag: sample-gallery
    component_type: image
    workflow_tag: python/image_workflow
    data_collection_tag: sample_images
    image_column: image_path
    s3_base_folder: "s3://bucket-name/images/"
    thumbnail_size: 150
    columns: 3
    max_images: 9
```

### Image Storage

Images can be stored and accessed in two ways:

**Option 1: Images already on S3/MinIO**

If your images are already uploaded to S3/MinIO, specify the location in your project configuration:

```yaml
# In project.yaml - dc_specific_properties
s3_base_folder: "s3://bucket-name/images/"
```

**Option 2: Upload local images with depictio-cli (Recommended)**

Use the `depictio-cli run` command to automatically upload images from a local directory to S3:

```yaml
# In project.yaml - dc_specific_properties
local_images_path: ./images  # Local path relative to project directory
```

```bash
# Run depictio-cli to sync project and upload images
depictio-cli run --project-dir /path/to/project
```

The CLI will:

1. Read the `local_images_path` from your project configuration
2. Upload images to the configured S3 bucket
3. Set the correct `s3_base_folder` automatically

!!! tip "Cross-DC Filtering"
    Image components support filtering via interactive components on the same Data Collection. Select samples using a MultiSelect filter, and the image gallery updates automatically.

---

## :material-map-marker-multiple: Map Components <small>(v0.8.0+)</small> { #map-components }

Map components display geospatial data on interactive tile-based maps using Plotly Express (no API key required).

### Coordinates Data Collection <small>(v0.12.0+)</small> { #coordinates-dc }

Map components require a Table DC that explicitly declares its latitude and longitude columns. The `DCTableCoordinatesConfig` variant — defined at `depictio/models/models/data_collections_types/table_coordinates.py:6` — extends the standard Table DC with three fields:

| Field | Required | Type | Default | Description |
|-------|:--------:|------|---------|-------------|
| `lat_column` | ✓ | str | — | Column holding latitude values |
| `lon_column` | ✓ | str | — | Column holding longitude values |
| `crs` | — | str | `EPSG:4326` | Coordinate reference system |

It inherits every standard Table DC capability (CSV / TSV / Parquet format, `polars_kwargs`, `keep_columns`, `columns_description`). The `dc_type` stays `"table"` — the variant is materialised at deserialisation when `lat_column` / `lon_column` are present. A model validator enforces that the two columns must differ.


![Coordinates DC example](../images/guides/map/coordinates_dc.png)

### Map Types

| Type | Function | Best For |
|------|----------|----------|
| :material-map-marker: `scatter_map` | Point markers at lat/lon coordinates | Sample locations, site maps |
| :material-heat-wave: `density_map` | Heatmap overlay from point density | Concentration hotspots |
| :material-map-legend: `choropleth_map` | Colored polygon regions from GeoJSON | Per-country/region statistics |

### Configuration Options

| Option | Applies To | Description |
|--------|------------|-------------|
| `lat_column` / `lon_column` | scatter, density | Columns with GPS coordinates (required) |
| `color_column` | scatter, choropleth | Column for color encoding |
| `size_column` | scatter | Column for marker size encoding |
| `hover_columns` | scatter, choropleth | Columns shown on hover tooltip |
| `map_style` | all | Tile style: `open-street-map`, `carto-positron`, `carto-darkmatter` |
| `opacity` | all | Marker/region opacity (0.0–1.0) |
| `default_zoom` / `default_center` | all | Override auto-computed viewport |

### Choropleth GeoJSON Sources

Choropleth maps require a GeoJSON FeatureCollection to define region boundaries. Three sources are supported:

| Source | Field | Description |
|--------|-------|-------------|
| URL | `geojson_url` | Public URL to a GeoJSON file |
| Data Collection | `geojson_dc_tag` | Tag of a `geojson`-type Data Collection in the same project |
| Inline | `geojson_data` | Embedded GeoJSON dict (large — prefer URL or DC) |

### Selection Filtering

Scatter maps support the same lasso/box/click selection as scatter plots. Enable with `selection_enabled: true` and `selection_column`. See [Interactive Selection Filtering](interactive-selection-filtering.md) for details.

!!! note "Choropleth Limitation"
    Choropleth maps do not support selection filtering (Plotly does not expose click/lasso on choropleth traces).

### YAML Examples

**Scatter map:**

```yaml
- tag: sampling-map
  component_type: map
  workflow_tag: python/my_workflow
  data_collection_tag: sample_metadata
  lat_column: latitude
  lon_column: longitude
  color_column: biome
  size_column: read_count
  hover_columns: [sample_id, site_name, country]
  map_style: carto-positron
  selection_enabled: true
  selection_column: sample_id
```

**Choropleth map:**

```yaml
- tag: country-choropleth
  component_type: map
  workflow_tag: python/my_workflow
  data_collection_tag: sample_metadata
  map_type: choropleth_map
  locations_column: country_name
  featureidkey: properties.NAME
  color_column: sample_id
  choropleth_aggregation: count
  color_continuous_scale: Viridis
  geojson_url: "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
```

---

## :material-link-variant: Cross-DC Filtering

Interactive components can filter across **linked Data Collections** using the Links system. See [Cross-DC Filtering](cross-dc-filtering.md) for details.

```text
┌─────────────────┐         ┌─────────────────┐
│  Filter: Status │  link   │  Table: Samples │
│  [MultiSelect]  │────────▶│  [auto-filters] │
└─────────────────┘         └─────────────────┘
```

---

## :material-creation: Component Creation

### Using the Stepper Wizard

The component builder guides you through creation:

1. :material-database: **Select Data Collection** - Choose your data source
2. :material-shape: **Choose Component Type** - Figure, Table, Card, Interactive, Text, MultiQC, or Map
3. :material-cog: **Configure Settings** - Type-specific options
4. :material-eye: **Preview** - See the component before adding
5. :material-plus-circle: **Add to Dashboard** - Place on the canvas

### Positioning Components

- :material-drag: **Drag and drop** components in Edit Mode
- :material-grid: Components snap to a **grid layout**
- :material-resize: Resize by dragging corner handles
WATCHER-VERIFY-1778951276
