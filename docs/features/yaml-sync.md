---
title: "YAML Dashboard Sync"
icon: material/sync
description: "Bidirectional synchronization between MongoDB dashboards and YAML files for Infrastructure-as-Code workflows."
---

# YAML Dashboard Sync

The YAML Dashboard Sync feature enables bidirectional synchronization between MongoDB-stored dashboards and human-readable YAML files. This enables Infrastructure-as-Code (IaC) workflows, version control integration, and collaborative dashboard development.

## Overview

```text
                      Auto-export on save
┌─────────────┐  ─────────────────────────────▶  ┌─────────────┐
│   MongoDB   │                                  │    YAML     │
│  Dashboard  │                                  │    Files    │
└─────────────┘  ◀─────────────────────────────  └─────────────┘
                   File watcher (debounced)
```

**Key Benefits:**

- **Version Control**: Track dashboard changes in Git with meaningful diffs
- **Infrastructure-as-Code**: Manage dashboards alongside your project configuration
- **Human-Readable Format**: Edit dashboards directly in YAML (60-80 lines vs 500+ MongoDB)
- **Collaborative Development**: Share and review dashboard configurations as code

## How It Works

### Export (MongoDB → YAML)

When a dashboard is saved in the web UI, Depictio automatically exports it to a YAML file:

1. Dashboard is saved via the web interface
2. Auto-export generates a human-readable YAML file
3. File is written to the configured `local_dir` directory
4. Git can track changes for version control

**Exported File Format:**

- MVP format: 60-80 lines (vs 500+ in MongoDB)
- Human-readable component IDs (`box-variety-sepal-length`)
- Flattened visualization structure (no nested dictionaries)
- Workflow/data_collection as simple tags

### Import (YAML → MongoDB)

When YAML files change, a file watcher detects modifications and syncs them back:

1. File watcher monitors `dashboards/local/` directory
2. Changes are debounced (default: 2 seconds)
3. Validation runs before import (schema, columns, types)
4. Valid changes sync to MongoDB
5. Invalid changes are rejected with detailed error messages

!!! warning "Safety Features"
    - File deletions do **not** delete MongoDB dashboards
    - New files require explicit import (not auto-created in MongoDB)
    - Validation blocks invalid configurations from being synced

## Directory Structure

### Local vs Templates

Depictio uses two directories for different use cases:

| Directory | Purpose | Git Tracking | Auto-Sync |
|-----------|---------|--------------|-----------|
| `dashboards/local/` | Instance-specific dashboards | `.gitignore` (recommended) | Yes (default) |
| `dashboards/templates/` | Shareable templates | Version-controlled | Optional |

### File Organization

Files are organized by project name when `DEPICTIO_DASHBOARD_YAML_ORGANIZE_BY_PROJECT=true`:

```text
dashboards/
├── local/                              # Instance-specific (auto-synced)
│   ├── Iris_Dataset_Project/
│   │   ├── Iris_Dashboard_demo_6824cb3b89d2b72169309737.yaml
│   │   └── Analysis_Dashboard_6824cb3b89d2b72169309738.yaml
│   └── Genomics_Project/
│       └── MultiQC_Overview_6824cb3b89d2b72169309739.yaml
│
└── templates/                          # Version-controlled templates
    └── nf-core/
        └── rnaseq_dashboard_template.yaml
```

**Filename Pattern:** `{Dashboard_Title}_{mongodb_id}.yaml`

## YAML Format

### MVP Format Structure

The MVP format is designed for readability and editability:

```yaml
dashboard: <mongodb_id>
title: Dashboard Title
components:
  - id: human-readable-component-id
    type: figure|card|interactive|table
    workflow: <workflow_tag>
    data_collection: <dc_tag>
    # Component-specific configuration...
```

### Complete Iris Dataset Example

Below is a real-world example showing all component types:

```yaml
dashboard: 6824cb3b89d2b72169309737
title: Iris Dashboard demo
components:
-   id: box-variety-sepal-length
    type: figure
    workflow: python/iris_workflow
    data_collection: iris_table
    visualization:
        chart: box
        x: variety
        y: sepal.length
        color_discrete_map: '{"Setosa": "#1f77b4", "Versicolor": "#ff7f0e", "Virginica": "#2ca02c"}'
        boxmode: group
        points: all
        notched: true
-   id: scatter-sepal-length-sepal-width
    type: figure
    workflow: python/iris_workflow
    data_collection: iris_table
    visualization:
        chart: scatter
        x: sepal.length
        y: sepal.width
        color: variety
        color_discrete_map: '{"Setosa": "#1f77b4", "Versicolor": "#ff7f0e", "Virginica": "#2ca02c"}'
        size: petal.length
        size_max: 20
        marginal_x: rug
        marginal_y: rug
        trendline: lowess
-   id: sepal-length-average
    type: card
    workflow: python/iris_workflow
    data_collection: iris_table
    aggregation:
        column: sepal.length
        function: average
        column_type: float64
    styling:
        title_color: '#8BC34A'
        icon_name: mdi:leaf
        icon_color: '#8BC34A'
        title_font_size: xl
        value_font_size: xl
-   id: variety-filter
    type: interactive
    workflow: python/iris_workflow
    data_collection: iris_table
    filter:
        column: variety
        type: MultiSelect
        column_type: object
        options:
        - Virginica
        - Versicolor
        - Setosa
        value:
        - Setosa
        - Versicolor
    styling:
        custom_color: '#858585'
        icon_name: bx:slider-alt
        title_size: md
-   id: sepal-length-filter
    type: interactive
    workflow: python/iris_workflow
    data_collection: iris_table
    filter:
        column: sepal.length
        type: RangeSlider
        column_type: float64
        min: 4.3
        max: 7.9
        default:
        - 4.3
        - 7.9
        value:
        - 4.3
        - 7.9
    styling:
        custom_color: '#F68B33'
        icon_name: bx:slider-alt
        title_size: md
        marks_number: 2
-   id: data-table
    type: table
    workflow: python/iris_workflow
    data_collection: iris_table
-   id: histogram-sepal-length
    type: figure
    workflow: python/iris_workflow
    data_collection: iris_table
    visualization:
        chart: histogram
        x: sepal.length
        color: variety
        nbins: 0
        barmode: relative
        cumulative: true
```

### Component Types Reference

| Type | Description | Key Fields |
|------|-------------|------------|
| `figure` | Visualizations (scatter, box, histogram, etc.) | `visualization.chart`, `visualization.x`, `visualization.y` |
| `card` | Metric cards with aggregations | `aggregation.column`, `aggregation.function` |
| `interactive` | Filters (RangeSlider, MultiSelect) | `filter.column`, `filter.type` |
| `table` | Data tables | (minimal configuration) |
| `image` | Image galleries from S3/MinIO | `image_column`, `s3_base_folder`, `thumbnail_size` |

#### Figure Chart Types

Supported chart types for `visualization.chart`:

- `scatter`, `box`, `histogram`, `bar`, `line`, `area`
- `violin`, `strip`, `pie`, `sunburst`, `treemap`
- `heatmap`, `density_contour`, `density_heatmap`

#### Card Aggregation Functions

Supported functions for `aggregation.function`:

- `count`, `nunique`, `sum`, `mean`, `average`
- `median`, `min`, `max`, `std`, `var`

#### Interactive Filter Types

Supported filter types:

- `RangeSlider` - Numeric range selection
- `MultiSelect` - Multiple value selection
- `Select` - Single value selection

#### Image Component Fields

Image components display image galleries from S3/MinIO storage:

```yaml
- tag: sample-gallery
  component_type: image
  workflow_tag: python/image_workflow
  data_collection_tag: sample_images
  image_column: image_path          # Column with image paths (required)
  s3_base_folder: "s3://bucket/images/"  # S3/MinIO prefix (required)
  thumbnail_size: 150               # Thumbnail height in pixels
  columns: 3                        # Grid columns
  max_images: 9                     # Maximum images to display
```

## Validation System

### Multi-Layer Validation

The validation system ensures YAML files are valid before syncing:

```text
┌─────────────────────────────────────────────────────────────┐
│  1. YAML Syntax Parsing                                     │
│     └─ Checks valid YAML format                             │
├─────────────────────────────────────────────────────────────┤
│  2. Pydantic Schema Validation                              │
│     └─ Validates against DashboardMVPYAML model             │
├─────────────────────────────────────────────────────────────┤
│  3. Component Type Validation                               │
│     └─ Validates chart types, aggregation functions         │
├─────────────────────────────────────────────────────────────┤
│  4. Column Name Validation                                  │
│     └─ Checks columns exist in data collection schema       │
├─────────────────────────────────────────────────────────────┤
│  5. Field Name Validation (Typo Detection)                  │
│     └─ Suggests corrections for misspelled fields           │
└─────────────────────────────────────────────────────────────┘
```

### Validation Configuration

Control validation behavior via environment variables:

```bash
# Enable/disable validation entirely
DEPICTIO_DASHBOARD_YAML_ENABLE_VALIDATION=true

# Block sync on validation errors (set false to only warn)
DEPICTIO_DASHBOARD_YAML_BLOCK_ON_VALIDATION_ERRORS=true

# Enable column name validation against data collection schema
DEPICTIO_DASHBOARD_YAML_VALIDATE_COLUMN_NAMES=true

# Enable component type validation (chart types, aggregations)
DEPICTIO_DASHBOARD_YAML_VALIDATE_COMPONENT_TYPES=true
```

### Validation Error Examples

**Invalid Chart Type:**
```
Error: Invalid chart type 'piechart'.
Valid types: scatter, box, histogram, bar, line, ...
Suggestion: Did you mean 'pie'?
```

**Invalid Column Name:**
```
Error: Column 'sepal_length' not found in data collection 'iris_table'.
Available columns: sepal.length, sepal.width, petal.length, petal.width, variety
Suggestion: Did you mean 'sepal.length'?
```

## CLI Commands

Use the CLI to validate YAML files before deployment.

For complete documentation of all dashboard CLI commands, see **[CLI Usage - Dashboard Commands](../depictio-cli/usage.md#dashboard-commands)**.

**Quick examples:**

```bash
# Validate a single file
depictio-cli dashboard validate dashboards/local/my_dashboard.yaml

# Validate all files in a directory
depictio-cli dashboard validate-dir dashboards/local/
```

## Configuration

### Environment Variables

See the [Environment Reference](../installation/env-reference.md#dashboard-yaml-sync) for all configuration options.

**Essential Settings:**

```bash
# Enable YAML sync (default: true)
DEPICTIO_DASHBOARD_YAML_ENABLED=true

# Local dashboard directory (instance-specific, auto-synced)
DEPICTIO_DASHBOARD_YAML_LOCAL_DIR=/path/to/dashboards/local

# Templates directory (version-controlled, optional watching)
DEPICTIO_DASHBOARD_YAML_TEMPLATES_DIR=/path/to/dashboards/templates

# Use MVP minimal format (recommended)
DEPICTIO_DASHBOARD_YAML_MVP_MODE=true

# Auto-export on dashboard save
DEPICTIO_DASHBOARD_YAML_AUTO_EXPORT_ON_SAVE=true

# Auto-import when files change
DEPICTIO_DASHBOARD_YAML_AUTO_IMPORT_ON_CHANGE=true

# Debounce delay for file watcher (seconds)
DEPICTIO_DASHBOARD_YAML_WATCHER_DEBOUNCE_SECONDS=2.0
```

### Docker Compose Integration

Mount your dashboards directory in Docker:

```yaml
services:
  depictio-backend:
    volumes:
      - ./dashboards/local:/app/dashboards/local
      - ./dashboards/templates:/app/dashboards/templates:ro
    environment:
      - DEPICTIO_DASHBOARD_YAML_LOCAL_DIR=/app/dashboards/local
      - DEPICTIO_DASHBOARD_YAML_TEMPLATES_DIR=/app/dashboards/templates
```

## Best Practices

### Version Control Strategy

1. **Add `dashboards/local/` to `.gitignore`** - Instance-specific dashboards shouldn't be version controlled
2. **Version control `dashboards/templates/`** - Share common templates across environments
3. **Use meaningful component IDs** - Makes Git diffs readable

### Component ID Naming

The MVP format generates human-readable IDs:

```yaml
# Good: Descriptive IDs
- id: box-variety-sepal-length      # Chart type + columns
- id: sepal-length-average          # Column + aggregation
- id: variety-filter                # Column + filter

# Avoid: Generic IDs
- id: figure-1
- id: card-2
```

### Team Workflows

1. **Development**: Edit YAML directly, changes auto-sync to MongoDB
2. **Review**: Use Git diffs to review dashboard changes
3. **Deployment**: Deploy templates to production environments
4. **Rollback**: Revert YAML changes with Git to restore previous state

## Troubleshooting

### Common Issues

**File not syncing:**

1. Check file watcher is running: `docker logs depictio-backend | grep "watcher"`
2. Verify file is in the watched directory
3. Check for validation errors in logs

**Validation failures:**

1. Run CLI validation: `depictio-cli dashboard validate file.yaml --verbose`
2. Check column names match data collection schema
3. Verify component types are supported

**Sync conflicts:**

1. The most recent change wins (file timestamp vs MongoDB timestamp)
2. Create a backup before manual edits
3. Use Git to track and resolve conflicts

### Debug Mode

Enable verbose logging for the YAML system:

```bash
DEPICTIO_LOGGING_VERBOSITY_LEVEL=DEBUG
```

## Future Roadmap

### Templates Marketplace (Planned)

- Share templates for nf-core pipeline dashboards
- Community-contributed templates
- One-click import from template catalog

### Template Variables (Planned)

```yaml
# Template with variables
title: "{{project_name}} - QC Dashboard"
components:
  - workflow: "{{workflow_name}}"
```

## See Also

- [Environment Reference - Dashboard YAML Settings](../installation/env-reference.md#dashboard-yaml-sync)
- [CLI Usage - Dashboard Commands](../depictio-cli/usage.md#dashboard-commands)
- [Dashboards Overview](dashboards.md)
- [Components Reference](components.md)
