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

- title: "Templates & Community"
  content: "Reusable dashboard templates for standard bioinformatics workflows, nf-core integration, and nf-core plugin for automatic data ingestion"
  icon: "./nf-core-logo-square.png"
  key: "nfcore"
  sub_title: "Phase 3: Templates 🚧"

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

| Challenge                      | Solution                                                                                                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboards disappear           | :fontawesome-solid-database: Persistent, queryable dashboards — compare experiments over time                                                                                           |
| Can't reproduce visualizations | :fontawesome-solid-file-code: YAML-defined dashboards + traceable data — export and re-import any dashboard as code                                                                     |
| No data lineage                | :fontawesome-solid-clock-rotate-left: Delta Lake storage — time travel, auditing, provenance                                                                                            |
| Siloed experiment data         | :fontawesome-solid-link: Cross-DC linking — meta-analysis across studies                                                                                                                |
| Dashboards not citable         | :fontawesome-solid-id-card: *Will show in the future* — DOI integration, persistent access IDs, citable dashboard snapshots                                                             |
| No sample-to-viz traceability  | :fontawesome-solid-fingerprint: *Will show in the future* — persistent URL / access ID from sample ([LabID](https://grp-gbcs.embl-community.io/labid-user-docs/)) to pipeline to Delta |
| Reproducibility requires setup | :fontawesome-solid-puzzle-piece: *Will show in the future* — nf-core plugin for automatic data ingestion; pre-built dashboard templates per pipeline                                    |

---

## Current Features

### Data Ingestion

- [x] YAML-based data ingestion via CLI ([docs](../depictio-cli/usage.md))
- [x] Polars-compatible formats (Parquet, CSV, JSON, TSV) → [Delta Lake](https://delta.io/)
- [x] S3/MinIO storage with backup/restore commands ([docs](../depictio-cli/usage.md#-backup-commands))
- [x] MultiQC report integration ([docs](../features/components.md#multiqc-components) | [:material-github: #626](https://github.com/depictio/depictio/pull/626))
- [x] Client-side table joining in CLI ([:material-github: #634](https://github.com/depictio/depictio/pull/634))

### Dashboard Components

- [x] Generic components: Figure, Table, Card, Interactive ([docs](../features/components.md))
- [x] MultiQC components for QC reports ([docs](../features/components.md#multiqc-components))
- [x] Image grid with S3/MinIO integration and configurable thumbnails ([:material-github: #664](https://github.com/depictio/depictio/pull/664))
- [x] Figure code mode with live preview ([:material-github: #639](https://github.com/depictio/depictio/pull/639))

### Dashboard Interactivity

- [x] Two-panel layout with tabs ([:material-github: #616](https://github.com/depictio/depictio/pull/616))
- [x] Cross-DC filtering via universal linking ([docs](../features/cross-dc-filtering.md))
- [x] Interactive selection filtering: scatter/table selections
- [x] YAML dashboard import/export ([docs](../features/yaml-sync.md))

### Infrastructure

- [x] Docker + Kubernetes with Helm charts ([docs](../installation/docker.md))
- [x] Celery/Redis background processing
- [x] Multi-app architecture (Management, Viewer, Editor)
- [x] Authentication: local, Google OAuth, unauthenticated mode

---

## Planned Features

### Phase 3: Templates & Community (0-6 months) :material-star:{ .priority }

Reusable dashboards for standard bioinformatics workflows, with a focus on nf-core community adoption.

- [ ] **Depictio templates system** — pre-configured project and dashboard templates exportable/importable as YAML bundles
- [ ] **nf-core dashboard templates** — one-click dashboards for [nf-core](https://nf-co.re/) pipelines (rnaseq, sarek, atacseq, methylseq, …)
- [ ] **nf-core plugin** — automatically registers nf-core pipeline outputs in Depictio at run time, no manual CLI step required
- [ ] **Template marketplace** — community-contributed templates with validation and screenshots
- [ ] **Schema versioning** — backwards compatibility guarantees across Depictio versions

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
