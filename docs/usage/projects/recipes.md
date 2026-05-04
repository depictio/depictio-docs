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

A recipe is a plain Python module that describes how to transform one or more raw files into a single tidy DataFrame. Each recipe lives in `depictio/projects/<pipeline>/recipes/` and declares:

- **`SOURCES`** — input files to read (paths relative to `--data-dir`, or references to other data collections via `dc_ref`)
- **`EXPECTED_SCHEMA`** — required output columns and their Polars data types
- **`OPTIONAL_SCHEMA`** *(optional)* — columns that may or may not be present (e.g. user-defined metadata columns)
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
| 2 | **Resolve** | Find each file under `--data-dir`; skip optional sources gracefully; fail fast if required files are missing |
| 3 | **Transform** | Call `transform(sources)`, verify it returns a non-empty `pl.DataFrame` |
| 4 | **Schema** | Assert every column in `EXPECTED_SCHEMA` is present with the correct dtype; validate `OPTIONAL_SCHEMA` columns if present |

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
Available recipes (6):
  nf-core/ampliseq/alpha_diversity.py
  nf-core/ampliseq/alpha_rarefaction.py
  nf-core/ampliseq/ancombc.py
  nf-core/ampliseq/taxonomy_composition.py
  nf-core/ampliseq/taxonomy_heatmap.py
  nf-core/ampliseq/taxonomy_rel_abundance.py
```

---

### `depictio recipe info <name>`

Show recipe details: docstring, sources, and expected output schema. Pass `--version` to inspect a version-specific override.

```bash
depictio recipe info nf-core/ampliseq/alpha_diversity.py
```

**Output:**

```
Recipe: nf-core/ampliseq/alpha_diversity.py
Description: Transform QIIME2 alpha diversity vector to per-sample Faith PD table.

Sources (1):
  faith_pd: qiime2/diversity/alpha_diversity/faith_pd_vector/metadata.tsv (TSV)

Expected output schema (2 columns):
  sample: Utf8
  faith_pd: Float64

Optional schema: {} (metadata columns passed through dynamically)
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
| `--version` | `-v` | `null` | Pipeline version for version-specific recipe (e.g. `2.14.0`) |
| `--output` | `-o` | `null` | Save result to `.parquet` or `.csv` file |
| `--head` | `-n` | `20` | Number of rows to display |

<!-- prettier-ignore -->
!!! note "dc_ref sources"
    Recipes that reference another data collection via `dc_ref` (e.g. `taxonomy_rel_abundance.py`) cannot be fully executed standalone. The CLI will report which sources are skipped and exit with code 0. These sources are resolved automatically during `depictio run` when all data collections are available.

---

## Recipe Anatomy: Ampliseq Examples

The six bundled ampliseq recipes cover the full spectrum of transformation patterns. Study them as templates for writing your own recipes.

### Example 1 — Simple file transformation (`alpha_diversity.py`)

**Pattern:** Filter comment rows, rename columns, cast types. Metadata columns embedded by the pipeline are passed through dynamically.

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
    "faith_pd": pl.Float64,
}
# Any metadata columns embedded by QIIME2 (e.g. habitat) are passed through.
OPTIONAL_SCHEMA: dict[str, type[pl.DataType]] = {}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["faith_pd"]
    df = df.filter(~pl.col("id").str.starts_with("#"))
    df = df.rename({"id": "sample"})
    df = df.with_columns(pl.col("faith_pd").cast(pl.Float64))
    return df  # all columns preserved, including any embedded metadata
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
    df = sources["faith_pd_csv"]
    value_cols = [c for c in df.columns if c.startswith("depth-")]
    df = df.unpivot(
        on=value_cols, index="sample-id", variable_name="depth_iter", value_name="faith_pd"
    )
    df = df.rename({"sample-id": "sample"})
    df = df.with_columns(
        pl.col("depth_iter").str.extract(r"depth-(\d+)", 1).cast(pl.Int64).alias("depth"),
        pl.col("depth_iter").str.extract(r"iter-(\d+)", 1).cast(pl.Int64).alias("iter"),
        pl.col("faith_pd").cast(pl.Float64),
    )
    return df.drop_nulls(subset=["faith_pd"]).select("sample", "depth", "iter", "faith_pd")
```

---

### Example 3 — Cross-DC join with optional metadata (`taxonomy_rel_abundance.py`)

**Pattern:** Reference another data collection via `dc_ref`, join generically on a shared key. The metadata source is **optional** — when absent, the recipe produces core columns only.

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
    RecipeSource(
        ref="metadata",
        dc_ref="metadata",    # references another DC by tag
        optional=True,         # absent when no metadata provided
    ),
]

EXPECTED_SCHEMA = {
    "sample": pl.Utf8,
    "taxonomy": pl.Utf8,
    "rel_abundance": pl.Float64,
    "Kingdom": pl.Utf8,
    "Phylum": pl.Utf8,
}
# Metadata columns are user-defined; validated dynamically
OPTIONAL_SCHEMA: dict[str, type[pl.DataType]] = {}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["rel_table"]
    df = df.rename({"#OTU ID": "taxonomy"})
    sample_cols = [c for c in df.columns if c != "taxonomy"]
    df = df.with_columns(pl.col(sample_cols).cast(pl.Float64))
    df = df.unpivot(
        on=sample_cols, index="taxonomy", variable_name="sample", value_name="rel_abundance"
    )
    df = df.filter(pl.col("rel_abundance").is_not_null() & (pl.col("rel_abundance") > 0))
    df = df.with_columns(
        pl.col("taxonomy").str.split(";").list.get(0).alias("Kingdom"),
        pl.col("taxonomy").str.split(";").list.get(1).fill_null("Unclassified").alias("Phylum"),
    )

    # Join ALL metadata columns generically when metadata is available
    metadata = sources.get("metadata")
    if metadata is not None:
        metadata = metadata.rename({"ID": "sample"})
        df = df.join(metadata, on="sample", how="left")

    core = ["sample", "taxonomy", "rel_abundance", "Kingdom", "Phylum"]
    extra = [c for c in df.columns if c not in core]
    return df.select(core + extra)
```

---

### Example 4 — Multi-file merge with source overrides (`ancombc.py`)

**Pattern:** Merge multiple slices of the same analysis into one long-format table. The recipe declares default source paths, but the **template overrides them** via `source_overrides` to parameterize the directory name with `{GROUP_COL}`.

```python
"""Merge ANCOM-BC differential abundance results (5 files) into one long-format table."""

import polars as pl
from depictio.models.models.transforms import RecipeSource

# Default paths — overridden by template.yaml source_overrides with {GROUP_COL}
SOURCES = [
    RecipeSource(ref="lfc", path="qiime2/ancombc/differentials/Category-habitat-level-2/lfc_slice.csv", format="CSV"),
    RecipeSource(ref="p_val", path="qiime2/ancombc/differentials/Category-habitat-level-2/p_val_slice.csv", format="CSV"),
    RecipeSource(ref="q_val", path="qiime2/ancombc/differentials/Category-habitat-level-2/q_val_slice.csv", format="CSV"),
    RecipeSource(ref="w", path="qiime2/ancombc/differentials/Category-habitat-level-2/w_slice.csv", format="CSV"),
    RecipeSource(ref="se", path="qiime2/ancombc/differentials/Category-habitat-level-2/se_slice.csv", format="CSV"),
]

EXPECTED_SCHEMA = {
    "id": pl.Utf8, "contrast": pl.Utf8,
    "lfc": pl.Float64, "p_val": pl.Float64, "q_val": pl.Float64,
    "w": pl.Float64, "se": pl.Float64,
    "Kingdom": pl.Utf8, "Phylum": pl.Utf8,
    "neg_log10_qval": pl.Float64, "significant": pl.Boolean,
}


def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    contrast_cols = [c for c in sources["lfc"].columns if c not in ("id", "(Intercept)")]
    melted = {
        name: sources[name].select("id", *contrast_cols)
            .unpivot(on=contrast_cols, index="id", variable_name="contrast", value_name=name)
        for name in ["lfc", "p_val", "q_val", "w", "se"]
    }
    result = melted["lfc"]
    for name in ["p_val", "q_val", "w", "se"]:
        result = result.join(melted[name], on=["id", "contrast"], how="left")

    return result.with_columns(
        pl.col("id").str.split(";").list.get(0).alias("Kingdom"),
        pl.col("id").str.split(";").list.get(1).fill_null("Unclassified").alias("Phylum"),
        (-pl.col("q_val").log(base=10)).alias("neg_log10_qval"),
        (pl.col("q_val") < 0.05).alias("significant"),
    ).select("id", "contrast", "lfc", "p_val", "q_val", "w", "se",
             "Kingdom", "Phylum", "neg_log10_qval", "significant")
```

<!-- prettier-ignore -->
!!! note "Source overrides"
    The `Category-habitat-level-2` directory name in the default SOURCES paths is a fallback. In the ampliseq template, these paths are overridden to `Category-{GROUP_COL}-level-2/` so they resolve dynamically based on the user's metadata grouping column.

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
| `optional` | `bool` | no | If `true`, source is skipped when unavailable instead of failing |
| `glob_pattern` | `str` | no | Glob pattern for matching multiple files (concatenated) |

Exactly one of `path`, `dc_ref`, or `glob_pattern` must be set per source.

### `glob_pattern` (per-sample inputs)

Use `glob_pattern` instead of `path` to fan multiple per-sample files
into one DataFrame. The glob is expanded by the recipe runner relative
to the project's `data_dir` (typically `--data-root`):

```python
SOURCES: list[RecipeSource] = [
    RecipeSource(
        ref="pangolin_raw",
        glob_pattern="variants/ivar/consensus/bcftools/pangolin/*.pangolin.csv",
        format="CSV",
    ),
]
```

Matched files are read individually and concatenated with
`pl.concat([...], how="diagonal_relaxed")`. `glob_pattern` is mutually
exclusive with `path` and `dc_ref`.

---

## Declaring a Recipe in `project.yaml`

To use a recipe in a project, set `source: "transformed"` on the data collection and specify the recipe name under `transform.recipe`:

```yaml
data_collections:
  - data_collection_tag: "alpha_diversity"
    description: "Per-sample alpha diversity"
    config:
      type: "Table"
      source: "transformed"
      transform:
        recipe: "nf-core/ampliseq/alpha_diversity.py"
      dc_specific_properties:
        format: "TSV"
        columns_description:
          "sample": "Sample identifier"
          "faith_pd": "Faith's Phylogenetic Diversity"
```

Use `source_overrides` to parameterize recipe source paths via template variables:

```yaml
  - data_collection_tag: "ancombc_results"
    config:
      type: "Table"
      source: "transformed"
      transform:
        recipe: "nf-core/ampliseq/ancombc.py"
        source_overrides:
          lfc:
            path: "qiime2/ancombc/differentials/Category-{GROUP_COL}-level-2/lfc_slice.csv"
          # ... one override per source ref
```

The recipe is executed during `depictio data process` (Step 5 of `depictio run`). All 4 checkpoints run automatically. If the recipe fails, the data collection is skipped and an error is logged.

<!-- prettier-ignore -->
!!! tip "Using templates"
    For nf-core/ampliseq, all six recipes are pre-configured in the bundled template. Use `depictio run --template nf-core/ampliseq/2.16.0 --data-root /your/data --var SAMPLESHEET_FILE=samplesheet.csv` to set up the complete project without writing any YAML. See [Templates](templates.md).

---

## Recipe File Locations

Recipes live inside the `depictio/projects/` directory, co-located with the templates that use them:

```
depictio/projects/
└── nf-core/
    └── ampliseq/
        ├── recipes/                          ← shared recipes (all pipeline versions)
        │   ├── alpha_diversity.py
        │   ├── alpha_rarefaction.py
        │   ├── ancombc.py
        │   ├── taxonomy_composition.py
        │   ├── taxonomy_heatmap.py
        │   └── taxonomy_rel_abundance.py
        ├── 2.14.0/
        │   ├── template.yaml
        │   └── recipes/                      ← version-specific overrides
        │       └── taxonomy_rel_abundance.py
        └── 2.16.0/
            ├── template.yaml                 ← no overrides, inherits shared
            └── dashboards/
                ├── base.yaml                 ← minimal (no metadata)
                └── full_analysis.yaml        ← metadata-aware with {GROUP_COL}
```

To add a recipe for a new pipeline, create `depictio/projects/{org}/{pipeline}/recipes/{name}.py` following the contract: define `SOURCES`, `EXPECTED_SCHEMA`, and `transform()`.

---

## Version-Specific Recipes

When a pipeline output format changes between versions (column renames, file moves, schema changes), you can add a version-specific override without touching the shared recipe.

**Resolution order** when running pipeline version `2.14.0`:

1. `projects/{pipeline}/2.14.0/recipes/{name}.py` — checked first (override)
2. `projects/{pipeline}/recipes/{name}.py` — used if no override exists (shared)

Most recipes are shared across all versions. Only the ones that actually differ need an override.

To test a version-specific recipe standalone:

```bash
# Uses shared recipe
depictio recipe run nf-core/ampliseq/taxonomy_rel_abundance.py --data-dir /data/run

# Uses the v2.14.0 override if it exists, falls back to shared otherwise
depictio recipe run nf-core/ampliseq/taxonomy_rel_abundance.py \
  --data-dir /data/run \
  --version 2.14.0
```

---

## Additional Resources

- **[Templates](templates.md)** — pre-packaged project configs that use recipes automatically
- **[YAML Examples](yaml-examples.md)** — recipe data collection patterns
- **[CLI Usage](../../depictio-cli/usage.md)** — full CLI command reference
