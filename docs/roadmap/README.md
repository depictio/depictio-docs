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
  content: "Support for multiple tabular formats: Parquet, CSV, JSON, TSV with automated processing"
  icon: ":fontawesome-solid-database:"
  key: "completed"
  sub_title: "Phase 1: Foundation ✅"

- title: "MultiQC Integration"
  content: "Seamless integration with bioinformatics quality control reports"
  icon: "./multiqc.png"
  key: "multiqc"
  sub_title: "Phase 2: Specialization ✅"

- title: "Workflow Templates"
  content: "Pre-configured dashboards for popular bioinformatics workflows and pipelines"
  icon: ":fontawesome-solid-sitemap:"
  key: "nfcore"
  sub_title: "Phase 3: Ecosystem 🚧"

- title: "Project Wizard"
  content: "Guided UI for project setup with workflow selection and intelligent recommendations"
  icon: ":fontawesome-solid-wand-magic-sparkles:"
  key: "planned"
  sub_title: "Phase 3: Ecosystem 📋"

- title: "AI Integration"
  content: "MCP server for AI-assisted dashboard creation and data exploration"
  icon: ":fontawesome-solid-robot:"
  key: "planned"
  sub_title: "Phase 4: Intelligence 📋"

::/timeline::

---

## Current Features

### Data Ingestion

- [x] YAML-based data ingestion via CLI ([docs](../depictio-cli/usage.md))
- [x] Polars-compatible formats (Parquet, CSV, JSON, TSV) → [Delta Lake](https://delta.io/)
- [x] S3/MinIO storage with backup/restore commands ([docs](../depictio-cli/usage.md#backup-commands))
- [x] MultiQC report integration ([docs](../features/components.md#multiqc-components) | [:material-github: #626](https://github.com/depictio/depictio/pull/626))
- [x] Client-side table joining in CLI ([:material-github: #634](https://github.com/depictio/depictio/pull/634))

### Authentication & Users

- [x] Username/password + JWT tokens with refresh support
- [x] Google OAuth ([docs](../installation/configuration.md#google-oauth))
- [x] Unauthenticated mode ([docs](../usage/guides/unauthenticated_mode.md))
- [x] CLI configuration via web interface

### Dashboard Components

- [x] Generic components: Figure, Table, Card, Interactive ([docs](../features/components.md))
- [x] MultiQC components for QC reports ([docs](../features/components.md#multiqc-components) | [:material-github: #626](https://github.com/depictio/depictio/pull/626))
- [x] Image gallery with S3/MinIO integration ([docs](../features/components.md#image-components) | [:material-github: #664](https://github.com/depictio/depictio/pull/664))
- [x] Figure code mode with live preview ([:material-github: #639](https://github.com/depictio/depictio/pull/639))
- [x] Table export to CSV with filtering

### Dashboard Interactivity

- [x] Two-panel layout with tabs ([:material-github: #616](https://github.com/depictio/depictio/pull/616))
- [x] Cross-DC filtering via universal linking ([docs](../features/cross-dc-filtering.md) | [:material-github: #640](https://github.com/depictio/depictio/pull/640))
- [x] Interactive selection filtering: scatter/table selections ([docs](../features/interactive-selection-filtering.md))
- [x] YAML dashboard import/export ([docs](../features/yaml-sync.md) | [:material-github: #663](https://github.com/depictio/depictio/pull/663))
- [x] Drag-and-drop component editing with auto-save

### Project & Admin

- [x] Project management with permissions ([docs](../usage/projects/guide.md))
- [x] YAML-based project configuration ([docs](../usage/projects/reference.md))
- [x] Admin interface for users, projects, dashboards ([docs](../usage/administration.md))

### Infrastructure

- [x] Docker + Kubernetes with Helm charts ([docs](../installation/docker.md) | [K8s](../installation/kubernetes.md))
- [x] Celery/Redis background processing ([:material-github: #644](https://github.com/depictio/depictio/pull/644))
- [x] Multi-app architecture (Management, Viewer, Editor)
- [x] Dash v3+ with Mantine Components v2.0+
- [x] Dark/light theme with auto-detection

---

## Planned Features

### Templates & Workflows :material-star:{ .priority }

- [ ] **Depictio templates system** - Pre-configured project and dashboard templates
- [ ] [nf-core](https://nf-co.re/) workflow templates (rnaseq, sarek, etc.)
- [ ] Template marketplace with validation

### Visualization Modules

- [ ] Reusable chart configurations catalog
- [ ] High-dimensional methods (UMAP, PCA, t-SNE)
- [ ] Omics visualizations (Volcano, MA, heatmaps)

### Genomics Integration

- [ ] [JBrowse2](https://jbrowse.org/) component for genome browser tracks (VCF, BAM, BED, GFF)

### AI & Integrations :material-star:{ .priority }

- [ ] **[MCP](https://modelcontextprotocol.io/) server** for AI-assisted dashboard creation
- [ ] Natural language queries for filtering and visualization

### Project Setup

- [ ] **Project creation wizard** with workflow selection
- [ ] CLI scan templates (`depictio-cli scan --template nf-core/sarek .`)

### Authentication

- [ ] Additional OAuth providers (GitHub, etc.)
- [ ] SSO/SAML authentication
- [ ] Groups management with dashboard sharing

### UI & Components

- [ ] Markdown component for documentation
- [ ] Extended interactive components (date picker, radio buttons)
- [ ] Theme customization (colors, fonts)

### Admin & Infrastructure

- [ ] Dedicated admin dashboard ([FastAPI-Admin](https://fastapi-admin-docs.long2ice.io/))
- [ ] API key management interface
- [ ] Separate frontend/backend containers
