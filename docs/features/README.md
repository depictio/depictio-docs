---
title: "Features"
icon: material/star
description: "Dashboards, component types, filtering, data types and how Depictio runs underneath."
---

# Features

What a Depictio dashboard can do, from its components to the filters that link them, and how the platform runs underneath.

## :material-view-dashboard: Dashboards

<div class="grid cards" markdown>

-   :material-view-dashboard-variant:{ .lg .middle .dp-purple } **Layout and tabs**

    ---

    View and edit modes, the filter panel, sections and tabs.

    [:octicons-arrow-right-24: Layout](dashboards.md)

-   :material-share-variant:{ .lg .middle .dp-violet } **Sharing**

    ---

    Permissions, share links and embedding a dashboard in another page.

    [:octicons-arrow-right-24: Sharing](dashboards.md#sharing-dashboards)

-   :material-new-box:{ .lg .middle .dp-blue } **What's new**

    ---

    What changed since your last visit: data, components and comments.

    [:octicons-arrow-right-24: What's new](whats-new.md)

-   :material-comment-text-multiple-outline:{ .lg .middle .dp-teal } **Comments and annotations**

    ---

    Threads on a component, and ranges, lines and notes drawn on it.

    [:octicons-arrow-right-24: Comments](comments-annotations.md)

-   :material-history:{ .lg .middle .dp-orange } **Versions and history**

    ---

    Preview, restore or bookmark any saved version of a dashboard.

    [:octicons-arrow-right-24: Versions](versioning.md)

-   :material-file-code:{ .lg .middle .dp-yellow } **Dashboards as YAML**

    ---

    Export, edit and import a dashboard as a YAML file.

    [:octicons-arrow-right-24: YAML sync](yaml-sync.md)

</div>

## :material-puzzle: Components

The ten types of **New component**, in the order, colours and icons of the app.

<div class="grid cards" markdown>

-   :material-chart-box:{ .lg .middle .dp-figure } **Figure**

    ---

    Plotly charts set up in the UI, or written in Python.

    [:octicons-arrow-right-24: Figure](components.md#figure-components)

-   :depictio-formkit-number:{ .lg .middle .dp-card } **Card**

    ---

    One aggregated value, with optional secondary metrics below it.

    [:octicons-arrow-right-24: Card](components.md#card-components)

-   :depictio-bx-slider-alt:{ .lg .middle .dp-interactive } **Interactive**

    ---

    Sliders, selects, date pickers and text inputs that filter the dashboard.

    [:octicons-arrow-right-24: Interactive](components.md#interactive-components)

-   :octicons-table-24:{ .lg .middle .dp-table } **Table**

    ---

    Interactive tables with sorting, filtering and row selection.

    [:octicons-arrow-right-24: Table](components.md#table-components)

-   :depictio-multiqc:{ .lg .middle .dp-multiqc } **MultiQC**

    ---

    One plot of a MultiQC report, read from its parquet file.

    [:octicons-arrow-right-24: MultiQC](components.md#multiqc-components)

-   :material-image-area:{ .lg .middle .dp-image } **Image**

    ---

    An image gallery from S3, with thumbnails and a full-size viewer.

    [:octicons-arrow-right-24: Image](components.md#image-components)

</div>

<div class="grid cards" markdown>

-   :material-map-marker-multiple:{ .lg .middle .dp-map } **Map**

    ---

    Geospatial data on an interactive tile map, with no API key.

    [:octicons-arrow-right-24: Map](components.md#map-components)

-   :material-dna:{ .lg .middle .dp-genome } **Genome browser**

    ---

    An embedded JBrowse 2 over a collection of genomic tracks.

    [:octicons-arrow-right-24: Genome browser](components.md#genome-browser-components)

-   :material-text-box-edit:{ .lg .middle .dp-text } **Text**

    ---

    Section headings and notes that document the dashboard.

    [:octicons-arrow-right-24: Text](components.md#text-components)

-   :material-chart-scatter-plot-hexbin:{ .lg .middle .dp-advanced-viz } **Advanced viz**

    ---

    Over forty domain charts, such as volcano, Manhattan and oncoplot.

    [:octicons-arrow-right-24: Advanced visualizations](advanced-visualizations.md)

-   :material-puzzle:{ .lg .middle } **All component types**

    ---

    Every type's options and YAML, and building under active filters.

    [:octicons-arrow-right-24: Component types](components.md)

-   :material-code-json:{ .lg .middle .dp-blue } **Export and embedding**

    ---

    Serve one component to another website, as a Plotly spec or a page.

    [:octicons-arrow-right-24: Export](component-export.md)

</div>

## :material-filter-variant: Data and filtering

<div class="grid cards" markdown>

-   :material-selection-drag:{ .lg .middle .dp-purple } **Selection filtering**

    ---

    Filter by selecting points, rows, map areas, genome regions or residues.

    [:octicons-arrow-right-24: Selection filtering](interactive-selection-filtering.md)

-   :material-link-variant:{ .lg .middle .dp-blue } **Cross-DC filtering**

    ---

    Link data collections so a filter on one reaches the others.

    [:octicons-arrow-right-24: Cross-DC filtering](cross-dc-filtering.md)

-   :material-filter-cog:{ .lg .middle .dp-teal } **Filter expressions**

    ---

    A Polars expression that narrows what a card or a filter reads.

    [:octicons-arrow-right-24: Filter expressions](filter-expressions.md)

-   :material-tag-multiple-outline:{ .lg .middle .dp-green } **Metadata panel**

    ---

    Label samples beside the dashboard, then compare the groups in charts.

    [:octicons-arrow-right-24: Metadata panel](metadata-panel.md)

-   :material-folder-play-outline:{ .lg .middle .dp-orange } **Runs**

    ---

    What each pipeline run produced, and what each scan changed.

    [:octicons-arrow-right-24: Runs](runs.md)

-   :material-compare-horizontal:{ .lg .middle .dp-pink } **Run comparison**

    ---

    Open a dashboard with what one run changed marked on it.

    [:octicons-arrow-right-24: Compare a run](runs.md#compare-a-dashboard-with-a-run)

</div>

## :material-dna: Data types

<div class="grid cards" markdown>

-   :depictio-multiqc:{ .lg .middle .dp-multiqc } **MultiQC**

    ---

    How reports are read, General Stats, sample links and comparing runs.

    [:octicons-arrow-right-24: MultiQC](multiqc.md)

-   :material-molecule:{ .lg .middle .dp-teal } **Proteins**

    ---

    Structures, alignments and per-residue facts, linked by residue.

    [:octicons-arrow-right-24: Proteins](proteins.md)

-   :material-dna:{ .lg .middle .dp-genome } **Genome browser**

    ---

    JBrowse 2 on a dashboard, filtered by it and filtering it back.

    [:octicons-arrow-right-24: Genome browser](genome-browser/index.md)

</div>

## :material-cog: System design

<div class="grid cards" markdown>

-   :material-sitemap:{ .lg .middle .dp-violet } **Architecture**

    ---

    The services behind Depictio, and how data flows between them.

    [:octicons-arrow-right-24: Architecture](architecture.md)

-   :material-cog-refresh:{ .lg .middle .dp-teal } **Background work**

    ---

    Celery workers for previews, heavy renders, thumbnails and ingestion.

    [:octicons-arrow-right-24: Background processing](architecture.md#background-processing-v060)

-   :material-speedometer:{ .lg .middle .dp-orange } **Performance and scaling**

    ---

    How large data collections stay responsive, and the settings that tune it.

    [:octicons-arrow-right-24: Performance](performance.md)

-   :material-database-outline:{ .lg .middle .dp-blue } **Data model**

    ---

    Domain objects, what is embedded where, and the MongoDB collections.

    [:octicons-arrow-right-24: Data model](data-model.md)

-   :material-shield-check:{ .lg .middle .dp-red } **Security**

    ---

    Authentication, access roles, code execution limits and audit logging.

    [:octicons-arrow-right-24: Security](security.md)

-   :material-radar:{ .lg .middle .dp-green } **Telemetry**

    ---

    What anonymous telemetry sends, how to check it and turn it off.

    [:octicons-arrow-right-24: Telemetry](telemetry.md)

</div>

[![Depictio system architecture: the React viewer, FastAPI, MongoDB, S3 storage, Redis and Celery workers](../images/architecture/system_light.png#only-light)](../images/architecture/system_light.png){target=_blank}
[![Depictio system architecture: the React viewer, FastAPI, MongoDB, S3 storage, Redis and Celery workers](../images/architecture/system_dark.png#only-dark)](../images/architecture/system_dark.png){target=_blank}

New here? Start with the [component types](components.md), then [Layout and tabs](dashboards.md).
