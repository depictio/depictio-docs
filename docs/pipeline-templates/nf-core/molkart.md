---
title: Molecular Cartography
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/molkart" target="_blank" title="nf-core/molkart on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/molkart/master/docs/images/nf-core-molkart_logo_dark.png" alt="nf-core/molkart">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/molkart/master/docs/images/nf-core-molkart_logo_light.png" alt="nf-core/molkart">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Molecular Cartography</h1>
    <p class="template-subtitle">Spot-based spatial transcriptomics from the spots to the cells: how many transcripts each segmentation method assigned, the contrast-enhanced tissue image with its labels and cells, per-cell and per-gene counts, and two segmentation methods compared on the same tissue.</p>
    <p class="template-links">
      <a href="https://nf-co.re/molkart" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/molkart" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="1.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="1.2.0" selected>1.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

!!! warning "Validated on synthetic outputs only"
    The AWS megatest of 1.2.0 publishes `pipeline_info/` and no per-sample
    output, so the template was written from the pipeline's documented layout
    and scripts and checked on a synthetic run built from the test-datasets
    inputs. The `test_full` run on a cluster is pending; until it is ingested,
    real file names and cell counts are unverified, which keeps the template a
    Draft.

The molkart template reads a Molecular Cartography run where the unit is one
cell of one sample under one segmentation method, with the transcripts
assigned to it. It is a paper-companion dashboard, easy to deploy, that sits
next to dedicated image viewers rather than replacing them.

- :material-shield-check-outline: **QC**: spot assignment per sample and method, the most detected genes before segmentation and the molkartqc table
- :material-microscope: **Tissue**: the contrast-enhanced image with the primary method's labels and one point per cell, the cell table and a cell record
- :material-dna: **Cell x gene**: the most abundant genes, breadth and level per sample, per-cell counts and a gene by sample heatmap
- :material-set-merge: **Segmentation comparison**: cells, areas and transcripts per method, and a second viewer with the comparison method's labels

A `Run at a glance` strip (samples by design group, spots kept, cells of the
primary method, panel genes), the collapsed `Sample sheet` and the `Sample
filters` (sample, design group) are pinned to every tab.

!!! info "One segmentation method per viewer"
    molkart can segment with several methods in one run, and label ids restart
    at 1 for every method, so each viewer reads one method only.
    `PRIMARY_SEGMENTATION` drives the Tissue and Cell x gene tabs, and
    `COMPARE_SEGMENTATION` the second viewer of the Segmentation comparison
    tab. Every method still lands in the QC table and in the comparison charts.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio run \
      --template nf-core/molkart/latest \
      --data-root /path/to/molkart_results \
      --var METADATA_FILE=/path/to/design.tsv
    ```

    molkart does not publish the samplesheet it ran on, so copy it under
    `input/` in the results. The design table is optional; without it the
    design filter and colouring are left out.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | none | Design table (TSV): sample id in `sample` or the first column, one column per factor |
    | `GROUP_COL` | first factor column | Design column of the pinned filter and the glance donut |
    | `PRIMARY_SEGMENTATION` | `mesmer` | Method whose labels and cells the Tissue and Cell x gene tabs show |
    | `COMPARE_SEGMENTATION` | `cellpose` | Method of the second viewer |
    | `SINGLE_SEGMENTATION` | unset | Set for a one-method run: drops the comparison viewer's collections |
    | `MEMBRANE_STACK` | unset | Set for membrane runs: the viewer reads the two-channel stack instead of the per-channel images |
    | `IMAGE_SAMPLE_PATTERN` | see the template | Regex giving the sample of an image file name |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio-cli config nextflow --install     # once per machine
    nextflow run nf-core/molkart -r 1.2.0 -profile docker --outdir results
    ```

    No `depictio run`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the contrast-enhanced image of every sample (a pyramidal
OME-TIFF), the filtered segmentation masks as label images, the spot2cell cell
by gene tables of every method, the molkartqc sheets and the Mindagap spot
tables with their duplicated spots marked. The label stores are the
**filtered** masks, whose label values are the cell ids spot2cell writes, so
the cells drawn over the image line up with their labels and with the table
rows. A cell id is unique within one sample and method only, so a combined key
joins the three for links and record cards. The MultiQC report of 1.2.0 holds
only the concatenated molkartqc sheets, which the template reads typed, so
there is no MultiQC tab.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. A one-method run with
    `SINGLE_SEGMENTATION` set drops the comparison viewer and its table.

<div class="tpl-version-block" data-version="1.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/molkart-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

Four tabs, read as a funnel: whether the spots were caught by cells, the
tissue cell by cell, the panel gene by gene, and how the segmentation methods
differ. Each tab below carries the **same icon and colour the dashboard gives
it**. The scatter, dot plot, heatmap and record tiles are described in
[Advanced Visualizations](../../features/components.md#advanced-visualizations).

=== ":material-shield-check-outline:{ .mc-teal } QC"

    *Were the cells kept, and did they catch the spots?*

    [![QC dashboard](../../images/pipeline-templates/nf-core/molkart/qc_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/qc_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![QC dashboard](../../images/pipeline-templates/nf-core/molkart/qc_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/qc_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The cards read the share of spots assigned to a cell, transcripts per cell,
    mean cell area and the share of spots duplicated along the tile grid lines.
    Bars compare spots assigned to cells per sample and method, and a scatter
    puts cells kept against spots assigned, one point per sample and method: a
    method that keeps many cells but catches few spots draws them too small.
    The most detected genes before segmentation come next, and the molkartqc
    table sits collapsed below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Sample` and the design group on the sample hub,
        persistent and pinned to the top of every tab, plus `Segmentation
        method` and a `Spots assigned (%)` range in the tab-local *QC filters*.

        | Section | What it holds |
        |---|---|
        | Run at a glance | 4 cards, pinned to every tab |
        | Sample sheet | *Sample hub*, collapsed and pinned to every tab |
        | Spot assignment | 4 cards, *Spots assigned to cells*, *Cells kept against spots assigned* |
        | Spot detection | *Most detected genes* |
        | QC table | *Spot assignment QC*, collapsed |

=== ":material-microscope:{ .mc-blue } Tissue"

    *Where are the cells, and which gene dominates each one?*

    [![Tissue dashboard](../../images/pipeline-templates/nf-core/molkart/tissue_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/tissue_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Tissue dashboard](../../images/pipeline-templates/nf-core/molkart/tissue_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/tissue_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The bioimage viewer shows the contrast-enhanced image of the first sample
    picked in the sample filters, with the `PRIMARY_SEGMENTATION` labels and
    one point per cell coloured by its dominant gene. A lasso on the points
    narrows the cell table beside it, and a row picked there opens the **Cell
    record** below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Dominant gene`, and `Cell area (px)` and `Transcripts
        per cell` ranges, in the tab-local *Cell filters*.

        | Section | What it holds |
        |---|---|
        | Cells in numbers | 4 cards |
        | Image | *Image, labels and cells*, *Cells* |
        | Cell detail | *Cell record* |

=== ":material-dna:{ .mc-grape } Cell x gene"

    *Which genes do the cells carry, and in how many cells?*

    [![Cell x gene dashboard](../../images/pipeline-templates/nf-core/molkart/cell_x_gene_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/cell_x_gene_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Cell x gene dashboard](../../images/pipeline-templates/nf-core/molkart/cell_x_gene_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/cell_x_gene_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    The most abundant genes by share of assigned transcripts, then a dot plot
    of breadth (the share of cells expressing a gene) and level (transcripts
    per expressing cell) per sample. Per-cell counts of the most expressed
    genes and a clustered gene by sample heatmap follow; the gene summary table
    sits collapsed below.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Gene` and a `Transcripts of the gene per cell` range in
        the tab-local *Gene filters*.

        | Section | What it holds |
        |---|---|
        | Panel in numbers | 4 cards |
        | Top genes | *Most abundant genes in cells*, *Breadth and level per sample* |
        | Expression per cell | *Transcripts per expressing cell*, *Genes against samples* |
        | Gene table | *Gene summary*, collapsed |

=== ":material-set-merge:{ .mc-orange } Segmentation comparison"

    *Do the segmentation methods agree on the same tissue?*

    [![Segmentation comparison dashboard](../../images/pipeline-templates/nf-core/molkart/segmentation_comparison_light.png#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/segmentation_comparison_light.png){ .tpl-shot target="_blank" rel="noopener" }

    [![Segmentation comparison dashboard](../../images/pipeline-templates/nf-core/molkart/segmentation_comparison_dark.png#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/molkart/segmentation_comparison_dark.png){ .tpl-shot target="_blank" rel="noopener" }

    Cells, cell area and transcripts per cell over every method, and the labels
    the area filter removed as too small. Cells per sample and method, cell area
    per method and transcripts per cell per method put the methods side by
    side. A second viewer draws the `COMPARE_SEGMENTATION` labels and cells
    over the same image, beside that method's cell table.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Segmentation method` and a `Cell area (px)` range in the
        tab-local *Method filters*.

        | Section | What it holds |
        |---|---|
        | Methods in numbers | 4 cards |
        | Counts and shapes | *Cells per sample and method*, *Cell area per method*, *Transcripts per cell per method* |
        | Second segmentation | *Image with the comparison labels*, *Cells of the comparison method* |

Tables and point views select on their entity column: the sample sheet on the
sample, and the cell map and the cell tables on the cell key. The sample
filters reach every collection through the project links.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/molkart, it does not run the pipeline.
Run the pipeline first, with every segmentation method you want to compare in
`--segmentation_method`:

```bash
nextflow run nf-core/molkart -r 1.2.0 \
  --input samplesheet.csv \
  --segmentation_method mesmer,cellpose \
  --outdir results -profile docker
```

molkart 1.2.0 publishes its masks, Mindagap tables and QC sheets as symlinks
into the work directory whatever `--publish_dir_mode` says, so copy the results
with the links dereferenced (`rsync -L`) before the work directory is cleaned.
Then copy the samplesheet under `input/` and point Depictio at the results:

```bash
rsync -aL results/ molkart_results/
mkdir -p molkart_results/input && cp samplesheet.csv molkart_results/input/
depictio run --template nf-core/molkart/latest --data-root molkart_results/
```

See [nf-co.re/molkart/usage](https://nf-co.re/molkart/1.2.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `--data-root` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name; the sample and the method are read off
the file names.

```text
<DATA_ROOT>/
├── input/samplesheet*.csv                           # copied in, not published
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── <sample>_<image>_gridfilled_clahe.tiff           # pyramidal OME-TIFF, the image
├── stack/<sample>_stack.ome.tif                     # membrane runs only
├── segmentation/filtered_masks/<sample>_<method>_filtered.tif
├── spot2cell/cellxgene_<sample>_<method>.csv        # one row per cell
├── molkartqc/<sample>.<method>.spot_QC.csv
└── mindagap/<sample>_<spots>_markedDups.txt         # spots, duplicates marked
```

The raw masks, the AnnData files and the MultiQC report are not read.

---

## :material-flask-outline: Validation runs

The AWS megatest of 1.2.0, `results-4ec0790d80cf77f2428d33b1a8571ccb498e2170`,
holds `pipeline_info/` only, so nothing can be fetched from it. The template
was checked on a synthetic run instead: three samples and three segmentation
methods, with a stand-in segmentation, pyramidal contrast-enhanced images, raw
and filtered masks, and spot2cell and molkartqc outputs computed with the
pipeline's own algorithms on the test-datasets spot table. The screenshots
above come from that run. The reference run is `-profile test_full` on a
cluster, pending; the download script only fetches the small test-datasets
inputs:

```bash
DEST=/tmp/molkart_inputs
bash depictio/projects/nf-core/molkart/1.2.0/download_test_data.sh "$DEST"
```

Do not pass `--project-name` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/molkart](https://nf-co.re/molkart): official pipeline documentation
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
    <span class="tpl-credit-note">Keep it working as nf-core/molkart releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
