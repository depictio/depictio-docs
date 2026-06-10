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
  sub_title: "Phase 2: Specialized Components ✅"

- title: "Image Grid Component"
  content: "S3-backed image galleries with configurable thumbnails and grid layout"
  icon: ":fontawesome-solid-images:"
  key: "completed"
  sub_title: "Phase 2: Specialized Components ✅"

- title: "Geospatial Map Component"
  content: "Scatter, density, and choropleth maps with cross-filtering and GeoJSON / Map-capable Table DCs (v0.12.0)"
  icon: ":fontawesome-solid-map-location-dot:"
  key: "completed"
  sub_title: "Phase 2: Specialized Components ✅"

- title: "Advanced Biology Visualizations"
  content: "Omics plots extending the v0.12 DC-level type-config pattern — Volcano, Manhattan, Sunburst, and more"
  icon: ":fontawesome-solid-dna:"
  key: "completed"
  sub_title: "Phase 2: Specialized Components ✅"

- title: "Templates & Community"
  content: "Reusable dashboard templates for standard bioinformatics workflows, nf-core integration, and nf-core plugin for automatic data ingestion"
  icon: "./nf-core-logo-square.png"
  key: "nfcore"
  sub_title: "Phase 3: Templates ✅"

- title: "React Viewer"
  content: "Vite + Mantine SPA — Dash removed in v0.13.12, canonical URLs live in v1.0.0"
  icon: ":fontawesome-brands-react:"
  key: "completed"
  sub_title: "Phase 3.5: UI Modernization ✅"

- title: "Citable Science"
  content: "DOI-backed snapshots and sample-to-viz provenance on top of the existing Serve hosting"
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

## Reproducibility & FAIR

Built with [FAIR principles](https://www.go-fair.org/fair-principles/) in mind. v0.12 ships YAML-defined dashboards, Cross-DC linking, nf-core/ampliseq templates, and hosting via [SciLifeLab Serve](https://serve.scilifelab.se/) ✅. Citable DOI snapshots, persistent IDs, and data lineage land in Phase 4.

| Challenge | Status |
| --------- | ------ |
| Reproducibility requires setup | :material-check-circle: nf-core/ampliseq templates **shipped** ([docs](../usage/projects/templates.md)); nf-core plugin planned |
| Can't reproduce visualizations | :material-check-circle: YAML-defined dashboards + traceable data ([docs](../features/yaml-sync.md)) |
| Siloed experiment data | :material-check-circle: Cross-DC linking ([docs](../features/cross-dc-filtering.md)) |
| Dashboards disappear | :material-check-circle: Hosted on [SciLifeLab Serve](https://serve.scilifelab.se/) ([changelog](../changelog/README.md)) |
| Not citable / no sample-to-viz traceability | :material-clock-outline: Phase 4 — DOI snapshots via [SciLifeLab Serve](https://serve.scilifelab.se/) + [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/) provenance |
| No data lineage | :material-clock-outline: Phase 4 — Delta Lake time travel, auditing |

---

## Current Features

### Data Ingestion

- [x] YAML-based data ingestion via CLI ([docs](../depictio-cli/usage.md))
- [x] Polars-compatible formats (Parquet, CSV, JSON, TSV) → [Delta Lake](https://delta.io/)
- [x] S3/MinIO storage with backup/restore commands ([docs](../depictio-cli/usage.md#-backup-commands))
- [x] MultiQC report integration ([docs](../features/components.md#multiqc-components) | [:material-github: #626](https://github.com/depictio/depictio/pull/626))
- [x] **MultiQC data lifecycle** — append / replace / clear runs from the viewer with uniformity validation (v0.12.0, [docs](../usage/projects/guide.md#managing-data-collections-from-the-viewer-v0120))
- [x] **DC-level type configuration** — Map-capable Table DCs (lat/lon column detection on upload, `DCTableCoordinatesConfig`); extensible to advanced-viz types (v0.12.0, [docs](../usage/projects/guide.md#type-specific-data-collection-configuration-react-beta))
- [x] Client-side table joining in CLI ([:material-github: #634](https://github.com/depictio/depictio/pull/634))
- [x] Recipe-based data transformation — Python recipes with 4-checkpoint validation ([docs](../usage/projects/recipes.md))
- [x] Template-based project setup — one-command project creation with `{DATA_ROOT}` substitution ([docs](../usage/projects/templates.md))


### Dashboard Components

Specialized components share a common pattern: a DC-level type-config (introduced for Map in v0.12.0) declares the columns that drive the visualization, so every figure built on top inherits the config — no per-figure boilerplate. Advanced biology visualizations extend the same pattern.

- [x] Generic components: Figure, Table, Card, Interactive ([docs](../features/components.md))
- [x] MultiQC components for QC reports ([docs](../features/components.md#multiqc-components))
- [x] Image grid with S3/MinIO integration and configurable thumbnails ([:material-github: #664](https://github.com/depictio/depictio/pull/664))
- [x] Geospatial map component: scatter, density, choropleth with GeoJSON DC support + Map-capable Table DCs (v0.12.0, [docs](../features/components.md#map-components))
- [x] Figure code mode with live preview ([:material-github: #639](https://github.com/depictio/depictio/pull/639))

### Dashboard Interactivity

- [x] Two-panel layout with tabs ([:material-github: #616](https://github.com/depictio/depictio/pull/616))
- [x] Cross-DC filtering via universal linking ([docs](../features/cross-dc-filtering.md))
- [x] **Cross-DC links UI** — Create / Edit / Delete links from the React Beta viewer with resolver picker and sample-mapping preview (v0.12.0, [docs](../features/cross-dc-filtering.md#data-collection-actions))
- [x] Interactive selection filtering: scatter/table/map selections
- [x] YAML dashboard import/export ([docs](../features/yaml-sync.md))

### Infrastructure

- [x] Docker + Kubernetes with Helm charts ([docs](../installation/docker.md))
- [x] [SciLifeLab Serve](https://serve.scilifelab.se/) hosting via `values-serve.yaml` overlay ([changelog](../changelog/README.md))
- [x] Celery/Redis background processing
- [x] Authentication: local, Google OAuth, unauthenticated mode

### Frontend

- [x] **React viewer** — Vite + Mantine SPA on canonical URLs (v1.0.0); Dash removed in v0.13.12

---

## Planned Features

### Phase 3: Templates & Community :material-star:{ .priority }

Reusable dashboards for standard bioinformatics workflows, with a focus on nf-core community adoption.

**Infrastructure (shipped)**

- [x] **Depictio templates system** — one-command project setup via `depictio run --template`, with `{DATA_ROOT}` substitution, template provenance tracking, and automatic dashboard import ([docs](../usage/projects/templates.md))
- [x] **Recipe-based data transformation** — versioned Python recipes with 4-checkpoint validation, co-located with templates ([docs](../usage/projects/recipes.md))

**Planned**

- [ ] **nf-core plugin** — automatically registers nf-core pipeline outputs in Depictio at run time, no manual CLI step required
- [ ] **`nextflow.config` template** — embed Depictio ingestion directly in your Nextflow config so data collection happens at pipeline runtime
- [ ] **Snakemake report plugin** — Depictio as a drop-in replacement for Snakemake's built-in HTML report, with interactive dashboards instead of static outputs

### Phase 3.5: React viewer — v1.0.0 ✅ :material-react:

The React viewer (Vite + Mantine SPA) is the sole frontend as of v1.0.0. Dash was removed in v0.13.12; canonical URLs went live in v1.0.0.

- [x] React viewer shipped (v0.12.0)
- [x] Dash frontend removed (v0.13.12)
- [x] URL graduation — canonical `/dashboards`, `/dashboard/{id}`, `/dashboard-edit/{id}` (v1.0.0)
- [x] Component parity audit complete

### Phase 4: Citable Science

DOI-backed citability and sample-to-viz provenance on top of the existing [SciLifeLab Serve](https://serve.scilifelab.se/) hosting.

- [ ] **DOI snapshots** — persistent stable URLs per dashboard version, citable in publications
- [ ] **Sample-to-viz provenance** — [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/) linking sample → pipeline run → Delta table → visualization
- [ ] **Static export** — [Quarto](https://quarto.org/) for publication supplements

### Phase 5: AI & Intelligence (12+ months)

- [ ] **Smart dashboard creation** — describe the analysis you need; AI proposes a layout and component configuration
- [ ] **AI-assisted analysis** — automated anomaly detection, visualization recommendations, and plain-language report narration
- [ ] **MCP server** — expose Depictio as a tool for AI agents to create dashboards, query data, and manage projects programmatically

---

### Links

- [:material-github: GitHub Issues](https://github.com/depictio/depictio/issues) — feature requests, bug reports
- [Contributing Guide](../developer/contributing.md) — detailed setup instructions
- [Developer Docs](../developer/README.md) — architecture overview
