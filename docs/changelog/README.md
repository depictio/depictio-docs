---
title: "Changelog"
icon: material/update
description: "Track changes and updates to Depictio across different versions."
hide:
  - navigation
---

# Changelog

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
