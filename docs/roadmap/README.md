---
title: "Roadmap"
icon: material/chart-timeline
description: "Explore the roadmap for Depictio, including current features and future plans."
hide:
  - navigation
---



## Big Picture - What we want to achieve

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

- title: "Configuration Assistant"
  content: "CLI-based project setup wizard with intelligent recommendations"
  icon: ":fontawesome-solid-terminal:"
  key: "nfcore"
  sub_title: "Phase 2: Specialization 🚧"

- title: "Workflow Templates"
  content: "Pre-configured dashboards for popular bioinformatics workflows and pipelines"
  icon: ":fontawesome-solid-sitemap:"
  key: "planned"
  sub_title: "Phase 3: Ecosystem 📋"

::/timeline::

## What we have now

### Data ingestion & data types supported

- [x] Data ingestion using Depictio-CLI (python package based [typer](https://typer.tiangolo.com/)) using YAML configuration file
- [x] Polars-compatible data format (Parquet, CSV, JSON, TSV) ingestion and transformation into [Delta Lake format](https://delta.io/)
- [x] Delta lake push to S3 bucket (on-premise or remote MinIO)
- [x] MultiQC report integration with dedicated visualization components (v0.5.0+)
- [x] Comprehensive S3 backup and restore strategy with CLI commands and API endpoints
- [x] Performance optimization with caching for iterative joins and component data
- [x] Enhanced CLI execution with run commands and improved logging
- [x] Client-side table joining moved from server to CLI for better performance (v0.6.0+)

### Authentication

- [x] Basic authentication (username/password) > register, login, logout
- [x] JWT token management
- [x] Refresh token support with enhanced security and session persistence
- [x] Public/private & API internal key creation
- [x] Profile management (change password)
- [x] Create CLI configuration through the web interface (YAML to be copy-pasted)
- [x] Google OAuth authentication integration
- [x] Unauthenticated mode with automatic anonymous login for public access
- [x] Temporary user functionality with session management and upgrade options

### Dashboards management

- [x] Create a dashboard for a project
- [x] Edit name, duplicate, delete a dashboard
- [x] Make public/private a dashboard at the instance level

### Dashboard design and interactivity

- [x] Dashboard design using generic components (figure, metrics card, interactive component, table, MultiQC)
- [x] Add/delete components
- [x] Resize and relayout components
- [x] Edit components (title, aggregation applied)
- [x] Duplicate components
- [x] Enable/disable interactivity
- [x] Enable/disable edit mode
- [x] Auto-save dashboard + manual save (trigger screenshot to be used as thumbnail)
- [x] Two-panel layout: left panel for filters/interactive components, right panel for visualizations (v0.6.0+)
- [x] Dashboard tabs with vertical organization in collapsible navbar (v0.6.0+)
- [x] Table component export to CSV with filter and sorting support (v0.6.0+)
- [x] Universal DC linking system for cross-DC filtering without pre-computed joins (v0.6.0+)
- [x] Figure code mode with live preview and bidirectional editor resize (v0.6.0+)
- [x] YAML dashboard validation with Pydantic-based configuration checking (v0.6.0+)

### Project management

- [x] Project management UI to list workflows and data collections
- [x] List and edit project permissions
- [x] Turn public/private a project

### Admin

- [x] Admin interface to list and manage users (delete functionality only)
- [x] Admin interface to list projects
- [x] Admin interface to list dashboards

### Testing & Quality Assurance

- [x] Pre-commit hooks for code quality enforcement
- [x] Comprehensive end-to-end testing with Cypress
- [x] Enhanced CI/CD workflows with automated testing
- [x] Integration tests for various components and workflows
- [x] Flask security assessment scanner integration
- [x] Improved test reliability and coverage

### Infrastructure & Deployment

- [x] Docker containerization with multi-architecture support (AMD64/ARM64)
- [x] Kubernetes deployment with Helm charts
- [x] Enhanced Helm chart configuration with persistent volumes and ingress
- [x] Gitpod workspace setup for streamlined development
- [x] Automated release workflows with changelog generation
- [x] Implement astral/ty as static type checking & in pre-commit hooks
- [x] Allow users to provide their own set of public/private keys
- [x] Celery/Redis background processing for heavy computations in design mode (v0.6.0+)
- [x] Multi-app architecture: separate Dash apps for Management, Viewer, and Editor (v0.6.0+)
- [x] Local Delta Table caching for improved API performance (v0.6.0+)
- [x] DevContainer and GitHub Codespaces support for cloud-based development

### UI

- [x] Functional dark/light mode theming with auto-theme detection
- [x] Upgrade dash to the latest version (v3+)
- [x] Upgrade dash mantine components to the latest version (2.0+) with enhanced components and styling
- [x] Improve UI/UX (e.g., loading spinner, error handling, etc.)
- [x] Improve dashboard layout and component resizing with vertical and horizontal growing

## What we plan for the future

### Data ingestion & data types supported

- [ ] Support for genome-browser tracks through [JBrowse2](https://jbrowse.org/) (e.g., VCF, BAM, BED, GFF)
- [ ] Data ingestion template for heavily-used and standardized nf-core community workflows (`depictio-cli scan --template nf-core/sarek .`)
- [ ] Single file loading (HTTP polars) without using CLI
- [ ] S3 bucket automatic cleanup when delta not listed in DB

### Authentication

- [ ] OAuth2 authentication (GitHub, etc.) - Google OAuth already implemented
- [ ] SSO/SAML authentication - partial SAML integration completed
- [ ] Groups management

### Dashboards management

- [ ] Dashboard sharing with specific users or groups
- [ ] Tagging system for dashboards

### Dashboard design and interactivity

- [ ] Implement JBrowse2 component for genome browser tracks
- [ ] High-dimensional data methods (e.g., UMAP, PCA, t-SNE)
- [ ] Omics data visualization methods (e.g., Volcano plot, ...)
- [ ] Markdown component
- [ ] Extend interactive component (date picker, radio buttons, etc.)
- [ ] Improve component properties (e.g., slider values range, figure styling, etc.)

### Admin

- [ ] Move admin interface to a dedicated FastAPI dashboard using [FastAPI-Users](https://frankie567.github.io/fastapi-users/) and [FastAPI-Admin](https://fastapi-admin-docs.long2ice.io/)
- [ ] List and manage groups
- [ ] Admin interface to list and manage API keys
- [ ] Update endpoints policy (hide/unprotect when needed)

### Development & Infrastructure

- [ ] Build separate containers for frontend and backend
- [ ] Performance testing for polars read/write from S3 with/without dashboard rendering

### Templates & Workflows

- [ ] Depictio templates system for workflow integration
- [ ] Dashboard templates for standardized nf-core workflows
- [ ] Template validation and CI/CD integration
- [ ] Template marketplace with screenshots and descriptions

### UI

- [ ] Further theme customization (colors, fonts) and CSS styling enhancements
