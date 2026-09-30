---
title: Cell Painting Profiling
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/cellpainting" target="_blank" title="nf-core/cellpainting on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/cellpainting/master/docs/images/nf-core-cellpainting_logo_dark.png" alt="nf-core/cellpainting">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/cellpainting/master/docs/images/nf-core-cellpainting_logo_light.png" alt="nf-core/cellpainting">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Cell Painting Profiling</h1>
    <p class="template-subtitle">A Cell Painting screen from the plate to the perturbations: cells segmented per well and site, image focus, saturation and illumination, the CellProfiler segmentation images, per-well morphological profiles and a feature-by-feature comparison of two groups, keyed on the plate map.</p>
    <p class="template-links">
      <a href="https://nf-co.re/cellpainting" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/cellpainting" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="1.0.0dev">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="1.0.0dev" selected>1.0.0dev</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

!!! warning "Built on an unreleased pipeline"
    nf-core/cellpainting has no release yet. The template lives in a
    `1.0.0dev/` directory and follows the `dev` branch pinned at commit
    `40423f0d1da0dde52bd5f1fd812ee6a1549cdfb3`, validated on the AWS megatest
    of that commit. Output paths may still change before the first release.
    The directory name is not a numeric version, so `nf-core/cellpainting/latest`
    does not resolve to it: name `nf-core/cellpainting/1.0.0dev` in full.

The cellpainting template reads a Cell Painting screen where the unit is one
cell of one site of one well, and every panel is keyed on the plate map. It is
a paper-companion dashboard, easy to deploy, that sits next to dedicated image
viewers rather than replacing them: the segmentation images sit beside the
per-cell tables, the QC and the filters.

- :material-microscope: **Overview**: the plate layout of cells segmented per well, cells per well by group, and the per-well profile table
- :material-check-decagram: **Plate QC**: cells per site, focus and saturation per channel, illumination correction and the segmented object shapes
- :material-image-multiple-outline: **Images**: the segmentation overlays and outlines CellProfiler wrote, as a gallery
- :material-chart-scatter-plot: **Profiles**: feature distributions, the well by feature heatmap of robust z-scores and the single-cell PCA
- :material-scale-balance: **Perturbations**: per-group summaries and a feature-by-feature comparison of two groups

A `Run at a glance` strip (wells by group, cells segmented, sites imaged, cells
per site), the collapsed `Plate map` and the `Well filters` (well, group) are
pinned to every tab.

!!! info "A curated feature set"
    CytoTable writes thousands of measurements per cell. The template reads a
    curated subset at read time, so a full plate never loads the full width:
    one to three features per family and compartment (size and shape, DNA
    content, stain intensities, texture, granularity, colocalisation,
    perinuclear mitochondria and crowding). A run with a custom analysis
    pipeline that does not measure one of them fails with an error naming the
    missing column.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio-cli images push /path/to/cellpainting_results \
      s3://depictio-bucket/nf-core-cellpainting/ --extensions .png
    depictio run \
      --template nf-core/cellpainting/1.0.0dev \
      --data-root /path/to/cellpainting_results \
      --var METADATA_FILE=/path/to/platemap.csv
    ```

    The pipeline takes no plate map and publishes none, so the template reads
    the screen's plate map from `METADATA_FILE`. It needs a plate and a well
    column (`plate` and `well`, or the JUMP `Metadata_Plate` and
    `Metadata_Well`); every other column is kept. A well imaged but absent from
    the plate map is kept, in group `Not in plate map`. The segmentation PNGs
    are not copied by the ingest: push them once, as above, before the run.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | `{DATA_ROOT}/input/platemap.csv` | The screen's plate map, CSV or TSV, one row per well |
    | `METADATA_ID_COL` | `well_id` | Recorded only: the hub joins on `well_id`, built from the plate and well columns |
    | `GROUP_COL` | `pert_type` | Plate map column wells are grouped by; the default follows the JUMP Cell Painting convention |
    | `GROUP_COL_DISPLAY` | `Perturbation type` | Reader-facing label of `GROUP_COL` in filter and chart titles |
    | `IMAGES_S3_BASE` | `s3://depictio-bucket/nf-core-cellpainting/` | S3 prefix the segmentation PNGs were pushed to |

    The Nextflow trigger resolves a template from the pipeline's manifest
    version, which a development directory does not match: for this template,
    run `depictio run` with the template named.

---

## :material-book-open-variant: Reference

The template reads the CytoTable Parquet file of every site, the CellProfiler
image quality table, the illumination correction functions and the
segmentation PNGs, and joins them to the plate map. Every collection is keyed
on the well (`<plate>_<well>`), with the site and the cell below it, all read
off the CytoTable file names; wells are normalised to a row letter and a
two-digit column on both sides. Per site and per well, counts and medians over
the cells follow the pycytominer `aggregate` convention. Well z-scores are
robust (median and MAD over every well of the run, not over negative
controls), and the PCA runs on every curated feature, standardised. The
illumination functions are reduced to the mean correction factor in rings from
the field centre to the corners.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. The image quality table, the
    illumination functions and the segmentation images are optional
    collections.

<div class="tpl-version-block" data-version="1.0.0dev" markdown>

--8<-- "pipeline-templates/nf-core/_generated/cellpainting-1.0.0dev.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Five tabs, read as a funnel: where the cells are on the plate, which sites and
channels to trust, the segmentation by eye, the morphological profile, and what
separates the perturbation groups. Each tab below carries the **same icon and
colour the dashboard gives it**. The plate heatmap, scatter, record and group
comparison tiles are described in
[Advanced Visualizations](../../features/components.md#advanced-visualizations).

=== ":material-microscope:{ .mc-teal } Overview"

    *Where are the cells on the plate?*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/cellpainting/overview_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/overview_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/cellpainting/overview_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/overview_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The plate layout draws cells segmented per well, plate rows down and plate
    columns across, with wells not imaged left empty; an edge or a corner that
    stands out points at a plate effect rather than a perturbation. Cells per
    well are coloured by group beside it. The per-well profile table drives a
    linked **Well record** next to it.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Well` and the plate map group on the well hub,
        persistent and pinned to the top of every tab, plus a `Cells per well`
        range in the tab-local *Well scope*.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Plate map | *Plate map*, collapsed and pinned to every tab |
        | Plate layout | *Cells segmented per well, plate layout*, *Cells segmented per well* |
        | Well detail | *Per-well profiles*, *Well record* |

=== ":material-check-decagram:{ .mc-blue } Plate QC"

    *Which sites and channels can be trusted?*

    [![Plate QC dashboard](../../images/pipeline-templates/nf-core/cellpainting/plate_qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/plate_qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Plate QC dashboard](../../images/pipeline-templates/nf-core/cellpainting/plate_qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/plate_qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Four site-level cards (nucleus and cell area, nuclear DNA, touching cells),
    then cells per site by well and cell count against nucleus size per site,
    lasso-enabled: a site far from the cloud is out of focus, empty or
    overcrowded. Focus (the power log-log slope) and saturation per channel
    come next, then the illumination correction from the field centre to the
    corners and its range per channel. The nucleus against cell area scatter of
    every cell shows whether the segmentation split or merged cells, and the
    site table drives a linked **Site record**.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Cells per site` range and `Channel` in the tab-local
        *Site scope*.

        | Section | What it holds |
        |---|---|
        | Cells per site | 4 cards, *Cells per site, by well*, *Cell count against nucleus size, per site* |
        | Image quality | *Blur per channel*, *Saturation per channel* |
        | Illumination correction | *Illumination correction, centre to corner*, *Correction range per channel* |
        | Segmentation | *Nucleus area against cell area* |
        | Site detail | *Per-site summary*, *Site record* |

=== ":material-image-multiple-outline:{ .mc-cyan } Images"

    *Does the segmentation look right by eye?*

    [![Images dashboard](../../images/pipeline-templates/nf-core/cellpainting/images_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/images_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Images dashboard](../../images/pipeline-templates/nf-core/cellpainting/images_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/images_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The segmentation images as a gallery: the assay-development object overlay
    of each well and, where published, the per-site outlines, narrowed by the
    pinned well and group filters and by image kind. The gallery reads the PNGs
    pushed under `IMAGES_S3_BASE`, and stays empty until they are pushed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Image kind` in the tab-local *Image scope*.

        | Section | What it holds |
        |---|---|
        | Segmentation images | 4 cards, *Segmentation overlays* |
        | Image list | *Image files*, collapsed |

=== ":material-chart-scatter-plot:{ .mc-violet } Profiles"

    *How do the wells differ, feature by feature?*

    [![Profiles dashboard](../../images/pipeline-templates/nf-core/cellpainting/profiles_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/profiles_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Profiles dashboard](../../images/pipeline-templates/nf-core/cellpainting/profiles_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/profiles_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The DNA content histogram reads the cell cycle (a 2N and a 4N peak), and
    cell area per well shows wells whose cells changed size. The well by feature
    heatmap of robust z-scores is annotated by group, so wells of one group that
    share a pattern cluster together. The single-cell PCA places every cell in
    feature space, and the cell table sits collapsed below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · a `Cell area (pixels)` range in the tab-local *Cell
        scope*.

        | Section | What it holds |
        |---|---|
        | Feature distributions | 4 cards, *DNA content per cell*, *Cell area per well* |
        | Well profiles | *Well x feature profile (robust z-scores)* |
        | Cell embedding | *Single-cell PCA* |
        | Cell table | *Single cells*, collapsed |

=== ":material-scale-balance:{ .mc-grape } Perturbations"

    *Which features separate two groups of wells?*

    [![Perturbations dashboard](../../images/pipeline-templates/nf-core/cellpainting/perturbations_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/perturbations_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Perturbations dashboard](../../images/pipeline-templates/nf-core/cellpainting/perturbations_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/cellpainting/perturbations_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Wells and cells per group, and the well medians of cell area and DNA
    content by group, then the two-group comparison: a Wilcoxon test per
    curated feature between the cells of two groups (plate map groups or saved
    selections), Benjamini-Hochberg corrected, drawn as a volcano. Cells of one
    well are not independent observations, so it ranks features to look at; it
    does not test the perturbation.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the plate map group of the cells, in the tab-local
        *Comparison scope*.

        | Section | What it holds |
        |---|---|
        | Per-group summaries | 4 cards, *Cell area by group*, *DNA content by group* |
        | Compare two groups | *Group A against group B, feature by feature* |

Tables and point views select on their entity column: the plate map and the
well table on the well, the site scatter and the site table on the site, and
the cell views on the cell. The well filters reach every collection through
the well key.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/cellpainting, it does not run the
pipeline. Run the pipeline first, on the commit the template was validated on:

```bash
nextflow run nf-core/cellpainting -r 40423f0d1da0dde52bd5f1fd812ee6a1549cdfb3 \
  --input samplesheet.csv \
  --outdir results -profile docker
```

`-r dev` follows the development branch instead. Then push the segmentation
images, copy the plate map under `input/` and point Depictio at the results.
The MultiQC report of this commit carries run metadata only, so there is no
MultiQC tab:

```bash
mkdir -p results/input && cp platemap.csv results/input/
depictio-cli images push results/ s3://depictio-bucket/nf-core-cellpainting/ --extensions .png
depictio run --template nf-core/cellpainting/1.0.0dev --data-root results/
```

See [nf-co.re/cellpainting](https://nf-co.re/cellpainting) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name; the batch, plate, well and site are read
off the CytoTable file names.

```text
<DATA_ROOT>/
├── input/platemap.csv                                  # the hub: copied in, not published
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── cytotable/<batch>_<plate>_<well>_<site>.parquet     # one row per cell
└── cellprofiler/
    ├── illumination_correction/**/<plate>_Illum<channel>.npy   # optional
    ├── assay_development/**/*_ObjectOverlay.png                 # optional, one per well
    └── analysis/**/                                             # optional
        ├── Image.csv                                            # focus and saturation
        └── *--{cell,nuclei}_outlines.png
```

The raw TIFF stacks are pipeline inputs, read from the image bucket, and are
not read. The run publishes no pyramidal image, so there is no bioimage viewer
on this template.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the pinned development
commit, `results-40423f0d1da0dde52bd5f1fd812ee6a1549cdfb3`, on its `test_full`
profile: one JUMP Cell Painting plate, four wells of nine sites and eight
channels. The screenshots above come from that run. On this commit the analysis
step is published flat rather than in one directory per site, so its image
quality table and outline images hold one site only; the per-cell data of every
site is intact in `cytotable/`, which the profiles use. The pipeline takes no
plate map, so the template ships the plate map of the imaged wells and the
download script copies it under `input/`:

```bash
DEST=/tmp/cellpainting_test
bash depictio/projects/nf-core/cellpainting/1.0.0dev/download_test_data.sh "$DEST"
depictio-cli images push "$DEST" s3://depictio-bucket/nf-core-cellpainting/ --extensions .png
depictio run --template nf-core/cellpainting/1.0.0dev --data-root "$DEST"
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/cellpainting](https://nf-co.re/cellpainting): official pipeline documentation
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
    <span class="tpl-credit-note">Keep it working as nf-core/cellpainting releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
