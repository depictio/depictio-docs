# Contributing to Depictio

Thank you for your interest in contributing to Depictio! This guide outlines the process for contributing to the project and provides resources to help you get started.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing-local-changes)
- [Code Style and Standards](#code-style-and-standards)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Requests](#pull-requests)
- [Code Review Process](#code-review-process)
- [Community](#community)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11 or higher (3.12 recommended)
- Docker and Docker Compose
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/YOUR-USERNAME/depictio.git
   cd depictio
   ```

3. Add the original repository as an upstream remote:

   ```bash
   git remote add upstream https://github.com/depictio/depictio.git
   ```

## Development Environment

### Option 1: Docker Compose (Recommended)

The recommended way to develop Depictio is using Docker Compose, which provides a consistent environment with all services configured.

```bash
# Build and start all services
docker compose -f docker-compose.dev.yaml \
               -f docker-compose/docker-compose.minio.yaml \
               --env-file docker-compose/.env up \
               --build --detach
```

Access the services:

| Service | URL |
|---------|-----|
| Backend API | `http://localhost:8058` |
| Frontend | `http://localhost:5080` |
| API Docs | `http://localhost:8058/docs` |

The source code is mounted as a volume for live reloading:

```yaml
volumes:
   - ./depictio:/app/depictio
```

### Option 2: DevContainer & GitHub Codespaces

For a cloud-based or containerized IDE experience, use the provided DevContainer configuration:

**VS Code DevContainer:**

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the repository in VS Code
3. Click "Reopen in Container" when prompted (or use Command Palette: `Dev Containers: Reopen in Container`)

**GitHub Codespaces:**

1. Go to the [Depictio repository](https://github.com/depictio/depictio)
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

Both options provide a pre-configured development environment with all dependencies installed.

### Alternative: Local Python Setup

For contributors who prefer local development without containers:

=== "uv (Fast)"

    ```bash
    # Install uv: https://docs.astral.sh/uv/
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Sync dependencies
    uv sync --all-extras

    # Install Playwright browsers
    uv run playwright install chromium
    ```

=== "pixi (With infrastructure)"

    ```bash
    # Install pixi: https://pixi.sh
    curl -fsSL https://pixi.sh/install.sh | bash

    # Install all dependencies (includes MongoDB, Redis, MinIO)
    pixi install

    # Start infrastructure and services
    pixi run start-infra
    pixi run api      # FastAPI backend
    pixi run dash     # Dash frontend
    ```

=== "pip (Traditional)"

    ```bash
    python -m venv depictio-dev-venv
    source depictio-dev-venv/bin/activate
    pip install -e ".[dev]"
    playwright install chromium
    ```

### Setting up Pre-commit Hooks

```bash
pre-commit install
```

### Docker Images

The project provides multiple Dockerfile options:

| Dockerfile | Description |
|------------|-------------|
| `Dockerfile_depictio_uv.dockerfile` | **Recommended** - Fast builds using uv |
| `Dockerfile_depictio_prod.dockerfile` | Multi-stage production build |
| `Dockerfile_depictio.dockerfile` | Legacy conda/mamba-based |

### Environment Variables

Depictio uses environment variables for configuration. Copy `.env.example` to `.env` and customize as needed.

Key development variables:

| Variable | Description |
|----------|-------------|
| `DEPICTIO_CONTEXT` | Set to `server` for API, `dash` for frontend |
| `MONGO_WIPE` | Set to `true` to reset database on startup |
| `LOGGING_VERBOSITY_LEVEL` | Set to `DEBUG` for detailed logs |

### Local Python Environment (Required)

Regardless of which development option you choose, you need local Python packages for running tests, pre-commit hooks, and the CLI.

**1. Main package (tests & pre-commit)**

```bash
# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install depictio with all dev dependencies
uv sync --all-extras

# Set up pre-commit hooks
uv run pre-commit install
```

**2. CLI package (separate)**

The CLI is a standalone package with its own `pyproject.toml`:

```bash
# Install depictio-cli
cd depictio/cli
uv sync

# Verify installation
uv run depictio --help
```

**Available tools:**

| Tool | Command | Purpose |
|------|---------|---------|
| **pytest** | `uv run pytest depictio/tests/ -xvs` | Run tests |
| **pre-commit** | `uv run pre-commit run --all-files` | Code quality checks |
| **ruff** | `uv run ruff check .` | Linting |
| **ty** | `uv run ty check depictio/` | Type checking |
| **depictio CLI** | `cd depictio/cli && uv run depictio --help` | CLI commands |

## Project Structure

```
depictio/
├── api/                 # FastAPI backend (port 8058)
│   ├── endpoints/       # API routes
│   ├── v1/              # API version 1
│   └── main.py          # Application entry point
├── dash/                # Dash frontend (port 5080)
│   ├── modules/         # Dashboard components
│   └── layouts/         # Page layouts
├── models/              # Shared Pydantic models
├── cli/                 # Command-line interface
└── tests/               # Test suites
```

### Component Development

Depictio uses a modular component system in `depictio/dash/modules/`:

| Component | Purpose |
|-----------|---------|
| `card_component/` | Text and summary cards |
| `figure_component/` | Plotly visualizations |
| `interactive_component/` | Filters, dropdowns, sliders |
| `table_component/` | Data tables |
<!-- | `jbrowse_component/` | Genome browser | -->
| `multiqc_component/` | MultiQC reports |

Each component follows this structure:

```
component_name/
├── frontend.py      # Dash callbacks and UI
└── utils.py         # Component building logic
```

## Development Workflow

1. Create a new branch for your feature or bugfix:

    ```bash
    git checkout -b <issue-type>/<issue-number>-<short-description>
    # Example: feature/123-add-new-component
    # Example: bugfix/456-fix-data-processing
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Description of your changes"
    ```

3. Keep your branch updated with upstream:

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

4. Push your branch to GitHub:

    ```bash
    git push origin <issue-type>/<issue-number>-<short-description>
    ```

5. Create a pull request on GitHub.

## Testing Local Changes

### Running Tests

```bash
# Run all tests
pytest depictio/tests/ -xvs

# Run with parallel execution
pytest depictio/tests/ -xvs -n auto

# Run specific test file
pytest depictio/tests/api/test_endpoints.py -xvs
```

### Code Quality Checks

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
ty check depictio/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Writing Tests

- Place tests in the `depictio/tests/` directory
- Follow existing structure: `tests/api/`, `tests/dash/`, `tests/cli/`
- Include both unit tests and integration tests

## Code Style and Standards

Depictio follows these coding standards:

- **PEP 8** for Python code style
- **Type hints** for all function parameters and return values
- **Docstrings** for modules, classes, and functions

We use pre-commit hooks to enforce:

| Tool | Purpose |
|------|---------|
| [`ruff`](https://github.com/astral-sh/ruff) | Code formatting and linting |
| [`ty`](https://github.com/astral-sh/ty) | Static type checking |

## Documentation

### Repository

Documentation is maintained in the [depictio-docs](https://github.com/depictio/depictio-docs) repository.

### Setup

1. Fork and clone the `depictio-docs` repository
2. Install dependencies:

   ```bash
   cd depictio-docs
   pip install -r requirements.txt
   ```

### Writing Documentation

- Documentation is built using [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- Source files are in the `docs/` directory
- Write in Markdown format
- Include code examples where appropriate

### Building Documentation

Preview documentation locally:

```bash
cd depictio-docs
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.

## Issue Reporting

### Bug Reports

When reporting a bug, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment information (OS, browser, Python version)

### Feature Requests

When requesting a feature, please include:

- A clear, descriptive title
- Detailed description of the proposed feature
- Rationale for adding the feature
- Implementation suggestions if applicable

## Pull Requests

### PR Guidelines

- Keep PRs focused on a single feature or bugfix
- Include tests for new functionality
- Update documentation as needed
- Reference related issues
- Ensure all CI checks pass

### PR Template

Your PR description should include:

- What changes were made
- Why the changes were made
- How to test the changes
- Any additional context or notes

## Code Review Process

All submissions require review. The review process includes:

1. **Automated checks** - CI/CD pipeline runs tests and linting
2. **Code review** - Maintainers review the changes
3. **Feedback** - Address any requested changes
4. **Approval** - Final approval and merge

## Community

### Communication Channels

- [GitHub Issues](https://github.com/depictio/depictio/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/depictio/depictio/discussions) - Questions and ideas

## License

By contributing to Depictio, you agree that your contributions will be licensed under the [MIT License](https://github.com/depictio/depictio/blob/main/LICENSE).
