---
title: "Dashboard YAML Management"
icon: material/file-code
description: "Manage dashboards as code using YAML files with depictio-cli import/export commands."
---

# Dashboard YAML Management

Depictio supports managing dashboards as human-readable YAML files using the `depictio-cli` command-line tool. This enables Infrastructure-as-Code (IaC) workflows, version control integration, and reproducible dashboard deployments.

!!! info "Implementation Reference"
The DashboardDataLite model and CLI dashboard commands were introduced in [:material-github: PR #663](https://github.com/depictio/depictio/pull/663){ target="\_blank" }.

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
- **Validation**: Validate YAML locally before deploying to server

## CLI Commands

The `depictio-cli dashboard` command group provides three commands for YAML management:

| Command    | Description                  | Server Required          |
| ---------- | ---------------------------- | ------------------------ |
| `validate` | Validate YAML schema locally | No                       |
| `import`   | Import YAML to server        | Yes (unless `--dry-run`) |
| `export`   | Export dashboard to YAML     | Yes                      |

### Validate

Validate a dashboard YAML file against the DashboardDataLite schema locally without server connection.

```bash
depictio-cli dashboard validate <yaml_file> [OPTIONS]
```

| Option            | Description                     |
| ----------------- | ------------------------------- |
| `--verbose`, `-v` | Show detailed validation output |

**Examples:**

```bash
# Basic validation
depictio-cli dashboard validate my_dashboard.yaml

# Verbose output with warnings
depictio-cli dashboard validate my_dashboard.yaml --verbose
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color, #1e1e1e); padding: 1em; border-radius: 0.25rem; overflow-x: auto;">
<pre style="margin: 0; color: var(--md-code-fg-color, #e0e0e0);">
Validating: my_dashboard.yaml
<span style="color: #4CAF50;">✓ Validation passed</span>
  Errors: <span style="color: #4CAF50;">0</span>
  Warnings: <span style="color: #4CAF50;">0</span>
</pre>
</div>

### Import

Import a dashboard YAML file to the server. The project is determined from the YAML `project_tag` field or the `--project` option.

```bash
depictio-cli dashboard import <yaml_file> [OPTIONS]
```

| Option            | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `--config`, `-c`  | Path to CLI config file (required unless `--dry-run`) |
| `--project`, `-p` | Project ID (overrides `project_tag` in YAML)          |
| `--overwrite`     | Update existing dashboard with same title             |
| `--dry-run`       | Validate only, don't import                           |
| `--api`           | API base URL (default: from config)                   |

**Examples:**

```bash
# Validate locally without server (no config needed)
depictio-cli dashboard import dashboard.yaml --dry-run

# Import to server
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml

# Update existing dashboard with same title
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --overwrite

# Override project from YAML
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --project 646b0f3c1e4a2d7f8e5b8c9a
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color, #1e1e1e); padding: 1em; border-radius: 0.25rem; overflow-x: auto;">
<pre style="margin: 0; color: var(--md-code-fg-color, #e0e0e0);">
Validating: <span style="color: #2196F3;">dashboard.yaml</span>
<span style="color: #4CAF50;">✓ Validation passed</span>
  Title: <span style="color: #FF9800;">Iris Dashboard Demo</span>
  Components: <span style="color: #2196F3;">7</span>
  Project: <span style="color: #9C27B0;">Iris_Dataset_Project</span> (from YAML project_tag)

Loading CLI configuration...
<span style="color: #4CAF50;">✓ Configuration loaded</span>
  API URL: <span style="color: #2196F3;">http://localhost:8058</span>

Importing dashboard (project: <span style="color: #9C27B0;">Iris_Dataset_Project</span>)...
<span style="color: #4CAF50;">✓ Dashboard imported successfully!</span>
  Dashboard ID: <span style="color: #2196F3;">6824cb3b89d2b72169309737</span>
  Title: <span style="color: #FF9800;">Iris Dashboard Demo</span>
  Project ID: <span style="color: #2196F3;">650a1b2c3d4e5f6a7b8c9d0e</span>

View at: <span style="color: #4CAF50;">http://localhost:8058/dashboard/6824cb3b89d2b72169309737</span>
</pre>
</div>

### Export

Export a dashboard from the server to a YAML file.

```bash
depictio-cli dashboard export <dashboard_id> [OPTIONS]
```

| Option           | Description                                  |
| ---------------- | -------------------------------------------- |
| `--config`, `-c` | Path to CLI config file (required)           |
| `--output`, `-o` | Output file path (default: `dashboard.yaml`) |
| `--api`          | API base URL (default: from config)          |

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
    component_type: figure|card|interactive|table|image
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
    column_type: float64
    icon_name: mdi:leaf
    icon_color: "#8BC34A"

  # Interactive: MultiSelect filter
  - tag: variety-filter
    component_type: interactive
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    interactive_component_type: MultiSelect
    column_name: variety
    column_type: object
    custom_color: "#858585"

  # Interactive: RangeSlider filter
  - tag: sepal-length-filter
    component_type: interactive
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    interactive_component_type: RangeSlider
    column_name: sepal.length
    column_type: float64

  # Table: Data display
  - tag: data-table
    component_type: table
    workflow_tag: python/iris_workflow
    data_collection_tag: iris_table
    page_size: 10

  # Image: Gallery component
  - tag: sample-gallery
    component_type: image
    workflow_tag: python/image_workflow
    data_collection_tag: sample_images
    image_column: image_path
    s3_base_folder: "s3://bucket/images/"
    thumbnail_size: 150
    columns: 3
    max_images: 9
```

### Component Types Reference

| Type          | Description                                    | Key Fields                                  |
| ------------- | ---------------------------------------------- | ------------------------------------------- |
| `figure`      | Visualizations (scatter, box, histogram, etc.) | `visu_type`, `dict_kwargs`                  |
| `card`        | Metric cards with aggregations                 | `aggregation`, `column_name`, `column_type` |
| `interactive` | Filters (RangeSlider, MultiSelect)             | `interactive_component_type`, `column_name` |
| `table`       | Data tables                                    | `page_size`                                 |
| `image`       | Image galleries from S3/MinIO                  | `image_column`, `s3_base_folder`            |

#### Figure Component

```yaml
- tag: scatter-plot
  component_type: figure
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  visu_type: scatter # scatter, box, histogram, bar, line, pie, etc.
  dict_kwargs:
    x: column_x
    y: column_y
    color: category_column
    title: Chart Title
```

**Supported chart types:** `scatter`, `box`, `histogram`, `bar`, `line`, `area`, `violin`, `strip`, `pie`, `sunburst`, `treemap`, `heatmap`, `density_contour`, `density_heatmap`

#### Card Component

```yaml
- tag: metric-card
  component_type: card
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  aggregation: average # count, sum, mean, average, median, min, max, nunique
  column_name: numeric_column
  column_type: float64 # float64, int64, object
  icon_name: mdi:chart-line
  icon_color: "#2196F3"
```

#### Interactive Component

```yaml
# MultiSelect filter
- tag: category-filter
  component_type: interactive
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  interactive_component_type: MultiSelect
  column_name: category
  column_type: object

# RangeSlider filter
- tag: numeric-filter
  component_type: interactive
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  interactive_component_type: RangeSlider
  column_name: value
  column_type: float64
```

**Supported filter types:** `RangeSlider`, `MultiSelect`, `Select`

#### Table Component

```yaml
- tag: data-table
  component_type: table
  workflow_tag: python/workflow_name
  data_collection_tag: table_dc
  page_size: 10 # 10, 25, 50, or 100
```

#### Image Component

```yaml
- tag: image-gallery
  component_type: image
  workflow_tag: python/workflow_name
  data_collection_tag: images_dc
  image_column: image_path # Column with relative image paths (required)
  s3_base_folder: "s3://bucket/images/" # S3/MinIO prefix (required)
  thumbnail_size: 150 # Thumbnail height in pixels
  columns: 4 # Grid columns
  max_images: 20 # Maximum images to display
```

## Validation

The CLI validates YAML files against the DashboardDataLite Pydantic model:

```text
┌─────────────────────────────────────────────────────────────┐
│  1. YAML Syntax Parsing                                     │
│     └─ Checks valid YAML format                             │
├─────────────────────────────────────────────────────────────┤
│  2. Pydantic Schema Validation                              │
│     └─ Validates against DashboardDataLite model            │
├─────────────────────────────────────────────────────────────┤
│  3. Component Type Validation                               │
│     └─ Validates chart types, aggregation functions         │
├─────────────────────────────────────────────────────────────┤
│  4. Required Fields                                         │
│     └─ Ensures all required fields are present              │
└─────────────────────────────────────────────────────────────┘
```

### Validation Error Examples

**Invalid component type:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color, #1e1e1e); padding: 1em; border-radius: 0.25rem; overflow-x: auto;">
<pre style="margin: 0; color: var(--md-code-fg-color, #e0e0e0);">
<span style="color: #F44336;">✗ Validation failed</span>
  Errors: <span style="color: #F44336;">1</span>

┌─────────────────────────────────────────────────────────────┐
│ Component     │ Field          │ Message                    │
├───────────────┼────────────────┼────────────────────────────┤
│ -             │ <span style="color: #FF9800;">component_type</span> │ <span style="color: #F44336;">Invalid value 'graphs'.</span>    │
│               │                │ Valid: figure, card, etc.  │
└─────────────────────────────────────────────────────────────┘
</pre>
</div>

**Missing required field:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color, #1e1e1e); padding: 1em; border-radius: 0.25rem; overflow-x: auto;">
<pre style="margin: 0; color: var(--md-code-fg-color, #e0e0e0);">
<span style="color: #F44336;">✗ Validation failed</span>
  Errors: <span style="color: #F44336;">1</span>

┌─────────────────────────────────────────────────────────────┐
│ Component     │ Field          │ Message                    │
├───────────────┼────────────────┼────────────────────────────┤
│ -             │ <span style="color: #FF9800;">workflow_tag</span>   │ <span style="color: #F44336;">Field required</span>             │
└─────────────────────────────────────────────────────────────┘
</pre>
</div>

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
- tag: box-variety-sepal-length # Chart type + data
- tag: sepal-length-average # Metric + aggregation
- tag: variety-filter # Column + purpose

# Avoid: Generic tags
- tag: figure-1
- tag: card-2
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
