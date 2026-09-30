---
title: Multiplexed Tissue Imaging
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/mcmicro" target="_blank" title="nf-core/mcmicro on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_dark.png" alt="nf-core/mcmicro">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_light.png" alt="nf-core/mcmicro">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Multiplexed Tissue Imaging</h1>
    <p class="template-subtitle">Multi-cycle immunofluorescence from the input checks to the cells: each sample's registered whole-slide image with its segmentation mask and MCQUANT cells drawn over it, the marker panel read across cells and samples, and two segmentation modules compared on the same image.</p>
    <p class="template-links">
      <a href="https://nf-co.re/mcmicro" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/mcmicro" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="2.0.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="2.0.0" selected>2.0.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The mcmicro template reads a multiplexed imaging run (CyCIF, CODEX, mIHC) where
the unit is one cell of one sample, measured on every marker of the panel. It
is a paper-companion dashboard, easy to deploy, that sits next to dedicated
image viewers rather than replacing them: every tile reads what the run
published, and nothing is re-segmented or re-quantified.

- ![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } **MultiQC**: the pipeline's own consistency checks on every sample's OME-XML and samplesheet
- :material-view-dashboard-outline: **Slide overview**: cells per sample and segmentation module, and how bright each marker is in each sample
- :material-microscope: **Image and cells**: the registered image with its mask and one point per cell, the cell table and a cell record
- :material-chart-bell-curve: **Markers**: the panel read across cells, the marker by sample heatmap, the marker components and a two-group comparison
- :material-shield-check-outline: **Segmentation QC**: how two segmentation modules differ on the same image

A `Run at a glance` strip (samples by design group, cells segmented, markers
quantified, cell area), the collapsed `Sample sheet` and the `Sample filters`
(sample, design group) are pinned to every tab, and the acquisition table of
every sample and cycle is pinned, collapsed, at the bottom.

!!! info "One segmentation module drives the image"
    mcmicro can run several segmentation modules at once, and a label value is a
    cell id only within its own mask. `SEGMENTER` picks the module whose mask and
    cells the Image and cells and Markers tabs read, and `COMPARE_SEGMENTER` the
    one drawn in the Segmentation QC tab's second viewer. The pipeline's own
    default module is `mccellpose`: pass `--var SEGMENTER=mccellpose` for such a
    run.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/mcmicro/latest \
      --data-root /path/to/mcmicro_results \
      --var METADATA_FILE=/path/to/design.tsv
    ```

    mcmicro does not publish the samplesheet or the marker sheet it ran on, so
    copy them under `input/` in the results. The design table is optional:
    without it every sample falls in one group, `all`.

    | Variable | Default | Role |
    |---|---|---|
    | `SAMPLESHEET_FILE` | `{DATA_ROOT}/input/` | The cycle samplesheet the run was launched with (`--input_cycle`) |
    | `SEGMENTER` | `mesmer` | Segmentation module whose mask and cells the Image and cells and Markers tabs show |
    | `COMPARE_SEGMENTER` | `cellpose` | Second module, drawn in the Segmentation QC tab's viewer; skipped when the run did not use it |
    | `METADATA_FILE` | none | Design table (TSV): sample id in `METADATA_ID_COL`, one column per factor |
    | `METADATA_ID_COL` | first column | Design table sample id column |
    | `GROUP_COL` | first factor column | Design factor carried as the `condition` column of the sample hub |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/mcmicro -r 2.0.0 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the ASHLAR registered image of every sample (a pyramidal
OME-TIFF, read tile by tile), the segmentation masks of every module as label
images, the MCQUANT single-cell tables and the pipeline's input checks. The
masks are matched back to their sample through the decorated file names the
segmenters write, and a label value is the MCQUANT `CellID`, so the cell
table's colour column, filters and lasso reach the labels. Two derived columns
make the cell table readable without knowing the panel: the dominant marker of
each cell (the non-nuclear marker furthest above its median in the same
sample) and the first two components of the standardised marker intensities.
The long per-marker table is capped per sample and module, taking every k-th
cell, so a whole-slide run keeps a distribution table of a readable size; the
per-cell table keeps every cell.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. Background subtraction, illumination
    correction and TMA dearraying are off by default in the pipeline, and a
    single-module run leaves the comparison viewer empty.

<div class="tpl-version-block" data-version="2.0.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/mcmicro-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Five tabs, read as a funnel: whether the inputs were consistent, what each slide
yielded, the image itself with its cells, the marker panel across cells, and
how the segmentation modules differ. Each tab below carries the **same icon and
colour the dashboard gives it**. The heatmap, record and group comparison tiles
are described in
[Advanced Visualizations](../../features/components.md#advanced-visualizations).

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    *Was every sample's input consistent before stitching?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mcmicro/multiqc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/multiqc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mcmicro/multiqc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/multiqc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Before stitching, mcmicro reads every raw cycle image's OME-XML and the
    samplesheet and checks tile size, pixel size, channel count, data type and
    exposure times for consistency. The tab shows that pass, warn and fail
    matrix, one column per sample: a warning here explains a stitching or
    intensity problem further down the funnel. The acquisition parameters
    behind it are the pinned reference table at the bottom of every tab.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and the design group on the sample hub,
        persistent and pinned to the top of every tab, plus a `Cycles imaged`
        range in the tab-local *Input scope*.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Sample sheet*, collapsed and pinned to every tab |
        | Input checks | *Input check matrix* |
        | Reference tables | *Acquisition per sample and cycle*, collapsed and pinned to the bottom of every tab |

=== ":material-view-dashboard-outline:{ .mc-teal } Slide overview"

    *How many cells did each slide yield, and how bright is each marker in it?*

    [![Slide overview dashboard](../../images/pipeline-templates/nf-core/mcmicro/slide_overview_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/slide_overview_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Slide overview dashboard](../../images/pipeline-templates/nf-core/mcmicro/slide_overview_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/slide_overview_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The cards count the segmentation modules, the cells of every module, the
    dominant markers and the marker intensity spread. Grouped bars put cells per
    sample next to each other module by module, a box plot draws the log1p
    intensity per sample of the markers picked in the tab filters, and a last
    chart counts the cells per dominant marker. When background subtraction
    ran, the channel sheet of the corrected image is a collapsed table.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Segmentation module` and `Marker` in the tab-local
        *Overview filters*.

        | Section | What it holds |
        |---|---|
        | Cells per sample | 4 cards, *Cells per sample and segmentation module* |
        | Marker intensities | *Marker intensity per sample*, *Cells per dominant marker* |
        | Channel sheet | *Channels of the corrected image*, collapsed |

=== ":material-microscope:{ .mc-indigo } Image and cells"

    *Where are the cells, and what does each one express?*

    [![Image and cells dashboard](../../images/pipeline-templates/nf-core/mcmicro/image_and_cells_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/image_and_cells_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Image and cells dashboard](../../images/pipeline-templates/nf-core/mcmicro/image_and_cells_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/image_and_cells_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The bioimage viewer shows the registered image of the first sample picked in
    the sample filters, with the `SEGMENTER` mask drawn over it and one point
    per cell coloured by its dominant marker. The cell filters narrow the
    points and the table together. A lasso on the points narrows the
    full-width cell table below, and a row picked there opens the **Cell
    record**: position, shape and place on the marker components.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Dominant marker`, and `Cell area (pixels)` and
        `Eccentricity` ranges, in the tab-local *Cell filters*.

        | Section | What it holds |
        |---|---|
        | Cell map | *Registered image with mask and cells* |
        | Cells | *Cells on the map* |
        | Cell detail | *Cell record* |

=== ":material-chart-bell-curve:{ .mc-violet } Markers"

    *How does the panel read across cells, samples and design groups?*

    [![Markers dashboard](../../images/pipeline-templates/nf-core/mcmicro/markers_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/markers_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Markers dashboard](../../images/pipeline-templates/nf-core/mcmicro/markers_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/markers_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    One box per marker of log1p intensity, nuclear stains coloured apart, then
    the marker by sample heatmap of median log1p intensity. The cells sit on
    their first two marker components, lasso-enabled, and can be coloured by
    any column from the tile header. The group comparison runs a Wilcoxon test
    on log1p intensity, marker by marker: it opens on two levels of the design
    group and switches to two saved cell selections once they exist.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Marker`, `Marker or nuclear stain` and `Dominant marker`
        in the tab-local *Marker filters*.

        | Section | What it holds |
        |---|---|
        | Marker distributions | *Intensity per marker*, *Median marker intensity per sample* |
        | Marker space | *Cells on the first two marker components* |
        | Compare groups | *Markers between two groups of cells* |

=== ":material-shield-check-outline:{ .mc-cyan } Segmentation QC"

    *Do the segmentation modules agree on the same image?*

    [![Segmentation QC dashboard](../../images/pipeline-templates/nf-core/mcmicro/segmentation_qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/segmentation_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Segmentation QC dashboard](../../images/pipeline-templates/nf-core/mcmicro/segmentation_qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mcmicro/segmentation_qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Cells per module and the median area, eccentricity and solidity as cards,
    then area and eccentricity per module as boxes and a parallel-coordinates
    view with one line per sample and module across cell count and median
    shape. A second viewer draws the `COMPARE_SEGMENTER` mask and cells over the
    same registered image, coloured by area. The per-sample roll-up table
    drives a linked **Sample and module record** below it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Segmentation module`, and `Cell area (pixels)` and
        `Solidity` ranges, in the tab-local *Segmentation filters*.

        | Section | What it holds |
        |---|---|
        | Module agreement | 4 cards, *Cell area per module*, *Cell eccentricity per module*, *Sample and module profiles* |
        | Second segmentation | *Registered image with the second module's mask* |
        | Per-sample roll-up | *Cells and shape per sample and module* |
        | Segmentation detail | *Sample and module record* |

Tables and point views select on their entity column: the sample sheet on the
sample, the cell map, the marker components and the cell table on the cell,
and the roll-up table on the sample and module. The sample filters reach every
table through the project links.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/mcmicro, it does not run the pipeline.
Run the pipeline first, with every segmentation module you want to compare in
`--segmentation`:

```bash
nextflow run nf-core/mcmicro -r 2.0.0 \
  --input_cycle samplesheet.csv \
  --marker_sheet markers.csv \
  --segmentation mesmer,cellpose \
  --outdir results -profile docker
```

Then copy the samplesheet and the marker sheet under `input/` and point
Depictio at the results. mcmicro 2.0.0 ships a MultiQC parquet, so no reprocess
step is needed:

```bash
mkdir -p results/input && cp samplesheet.csv markers.csv results/input/
depictio run --template nf-core/mcmicro/latest --data-root results/
```

See [nf-co.re/mcmicro/usage](https://nf-co.re/mcmicro/2.0.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name; the segmentation module is read off the
directory path.

```text
<DATA_ROOT>/
├── input/                                    # samplesheet, marker sheet, design: copied in
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── multiqc/multiqc_data/multiqc.parquet      # the input checks
├── registration/ashlar/<sample>.ome.tif      # pyramidal OME-TIFF, the image
├── segmentation/<module>/<sample>*.tif       # integer label masks
├── quantification/mcquant/<module>/*.csv     # one row per cell, one column per marker
├── backsub/                                  # optional (--backsub)
├── illumination_correction/basicpy/          # optional (--illumination basicpy)
└── tma_dearray/                              # optional (--tma_dearray)
```

The raw cycle images are pipeline inputs and are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 2.0.0 release,
`results-f4400001578642e370a72668966c6602fe172ef6`, on its `test_full` profile:
two samples of two cycles each, BaSiCPy illumination correction, background
subtraction, and Mesmer and Cellpose segmentation quantified by MCQUANT. The
screenshots above come from that run. The whole results prefix is small, so
every image and mask is fetched. The run publishes no samplesheet, marker sheet
or design table, so the template ships them and the download script output says
how to copy them under `input/`:

```bash
DEST=/tmp/mcmicro_test
bash depictio/projects/nf-core/mcmicro/2.0.0/download_test_data.sh "$DEST"
mkdir -p "$DEST/input" && cp depictio/projects/nf-core/mcmicro/2.0.0/input/* "$DEST/input/"
depictio run --template nf-core/mcmicro/latest --data-root "$DEST" \
  --var METADATA_FILE="$DEST/input/metadata.tsv"
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it Experimental.</span>
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
