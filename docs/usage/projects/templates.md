# <span style="color: #45B8AC;">:material-layers:</span> Templates

Templates are pre-packaged project configurations that let you set up a complete bioinformatics analysis project with a single command. A template bundles the project YAML, bundled dashboards, and referenced recipes for a specific pipeline version — so you get a working Depictio project from raw pipeline output in minutes.

## What is a Template?

A template is a `template.yaml` file (an extended project YAML) that ships inside Depictio under `depictio/projects/<pipeline>/<version>/`. It contains:

- A **`template:`** metadata block with variable declarations, conditionals, and dashboard references
- A **standard project configuration** (workflows, data collections, links) with `{VAR_NAME}` placeholders
- References to **bundled dashboard YAML** files (one or more, selected by conditionals)
- References to **recipes** for data collections that need transformation

Running `depictio run --template <id> --data-root /your/data` resolves all placeholders, applies conditional rules, and sets up the complete project — including importing the bundled dashboards.

---

## Template Variables

Every template declares its own set of variables in the `template.variables` block. Variable names are **template-specific** — each pipeline template decides what it needs.

The only universal variable is **`DATA_ROOT`**, which is always required and set via `--data-root`. All other variables are passed via `--var KEY=VALUE` and depend on the template.

**Auto-detected variables:** When a template uses a metadata file variable, the system can auto-detect annotation columns from the file headers. The first annotation column becomes `GROUP_COL` (overridable via `--var GROUP_COL=...`), and all annotation columns are stored as `ANNOTATION_COLS`. This enables dashboard facetting and grouping without hardcoding column names.

---

## Template YAML Structure

The `template:` block sits at the top of an otherwise-normal `project.yaml`. It declares variables, conditionals, and dashboard references.

```yaml
template:
  template_id: "nf-core/ampliseq/2.16.0"
  description: "nf-core/ampliseq microbial community analysis template"
  version: "1.1.0"

  # Variables: each template declares its own
  variables:
    - name: "DATA_ROOT"
      description: "Root directory containing pipeline output"
      required: true
    - name: "SAMPLESHEET_FILE"
      description: "Path to ampliseq samplesheet CSV"
      required: true
    - name: "METADATA_FILE"
      description: "Path to sample metadata TSV. All non-ID columns become annotations."
      required: false
    - name: "GROUP_COL"
      description: "Metadata column for grouping/facetting. Auto-detected if not provided."
      required: false

  # Default dashboards (can be overridden by conditionals)
  dashboards:
    - "dashboards/base.yaml"

  # Conditionals: toggle DCs and dashboards based on which variables are provided
  conditional:
    - if_var_absent: "METADATA_FILE"
      remove_dc_tags: ["metadata", "ancombc_results"]
      dashboards: ["dashboards/base.yaml"]
    - if_var_present: "METADATA_FILE"
      dashboards: ["dashboards/base.yaml", "dashboards/full_analysis.yaml"]

# ============================================================================
# Standard project configuration with {VAR_NAME} placeholders
# ============================================================================
name: "Ampliseq Microbial Community Analysis"
project_type: "advanced"
workflows:
  - name: "ampliseq"
    data_collections:
      - data_collection_tag: "multiqc_data"
        config:
          type: "MultiQC"
          scan:
            scan_parameters:
              regex_config:
                pattern: "multiqc/multiqc_data/multiqc.parquet"

      - data_collection_tag: "metadata"
        optional: true          # excluded when METADATA_FILE is absent
        config:
          type: "Table"
          scan:
            scan_parameters:
              filename: "{METADATA_FILE}"

      - data_collection_tag: "ancombc_results"
        config:
          type: "Table"
          source: "transformed"
          transform:
            recipe: "nf-core/ampliseq/ancombc.py"
            source_overrides:     # parameterize recipe paths via template variables
              lfc:
                path: "qiime2/ancombc/differentials/Category-{GROUP_COL}-level-2/lfc_slice.csv"
              # ... (one override per source)
```

---

## Conditionals

Conditionals let a template adapt its project structure based on which optional variables the user provides. Each rule can:

- **Remove data collections** (`remove_dc_tags`) — and automatically prune any links referencing them
- **Override the dashboard list** (`dashboards`) — select different dashboard variants

Rules fire based on `if_var_absent` (variable not provided) or `if_var_present` (variable provided). This enables patterns like "include differential abundance analysis only when metadata is available."

---

## Source Overrides

When a recipe's source file paths depend on a template variable (e.g., the ANCOM-BC directory name depends on which metadata column was used for grouping), use `source_overrides` in the template YAML to parameterize them:

```yaml
transform:
  recipe: "nf-core/ampliseq/ancombc.py"
  source_overrides:
    lfc:
      path: "qiime2/ancombc/differentials/Category-{GROUP_COL}-level-2/lfc_slice.csv"
```

The recipe's Python code stays generic — the template YAML handles path resolution via variable substitution.

---

## Using a Template

### Minimal usage (no metadata)

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --var SAMPLESHEET_FILE=samplesheet.csv
```

### With metadata (auto-detects GROUP_COL)

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --var METADATA_FILE=Metadata.tsv
# → reads Metadata.tsv headers, first annotation column becomes GROUP_COL
# → enables metadata-aware dashboards and ANCOM-BC analysis
```

### Override the grouping column

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --var METADATA_FILE=Metadata.tsv \
  --var GROUP_COL=treatment
```

### Override bundled dashboards or skip import

```bash
# Use a custom dashboard instead
depictio run --template nf-core/ampliseq/2.16.0 --data-root /data \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --dashboard /custom/my_dashboard.yaml

# Skip automatic dashboard import
depictio run --template nf-core/ampliseq/2.16.0 --data-root /data \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --skip-dashboard-import
```

**Template flags reference:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--template` | `string` | yes (mutually exclusive with `--project-config-path`) | Template ID (e.g. `nf-core/ampliseq/2.16.0`) |
| `--data-root` | `path` | yes when `--template` is set | Root directory substituted for `{DATA_ROOT}` |
| `--var` | `KEY=VALUE` | depends on template | Pass template-specific variables; repeatable |
| `--dashboard` | `path` | no | Override default dashboard(s); repeatable |
| `--skip-dashboard-import` | `flag` | no | Skip the automatic dashboard import step |
| `--project-name` | `string` | no | Custom project name (auto-generated from template if omitted) |

---

## 8-Step Template Workflow

When `--template` is set, `depictio run` adds an extra step 0 before the standard pipeline:

!!! info "Step 0 — Template mode only"
    Before the standard pipeline runs, the CLI inserts **Step 0: Template resolution**. This step loads the `template.yaml`, substitutes all `{VAR_NAME}` placeholders, auto-detects metadata columns if applicable, applies conditional rules (removing DCs and selecting dashboards), and validates the data directory. Steps 1–8 are identical regardless of whether you use `--template` or `--project-config-path`.

| Step | Name | Description |
|------|------|-------------|
| **0** :material-new-box:{ title="Template mode only" } | **Template resolution** | Load template, substitute variables, apply conditionals, auto-detect metadata columns |
| 1 | Config validation | Pydantic validation of the resolved project config |
| 2 | Authentication | Login + fetch JWT token |
| 3 | Project sync | Create or update project in MongoDB via API |
| 4 | File scan | Discover data collection files |
| 5 | Data process | Execute recipes, convert to Delta Lake |
| 6 | Join computation | Compute cross-DC joins |
| 7 | Finalize | Mark project as ready |
| **8** | Dashboard import | Import bundled dashboard YAML (with variable substitution) |

Step 8 is skipped when `--skip-dashboard-import` is set. Dashboard YAML files also undergo variable substitution (e.g. `{GROUP_COL}` in filter columns).

---

## Template Origin Badge

Once a project is created from a template, the UI shows a badge on every dashboard card and in the dashboard settings drawer:

```
Template: nf-core/ampliseq/2.16.0
```

This provenance is stored in the `template_origin` field on the Project document in MongoDB, including:

- `template_id` — e.g. `"nf-core/ampliseq/2.16.0"`
- `template_version` — e.g. `"1.1.0"`
- `data_root` — the resolved path used at creation time
- `applied_at` — timestamp of project creation
- `config_snapshot` — frozen copy of the resolved config for reproducibility

---

## Available Templates

| Template ID | Pipeline | Version | DCs | Recipes | Notes |
|-------------|----------|---------|-----|---------|-------|
| `nf-core/ampliseq/2.14.0` | 16S rRNA amplicon sequencing | 2.14.0 | 7 | 5 | Older column naming |
| `nf-core/ampliseq/2.16.0` | 16S rRNA amplicon sequencing | 2.16.0 | 9 | 6 | Conditional metadata support, 5 cross-DC links |

### Required directory structure for `nf-core/ampliseq/2.16.0`

```text
<DATA_ROOT>/
├── samplesheet.csv                               # Pipeline samplesheet (--var SAMPLESHEET_FILE)
├── Metadata.tsv                                   # Sample metadata (optional, --var METADATA_FILE)
├── multiqc/
│   └── multiqc_data/
│       └── multiqc.parquet                        # Auto-detected by MultiQC DC
└── qiime2/
    ├── alpha-rarefaction/
    │   └── faith_pd.csv                           # Rarefaction curves (wide CSV)
    ├── ancombc/                                   # ⚠ Only when METADATA_FILE provided
    │   └── differentials/
    │       └── Category-<GROUP_COL>-level-2/      # Directory name matches GROUP_COL value
    │           ├── lfc_slice.csv
    │           ├── p_val_slice.csv
    │           ├── q_val_slice.csv
    │           ├── se_slice.csv
    │           └── w_slice.csv
    ├── barplot/
    │   └── level-2.csv                            # Taxonomy barplot (wide CSV)
    ├── diversity/
    │   └── alpha_diversity/
    │       └── faith_pd_vector/
    │           └── metadata.tsv                   # Faith PD per sample
    └── rel_abundance_tables/
        └── rel-table-2.tsv                        # Relative abundance table (wide TSV)
```

The template runs 6 recipes to transform raw QIIME2 outputs into dashboard-ready tables:

| Recipe | Input | Output columns |
|--------|-------|----------------|
| `alpha_diversity.py` | `faith_pd_vector/metadata.tsv` | `sample`, `faith_pd` + any embedded metadata cols |
| `alpha_rarefaction.py` | `alpha-rarefaction/faith_pd.csv` | `sample`, `depth`, `iter`, `faith_pd` |
| `taxonomy_composition.py` | `barplot/level-2.csv` | `sample`, `taxonomy`, `count` + any metadata cols |
| `taxonomy_rel_abundance.py` | `rel-table-2.tsv` + metadata DC | `sample`, `taxonomy`, `rel_abundance`, `Kingdom`, `Phylum` + metadata cols |
| `taxonomy_heatmap.py` | taxonomy_rel_abundance DC + metadata DC | `Phylum`, `Kingdom`, sample columns + `_col_annotations_json` |
| `ancombc.py` | 5 ANCOM-BC slice CSVs (via source_overrides) | `id`, `contrast`, `lfc`, `q_val`, `neg_log10_qval`, `significant`, ... |

And 5 cross-DC links for interactive filtering from the metadata table to all other data collections (auto-pruned when metadata is absent).

---

## Additional Resources

- **[Recipes](recipes.md)** — how to write and test recipes
- **[YAML Examples](yaml-examples.md#pattern-template-project)** — template YAML patterns
- **[Projects Guide](guide.md#template-projects)** — template projects in context
- **[CLI Usage](../../depictio-cli/usage.md)** — full `depictio run` reference
