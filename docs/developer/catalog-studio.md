---
title: "Catalog Studio"
icon: material/hammer-wrench
description: "Author Depictio Tools Catalog entries visually — no YAML — then open a one-click PR. The GitHub Pages Tools Studio."
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../../images/logo/tools_catalog_logo.png" alt="Depictio Tools Catalog">
  <h1 class="catalog-hero__title" id="catalog-studio">Catalog Studio</h1>
</div>

**Depictio Tools Studio** is a no-backend web app for authoring
[Tools Catalog](../catalog/index.md) entries **without writing YAML**. It runs
entirely in your browser (GitHub Pages) — import a tool, upload a fixture, design
its renders on live previews, and open a pull request in one click.

<div class="catalog-cta-wrap" markdown>
[Open the Tools Studio :material-arrow-right:](https://depictio.github.io/depictio/){ .catalog-cta }
</div>

!!! success "The recommended way to contribute a tool"
    Catalog Studio is now the recommended path for adding a tool. It generates
    the exact same files as the manual route — so if you'd rather hand-write
    them (or need to understand what the Studio produces), the
    [Contributing a Tool](contributing-a-tool.md) guide remains the field-by-field
    reference.

## What it produces

The Studio is a front-end over the same catalog contract — it writes the three
co-located files a tool entry needs:

<div class="module-flow" markdown>

<div class="module-flow__step module-flow__step--file" markdown>
:material-identifier:{ .lg } **`module.yaml`**

The tool's identity — `id`, `name`, and its upstream source.
</div>

<div class="module-flow__step module-flow__step--module" markdown>
:material-file-cog-outline:{ .lg } **`<output>.yaml`**

`find` the file, optional `recipe`, and the `renders_as` it offers.
</div>

<div class="module-flow__step module-flow__step--component" markdown>
:material-table-check:{ .lg } **`<output>.tsv`** <span class="module-flow__opt">fixture</span>

A small real sample so every render is validated and previewed.
</div>

</div>

## The authoring workflow

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../images/guides/catalog-studio/overview.png" target="_blank">
        <img src="../../images/guides/catalog-studio/overview.png" width="800" style="max-width: 100%;">
    </a>
</div>

**Tool identity & outputs.** A two-panel layout: set the tool's identity on one
side and configure its outputs on the other.

**nf-core import.** Point at an nf-core module and the Studio auto-fills the
identifiers and output metadata from the module's `meta.yml`.

<div style="border: 1px solid grey; width: 602px; max-width: 100%; padding: 1px;">
    <a href="../../images/guides/catalog-studio/nfcore-import.png" target="_blank">
        <img src="../../images/guides/catalog-studio/nfcore-import.png" width="600" style="max-width: 100%;">
    </a>
</div>

**Fixture upload.** Drop in a CSV/TSV sample of the output; the Studio parses it
and **infers column dtypes**, which ground every render binding.

**Visualization designer.** Design each render on a **live preview** using
Depictio's real builder components — the figure builder with a Plotly preview
(and in-browser Python via Pyodide), plus table, interactive, and card
components, all theme-aware.

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../images/guides/catalog-studio/viz-designer-plotly.png" target="_blank">
        <img src="../../images/guides/catalog-studio/viz-designer-plotly.png" width="800" style="max-width: 100%;">
    </a>
</div>

## Add to existing tools

The Studio matches your work against a snapshot of the live catalog, so you can
extend an existing tool rather than duplicate it — **append visualizations** to
an existing output (preserving its YAML comments), or **create new outputs**
inside an existing tool.

!!! info "Duplicate detection"
    The Studio compares against the catalog by tool **id**, **name**, and
    **nf-core module path**, and warns you when an entry already exists —
    suggesting you add to it instead.

## Export & open a PR

=== "One-click PR"

    Sign in with **GitHub OAuth** (`public_repo` scope — no personal access
    token needed). The Studio opens a pull request for you via a Cloudflare
    Worker (code→token exchange), with a sectioned PR body including the
    validation details.

    <div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
        <a href="../../images/guides/catalog-studio/export-pr.png" target="_blank">
            <img src="../../images/guides/catalog-studio/export-pr.png" width="800" style="max-width: 100%;">
        </a>
    </div>

=== "Zip download (fallback)"

    When OAuth isn't configured, download the tool folder as a zip and open the
    PR by hand — see [Step 5 of the manual guide](contributing-a-tool.md#step-5-validate-preview-and-open-a-pr).

## Validation

Every entry passes the same CI gate — `depictio-cli dev catalog validate` — which
now checks three layers:

1. **Component** — renders target real Depictio components with valid required fields.
2. **Column names** — bound columns exist in the fixture / schema.
3. **Dtype** — bound columns are type-compatible with their render roles.

!!! note "Catalog scale"
    The gate currently validates the full catalog: **7 tools, 28 outputs,
    47 renders** (26 dtype-checked).

!!! note "Prefer to hand-write YAML?"
    See [Contributing a Tool](contributing-a-tool.md) for the file-by-file
    reference and the pre-submit checklist.
