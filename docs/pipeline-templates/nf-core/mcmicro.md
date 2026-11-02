---
title: Multiplexed tissue imaging
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/mcmicro" target="_blank" title="nf-core/mcmicro on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_dark.png" alt="nf-core/mcmicro">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_light.png" alt="nf-core/mcmicro">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Multiplexed tissue imaging</h1>
    <p class="template-subtitle">The input image checks, PNG previews of the registered images, how each segmentation method cuts them into cells, then where the cells sit, what they express and their size and shape.</p>
    <p class="template-links">
      <a href="https://nf-co.re/mcmicro" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/mcmicro" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="2.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="2.0.0" selected>2.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The mcmicro template follows an nf-core/mcmicro run from registered images to
single cells, one sample being one tissue image:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- ![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } **MultiQC**: the prelude's input image checks, per image
- :material-image-multiple-outline: **Previews**: PNG previews of the registered images and the mask outlines
- :material-shape-outline: **Segmentation**: cells per image and method, their areas, and how the methods agree
- :material-map-marker-radius-outline: **Spatial**: the cell map, coloured by marker, with the intensities of the selected cells
- :material-palette-outline: **Markers**: marker intensities per method and the marker correlation
- :material-shape-plus-outline: **Morphology**: cell area, eccentricity and solidity per method

The persistent `Sample filters` (group and image) sit in the collapsed left panel and
narrow every tab but MultiQC.

!!! warning "Early: the image tabs are a stand-in"
    Depictio has no OME-TIFF or zarr viewer yet, so the registered images and the
    mask outlines reach the dashboard as PNG previews written at fetch time by the
    template's `scripts/make_previews.py` (numpy, tifffile and Pillow). A run
    without `previews/` loses the Previews tab and the image under the cell map,
    nothing else:

    ```bash
    python depictio/projects/nf-core/mcmicro/2.0.0/scripts/make_previews.py <outdir> \
      --markers <outdir>/input/markers.csv
    ```

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/mcmicro_results \
      --template nf-core/mcmicro/latest \
      --var METADATA_FILE=/path/to/samplesheet.csv \
      --var MARKER_SHEET=/path/to/markers.csv
    ```

    mcmicro publishes neither its samplesheet nor its marker sheet. Copy them under
    `input/` in the data root (`input/samplesheet.csv`, `input/markers.csv`), where they
    are read by default, or pass the two variables. `GROUP_COL` defaults to `cycles`,
    the cycle count of the image; name a design column added to the sheet instead. For
    a run with one method in `--segmentation`, pass `--var SINGLE_SEGMENTER=true`.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/mcmicro -r 2.0.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the samplesheet, the marker sheet, the MultiQC report and the
MCQUANT tables, one per sample and segmenter, from which every cell-level
collection is built. The PNG previews are an optional Image collection, and so is
the segmenter agreement, which needs two methods in the run.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="2.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/mcmicro-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in two groups, read as a
funnel from the input images and their segmentation to the cells. Each tab below
carries the **same icon and colour the dashboard gives it**.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Previews, Segmentation |
| Cells | Spatial, Markers, Morphology |

=== ":material-compass-outline: Overview"

    *Multiplexed tissue imaging, from registered images to the cells and their markers.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/mcmicro/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/mcmicro/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A hero links the run parameters. *The run* lists the images, the channels quantified
    and the segmentation methods, and *Pipeline* walks five steps (check, register,
    subtract, segment, quantify), each linked to its parameters and its tab. Four key
    figures (images, cells, channels, median cell area) and the findings follow the
    filters.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Do the input tiles carry consistent image metadata?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mcmicro/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mcmicro/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The prelude's input image check matrix: a row per check (tile size, pixel size,
    channel count, data type, exposure), a column per image, pass or warning. The sample
    filters do not reach it, because its rows are checks, not samples.

=== ":material-image-multiple-outline:{ .mc-cyan } Previews"

    **Data & QC** · *What do the registered images and their masks look like?*

    [![Previews dashboard](../../images/pipeline-templates/nf-core/mcmicro/previews_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/previews_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Previews dashboard](../../images/pipeline-templates/nf-core/mcmicro/previews_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/previews_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A gallery of the previews: one grey image per channel, a composite and the mask
    outlines. Filters: stage and channel. The preview table with sizes and scale is
    collapsed.

=== ":material-shape-outline:{ .mc-blue } Segmentation"

    **Data & QC** · *How many cells does each method find, and do they agree?*

    [![Segmentation dashboard](../../images/pipeline-templates/nf-core/mcmicro/segmentation_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/segmentation_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Segmentation dashboard](../../images/pipeline-templates/nf-core/mcmicro/segmentation_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/segmentation_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Cells per image and method (log scale) beside the cell areas per method. Then the
    agreement between methods: per image, the share of one method's cells whose area
    holds the centroid of a cell of the other. Filter: segmenter.

=== ":material-map-marker-radius-outline:{ .mc-grape } Spatial"

    **Cells** · *Where do the cells sit, and what do they express?*

    [![Spatial dashboard](../../images/pipeline-templates/nf-core/mcmicro/spatial_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/spatial_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Spatial dashboard](../../images/pipeline-templates/nf-core/mcmicro/spatial_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/spatial_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The cell map: one point per cell, one image at a time, sized by its area and
    coloured by a marker picked in the tile or by the segmenter, over the nuclear-stain
    preview when the run has previews. A lasso selects cells and the box plot below
    shows their marker intensities. Filters: segmenter and cell area.

=== ":material-palette-outline:{ .mc-violet } Markers"

    **Cells** · *How bright is each marker, and which markers go together?*

    [![Markers dashboard](../../images/pipeline-templates/nf-core/mcmicro/markers_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/markers_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Markers dashboard](../../images/pipeline-templates/nf-core/mcmicro/markers_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/markers_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    One box per marker and method of the asinh intensities, and the marker correlation
    heatmap, clustered. Filters: marker, marker role and segmenter. The per-image marker
    table and the marker sheet are collapsed.

=== ":material-shape-plus-outline:{ .mc-orange } Morphology"

    **Cells** · *What size and shape are the cells?*

    [![Morphology dashboard](../../images/pipeline-templates/nf-core/mcmicro/morphology_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/morphology_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Morphology dashboard](../../images/pipeline-templates/nf-core/mcmicro/morphology_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/morphology_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Every cell by its area (log) and eccentricity, coloured by segmenter, then the area
    histogram per method beside the solidity per method. Filters: segmenter, area and
    eccentricity.

The sample sheet selects on `sample`, which reaches every per-image collection and the
previews. The cell map and the morphology scatter select on `cell_key`, which
reaches the per-cell marker intensities.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/mcmicro, it does not run the pipeline.
Run the pipeline first, with the cycle samplesheet and the marker sheet:

```bash
nextflow run nf-core/mcmicro -r 2.0.0 \
  --input_cycle samplesheet.csv --marker_sheet markers.csv \
  --segmentation mesmer,cellpose \
  -profile docker --outdir results
```

Then copy both sheets under `input/`, write the previews and point Depictio at the results:

```bash
mkdir -p results/input && cp samplesheet.csv markers.csv results/input/
python depictio/projects/nf-core/mcmicro/2.0.0/scripts/make_previews.py results/ \
  --markers results/input/markers.csv
depictio ingest results/ --template nf-core/mcmicro/latest
```

See [nf-co.re/mcmicro/usage](https://nf-co.re/mcmicro/2.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/
│   ├── samplesheet.csv                        # the hub: one row per image (METADATA_FILE)
│   └── markers.csv                            # the panel (MARKER_SHEET)
├── multiqc/multiqc_data/multiqc.parquet
├── quantification/mcquant/<segmenter>/*.csv   # MCQUANT, one table per image and method
├── registration/ashlar/*.ome.tif              # previews only
├── segmentation/                              # masks, previews only
├── previews/previews.tsv                      # optional, written by make_previews.py
└── pipeline_info/
    ├── params.json
    └── software_versions.yml
```

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 2.0.0 release,
`s3://nf-core-awsmegatests/mcmicro/results-f4400001578642e370a72668966c6602fe172ef6/`:
two samples from two cycles of a CyCIF tonsil test image, segmented with Mesmer
and Cellpose. The run does not publish its sheets, so the template vendors the
pipeline's own `samplesheet-test_full.csv` and `markers-test_full.csv` under
`input/`, and the download script copies them and writes the previews:

```bash
bash depictio/projects/nf-core/mcmicro/2.0.0/download_test_data.sh /tmp/mcmicro_test
depictio ingest /tmp/mcmicro_test --template nf-core/mcmicro/latest
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/mcmicro](https://nf-co.re/mcmicro): official pipeline documentation
- [nf-co.re/mcmicro/2.0.0/results](https://nf-co.re/mcmicro/2.0.0/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/mcmicro releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
