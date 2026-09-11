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
`depictio-cli run --template …` command. Where a [catalog tool](contributing-a-tool.md)
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
    └── recipes/                 # version-specific overrides (optional)
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
depictio-cli run --template <pipeline>/<version> --data-root /path/to/run --dry-run
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
depictio-cli dev recipe info <pipeline>/my_recipe.py
depictio-cli dev recipe run  <pipeline>/my_recipe.py --data-dir /path/to/run --head 10
```

## Step 4 — Build the dashboards

The fastest path is to build interactively and export:

1. Ingest the run without importing dashboards:
   `depictio-cli run --template <id> --data-root <path> --skip-dashboard-import`
2. Build the dashboard in the Depictio UI.
3. **Dashboard settings → Export YAML**, and save it as `dashboards/main.yaml`.

### Shortcut: export the whole bundle

If the project already exists on an instance, built by hand or from an earlier
run, `depictio-cli template export` writes the entire bundle in one go:

```bash
depictio-cli template export <project_id> \
  --template-id <pipeline>/<version> \
  --config ~/.depictio/admin_config.yaml \
  --data-root /path/to/run \
  -o depictio/projects
```

It strips runtime state, rewrites the data root as `{DATA_ROOT}` (and any
stored manifest URL as `{MANIFEST_URL}`), exports every dashboard as tag-based
YAML, synthesises the `template:` block, and refuses to emit a bundle that
would not re-instantiate. What comes out is a valid starting point; you still
edit the description, declare extra variables and conditionals, and add
recipes by hand. See
[Export a project as a template](../usage/projects/templates.md#export-a-project-as-a-template).

## Manifest-driven templates { #manifest-driven-templates }

A template does not have to expect a local directory tree. Declare a
`MANIFEST_URL` variable and give each data collection a `manifest` scan whose
`manifest_type` names the manifest `type` it consumes, by convention its own
tag:

```yaml
template:
  template_id: "<org>/<name>/<version>"
  description: "Short description for the template index"
  version: "1.0.0"
  variables:
    - name: "MANIFEST_URL"
      description: "URL of the Data Manifest (JSON or CSV) listing {id, type, url[, run]} entries"
      required: true
  dashboards:
    - "dashboards/main.yaml"

name: "My Manifest Analysis"
project_type: "basic"
workflows:
  - name: "manifest"
    engine: { name: "python" }
    data_location:
      structure: "flat"
      locations: ["{MANIFEST_URL}"]
    data_collections:
      - data_collection_tag: "samples"
        config:
          type: "Table"
          metatype: "Metadata"
          scan:
            mode: manifest
            scan_parameters:
              manifest_url: "{MANIFEST_URL}"
              manifest_type: "samples"
          dc_specific_properties:
            format: "CSV"
      - data_collection_tag: "measurements"
        optional: true
        config:
          type: "Table"
          scan:
            mode: manifest
            scan_parameters:
              manifest_url: "{MANIFEST_URL}"
              manifest_type: "measurements"
          dc_specific_properties:
            format: "CSV"
```

Such a template is instantiated with `--manifest <url or path>` on the CLI, or
from the **From Manifest** tab of the web UI (`POST /projects/from_manifest`).
The tab only lists templates in which at least one data collection uses a
`manifest` scan. Two things follow from the
[manifest contract](../usage/projects/remote-data.md#the-data-manifest-contract):

- Mark `optional: true` the collections the manifest may not cover. When the
  manifest has no rows of that `type`, the collection and the links referencing
  it are pruned and the ingestion report records why. A *required* collection
  with no rows fails the run instead, naming the missing type.
- Every collection built from the manifest carries the `depictio_manifest_id`
  column, so links between them can use the `direct` resolver on that column
  with no mapping.

There is no `{DATA_ROOT}` to validate against, so `expected_files` does not
apply; the preview step of the UI, or `dry_run: true` on the endpoint, plays
that role by reporting the coverage of the manifest against the template.

Do not over-think where the data must live: whoever instantiates the template
can override any collection's location with `--bind TAG=LOCATION`, whatever
scan mode the template declares.

## Step 5 — Test end-to-end & open a PR

```bash
depictio-cli run --template <pipeline>/<version> --data-root /path/to/run
```

Check before submitting:

- [ ] `template_id` follows `<org>/<pipeline>/<version>`.
- [ ] Every recipe has a docstring and a typed `EXPECTED_SCHEMA`; `depictio-cli dev recipe run` passes for each.
- [ ] Dashboard YAML is committed.
- [ ] No hardcoded absolute paths or URLs: only `{DATA_ROOT}`, `{MANIFEST_URL}` and other template variables.
- [ ] A full `depictio-cli run --template …` completes without error and dashboards render with the template badge.

In the PR, include: the pipeline name + docs link, the version tested, the
reference dataset used (e.g. an nf-core AWS results URL), and a screenshot of at
least one dashboard.

## Badge promotion

Submitted templates start **Experimental** and are promoted as they're reviewed
and tested:

| Badge | Criteria |
|-------|----------|
| <span style="white-space: nowrap">:material-flask-outline:{ style="color: #FF9800" } **Experimental**</span> | Shared as-is. PR submitted; feedback and PRs welcome. |
| <span style="white-space: nowrap">:material-check-circle-outline:{ style="color: #2196F3" } **Reviewed**</span> | Tested, CI passes, reviewed by the Depictio team or community. |
| <span style="white-space: nowrap">:material-shield-check:{ style="color: #4CAF50" } **Certified**</span> | Validated by the pipeline lead developer. Highest trust level. |

## Getting help

- Open a [GitHub Discussion](https://github.com/depictio/depictio/discussions) and tag your PR `template`.
- Reference implementation: `depictio/projects/nf-core/ampliseq/`.
