---
title: "Filter Expressions"
icon: material/filter-cog
description: "Polars-based filter expressions for conditional aggregation and scoped interactive components."
---

# :material-filter-cog: Filter Expressions

Filter expressions let you pre-filter data **before** aggregation or option computation using [Polars](https://docs.pola.rs/) syntax. They are available on **card** and **interactive** components via the `filter_expr` YAML field.

!!! info "Introduced in v0.8.0-b2"
    Filter expressions were added in [:material-github: PR #710](https://github.com/depictio/depictio/pull/710){ target="\_blank" }.

## Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Data Pipeline                                │
│                                                                 │
│  Delta Table ──▶ Interactive Filters ──▶ filter_expr ──▶ Result │
│                  (user selections)       (YAML-defined)         │
│                                                                 │
│  Card:        filter_expr narrows data before aggregation       │
│  Interactive: filter_expr scopes dropdown options / slider range │
└─────────────────────────────────────────────────────────────────┘
```

**Key behaviors:**

- `filter_expr` applies **on top of** interactive filters (dual-layer)
- On **cards**: narrows the dataset before computing the metric value
- On **interactive components**: restricts available options/range to the filtered subset
- Expressions are validated and executed in a sandboxed namespace for security

## Syntax

Expressions use Polars column syntax. Two constructors are available:

| Constructor | Description | Example |
|-------------|-------------|---------|
| `col('name')` | Reference a column | `col('coverage')` |
| `lit(value)` | Explicit literal value | `lit(30)` |

### Comparison Operators

```yaml
filter_expr: "col('coverage') >= 30"
filter_expr: "col('quality') > 80"
filter_expr: "col('status') == 'passed'"
filter_expr: "col('status') != 'failed'"
```

### Logical Operators

Combine conditions with `&` (AND), `|` (OR), `~` (NOT). Use parentheses for grouping:

```yaml
# AND — both conditions must be true
filter_expr: "(col('coverage') >= 30) & (col('quality') > 80)"

# OR — either condition
filter_expr: "(col('type') == 'tumor') | (col('type') == 'metastasis')"

# NOT — negate a condition
filter_expr: "~col('sample_type').is_in(['control', 'blank'])"
```

### Membership & Null Checks

| Method | Description | Example |
|--------|-------------|---------|
| `.is_in([...])` | Value in list | `col('biome').is_in(['forest', 'ocean'])` |
| `.is_null()` | Value is null | `col('score').is_null()` |
| `.is_not_null()` | Value is not null | `col('score').is_not_null()` |
| `.is_between(lo, hi)` | Value in range | `col('expression').is_between(1.0, 100.0)` |

### String Methods

Access via the `.str` namespace:

| Method | Description | Example |
|--------|-------------|---------|
| `.str.contains(pat)` | Substring match | `col('gene').str.contains('HOX')` |
| `.str.starts_with(pfx)` | Prefix match | `col('id').str.starts_with('SAMPLE_')` |
| `.str.ends_with(sfx)` | Suffix match | `col('file').str.ends_with('.fastq')` |
| `.str.to_lowercase()` | Convert to lowercase | `col('name').str.to_lowercase()` |
| `.str.to_uppercase()` | Convert to uppercase | `col('name').str.to_uppercase()` |
| `.str.strip()` | Trim whitespace | `col('name').str.strip()` |

### Date/Time Accessors

Access via the `.dt` namespace:

| Method | Description | Example |
|--------|-------------|---------|
| `.dt.year()` | Extract year | `col('run_date').dt.year() == 2026` |
| `.dt.month()` | Extract month | `col('run_date').dt.month() >= 6` |
| `.dt.day()` | Extract day | `col('run_date').dt.day() == 1` |

### Window Functions

Broadcast an aggregation across groups with `.over('group_column')`. This enables **group-level filtering** — keep or discard entire groups based on an aggregate property:

| Pattern | Description |
|---------|-------------|
| `col('x').count().over('group') >= N` | Groups with at least N rows |
| `col('x').mean().over('group') > threshold` | Groups with mean above threshold |
| `col('x').std().over('group') < threshold` | Low-variance groups |
| `col('x').min().over('group') > threshold` | Groups where all values exceed threshold |

**Available aggregation methods:** `.mean()`, `.sum()`, `.min()`, `.max()`, `.count()`, `.std()`, `.median()`

```yaml
# Only taxa with 100+ observations
filter_expr: "col('taxonomy').count().over('taxonomy') >= 100"

# Genes with mean expression > 1.0
filter_expr: "col('expression').mean().over('gene') > 1.0"

# Batches where minimum read depth exceeds 30
filter_expr: "col('read_depth').min().over('batch') > 30"
```

### Column-to-Column Comparison

Compare two columns directly:

```yaml
filter_expr: "col('tumor_expr') > col('normal_expr')"
filter_expr: "col('sepal.length') > col('petal.length')"
```

### Type Casting

```yaml
filter_expr: "col('score').cast(float) > 0.5"
```

## Usage on Cards

Add `filter_expr` to a card component to compute a **conditional aggregation**:

```yaml
# Count only high-quality samples
- tag: hq-sample-count
  component_type: card
  workflow_tag: python/samples_workflow
  data_collection_tag: samples
  aggregation: count
  column_name: sample_id
  filter_expr: "(col('coverage') >= 30) & (col('contamination') < 0.05)"
  title: "HQ Samples"
  icon_name: mdi:check-circle
  icon_color: "#43A047"
```

Works with [multi-metric summary cards](components.md#multi-metric-summary-cards) — all secondary metrics are also computed on the filtered data:

```yaml
- tag: filtered-summary
  component_type: card
  aggregation: average
  aggregations: [median, std_dev, min, max]
  column_name: expression
  filter_expr: "col('gene_type') == 'protein_coding'"
  # ...
```

## Usage on Interactive Components

Add `filter_expr` to an interactive component to **scope its options**:

```yaml
# Only show varieties that have petal.length > 4
- tag: long-petal-varieties
  component_type: interactive
  interactive_component_type: MultiSelect
  column_name: variety
  filter_expr: "col('petal.length') > 4"
  title: "Varieties (petal > 4 cm)"
  # ...
```

**Effect by component type:**

| Component | Effect of filter_expr |
|-----------|----------------------|
| Select / MultiSelect / SegmentedControl | Only shows unique values present in filtered data |
| Slider / RangeSlider | Adjusts min/max range to filtered data |
| DateRangePicker | Adjusts date range to filtered data |

## Security

Expressions are validated before execution. Only Polars column operations are allowed:

**Allowed:** `col()`, `lit()`, comparison operators, logical operators, the methods listed above

**Blocked:** `import`, `exec`, `eval`, `open`, `os`, `sys`, `lambda`, `def`, `class`, loops, dunder attributes, and all other Python builtins

Expressions run in a restricted namespace containing only `col` and `lit` — no access to the broader Python runtime.

## See Also

- [Card Components](components.md#card-components)
- [Interactive Components](components.md#interactive-components)
- [Dashboard YAML Management](yaml-sync.md)
