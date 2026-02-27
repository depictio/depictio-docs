---
title: "Dashboard YAML Management"
icon: material/file-code
description: "Manage dashboards as code using YAML files with depictio-cli import/export commands."
---

# Dashboard YAML Management

Depictio supports managing dashboards as human-readable YAML files using the `depictio-cli` command-line tool. This enables Infrastructure-as-Code (IaC) workflows, version control integration, and reproducible dashboard deployments.

!!! info "Implementation Reference"
    The DashboardDataLite model and CLI dashboard commands were introduced in [:material-github: PR #663](https://github.com/depictio/depictio/pull/663){ target="\_blank" }. Domain validation (enum constraints, cross-field rules, server schema checks) was added in [:material-github: PR #684](https://github.com/depictio/depictio/pull/684){ target="\_blank" }.

## Overview

```text
┌─────────────────┐                        ┌─────────────────┐
│   YAML Files    │  depictio-cli import   │    MongoDB      │
│   (version      │ ─────────────────────▶ │   Dashboard     │
│    controlled)  │                        │                 │
│                 │  depictio-cli export   │                 │
│                 │ ◀───────────────────── │                 │
└─────────────────┘                        └─────────────────┘
```

**Key Benefits:**

- **Version Control**: Track dashboard changes in Git with meaningful diffs
- **Infrastructure-as-Code**: Manage dashboards alongside your project configuration
- **Human-Readable Format**: Edit dashboards directly in YAML (60-80 lines vs 500+ in MongoDB)
- **Reproducible Deployments**: Import dashboards to any Depictio instance
- **Early Validation**: Catch invalid field values and incompatible combinations before importing

## CLI Commands

The `depictio-cli dashboard` command group provides three commands for YAML management:

| Command    | Description                              | Server Required          |
| ---------- | ---------------------------------------- | ------------------------ |
| `validate` | Validate YAML (schema + server schema)   | Optional (for Pass 2)    |
| `import`   | Import YAML to server                    | Yes (unless `--dry-run`) |
| `export`   | Export dashboard to YAML                 | Yes                      |

### Validate

Validate a dashboard YAML file. Runs in two passes:

- **Pass 1 — schema + domain** (always, no server required): checks required fields, enum values (`visu_type`, `column_type`), and cross-field rules (aggregation × column_type, interactive_type × column_type, mode/code_content).
- **Pass 2 — server schema** (default when `--config` is provided): resolves each component's `workflow_tag` + `data_collection_tag` against the live delta table schema, checks that `column_name` exists, and validates aggregation/interactive type against the inferred column type. Skip with `--offline`.

```bash
depictio-cli dashboard validate <yaml_file> [OPTIONS]
```

| Option              | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| `--config`, `-c`    | Path to CLI config file (enables server schema validation — Pass 2)      |
| `--offline`         | Skip server schema check (Pass 1 only — useful without server access)    |
| `--verbose`, `-v`   | Show detailed validation output                                          |
| `--api`             | API base URL (default: from config)                                      |

**Examples:**

```bash
# Schema + domain only (no server needed)
depictio-cli dashboard validate my_dashboard.yaml

# Full validation including server column check
depictio-cli dashboard validate my_dashboard.yaml --config ~/.depictio/admin_config.yaml

# Force offline even when config is provided
depictio-cli dashboard validate my_dashboard.yaml --config ~/.depictio/admin_config.yaml --offline
```

**Example Output (all passes OK):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
  <span style="color: #2e7d32;">✓ Schema + domain OK</span>
  Pass 2: server schema validation
  <span style="color: #2e7d32;">✓ Server schema OK</span>

<span style="color: #2e7d32;">✓ Validation passed</span>
</pre>
</div>

**Example Output (domain error — invalid visu_type):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
<span style="color: #c62828;">✗ Schema/domain validation failed</span>
                         Validation Errors
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component     ┃ Field     ┃ Message                                            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ pie-chart     │ -         │ Invalid visu_type 'pie' for mode='ui'.             │
│               │           │ Valid values: scatter, line, bar, box, histogram   │
│ treemap-chart │ -         │ Invalid visu_type 'treemap' for mode='ui'.         │
│               │           │ Valid values: scatter, line, bar, box, histogram   │
└───────────────┴───────────┴────────────────────────────────────────────────────┘
</pre>
</div>

### Import

Import a dashboard YAML file to the server. Always runs schema + domain validation first (Pass 1). Also runs server schema validation by default (Pass 2) — skip with `--offline`.

```bash
depictio-cli dashboard import <yaml_file> [OPTIONS]
```

| Option              | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| `--config`, `-c`    | Path to CLI config file (required unless `--dry-run`)          |
| `--project`, `-p`   | Project ID (overrides `project_tag` in YAML)                   |
| `--overwrite`       | Update existing dashboard with same title                      |
| `--dry-run`         | Validate schema + domain only, don't import (no server needed) |
| `--offline`         | Skip server schema check (column names not verified)           |
| `--api`             | API base URL (default: from config)                            |

!!! note "Validation before import"
    `dashboard import` always validates your YAML before sending it to the server. A failed validation aborts the import — you never import a dashboard that fails schema or domain checks.

**Examples:**

```bash
# Schema + domain validation only (no config, no import)
depictio-cli dashboard import dashboard.yaml --dry-run

# Full validation + import (server schema check runs by default)
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml

# Import without server schema check
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --offline

# Update existing dashboard with same title
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --overwrite

# Override project from YAML
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --project 646b0f3c1e4a2d7f8e5b8c9a
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);"><span style="color: #0097a7;">Validating:</span> <span style="color: #c2185b;">dashboard.yaml</span>
<span style="color: #2e7d32;">✓ Validation passed</span>
  Title: Iris Dashboard Demo
  Components: 7
  Project: Iris_Dataset_Project (from YAML project_tag)

<span style="color: #0097a7;">Loading CLI configuration...</span>
<span style="color: #2e7d32;">✓ Configuration loaded</span>
  API URL: localhost:8058

<span style="color: #0097a7;">Importing dashboard (project: Iris_Dataset_Project)...</span>
<span style="color: #2e7d32;">✓ Dashboard imported successfully!</span>
  Dashboard ID: 6824cb3b89d2b72169309737
  Title: Iris Dashboard Demo
  Project ID: 650a1b2c3d4e5f6a7b8c9d0e

<span style="color: #0097a7;">View at:</span> localhost:8058/dashboard/6824cb3b89d2b72169309737
</pre>
</div>

### Export

Export a dashboard from the server to a YAML file.

```bash
depictio-cli dashboard export <dashboard_id> [OPTIONS]
```

| Option            | Description                                  |
| ----------------- | -------------------------------------------- |
| `--config`, `-c`  | Path to CLI config file (required)           |
| `--output`, `-o`  | Output file path (default: `dashboard.yaml`) |
| `--api`           | API base URL (default: from config)          |

**Examples:**

```bash
# Export to default file
depictio-cli dashboard export 6824cb3b89d2b72169309737 --config ~/.depictio/admin_config.yaml

# Export to specific file
depictio-cli dashboard export 6824cb3b89d2b72169309737 --config ~/.depictio/admin_config.yaml -o iris_dashboard.yaml
```

## YAML Format

### DashboardDataLite Structure

The lite format is designed for human readability:

```yaml
title: Dashboard Title
subtitle: Optional subtitle
project_tag: Project_Name

components:
  - tag: component-identifier
    component_type: figure|card|interactive|table|image|multiqc
    workflow_tag: engine/workflow_name
    data_collection_tag: dc_tag
    # Component-specific fields...
```

### Complete Example

```yaml
title: Iris Dashboard Demo
subtitle: Sample analysis dashboard
project_tag: Iris_Dataset_Project

components:
  # Figure: Box plot
  - tag: box-variety-sepal-length
    component_type: figure
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    visu_type: box
    dict_kwargs:
      x: variety
      y: sepal.length
      color: variety
      title: Sepal Length by Variety

  # Figure: Scatter plot
  - tag: scatter-sepal-petal
    component_type: figure
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    visu_type: scatter
    dict_kwargs:
      x: sepal.length
      y: petal.length
      color: variety

  # Card: Metric with aggregation
  - tag: sepal-length-average
    component_type: card
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    aggregation: average
    column_name: sepal.length
    icon_name: mdi:leaf
    icon_color: "#8BC34A"

  # Interactive: MultiSelect filter
  - tag: variety-filter
    component_type: interactive
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    interactive_component_type: MultiSelect
    column_name: variety
    custom_color: "#858585"

  # Interactive: RangeSlider filter
  - tag: sepal-length-filter
    component_type: interactive
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    interactive_component_type: RangeSlider
    column_name: sepal.length

  # Table: Data display
  - tag: data-table
    component_type: table
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table

  # Image: Gallery component
  - tag: sample-gallery
    component_type: image
    workflow_tag: python/image_workflow
    data_collection_tag: sample_images
    image_column: image_path
    thumbnail_size: 150
    columns: 3
    max_images: 9

  # MultiQC: Quality control report
  - tag: fastqc-quality
    component_type: multiqc
    workflow_tag: python/nf_workflow
    data_collection_tag: multiqc_report
    selected_module: fastqc
    selected_plot: per_base_sequence_quality

  # Figure: Clustered heatmap
  - tag: gene-expression-heatmap
    component_type: figure
    workflow_tag: python/bio_workflow
    data_collection_tag: expression_matrix
    visu_type: heatmap
    dict_kwargs:
      index_column: gene_name
      row_annotations: [gene_type]
      cluster_rows: true
      normalize: zscore

  # Map: Scatter map with selection
  - tag: sampling-map
    component_type: map
    workflow_tag: python/my_workflow
    data_collection_tag: sample_metadata
    lat_column: latitude
    lon_column: longitude
    color_column: biome
    hover_columns: [sample_id, site_name]
    map_style: carto-positron
    selection_enabled: true
    selection_column: sample_id
```

## Component Types Reference

| Type          | Description                                    | Required Fields                                          |
| ------------- | ---------------------------------------------- | -------------------------------------------------------- |
| `figure`      | Plotly charts (scatter, box, heatmap, etc.)    | `visu_type` (ui mode) or `code_content` (code mode)     |
| `card`        | Metric cards with aggregations                 | `aggregation`, `column_name`                             |
| `interactive` | Filters (RangeSlider, MultiSelect, etc.)       | `interactive_component_type`, `column_name`              |
| `table`       | Data tables                                    | _(none beyond base fields)_                              |
| `image`       | Image galleries from S3/MinIO                  | `image_column`                                           |
| `multiqc`     | MultiQC quality control report viewer          | `selected_module`, `selected_plot`                       |
| `map`         | Geospatial maps (scatter, density, choropleth) | `lat_column`, `lon_column` (scatter/density) or `locations_column`, GeoJSON source (choropleth) |

### Figure Component

Two rendering modes are supported:

**UI Mode** (default) — select a chart type and pass Plotly Express parameters:

```yaml
- tag: scatter-plot
  component_type: figure
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  visu_type: scatter       # see valid values below
  dict_kwargs:
    x: column_x
    y: column_y
    color: category_column
    title: Chart Title
```

**Valid `visu_type` values (UI mode):** `scatter`, `line`, `bar`, `box`, `histogram`, `heatmap`

**Code Mode** — write arbitrary Python/Plotly code for full flexibility:

```yaml
- tag: custom-plot
  component_type: figure
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  mode: code
  code_content: |
    import plotly.express as px
    fig = px.scatter_matrix(df, dimensions=["sepal.length", "sepal.width", "petal.length"])
```

**ComplexHeatmap** — clustered heatmap with annotations (via [:material-open-in-new: plotly-complexheatmap](https://github.com/weber8thomas/plotly-complexheatmap){ target="_blank" }):

```yaml
- tag: gene-expression-heatmap
  component_type: figure
  workflow_tag: python/workflow_name
  data_collection_tag: expression_dc
  visu_type: heatmap
  dict_kwargs:
    index_column: gene_name
    value_columns: [sample_A, sample_B, sample_C]
    row_annotations: [gene_type, pathway]
    cluster_rows: true
    cluster_cols: true
    normalize: zscore
    colorscale: RdBu_r
    split_rows_by: gene_type
    cluster_method: ward
    cluster_metric: euclidean
```

Heatmap `dict_kwargs` parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `index_column` | string | Column for row labels |
| `value_columns` | list | Numeric columns for the matrix (omit for all numeric) |
| `row_annotations` | list | Columns shown as colored side bars |
| `cluster_rows` / `cluster_cols` | bool | Enable hierarchical clustering |
| `normalize` | string | `zscore`, `minmax`, or `none` |
| `colorscale` | string | Plotly colorscale (e.g. `RdBu_r`, `Viridis`) |
| `split_rows_by` | string | Split heatmap rows by annotation column |
| `cluster_method` | string | `ward`, `average`, `complete`, `single` |
| `cluster_metric` | string | `euclidean`, `correlation`, `cosine` |

!!! note "Code mode and visu_type"
    `visu_type` is not validated when `mode: code`. Any Plotly chart can be built in code mode. `code_content` must be non-empty when `mode: code`.

**Selection filtering** — enable lasso/box selection to filter linked components:

```yaml
- tag: scatter-with-selection
  component_type: figure
  visu_type: scatter
  selection_enabled: true
  selection_column: sample_id   # required when selection_enabled=true
  # ...
```

### Card Component

```yaml
- tag: metric-card
  component_type: card
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  aggregation: average
  column_name: numeric_column
  column_type: float64     # optional — enables offline aggregation validation
  icon_name: mdi:chart-line
  icon_color: "#2196F3"
```

**Aggregation × column_type compatibility:**

| column_type  | Valid aggregations                                                              |
| ------------ | ------------------------------------------------------------------------------- |
| `int64`      | `count`, `sum`, `average`, `median`, `min`, `max`, `range`, `variance`, `std_dev`, `skewness`, `kurtosis` |
| `float64`    | `count`, `sum`, `average`, `median`, `min`, `max`, `range`, `variance`, `std_dev`, `percentile`, `skewness`, `kurtosis` |
| `bool`       | `count`, `sum`, `min`, `max`                                                    |
| `datetime`   | `count`, `min`, `max`                                                           |
| `timedelta`  | `count`, `sum`, `min`, `max`                                                    |
| `category`   | `count`, `mode`                                                                 |
| `object`     | `count`, `mode`, `nunique`                                                      |

!!! tip "column_type is optional"
    If you omit `column_type`, validation against the compatibility table is skipped offline. When `--config` is provided, the column type is inferred from the server schema and used for validation automatically.

### Interactive Component

```yaml
# MultiSelect — for categorical/text columns
- tag: category-filter
  component_type: interactive
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  interactive_component_type: MultiSelect
  column_name: category

# RangeSlider — for numeric columns
- tag: numeric-filter
  component_type: interactive
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  interactive_component_type: RangeSlider
  column_name: value
  column_type: float64     # optional — enables offline type compatibility check

# DateRangePicker — for datetime columns
- tag: date-filter
  component_type: interactive
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  interactive_component_type: DateRangePicker
  column_name: sample_date
```

**Interactive type × column_type compatibility:**

| column_type  | Valid interactive_component_type                    |
| ------------ | --------------------------------------------------- |
| `int64`      | `Slider`, `RangeSlider`                             |
| `float64`    | `Slider`, `RangeSlider`                             |
| `datetime`   | `DateRangePicker`                                   |
| `category`   | `Select`, `MultiSelect`, `SegmentedControl`         |
| `object`     | `Select`, `MultiSelect`, `SegmentedControl`         |
| `bool`       | _(not yet supported)_                               |
| `timedelta`  | _(not supported)_                                   |

### Table Component

```yaml
- tag: data-table
  component_type: table
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  page_size: 25          # rows per page (default: 10)
  columns: [col1, col2]  # optional: restrict visible columns
```

### Image Component

```yaml
- tag: image-gallery
  component_type: image
  workflow_tag: python/workflow_name
  data_collection_tag: images_dc
  image_column: image_path   # required: column with image paths
  thumbnail_size: 150        # pixels (default: 150)
  columns: 4                 # grid columns (default: 4)
  max_images: 20             # max images shown (default: 20)
```

!!! note "`s3_base_folder` is optional"
    If omitted, the image base folder is resolved automatically from the data collection's S3 configuration at runtime.

### MultiQC Component

Embeds a specific plot from a MultiQC quality control report. Both `selected_module` and `selected_plot` are required — they uniquely identify which plot to render.

```yaml
- tag: fastqc-quality
  component_type: multiqc
  workflow_tag: python/nf_workflow
  data_collection_tag: multiqc_report
  selected_module: fastqc
  selected_plot: per_base_sequence_quality
```

!!! warning "Both fields are required"
    Omitting either `selected_module` or `selected_plot` will fail validation. Unlike the Dash runtime (which can auto-select), YAML-defined components must be explicit about which plot to display.

### Map Component

Supports three map types: `scatter_map` (default), `density_map`, and `choropleth_map`.

**Scatter map** — point markers at lat/lon coordinates:

```yaml
- tag: sampling-map
  component_type: map
  workflow_tag: python/my_workflow
  data_collection_tag: sample_metadata
  lat_column: latitude
  lon_column: longitude
  color_column: biome
  size_column: read_count
  hover_columns: [sample_id, site_name]
  map_style: carto-positron
  selection_enabled: true
  selection_column: sample_id
```

**Choropleth map** — colored regions from GeoJSON:

```yaml
- tag: country-choropleth
  component_type: map
  workflow_tag: python/my_workflow
  data_collection_tag: sample_metadata
  map_type: choropleth_map
  locations_column: country_name
  featureidkey: properties.NAME
  color_column: sample_id
  choropleth_aggregation: count
  color_continuous_scale: Viridis
  opacity: 0.6
  # GeoJSON source — pick one:
  geojson_url: "https://example.com/countries.geojson"   # URL
  # geojson_dc_tag: europe_geojson                        # DC tag
```

**Valid `map_type` values:** `scatter_map`, `density_map`, `choropleth_map`

**Valid `map_style` values:** `open-street-map`, `carto-positron`, `carto-darkmatter`

!!! note "Choropleth requirements"
    Choropleth maps require `locations_column`, `color_column`, and a GeoJSON source (`geojson_url`, `geojson_dc_tag`, or `geojson_data`). Selection filtering is not supported on choropleth maps.

## Validation

The CLI validates YAML files in two passes:

```text
┌──────────────────────────────────────────────────────────────┐
│  Pass 1 — Schema + Domain  (always, no server needed)        │
│                                                              │
│  ✓ YAML syntax parsing                                       │
│  ✓ Required fields (title, component required fields)        │
│  ✓ visu_type enum (scatter, line, bar, box, histogram, ...)  │
│  ✓ mode/code_content cross-field rule                        │
│  ✓ selection_enabled/selection_column cross-field rule       │
│  ✓ aggregation × column_type compatibility (if provided)     │
│  ✓ interactive_type × column_type compatibility (if provided)│
│  ✓ MultiQC: selected_module + selected_plot both required    │
│  ✓ Image: image_column required                              │
├──────────────────────────────────────────────────────────────┤
│  Pass 2 — Server Schema  (with --config, skip: --offline)    │
│                                                              │
│  ✓ Resolves workflow_tag + data_collection_tag → DC schema   │
│  ✓ Checks column_name exists in delta table schema           │
│  ✓ Infers column_type from schema → validates aggregation    │
│    and interactive_component_type against inferred type      │
└──────────────────────────────────────────────────────────────┘
```

Error output is a clean per-component table — each invalid field gets its own row:

```
                     Validation Errors
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Component              ┃ Field           ┃ Message        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ image-missing-column   │ image_column    │ Field required │
│ multiqc-missing-module │ selected_module │ Field required │
│ multiqc-missing-plot   │ selected_plot   │ Field required │
└────────────────────────┴─────────────────┴────────────────┘
```

## Best Practices

### File Organization

```text
project/
├── project.yaml              # Project configuration
├── dashboards/
│   ├── overview.yaml         # Main overview dashboard
│   ├── qc_metrics.yaml       # QC-specific dashboard
│   └── samples.yaml          # Sample analysis dashboard
└── README.md
```

### Component Naming

Use descriptive tags that indicate purpose:

```yaml
# Good: Descriptive tags
- tag: box-variety-sepal-length   # Chart type + data
- tag: sepal-length-average       # Metric + aggregation
- tag: variety-filter             # Column + purpose

# Avoid: Generic tags
- tag: figure-1
- tag: card-2
```

### Incremental Validation Workflow

```bash
# Step 1 — check schema and domain constraints (no server needed)
depictio-cli dashboard validate my.yaml

# Step 2 — full validation including column names
depictio-cli dashboard validate my.yaml --config ~/.depictio/admin_config.yaml

# Step 3 — dry import (schema check only, no write)
depictio-cli dashboard import my.yaml --dry-run

# Step 4 — actual import
depictio-cli dashboard import my.yaml --config ~/.depictio/admin_config.yaml

# Step 5 — roundtrip check (export back and diff)
depictio-cli dashboard export <id> -o out.yaml
diff my.yaml out.yaml
```

### Version Control

- **Do version control** dashboard YAML files
- **Use meaningful commit messages** describing dashboard changes
- **Review diffs** before merging dashboard changes
- **Tag releases** when deploying to production

## See Also

- [CLI Usage - Dashboard Commands](../depictio-cli/usage.md#dashboard-commands)
- [Components Reference](components.md)
- [Dashboards Overview](dashboards.md)
