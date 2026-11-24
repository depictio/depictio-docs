# Features

What a Depictio dashboard can do, from its components to the filters that link them, and how the platform runs underneath.

## Dashboards

- **Layout and tabs**

  ______________________________________________________________________

  View and edit modes, the filter panel, sections and tabs.

  [Layout](https://depictio.github.io/depictio-docs/latest/features/dashboards/index.md)

- **Sharing**

  ______________________________________________________________________

  Permissions, share links and embedding a dashboard in another page.

  [Sharing](https://depictio.github.io/depictio-docs/latest/features/dashboards/#sharing-dashboards)

- **What's new**

  ______________________________________________________________________

  What changed since your last visit: data, components and comments.

  [What's new](https://depictio.github.io/depictio-docs/latest/features/whats-new/index.md)

- **Comments and annotations**

  ______________________________________________________________________

  Threads on a component, and ranges, lines and notes drawn on it.

  [Comments](https://depictio.github.io/depictio-docs/latest/features/comments-annotations/index.md)

- **Versions and history**

  ______________________________________________________________________

  Preview, restore or bookmark any saved version of a dashboard.

  [Versions](https://depictio.github.io/depictio-docs/latest/features/versioning/index.md)

- **Dashboards as YAML**

  ______________________________________________________________________

  Export, edit and import a dashboard as a YAML file.

  [YAML sync](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md)

## Components

The ten types of **New component**, in the order, colours and icons of the app.

- **Figure**

  ______________________________________________________________________

  Plotly charts set up in the UI, or written in Python.

  [Figure](https://depictio.github.io/depictio-docs/latest/features/components/#figure-components)

- **Card**

  ______________________________________________________________________

  One aggregated value, with optional secondary metrics below it.

  [Card](https://depictio.github.io/depictio-docs/latest/features/components/#card-components)

- **Interactive**

  ______________________________________________________________________

  Sliders, selects, date pickers and text inputs that filter the dashboard.

  [Interactive](https://depictio.github.io/depictio-docs/latest/features/components/#interactive-components)

- **Table**

  ______________________________________________________________________

  Interactive tables with sorting, filtering and row selection.

  [Table](https://depictio.github.io/depictio-docs/latest/features/components/#table-components)

- **MultiQC**

  ______________________________________________________________________

  One plot of a MultiQC report, read from its parquet file.

  [MultiQC](https://depictio.github.io/depictio-docs/latest/features/components/#multiqc-components)

- **Image**

  ______________________________________________________________________

  An image gallery from S3, with thumbnails and a full-size viewer.

  [Image](https://depictio.github.io/depictio-docs/latest/features/components/#image-components)

- **Map**

  ______________________________________________________________________

  Geospatial data on an interactive tile map, with no API key.

  [Map](https://depictio.github.io/depictio-docs/latest/features/components/#map-components)

- **Genome browser**

  ______________________________________________________________________

  An embedded JBrowse 2 over a collection of genomic tracks.

  [Genome browser](https://depictio.github.io/depictio-docs/latest/features/components/#genome-browser-components)

- **Text**

  ______________________________________________________________________

  Section headings and notes that document the dashboard.

  [Text](https://depictio.github.io/depictio-docs/latest/features/components/#text-components)

- **Advanced viz**

  ______________________________________________________________________

  Over forty domain charts, such as volcano, Manhattan and oncoplot.

  [Advanced visualizations](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/index.md)

- **All component types**

  ______________________________________________________________________

  Every type's options and YAML, and building under active filters.

  [Component types](https://depictio.github.io/depictio-docs/latest/features/components/index.md)

- **Export and embedding**

  ______________________________________________________________________

  Serve one component to another website, as a Plotly spec or a page.

  [Export](https://depictio.github.io/depictio-docs/latest/features/component-export/index.md)

## Data and filtering

- **Selection filtering**

  ______________________________________________________________________

  Filter by selecting points, rows, map areas, genome regions or residues.

  [Selection filtering](https://depictio.github.io/depictio-docs/latest/features/interactive-selection-filtering/index.md)

- **Cross-DC filtering**

  ______________________________________________________________________

  Link data collections so a filter on one reaches the others.

  [Cross-DC filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md)

- **Filter expressions**

  ______________________________________________________________________

  A Polars expression that narrows what a card or a filter reads.

  [Filter expressions](https://depictio.github.io/depictio-docs/latest/features/filter-expressions/index.md)

- **Metadata panel**

  ______________________________________________________________________

  Label samples beside the dashboard, then compare the groups in charts.

  [Metadata panel](https://depictio.github.io/depictio-docs/latest/features/metadata-panel/index.md)

- **Runs**

  ______________________________________________________________________

  What each pipeline run produced, and what each scan changed.

  [Runs](https://depictio.github.io/depictio-docs/latest/features/runs/index.md)

- **Run comparison**

  ______________________________________________________________________

  Open a dashboard with what one run changed marked on it.

  [Compare a run](https://depictio.github.io/depictio-docs/latest/features/runs/#compare-a-dashboard-with-a-run)

## Data types

- **MultiQC**

  ______________________________________________________________________

  How reports are read, General Stats, sample links and comparing runs.

  [MultiQC](https://depictio.github.io/depictio-docs/latest/features/multiqc/index.md)

- **Proteins**

  ______________________________________________________________________

  Structures, alignments and per-residue facts, linked by residue.

  [Proteins](https://depictio.github.io/depictio-docs/latest/features/proteins/index.md)

- **Genome browser**

  ______________________________________________________________________

  JBrowse 2 on a dashboard, filtered by it and filtering it back.

  [Genome browser](https://depictio.github.io/depictio-docs/latest/features/genome-browser/index.md)

## System design

- **Architecture**

  ______________________________________________________________________

  The services behind Depictio, and how data flows between them.

  [Architecture](https://depictio.github.io/depictio-docs/latest/features/architecture/index.md)

- **Background work**

  ______________________________________________________________________

  Celery workers for previews, heavy renders, thumbnails and ingestion.

  [Background processing](https://depictio.github.io/depictio-docs/latest/features/architecture/#background-processing-v060)

- **Performance and scaling**

  ______________________________________________________________________

  How large data collections stay responsive, and the settings that tune it.

  [Performance](https://depictio.github.io/depictio-docs/latest/features/performance/index.md)

- **Data model**

  ______________________________________________________________________

  Domain objects, what is embedded where, and the MongoDB collections.

  [Data model](https://depictio.github.io/depictio-docs/latest/features/data-model/index.md)

- **Security**

  ______________________________________________________________________

  Authentication, access roles, code execution limits and audit logging.

  [Security](https://depictio.github.io/depictio-docs/latest/features/security/index.md)

- **Telemetry**

  ______________________________________________________________________

  What anonymous telemetry sends, how to check it and turn it off.

  [Telemetry](https://depictio.github.io/depictio-docs/latest/features/telemetry/index.md)

New here? Start with the [component types](https://depictio.github.io/depictio-docs/latest/features/components/index.md), then [Layout and tabs](https://depictio.github.io/depictio-docs/latest/features/dashboards/index.md).
