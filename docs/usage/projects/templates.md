# <span style="color: #45B8AC;">:material-layers:</span> Template System Reference

This page documents the **template YAML format** and resolution mechanics. For browsing available templates and quick start guides, see the [Template Catalog](../../pipeline-templates/README.md).

---

## What is a Template?

A template is a `template.yaml` file that ships inside Depictio under `depictio/projects/<pipeline>/<version>/`. It extends a standard project YAML with:

- A **`template:`** metadata block — variable declarations, conditionals, dashboard references
- **`{VAR_NAME}` placeholders** throughout the project config — resolved at runtime
- References to **bundled dashboard YAML** files — imported automatically
- References to **recipes** for transformed data collections

---

## Template Variables

Every template declares its own variables. Variable names are **template-specific** — each pipeline decides what it needs.

`DATA_ROOT` is the only universal variable (always required, set via `--data-root`). All others are passed via `--var KEY=VALUE`.

**Auto-detected variables:** When a metadata file is provided, the system reads its headers and auto-populates:

- `GROUP_COL` — first non-ID annotation column (overridable)
- `GROUP_COL_DISPLAY` — title-cased version for chart labels
- `ANNOTATION_COLS` — comma-separated list of all annotation columns

---

## Template YAML Structure

```yaml
template:
  template_id: "org/pipeline/version"
  description: "Human-readable description"
  version: "1.0.0"

  variables:
    - name: "DATA_ROOT"
      description: "Pipeline output root directory"
      required: true
    - name: "OPTIONAL_VAR"
      description: "An optional variable"
      required: false

  dashboards:
    - "dashboards/base.yaml"

  conditional:
    - if_var_absent: "OPTIONAL_VAR"
      remove_dc_tags: ["optional_dc"]
      dashboards: ["dashboards/base.yaml"]
    - if_var_present: "OPTIONAL_VAR"
      dashboards: ["dashboards/base.yaml", "dashboards/extended.yaml"]
```

Below the `template:` block is a standard project configuration with `{VAR_NAME}` placeholders.

---

## Conditionals

Conditionals adapt the project based on which optional variables the user provides. Each rule can:

- **Remove data collections** (`remove_dc_tags`) — and automatically prune any links referencing them
- **Override the dashboard list** (`dashboards`) — select different dashboard variants

Rules fire on `if_var_absent` (variable not provided) or `if_var_present` (variable provided).

---

## Source Overrides

When a recipe's source paths depend on a template variable, use `source_overrides`:

```yaml
transform:
  recipe: "org/pipeline/my_recipe.py"
  source_overrides:
    input_file:
      path: "results/Category-{GROUP_COL}-level-2/data.csv"
```

The recipe Python code stays generic — path resolution happens via variable substitution in the YAML.

---

## CLI Flags

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--template` | `string` | yes | Template ID (e.g. `nf-core/ampliseq/2.16.0`) |
| `--data-root` | `path` | yes | Root directory substituted for `{DATA_ROOT}` |
| `--var` | `KEY=VALUE` | depends on template | Pass template-specific variables; repeatable |
| `--dashboard` | `path` | no | Override default dashboard(s); repeatable |
| `--skip-dashboard-import` | `flag` | no | Skip automatic dashboard import |
| `--project-name` | `string` | no | Custom project name |

---

## Resolution Workflow

When `--template` is set, `depictio run` inserts **Step 0: Template resolution** before the standard pipeline:

| Step | Name | Description |
|------|------|-------------|
| **0** | Template resolution | Load YAML, substitute variables, auto-detect metadata columns, apply conditionals |
| 1 | Config validation | Pydantic validation of the resolved project config |
| 2 | Authentication | Login + fetch JWT token |
| 3 | Project sync | Create or update project on server |
| 4 | File scan | Discover data collection files |
| 5 | Data process | Execute recipes, write to Delta Lake |
| 6 | Join computation | Compute cross-DC joins |
| 7 | Finalize | Mark project as ready |
| **8** | Dashboard import | Import bundled dashboard YAML (with variable substitution) |

Dashboard YAML files also undergo variable substitution (e.g. `{GROUP_COL}` in filter columns, chart titles).

---

## Template Origin

Once a project is created from a template, the UI shows a template badge on dashboard cards and in the project data manager. This provenance is stored in the `template_origin` field:

- `template_id` — e.g. `"nf-core/ampliseq/2.16.0"`
- `template_version` — schema version
- `data_root` — the resolved path
- `variables` — all resolved variable values
- `applied_at` — timestamp
- `config_snapshot` — frozen copy of the resolved config

---

## Cross-DC Links

Templates define links between data collections using **tags** (not IDs):

```yaml
links:
  - source_dc_tag: "metadata"
    source_column: "ID"
    target_dc_tag: "alpha_diversity"
    target_type: "table"
    link_config:
      resolver: "direct"
      target_field: "sample"
```

Tags are resolved to MongoDB ObjectIds after the project is synced to the server. Links referencing removed DCs (via conditionals) are auto-pruned.

---

## Additional Resources

- **[Template Catalog](../../pipeline-templates/README.md)** — browse and use available templates
- **[Recipes](recipes.md)** — how to write and test data transformation recipes
- **[Contributing Templates](../../developer/contributing-templates.md)** — add a new template
- **[CLI Usage](../../depictio-cli/usage.md)** — full `depictio run` reference
