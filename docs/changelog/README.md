---
title: "Changelog"
icon: material/update
description: "Track changes and updates to Depictio across different versions."
hide:
  - navigation
---

# Changelog

## [v0.0.5](https://github.com/depictio/depictio/releases/tag/v0.0.5)

### Docker Images

```bash
ghcr.io/depictio/depictio:0.0.5
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

This changelog highlights the key changes in this release, organized by category. Special focus has been given to improvements in CLI, Docker, CI/CD, Helm, and code refactoring.

### ✨ Highlights

This section provides a high-level overview of the most significant improvements in each category.

#### ⚙️ Setup & Configuration Highlights

* Enhance S3 configuration handling, logging, and URL management for better integration between services ([54fec27c](https://github.com/depictio/depictio/commit/54fec27c), [49ded59c](https://github.com/depictio/depictio/commit/49ded59c), [5eb17f50](https://github.com/depictio/depictio/commit/5eb17f50))
* Update port settings and environment variables for external and internal API/Dash URLs ([98fe3654](https://github.com/depictio/depictio/commit/98fe3654), [ac03c664](https://github.com/depictio/depictio/commit/ac03c664))

#### 🔧 CLI Highlights

* Add run and standalone commands to CLI, enhance logging, and remove installation test script ([0bad4848](https://github.com/depictio/depictio/commit/0bad4848))
* Refactor scan/processing to improve logging and implement a run function for full execution of all steps ([c3335e41](https://github.com/depictio/depictio/commit/c3335e41))
* Add backend log retrieval steps to the Iris CLI workflow ([96a0630a](https://github.com/depictio/depictio/commit/96a0630a))
* Add Palmer Penguins dataset to test sequencing-runs ingestion ([0b7b1845](https://github.com/depictio/depictio/commit/0b7b1845))

#### 🐳 Docker Highlights

* Enhance Docker build workflow with security improvements, better output management, and health checks ([e684982b](https://github.com/depictio/depictio/commit/e684982b), [bb65a818](https://github.com/depictio/depictio/commit/bb65a818))
* Add permissions for Docker build job to read contents and write packages ([e82dc682](https://github.com/depictio/depictio/commit/e82dc682))
* Correct path for admin_config.yaml in Docker copy command ([77d3c4ee](https://github.com/depictio/depictio/commit/77d3c4ee))
* Update comment formatting for DEPICTIO_VERSION in docker-compose.dev.yaml ([bee58cb4](https://github.com/depictio/depictio/commit/bee58cb4))

#### 🧪 Testing & CI Highlights

* Enhance Iris integration verification in CI workflow with checks for project, deltatable, and dashboard ([9a8a6b00](https://github.com/depictio/depictio/commit/9a8a6b00))
* Add and refine test fixtures for setting DEPICTIO_CONTEXT environment variable in tests ([cb64d183](https://github.com/depictio/depictio/commit/cb64d183), [596395e6](https://github.com/depictio/depictio/commit/596395e6), [2c5ac43f](https://github.com/depictio/depictio/commit/2c5ac43f))
* Add a test suite for File model validation ([9957daa3](https://github.com/depictio/depictio/commit/9957daa3))
* Add a workflow to notify the documentation repository of new releases ([3dee7132](https://github.com/depictio/depictio/commit/3dee7132))

#### ⎈ Helm Highlights

* Add GitHub Actions workflow for testing, building, and pushing Helm chart based on chart version ([4c965fa6](https://github.com/depictio/depictio/commit/4c965fa6))
* Add persistent volume claims for keys and update deployments to mount them correctly ([fc0926ac](https://github.com/depictio/depictio/commit/fc0926ac), [e2a73584](https://github.com/depictio/depictio/commit/e2a73584))
* Expose MinIO credentials in configmaps and include release name in resource names for better management ([82ca4c2a](https://github.com/depictio/depictio/commit/82ca4c2a), [bdd9af31](https://github.com/depictio/depictio/commit/bdd9af31))
* Fix and standardize Helm chart secrets, configurations, and metadata ([b2fb78d2](https://github.com/depictio/depictio/commit/b2fb78d2), [39ca4f3f](https://github.com/depictio/depictio/commit/39ca4f3f))
* Update versioning scripts and configurations to support Helm chart version bumping ([98ba8b24](https://github.com/depictio/depictio/commit/98ba8b24), [815214af](https://github.com/depictio/depictio/commit/815214af))

#### ♻️ Code Refactoring & Bug Fixes Highlights

* Fix version formatting in pyproject.toml and bumpversion configurations ([79750997](https://github.com/depictio/depictio/commit/79750997), [07324182](https://github.com/depictio/depictio/commit/07324182), [815214af](https://github.com/depictio/depictio/commit/815214af))
* Clean up pre-commit configuration and remove unused imports ([ab6a40e2](https://github.com/depictio/depictio/commit/ab6a40e2), [d6b228b1](https://github.com/depictio/depictio/commit/d6b228b1))

## [v0.0.4](https://github.com/depictio/depictio/releases/tag/v0.0.4)

Generating changelog from dev to v0.0.4

### Docker Images

```bash
ghcr.io/depictio/depictio:0.0.4
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

This changelog highlights the key changes in v0.0.4, organized by category. Special focus has been given to improvements in setup, Docker, Cypress testing, GitHub CI, Beanie implementation, code refactoring, and UI enhancements.

### **⚙️ Setup & Configuration**

* Update email addresses for default users, add .env file for development, and adjust Docker volume paths (a835bb1)
* Implement centralized logging initialization and update logging setup for CLI and models (2f20b67)
* Enhance MinIO configuration and S3 utilities with new integration tests and refactoring (7e4fe38, 3110cfd)
* Implement consistent API internal key generation, loading, and management (df71b3b, 9359bd4, 58f344e)
* Add initial project configurations and Depictio example project generator script (8befa4a, 889888b, 8c502af)

### **🐳 Docker related**

* Update deployment scripts (d052856, 48282e3, 3a959b7)
* Refactor Docker workflows, enhance environment variables, and add support for AMD64/ARM64 builds with version tagging (e0139c6, 75b3652, 455d5ee)
* Update Dockerfiles for improved environment setup and new scripts/dependencies (5ed61af, 3f48a1d, bc4fe1f, b255e7c)
* Enhance Docker setup in deployment workflow with caching, BuildKit, and updated image build steps (8edf857, 7c01dc5)
* Update devcontainer configurations for workspace, zsh, uv package manager, and cloning depictio-models (2ae702c, 01f2dbc, 55964e4)

### **🧪 Testing & CI**

* Add GitHub Actions workflows for automated release creation, changelog generation, Helm chart testing, and Docker image builds (74536b3, 59023b4, 76544d7, ef0e4bf)
* Add end-to-end tests for user authentication, registration, and dashboard management using Cypress (72550ff, 532e9b7, d7382b9)
* Implement comprehensive unit and integration tests for various modules including user models, token management, CLI commands, S3 utilities, and system initialization (df44475, 7340269, cac52fe, e13ace2)
* Migrate pytest configuration to pyproject.toml and add VSCode settings for Python testing (d640f0a, 104de0e)
* Enhance deployment workflows with improved Python setup, dependency installation, caching, and artifact handling (6f33111, d25962d, 48c549b)

### **🧱 Beanie Implementation**

* Implement FastAPI user management with Beanie ODM (6470af8, 47e9cd4)
* Add user creation helpers using Beanie ODM with validation (bc3f3d3)
* Add beanie setup for various tests and update model references to use Beanie models (e.g., ProjectBeanie) (ec008e0, db00fca, aa9796f)
* Update create_group endpoint to support async operations and use GroupBeanie model (848e48f)

### **♻️ Code Refactoring**

* Extensive refactoring of import statements, code organization, and whitespace across numerous files for clarity and consistency (f8b0f91, 1999b6e, e3385c6, 239ad86)
* Refactor user creation, fetching, and token handling logic, often converting to async methods and improving error handling (0f6a7f5, 1fa623e, f6949db, b6c658c)
* Streamline project and data collection retrieval, often removing workflow_id dependencies and using IDs directly (2891d6d, b13dde2, f8163f9)
* Improve ObjectId handling, validation, and serialization in models and API calls (0a59584, bfefec4)
* Move and reorganize code, such as refactoring app.py into multiple files, moving scripts into src/, and modularizing key utilities (374dee5, 429e354, fdee057)

### **🎨 UI Improvements**

* Add and enhance various UI components: password editing modal, color palette page, clipboard functionality, animated badges, segmented controls, stylish modals for dashboard/item creation, and delete confirmation modals (767908f, bfc6818, edc24f5, 321d7d4, 5af06e7, 50e510b)
* Implement project permissions management UI, including user role badges, project visibility toggles, and a dedicated permissions page (d17f369, 221c95b, 0b4d4e4)
* Improve layout and styling for About page, project items, "no projects" message, dashboard modals, and admin management sections (b752a7a, c66f4d8, fbda153, ee47204)
* Enhance dashboard functionality: public/private toggle, edit dashboard name, display project name in header, and add tooltips/badges to tables (9c192bd, 1dcaa12, 3ef45cd)
* Add favicons for branding (6f70d02)

### **🚀 Features (General)**

* Add BaseApiResponse model and enhance data collection configurations (dd272b8)
* Implement API calls for token management, password editing, and various user/group/project/dashboard CRUD operations (4f4439d, 05e51ef, 7cbee90, 6aaed8e, 60974ec)
* Add background task processing for initial data collections and an endpoint to trigger it (6997d36, db56b29)
* Implement user registration logic and endpoints, replacing local lookups with API calls (ad3fa4f, 031a2f3, dd83de7)

### **🐛 Bug Fixes**

* Correct various file paths, IDs, and configurations for consistency and relative access, especially in initial_project_cli.yaml and S3 settings (214659e, 26804fa, 63d55b3, d1a87c9)
* Address issues with user fetching functions, replacing deprecated calls and ensuring async execution (f334386, 725c3d9, 049422e)
* Fix import paths due to module restructuring and clean up unused/commented code (ec1f4f5, 1e82323, f53e9ae)
* Resolve issues with database initialization, including missing collections and enabling data saving (324d39a, aa8ec53)
* Correct dependency management: add missing dependencies (tomli, bleach, typeguard, mypy-boto3-s3) and remove unused ones (5254cfd, c227a29, 5c2b2d8**)**

### Documentation

Full documentation: <https://depictio.github.io/depictio-docs/>

## [v0.0.3](https://github.com/depictio/depictio/releases/tag/v0.0.3)

### Bug Fixes

* Component size were modified to reflect better size on the dashboard

### Features

* Edit component (goes to design part (step 3 of component creation))
* Display/hide component options
* Component options to dmc.ActionIcon (smaller icons without text)
* Reset all filters button
* Change offcanvas sidebar layout
* Admin view (list dashboards)
* Graph interaction (click, select data through "Box select")
* Reset graph interaction (via dedicated button)
* Public/private dashboard (public dashboards are visible but not editable by all users ; possibility to copy public dashboard to private personal dashboard)

## [v0.0.2](https://github.com/depictio/depictio/releases/tag/v0.0.2)

### Bug Fixes

* Switch from dashboard & component ID increment to UUID
* Fix double click on add component button

### Features

* Autosave dashboard
* Duplicate dashboard
* Edit dashboard name
* Admin view (list users)

## [v0.0.1](https://github.com/depictio/depictio/releases/tag/v0.0.1)

### Features

* Initial release of the project
* Support for creating dashboards with multiple components (figure, metrics card, interactive & table)
* Drag & layout components on the dashboard
* Delete components
