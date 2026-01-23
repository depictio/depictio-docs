---
title: "Changelog"
icon: material/update
description: "Track changes and updates to Depictio across different versions."
hide:
  - navigation
---

# Changelog


## **v0.6.0 Beta Releases**

!!! warning "Beta Releases"
    These are pre-release versions intended for testing. Use in production at your own risk.

### **[v0.6.0-b8](https://github.com/depictio/depictio/releases/tag/v0.6.0-b8)** (January 23, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b8
ghcr.io/depictio/depictio:beta
ghcr.io/depictio/depictio:edge
```

#### **🧹 CI/CD**

* **Documentation Workflow**: Fixed race condition where docs update ran before Docker image was pushed by moving `repository_dispatch` to end of Docker build workflow. ([61a1b6fa](https://github.com/depictio/depictio/commit/61a1b6fa))

---

### **[v0.6.0-b7](https://github.com/depictio/depictio/releases/tag/v0.6.0-b7)** (January 23, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b7
```

#### **✨ Features**

* **Fullscreen Mode**: Added fullscreen mode for figure components, allowing users to expand charts to full viewport. ([0fe66bd8](https://github.com/depictio/depictio/commit/0fe66bd8))

#### **🚀 Improvements**

* **Screenshot Generation**: Moved screenshot generation to background Celery task for improved API responsiveness. ([81ce338d](https://github.com/depictio/depictio/commit/81ce338d))
* **Code Cleanup**: Removed 700+ lines of commented backup code from save module. ([ea91dbb6](https://github.com/depictio/depictio/commit/ea91dbb6))

#### **🧹 CI/CD**

* **Docs Workflow Refactor**: Moved API documentation update workflow from depictio repo to depictio-docs repo for better separation of concerns. ([037df501](https://github.com/depictio/depictio/commit/037df501))
* Added tag push trigger to update-api-docs workflow. ([25856c56](https://github.com/depictio/depictio/commit/25856c56))

---

### **[v0.6.0-b5](https://github.com/depictio/depictio/releases/tag/v0.6.0-b5)** (January 23, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b5
ghcr.io/depictio/depictio:edge
```

#### **✨ Features**

* **Gunicorn Token Masking**: Added gunicorn config with token masking in access logs for improved security. ([e22778d9](https://github.com/depictio/depictio/commit/e22778d9))
* **Celery Worker Deployment**: Added Celery worker deployment to Helm charts for background task processing. ([c702296c](https://github.com/depictio/depictio/commit/c702296c))
* **Docker Health Checks**: Added healthchecks and restart policies for production readiness. ([89e8522a](https://github.com/depictio/depictio/commit/89e8522a))
* **Automated OpenAPI Docs**: Added automated OpenAPI spec extraction for documentation. ([0173ecc4](https://github.com/depictio/depictio/commit/0173ecc4))

#### **🐛 Fixes**

* Fixed slider mark labels visibility in dark mode using dmc.Text components. ([a59f9802](https://github.com/depictio/depictio/commit/a59f9802), [d2a0d765](https://github.com/depictio/depictio/commit/d2a0d765))
* Fixed parameter order in update_aggregation_options callback. ([c114b5ec](https://github.com/depictio/depictio/commit/c114b5ec))
* Fixed type check for edit_context before calling .get(). ([17e034c7](https://github.com/depictio/depictio/commit/17e034c7))
* Fixed screenshot trigger and updated accordion selectors for DMC 2.0+. ([cae52478](https://github.com/depictio/depictio/commit/cae52478))
* Added fallback on non-200 status in _check_deltatables. ([adf75978](https://github.com/depictio/depictio/commit/adf75978))
* Fixed triangle background animations visibility on auth page. ([6370fc53](https://github.com/depictio/depictio/commit/6370fc53))

#### **🚀 Improvements**

* Comprehensive code simplification and modularization of Dash components. ([bbf8395e](https://github.com/depictio/depictio/commit/bbf8395e))
* Simplified figure and table component callbacks. ([b83ecf0d](https://github.com/depictio/depictio/commit/b83ecf0d))
* Cleaned up verbose logs in table, text, and multiqc components. ([ebb6c18e](https://github.com/depictio/depictio/commit/ebb6c18e))
* Removed verbose runtime logs from frontend callbacks. ([af750d3f](https://github.com/depictio/depictio/commit/af750d3f))

#### **🧹 CI/CD**

* Use content-based hash for Docker image tags. ([aa9da340](https://github.com/depictio/depictio/commit/aa9da340))
* Switched to uv-based Dockerfile for faster Helm builds. ([8afa0a36](https://github.com/depictio/depictio/commit/8afa0a36))
* Added Celery worker validation to test-build-push workflow. ([d36df38c](https://github.com/depictio/depictio/commit/d36df38c))

---

### **[v0.6.0-b4](https://github.com/depictio/depictio/releases/tag/v0.6.0-b4)** (January 22, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b4
ghcr.io/depictio/depictio:edge
```

#### **✨ Features**

* **Universal DC Linking System**: New cross-DC filtering system that allows linking data collections for runtime filtering without pre-computed joins. ([#640](https://github.com/depictio/depictio/pull/640))
* **Figure Code Mode Refactor**: Complete refactor of figure code mode with live preview, bidirectional editor resize, and improved theme switching. ([#639](https://github.com/depictio/depictio/pull/639))
* **YAML Dashboard Validation**: Pydantic-based validation for dashboard YAML configuration with column name, chart type, and aggregation validation.
* **Client-Side Table Joining**: Moved table joining from server to CLI for better performance and flexibility. ([#634](https://github.com/depictio/depictio/pull/634))

#### **🐛 Fixes**

* Fixed Ace editor theme switching and Execute button functionality in figure code mode.
* Fixed HTTP status code checks for link create/delete in CLI.
* Improved syntax error messages for code execution in figures.

---

### **[v0.6.0-b3](https://github.com/depictio/depictio/releases/tag/v0.6.0-b3)** (January 20, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b3
```

#### **✨ Features**

* **Figure Component Improvements**: Loading indicator for figure preview rendering, improved stepper UX. ([#622](https://github.com/depictio/depictio/pull/622))
* **Celery by Default**: Celery is now enabled by default for design mode with Docker Compose profiles for flexible deployment.
* **AI Development Tools**: Added Claude Code development toolkit and AI tools support in devcontainer.

#### **🐛 Fixes**

* Eliminated multiple scrollbars in dashboard edit mode.
* Fixed optional parameters persisting incorrectly in figure component.
* Improved stepper header centering and spacing.

---

### **[v0.6.0-b2](https://github.com/depictio/depictio/releases/tag/v0.6.0-b2)** (January 8, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b2
```

#### **✨ Features**

* **Dashboard Performance & UX**: Major performance improvements with ALL pattern rendering for cards and interactive components. ([#616](https://github.com/depictio/depictio/pull/616))
* **Local Delta Table Caching**: Added local filesystem caching for Delta tables to improve API performance.
* **Client-Side Performance Monitoring**: Added performance monitoring utilities for frontend optimization.

#### **🐛 Fixes**

* Suppressed third-party console warnings and fixed favicon issues.
* Fixed frontend container startup issues in CI.
* Improved quality job caching to skip when no code changes.

---

### **[v0.6.0-b1](https://github.com/depictio/depictio/releases/tag/v0.6.0-b1)** (January 7, 2026)

#### Docker Images

```bash
ghcr.io/depictio/depictio:0.6.0-b1
```

#### **✨ Major Features**

* **Multi-App Architecture**: Refactored frontend into three independent Dash applications for improved performance and callback isolation. ([#615](https://github.com/depictio/depictio/pull/615), [#616](https://github.com/depictio/depictio/pull/616))
    * **Management App** (`/`): Auth, dashboards, projects, admin
    * **Viewer App** (`/dashboard/`): Read-only dashboard viewing
    * **Editor App** (`/dashboard-edit/`): Dashboard editing and component builder
* **Two-Panel Layout**: Dashboard components are now organized into left (filters) and right (visualizations) panels.
* **Dashboard Tabs**: Support for tabbed organization within dashboards with custom icons and colors.
* **Table Component Export**: Export table data to CSV with support for filters and sorting. ([#625](https://github.com/depictio/depictio/pull/625))
* **Celery Background Processing**: Redis/Celery integration for heavy computations in design mode.

#### **🚀 Improvements**

* Dual-panel grid system with save/restore functionality.
* Enhanced interactive component design and edit mode callbacks.
* Improved card component metadata handling.
* Centralized version management in VERSION file.

---

## **[v0.5.3](https://github.com/depictio/depictio/releases/tag/v0.5.3)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.5.3
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **🐛 Fixes**

* Preserve original IDs during project creation to ensure consistency across K8s instances  [d4a57a5d](https://github.com/depictio/depictio/commit/d4a57a5d)

## **[v0.5.2](https://github.com/depictio/depictio/releases/tag/v0.5.2)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.5.2
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Features**

* **S3 & Project Management**: Added S3 delta table checks, improved project ID handling, and auto-promotion for data collection IDs with join configurations. ([bc31ff79](https://github.com/depictio/depictio/commit/bc31ff79), [103baee8](https://github.com/depictio/depictio/commit/103baee8), [7dfdcc24](https://github.com/depictio/depictio/commit/7dfdcc24))
* **Dashboard Enhancements**: Improved filtering logic, enhanced permission checks, component resizing, and metadata synchronization. ([3e259297](https://github.com/depictio/depictio/commit/3e259297), [c913dd2b](https://github.com/depictio/depictio/commit/c913dd2b), [aa03799f](https://github.com/depictio/depictio/commit/aa03799f), [d03deeb8](https://github.com/depictio/depictio/commit/d03deeb8))
* **Icon & Styling Updates**: Updated dashboard icons with ActionIcon, DashIconify refactor, and improved figure/component styling. ([ce4acaca](https://github.com/depictio/depictio/commit/ce4acaca), [1e9e9d8a](https://github.com/depictio/depictio/commit/1e9e9d8a), [76c55c18](https://github.com/depictio/depictio/commit/76c55c18))
* **MultiQC Enhancements**: Added styling and metadata handling for MultiQC data collections. ([b2d995fd](https://github.com/depictio/depictio/commit/b2d995fd))
* **Workflow & Helm Support**: URL pattern helpers for API/MinIO and improved backend/frontend deployments. ([5a7850f1](https://github.com/depictio/depictio/commit/5a7850f1), [d09e6096](https://github.com/depictio/depictio/commit/d09e6096))

---

### **🐛 Fixes**

* **UI & Layout**: Prevented horizontal scrollbar, removed default background on draggable components, adjusted theme switch behavior. ([310a8d9f](https://github.com/depictio/depictio/commit/310a8d9f), [6e06fd6c](https://github.com/depictio/depictio/commit/6e06fd6c), [937e08b1](https://github.com/depictio/depictio/commit/937e08b1))
* **Standardization & Cleanup**: Fixed naming inconsistencies in Iris Dashboard demo and commented out redundant tests/code. ([ca6ee804](https://github.com/depictio/depictio/commit/ca6ee804), [d7d8a3d8](https://github.com/depictio/depictio/commit/d7d8a3d8), [8a83fe7b](https://github.com/depictio/depictio/commit/8a83fe7b), [acf26a86](https://github.com/depictio/depictio/commit/acf26a86))

## **[v0.5.1](https://github.com/depictio/depictio/releases/tag/v0.5.1)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.5.1
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **🐛 Fixes**

* **UI & State**: Updated handle colors, navbar/logo sizing, layout IDs, and removed unused states. ([08938777](https://github.com/depictio/depictio/commit/08938777), [435aa448](https://github.com/depictio/depictio/commit/435aa448), [a164f8cb](https://github.com/depictio/depictio/commit/a164f8cb))
* **Caching**: Fixed Redis cache stats logging. ([ffcfd7a1](https://github.com/depictio/depictio/commit/ffcfd7a1))

---

### **🚀 Improvements**

* **Theming & Layout**: Enhanced clientside layout, padding, resize handle visibility, and logo updates. ([b10bf77b](https://github.com/depictio/depictio/commit/b10bf77b), [58b0690b](https://github.com/depictio/depictio/commit/58b0690b), [250437a2](https://github.com/depictio/depictio/commit/250437a2))
* **Redis Integration in K8S**: Added support with configuration and connectivity tests. ([f86b4f10](https://github.com/depictio/depictio/commit/f86b4f10))
* **Theme Cleanup**: Removed dark theme–specific styles from auth modal and Google button. ([6ddaf469](https://github.com/depictio/depictio/commit/6ddaf469))
* **Component Editing**: Always create component buttons in edit mode and determine initial edit state. ([669fdc92](https://github.com/depictio/depictio/commit/669fdc92), [1e56ebe3](https://github.com/depictio/depictio/commit/1e56ebe3))
* **Dashboard UI**: Improved header, modal layout, subtitle/icon customization, and sidebar/navbar handling. ([ba99f97b](https://github.com/depictio/depictio/commit/ba99f97b), [40d10c09](https://github.com/depictio/depictio/commit/40d10c09), [0d4ad756](https://github.com/depictio/depictio/commit/0d4ad756))

## **[v0.5.0](https://github.com/depictio/depictio/releases/tag/v0.5.0)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.5.0
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Features**

* **MultiQC Integration**: Added a dedicated component to visualize and explore MultiQC outputs directly in the dashboard. This includes report scanning and aggregation, component creation through the MultiQC API, figure patching to link with external metadata, and dataset filtering to display resulting samples. ([2f1e9d31](https://github.com/depictio/depictio/commit/2f1e9d31))
* **User Experience**: Introduced a new header design with cleaner layout and added iconography for better navigation. ([d6f0c1b2](https://github.com/depictio/depictio/commit/d6f0c1b2))
* **Table Enhancements**: Added column selector and filtering options to DataTable for more flexible data exploration. ([d53caae1](https://github.com/depictio/depictio/commit/d53caae1))
* **Live Updates**: Implemented dynamic refresh for dashboard elements to reflect state changes instantly. ([46a4e0a3](https://github.com/depictio/depictio/commit/46a4e0a3))

---

### **🛠 Fixes**

* **Data Handling**: Resolved issues with inconsistent plot rendering and duplicate state updates. ([02c5e7e4](https://github.com/depictio/depictio/commit/02c5e7e4))
* **Theme Sync**: Fixed a race condition during theme switching that caused UI flickers. ([30b9f24d](https://github.com/depictio/depictio/commit/30b9f24d))

---

### **🚀 Improvements**

* **Performance**: Optimized DataTable rendering and minimized unnecessary callback triggers. Introduced a new component update mechanism switching from full sequential rendering to initial rendering followed by parallel patching of components using Dash properties. ([f8e2f5a1](https://github.com/depictio/depictio/commit/f8e2f5a1))
* **UI Responsiveness**: Moved more callbacks clientside for smoother interactions and reduced latency. ([a86bf22e](https://github.com/depictio/depictio/commit/a86bf22e))
* **Code Cleanup**: Simplified logging and removed obsolete debug statements. ([bc2a93d4](https://github.com/depictio/depictio/commit/bc2a93d4))

## **[v0.4.0](https://github.com/depictio/depictio/releases/tag/v0.4.0)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.4.0
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Features**

* **Caching & Performance**: Added `flask-caching` and `orjson` for faster data handling. ([b3bdd21f](https://github.com/depictio/depictio/commit/b3bdd21f))
* **UI Interactivity**: Introduced Dock-style animations and live mode toggle. ([0b6d073e](https://github.com/depictio/depictio/commit/0b6d073e), [14fe2314](https://github.com/depictio/depictio/commit/14fe2314))
* **Data Debugging**: Added scripts for DataTable and plot input inspection. ([b62fe583](https://github.com/depictio/depictio/commit/b62fe583))

---

### **🚀 Improvements**

* **Editing Flow**: Refined UI elements, edit mode logic, and live interactivity. ([71c78e83](https://github.com/depictio/depictio/commit/71c78e83), [a01f3ac9](https://github.com/depictio/depictio/commit/a01f3ac9))
* **Theme & Rendering**: Optimized theme updates and fixed marginal plot loops. ([b05a5c9d](https://github.com/depictio/depictio/commit/b05a5c9d), [0149dcca](https://github.com/depictio/depictio/commit/0149dcca))
* **Performance**: Moved UI state to clientside, added caching, and improved async handling. ([59c40d06](https://github.com/depictio/depictio/commit/59c40d06), [e80e57d2](https://github.com/depictio/depictio/commit/e80e57d2), [696748d1](https://github.com/depictio/depictio/commit/696748d1))

## **[v0.3.2](https://github.com/depictio/depictio/releases/tag/v0.3.2)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.3.2
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Features**

* **Analytics & Session Management**: Enhanced analytics session management, including cleanup for anonymous sessions. Implemented both in-house analytics & Google Analytics integration to track unique connections and user activity. ([956d35f3](https://github.com/depictio/depictio/commit/956d35f3), [146e042a](https://github.com/depictio/depictio/commit/146e042a))
* **Admin Dashboard**: Implemented a dedicated Admin Analytics Dashboard with related functionalities in admin section. Enhanced the analytics data service to include user ID validation and filtering for more precise data. ([8837a4fd](https://github.com/depictio/depictio/commit/8837a4fd), [41061497](https://github.com/depictio/depictio/commit/41061497))

### **🚀 Improvements**

* **Configuration**: Updated MinIO and backend configurations to optimize resource limits and enhance security context. ([9e681bfc](https://github.com/depictio/depictio/commit/9e681bfc))

## **[v0.3.1](https://github.com/depictio/depictio/releases/tag/v0.3.1)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.3.1
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **🐛 Bug Fixes**

* **Helm Chart & Deployment**: Adjusted resource limits and logging verbosity for backend services. Ensured proper permissions for frontend mounted directories and fixed authentication defaults in values.yaml. ([1ddc1d5e](https://github.com/depictio/depictio/commit/1ddc1d5e), [47214581](https://github.com/depictio/depictio/commit/47214581), [e574a013](https://github.com/depictio/depictio/commit/e574a013))
* **Data Integrity**: Ensured depictio_run_id is included in joins for proper run isolation and normalized column data types in precompute_columns_specs function. ([e21ef1eb](https://github.com/depictio/depictio/commit/e21ef1eb), [f5ce756d](https://github.com/depictio/depictio/commit/f5ce756d))

### **🚀 Improvements**

* **Code Cleanliness & Consistency**: Standardized import statements across multiple files and removed unused imports. ([0349df19](https://github.com/depictio/depictio/commit/0349df19), [53b6b467](https://github.com/depictio/depictio/commit/53b6b467))
* **Testing**: Implemented robust typing commands for improved input reliability in tests. ([f85a98e4](https://github.com/depictio/depictio/commit/f85a98e4))

### **🧹 Chores**

* **Logging**: Enhanced logging in API calls and data collection processing functions. ([0d662764](https://github.com/depictio/depictio/commit/0d662764))
* **UMAP**: Disabled UMAP visualization temporarily. ([593ad1dd](https://github.com/depictio/depictio/commit/593ad1dd))

## **[v0.3.0](https://github.com/depictio/depictio/releases/tag/v0.3.0)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.3.0
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Major Features**

* **Enhanced Data Management**: Optimized DataFrame loading with lazy scanning and adaptive memory management. Implemented total storage size calculation and progress indicators for data collections. ([a308c300](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/a308c300), [8afcdf2e](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/8afcdf2e), [bfcb6fd8](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/bfcb6fd8))
* **Comprehensive Project & Data Collection Management**: Introduced new modal-based UI to manage workflows and data collection per project. Added features for creating, updating, deleting, and viewing data collections and projects. ([b9cb4727](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/b9cb4727), [78b93457](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/78b93457), [fb06d84e](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/fb06d84e))

### **🐛 Bug Fixes**

* **Temp users data handling**: Improved error handling for temporary user cleanup. ([1253e8a6](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/1253e8a6), [6fd41333](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/6fd41333))
* **Figures & Components Logic**: Added validation to prevent df reassignment in user code. Fix “Edit mode” for figure components. Enhanced figure generation to allow editing existing figures even with auto-generation disabled. ([318c7ae9](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/318c7ae9), [48f91115](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/48f91115))
* **UI & Layout**: Corrected project update logic and improved modal ID handling. ([f6b68c73](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/f6b68c73), [93d72bba](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/93d72bba))

### **🚀 Improvements**

* **CLI & Theming Enhancements**: Added customizable ASCII logo display for the CLI. Implemented theme-aware color handling for card and interactive components. ([63a0e62f](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/63a0e62f), [7d5957f0](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/7d5957f0), [1c201684](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/1c201684))

## **[v0.2.1](https://github.com/depictio/depictio/releases/tag/v0.2.1)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.2.1
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Features**

* **Theming & Components**: Plotly templates were updated to 'mantine_light' and 'mantine_dark'. AG Grid and text components now have theme-aware styling. ([04e4069e](https://github.com/depictio/depictio/commit/04e4069e), [97e6c0f5](https://github.com/depictio/depictio/commit/97e6c0f5))
* **Interactivity & Access**: Interactive components can now restore saved configurations and values. Added EMBL-specific security contexts for unauthenticated mode. ([892de076](https://github.com/depictio/depictio/commit/892de076), [08a6e311](https://github.com/depictio/depictio/commit/08a6e311), [db18d84f](https://github.com/depictio/depictio/commit/db18d84f))

### **🐛 Bug Fixes**

* **Security & Stability**: Addressed security vulnerabilities by updating seccompProfile. Fixed an UnboundLocalError and ensured metadata store indices are consistent. ([1b18d95a](https://github.com/depictio/depictio/commit/1b18d95a), [e828952a](https://github.com/depictio/depictio/commit/e828952a), [5a550856](https://github.com/depictio/depictio/commit/5a550856))
* **Layout & Visuals**: Resolved footer positioning issues and adjusted default component dimensions for better layout consistency. ([f245982e](https://github.com/depictio/depictio/commit/f245982e), [2e16fdb9](https://github.com/depictio/depictio/commit/2e16fdb9))
* **Visuals**: Updated logo images in the README for improved visibility in both light and dark modes. ([ca46ddc1](https://github.com/depictio/depictio/commit/ca46ddc1))

### **🚀 Improvements**

* **Code Refactoring**: Simplified input handling in save and text component callbacks. ([8937bea3](https://github.com/depictio/depictio/commit/8937bea3))

### **🧹 Chores**

* **Logging**: Refactored logging in various modules to reduce verbosity. ([322c80c1](https://github.com/depictio/depictio/commit/322c80c1))
* **Version**: Bumped the project version from 0.2.0 to 0.2.1. ([8cd1e0e2](https://github.com/depictio/depictio/commit/8cd1e0e2))

## **[v0.2.0](https://github.com/depictio/depictio/releases/tag/v0.2.0)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.2.0
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Major Features**

* **UI Theming & UX**: Fully functional dark/light theme ([68af2cc0](https://github.com/depictio/depictio/commit/68af2cc0), [b085b89b](https://github.com/depictio/depictio/commit/b085b89b)). Switched from dash-draggable to dash-dynamic-react-grid ([aacea638](https://github.com/depictio/depictio/commit/aacea638)). Revised UX with improved component buttons layout. Implemented progressive loading over dashboard restore + logo animation ([e40ba587](https://github.com/depictio/depictio/commit/e40ba587), [d8d696d2](https://github.com/depictio/depictio/commit/d8d696d2)).
* **Figure component**: UI mode completely revised > switching from documentation parsing to function signature inspection and organisation into pydantic models. New code mode allowing user to write/port existing code with RestrictedPython providing code filtering and restricted execution environment to limit dangerous operations. ([691a2678](https://github.com/depictio/depictio/commit/691a2678), [b5c229b2](https://github.com/depictio/depictio/commit/b5c229b2))
* **Table component**: Infinite scrolling and pagination for the table component ([99f8e5a2](https://github.com/depictio/depictio/commit/99f8e5a2), [5466aa76](https://github.com/depictio/depictio/commit/5466aa76)).
* **Text component**: Inline editable text components (using markdown headers style) with adjustable positioning (justify). ([2b2d267a](https://github.com/depictio/depictio/commit/2b2d267a), [114f713e](https://github.com/depictio/depictio/commit/114f713e), [59c8fc80](https://github.com/depictio/depictio/commit/59c8fc80))
* **Card component**: improved styling & provide trend information to show difference compare to non filtered data (increase/decrease) ([9f2ab88c](https://github.com/depictio/depictio/commit/9f2ab88c), [6d51e3af](https://github.com/depictio/depictio/commit/6d51e3af))
* **Interactive component**: switched every component to DMC. Implemented scale (log/linear) + number of marks for slider & rangeslider components. ([c73f4204](https://github.com/depictio/depictio/commit/c73f4204), [9f2ab88c](https://github.com/depictio/depictio/commit/9f2ab88c), [7f99958f](https://github.com/depictio/depictio/commit/7f99958f))
* **Notes & documentation footer**: notes taking using dmc.RichTextEditor (markdown style, links, bullet points, code blocks …) with fullscreen mode and responsive layout. ([d226f52b](https://github.com/depictio/depictio/commit/d226f52b), [3af94fd3](https://github.com/depictio/depictio/commit/3af94fd3), [b06eb2ee](https://github.com/depictio/depictio/commit/b06eb2ee), [f245982e](https://github.com/depictio/depictio/commit/f245982e))
* **Buttons**: Reset button functionality and visibility logic for interactive components ([583aa04f](https://github.com/depictio/depictio/commit/583aa04f), [166a2af1](https://github.com/depictio/depictio/commit/166a2af1), [52684721](https://github.com/depictio/depictio/commit/52684721), [8e5ef9cc](https://github.com/depictio/depictio/commit/8e5ef9cc)).

### **🐛 Bug Fixes**

* **Component & UI Fixes**:
  * Resolved circular reference issues in the dashboard context and fixed AG Grid popup visibility ([2b9e64c9](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/2b9e64c9), [f5bf946d](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/f5bf946d)).
  * Addressed layout issues for Accordion components on the projects page and improved styles for draggable components in dark mode ([d8907eae](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/d8907eae), [6c9febbf](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/6c9febbf)).
* **Authentication & CI**: Fixed Google OAuth configuration and routes, and addressed CI issues related to authentication ([19396605](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/19396605), [78dbc295](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/78dbc295)).
* **Cypress Tests**: Updated header element selectors and improved modal visibility checks in Cypress tests ([b17fb7bb](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/b17fb7bb)).

### **🚀 Improvements**

* **Dash Component Refactoring**: Refactored Dash components to use updated props and styling conventions, ensuring compatibility with Dash v3 and Dash Mantine 2.0+ ([8ed8f068](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/8ed8f068), [a7a0e3bb](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/a7a0e3bb)).
* **Code & Styling Refactoring**: Improved overall code structure for enhanced readability and maintainability, and refactored auth modal styles for better appearance ([3ff3e54d](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/3ff3e54d), [7ed7c995](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/7ed7c995)).

### **Chores 🧹**

* **Dependencies**: Added SVG format for logos ([9a9ceb9f](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/9a9ceb9f)).
* **Pre-commit**: Improved pre-commit hooks for code quality enforcement ([75cb3058](https://www.google.com/search?q=https://github.com/depictio/depictio/commit/75cb3058)).

## **[v0.1.1](https://github.com/depictio/depictio/releases/tag/v0.1.1)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.1.1
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Major Features**

* **UI Theming**: Implemented functional dark/light modes with auto-theming, including progress on Plotly figures, dashboard button visibility, and projects section theming ([a851f175](https://github.com/depictio/depictio/commit/a851f175), [d6d83410](https://github.com/depictio/depictio/commit/d6d83410)).

### **🐛 Bug Fixes**

* **Cypress Tests**: Updated header element selectors and improved modal visibility checks in Cypress tests ([b17fb7bb](https://github.com/depictio/depictio/commit/b17fb7bb)).
* **Authentication**: Removed unused expiry_minutes parameters from user upgrade API calls and fixed CI issues related to authentication ([b9c5241f](https://github.com/depictio/depictio/commit/b9c5241f), [78dbc295](https://github.com/depictio/depictio/commit/78dbc295)).
* **CLI Configuration**: Resolved inconsistencies in CLI configuration field names and updated mock configurations for tests ([ce91c581](https://github.com/depictio/depictio/commit/ce91c581), [846fd4c1](https://github.com/depictio/depictio/commit/846fd4c1)).

### **🚀 Improvements**

* **Dash Components**: Refactored Dash components to use updated props and styling conventions, ensuring compatibility with Dash v3 and Dash Mantine 2.0+ ([8ed8f068](https://github.com/depictio/depictio/commit/8ed8f068), [a7a0e3bb](https://github.com/depictio/depictio/commit/a7a0e3bb)).
* **Code Structure**: Improved overall code structure for enhanced readability and maintainability across various modules ([3ff3e54d](https://github.com/depictio/depictio/commit/3ff3e54d), [89e62ec9](https://github.com/depictio/depictio/commit/89e62ec9)).

### **🧹Chores**

* **Pre-commit**: Initialized pre-commit hooks for code quality enforcement ([75cb3058](https://github.com/depictio/depictio/commit/75cb3058)).

## **[v0.1.0](https://github.com/depictio/depictio/releases/tag/v0.1.0)**

### Docker Images

```bash
ghcr.io/depictio/depictio:0.1.0
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

### **✨ Major Features**

* **Backup & Restore**: Implemented a comprehensive S3 backup and restore strategy manager, including CLI commands and endpoints for seamless integration ([92ce14ff](https://github.com/depictio/depictio/commit/92ce14ff), [c126e407](https://github.com/depictio/depictio/commit/c126e407)).

* **Unauthenticated Mode & Temporary Users**: Added full support for an unauthenticated mode with automatic anonymous login and temporary user creation for defined time, including session management, upgrade options, and automated creation and cleanup features  ([38ff59d7](https://github.com/depictio/depictio/commit/38ff59d7), [6caf2863](https://github.com/depictio/depictio/commit/6caf2863), [7622d11f](https://github.com/depictio/depictio/commit/7622d11f), [a5d70429](https://github.com/depictio/depictio/commit/a5d70429)).
* **Google OAuth**: Implemented Google OAuth authentication endpoints and updated related configurations ([a07364cb](https://github.com/depictio/depictio/commit/a07364cb), [19396605](https://github.com/depictio/depictio/commit/19396605)).

### **🐛 Bug Fixes**

* **Screenshot Generation**: Resolved screenshot endpoint authentication and CI timeout issues, and simplified screenshot generation tests ([faecb4ec](https://github.com/depictio/depictio/commit/faecb4ec), [98598ee5](https://github.com/depictio/depictio/commit/98598ee5)).

### **🚀 Improvements**

* **Performance & Caching**: Implemented caching for iterative joins, component data, workflows, and data collection specs to significantly enhance performance ([78a7704a](https://github.com/depictio/depictio/commit/78a7704a), [cc7d7dbe](https://github.com/depictio/depictio/commit/cc7d7dbe)).
* **E2E Tests**: Enhanced Cypress tests with improved Chrome configuration and reliability, including better login handling and dashboard navigation ([dba2e3e3](https://github.com/depictio/depictio/commit/dba2e3e3), [ca9fac6c](https://github.com/depictio/depictio/commit/ca9fac6c)).
* **Code Structure**: Refactored the code structure across multiple modules for improved readability and maintainability ([3f1f1b9b](https://github.com/depictio/depictio/commit/3f1f1b9b), [dfeaf1f6](https://github.com/depictio/depictio/commit/dfeaf1f6)).
* **Type checking**: Implemented type checking with `ty` for better code quality and consistency.
* **Logging**: Reduced logging verbosity across various modules for improved log management and clarity ([edd44b51](https://github.com/depictio/depictio/commit/edd44b51), [4e408f36](https://github.com/depictio/depictio/commit/4e408f36)).

### **🧹Chores**

* **Changelog & CI**: Updated changelog generation, fixed release DNS issues in Helm CI, and added a CODEOWNERS file ([dd019370](https://github.com/depictio/depictio/commit/dd019370)).

## **[v0.0.6](https://github.com/depictio/depictio/releases/tag/v0.0.6)**

```bash
ghcr.io/depictio/depictio:0.0.6
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

This release focuses on significant enhancements across Authentication, User Management, and Security, making the application more robust and secure. Key improvements include refresh token, fix issues related to outdated tokens and provide a consolidated CI workflows for the CLI.

### **✨ Features & Improvements**

* **Authentication**: Implemented refresh token support across token management, enhancing security and user session persistence ([6a198be9](https://github.com/depictio/depictio/commit/6a198be9), [ae25380f](https://github.com/depictio/depictio/commit/ae25380f)).
* **User Management**: Updated the user creation process to allow optional user IDs and group parameters, and improved user existence checks ([66d6aec9](https://github.com/depictio/depictio/commit/66d6aec9)).
* **Security**: Added a Flask security assessment scanner for comprehensive application security checks ([caa5476c](https://github.com/depictio/depictio/commit/caa5476c)).

### **⌨️ CLI Highlights**

* **CI/CD**: Consolidated CI workflows by adding test, lint, build, and publish steps for depictio-cli ([83abfc65](https://github.com/depictio/depictio/commit/83abfc65)).
* **Project Structure**: Updated CI workflows and initial CLI structure, removing setup.py and adjusting pyproject.toml for dependencies ([2915d3d2](https://github.com/depictio/depictio/commit/2915d3d2)).
* **Packaging**: Fixed package directory mapping and license format in pyproject.toml ([9147327f](https://github.com/depictio/depictio/commit/9147327f), [af37c922](https://github.com/depictio/depictio/commit/af37c922)).

### **💻 Gitpod & Dev Environment Highlights**

* **Setup**: Added and enhanced Gitpod workspace setup, including zsh, starship configuration, and Docker permissions ([e47b0c27](https://github.com/depictio/depictio/commit/e47b0c27), [a1e50c03](https://github.com/depictio/depictio/commit/a1e50c03)).
* **Configuration**: Made backend and MinIO ports visible in Gitpod configuration for easier access during development ([d091cfc6](https://github.com/depictio/depictio/commit/d091cfc6)).
* **Environment**: Updated environment configuration for Gitpod setup and adjusted logging verbosity for a cleaner development experience ([6b74b5f2](https://github.com/depictio/depictio/commit/6b74b5f2)).

### **🧪 Testing & CI Highlights**

* **Connectivity**: Enhanced inter-service connectivity tests with readiness checks and improved error handling ([ea147c59](https://github.com/depictio/depictio/commit/ea147c59)).
* **Release Process**: Enhanced release name generation in CI to ensure DNS compliance ([86d5feaf](https://github.com/depictio/depictio/commit/86d5feaf)).
* **Issue Templates**: Improved issue templates for bug reports and feature requests to streamline contributions ([a0fa5096](https://github.com/depictio/depictio/commit/a0fa5096)).

### **🐳 Docker & Helm Highlights**

* **Gunicorn**: Fixed a single-worker issue with Gunicorn and optimized timeouts ([16d3a92d](https://github.com/depictio/depictio/commit/16d3a92d)).
* **Helm**: Updated public URLs in ConfigMaps and improved MongoDB connection logic and MinIO configuration in Helm charts ([b93ee6cf](https://github.com/depictio/depictio/commit/b93ee6cf), [dce087f8](https://github.com/depictio/depictio/commit/dce087f8)).
* **Helm**: Fixed an issue with backend service name in the ConfigMap to enable screenshot generation ([965ca53b](https://github.com/depictio/depictio/commit/965ca53b)).

## [v0.0.5](https://github.com/depictio/depictio/releases/tag/v0.0.5)

### Docker Images

```bash
ghcr.io/depictio/depictio:0.0.5
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

This version brings substantial updates to S3 & Services configuration, streamlining data handling and external service integration. Notable progress has also been made in CLI execution logic and Docker build workflows, alongside critical Helm chart improvements.

### **⚙️ Setup & Configuration Highlights**

* **S3 & Services**: Enhanced S3 configuration handling, logging, and URL management for better integration between internal and external services ([54fec27c](https://github.com/depictio/depictio/commit/54fec27c), [49ded59c](https://github.com/depictio/depictio/commit/49ded59c), [5eb17f50](https://github.com/depictio/depictio/commit/5eb17f50)).
* **Data**: Added the Palmer Penguins dataset to test and validate the sequencing-runs ingestion pipeline ([0b7b1845](https://github.com/depictio/depictio/commit/0b7b1845)).
* **Environment**: Added a step to generate the .env file from an example in deployment workflows to ensure consistency ([f5ad8f11](https://github.com/depictio/depictio/commit/f5ad8f11)).

### **⌨️ CLI Highlights**

* **CI/CD**: Added a dedicated GitHub Actions workflow for testing, linting, and building the depictio-cli package ([46503f33](https://github.com/depictio/depictio/commit/46503f33)).
* **Execution**: Refactored the scan/processing logic to improve logging and implemented a run function for a full, end-to-end execution of all steps ([c3335e41](https://github.com/depictio/depictio/commit/c3335e41)).
* **Commands**: Added run and standalone commands, improved logging, and updated command documentation ([0bad4848](https://github.com/depictio/depictio/commit/0bad4848), [b3d6a8a9](https://github.com/depictio/depictio/commit/b3d6a8a9)).

### **🐳 Docker Highlights**

* **CI/CD**: Enhanced the Docker build workflow with improved security, better output management, and service health checks ([e684982b](https://github.com/depictio/depictio/commit/e684982b), [bb65a818](https://github.com/depictio/depictio/commit/bb65a818)).
* **Configuration**: Corrected the path for admin_config.yaml in the Docker copy command ([77d3c4ee](https://github.com/depictio/depictio/commit/77d3c4ee)).

### **🧪 Testing & CI Highlights**

* **CI/CD Workflow Refactoring**: Refactored the main deployment workflow by splitting it into smaller, more manageable CI jobs with enhanced logging ([1d605c88](https://github.com/depictio/depictio/commit/1d605c88), [e8f1bbf2](https://github.com/depictio/depictio/commit/e8f1bbf2)).
* **Integration Tests**: Enhanced the Iris dataset integration test with verification checks for project, deltatable, and dashboard creation ([9a8a6b00](https://github.com/depictio/depictio/commit/9a8a6b00)).
* **Test Environment**: Added and refined test fixtures to properly set the DEPICTIO_CONTEXT environment variable for tests ([cb64d183](https://github.com/depictio/depictio/commit/cb64d183), [596395e6](https://github.com/depictio/depictio/commit/596395e6)).

### **⎈ Helm Highlights**

* **CI/CD**: Added a dedicated GitHub Actions workflow for testing, building, and pushing the Helm chart ([4c965fa6](https://github.com/depictio/depictio/commit/4c965fa6)).
* **Configuration**: Improved service port variables, initContainers, MongoDB connection logic, and MinIO configuration ([959ee2e9](https://github.com/depictio/depictio/commit/959ee2e9), [dce087f8](https://github.com/depictio/depictio/commit/dce087f8)).
* **Storage**: Added persistent volume claims for keys and adjusted default storage sizes for various components ([fc0926ac](https://github.com/depictio/depictio/commit/fc0926ac), [cd1de3f8](https://github.com/depictio/depictio/commit/cd1de3f8)).
* **Ingress**: Enhanced the ingress configuration with default annotations, timeout settings, and correct service hostnames ([4d75fb17](https://github.com/depictio/depictio/commit/4d75fb17), [770d8e5d](https://github.com/depictio/depictio/commit/770d8e5d)).

## [v0.0.4](https://github.com/depictio/depictio/releases/tag/v0.0.4)

Generating changelog from dev to v0.0.4

### Docker Images

```bash
ghcr.io/depictio/depictio:0.0.4
ghcr.io/depictio/depictio:latest
ghcr.io/depictio/depictio:stable
ghcr.io/depictio/depictio:edge
```

This release introduces a first version of project-level permissions and user management features, enhancing access control for collaboration. Major UI/UX improvements and a fundamental backend refactoring to a project-centric architecture also define this version.

### **✨ Features & Improvements**

* **Permissions & User Management**: Introduced initial project-level permissions management, user and group management features, including endpoints and UI modals for creation, deletion, and management ([d17f3690](https://github.com/depictio/depictio/commit/d17f3690), [10af7623](https://github.com/depictio/depictio/commit/10af7623)).
* **Authentication & API**: Added SAML integration, API calls for token management, password editing, user registration, and improved API key validation ([47e9cd43](https://github.com/depictio/depictio/commit/47e9cd43), [7b9f5437](https://github.com/depictio/depictio/commit/7b9f5437)).
* **Dashboarding**: Enhanced dashboard public/private toggles, edit functionality, and project-specific handling, including screenshot capturing ([532e9b7c](https://github.com/depictio/depictio/commit/532e9b7c), [9c192bd0](https://github.com/depictio/depictio/commit/9c192bd0)).

### **🎨 UI & UX Highlights**

* **Modals & Components**: Introduced new UI components like password editing modals and stylish modals for dashboard/item creation and deletion confirmations ([767908fc](https://github.com/depictio/depictio/commit/767908fc), [50e510b8](https://github.com/depictio/depictio/commit/50e510b8)).
* **Layout & Styling**: Improved the layout and styling across the application, notably for project items and admin management sections, with added branding favicons ([c66f4d87](https://github.com/depictio/depictio/commit/c66f4d87), [6f70d027](https://github.com/depictio/depictio/commit/6f70d027)).

### **⚙️ Setup & Configuration**

* **Environment & Logging**: Refined environment variable handling and implemented centralized logging initialization ([a835bb16](https://github.com/depictio/depictio/commit/a835bb16), [2f20b67c](https://github.com/depictio/depictio/commit/2f20b67c)).
* **Database & Storage**: Enhanced MongoDB connection handling and initial project/user creation during database initialization, alongside MinIO configuration ([93e3d610](https://github.com/depictio/depictio/commit/93e3d610), [cd9fa0b9](https://github.com/depictio/depictio/commit/cd9fa0b9)).

### **🐳 Docker & Dev Environment Highlights**

* **Docker Workflows & Builds**: Refactored Docker workflows, enhanced environment variables, and added support for AMD64/ARM64 builds ([d052856e](https://github.com/depictio/depictio/commit/d052856e), [e0139c67](https://github.com/depictio/depictio/commit/e0139c67)).
* **Devcontainer Configurations**: Enhanced Gitpod and devcontainer configurations to streamline local development setup ([2ae702cc](https://github.com/depictio/depictio/commit/2ae702cc)).

### **🧪 Testing & CI Highlights**

* **GitHub Actions Workflows**: Added comprehensive GitHub Actions workflows for automated release creation, changelog generation, and Docker image builds ([74536b3d](https://github.com/depictio/depictio/commit/74536b3d), [76544d7c](https://github.com/depictio/depictio/commit/76544d7c)).
* **End-to-End & Unit Tests**: Implemented extensive end-to-end tests for user authentication and dashboard management, and comprehensive unit tests for various modules ([72550ffa](https://github.com/depictio/depictio/commit/72550ffa), [df44475b](https://github.com/depictio/depictio/commit/df44475b)).

### **🧱 Beanie Implementation**

* **User & Group Management**: Implemented FastAPI user and group management with Beanie ODM, including helpers for user and group creation ([6470af84](https://github.com/depictio/depictio/commit/6470af84)).
* **Testing & Model Integration**: Added Beanie setup for various tests and updated model references for consistent integration ([ec008e0f](https://github.com/depictio/depictio/commit/ec008e0f)).

### **♻️ Code Refactoring**

* **Code Organization & Clarity**: Performed refactoring of import statements, code organization, and whitespace across numerous files ([f8b0f913](https://github.com/depictio/depictio/commit/f8b0f913), [239ad86e](https://github.com/depictio/depictio/commit/239ad86e)).
* **API & Data Models**: Refactored API and data models to use depictio-models as a centralized library and updated dependencies to Pydantic v2 ([2170ae17](https://github.com/depictio/depictio/commit/2170ae17), [e8397589](https://github.com/depictio/depictio/commit/e8397589)).

### **🐛 Bug Fixes**

* **CI/CD & Deployment**: Corrected workflow triggers and addressed various Docker and Helm deployment issues, including volume paths and logging ([14539146](https://github.com/depictio/depictio/commit/14539146), [a376bf98](https://github.com/depictio/depictio/commit/a376bf98)).
* **Data & Configuration Paths**: Corrected various file paths, IDs, and configurations for consistency and relative access ([a835bb16](https://github.com/depictio/depictio/commit/a835bb16), [214659e3](https://github.com/depictio/depictio/commit/214659e3)).
* **User & Authentication**: Addressed issues with user fetching functions, replacing deprecated calls and ensuring proper asynchronous execution ([f334386c](https://github.com/depictio/depictio/commit/f334386c), [725c3d98](https://github.com/depictio/depictio/commit/725c3d98)).

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
