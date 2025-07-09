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
- [x] Comprehensive S3 backup and restore strategy with CLI commands and API endpoints
- [x] Performance optimization with caching for iterative joins and component data
- [x] Enhanced CLI execution with run commands and improved logging

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

### UI

- [x] Functional dark/light mode theming with auto-theme detection
- [x] Upgrade dash to the latest version (v3+)
- [x] Upgrade dash mantine components to the latest version (2.0+) with enhanced components and styling

## What we plan for the future

### Data ingestion & data types supported

- [ ] Support MultiQC report integration (leverage MultiQC 1.29 with parquet file)
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
- [ ] Extend interactive component (date, radio, ...)
- [ ] Improve component (e.g., slider values range, figure styling and properties, etc.)
- [ ] Add more grouping functionalities

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

- [ ] Improve UI/UX (e.g., loading spinner, error handling, etc.)
- [ ] Further theme customization (colors, fonts) and CSS styling enhancements
