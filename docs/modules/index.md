---
title: "Depictio Modules"
icon: material/view-module
description: "Browse the live catalog of Depictio modules — reusable integrations that turn bioinformatics tool outputs into dashboard components."
hide:
  - navigation
  - toc
---

# :material-view-module: Depictio Modules

**A module maps a workflow's output files to predefined visualizations.**
Point Depictio at a pipeline run — every output a module recognises becomes a
dashboard component, with no manual wiring.

<div class="module-flow" markdown>

<div class="module-flow__step module-flow__step--file" markdown>
:material-file-document-outline:{ .lg } **Workflow output**

A file your pipeline produced — stats tables, metrics, reports.
</div>

<div class="module-flow__step module-flow__step--module" markdown>
:material-view-module:{ .lg } **Module**

Recognises the tool's file and prepares its columns.
</div>

<div class="module-flow__step module-flow__step--component" markdown>
:material-view-dashboard-variant:{ .lg } **Visualization**

A predefined component — figure, table, card, or advanced viz.
</div>

</div>

Browse the catalog below: filter by component type or kind, and inspect each
output's exact column bindings.

<div class="catalog-embed" markdown>
  <div class="catalog-demo-header">
    <span class="catalog-demo-title">Depictio Modules</span>
    <button class="catalog-fs-close" type="button" onclick="toggleCatalogFullscreen(this)" title="Exit fullscreen" aria-label="Exit fullscreen">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
    </button>
  </div>
  <button class="catalog-fs-btn" type="button" onclick="toggleCatalogFullscreen(this)" title="Toggle fullscreen" aria-label="Toggle fullscreen">
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
  </button>
  <div class="catalog-iframe-light">
    <iframe src="../assets/component-catalog-light.html" title="Depictio modules catalog (light)" width="100%" height="1100px" frameborder="0" loading="lazy"></iframe>
  </div>
  <div class="catalog-iframe-dark">
    <iframe src="../assets/component-catalog-dark.html" title="Depictio modules catalog (dark)" width="100%" height="1100px" frameborder="0" loading="lazy"></iframe>
  </div>
</div>

## :material-sitemap: How a module works

Every module follows the same path — from a raw file on disk to a live dashboard
component:

<div class="module-flow" markdown>

<div class="module-flow__step module-flow__step--detect" markdown>
:material-file-search:{ .lg } **Detect**

Recognise which file in a run is this tool's output, by filename or path pattern.
</div>

<div class="module-flow__step module-flow__step--reshape" markdown>
:material-cog-transfer:{ .lg } **Reshape** <span class="module-flow__opt">optional</span>

Transform the raw file into tidy, bindable columns. Already-tidy outputs skip this.
</div>

<div class="module-flow__step module-flow__step--render" markdown>
:material-view-dashboard-variant:{ .lg } **Render**

Bind those columns to a dashboard component — chart, table, card, or advanced viz.
</div>

</div>

!!! info "Validated bindings"
    Column schemas live in exactly one place per output, and continuous integration
    validates every render binding against the real reshaped columns — so a module
    that ships green is wired correctly, with no manual review.

For the configuration reference of each component type, see the
[:material-puzzle: Dashboard Components](../features/components.md) guide.

!!! tip "Add a module"
    Extending the catalog is a single-folder contribution: a small module definition
    plus one description per output and a fixture file. See the catalog README in the
    depictio repository for the full contract.
