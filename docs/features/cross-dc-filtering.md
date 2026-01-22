# Cross-DC Filtering

Filter data in one collection and automatically update related visualizations—no pre-computed joins needed.

## Overview

**Links** connect Data Collections for interactive filtering at runtime. When you filter a metadata table, linked MultiQC plots and other visualizations update automatically.

```text
┌─────────────────┐         ┌─────────────────┐
│  Metadata Table │  link   │  MultiQC Plots  │
│                 │────────▶│                 │
│  [filter here]  │         │  [auto-updates] │
└─────────────────┘         └─────────────────┘
```

## How It Works

1. Define a **link** between source DC (e.g., metadata table) and target DC (e.g., MultiQC)
2. Add a filter component to your dashboard
3. When users filter the source DC, linked targets automatically show only matching data

## Configuration

Add links to your project YAML:

```yaml
links:
  - source_dc_id: sample_metadata
    source_column: sample_id
    target_dc_id: multiqc_fastqc
    target_type: multiqc
    link_config:
      resolver: sample_mapping
```

### Link Fields

| Field | Required | Description |
|-------|----------|-------------|
| `source_dc_id` | Yes | Data collection containing the filter |
| `source_column` | Yes | Column to filter on |
| `target_dc_id` | Yes | Data collection to receive filtered values |
| `target_type` | Yes | Type of target: `table` or `multiqc` |
| `link_config` | Yes | Resolution configuration (see below) |

### Link Config Options

```yaml
link_config:
  resolver: sample_mapping    # Resolution strategy
  target_field: sample_name   # Field to match in target (optional)
```

## Resolvers

Resolvers map source values to target identifiers:

| Resolver | Use Case | Example |
|----------|----------|---------|
| `direct` | Same value in both DCs | `sample_id` → `sample_id` |
| `sample_mapping` | Canonical ID → MultiQC variants | `S1` → `[S1_R1, S1_R2]` |
| `pattern` | Template substitution | `{sample}.bam` |

### When to Use Each Resolver

- **`direct`**: Source and target use identical identifiers
- **`sample_mapping`**: MultiQC sample names differ from your canonical IDs (most common for MultiQC)
- **`pattern`**: Target uses predictable naming convention

## Supported Target Types

| Type | Filter Action | Status |
|------|---------------|--------|
| `table` | Filters rows with `WHERE IN` | Available |
| `multiqc` | Filters plot samples | Available |
| `jbrowse2` | Shows/hides tracks | Planned |
| `images` | Filters image gallery | Planned |

## Complete Example

```yaml
name: "RNA-seq QC Analysis"
project_type: "advanced"

# Define links for cross-DC filtering
links:
  # Link metadata to MultiQC plots
  - source_dc_id: sample_metadata
    source_column: sample_id
    target_dc_id: multiqc_general_stats
    target_type: multiqc
    link_config:
      resolver: sample_mapping

  # Link metadata to expression table
  - source_dc_id: sample_metadata
    source_column: sample_id
    target_dc_id: gene_expression
    target_type: table
    link_config:
      resolver: direct
      target_field: sample_id

workflows:
  - name: "rnaseq_pipeline"
    # ... workflow config ...

    data_collections:
      - data_collection_tag: "sample_metadata"
        config:
          type: "table"
          metatype: "metadata"
          # ... scan config ...

      - data_collection_tag: "multiqc_general_stats"
        config:
          type: "MultiQC"

      - data_collection_tag: "gene_expression"
        config:
          type: "table"
          metatype: "aggregate"
          # ... scan config ...
```

## Dashboard Usage

1. Create a dashboard with your linked data collections
2. Add a **filter component** (dropdown, multi-select) on the source DC
3. Add visualizations for the target DCs
4. Filter the source → targets update automatically

## Links vs Joins

| Feature | Links | Joins |
|---------|-------|-------|
| Execution | Runtime (on filter) | Pre-computed (CLI batch) |
| Storage | None | Delta table in S3 |
| Target types | Any (table, MultiQC, ...) | Tables only |
| Use case | Interactive filtering | Combined datasets |

Use **links** for interactive cross-DC filtering. Use **joins** when you need a permanently combined dataset.
