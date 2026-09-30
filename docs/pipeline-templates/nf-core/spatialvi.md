---
title: Visium Spatial Transcriptomics
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/spatialvi" target="_blank" title="nf-core/spatialvi on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/spatialvi/dev/docs/images/nf-core-spatialvi_logo_dark.png" alt="nf-core/spatialvi">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/spatialvi/dev/docs/images/nf-core-spatialvi_logo_light.png" alt="nf-core/spatialvi">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Visium Spatial Transcriptomics</h1>
    <p class="template-subtitle">10x Visium from the capture area to the clusters: Space Ranger QC per sample, the tissue image with its spots coloured by cluster, spatially variable genes ranked per sample, and the integrated clusters on the tissue, next to the MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/spatialvi" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/spatialvi" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.0.0dev">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="1.0.0dev" selected>1.0.0dev</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

!!! warning "Built on an unreleased pipeline, validated on synthetic outputs only"
    nf-core/spatialvi (formerly spatialtranscriptomics) has no release and no
    AWS megatest. The template lives in a `1.0.0dev/` directory and follows the
    `dev` branch pinned at commit `441ded53109f57ecf70555fb0b060546b34b4a2c`.
    It was checked on a synthetic run built from the test-datasets Space
    Ranger outputs; the `test` run on a cluster is pending, which keeps the
    template a Draft. The directory name is not a numeric version, so
    `nf-core/spatialvi/latest` does not resolve to it: name
    `nf-core/spatialvi/1.0.0dev` in full.

The spatialvi template reads a Visium run where the unit is one capture spot of
one sample, kept by the QC filter and clustered. It is a paper-companion
dashboard, easy to deploy, that sits next to dedicated image viewers rather
than replacing them.

- ![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } **MultiQC**: the Space Ranger curves, read quality and the spots and genes removed by the QC filter
- :material-shield-check-outline: **Space Ranger QC**: capture, sequencing and mapping metrics per sample, and the capture array
- :material-microscope: **Tissue & spots**: the tissue image with one point per kept spot coloured by cluster, the spot table and a spot record
- :material-waves: **Spatially variable genes**: spatial score against significance, the score per sample and the ranked genes
- :material-set-merge: **Integration**: the per-sample and integrated clusters, how they split across each other, and the integrated clusters on the tissue

A `Run at a glance` strip (samples, spots under tissue, reads sequenced,
spatially variable genes), the collapsed `Sample sheet` and the `Sample
filters` (sample, design group) are pinned to every tab. When `GENES` is set, a
second dashboard, **Genes on tissue**, colours the spots by the expression of
one picked gene and shows expression by cluster.

!!! info "One sample on the image"
    The SpatialData stores name their elements after the sample, and a
    collection reads one element path, so the Tissue & spots and Integration
    tabs show the sample named by `IMAGE_SAMPLE` only. The Space Ranger and
    spatially variable gene tabs cover every sample.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/spatialvi/1.0.0dev \
      --data-root /path/to/spatialvi_results \
      --var IMAGE_SAMPLE=<sample> \
      --var METADATA_FILE=/path/to/spatialvi_results/input/samplesheet.csv
    ```

    `IMAGE_SAMPLE` is spelt as the store names it: the sample id with every
    character other than letters, digits, `_` and `-` dropped. The pipeline's
    own samplesheet can serve as the design table once copied under `input/`.

    | Variable | Default | Role |
    |---|---|---|
    | `IMAGE_SAMPLE` | required | Sample whose tissue image and spots the Tissue & spots and Integration tabs read |
    | `INTEGRATION_METHOD` | `harmony` | Integration method of the run; names the integrated store |
    | `GENES` | unset | Comma-separated var names (gene ids of the reference) that add the Genes on tissue dashboard |
    | `METADATA_FILE` | unset | Design table (CSV): the pipeline samplesheet or any table keyed on the sample |
    | `METADATA_ID_COL` | `sample` | Design table sample column |
    | `GROUP_COL` | `slide` | Design column of the pinned group filter |
    | `GROUP_COL_DISPLAY` | `Slide` | Reader-facing label of `GROUP_COL` |

    The Nextflow trigger resolves a template from the pipeline's manifest
    version, which a development directory does not match: for this template,
    run `depictio run` with the template named.

---

## :material-book-open-variant: Reference

The template reads the Space Ranger metrics and spot positions of every
sample, the squidpy spatially variable gene tables, the merged and integrated
SpatialData stores and the MultiQC parquet. The hires tissue image of
`IMAGE_SAMPLE` is read from the merged store, and its spot table from the same
store and the integrated one. The stores' spatial coordinates are already in
hires pixels, so the spot tables read their position from the spot shapes,
which map to the image exactly. The stores use the reference's gene ids as
var names, not symbols, so `GENES` takes ids; for the same reason the
pipeline's mitochondrial prefix test finds no genes, and the mitochondrial
share reads 0.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. A run started from existing Space
    Ranger outputs has no FastQC panels.

<div class="tpl-version-block" data-version="1.0.0dev" markdown>

--8<-- "pipeline-templates/nf-core/_generated/spatialvi-1.0.0dev.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Five tabs, read as a funnel: the report, whether each capture area worked,
where the clusters sit in the tissue, which genes follow the tissue, and which
clusters the samples share. Each tab below carries the **same icon and colour
the dashboard gives it**. The scatter and record tiles are described in
[Advanced Visualizations](../../features/components.md#advanced-visualizations).

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Did the reads become spots?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/spatialvi/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/spatialvi/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Space Ranger's median genes per spot, sequencing saturation and genomic DNA
    curves, the FastQC read quality panels, and the spots and genes removed by
    the pipeline's QC filter.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and the design group on the sample hub,
        persistent and pinned to the top of every tab.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Sample sheet*, collapsed and pinned to every tab |
        | Space Ranger curves | *Median genes per spot*, *Sequencing saturation*, *UMIs from genomic DNA* |
        | Read quality | *Sequence counts*, *Per-sequence quality scores*, *GC content*, *Sequence duplication levels* |
        | Spot filtering | *Spots and genes removed by the QC filter* |

=== ":material-shield-check-outline:{ .mc-indigo } Space Ranger QC"

    *Did each capture area work?*

    [![Space Ranger QC dashboard](../../images/pipeline-templates/nf-core/spatialvi/space_ranger_qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/space_ranger_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Space Ranger QC dashboard](../../images/pipeline-templates/nf-core/spatialvi/space_ranger_qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/space_ranger_qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Genes, UMIs, saturation and tissue coverage per sample as cards, then depth
    against genes per spot and the share of reads mapped confidently. The
    capture array is drawn spot by spot, coloured by the tissue call, so a
    tissue detection that missed a fold or took in background shows at once.
    The metrics table drives a linked **Sample record** below it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Spots under tissue` range, `Assay` and `Tissue call`
        in the tab-local *Space Ranger filters*.

        | Section | What it holds |
        |---|---|
        | Capture and sequencing | 4 cards |
        | Depth and mapping | *Depth against genes per spot*, *Reads mapped confidently (%)* |
        | Capture area | *Capture array* |
        | Space Ranger metrics | *Space Ranger metrics* |
        | Sample detail | *Sample record* |

=== ":material-microscope:{ .mc-grape } Tissue & spots"

    *Where do the clusters sit in the tissue?*

    [![Tissue & spots dashboard](../../images/pipeline-templates/nf-core/spatialvi/tissue_spots_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/tissue_spots_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Tissue & spots dashboard](../../images/pipeline-templates/nf-core/spatialvi/tissue_spots_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/tissue_spots_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The bioimage viewer shows the hires tissue image of `IMAGE_SAMPLE`, with
    one point per kept spot coloured by Leiden cluster. A lasso narrows the
    spot table beside it, and a row opens the **Spot record** below. Spot QC
    follows: UMIs against genes per spot, and UMIs per spot by cluster, where a
    cluster of low-depth spots is more often a tissue edge than a region.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Leiden cluster`, and `UMIs per spot` and `Genes per
        spot` ranges, in the tab-local *Spot filters*.

        | Section | What it holds |
        |---|---|
        | Spots in numbers | 4 cards |
        | Tissue | *Tissue and spots*, *Spots* |
        | Spot QC | *UMIs against genes per spot*, *UMIs per spot by cluster* |
        | Spot detail | *Spot record* |

=== ":material-waves:{ .mc-cyan } Spatially variable genes"

    *Which genes follow the tissue layout?*

    [![Spatially variable genes dashboard](../../images/pipeline-templates/nf-core/spatialvi/spatially_variable_genes_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/spatially_variable_genes_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Spatially variable genes dashboard](../../images/pipeline-templates/nf-core/spatialvi/spatially_variable_genes_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/spatially_variable_genes_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    squidpy ranks the genes of each sample by spatial autocorrelation (Moran's
    I by default). The cards read the genes tested, the strongest and median
    spatial score and the statistic used; a scatter puts the spatial score
    against its significance, and a box plot the score per sample. The ranked
    gene table drives a linked **Gene record** below it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Significance`, a `Spatial score` range and a `Minimum
        -log10 q-value` slider in the tab-local *Gene filters*.

        | Section | What it holds |
        |---|---|
        | Genes in numbers | 4 cards |
        | Score distributions | *Spatial score against significance*, *Spatial score per sample* |
        | Ranked genes | *Ranked genes* |
        | Gene detail | *Gene record* |

=== ":material-set-merge:{ .mc-teal } Integration"

    *Which clusters do the samples share once integrated?*

    [![Integration dashboard](../../images/pipeline-templates/nf-core/spatialvi/integration_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/integration_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Integration dashboard](../../images/pipeline-templates/nf-core/spatialvi/integration_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/spatialvi/integration_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Spots per cluster and per sample, for the per-sample Leiden clusters and
    the clusters of the batch-corrected embedding (Harmony by default), picked
    with the Clustering control. A second chart shows how the per-sample
    clusters split across the integrated ones, and a second viewer draws the
    tissue coloured by integrated cluster. The composition table sits collapsed
    below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Clustering` and `Integrated cluster` in the tab-local
        *Cluster filters*.

        | Section | What it holds |
        |---|---|
        | Clusters in numbers | 4 cards |
        | Composition | *Spots per cluster (%)* |
        | Integrated clusters on tissue | *Integrated clusters on the tissue* |
        | Cluster agreement | *Per-sample clusters across integrated clusters* |
        | Composition table | *Cluster composition*, collapsed |

Tables and point views select on their entity column: the sample sheet and the
metrics table on the sample, the spot map and the spot table on the spot, and
the ranked gene table on the gene of one sample.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/spatialvi, it does not run the
pipeline. Run the pipeline first, on the commit the template was validated on:

```bash
nextflow run nf-core/spatialvi -r 441ded53109f57ecf70555fb0b060546b34b4a2c \
  --input samplesheet.csv \
  --outdir results -profile docker
```

`-r dev` follows the development branch instead. Then copy the samplesheet
under `input/` and point Depictio at the results:

```bash
mkdir -p results/input && cp samplesheet.csv results/input/
depictio run --template nf-core/spatialvi/1.0.0dev --data-root results/ \
  --var IMAGE_SAMPLE=<sample> \
  --var METADATA_FILE=results/input/samplesheet.csv
```

See [nf-co.re/spatialvi](https://nf-co.re/spatialvi) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name; the sample is read off the directory
path.

```text
<DATA_ROOT>/
├── input/samplesheet.csv                          # copied in, not published
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/multiqc_data/multiqc.parquet
├── <sample>/
│   ├── spaceranger/outs/
│   │   ├── metrics_summary.csv
│   │   └── spatial/tissue_positions.csv
│   └── data/<sample>_svg.csv                      # spatially variable genes
└── integration/data/
    ├── merged.zarr/                               # every sample's SpatialData elements
    └── <INTEGRATION_METHOD>.zarr/                 # the same with the integrated clusters
```

The AnnData files under `<sample>/data/` are not read. A sample id with a dot
loses it in the store's element names, and its spots then get no integrated
cluster.

---

## :material-flask-outline: Validation runs

nf-core/spatialvi has no release and no AWS megatest. The template was checked
on a synthetic run: the test-datasets Space Ranger outputs copied into two
samples, one of them with a dotted id, with the pipeline's own module scripts
(read, quality control, clustering, spatially variable genes and integration)
run outside Nextflow and MultiQC run on the result. The screenshots above come
from that run; it has no FASTQ files, so no FastQC panels. The reference run is
`-profile test` on a cluster, pending; the download script only fetches the
small test-datasets samplesheets:

```bash
DEST=/tmp/spatialvi_inputs
bash depictio/projects/nf-core/spatialvi/1.0.0dev/download_test_data.sh "$DEST"
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/spatialvi](https://nf-co.re/spatialvi): official pipeline documentation
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
    <span class="tpl-credit-note">Keep it working as nf-core/spatialvi releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
