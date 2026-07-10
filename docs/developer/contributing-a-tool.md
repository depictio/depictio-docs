---
title: "Contributing a Tool"
icon: material/hammer-wrench
description: "How to add a bioinformatics tool to the Depictio Tools Catalog — module.yaml, per-output YAML, and a fixture, validated in CI."
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../../images/logo/tools_catalog_logo.png" alt="Depictio Tools Catalog">
  <h1 class="catalog-hero__title" id="contributing-a-tool">Contributing a Tool</h1>
</div>

This guide explains how to add a bioinformatics **tool** to the
[Tools Catalog](../catalog/index.md). A tool entry tells Depictio how to
recognise a pipeline's output files and turn them into ready-made dashboard
renders — so users get visualizations automatically, with no manual wiring.

Adding a tool is a **single-folder pull request** under
`depictio/catalog/<tool>/` — no Depictio internals to learn, and no Python
unless an output needs reshaping. Everything is validated in CI by
`depictio-cli dev catalog validate`.

!!! tip "Fastest path: Catalog Studio"
    You don't have to write these files by hand. [**Catalog Studio**](catalog-studio.md)
    is a no-YAML web app that generates exactly the files below — import an
    nf-core module, upload a fixture, design the renders on live previews, and
    open a one-click PR. The rest of this page documents **the files Studio
    generates, and how to write them by hand.**

## The files

A tool is one folder: `module.yaml` identifies it, and the rest repeat per
output file.

| File | One per | Purpose |
|------|---------|---------|
| `module.yaml` | tool | Tool **identity** — `id`, `name`, `nf_core_url`. |
| `<output>.yaml` | output | **`find`** the file, optional **`recipe`**, and the **`renders_as`** it offers. |
| `<output>.tsv` | output | **Fixture** — a small sample, so CI previews & checks every render. |
| `<output>.py` | output · optional | **Recipe** — only when the raw file needs reshaping. |

The `.tsv` fixture and `.py` recipe are **not alternatives** — they do different
jobs and a tool often ships both (the `ivar` example below has both). The recipe
is the only optional piece: skip it when the raw file is already tidy.

A real single-output tool (`depictio/catalog/ivar/`):

```
ivar/
├── module.yaml          # id: ivar, name: iVar, nf_core_url: …
├── variants_long.yaml   # find + recipe + renders_as
├── variants_long.py     # recipe: reshape variants_long_table.csv
└── variants_long.tsv    # fixture
```

## Step 1 — `module.yaml` (identity)

Keep it lightweight: homepage, bio.tools id and EDAM terms are derived from the
nf-core `meta.yml` that `nf_core_url` points at — don't duplicate them. Declare
an identity field here only to *override* a stale `meta.yml`.

```yaml
id: ivar
name: iVar
nf_core_url: https://github.com/nf-core/modules/tree/master/modules/nf-core/ivar/variants
```

For a tool with no single nf-core module (e.g. QIIME 2), declare the full
identity (`description`, `homepage`, `biotools_url`, `edam_topics`) here and set
`nf_core_url` per output instead.

## Step 2 — `<output>.yaml` (one per output file)

```yaml
id: ivar_variants_long                          # globally-unique; used as `use: ivar/variants_long`
mode: variants
description: Per-sample annotated variant calls (long table).
find: { filename: "variants_long_table.csv" }   # recognise the raw file
recipe: ivar/variants_long.py                   # optional — owns the output columns
fixture: variants_long.tsv                      # co-located bindable sample
renders_as:
  - { id: manhattan, component: advanced_viz, kind: manhattan, roles: {chr: CHROM, pos: POS, score: AF} }
  - { component: figure, visu_type: histogram, dict_kwargs: {x: AF, color: EFFECT} }
  - { component: card, column: AF, aggregation: average }
  - { component: table }
```

**`find`** — recognise the file by name or path:

```yaml
find: { filename: "variants_long_table.csv" }          # glob on the basename
find: { path_glob: "**/mosdepth/genome/*.coverage.tsv" } # glob on the path (supports **)
```

**`renders_as`** — each entry binds the output's columns to a dashboard
component (see the YAML above for full examples). Besides `component`, each takes:

| Component | Keys |
|-----------|------|
| `advanced_viz` | `kind` + `roles` |
| `figure` (UI) | `visu_type` + `dict_kwargs` |
| `figure` (code) | `code` (Python that sets `fig` from `df` + `px`) |
| `card` | `column` + `aggregation` |
| `table` | — |
| `multiqc` | `section` |

Give an `advanced_viz` render an optional `id:` to address it from a dashboard as
`use: <tool>/<id>` — e.g. the `id: manhattan` in the YAML above is referenced as
`use: ivar/manhattan`.

> **Schema-ownership rule:** if you set `recipe`, the recipe owns the columns —
> do **not** also declare `columns`. If the raw file is already tidy and bindable,
> skip the recipe and declare `columns: {NAME: Dtype, …}` (polars dtypes) instead.
> Validation rejects setting both.

## Step 3 — Recipe (only if the file needs reshaping)

A recipe is a small polars module co-located as `<output>.py`. It declares its
inputs, its output schema, and a `transform`:

```python
"""Reshape variants_long_table.csv into tidy, bindable columns."""

import polars as pl
from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(ref="variants_raw", glob_pattern="variants/*/variants_long_table.csv", format="CSV"),
]

EXPECTED_SCHEMA: dict[str, type[pl.DataType]] = {
    "sample": pl.Utf8, "CHROM": pl.Utf8, "POS": pl.Int64,
    "AF": pl.Float64, "GENE": pl.Utf8, "EFFECT": pl.Utf8,
}

def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["variants_raw"]
    return df.select(EXPECTED_SCHEMA.keys())   # exactly the EXPECTED_SCHEMA columns
```

`EXPECTED_SCHEMA` is what the catalog grounds every render binding against. This
is the same recipe contract used by [templates](contributing-templates.md). To
see a recipe's output columns while writing `roles`:
`depictio-cli dev catalog columns ivar/variants_long.py`.

## Step 4 — Fixture

Save a small, real sample of the output as `<output>.tsv` (`.csv` / `.parquet`
also work), co-located in the folder. It must contain every column your
`renders_as` binds to — CI reads its real columns to validate (and preview)
each render.

## Step 5 — Validate, preview, and open a PR

```bash
# Validate just your tool (load → find → recipe → render bindings)
depictio-cli dev catalog validate --path depictio/catalog/<tool>

# Live-preview an output rendered on its fixture
depictio-cli catalog preview <tool>_<output>

# Helpful while authoring
depictio-cli catalog list                 # every tool + output + render targets
depictio-cli catalog info <tool>          # one tool in detail
depictio-cli dev catalog match /path/run  # which outputs are recognised in a run
```

Tip — add this header to each catalog YAML for live validation and autocomplete
in your editor:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/depictio/depictio/main/depictio/catalog/catalog.schema.json
```

Before submitting, check:

- [ ] `module.yaml` has `id`, `name`, and (where applicable) `nf_core_url`.
- [ ] Each `<output>.yaml` has a unique `id`, a `find`, and at least one `renders_as`.
- [ ] On outputs that bind columns, set `recipe` **or** `columns` (declare one) — never both.
- [ ] A fixture is committed for every output that binds columns, covering all bound columns.
- [ ] Each bound column's dtype is compatible with the render role it fills (the `dev catalog validate` dtype check passes).
- [ ] `depictio-cli dev catalog validate --path depictio/catalog/<tool>` passes green.

In the PR, link the tool's nf-core module / homepage and note the pipeline whose
output you tested against.

## Reference

- In-repo: `depictio/catalog/README.md` (overview) and `depictio/catalog/SCHEMA.md` (full field reference).
- The component config reference: [Dashboard Components](../features/components.md).
- Questions: [GitHub Discussions](https://github.com/depictio/depictio/discussions) — tag your PR `catalog`.
