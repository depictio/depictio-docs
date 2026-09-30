---
title: Spatial Omics Segmentation
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/sopa" target="_blank" title="nf-core/sopa on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/sopa/master/docs/images/nf-core-sopa_logo_dark.png" alt="nf-core/sopa">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/sopa/master/docs/images/nf-core-sopa_logo_light.png" alt="nf-core/sopa">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Spatial Omics Segmentation</h1>
    <p class="template-subtitle">Segmented cells of any spatial omics technology sopa reads, over the tissue: the morphology image of each SpatialData store with its cells, per-sample cell yield and area, cluster and cell-type composition, a chosen gene list per cluster, and the segmentation method's own per-cell QC.</p>
    <p class="template-links">
      <a href="https://nf-co.re/sopa" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/sopa" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.0.1">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="1.0.1" selected>1.0.1</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

!!! warning "Validated on synthetic outputs only"
    The AWS megatest of 1.0.1 cannot be read: its per-sample `.zarr` store is a
    dangling symlink and the explorer image is JPEG 2000. The template was
    written from the pipeline's documented layout and test snapshots and
    checked on a synthetic run of sopa on its toy dataset. The `test` and
    `test_full` runs on a cluster are pending, which keeps the template a
    Draft.

The sopa template reads one SpatialData store per sample, where the unit is one
segmented cell, whatever the technology (Xenium, MERSCOPE, CosMx, Visium HD,
PhenoCycler, MACSima, H&E). It is a paper-companion dashboard, easy to deploy,
that sits next to dedicated image viewers rather than replacing them: sopa's
own Xenium Explorer files remain the place for transcript-level inspection.

- :material-view-dashboard-outline: **Overview**: cells per sample, cell area and transcripts per cell per sample
- :material-microscope: **Tissue and cells**: the morphology image with one point per cell, the cell table and a cell record
- :material-dna: **Clusters and genes**: cluster and cell-type composition per sample, and the chosen genes per cluster
- :material-shape-outline: **Segmentation**: cell size per cluster and Proseg's own per-cell readings

A `Run at a glance` strip (samples, cells segmented, cell area, clusters), the
collapsed `Sample sheet` and the `Sample filters` (sample, condition) are
pinned to every tab.

!!! info "No gene is chosen for you"
    A spatial panel has hundreds of genes, or the whole transcriptome, and no
    gene is a sensible default across tissues and technologies. The run names
    its genes through `GENES`, typically the lineage markers of the tissue or
    the genes of the paper's figures. Without it the gene tiles are left out.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/sopa/latest \
      --data-root /path/to/sopa_results \
      --var IMAGE_ELEMENT=morphology_focus \
      --var GENES=GENE1,GENE2,GENE3
    ```

    `IMAGE_ELEMENT` names the morphology image inside each store, which the
    technology reader sets; the store's root attribute
    `cell_segmentation_image` names it too.

    | Variable | Default | Role |
    |---|---|---|
    | `IMAGE_ELEMENT` | `image` | Image element the viewer shows and the cell coordinates refer to: `morphology_focus` on Xenium, `<dataset_id>_full_image` on Visium HD, `image` on the toy dataset |
    | `GENES` | unset | Comma-separated gene names, as in the cell table's var names, read for the Clusters and genes tab |
    | `METADATA_FILE` | none | Design table (TSV), one row per sample |
    | `METADATA_ID_COL` | first column | Design table sample id column |
    | `GROUP_COL` | first factor column | Design factor carried as the `condition` column of the sample hub |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/sopa -r 1.0.1 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

Every collection reads the `<sample>.zarr` stores: sopa writes no per-cell
table outside them. The cell table is read with its `obs` columns, and the
cell coordinates are converted into the pixels of the morphology image, so the
points land on the image without any scale setting. What `obs` carries depends
on the run's options (Leiden with scanpy preprocessing, a cell type with
fluorescence annotation, and each segmentation method's own columns), so the
template folds it onto one schema: the cluster is Leiden when it ran, else the
method's own clustering, else empty. sopa numbers the cells of every store from
the same start, so a run-wide cell key joins the sample and the cell id. Cell
area is in the units of the boundaries: image pixels for Cellpose and
StarDist, microns for the transcript-based methods.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. Without `GENES` the gene collections
    are pruned, and the Proseg readings only fill on a Proseg run.

<div class="tpl-version-block" data-version="1.0.1" markdown>

--8<-- "pipeline-templates/nf-core/_generated/sopa-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Four tabs, read as a funnel: what each sample yielded, the cells over the
tissue, what the cells are, and whether the cells are cells. Each tab below
carries the **same icon and colour the dashboard gives it**. The dot plot,
scatter and record tiles are described in
[Advanced Visualizations](../../features/components.md#advanced-visualizations).

=== ":material-view-dashboard-outline:{ .mc-teal } Overview"

    *What did each sample yield?*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/sopa/overview_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/overview_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/sopa/overview_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/overview_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Cells per sample from the sample hub, then cell area and transcripts per
    cell per sample. Transcripts per cell is filled only when the cell table
    carries a per-cell count (Baysor writes one); on a Proseg, Cellpose or
    StarDist run it stays empty.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and `Condition` on the sample hub, persistent
        and pinned to the top of every tab, plus a `Cells per sample` range and
        `Segmentation method` in the tab-local *Sample scope*.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Sample hub*, collapsed and pinned to every tab |
        | Cell yield | *Cells per sample*, *Cell area per sample*, *Transcripts per cell* |

=== ":material-microscope:{ .mc-violet } Tissue and cells"

    *Where are the cells, and which cluster is where?*

    [![Tissue and cells dashboard](../../images/pipeline-templates/nf-core/sopa/tissue_and_cells_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/tissue_and_cells_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Tissue and cells dashboard](../../images/pipeline-templates/nf-core/sopa/tissue_and_cells_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/tissue_and_cells_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The bioimage viewer shows the morphology image of the first sample picked
    in the sample filters, with every cell as a point at its centroid coloured
    by cluster. sopa writes the segmentation as shapes, which the viewer does
    not draw yet, so the cells are points rather than outlines. A lasso on the
    points narrows the cell table below, and a row picked there fills the
    **Cell record** at the end of the tab.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Cluster`, `Cell type` and a `Cell area` range in the
        tab-local *Cell filters*.

        | Section | What it holds |
        |---|---|
        | Tissue | *Morphology image and segmented cells* |
        | Cells | *Cell table* |
        | Cell detail | *Cell record* |

=== ":material-dna:{ .mc-indigo } Clusters and genes"

    *What are the cells, and which genes mark each cluster?*

    [![Clusters and genes dashboard](../../images/pipeline-templates/nf-core/sopa/clusters_and_genes_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/clusters_and_genes_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Clusters and genes dashboard](../../images/pipeline-templates/nf-core/sopa/clusters_and_genes_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/clusters_and_genes_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Cluster and cell-type composition per sample, as a percent of the sample's
    cells, with the most abundant labels of the run kept and the rest pooled
    as Other; a run that computed neither reads `unassigned`. With `GENES`, a
    marker dot plot draws mean expression and the share of expressing cells
    per cluster, and a box plot the per-cell expression by cluster.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Cluster or cell type` and `Gene` in the tab-local
        *Cluster scope*.

        | Section | What it holds |
        |---|---|
        | Composition | *Cluster and cell type composition* |
        | Marker genes | *Marker dot plot*, *Expression per cluster* |

=== ":material-shape-outline:{ .mc-orange } Segmentation"

    *Are the segmented cells real cells?*

    [![Segmentation dashboard](../../images/pipeline-templates/nf-core/sopa/segmentation_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/segmentation_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Segmentation dashboard](../../images/pipeline-templates/nf-core/sopa/segmentation_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/sopa/segmentation_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Cell area per cluster first: a cluster of tiny or huge cells is more often
    an artefact than a cell type. Then Proseg's own readings: volume, surface
    area, their ratio (high for thin or fragmented cells) and the expression
    scale, as cards, a volume against surface area scatter and the ratio per
    sample. The per-cell table sits collapsed below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Cell volume` and `Surface to volume` ranges in the
        tab-local *Segmentation scope*.

        | Section | What it holds |
        |---|---|
        | Cell size | *Cell area per cluster* |
        | Proseg readings | 4 cards, *Volume against surface area*, *Surface to volume per sample* |
        | Proseg cells | *Proseg per-cell readings*, collapsed |

Tables and point views select on their entity column: the sample sheet on the
sample, and the cell map and the cell table on the run-wide cell key, which
also narrows the gene and Proseg tiles.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/sopa, it does not run the pipeline.
Run the pipeline first, with the technology and segmentation options your data
needs (see the usage documentation below) and the default publish mode, which
writes real `.zarr` directories:

```bash
nextflow run nf-core/sopa -r 1.0.1 \
  --input samplesheet.csv \
  --outdir results -profile docker
```

Then point Depictio at the results, naming the image element and the genes to
read:

```bash
depictio run --template nf-core/sopa/latest --data-root results/ \
  --var IMAGE_ELEMENT=morphology_focus --var GENES=GENE1,GENE2
```

See [nf-co.re/sopa/usage](https://nf-co.re/sopa/1.0.1/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. The stores sit
at its top level, one per sample.

```text
<DATA_ROOT>/
├── pipeline_info/
│   ├── params*.json
│   └── *software*versions*.yml
├── <sample>.zarr/                       # SpatialData store
│   ├── images/<IMAGE_ELEMENT>/          # morphology image, multiscale
│   ├── shapes/<method>_boundaries/      # cell polygons, not read
│   ├── points/transcripts/              # not read
│   └── tables/table/                    # one row per cell
└── <sample>.explorer/                   # Xenium Explorer files, not read
```

The transcripts, the cell polygons, the UMAP and the per-cell channel means
are not read, nor is sopa's own QC report.

---

## :material-flask-outline: Validation runs

The AWS megatest of 1.0.1 cannot be used, so the template was checked on a
synthetic run: sopa on its toy dataset, three samples, the pipeline's `test`
steps run through the sopa command line (channel aggregation, fluorescence
annotation, scanpy preprocessing, explorer and report), with Proseg replaced by
the toy cells and the columns Proseg writes added. The screenshots above come
from that run. The reference runs, `-profile test` (the toy dataset) and
`-profile test_full` (a Visium HD run segmented with StarDist and Proseg), are
pending on a cluster.

Do not pass `--project-name` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/sopa](https://nf-co.re/sopa): official pipeline documentation
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
    <span class="tpl-credit-note">Keep it working as nf-core/sopa releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
