---
title: "Interactive Selection Filtering"
icon: material/selection-drag
description: "Use scatter plot selections and table row selections to filter dashboard components."
---

# :material-selection-drag: Interactive Selection Filtering

Filter dashboard components by selecting points on scatter plots or rows in tables—no pre-configuration needed.

## :material-information-outline: Overview

**Interactive Selection Filtering** extends the filtering system beyond traditional dropdowns and sliders. You can now:

- :material-chart-scatter-plot: **Lasso or box-select** points on scatter plots
- :material-gesture-tap: **Click** individual points on scatter plots
- :material-table-row: **Select rows** in AG Grid tables

Selected values automatically filter other components on the same Data Collection.

```text
┌─────────────────────┐         ┌─────────────────────┐
│  Scatter Plot       │         │  Image Gallery      │
│                     │         │                     │
│  [lasso select]     │────────▶│  [auto-filters]     │
│  ○ ○ ● ● ○         │         │  [shows 2 images]   │
└─────────────────────┘         └─────────────────────┘
```

## :material-chart-scatter-plot: Scatter Plot Selection

### Selection Modes

| Mode | Action | Result |
|------|--------|--------|
| :material-selection-drag: **Lasso** | Draw freeform shape around points | Select all enclosed points |
| :material-selection: **Box** | Draw rectangle around points | Select all enclosed points |
| :material-cursor-default-click: **Click** | Click individual point | Select single point |

### Enabling Selection

Add these properties to your figure component:

```yaml
components:
  - tag: quality-scatter
    component_type: figure
    workflow_tag: python/my_workflow
    data_collection_tag: sample_data
    visu_type: scatter
    dict_kwargs:
      x: category
      y: quality_score
      color: category
    # Enable selection filtering
    selection_enabled: true
    selection_column: sample_id
```

### Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `selection_enabled` | :material-check: Yes | Enable selection filtering (`true`/`false`) |
| `selection_column` | :material-check: Yes | Column to extract from selected points for filtering |

!!! tip "Selection Column"
    The `selection_column` should contain unique identifiers (e.g., `sample_id`) that exist in other components' data. This enables cross-component filtering.

### Using Selection in the Dashboard

1. :material-pencil: Enable **Edit Mode** and add a scatter plot with `selection_enabled: true`
2. :material-eye: Switch to **View Mode**
3. :material-selection-drag: Use the toolbar to select **Lasso** or **Box Select** mode
4. :material-gesture-tap: Draw a selection around points or click individual points
5. :material-filter: Other components automatically filter to show only selected samples

### Reset Selection

Click the :material-refresh: **Reset** button on the scatter plot to clear the selection and show all data.

---

## :material-table: Table Row Selection

### Enabling Row Selection

Add these properties to your table component:

```yaml
components:
  - tag: samples-table
    component_type: table
    workflow_tag: python/my_workflow
    data_collection_tag: sample_data
    page_size: 10
    # Enable row selection filtering
    row_selection_enabled: true
    row_selection_column: sample_id
```

### Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `row_selection_enabled` | :material-check: Yes | Enable row selection filtering (`true`/`false`) |
| `row_selection_column` | :material-check: Yes | Column to extract from selected rows for filtering |

### Using Row Selection

1. :material-table-row: Click rows in the table to select them
2. :material-checkbox-multiple-marked: Hold `Ctrl`/`Cmd` to select multiple rows
3. :material-filter: Other components automatically filter to show selected samples

### Reset Selection

Click the :material-refresh: **Reset** button on the table to clear row selection.

---

## :material-link-variant: How It Works

Selection filtering integrates with the existing interactive filtering system:

```text
┌─────────────────────────────────────────────────────────────┐
│                 interactive-values-store                     │
├─────────────────────────────────────────────────────────────┤
│  [                                                          │
│    {index: "dropdown-1", value: ["A", "B"], source: null},  │
│    {index: "scatter-1", value: ["S1", "S2"],                │
│     source: "scatter_selection"},                           │
│    {index: "table-1", value: ["S3"],                        │
│     source: "table_selection"},                             │
│  ]                                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
           ┌──────────────────┴──────────────────┐
           │         All Components Filter        │
           │  (cards, figures, tables, images)   │
           └─────────────────────────────────────┘
```

Selection data is stored with a `source` field:

- `scatter_selection` - From scatter plot lasso/box/click
- `table_selection` - From table row selection
- `null` - From interactive components (dropdowns, sliders)

All sources combine to filter dashboard components.

---

## :material-code-braces: Complete Example

```yaml
title: "Sample Analysis Dashboard"
subtitle: "Interactive filtering with scatter and table selection"
project_tag: "My Project"

components:
  # Scatter plot with selection enabled
  - tag: quality-scatter
    component_type: figure
    workflow_tag: python/analysis_workflow
    data_collection_tag: sample_data
    visu_type: scatter
    dict_kwargs:
      x: category
      y: quality_score
      title: "Quality by Category (select to filter)"
      color: category
    selection_enabled: true
    selection_column: sample_id

  # Table with row selection enabled
  - tag: samples-table
    component_type: table
    workflow_tag: python/analysis_workflow
    data_collection_tag: sample_data
    page_size: 10
    row_selection_enabled: true
    row_selection_column: sample_id

  # Image gallery (filters based on selections)
  - tag: sample-images
    component_type: image
    workflow_tag: python/analysis_workflow
    data_collection_tag: sample_data
    image_column: image_path
    s3_base_folder: "s3://bucket/images/"
    thumbnail_size: 150
    columns: 3

  # Card showing count (filters based on selections)
  - tag: selected-count
    component_type: card
    workflow_tag: python/analysis_workflow
    data_collection_tag: sample_data
    aggregation: count
    column_name: sample_id
    column_type: object
    icon_name: mdi:counter

  # Traditional dropdown filter (works alongside selections)
  - tag: category-filter
    component_type: interactive
    workflow_tag: python/analysis_workflow
    data_collection_tag: sample_data
    interactive_component_type: MultiSelect
    column_name: category
    column_type: object
```

---

## :material-compare: Selection vs Interactive Components

| Feature | :material-selection-drag: Selection | :material-tune: Interactive |
|---------|-----------|-------------|
| Input method | Click/drag on visualization | Dropdown/slider/picker |
| Multi-select | Yes (lasso, box, ctrl+click) | Depends on component type |
| Visual feedback | Highlighted points/rows | Selected values in control |
| Best for | Exploratory filtering | Known filter criteria |
| Reset | Per-component reset button | Per-component or global reset |

!!! tip "Combine Both Methods"
    Selection filtering and interactive components work together. Use dropdowns for known categories, then refine with scatter selections for data exploration.

---

## :material-alert-circle-outline: Limitations

- **Same Data Collection**: Selection filtering works within the same Data Collection. For cross-DC filtering, use [Links](cross-dc-filtering.md).
- **Scatter Only**: Currently only scatter plots support selection (not bar charts, histograms, etc.).
- **No Persistence**: Selections are cleared on page reload.

---

## :material-frequently-asked-questions: FAQ

??? question "Can I select points across multiple scatter plots?"
    Each scatter plot maintains its own selection. Selections from multiple plots combine (AND logic) to filter other components.

??? question "How do I know which column to use for `selection_column`?"
    Use a column with unique identifiers that exists in all components you want to filter. Typically this is `sample_id`, `id`, or similar.

??? question "Can I disable the reset button?"
    Currently, the reset button always appears for selection-enabled components. This ensures users can always clear their selection.

??? question "Does selection work with Code Mode figures?"
    Yes, but you must include the `selection_column` in your figure's `custom_data` parameter for the selection to extract values correctly.
