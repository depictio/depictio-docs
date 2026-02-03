---
title: "Dashboard Components"
icon: material/view-dashboard
description: "Complete guide to Depictio's dashboard component types and their configuration."
---

# :material-puzzle: Dashboard Components

Depictio provides a variety of component types for building interactive dashboards. This guide covers each component type, when to use it, and how to configure it.

## :material-format-list-bulleted: Component Overview

<div class="grid cards" markdown>

-   :material-chart-scatter-plot:{ .lg .middle } **Figure**

    ---

    Charts and plots (scatter, bar, histogram, line, box, pie, and more)

-   :material-table:{ .lg .middle } **Table**

    ---

    Interactive data tables with filtering and sorting

-   :material-card-text:{ .lg .middle } **Card**

    ---

    Metric display with aggregations

-   :material-format-header-1:{ .lg .middle } **Text**

    ---

    Section headers (H1, H2, H3)

-   :material-tune:{ .lg .middle } **Interactive**

    ---

    User input components for filtering (slider, dropdown, date picker)

-   :material-microscope:{ .lg .middle } **MultiQC**

    ---

    Quality control report visualizations

-   :material-image-multiple:{ .lg .middle } **Image**

    ---

    Image galleries with S3/MinIO storage integration

</div>

---

## :material-chart-scatter-plot: Figure Components

Figure components display data visualizations using Plotly charts. They support both **UI Mode** (drag-and-drop configuration) and **Code Mode** (Python code for custom plots).

### Supported Chart Types

**UI Mode** provides a curated selection of chart types through the visual interface:

| Category | Chart Types |
|----------|-------------|
| :material-chart-scatter-plot: **Basic Charts** | Scatter, Bar, Line, Area, Pie, Donut |
| :material-chart-box: **Statistical** | Histogram, Box, Violin, Strip |
| :material-chart-bell-curve: **Distribution** | Density Heatmap, Density Contour |
| :material-chart-tree: **Hierarchical** | Treemap, Sunburst |

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
    Code Mode uses RestrictedPython for security. Only approved libraries (pandas, plotly) are available. See [Security](security.md) for details.

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Title | Chart title displayed at top | Auto-generated |
| X-axis label | Label for horizontal axis | Column name |
| Y-axis label | Label for vertical axis | Column name |
| Color | Column for color encoding | None |
| Hover data | Additional columns shown on hover | None |

### Selection Filtering (Scatter Plots)

Scatter plots can act as interactive filters. Enable selection to let users lasso, box-select, or click points to filter other components.

| Option | Description |
|--------|-------------|
| `selection_enabled` | Enable selection filtering (`true`/`false`) |
| `selection_column` | Column to extract from selected points |

See [Interactive Selection Filtering](interactive-selection-filtering.md) for details.

---

## :material-table: Table Components

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

### Row Selection Filtering

Tables can act as interactive filters. Enable row selection to let users click rows to filter other components.

| Option | Description |
|--------|-------------|
| `row_selection_enabled` | Enable row selection filtering (`true`/`false`) |
| `row_selection_column` | Column to extract from selected rows |

See [Interactive Selection Filtering](interactive-selection-filtering.md) for details.

---

## :material-card-text: Card Components

Card components display single metrics with optional aggregations and styling.

### Aggregation Types

| Aggregation | Description | Example |
|-------------|-------------|---------|
| :material-counter: **count** | Number of rows | Total samples |
| :material-sigma: **sum** | Sum of values | Total reads |
| :material-chart-line-variant: **mean** | Average value | Average coverage |
| :material-format-vertical-align-center: **median** | Median value | Median quality score |
| :material-arrow-down: **min** | Minimum value | Minimum mapping rate |
| :material-arrow-up: **max** | Maximum value | Maximum duplication rate |
| :material-tag-multiple: **unique** | Count of unique values | Unique sample types |

### Configuration

1. Select a **Data Collection**
2. Choose a **Column** to aggregate
3. Select an **Aggregation** type
4. Customize the **Title** and **Format**

### Styling Options

| Option | Description | Example |
|--------|-------------|---------|
| Title | Metric label | "Total Samples" |
| Format | Number formatting | `{:,.0f}` or `{:.2%}` |
| Color | Card accent color | Mantine color |
| Icon | Optional icon | `mdi:chart-line` |

---

## :material-format-header-1: Text Components

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

## :material-tune: Interactive Components

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

---

## :material-microscope: MultiQC Components

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

## :material-image-multiple: Image Components

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

Images must be uploaded to S3/MinIO before they can be displayed:

```bash
# Upload images to MinIO
mc cp --recursive ./images/ minio/depictio-bucket/project/images/
```

!!! tip "Cross-DC Filtering"
    Image components support filtering via interactive components on the same Data Collection. Select samples using a MultiSelect filter, and the image gallery updates automatically.

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
2. :material-shape: **Choose Component Type** - Figure, Table, Card, Interactive, Text, or MultiQC
3. :material-cog: **Configure Settings** - Type-specific options
4. :material-eye: **Preview** - See the component before adding
5. :material-plus-circle: **Add to Dashboard** - Place on the canvas

### Positioning Components

- :material-drag: **Drag and drop** components in Edit Mode
- :material-grid: Components snap to a **grid layout**
- :material-resize: Resize by dragging corner handles
