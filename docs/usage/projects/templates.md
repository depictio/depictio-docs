# <span style="color: #45B8AC;">:material-layers:</span> Templates

Templates are pre-packaged project configurations that let you set up a complete bioinformatics analysis project with a single command. A template bundles the project YAML, bundled dashboards, and referenced recipes for a specific pipeline version — so you get a working Depictio project from raw pipeline output in minutes.

## What is a Template?

A template is a `template.yaml` file (an extended project YAML) that ships inside Depictio under `depictio/projects/<pipeline>/<version>/`. It contains:

- A **`template:`** metadata block with variable declarations
- A **standard project configuration** (workflows, data collections, links) with `{DATA_ROOT}` placeholders throughout
- References to **bundled dashboard YAML** files
- References to **recipes** for data collections that need transformation

Running `depictio run --template <id> --data-root /your/data` resolves all `{DATA_ROOT}` placeholders, validates your data directory, and sets up the complete project automatically — including importing the bundled dashboards.

---

## Template YAML Structure

The `template:` block sits at the top of an otherwise-normal `project.yaml`. Below it is the standard project configuration with `{DATA_ROOT}` substituted at runtime.

```yaml
# Template metadata (parsed and removed before Project model validation)
template:
  template_id: "nf-core/ampliseq/2.16.0"
  description: "nf-core/ampliseq microbial community analysis template for 16S/ITS amplicon sequencing"
  version: "1.0.0"
  variables:
    - name: "DATA_ROOT"
      description: "Root directory containing ampliseq pipeline output data"
      required: true
  dashboards:
    - "dashboards/full_analysis.yaml"

# ============================================================================
# Standard project configuration with {DATA_ROOT} placeholders
# ============================================================================
name: "Ampliseq Microbial Community Analysis"
project_type: "advanced"
is_public: true
workflows:
  - name: "ampliseq"
    version: "2.16.0"
    engine:
      name: "nextflow"
      version: "24.10.4"
    data_location:
      structure: "flat"
      locations:
        - "{DATA_ROOT}"   # ← resolved at runtime
    data_collections:
      - data_collection_tag: "metadata"
        config:
          type: "Table"
          metatype: "Metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "{DATA_ROOT}/input/Metadata_full.tsv"
      - data_collection_tag: "alpha_diversity"
        config:
          type: "Table"
          source: "transformed"
          transform:
            recipe: "nf-core/ampliseq/alpha_diversity.py"
      # ... more data collections ...
```

---

## Using a Template

### Minimal usage

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run
```

### Override the bundled dashboard

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --dashboard /custom/my_dashboard.yaml
```

### Skip automatic dashboard import

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --skip-dashboard-import
```

### Set a custom project name

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --project-name "My Ampliseq Study 2026"
```

**Template flags reference:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--template` | `string` | yes (mutually exclusive with `--project-config-path`) | Template ID (e.g. `nf-core/ampliseq/2.16.0`) |
| `--data-root` | `path` | yes when `--template` is set | Root directory substituted for `{DATA_ROOT}` |
| `--dashboard` | `path` | no | Override default dashboard(s); repeatable for multiple files |
| `--skip-dashboard-import` | `flag` | no | Skip the automatic dashboard import step |
| `--project-name` | `string` | no | Custom project name (auto-generated from template if omitted) |

---

## 8-Step Template Workflow

When `--template` is set, `depictio run` adds an extra step 0 before the standard pipeline:

| Step | Name | Description |
|------|------|-------------|
| **0** | Template resolution | Load `template.yaml`, substitute `{DATA_ROOT}`, validate data directory structure |
| 1 | Config validation | Pydantic validation of the resolved project config |
| 2 | Authentication | Login + fetch JWT token |
| 3 | Project sync | Create or update project in MongoDB via API |
| 4 | File scan | Discover data collection files |
| 5 | Data process | Execute recipes, convert to Delta Lake |
| 6 | Join computation | Compute cross-DC joins |
| 7 | Finalize | Mark project as ready |
| **8** | Dashboard import | Import bundled dashboard YAML automatically |

Step 8 is skipped when `--skip-dashboard-import` is set.

---

## Template Origin Badge

Once a project is created from a template, the UI shows a badge on every dashboard card and in the dashboard settings drawer:

```
Template: nf-core/ampliseq/2.16.0
```

This provenance is stored in the `template_origin` field on the Project document in MongoDB, including:

- `template_id` — e.g. `"nf-core/ampliseq/2.16.0"`
- `template_version` — e.g. `"1.0.0"`
- `data_root` — the resolved path used at creation time
- `applied_at` — timestamp of project creation
- `config_snapshot` — frozen copy of the resolved config for reproducibility

---

## Available Templates

| Template ID | Pipeline | Version | Notes |
|-------------|----------|---------|-------|
| `nf-core/ampliseq/2.14.0` | 16S rRNA amplicon sequencing | 2.14.0 | Older column naming (`sample` instead of `ID` in metadata) |
| `nf-core/ampliseq/2.16.0` | 16S rRNA amplicon sequencing | 2.16.0 | Current; 7 data collections + 5 cross-DC links |

### Required directory structure for `nf-core/ampliseq/2.16.0`

```text
<DATA_ROOT>/
├── input/
│   └── Metadata_full.tsv                      # Sample metadata (ID, name, habitat, ...)
├── multiqc/                                    # MultiQC HTML report + data directory
│   └── multiqc_data/
│       └── multiqc.parquet                     # Auto-detected by MultiQC DC
└── qiime2/
    ├── alpha-rarefaction/
    │   └── faith_pd.csv                        # Rarefaction curves (wide CSV)
    ├── ancombc/
    │   └── differentials/
    │       └── Category-habitat-level-2/
    │           ├── lfc_slice.csv               # Log-fold change
    │           ├── p_val_slice.csv             # P-values
    │           ├── q_val_slice.csv             # FDR-adjusted p-values
    │           ├── se_slice.csv                # Standard errors
    │           └── w_slice.csv                 # W statistics
    ├── barplot/
    │   └── level-2.csv                         # Taxonomy barplot (wide CSV)
    ├── diversity/
    │   └── alpha_diversity/
    │       └── faith_pd_vector/
    │           └── metadata.tsv                # Faith PD per sample
    └── rel_abundance_tables/
        └── rel-table-2.tsv                     # Relative abundance table (wide TSV)
```

The template runs 5 recipes to transform raw QIIME2 outputs into dashboard-ready tables:

| Recipe | Input | Output columns |
|--------|-------|----------------|
| `alpha_diversity.py` | `faith_pd_vector/metadata.tsv` | `sample`, `habitat`, `faith_pd` |
| `alpha_rarefaction.py` | `alpha-rarefaction/faith_pd.csv` | `sample`, `depth`, `iter`, `faith_pd` |
| `taxonomy_composition.py` | `barplot/level-2.csv` | `sample`, `taxonomy`, `count`, `habitat` |
| `taxonomy_rel_abundance.py` | `rel-table-2.tsv` + metadata DC | `sample`, `taxonomy`, `rel_abundance`, `habitat`, `Kingdom`, `Phylum` |
| `ancombc.py` | 5 ANCOM-BC slice CSVs | `id`, `contrast`, `lfc`, `q_val`, `neg_log10_qval`, `significant`, ... |

And 5 cross-DC links for interactive filtering from the metadata table to all other data collections.

---

## Additional Resources

- **[Recipes](recipes.md)** — how to write and test recipes
- **[YAML Examples](yaml-examples.md#pattern-template-project)** — template YAML patterns
- **[Projects Guide](guide.md#template-projects)** — template projects in context
- **[CLI Usage](../../depictio-cli/usage.md)** — full `depictio run` reference
