# <span style="color: #45B8AC;">:material-chef-hat:</span> Recipes

Recipes are the data transformation layer of the Depictio CLI. They convert raw bioinformatics pipeline output files into clean, dashboard-ready [Polars](https://pola.rs/) DataFrames — automatically, reproducibly, and with full validation.

<div style="display:flex;flex-direction:column;align-items:center;gap:10px;max-width:420px;margin:24px auto;font-size:0.9em;">

  <div style="width:100%;border:1.5px solid #bbb;border-radius:8px;background:#f9f9f9;padding:12px 16px;">
    <div style="font-weight:600;color:#888;font-size:0.75em;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">Upstream — Workflow</div>
    <div style="background:#efefef;border:1px solid #ccc;border-radius:6px;padding:9px 13px;">
      <strong>Bioinformatics pipeline</strong><br>
      <span style="color:#666;font-size:0.85em;">nf-core / Nextflow / Snakemake</span>
    </div>
    <div style="text-align:center;color:#aaa;margin:6px 0;font-size:1.1em;">↓</div>
    <div style="background:#efefef;border:1px solid #ccc;border-radius:6px;padding:9px 13px;">
      <strong>Raw output files</strong>
      <ul style="margin:5px 0 0 0;padding-left:16px;color:#555;font-size:0.85em;">
        <li>wide CSV</li><li>nested TSV</li><li>non-standard headers</li>
      </ul>
    </div>
  </div>

  <div style="color:#45B8AC;font-size:1.4em;line-height:1;">↓</div>

  <div style="width:100%;background:#45B8AC;color:#fff;border-radius:8px;padding:12px 16px;">
    <strong>Recipe</strong>
    <ul style="margin:5px 0 0 0;padding-left:16px;font-size:0.85em;">
      <li>reformat &amp; reshape</li><li>wide → long</li><li>rename columns</li><li>compute metrics</li>
    </ul>
  </div>

  <div style="color:#45B8AC;font-size:1.4em;line-height:1;">↓</div>

  <div style="width:100%;border:1.5px solid #45B8AC;border-radius:8px;background:#f0fafa;padding:12px 16px;">
    <div style="display:flex;align-items:center;gap:6px;font-weight:600;color:#45B8AC;font-size:0.75em;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">
      <img src="../../../images/logo/logo_icon.png" alt="Depictio" style="height:16px;width:auto;vertical-align:middle;">
      Downstream — Depictio
    </div>
    <div style="background:#b2dfdb;border:1px solid #45B8AC;border-radius:6px;padding:9px 13px;">
      <strong>Tidy DataFrame</strong>
      <ul style="margin:5px 0 0 0;padding-left:16px;font-size:0.85em;">
        <li>long format</li><li>clean schema</li><li>validated types</li>
      </ul>
    </div>
    <div style="text-align:center;color:#45B8AC;margin:6px 0;font-size:1.1em;">↓</div>
    <div style="background:#45B8AC;color:#fff;border-radius:6px;padding:9px 13px;text-align:center;font-weight:600;">
      Dashboard figures &amp; tables
    </div>
  </div>

</div>

## What is a Recipe?

A recipe is a plain Python module that describes how to transform one or more raw files into a single tidy DataFrame. Each recipe lives in `depictio/recipes/<pipeline>/` and declares exactly three things:

- **`SOURCES`** — input files to read (paths relative to `--data-dir`, or references to other data collections via `dc_ref`)
- **`EXPECTED_SCHEMA`** — required output columns and their Polars data types
- **`transform(sources)`** — a pure function that takes loaded DataFrames and returns the output DataFrame

Recipes are used in two ways:

1. **Standalone testing** — `depictio recipe run` executes a recipe locally against a data directory, so you can validate your data before registering a project.
2. **Project integration** — a `data_collection` with `source: "transformed"` tells the CLI to run the recipe during `depictio run`, storing the result as a Delta Lake table.

---

## The 4-Checkpoint Validation Pipeline

Every recipe execution — whether via `depictio recipe run` or `depictio run` — runs through four automatic checkpoints:

| # | Checkpoint | What it checks |
|---|-----------|----------------|
| 1 | **Load** | Import the recipe module; verify `SOURCES`, `EXPECTED_SCHEMA`, and a callable `transform()` exist |
| 2 | **Resolve** | Find each file under `--data-dir`; fail fast if any file is missing or empty |
| 3 | **Transform** | Call `transform(sources)`, verify it returns a non-empty `pl.DataFrame` |
| 4 | **Schema** | Assert every column in `EXPECTED_SCHEMA` is present with the correct dtype |

If any checkpoint fails, execution stops with a clear error message pointing to the exact problem.

---

## CLI Commands

### `depictio recipe list`

List all bundled recipes.

```bash
depictio recipe list
```

**Output:**

```
Available recipes (5):
  nf-core/ampliseq/alpha_diversity.py
  nf-core/ampliseq/alpha_rarefaction.py
  nf-core/ampliseq/ancombc.py
  nf-core/ampliseq/taxonomy_composition.py
  nf-core/ampliseq/taxonomy_rel_abundance.py
```

---

### `depictio recipe info <name>`

Show recipe details: docstring, sources, and expected output schema.

```bash
depictio recipe info nf-core/ampliseq/alpha_diversity.py
```

**Output:**

```
Recipe: nf-core/ampliseq/alpha_diversity.py
Description: Transform QIIME2 alpha diversity vector to per-sample Faith PD table.

Sources (1):
  faith_pd: qiime2/diversity/alpha_diversity/faith_pd_vector/metadata.tsv (TSV)

Expected output schema (3 columns):
  sample: Utf8
  habitat: Utf8
  faith_pd: Float64
```

---

### `depictio recipe run <name>`

Execute a recipe against local data with all 4 validation checkpoints.

```bash
depictio recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results
```

**Options:**

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--data-dir` | `-d` | **required** | Root directory with workflow output files |
| `--output` | `-o` | `null` | Save result to `.parquet` or `.csv` file |
| `--head` | `-n` | `20` | Number of rows to display |

**Example with output:**

```bash
depictio recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results \
  --output alpha_diversity.parquet \
  --head 5
```

**Example output:**

```
  Loaded recipe: nf-core/ampliseq/alpha_diversity.py (1 source(s))
  Resolved source 'faith_pd': 48 rows x 3 columns
  Transform produced 48 rows x 3 columns
  Schema valid: sample(Utf8), habitat(Utf8), faith_pd(Float64)

shape: (5, 3)
┌─────────────┬────────────┬──────────┐
│ sample      ┆ habitat    ┆ faith_pd │
│ ---         ┆ ---        ┆ ---      │
│ str         ┆ str        ┆ f64      │
╞═════════════╪════════════╪══════════╡
│ SRR13122774 ┆ Groundwater┆ 12.3     │
│ SRR13122775 ┆ River      ┆ 8.7      │
│ ...         ┆ ...        ┆ ...      │
└─────────────┴────────────┴──────────┘

  Saved to alpha_diversity.parquet
```

<!-- prettier-ignore -->
!!! note "dc_ref sources"
    Recipes that reference another data collection via `dc_ref` (e.g. `taxonomy_rel_abundance.py`) cannot be fully executed standalone. The CLI will report which sources are skipped and exit with code 0. These sources are resolved automatically during `depictio run` when all data collections are available.

---

## Recipe Anatomy: Ampliseq Examples

The five bundled ampliseq recipes cover the full spectrum of transformation patterns. Study them as templates for writing your own recipes.

### Example 1 — Simple file transformation (`alpha_diversity.py`)

**Pattern:** Filter comment rows, rename columns, cast types.

Input: QIIME2 TSV with a `#` comment header row and an `id` column instead of `sample`.

```python
"""Transform QIIME2 alpha diversity vector to per-sample Faith PD table."""

import polars as pl

from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(
        ref="faith_pd",
        path="qiime2/diversity/alpha_diversity/faith_pd_vector/metadata.tsv",
        format="TSV",
    ),
]

EXPECTED_SCHEMA: dict[str, type[pl.DataType]] = {
    "sample": pl.Utf8,
    "habitat": pl.Utf8,
    "faith_pd": pl.Float64,
}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Transform raw Faith PD vector to clean per-sample table."""
    df = sources["faith_pd"]
    df = df.filter(~pl.col("id").str.starts_with("#"))  # drop comment rows
    df = df.rename({"id": "sample"})
    df = df.with_columns(pl.col("faith_pd").cast(pl.Float64))
    return df.select("sample", "habitat", "faith_pd")
```

---

### Example 2 — Wide-to-long reshape (`alpha_rarefaction.py`)

**Pattern:** Unpivot wide columns into long format with regex extraction.

Input: Wide CSV where columns are `depth-500_iter-3`, `depth-1000_iter-1`, etc.
Output: Long-format `(sample, depth, iter, faith_pd)` — ready for line charts.

```python
"""Transform QIIME2 alpha rarefaction wide CSV to long-format rarefaction curves."""

import polars as pl

from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(
        ref="faith_pd_csv",
        path="qiime2/alpha-rarefaction/faith_pd.csv",
        format="CSV",
    ),
]

EXPECTED_SCHEMA = {
    "sample": pl.Utf8,
    "depth": pl.Int64,
    "iter": pl.Int64,
    "faith_pd": pl.Float64,
}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Melt wide rarefaction table (depth-X_iter-Y columns) to long format."""
    df = sources["faith_pd_csv"]

    value_cols = [c for c in df.columns if c.startswith("depth-")]
    df = df.unpivot(
        on=value_cols, index="sample-id", variable_name="depth_iter", value_name="faith_pd"
    )
    df = df.rename({"sample-id": "sample"})

    # Extract depth and iter from column names like "depth-500_iter-3"
    df = df.with_columns(
        pl.col("depth_iter").str.extract(r"depth-(\d+)", 1).cast(pl.Int64).alias("depth"),
        pl.col("depth_iter").str.extract(r"iter-(\d+)", 1).cast(pl.Int64).alias("iter"),
        pl.col("faith_pd").cast(pl.Float64),
    )

    return df.drop_nulls(subset=["faith_pd"]).select("sample", "depth", "iter", "faith_pd")
```

---

### Example 3 — Cross-DC join via `dc_ref` (`taxonomy_rel_abundance.py`)

**Pattern:** Reference another data collection instead of a file, join on a shared key.

The `dc_ref="metadata"` entry tells the system to load the `metadata` data collection (by tag) and inject it into `sources` before calling `transform()`. This enables metadata enrichment without duplicating files.

```python
"""Transform QIIME2 relative abundance table to long-format per-sample taxonomy table."""

import polars as pl

from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(
        ref="rel_table",
        path="qiime2/rel_abundance_tables/rel-table-2.tsv",
        format="TSV",
        read_kwargs={"skip_rows": 1},
    ),
    RecipeSource(ref="metadata", dc_ref="metadata"),  # ← references another DC by tag
]

EXPECTED_SCHEMA = {
    "sample": pl.Utf8,
    "taxonomy": pl.Utf8,
    "rel_abundance": pl.Float64,
    "habitat": pl.Utf8,
    "Kingdom": pl.Utf8,
    "Phylum": pl.Utf8,
}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Unpivot wide abundance table and join with metadata."""
    df = sources["rel_table"]
    df = df.rename({"#OTU ID": "taxonomy"})

    sample_cols = [c for c in df.columns if c != "taxonomy"]
    df = df.with_columns([pl.col(c).cast(pl.Float64) for c in sample_cols])
    df = df.unpivot(
        on=sample_cols, index="taxonomy", variable_name="sample", value_name="rel_abundance"
    )
    df = df.filter(pl.col("rel_abundance").is_not_null() & (pl.col("rel_abundance") > 0))
    df = df.with_columns(
        pl.col("taxonomy").str.split(";").list.get(0).alias("Kingdom"),
        pl.col("taxonomy").str.split(";").list.get(1).fill_null("Unclassified").alias("Phylum"),
    )

    metadata = sources["metadata"]
    # Handle both column naming conventions (v2.14: "sample", v2.16+: "ID")
    if "ID" in metadata.columns and "sample" not in metadata.columns:
        metadata = metadata.rename({"ID": "sample"})
    metadata = metadata.select("sample", "habitat")

    return df.join(metadata, on="sample", how="left").select(
        "sample", "taxonomy", "rel_abundance", "habitat", "Kingdom", "Phylum"
    )
```

---

### Example 4 — Multi-file merge (`ancombc.py`)

**Pattern:** Merge multiple slices of the same analysis into one long-format table, compute derived columns.

Merges 5 separate ANCOM-BC result CSVs (lfc, p_val, q_val, w, se) into one differential abundance table with `-log10(q)` and significance flag.

```python
"""Merge ANCOM-BC differential abundance results (5 files) into one long-format table."""

import polars as pl

from depictio.models.models.transforms import RecipeSource

SOURCES = [
    RecipeSource(
        ref="lfc",
        path="qiime2/ancombc/differentials/Category-habitat-level-2/lfc_slice.csv",
        format="CSV",
    ),
    RecipeSource(
        ref="p_val",
        path="qiime2/ancombc/differentials/Category-habitat-level-2/p_val_slice.csv",
        format="CSV",
    ),
    RecipeSource(
        ref="q_val",
        path="qiime2/ancombc/differentials/Category-habitat-level-2/q_val_slice.csv",
        format="CSV",
    ),
    RecipeSource(
        ref="w",
        path="qiime2/ancombc/differentials/Category-habitat-level-2/w_slice.csv",
        format="CSV",
    ),
    RecipeSource(
        ref="se",
        path="qiime2/ancombc/differentials/Category-habitat-level-2/se_slice.csv",
        format="CSV",
    ),
]

EXPECTED_SCHEMA = {
    "id": pl.Utf8, "contrast": pl.Utf8,
    "lfc": pl.Float64, "p_val": pl.Float64, "q_val": pl.Float64,
    "w": pl.Float64, "se": pl.Float64,
    "Kingdom": pl.Utf8, "Phylum": pl.Utf8,
    "neg_log10_qval": pl.Float64, "significant": pl.Boolean,
}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    """Melt each ANCOM-BC slice and join into one table with taxonomy annotations."""
    contrast_cols = [c for c in sources["lfc"].columns if c not in ("id", "(Intercept)")]

    melted = {
        name: (
            sources[name]
            .select("id", *contrast_cols)
            .unpivot(on=contrast_cols, index="id", variable_name="contrast", value_name=name)
        )
        for name in ["lfc", "p_val", "q_val", "w", "se"]
    }

    result = melted["lfc"]
    for name in ["p_val", "q_val", "w", "se"]:
        result = result.join(melted[name], on=["id", "contrast"], how="left")

    for col_name in ["lfc", "p_val", "q_val", "w", "se"]:
        result = result.with_columns(pl.col(col_name).cast(pl.Float64))

    return result.with_columns(
        pl.col("id").str.split(";").list.get(0).alias("Kingdom"),
        pl.col("id").str.split(";").list.get(1).fill_null("Unclassified").alias("Phylum"),
        (-pl.col("q_val").log(base=10)).alias("neg_log10_qval"),
        (pl.col("q_val") < 0.05).alias("significant"),
    ).select(
        "id", "contrast", "lfc", "p_val", "q_val", "w", "se",
        "Kingdom", "Phylum", "neg_log10_qval", "significant",
    )
```

---

## `RecipeSource` Reference

`RecipeSource` is the Pydantic model that describes one input to a recipe.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ref` | `str` | yes | Key in the `sources` dict passed to `transform()` |
| `path` | `str` | if no `dc_ref` | File path relative to `--data-dir` |
| `dc_ref` | `str` | if no `path` | Tag of another data collection to inject (resolved by the API) |
| `format` | `str` | yes if `path` set | `CSV`, `TSV`, or `Parquet` (case-insensitive) |
| `read_kwargs` | `dict` | no | Extra kwargs forwarded to the Polars reader (e.g. `{"skip_rows": 1}`) |

Exactly one of `path` or `dc_ref` must be set per source.

---

## Declaring a Recipe in `project.yaml`

To use a recipe in a project, set `source: "transformed"` on the data collection and specify the recipe name under `transform.recipe`:

```yaml
data_collections:
  - data_collection_tag: "alpha_diversity"
    description: "Per-sample alpha diversity (from raw QIIME2 Faith PD vector)"
    config:
      type: "Table"
      source: "transformed"
      transform:
        recipe: "nf-core/ampliseq/alpha_diversity.py"
        # Optional: override a source file path
        source_overrides:
          faith_pd:
            path: "custom/path/to/faith_pd_vector/metadata.tsv"
      dc_specific_properties:
        format: "TSV"
        columns_description:
          "sample": "Sample identifier"
          "habitat": "Habitat type"
          "faith_pd": "Faith's Phylogenetic Diversity"
```

The recipe is executed during `depictio data process` (Step 5 of `depictio run`). All 4 checkpoints run automatically. If the recipe fails, the data collection is skipped and an error is logged.

<!-- prettier-ignore -->
!!! tip "Using templates"
    For nf-core/ampliseq, all five recipes are pre-configured in the bundled template. Use `depictio run --template nf-core/ampliseq/2.16.0 --data-root /your/data` to set up the complete project without writing any YAML. See [Templates](templates.md).

---

## Additional Resources

- **[Templates](templates.md)** — pre-packaged project configs that use recipes automatically
- **[YAML Examples](yaml-examples.md)** — recipe data collection patterns
- **[CLI Usage](../../depictio-cli/usage.md)** — full CLI command reference
