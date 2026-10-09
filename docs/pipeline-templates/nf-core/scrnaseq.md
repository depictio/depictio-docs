---
title: Single-cell RNA-seq
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/scrnaseq" target="_blank" title="nf-core/scrnaseq on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/scrnaseq/master/docs/images/nf-core-scrnaseq_logo_dark.png" alt="nf-core/scrnaseq">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/scrnaseq/master/docs/images/nf-core-scrnaseq_logo_light.png" alt="nf-core/scrnaseq">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Single-cell RNA-seq</h1>
    <p class="template-subtitle">From reads to called cells on the Cell Ranger route: library metrics, the knee curve and CellBender, per-cell QC, embeddings, clusters and marker genes, with an optional comparison of the aligner routes.</p>
    <p class="template-links">
      <a href="https://nf-co.re/scrnaseq" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/scrnaseq" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="4.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="4.2.0" selected>4.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The scrnaseq template follows a 10x run from the raw reads to the genes that mark
each cluster:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: FastQC and Cell Ranger's own summary from the MultiQC report, and each library's metrics against 10x Genomics' cut-offs
- :material-scatter-plot: **Cells**: the barcodes called as cells and the ambient RNA removed, how the aligner routes agree, the MAD rules that flag a cell, the UMAP and t-SNE, and the clusters with their cell cycle
- :material-dna: **Genes**: the marker genes of each cluster, and two lassoed groups of cells tested gene by gene

The persistent `Sample filters` sit in the left panel and narrow every tab. On
the tabs that draw cells, the collapsed `Cell filters` (cluster, QC status, UMIs
and genes per cell) compose forward through the `cluster_label` links, so a
cluster picked there narrows the cluster, marker, per-cell expression and
cell-cycle tables alike.

!!! info "The Cell Ranger route carries the dashboard"
    Only `--aligner cellranger` (the pipeline default) publishes the matrices,
    the secondary analysis and a MultiQC report the template reads, so it is
    required. The simpleaf and kallisto routes are optional and feed the Aligner
    Concordance tab only; a Cell Ranger-only run has no Aligner Concordance tab.

!!! warning "Two readings assume a human reference"
    The mitochondrial share and the MAD mito rule read gene symbols starting
    with `MT-`, and the cell-cycle scores read the human Tirosh gene sets. On
    another organism, or a reference without mitochondrial genes, the mito
    columns read 0 and the phase degrades to NA. The dashboard therefore leads
    with the top-20 gene share and the ribosomal share.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/scrnaseq_results \
      --template nf-core/scrnaseq/latest
    ```

    Pass the results root. The sample hub reads the samplesheet the
    run was launched with, which the pipeline does not publish: copy it anywhere
    under the results root first (for example `input/samplesheet.csv`). To keep
    the lineage markers of your tissue on the per-cell marker tiles, name them:

    ```bash
    depictio ingest /path/to/scrnaseq_results \
      --template nf-core/scrnaseq/latest \
      --var MARKER_PANEL=GENE1,GENE2,GENE3
    ```

    | Variable | Default | Role |
    |---|---|---|
    | `MARKER_PANEL` | none | Comma-separated gene symbols the Markers violins and the colour menu of the Embeddings gene UMAP always carry. Unset, or with none of its genes in the reference, the tiles use the top markers of every graph-based cluster |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/scrnaseq -r 4.2.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the MultiQC report and Cell Ranger's `outs/` directory: the
per-sample `metrics_summary.csv`, the raw and filtered feature-barcode matrices
and the `analysis/` tables (every clustering, the UMAP, t-SNE and PCA
projections, the feature dispersion and the marker genes of every resolution).
Cell Ranger writes no sample column, so raw scans carry the file path and
recipes recover the sample from it. The knee curve is summed straight out of the
raw MatrixMarket file with a streaming scan, never a dense matrix.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="4.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/scrnaseq-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then nine child tabs in three groups, read as a
funnel from the reads to the cells, their clusters and the genes that mark them.
Each tab below carries the **same icon and colour the dashboard gives it**, so the
page and the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Library QC |
| Cells | Cell Calling, Aligner Concordance, Cell QC, Embeddings, Clusters |
| Genes | Markers, Compare Selections |

Each child tab opens with a short intro and a strip of two to four cards, then at
most three open sections; tables and details follow, collapsed. The persistent
*Sample filters* (the sample) sit in the left panel and narrow every tab through
the sample links. The persistent *Cell filters* (cluster, QC status, UMIs and genes
per cell, on the per-cell QC table) sit collapsed at the bottom of the panel on the
four tabs that draw cells: Cell QC, Embeddings, Clusters and Markers. A cluster
picked there narrows the cluster summary, marker, expression and cell-cycle tables
through the `cluster_label` links. The *Sample sheet* is pinned, collapsed, to the
bottom of every child tab. Cell Ranger clusters each sample on its own, so on a
multi-sample run a cluster label shared by two samples is not the same population.

=== ":material-compass-outline: Overview"

    *Droplet single-cell RNA-seq, from reads to called cells, clusters and their marker genes.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/scrnaseq/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/scrnaseq/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how the two
    filter levels work, *The run* lists the samples, the aligner, the protocol and
    the genome, and *Pipeline* walks the five steps from reads to marker genes
    (reads, count, call, flag, cluster), each linked to its parameters and its tab.
    Every key figure, finding and highlight reads the Cell Ranger route, which every
    run writes. The findings are live values: they follow the filters.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (the QC status and the sample), and so does *Findings* (the
        sample and the cluster): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: cells called, genes per cell, clusters, marker genes |
        | Findings | Live result rows, then 4 figures: the UMAP by cluster, the barcode-rank curve, the cells per cluster with the flagged ones on top and the strongest marker of each cluster |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the reads and Cell Ranger's own QC hold for every sample?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only, from the pipeline's own report. Open: the general
    statistics and Cell Ranger count's summary table, then its median-genes and
    saturation curves, then the FastQC sequence counts and per-sequence quality.
    GC content and duplication are collapsed; duplication runs high by design, since
    each transcript is read many times. Cell Ranger's own barcode-rank panel is left
    out: the Cell Calling tab draws the same curve with the called cells marked.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · no filter of its own: the persistent `Sample` filter reaches
        the report through the sample link.

        | Section | What it holds |
        |---|---|
        | QC overview | 2 MultiQC panels |
        | Cell Ranger curves | 2 MultiQC panels |
        | Read quality | 2 MultiQC panels |
        | QC details (collapsed) | 2 MultiQC panels |

=== ":material-check-decagram:{ .mc-blue } Library QC"

    **Data & QC** · *Do the libraries meet 10x Genomics' own QC guidance?*

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/library_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/library_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/library_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/library_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The reads in cells, the sequencing saturation and the reads on the
    transcriptome as levels out of 100, and the reads per cell with the samples
    counted against the 20,000 10x recommends. Then each library metric (saturation,
    reads in cells, valid barcodes, Q30 on the RNA read, mapped to the transcriptome)
    as a dot coloured by its verdict beside a grey tick at the 10x cut-off, and the
    reads by genomic region, grouped rather than stacked because antisense overlaps
    exonic and intronic. The checks table and Cell Ranger's metrics are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Check verdict` on `cellranger_library_metrics_long` and
        `Mapping region` on `cellranger_mapping_breakdown`.

        | Section | What it holds |
        |---|---|
        | Libraries at a glance | 4 cards |
        | Against 10x's guidance | *Library metrics against their cut-offs* |
        | Where the reads map | *Read mapping by region* |
        | Metrics tables (collapsed) | *Library checks*, *Cell Ranger metrics* |

=== ":material-filter-variant:{ .mc-cyan } Cell Calling"

    **Cells** · *How many barcodes are cells, and how much ambient RNA was removed?*

    [![Cell Calling dashboard](../../images/pipeline-templates/nf-core/scrnaseq/cell_calling_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/cell_calling_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Cell Calling dashboard](../../images/pipeline-templates/nf-core/scrnaseq/cell_calling_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/cell_calling_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The barcodes observed, followed down to the cells Cell Ranger calls, the cells
    CellBender keeps and the cells that pass QC, each stage a subset of the one
    before; then the UMI counts CellBender keeps out of the raw counts. Then the
    barcode-rank ("knee") curve, computed off the raw matrix, one curve per sample
    with the called cells drawn darker. Most barcodes are empty droplets: the cliff
    is where the cells end. The calling funnel and CellBender's metrics are
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `UMIs per barcode` range on `cellranger_barcode_rank`.

        | Section | What it holds |
        |---|---|
        | Calling at a glance | 2 cards |
        | The knee | 1 advanced visualization |
        | Calling tables (collapsed) | *Cell-calling funnel*, *CellBender metrics* |

    !!! tip "Without CellBender"
        A `--skip_cellbender` run has no CellBender card or table here, and the
        funnel card widens. The funnel's CellBender stage and the CellBender shares
        on Clusters read empty.

=== ":material-set-merge:{ .mc-lime } Aligner Concordance"

    **Cells** · *Do Cell Ranger, simpleaf and kallisto call the same cells?*

    [![Aligner Concordance dashboard](../../images/pipeline-templates/nf-core/scrnaseq/aligner_concordance_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/aligner_concordance_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Aligner Concordance dashboard](../../images/pipeline-templates/nf-core/scrnaseq/aligner_concordance_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/aligner_concordance_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A run with several `--aligner` routes calls cells three ways, each with
    CellBender on top. The cells each route calls, and the barcodes any method calls,
    split by how many methods agree. Then each route's own call against CellBender's
    on it (the diagonal is agreement) beside its mapping rate, and the UpSet of the
    five cell calls, matched on the bare 16-base barcode so the overlap compares the
    same droplets. Most cells should sit in the intersection of every method.
    simpleaf's knee curve and both tables are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Aligner route` on `aligner_summary` and a `Methods agreeing`
        range on `cell_calls_by_method`.

        | Section | What it holds |
        |---|---|
        | Routes at a glance | 2 cards |
        | Routes side by side | 1 advanced visualization + *Mapping rate per route* |
        | Cell-call overlap | 1 advanced visualization |
        | Route details (collapsed) | 1 advanced visualization (the simpleaf knee), *Aligner summary*, *Cell calls by method* |

    !!! tip "Only with more than one route"
        Every collection this tab reads is optional. A Cell Ranger-only run, the
        pipeline default, has no Aligner Concordance tab.

=== ":material-shield-check-outline:{ .mc-grape } Cell QC"

    **Cells** · *Which called cells do the MAD rules flag, and why?*

    [![Cell QC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/cell_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/cell_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Cell QC dashboard](../../images/pipeline-templates/nf-core/scrnaseq/cell_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/cell_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The called cells as a ring by the rule that flags them, the UMIs and the genes
    per cell, and the top-20 gene share. Then UMIs against genes per cell on log
    axes, coloured by QC status, and the UMIs and top-20 share per cluster as boxes.
    The rules run per sample on log1p values: 5 MAD below the median for UMIs and
    genes, 5 MAD above for the top-20 share, the median plus 3 MAD or 8% for the
    mitochondrial share. Flagged cells stay in the data; the cell filters take them
    out. The per-cell table is collapsed, with a cell record beside it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Failing rule` and a `Top-20 gene share (%)` range on
        `cellranger_cell_qc`, plus the cell filters.

        | Section | What it holds |
        |---|---|
        | Cell QC at a glance | 4 cards |
        | Depth against genes | 1 advanced visualization |
        | Per cluster | *UMIs per cell, by cluster*, *Top-20 gene share, by cluster* |
        | Flagged cells (collapsed) | *Per-cell QC* + a cell record card |

=== ":material-scatter-plot:{ .mc-indigo } Embeddings"

    **Cells** · *Do the cells separate into groups on the UMAP and t-SNE?*

    [![Embeddings dashboard](../../images/pipeline-templates/nf-core/scrnaseq/embeddings_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/embeddings_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Embeddings dashboard](../../images/pipeline-templates/nf-core/scrnaseq/embeddings_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/embeddings_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The cells on the map, the genes scored for dispersion as a ring of those the PCA
    used, the first component's share of the variance and the genes whose normalised
    dispersion passes 0.5. Then the UMAP by cluster, where a lasso filters the other
    tabs, and the same UMAP bound to the per-cell expression table: every panel gene
    is a column of its colour menu. The t-SNE, mean expression against dispersion and
    the variance per component are collapsed. Cell Ranger selects every gene with a
    finite dispersion, so the selection is not a variable-gene call.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Ribosomal share (%)` range on `cellranger_cell_qc` and a
        `Normalised dispersion` range on `cellranger_hvg_dispersion`, plus the cell
        filters.

        | Section | What it holds |
        |---|---|
        | Maps at a glance | 4 cards |
        | Cells on the map | 1 advanced visualization |
        | A gene on the map | 1 advanced visualization |
        | t-SNE (collapsed) | 1 advanced visualization |
        | Feature selection and PCA (collapsed) | 1 advanced visualization + *Variance per component* |

=== ":material-chart-donut:{ .mc-violet } Clusters"

    **Cells** · *Which clusters are large and clean, and which are cycling?*

    [![Clusters dashboard](../../images/pipeline-templates/nf-core/scrnaseq/clusters_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/clusters_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Clusters dashboard](../../images/pipeline-templates/nf-core/scrnaseq/clusters_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/clusters_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The cells in the clusters, the flagged share of the highest cluster against 5%
    and 10%, the cells by cell-cycle phase and the share of the lowest cluster's
    cells CellBender also calls, against 95% and 90%. Then the cells per cluster with
    the flagged ones on top, the QC medians of each cluster coloured by z-score, and
    S against G2/M score per cell beside the phase mix of each cluster. A cluster
    with a high flagged share or low depth may be damaged cells, not a cell type. The
    stability Sankey across resolutions and the cluster table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Cells per cluster` range on `cellranger_cluster_summary`
        and `Cell-cycle phase` on `cellranger_cell_cycle`, plus the cell filters.

        | Section | What it holds |
        |---|---|
        | Clusters at a glance | 4 cards |
        | Cluster sizes | *Cells per cluster* |
        | Cluster QC profile | *Cluster QC medians* |
        | Cell cycle | 1 advanced visualization + *Phase mix per cluster* |
        | Cluster details (collapsed) | 1 advanced visualization + *Cluster summary* |

=== ":material-dna:{ .mc-pink } Markers"

    **Genes** · *Which genes mark each cluster?*

    [![Markers dashboard](../../images/pipeline-templates/nf-core/scrnaseq/markers_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/markers_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Markers dashboard](../../images/pipeline-templates/nf-core/scrnaseq/markers_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/markers_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The marker genes up-regulated at adjusted p below 0.05, with how many recur
    across clusters, and their median log2 fold change. Then the dot plot (dot size
    the share of the cluster's cells expressing the gene, colour its mean), and the
    volcano beside the strongest marker of each cluster. The volcano has no QQ view:
    these are Cell Ranger's top-ranked markers per cluster, not a genome-wide test.
    The violins cell by cell, the marker table with a gene record beside it and the
    marker expression table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Clustering` on `cellranger_diffexp` (opens on `graphclust`)
        and `Gene, cell by cell` on `cellranger_cell_expression_long`, plus the cell
        filters.

        | Section | What it holds |
        |---|---|
        | Markers at a glance | 2 cards |
        | Marker dot plot | 1 advanced visualization |
        | Differential expression | 1 advanced visualization + *Strongest marker per cluster* |
        | Per-cell marker spread (collapsed) | *Marker expression per cluster* |
        | Gene detail (collapsed) | *Marker genes* + a gene record card, *Marker expression per cluster* |

=== ":material-scale-balance:{ .mc-teal } Compare Selections"

    **Genes** · *Which genes separate two groups of cells you lasso?*

    [![Compare Selections dashboard](../../images/pipeline-templates/nf-core/scrnaseq/compare_selections_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/compare_selections_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Compare Selections dashboard](../../images/pipeline-templates/nf-core/scrnaseq/compare_selections_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/scrnaseq/compare_selections_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The cells on the map as a ring by QC status, and the clusters on it. Then the
    UMAP with lasso on: save one set of cells as group A and a second as group B,
    and every gene of the marker panel is tested between them (Wilcoxon rank-sum on
    log1p(CP10k), FDR-corrected across genes). With no groups saved it compares the
    two largest clusters. Narrow to `pass` cells first: two groups of very different
    depth differ on almost every gene for the wrong reason.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Clusters on the map` and a `QC status` switch on
        `cellranger_cell_expression`.

        | Section | What it holds |
        |---|---|
        | Cells in play | 2 cards |
        | Pick the cells | 1 advanced visualization |
        | Compare the groups | 1 advanced visualization |

Every scatter and embedding of cells selects on `barcode` (the UMI against genes
scatter, the UMAP and t-SNE, the phase scatter, the lasso UMAP; the UMAP coloured
by a gene does not), the route scatter on `aligner`, and the tables on their entity
column: `sample_id` in the sample sheet, `sample` in the metrics and funnel tables,
`barcode` for cells, `cluster_label` for clusters, `gene` for markers, `aligner`
for routes and `barcode_core` for the cell-call overlap. A pick narrows the other
tiles on the same collection or linked to it, and each record card follows the
table beside it.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/scrnaseq, it does not run the pipeline.
Run the pipeline first, on the Cell Ranger route:

```bash
nextflow run nf-core/scrnaseq -r 4.2.0 \
  --input samplesheet.csv \
  --fasta genome.fa --gtf genes.gtf \
  --aligner cellranger --protocol 10XV3 \
  --outdir results -profile docker
```

Then copy the samplesheet next to the results and point Depictio at them:

```bash
mkdir -p results/input && cp samplesheet.csv results/input/
depictio ingest results/ --template nf-core/scrnaseq/latest
```

To fill the Aligner Concordance tab, run the pipeline once more per extra
`--aligner` route and gather the route directories under one results root. See
[nf-co.re/scrnaseq/usage](https://nf-co.re/scrnaseq/4.2.0/docs/usage) for full
pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the results root. Every scan is anchored on the tool
directory name (`cellranger/`, `simpleaf/`, `kallisto/`), so a single-route
output directory and a root holding several routes scan the same way.

```text
<DATA_ROOT>/
├── input/samplesheet.csv                      # the hub: copy it in, anywhere under the root
├── [aligner_cellranger/]
│   ├── pipeline_info/{params,software_versions}*
│   ├── multiqc/multiqc_data/multiqc.parquet   # native, no reprocess
│   └── cellranger/
│       ├── count/<sample>/outs/
│       │   ├── metrics_summary.csv
│       │   ├── raw_feature_bc_matrix/{matrix.mtx.gz,barcodes.tsv.gz,features.tsv.gz}
│       │   ├── filtered_feature_bc_matrix/{matrix.mtx.gz,barcodes.tsv.gz,features.tsv.gz}
│       │   └── analysis/{clustering,umap,tsne,pca,diffexp}/*/*.csv
│       └── <sample>/cellbender_removebackground/*_{metrics,cell_barcodes}.csv   # optional
├── [aligner_simpleaf/]simpleaf/<sample>/      # optional: af_quant, af_map, qcatch, CellBender
└── [aligner_kallisto/]kallisto/<sample>.count/ # optional: run_info.json, inspect.json, barcodes
```

The BAM, BUS, `.h5`, `.h5ad`, `.cloupe` and `.rds` binaries are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 4.2.0 release,
`results-3fc17b4f971a89e47c88337de71d0e777ffad8cc`: the pbmc8k sample (10x v2
chemistry, GRCh38) on the Cell Ranger, simpleaf and kallisto routes, so the
Aligner Concordance tab is filled. The screenshots above come from that run.
`megatest.yaml` lists the tables-only subset the template needs; the samplesheet
the run names in `params.json` is fetched into `input/` separately:

```bash
bash depictio/projects/nf-core/scrnaseq/4.2.0/download_test_data.sh /tmp/scrnaseq_test
depictio ingest /tmp/scrnaseq_test --template nf-core/scrnaseq/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/scrnaseq](https://nf-co.re/scrnaseq): official pipeline documentation
- [nf-co.re/scrnaseq/4.2.0/results](https://nf-co.re/scrnaseq/4.2.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/scrnaseq releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
