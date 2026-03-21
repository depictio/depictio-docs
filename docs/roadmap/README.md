---
title: "Roadmap"
icon: material/chart-timeline
description: "Explore the roadmap for Depictio, including current features and future plans."
hide:
  - navigation
---

## Big Picture

::timeline:: class="depictio-roadmap" center alternate

- title: "Visualization Studio"
  content: "Interactive dashboards with modern web components and real-time data binding"
  icon: ":fontawesome-solid-chart-line:"
  key: "completed"
  sub_title: "Phase 1: Foundation ✅"

- title: "Data Ingestion"
  content: "Multiple tabular formats with Delta Lake storage and data provenance"
  icon: ":fontawesome-solid-database:"
  key: "completed"
  sub_title: "Phase 1: Foundation ✅"

- title: "MultiQC Integration"
  content: "Seamless integration with bioinformatics quality control reports"
  icon: "./multiqc.png"
  key: "multiqc"
  sub_title: "Phase 2: Specialization ✅"

- title: "Image Grid Component"
  content: "S3-backed image galleries with configurable thumbnails and grid layout"
  icon: ":fontawesome-solid-images:"
  key: "completed"
  sub_title: "Phase 2: Specialization ✅"

- title: "Geospatial Map Component"
  content: "Scatter, density, and choropleth maps with cross-filtering and GeoJSON data collection support"
  icon: ":fontawesome-solid-map-location-dot:"
  key: "completed"
  sub_title: "Phase 2: Specialization ✅"

- title: "Templates & Community"
  content: "Reusable dashboard templates for standard bioinformatics workflows, nf-core integration, and nf-core plugin for automatic data ingestion"
  icon: "./nf-core-logo-square.png"
  key: "nfcore"
  sub_title: "Phase 3: Templates ✅🚧"

- title: "Scientific Reproducibility"
  content: "DOI integration, persistent access IDs, citable dashboards, full data provenance from sample to visualization"
  icon: ":fontawesome-solid-flask:"
  key: "planned"
  sub_title: "Phase 4: Reproducibility 📋"

- title: "AI & Intelligence"
  content: "Smart dashboard creation & AI-assisted analysis"
  icon: ":fontawesome-solid-robot:"
  key: "planned"
  sub_title: "Phase 5: Intelligence 📋"

::/timeline::

---

## The Reproducibility Challenge

<!-- prettier-ignore -->
!!! quote "The Reproducibility Crisis in Data Visualization"
    - *"Dashboards disappear after papers are published."*
    - *"Visualizations can't be reproduced months later."*
    - *"Data lineage is lost between pipeline runs."*
    - *"Cross-experiment comparisons are impossible."*

Depictio is built with [FAIR principles](https://www.go-fair.org/fair-principles/) in mind: **F**indable, **A**ccessible, **I**nteroperable, **R**eusable. Some challenges are already addressed today; others are part of our roadmap and will be tackled in future releases.

**How Depictio will address the reproducibility crisis:**

| Challenge                      | Solution                                                                                                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboards disappear           | :fontawesome-solid-database: *Will show in the future* — persistent, queryable dashboards for cross-experiment comparison                                                               |
| Can't reproduce visualizations | :fontawesome-solid-file-code: YAML-defined dashboards + traceable data — export and re-import any dashboard as code                                                                     |
| No data lineage                | :fontawesome-solid-clock-rotate-left: *Will show in the future* — Delta Lake time travel, auditing, and provenance                                                                      |
| Siloed experiment data         | :fontawesome-solid-link: Cross-DC linking — meta-analysis across studies                                                                                                                |
| Dashboards not citable         | :fontawesome-solid-id-card: *Will show in the future* — DOI integration, persistent access IDs, citable dashboard snapshots                                                             |
| No sample-to-viz traceability  | :fontawesome-solid-fingerprint: *Will show in the future* — persistent URL / access ID from sample ([LabID](https://grp-gbcs.embl-community.io/labid-user-docs/)) to pipeline to Delta |
| Reproducibility requires setup | :fontawesome-solid-puzzle-piece: Pre-built templates for nf-core/ampliseq **shipped** ([docs](../usage/projects/templates.md)); nf-core plugin for automatic data ingestion planned |

---

## Current Features

### Data Ingestion

- [x] YAML-based data ingestion via CLI ([docs](../depictio-cli/usage.md))
- [x] Polars-compatible formats (Parquet, CSV, JSON, TSV) → [Delta Lake](https://delta.io/)
- [x] S3/MinIO storage with backup/restore commands ([docs](../depictio-cli/usage.md#-backup-commands))
- [x] MultiQC report integration ([docs](../features/components.md#multiqc-components) | [:material-github: #626](https://github.com/depictio/depictio/pull/626))
- [x] Client-side table joining in CLI ([:material-github: #634](https://github.com/depictio/depictio/pull/634))
- [x] Recipe-based data transformation — Python recipes with 4-checkpoint validation ([docs](../usage/projects/recipes.md))
- [x] Template-based project setup — one-command project creation with `{DATA_ROOT}` substitution ([docs](../usage/projects/templates.md))
- [x] nf-core/ampliseq templates (v2.14.0, v2.16.0) with 5 bundled recipes and auto dashboard import

### Dashboard Components

- [x] Generic components: Figure, Table, Card, Interactive ([docs](../features/components.md))
- [x] MultiQC components for QC reports ([docs](../features/components.md#multiqc-components))
- [x] Image grid with S3/MinIO integration and configurable thumbnails ([:material-github: #664](https://github.com/depictio/depictio/pull/664))
- [x] Geospatial map component: scatter, density, choropleth with GeoJSON DC support ([docs](../features/components.md#map-components))
- [x] Figure code mode with live preview ([:material-github: #639](https://github.com/depictio/depictio/pull/639))

### Dashboard Interactivity

- [x] Two-panel layout with tabs ([:material-github: #616](https://github.com/depictio/depictio/pull/616))
- [x] Cross-DC filtering via universal linking ([docs](../features/cross-dc-filtering.md))
- [x] Interactive selection filtering: scatter/table/map selections
- [x] YAML dashboard import/export ([docs](../features/yaml-sync.md))

### Infrastructure

- [x] Docker + Kubernetes with Helm charts ([docs](../installation/docker.md))
- [x] Celery/Redis background processing
- [x] Multi-app architecture (Management, Viewer, Editor)
- [x] Authentication: local, Google OAuth, unauthenticated mode

---

## Planned Features

### Phase 3: Templates & Community :material-star:{ .priority }

Reusable dashboards for standard bioinformatics workflows, with a focus on nf-core community adoption.

- [x] **Depictio templates system** — one-command project setup via `depictio run --template`, with `{DATA_ROOT}` substitution, template provenance tracking, and automatic dashboard import ([docs](../usage/projects/templates.md))
- [x] **Recipe-based data transformation** — versioned Python recipes with 4-checkpoint validation, co-located with templates ([docs](../usage/projects/recipes.md))
- [x] **nf-core/ampliseq templates** — complete templates for v2.14.0 and v2.16.0 with 5 recipes covering alpha diversity, rarefaction, taxonomy, and differential abundance
- [ ] **More nf-core pipeline templates** — rnaseq, sarek, atacseq, methylseq, …
- [ ] **nf-core plugin** — automatically registers nf-core pipeline outputs in Depictio at run time, no manual CLI step required
- [ ] **Template marketplace** — community-contributed templates with validation and screenshots

### Phase 4: Scientific Reproducibility (6-12 months)

Publication-grade traceability and citation support for research outputs.

- [ ] **DOI integration** — citable dashboard snapshots and persistent access IDs
- [ ] **Persistent access IDs** — stable URLs per dashboard version; link from sample ID → pipeline run → Delta table → visualization
- [ ] **Data provenance** — via [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/) integration for pipeline versions, parameters, and timestamps
- [ ] **Static export** — [Quarto](https://quarto.org/) integration for HTML/PDF publication supplements

### Phase 5: AI & Intelligence (12+ months)

- [ ] **Smart dashboard creation** — describe the analysis you need; AI proposes a layout and component configuration
- [ ] **AI-assisted analysis** — automated anomaly detection, visualization recommendations, and plain-language report narration
- [ ] **MCP server** — expose Depictio as a tool for AI agents to create dashboards, query data, and manage projects programmatically

---

### Visualization Modules

- [ ] Reusable chart configurations catalog
- [ ] High-dimensional methods (UMAP, PCA, t-SNE)
- [ ] Omics visualizations (Volcano, MA, heatmaps)
- [ ] [JBrowse2](https://jbrowse.org/) genome browser component

### UI & Components

- [ ] Markdown component for documentation
- [ ] Extended interactive components (radio buttons, improved sliders, …)
- [ ] Project creation wizard with workflow selection

---

### Links

- [:material-github: GitHub Issues](https://github.com/depictio/depictio/issues) — feature requests, bug reports
- [Contributing Guide](../developer/contributing.md) — detailed setup instructions
- [Developer Docs](../developer/index.md) — architecture overview
