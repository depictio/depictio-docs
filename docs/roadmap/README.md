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

- title: "Scientific Reproducibility"
  content: "YAML-first dashboards, data provenance, DOI/ORCID integration"
  icon: ":fontawesome-solid-flask:"
  key: "nfcore"
  sub_title: "Phase 3: Reproducibility 🚧"

- title: "Open Science"
  content: "Zenodo archival, RO-Crate export, LIMS integrations"
  icon: ":fontawesome-solid-globe:"
  key: "planned"
  sub_title: "Phase 4: Integration 📋"

- title: "AI & Automation"
  content: "MCP server for AI-assisted dashboard creation and data exploration"
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

Depictio is built with [FAIR principles](https://www.go-fair.org/fair-principles/) in mind: **F**indable, **A**ccessible, **I**nteroperable, **R**eusable.

**Depictio addresses this with:**

| Challenge                      | Solution                                                                                                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboards disappear           | :fontawesome-solid-database: Persistent, queryable dashboards — compare experiments over time                                                                                           |
| Can't reproduce visualizations | :fontawesome-solid-file-code: YAML-defined dashboards + traceable data — persistent IDs from sample ([LabID](https://grp-gbcs.embl-community.io/labid-user-docs/)) to pipeline to Delta |
| No data lineage                | :fontawesome-solid-clock-rotate-left: Delta Lake storage — time travel, auditing, provenance                                                                                            |
| Siloed experiment data         | :fontawesome-solid-link: Cross-DC linking — meta-analysis across studies                                                                                                                |

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
- [x] Image gallery with S3/MinIO integration ([:material-github: #664](https://github.com/depictio/depictio/pull/664))
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

### Tier 1: Scientific Reproducibility (0-6 months) :material-star:{ .priority }

Essential for research workflows and publication-ready outputs.

- [ ] **YAML-first dashboards** — all state exportable, no GUI-only configuration
- [ ] **Data provenance** — via [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/) integration for pipeline versions, parameters, timestamps
- [ ] **DOI/ORCID integration** — citable dashboards, researcher attribution
- [ ] **Static export** — [Quarto](https://quarto.org/) integration for HTML/PDF publication supplements
- [ ] **nf-core plugin** — submit pipeline outputs directly to Depictio
- [ ] **Schema versioning** — backwards compatibility guarantees

### Tier 2: Open Science Integration (6-12 months)

Valuable for sharing and archiving research outputs.

- [ ] **RO-Crate export** — [Research Object](https://www.researchobject.org/) standard packaging
- [ ] **Zenodo integration** — one-click dashboard archival with DOI

### Tier 3: Community-Driven (12+ months)

Features driven by community requests and contributions.

- [ ] **Multi-user collaboration** — shared lab dashboards, real-time editing
- [ ] **AI-assisted creation** — MCP server, natural language dashboard building

---

### Templates & Workflows

- [ ] **Depictio templates system** — pre-configured project and dashboard templates
- [ ] [nf-core](https://nf-co.re/) workflow templates (rnaseq, sarek, atacseq, etc.)
- [ ] Template marketplace with validation and screenshots

### Visualization Modules

- [ ] Reusable chart configurations catalog
- [ ] High-dimensional methods (UMAP, PCA, t-SNE)
- [ ] Omics visualizations (Volcano, MA, heatmaps)
- [ ] [JBrowse2](https://jbrowse.org/) genome browser component

### UI & Components

- [ ] Markdown component for documentation
- [ ] Extended interactive components (radio buttons, improved sliders, ...)
- [ ] Project creation wizard with workflow selection

---

### Links

- [:material-github: GitHub Issues](https://github.com/depictio/depictio/issues) — feature requests, bug reports
- [Contributing Guide](../developer/contributing.md) — detailed setup instructions
- [Developer Docs](../developer/index.md) — architecture overview
