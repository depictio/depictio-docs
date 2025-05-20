---
title: "Roadmap"
icon: material/chart-timeline
description: "Explore the roadmap for Depictio, including current features and future plans."
hide:
  - navigation
---

## What we have now

### Data ingestion & data types supported

- [x] Data ingestion using Depictio-CLI (python package based [typer](https://typer.tiangolo.com/)) using YAML configuration file
- [x] Polars-compatible data format (Parquet, CSV, JSON, TSV) ingestion and transformation into [Delta Lake format](https://delta.io/)
- [x] Delta lake push to S3 bucket (on-premise or remote MinIO)

### Authentication

- [x] Basic authentication (username/password) > register, login, logout
- [x] JWT token management
- [x] Public/private & API internal key creation
- [x] Profile management (change password)
- [x] Create CLI configuration through the web interface (YAML to be copy-pasted)

### Dashboards management

- [x] Create a dashboard for a project
- [x] Edit name, duplicate, delete a dashboard
- [x] Make public/private a dashboard at the instance level

### Dashboard design and interactivity

- [x] Dashboard design using generic components (figure, metrics card, interactive component, table)
- [x] Add/delete components
- [x] Resize and relayout components
- [x] Edit components (title, aggregation applied)
- [x] Duplicate components
- [x] Enable/disable interactivity
- [x] Enable/disable edit mode
- [x] Auto-save dashboard + manual save (trigger screenshot to be used as thumbnail)

### Project management

- [x] Project management UI to list workflows and data collections
- [x] List and edit project permissions
- [x] Turn public/private a project

### Admin

- [x] Admin interface to list and manage users (delete functionality only)
- [x] Admin interface to list projects
- [x] Admin interface to list dashboards

## What we plan for the future

### Data ingestion & data types supported

- [ ] Support MultiQC report integration
- [ ] Support for genome-browser tracks through [JBrowse2](https://jbrowse.org/) (e.g., VCF, BAM, BED, GFF)
- [ ] Data ingestion template for heavily-used and standardized nf-core community workflows (`depictio-cli scan --template nf-core/sarek .`)

### Authentication

- [ ] OAuth2 authentication (Google, GitHub, etc.)
- [ ] SSO/SAML authentication
- [ ] Groups management

### Dashboards management

- [ ] Dashboard sharing with specific users or groups
- [ ] Tagging system for dashboards)

### Dashboard design and interactivity

- [ ] Implement JBrowse2 component for genome browser tracks
- [ ] High-dimensional data methods (e.g., UMAP, PCA, t-SNE)
- [ ] Omics data visualization methods (e.g., Volcano plot, ...)
- [ ] Markdown component
- [ ] Extend interactive component (date, radio, ...)
- [ ] Improve component (e.g., slider values range, figure styling and properties, etc.)
- [ ] Add more grouping functionalities

### Admin

- [ ] Move admin interface to a dedicated FastAPI dashboard using [FastAPI-Users](https://frankie567.github.io/fastapi-users/) and [FastAPI-Admin](https://fastapi-admin-docs.long2ice.io/)
- [ ] List and manage groups
- [ ] Admin interface to list and manage API keys

### UI

- [ ] Improve UI/UX (e.g., loading spinner, error handling, etc.)
- [ ] Upgrade dash to the latest version (v3)
- [ ] Upgrade dash mantine components to the latest version (>v1.0)
- [ ] Improve theme customization (night mode, colors, fonts) and CSS styling
