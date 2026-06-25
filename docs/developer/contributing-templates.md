---
title: "Contributing a Template"
icon: material/view-dashboard-variant
description: "How to add a pipeline template to Depictio — a single-folder bundle of project config, recipes, and dashboards that turns a pipeline run into a complete analysis with one command."
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../../images/logo/templates_catalog_logo.png" alt="Depictio Templates">
  <h1 class="catalog-hero__title" id="contributing-a-template">Contributing a Template</h1>
</div>

A **template** turns a whole pipeline run into a ready-made Depictio project —
data collections, recipes, and dashboards — that a user sets up with a single
`depictio run --template …` command. Where a [catalog tool](contributing-a-tool.md)
wires up *one* tool's outputs, a template assembles *many* into a complete,
opinionated analysis for a specific pipeline.

Adding one is a **single-folder pull request** under
`depictio/projects/<pipeline>/<version>/`. Before you start, browse the existing
[Templates](../pipeline-templates/README.md) and skim the
[Recipes](../usage/projects/recipes.md) reference.

## The building blocks

Each template version is one folder:

| Path | Purpose |
|------|---------|
| `template.yaml` | **Required.** Project config + a `template:` block declaring variables (e.g. `DATA_ROOT`) and which dashboards to load. |
| `dashboards/*.yaml` | One or more dashboard layouts, exported from the UI. |
| `.db_seeds/*.json` | Pre-baked dashboard JSON so fresh deployments load instantly. Generated, not hand-written. |
| `recipes/*.py` | Optional reshapes for outputs that aren't already tidy. Shared across versions, with per-version overrides. |

A real template (`depictio/projects/nf-core/ampliseq/`):

```
nf-core/ampliseq/
├── recipes/                     # shared across all versions
│   ├── alpha_diversity.py
│   └── …
└── 2.16.0/
    ├── template.yaml            # the template definition
    ├── dashboards/
    │   └── full_analysis.yaml
    ├── .db_seeds/               # generated dashboard seeds
    │   └── dashboard_*.json
    ├── recipes/                 # version-specific overrides (optional)
    └── generate_seeds.sh        # bakes the seeds (see Step 5)
```

Recipe lookup is **versioned-then-shared**: Depictio tries
`<version>/recipes/<name>.py` first, then falls back to the shared
`recipes/<name>.py`. Only add a version-specific override when an output's schema
genuinely changes between pipeline versions.

## Step 1 — Scaffold the folder

```bash
mkdir -p depictio/projects/<pipeline>/<version>/dashboards
mkdir -p depictio/projects/<pipeline>/recipes
```

## Step 2 — Write `template.yaml`

It's a standard Depictio project YAML with an extra `template:` block on top.
Every file path uses `{DATA_ROOT}` (and any custom variables) so it resolves
against the user's run at runtime.

```yaml
# ── Template metadata ─────────────────────────────────────────────
template:
  template_id: "<pipeline>/<version>"        # e.g. nf-core/rnaseq/3.14.0
  description: "Short description for the template index"
  version: "1.0.0"                           # template version, not pipeline version
  variables:
    - name: "DATA_ROOT"
      description: "Root directory of the pipeline output"
      required: true
  dashboards:
    - "dashboards/main.yaml"                  # relative to this folder

# ── Standard project config with {DATA_ROOT} placeholders ─────────
name: "My Pipeline Analysis"
project_type: "advanced"
is_public: true
workflows:
  - name: "my-pipeline"
    version: "<version>"
    engine: { name: "nextflow", version: "24.10.4" }
    data_location:
      structure: "flat"
      locations: ["{DATA_ROOT}"]
    data_collections:
      - data_collection_tag: "metadata"
        config:
          type: "Table"
          metatype: "Metadata"
          scan: { mode: "single", scan_parameters: { filename: "{DATA_ROOT}/path/to/metadata.tsv" } }
      - data_collection_tag: "my_dc"
        config:
          type: "Table"
          source: "transformed"
          transform: { recipe: "<pipeline>/my_recipe.py" }
```

**Dry-run early** to confirm your scan patterns match real files and the right
data collections resolve — without ingesting anything:

```bash
depictio run --template <pipeline>/<version> --data-root /path/to/run --dry-run
```

## Step 3 — Write recipes (only for outputs that need reshaping)

Same recipe contract as the catalog: `SOURCES`, `EXPECTED_SCHEMA`, `transform`.

```python
"""Short description of what this recipe produces."""

import polars as pl
from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(ref="my_file", path="relative/path/from/DATA_ROOT/to/file.csv", format="CSV"),
]

EXPECTED_SCHEMA: dict[str, type[pl.DataType]] = {
    "sample": pl.Utf8,
    "value":  pl.Float64,
}

def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["my_file"]
    return df.select("sample", "value")        # exactly the EXPECTED_SCHEMA columns
```

Test it against real data before moving on (all four checkpoints — load →
resolve → transform → schema — must pass green):

```bash
depictio dev recipe info <pipeline>/my_recipe.py
depictio dev recipe run  <pipeline>/my_recipe.py --data-dir /path/to/run --head 10
```

## Step 4 — Build the dashboards

The fastest path is to build interactively and export:

1. Ingest the run without importing dashboards:
   `depictio run --template <id> --data-root <path> --skip-dashboard-import`
2. Build the dashboard in the Depictio UI.
3. **Dashboard settings → Export YAML**, and save it as `dashboards/main.yaml`.

## Step 5 — Bake the seeds

Fresh deployments load dashboards from `.db_seeds/*.json`, not from the YAML — so
regenerate them whenever the dashboards change. Each template ships a
`generate_seeds.sh` that ingests a test run, exports the resulting dashboard
documents, and remaps them to static reference IDs. Model yours on an existing
one (e.g. `nf-core/ampliseq/2.16.0/generate_seeds.sh`):

```bash
bash depictio/projects/<pipeline>/<version>/generate_seeds.sh /path/to/test-run
```

It needs a local stack (API + MongoDB) and the CLI admin token — see the script
header for prerequisites.

## Step 6 — Test end-to-end & open a PR

```bash
depictio run --template <pipeline>/<version> --data-root /path/to/run
```

Check before submitting:

- [ ] `template_id` follows `<org>/<pipeline>/<version>`.
- [ ] Every recipe has a docstring and a typed `EXPECTED_SCHEMA`; `depictio dev recipe run` passes for each.
- [ ] Dashboard YAML **and** the regenerated `.db_seeds/*.json` are committed.
- [ ] No hardcoded absolute paths — only `{DATA_ROOT}` / template variables.
- [ ] A full `depictio run --template …` completes without error and dashboards render with the template badge.

In the PR, include: the pipeline name + docs link, the version tested, the
reference dataset used (e.g. an nf-core AWS results URL), and a screenshot of at
least one dashboard.

## Badge promotion

Submitted templates start **Experimental** and are promoted as they're reviewed
and tested:

| Badge | Criteria |
|-------|----------|
| :material-flask:{ style="color: #FF9800" } **Experimental** | PR submitted; CI passes; basic recipe validation |
| :material-check-circle:{ style="color: #4CAF50" } **Verified** | Reviewed by a core team member; schema tested; dashboards render correctly |
| :material-check-decagram:{ style="color: #45B8AC" } **Official** | Built or co-built by the core team; tested against official reference data; supported across releases |

## Getting help

- Open a [GitHub Discussion](https://github.com/depictio/depictio/discussions) and tag your PR `template`.
- Reference implementation: `depictio/projects/nf-core/ampliseq/`.
