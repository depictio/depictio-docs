# Contributing Templates

This guide explains how to create, test, and contribute a new template to Depictio.

A template bundles a pipeline-specific project configuration, recipes, and dashboards so that users can set up a complete analysis with a single command. Before writing your template, check [Templates](../pipeline-templates/README.md) to see what already exists.

The path from pipeline output to a merged template, at a glance:

1. **Analyse the pipeline output** — list the files a typical run produces.
2. **Write `template.yaml`** — declare variables and data collections.
3. **Dry-run** — `depictio run --dry-run` to confirm which DCs resolve for your data.
4. **Write recipes** — reshape raw outputs into the DC schemas.
5. **Build dashboards** and **bake seeds** with the template's `generate_seeds.sh`.
6. **Document** — write the narrative page, then run `gen_template_docs.py` to generate its reference tables.
7. **Open a PR**.

!!! tip "What fields actually exist"
    The per-pipeline reference pages (e.g. [nf-core/ampliseq](../pipeline-templates/nf-core/ampliseq.md#reference)) are **generated from each `template.yaml`** by `depictio/dev_scripts/gen_template_docs.py` — use them as the authoritative list of variables, data collections, conditional routes and recipe schemas. The Pydantic models in `depictio/models/models/templates.py` are the source of truth for which `template:` fields are valid.

---

## Prerequisites

- Depictio CLI installed and working (`depictio --version`)
- Access to real pipeline output data for testing
- Familiarity with [Recipes](../usage/projects/recipes.md)

---

## Directory layout

Templates live inside the Depictio repository under `depictio/projects/`:

```text
depictio/projects/
└── <pipeline>/                         # e.g. nf-core/ampliseq
    ├── recipes/                        # Shared recipes (all versions)
    │   ├── alpha_diversity.py
    │   └── ...
    └── <version>/                      # e.g. 2.16.0
        ├── template.yaml               # Required — defines the template
        ├── dashboards/                 # Dashboard YAML files
        │   └── full_analysis.yaml
        ├── .db_seeds/                  # Pre-built dashboard JSON seeds
        │   ├── dashboard_community.json
        │   └── ...
        └── recipes/                    # Version-specific recipe overrides (optional)
            └── taxonomy_rel_abundance.py
```

The recipe lookup follows a **versioned-then-shared fallback**: Depictio first looks for `<version>/recipes/<name>.py`; if not found, it falls back to the shared `recipes/<name>.py`. Only add version-specific overrides when the output schema genuinely differs between versions.

---

## Step 1 — Create the template directory

```bash
mkdir -p depictio/projects/<your-pipeline>/<version>/dashboards
mkdir -p depictio/projects/<your-pipeline>/recipes
```

---

## Step 2 — Write `template.yaml`

The `template.yaml` is a standard Depictio project YAML with an extra `template:` metadata block at the top.

```yaml
# ── Template metadata ────────────────────────────────────────────────────────
template:
  template_id: "<your-pipeline>/<version>"   # e.g. nf-core/rnaseq/3.14.0
  description: "Short description for the template index"
  version: "1.0.0"                           # template version, not pipeline version
  variables:
    - name: "DATA_ROOT"
      description: "Root directory of your pipeline output"
      required: true
  dashboards:
    - "dashboards/main.yaml"                 # relative to this directory

# ── Standard project config with {DATA_ROOT} placeholders ────────────────────
name: "My Pipeline Analysis"
project_type: "advanced"
is_public: true
workflows:
  - name: "my-pipeline"
    version: "<version>"
    engine:
      name: "nextflow"
      version: "24.10.4"
    data_location:
      structure: "flat"
      locations:
        - "{DATA_ROOT}"
    data_collections:
      - data_collection_tag: "metadata"
        config:
          type: "Table"
          metatype: "Metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "{DATA_ROOT}/path/to/metadata.tsv"
      - data_collection_tag: "my_transformed_dc"
        config:
          type: "Table"
          source: "transformed"
          transform:
            recipe: "<your-pipeline>/my_recipe.py"
```

Every file path under `data_location` and `scan_parameters` must use `{DATA_ROOT}` so they are resolved at runtime.

### Dry-run to see which collections resolve

Before writing any recipes, resolve the template against real data without ingesting anything:

```bash
depictio run \
  --template <your-pipeline>/<version> \
  --data-root /path/to/real/pipeline/output \
  --dry-run
```

In template mode this runs **Step 0** only — it resolves the template, applies the conditional routes, and logs the surviving data collections per workflow. Use it to confirm your scan patterns match real files and that the right DCs are kept/pruned for your run before investing in recipes.

---

## Step 3 — Write recipes

Each recipe is a plain Python module placed in `depictio/projects/<pipeline>/recipes/`.

```python
"""Short description of what this recipe produces."""

import polars as pl
from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(
        ref="my_file",
        path="relative/path/from/DATA_ROOT/to/file.csv",
        format="CSV",
    ),
]

EXPECTED_SCHEMA: dict[str, type[pl.DataType]] = {
    "sample": pl.Utf8,
    "value":  pl.Float64,
}

def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["my_file"]
    # ... reshape, rename, cast ...
    return df.select("sample", "value")
```

Test the recipe locally before moving on:

```bash
depictio dev recipe info <your-pipeline>/my_recipe.py
depictio dev recipe run <your-pipeline>/my_recipe.py --data-dir /path/to/real/data --head 10
```

All 4 checkpoints (load → resolve → transform → schema) must pass with green output.

See [Recipes](../usage/projects/recipes.md) for the full recipe reference and annotated examples.

---

## Step 4 — Build dashboards

Create at least one dashboard YAML under `dashboards/`. The easiest workflow:

1. Run the template manually against real data: `depictio run --template <id> --data-root <path> --skip-dashboard-import`
2. Use the Depictio UI to build the dashboard interactively
3. Export it: **Dashboard settings → Export YAML**
4. Save the exported YAML as `dashboards/main.yaml`

Regenerate the `.db_seeds/*.json` files so fresh deployments load the dashboards correctly. Each template version ships a `generate_seeds.sh` that ingests a test run and exports the resulting dashboard documents as seeds — model yours on an existing one (e.g. `depictio/projects/nf-core/ampliseq/2.16.0/generate_seeds.sh`):

```bash
bash depictio/projects/<pipeline>/<version>/generate_seeds.sh /path/to/test-data
```

!!! info "Why a script, not a single command"
    Seeding ingests the template against real data, then exports and remaps the Mongo dashboard documents to the static reference IDs so tiles resolve on a fresh deploy. The per-template `generate_seeds.sh` captures that sequence — see the script header for its prerequisites.

---

## Step 5 — Test end-to-end

Run the full template against real pipeline output:

```bash
depictio run \
  --template <your-pipeline>/<version> \
  --data-root /path/to/real/pipeline/output
```

Verify:
- [ ] All steps 0–8 complete without error
- [ ] Dashboards appear in the UI with the template badge
- [ ] Cross-DC filtering works across data collections
- [ ] Recipe outputs match expected schemas

---

## Step 6 — Document the template

Each pipeline gets a narrative page under `docs/pipeline-templates/nf-core/<pipeline>.md` in the [depictio-docs](https://github.com/depictio/depictio-docs) repo — intro, screenshots, and a dashboard-tab walkthrough. The **reference tables** (variables, data collections, conditional routes, cross-DC links, recipe schemas) are *not* hand-written: they are generated from your `template.yaml` so they never drift from the code.

From the `depictio` repo, with `depictio-docs` checked out alongside it:

```bash
python -m depictio.dev_scripts.gen_template_docs
```

This writes `docs/pipeline-templates/nf-core/_generated/<pipeline>-<version>.md`. Pull it into your narrative page with an mkdocs snippet:

```markdown
## Reference

--8<-- "pipeline-templates/nf-core/_generated/<pipeline>-<version>.md"
```

Re-run the script whenever you touch the template — `gen_template_docs.py --check` (exit 1 if any partial is stale) is available for a CI guard. Commit **both** the narrative page and the generated partial.

---

## Step 7 — Open a pull request

Before submitting, check:

- [ ] `template_id` follows the `<org>/<pipeline>/<version>` convention
- [ ] All recipe files have a module docstring and typed `EXPECTED_SCHEMA`
- [ ] `depictio dev recipe run` passes for all recipes against the reference dataset
- [ ] Dashboard YAML and `.db_seeds/*.json` are both committed
- [ ] Narrative page added and its generated reference partial regenerated (`gen_template_docs.py --check` passes)
- [ ] No hardcoded absolute paths — only `{DATA_ROOT}` placeholders

In the PR description, include:

- Pipeline name and link to the official docs
- Pipeline version tested
- Reference dataset used (e.g. nf-core AWS results URL)
- Screenshot of at least one dashboard

Submitted templates start as **Experimental** and are promoted to **Verified** after core review, then **Official** once tested against a reference dataset.

---

## Badge promotion criteria

| Badge | Criteria |
|-------|---------|
| :material-flask:{ style="color: #FF9800" } **Experimental** | PR submitted; CI passes; basic recipe validation |
| :material-check-circle:{ style="color: #4CAF50" } **Verified** | Reviewed by a core team member; schema tested; dashboard renders correctly |
| :material-check-decagram:{ style="color: #45B8AC" } **Official** | Developed or co-developed by core team; tested against official reference data; supported across releases |

---

## Getting help

- Open a [GitHub Discussion](https://github.com/depictio/depictio/discussions) for questions
- Tag your PR with `template` for routing to the right reviewer
- Check existing templates in `depictio/projects/nf-core/ampliseq/` as a reference implementation
