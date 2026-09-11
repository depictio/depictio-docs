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

`DATA_ROOT` is the usual root variable, set via `--data-root`. A manifest-driven template declares `MANIFEST_URL` instead, set via `--manifest`. All others are passed via `--var KEY=VALUE`. `--bind TAG=LOCATION` can stand in for either root variable by pointing each data collection at its own location; see [Instantiating with `--manifest` or `--bind`](#instantiating-with-manifest-or-bind).

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
| `--template` | `string` | yes | Template ID. Pin a version (`nf-core/ampliseq/2.16.0`), or use `nf-core/ampliseq/latest`, or just `nf-core/ampliseq`, to resolve the newest shipped version (v1.5.2+). On the CLI, also a path to an [exported bundle](#running-an-exported-bundle) |
| `--data-root` | `path` | one of the three | Root directory substituted for `{DATA_ROOT}` |
| `--manifest` | `url` or `path` | one of the three | Data Manifest substituted for `{MANIFEST_URL}`; mutually exclusive with `--data-root` |
| `--bind` | `TAG=LOCATION` | one of the three | Point one data collection at a location; the scan mode is inferred from its shape. Repeatable |
| `--var` | `KEY=VALUE` | depends on template | Pass template-specific variables; repeatable |
| `--dashboard` | `path` | no | Override default dashboard(s); repeatable |
| `--skip-dashboard-import` | `flag` | no | Skip automatic dashboard import |
| `--project-name` | `string` | no | Custom project name |

### Instantiating with `--manifest` or `--bind` { #instantiating-with-manifest-or-bind }

`--data-root`, `--manifest` and `--bind` all answer the same question, where
the data is, and a template run needs at least one of them:

```bash
# A manifest-driven template: no local root at all
depictio-cli run --template generic/manifest-tables/1 \
  --manifest https://data.example.org/run42/manifest.json

# Any template, each data collection pointed at its own location
depictio-cli run --template my-lab/rnaseq-qc/1 \
  --bind metadata=/data/run42/metadata.tsv \
  --bind samples=s3://my-bucket/run42/*.samples.csv
```

`--manifest` takes a URL or a local file path and becomes the `MANIFEST_URL`
variable. `--bind` is applied after resolution, so it wins over whatever
`{DATA_ROOT}` or `{MANIFEST_URL}` resolved to for that collection, and a
required variable that no collection uses any more is not asked for. A
`--bind` naming a tag the template does not declare is an error, listing the
tags that exist. The location shapes and the mode each one implies are on
[Remote data and manifests](remote-data.md#bind-a-data-collection-to-a-location).

### Running an exported bundle { #running-an-exported-bundle }

On the CLI, `--template` also accepts a path: a directory holding a
`template.yaml` (or `project.yaml`), or a YAML file. That is what makes an
[exported bundle](#export-a-project-as-a-template) usable by whoever receives
it, without copying it into an installation first:

```bash
depictio-cli run --template ./my-lab/rnaseq-qc/1 \
  --bind samples=s3://their-bucket/run7/*.samples.csv
```

An existing path wins over an installed template of the same name. The server
never accepts the path form: it resolves ids on behalf of remote callers, and
ids are confined to the templates directory in both contexts.

---

## Resolution Workflow

When `--template` is set, `depictio run` inserts **Step 0: Template resolution** before the standard pipeline:

| Step | Name | Description |
|------|------|-------------|
| **0** | Template resolution | Load YAML, substitute variables, auto-detect metadata columns, apply conditionals, then [materialise recipe seeds](#recipe-seeds) |
| 1 | Config validation | Pydantic validation of the resolved project config |
| 2 | Authentication | Login + fetch JWT token |
| 3 | Project sync | Create or update project on server |
| 4 | File scan | Discover data collection files |
| 5 | Data process | Execute recipes, write to Delta Lake |
| 6 | Join computation | Compute cross-DC joins |
| 7 | Finalize | Mark project as ready |
| **8** | Dashboard import | Import bundled dashboard YAML (with variable substitution) |

Dashboard YAML files also undergo variable substitution (e.g. `{GROUP_COL}` in filter columns, chart titles).

### Recipe seeds <small>(v1.6.0+)</small> { #recipe-seeds }

A reference template ships each recipe's *output* as a committed
`{DATA_ROOT}/{dc_tag}.tsv`, so the bundled projects can be explored without the
pipeline run behind them. Since **v1.6.0** `--template` reads those seeds, the way
first-boot seeding always did: where a seed exists for a `source: transformed`
data collection, the recipe is replaced by a plain scan of that file. The
collection keeps `source: transformed`, so the viewer still shows its lineage.

A data collection with no seed is left alone and its recipe runs as before. Seed
coverage is uneven: `nf-core/viralrecon/3.0.0` ships one for all ten of its
recipe collections, `nf-core/ampliseq/2.16.0` for sixteen of nineteen.

This runs *after* conditionals, so a collection a conditional gated out stays
gated out even with a seed sitting beside it.

!!! note "A seed is matched by name, not assumed"
    Only a `source: transformed` collection is redirected. A `{dc_tag}.tsv` next
    to a `source: native` collection of the same tag is that collection's own
    input, and is scanned normally.

!!! warning "Templates ship with the repository, not the wheel"
    The bundled projects live under `depictio/projects/`, which is not part of the
    published `depictio-cli` package. Re-ingesting a bundled project from its own
    directory works from a repository checkout or a container image that carries
    them.

---

## Template Origin

Once a project is created from a template, the UI shows a template badge on dashboard cards and in the project data manager. This provenance is stored in the `template_origin` field:

- `template_id` — e.g. `"nf-core/ampliseq/2.16.0"`
- `template_version` — schema version
- `data_root` — the resolved path
- `variables` — all resolved variable values
- `applied_at` — timestamp
- `config_snapshot` — frozen copy of the resolved config
- `run_provenance`: the pipeline's own run parameters, see below <small>(v1.8.3+)</small>

---

## Run provenance <small>(v1.8.3+)</small> { #run-provenance }

`template_origin` records how *Depictio* was invoked. **Run provenance** records
how the *pipeline* was, by reading the run's own parameter, version and recap
files and storing them as ordered entries on `template_origin.run_provenance`.

<!-- prettier-ignore -->
!!! note "Three different things are called provenance"
    This section is about **pipeline run parameters**. The
    [ingestion run](../administration/monitoring.md#ingestion) provenance is
    about how the CLI was invoked (host, CLI version, command line), and
    [Template Origin](#template-origin) above is about which template produced
    the project.

A template declares the recipe under `template.provenance`:

```yaml
template:
  provenance:
    sources:
      - name: "params"
        glob: "pipeline_info/params*.json"
        format: "json"
        pick: "latest"
        exclude_keys:
          - "*_ref_databases*"     # bulky reference-DB catalogs
      - name: "software_versions"
        glob: "pipeline_info/*software*versions.yml"
        format: "yaml"
        group: "Software versions"
    groups:
      - group: "Cutadapt (primer trimming)"
        key_patterns: ["FW_primer", "RV_primer", "cutadapt_*", "skip_cutadapt"]
      - group: "DADA2 (denoising & filtering)"
        key_patterns: ["trunclenf", "trunclenr", "trunc_qmin", "max_ee", "dada_*"]
    highlight:
      - "FW_primer"
      - "RV_primer"
      - "diversity_rarefaction_depth"
```

### `sources`

One entry per file, or file family, to read.

| Field | Default | Description |
|-------|---------|-------------|
| `name` | required | Label shown next to each entry |
| `glob` | required | Glob relative to `DATA_ROOT`, so one spec fits every run |
| `format` | `auto` | `json`, `yaml`, `tsv` (two-column key/value) or `auto`, by suffix |
| `pick` | `latest` | When the glob matches several files: `latest` (last in sorted order, which is chronological for nf-core timestamps), `first`, or `all` (merged in order, later wins) |
| `exclude_keys` | `[]` | fnmatch globs of keys to drop |
| `group` | unset | Put every key of this source in one group, bypassing the group rules |

Nested files are flattened to dotted keys.

### `groups`

Each rule assigns keys matching any of its `key_patterns` (fnmatch globs against
the flattened key) to a named group, in declaration order, first match winning.

### `highlight`

Keys surfaced inline in the dashboard's settings drawer. The full listing always
stays in the ingestion report.

<!-- prettier-ignore -->
!!! info "Complete by construction"
    `exclude_keys` is the only way a key is omitted. Everything else is kept, and
    keys no group rule matches land in a catch-all **Other** group rather than
    being dropped.

A template with no `provenance:` block gets a default spec: the latest
`pipeline_info/params*.json`, everything in one *Parameters* group.

### Files with no template

`--provenance-file` takes an arbitrary recap file, JSON, YAML or two-column TSV,
and lists its entries under a **User provided** group. The flag is repeatable.

```bash
depictio-cli run --provenance-file run_summary.yaml --provenance-file thresholds.tsv
```

### Where it surfaces

- **Ingestion report**: a *Run provenance* card, one accordion per group, with
  per-row copy, full-text search across keys and values, and the source files
  listed. See [Ingestion Report & Health](../../features/dashboards.md#ingestion-report-health).
- **Dashboard settings drawer**: a *Run parameters* row showing the highlighted
  keys inline, linking to the full report. See
  [Using the dashboard](../guides/dashboard_usage.md#dashboard-settings-drawer).

The bundled `nf-core/ampliseq` template ships a spec covering Cutadapt, DADA2,
taxonomy, QIIME2 filtering, diversity and rarefaction, differential abundance,
skipped steps and software versions.

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

## Export a project as a template { #export-a-project-as-a-template }

The inverse of instantiation: freeze a live project and its dashboards into a
template bundle. Build one good project interactively, export it, and the next
run of the same pipeline is one command.

=== "CLI"

    ```bash
    depictio-cli template export <project_id> \
      --template-id my-lab/rnaseq-qc/1 \
      --config ~/.depictio/admin_config.yaml \
      -o depictio/projects
    ```

    The bundle is unpacked into `<output-dir>/<template-id>/`. `--version`,
    `--description` and `--data-root` are optional; see the
    [CLI reference](../../depictio-cli/usage.md#template-commands).

=== "Web UI"

    On the project page, **Export as template**. The button is enabled for
    users who can edit the project and shown disabled otherwise, with an
    *Owner permission required* hint. The dialog asks for a template ID, a
    version, an optional description and an optional data root, then
    downloads the bundle as a zip.

=== "API"

    `POST /projects/{project_id}/export_template` with
    `{"template_id", "version", "description", "data_root"}` returns the zip.

### What the bundle contains

| Path | Content |
|------|---------|
| `template.yaml` | A synthesised `template:` block (id, description, version, variables, dashboard list) followed by the project configuration |
| `dashboards/*.yaml` | One file per main dashboard tab, child tabs included, referencing data collections by tag |

Runtime state is stripped: ids, permissions, file hashes, runs, registration
and modification timestamps, `template_origin`, `yaml_config_path`, the
generated `workflow_tag`, and the per-collection size metadata that ingestion
keeps on each data collection. Per-project storage credentials are never
exported.

Data bindings are re-parameterised. Stored manifest URLs become
`{MANIFEST_URL}`, declared as a required variable. A local path prefix becomes
`{DATA_ROOT}` when `--data-root` is given, or when the project itself came
from a template that recorded one. A template binds one manifest, so distinct
stored manifest URLs all collapse onto the same placeholder, with a warning.

### Round-trip guarantee

Before the bundle is returned it is checked against the same models
instantiation uses: the `template:` block must validate as template metadata,
and the configuration with placeholders substituted must validate as a
project. If either fails the request is rejected and nothing is emitted, so an
exported bundle always re-instantiates through the resolver. Drop the
directory under `depictio/projects/` and it is auto-discovered by the resolver
and the picker, or run it directly by path with `--template ./folder`.

---

## Additional Resources

- **[Template Catalog](../../pipeline-templates/README.md)** — browse and use available templates
- **[Remote data and manifests](remote-data.md)**: URL, prefix and manifest scan modes, `--bind`, sharing a project
- **[Recipes](recipes.md)** — how to write and test data transformation recipes
- **[Contributing Templates](../../developer/contributing-templates.md)** — add a new template
- **[CLI Usage](../../depictio-cli/usage.md)** — full `depictio run` reference
