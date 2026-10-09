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
`depictio ingest <results dir> --template …` command. Where a [catalog tool](contributing-a-tool.md)
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
└── 2.18.0/
    ├── template.yaml            # the template definition
    ├── dashboards/
    │   └── base.yaml
    ├── docs/
    │   └── dashboards.md        # what each tab shows, per route
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
depictio ingest /path/to/run --template <pipeline>/<version> --dry-run
```

## Step 3 — Write recipes (only for outputs that need reshaping)

Same recipe contract as the catalog: `SOURCES`, `OUTPUT_SCHEMA`, `transform`.

```python
"""Short description of what this recipe produces."""

import polars as pl
from depictio.models.models.transforms import RecipeSource

SOURCES: list[RecipeSource] = [
    RecipeSource(ref="my_file", path="relative/path/from/DATA_ROOT/to/file.csv", format="CSV"),
]

OUTPUT_SCHEMA: dict[str, type[pl.DataType]] = {
    "sample": pl.Utf8,
    "value":  pl.Float64,
}

def transform(sources: dict[str, pl.DataFrame]) -> pl.DataFrame:
    df = sources["my_file"]
    return df.select("sample", "value")        # exactly the OUTPUT_SCHEMA columns
```

Test it against real data before moving on (all five checkpoints, load →
resolve → input schema → transform → output schema, must pass green):

```bash
depictio dev recipe info <pipeline>/my_recipe.py
depictio dev recipe run  <pipeline>/my_recipe.py --data-dir /path/to/run --head 10
```

## Step 4 — Build the dashboards

nf-core templates share one layout, so read the
[Template authoring rules](#template-authoring-rules) before you start, and copy
the structure of the reference template, `nf-core/ampliseq/2.18.0/dashboards/base.yaml`.

1. Ingest the run without importing dashboards:
   `depictio ingest <path> --template <id> --skip dashboards`
2. Build the tabs in the Depictio UI, or write them in YAML from the reference.
   **Dashboard settings → Export YAML** turns a UI draft into YAML.
3. Save the result as `dashboards/base.yaml`, then replace every value that
   belongs to one run (a group column, a sample id column) with a template
   variable such as `{GROUP_COL}`.
4. Check it:

    ```bash
    depictio dashboard validate dashboards/base.yaml --offline
    pytest depictio/tests/models/test_template_conventions.py \
      depictio/tests/models/test_shipped_dashboard_yamls.py -k <pipeline>
    ```

5. Import it on a running server and open every tab.

## Step 5 — Test end-to-end & open a PR

```bash
depictio ingest /path/to/run --template <pipeline>/<version>
```

Check before submitting:

- [ ] `template_id` follows `<org>/<pipeline>/<version>`.
- [ ] Every recipe has a docstring and a typed `OUTPUT_SCHEMA`; `depictio dev recipe run` passes for each.
- [ ] Dashboard YAML is committed, follows the [Template authoring rules](#template-authoring-rules), and the template's `docs/dashboards.md` describes every tab.
- [ ] No hardcoded absolute paths — only `{DATA_ROOT}` / template variables.
- [ ] A full `depictio ingest <path> --template …` completes without error and dashboards render with the template badge.

In the PR, include: the pipeline name + docs link, the version tested, the
reference dataset used (e.g. an nf-core AWS results URL), and a screenshot of at
least one dashboard.

## Step 6 — Document the template

Every template gets one page, `docs/pipeline-templates/nf-core/<pipeline>.md` in
[depictio-docs](https://github.com/depictio/depictio-docs), registered in three
places: the nav in `mkdocs.yml`, a row in `pipeline-templates/nf-core/index.md`,
and a card in `pipeline-templates/README.md` carrying `data-tpl-name`,
`data-tpl-status`, `data-tpl-version` and `data-tpl-keywords`, which is what the
catalogue search, the status chips and the table view read.

Copy the skeleton from [ampliseq](../pipeline-templates/nf-core/ampliseq.md).
**Required** means every page has it; the two optional sections answer a question
most templates do not raise.

| Section | Presence | What goes in it |
|---|---|---|
| Front matter | <span class="gtd-badge gtd-req">required</span> | `title:` the domain name a reader would search for, and `hide: [navigation]` |
| `.template-banner` | <span class="gtd-badge gtd-req">required</span> | logo pair, title, subtitle, nf-co.re and GitHub links, status badge |
| Intro | <span class="gtd-badge gtd-req">required</span> | one sentence, then 4 to 6 `:material-*:` bullets, one per analysis area |
| Scope admonition | <span class="gtd-badge gtd-opt">optional</span> | `!!! info` or `!!! warning`, when the template covers one route of the pipeline only |
| `## Quick start` | <span class="gtd-badge gtd-req">required</span> | the `depictio ingest` that needs nothing but the results directory, and the Nextflow trigger beside it |
| `## Choosing a template` | <span class="gtd-badge gtd-opt">optional</span> | a table of `--template` ids, when the template ships under several |
| `## Reference` | <span class="gtd-badge gtd-req">required</span> | the picker, then one version block per version around its generated partial |
| `## Dashboard tabs` | <span class="gtd-badge gtd-req">required</span> | one content tab per dashboard tab, in dashboard order: summary line, screenshot, two or three sentences, `??? abstract` with the filters and sections |
| `## Running the pipeline` | <span class="gtd-badge gtd-req">required</span> | the `nextflow run` that produces the inputs, the `depictio ingest` that reads them, the pipeline usage link |
| `## Required data structure` | <span class="gtd-badge gtd-req">required</span> | a `text` tree of `<DATA_ROOT>/`, with the mandatory files called out |
| `## Test data` | <span class="gtd-badge gtd-opt">if shipped</span> | `download_test_data.sh` or the megatest prefix, and the run that follows |
| `## Additional resources` | <span class="gtd-badge gtd-req">required</span> | four links: nf-co.re, the AWS results, Template System Reference, Recipes |
| `## Authorship` | <span class="gtd-badge gtd-req">required</span> | developers, reviewers and maintainers, as `.tpl-credits` cards |

Four rules are easy to get wrong:

**Tab names, icons and colours are read, never chosen.** A tab is titled with its
`title` in `dashboards/base.yaml`, or `main_tab_name` for the first one, and
`tab_icon: mdi:chart-scatter-plot` with `tab_icon_color: indigo` becomes
`:material-chart-scatter-plot:{ .mc-indigo }`. A tab whose icon is the MultiQC
logo carries the logo image instead. Check the icon exists in the bundled Material
set before using it: `mdi:target-arrow` does not, `bullseye-arrow` is the same glyph.

**The reference is one block per version**, driven by the picker rather than by a
tab strip, with the include flush left inside it:

```markdown
<div class="tpl-version-block" data-version="2.18.0" markdown>

;--8<-- "pipeline-templates/nf-core/_generated/ampliseq-latest.md"

</div>
```

Generate those partials with
`python -m depictio.dev_scripts.gen_template_docs --docs-root <depictio-docs>`.
It rewrites every template, so stage only your own.

**Screenshots** live at
`docs/images/pipeline-templates/nf-core/<pipeline>/<tab_slug>_light.png`, named
after the tab they show, and are linked with
`{ .tpl-shot target="_blank" rel="noopener" }` so a full-height capture lands in
the scrollable frame instead of being cropped. Add the `_dark.png` twin, with
`#only-light` and `#only-dark`, when you have one.

**Keep it near 300 lines**, and no em dashes in new prose. The template's own
`docs/dashboards.md` is source material to condense, not to port: implementation
notes and megatest bookkeeping stay in the depictio repo.

## Template authoring rules { #template-authoring-rules }

Every nf-core template follows the same layout rules, so the dashboards of two
pipelines read alike. This section summarises them.
[RULES.md](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/RULES.md)
in the depictio repo is the full and authoritative list. nf-core/ampliseq
(`ampliseq/2.18.0/dashboards/base.yaml`) is the reference implementation: when a
rule leaves room for doubt, do what it does.

### The family of tabs

- The main tab is the **Overview** (`main_tab_name: Overview`). The family keeps
  `title: nf-core/<pipeline>`.
- Child tabs carry a `tab_group`. The first group is always `Data & QC`, then one
  or two analysis groups named for the pipeline, at most two words and five tabs each.
- The MultiQC report is a child tab named exactly `MultiQC`, in `Data & QC`. It holds
  MultiQC panels only. A pipeline without a MultiQC report has no such tab.
- `tab_order` runs without gaps inside a group, and the groups go from broad to narrow.
- Every child tab has a `subtitle` of at most 12 words: the question it answers.

### The Overview

At most 24 grid rows at compact width, in this order:

| Block | What it holds |
|---|---|
| Hero | One text: the pipeline title (its wordmark as `logo:` when Depictio ships one), one sentence on the run, a `[Run parameters](params:)` link |
| About | Two card texts side by side: *About this dashboard*, and *The run* with run facts from `{{param:…}}` and live values |
| Pipeline | A card text with a `::: steps` flow of 4 to 6 steps, each linking its parameters and its tab |
| Key figures | A filter bar (the group, then the sample) and 4 `headline` cards, each with a `caption`, a `link: tab:<Tab>` and a `description` |
| Findings | A filter bar, a findings text with [live values](../features/yaml-sync.md#text-live-values), then 4 figures, one per analysis tab, two equal tiles (w4) per row |
| How to read | One text: a heading per tab group, then one `[Tab](tab:Tab)` line per tab with its question |

```yaml
main_dashboard:
  title: nf-core/<pipeline>
  main_tab_name: Overview
  tab_icon: mdi:compass-outline
  filter_panel_default: collapsed
  content_width_default: compact
  show_tab_header: false
  category_colors:
    "{GROUP_COL}": auto
  filter_sections:
    - {name: Sample filters, persistent: true, pin: top, icon: mdi:filter-variant, color: teal}
  grid_sections:
    - {name: Key figures, appearance: plain, card_variant: headline, filter_bar: true, visible_filters: 2}
    - {name: Findings, appearance: plain, figure_style: minimal, filter_bar: true, visible_filters: 2}
    - {name: How to read this dashboard, appearance: plain}
    - {name: Sample sheet, persistent: true, pin: bottom, collapsed: true, exclude_tabs: [Overview]}
  components:
    - component_type: text
      section: Findings
      surface: card
      values:
        top: {dc: <tag>, column: <category>, aggregation: top, weight: <abundance>}
        top_share: {dc: <tag>, column: <category>, aggregation: top_share, weight: <abundance>, format: percent}
      body: |
        - **{{top_share}}** of reads are {{top}} – the dominant <category> [<Tab>](tab:<Tab>)
    - component_type: highlight
      section: Findings
      source_tab: <Tab>
      source_component: <index of a figure on that tab>
      caption: One sentence on what the figure shows.
```

- The filter bar of a section narrows that section only, and its description says
  so. The persistent `Sample filters` in the left panel narrow every tab.
- A highlight redraws a figure or an advanced visualization of another tab under
  the Overview's filters. It cannot show a MultiQC panel, a card or a table.
- Each figure says something the Key figures do not: prefer a tab's result (the
  volcano, the ordination) over a box of a number a card already shows.

### Child tabs

- One intro text at the top, full width: at most 3 sentences on the method, with a
  link to its tool, and on how to read the tab.
- Then a strip of 4 cards (or 2 wide ones), never 3. The MultiQC tab has none.
- Then at most 3 open sections, then collapsed ones: tables, record cards, per-sample
  details, route alternates. At most 20 rows are open by default.
- Each section says what it shows in its `description` (one sentence, at most 90
  characters). The intro is the only text tile of a child tab.
- A dense advanced visualization opens on its readable form (the tree on its
  summary), with the full view a switch away.

### Card styles

- Key figures use the `headline` variant, with a `composition`, `box_plot`,
  `coverage` or `threshold` secondary.
- A child tab's strip uses the `default` variant. Each card has its own icon, its own
  `icon_color` (a Mantine palette name) and a secondary chosen for what it says, with
  a `caption` naming that secondary.
- The icon is the watermark on the right: never `icon_style: badge`, and no
  `title_color`, `title_font_size` or `value_font_size`.
- A 0 to 1 share takes `format: percent` and a large count `format: si`, so a card
  prints `41%` and `214k`, not `0.41` and `214,173`
  ([number format](../features/yaml-sync.md)). A caption or description quotes the
  same unit as the card.
- A secondary with one value, a fraction printed as "of 1" or a ranking of long ids
  reads as a defect. RULES.md lists the fix for each.

### Filters

- Child tabs filter from the left panel only: the pinned, persistent `Sample filters`,
  plus at least one filter section on the tab's own data.
- Filter bars (`filter_bar: true`) appear on the Overview only, with at most 2
  visible controls. The group filter comes first.
- Every filter has an icon and a colour, `display: {icon_name: mdi:…, custom_color:
  <palette name>}`, and a column keeps its colour on every tab.
- A link whose target spells the sample with a stage suffix (a Picard
  `WT_REP1.mLb.mkD.sorted` against the sheet's `WT_REP1`) takes `resolver: pattern` and
  `pattern: "{sample}.mLb.mkD.sorted"`. A `direct` link there matches no row, and the
  filter silently stops reaching the tile.

### Colours

- [`category_colors`](../features/yaml-sync.md#category-colors) is declared once, on
  the Overview, and the child tabs inherit it.
- The group column takes `"{GROUP_COL}": auto`. A column with more than 8 values
  takes `"*": "auto:<abundance column>"`, with `Other` and `Unclassified` pinned grey.
- No per-figure colour map for a column `category_colors` covers, and no hardcoded
  colours elsewhere. Code figures read `depictio_category_colors` and
  `depictio_group_kwargs`.
- A sample-space embedding (a PCA, an MDS) colours its points by the group. When its
  data collection has no group column, the recipe adds one; the tile never draws a
  single colour.

### Viz controls

- Leave the placement unset: the controls [dock by tile width](../features/dashboards.md#viz-controls).
  Never set `controls_placement` or `advanced_viz_controls`.
- Advanced visualization tiles are `w: 8` (controls on the right) or `w: 3` to `w: 7`
  (controls on top). A sample correlation heatmap takes `w: 8`.
- Axes carry words, not column names: `effect_label`, `significance_label`,
  `axis_prefix`, `labels:`.
- A locus navigator opens with `default_region: first`, the whole first contig the data
  carries (in the assembly's order when the tile names one), never a contig or window
  from one run: a curated window opens empty on a run aligned to part of the genome.
  A file track reads its files only below its window (1 Mb for VCF), so the default
  region stays inside it, or `file_window_size` grows.

### Heights

- The stored `h` is a floor: the viewer fits text, cards, tables and advanced
  visualizations to their content. Never write `fit: fixed`.
- Card 2, table 6, figure 4, advanced visualization 5 or 6, MultiQC panel 4,
  highlight 4. A text takes the height the lint estimates.
- Tables are full width, except beside their record card (`w: 5` + `w: 3`).

### Routes and pruning

- `template.yaml` prunes data collections per route: no metadata, another
  classifier, a skipped step. Route alternates (the same card from two
  classifiers) share one grid slot.
- At import, a highlight whose source is gone is removed, and so is each `values`
  list item whose data collection is missing. Give highlight sources a short,
  meaningful `index`.
- Text that cannot be pruned (hero, steps, how to read) names no `{VARIABLE}`.
- No `filter_expr` names `{GROUP_COL}`. Without metadata it resolves to the
  `__no_group__` sentinel, which the filter check rejects, and the import fails
  before any pruning. Narrow to the group column in the recipe instead, with
  `params: {group_col: "{GROUP_COL}"}`.

### Prose

- No em dashes. Result rows separate the claim from its context with " – ".
- Lists, headings and `:::` blocks use `body: |`. Prose-only bodies use `body: >`.
  At most 3 sentences per paragraph.
- No megatest sample names, genes or loci: the `forbidden_terms` of `megatest.yaml`
  are checked in every title, description, body and caption.
- When a default changes, update the title, the section description, the caption
  and the template's `docs/dashboards.md` with it.

## Badge promotion

A template starts **Draft** while it still needs a review to be usable, or
**Experimental** when it works but is shared as-is. Both are promoted as they're
reviewed and tested:

| Badge | Criteria |
|-------|----------|
| <span style="white-space: nowrap">:material-pencil-outline:{ style="color: #90A4AE" } **Draft**</span> | Generated and not yet reviewed. Expect it to need fixes before it is usable. |
| <span style="white-space: nowrap">:material-flask-outline:{ style="color: #FF9800" } **Experimental**</span> | Shared as-is. PR submitted; feedback and PRs welcome. |
| <span style="white-space: nowrap">:material-check-circle-outline:{ style="color: #2196F3" } **Reviewed**</span> | Tested, CI passes, reviewed by the Depictio team or community. |
| <span style="white-space: nowrap">:material-shield-check:{ style="color: #4CAF50" } **Certified**</span> | Validated by the pipeline lead developer. Highest trust level. |

## Getting help

- Open a [GitHub Discussion](https://github.com/depictio/depictio/discussions) and tag your PR `template`.
- Reference implementation: `depictio/projects/nf-core/ampliseq/`.
