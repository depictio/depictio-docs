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

- Python 3.11 or higher
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

### Setting up test environment

1. Create a virtual environment using Python's `venv` module or your preferred tool (e.g., `virtualenv`, `conda`, `uv`):

Example using `venv`:

   ```bash
   python -m venv depictio-dev-venv
   source depictio-dev-venv/bin/activate
   ```

Example using `uv`:

   ```bash
   uv venv depictio-dev-venv --python 3.12
   ```

2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Set up pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Running Depictio Locally using Docker Compose

To modify and test Depictio locally, you can use Docker Compose to set up the development environment. This will allow you to run both the backend and frontend services and modify the code as needed from the `depictio` directory (mounted as a volume in the Docker container).

```bash
volumes:
   - ./depictio:/app/depictio
```

1. To build the Docker images and start the services, run the following command from the root of the project:

```bash
docker compose -f docker-compose.dev.yaml \
               -f docker-compose/docker-compose.minio.yaml \
               --env-file docker-compose/.env up \
               --build --detach
```

2. Access the backend API at `http://localhost:8058` and the frontend at `http://localhost:5080`.

### Dependencies

Currently, Depictio is using a single container for both the backend and frontend services (`docker-images/Dockerfile_depictio.dockerfile`).
This is done to simplify the development process. The container is built using a micromamba environment that includes all necessary dependencies for both the backend and frontend (`conda_ens/depictio.yaml`). As the project grows, we may consider splitting the backend and frontend into separate containers for better scalability and maintainability. The current container build process also includes a [**Playwright**](https://playwright.dev/) installation to generate thumbnails to be served on the landing page of the dashboard. As [**Cypress**](https://www.cypress.io/)
is currently used for end-to-end testing, we might consider switching to it for thumbnail generation in the future.

### Environment Variables

Depictio uses environment variables for configuration. You can set these in a `.env` file in the root directory or pass them directly to Docker Compose. The `.env.example` file provides a template for the required variables.

Important variables during development include:

- `DEV_MODE`: Set to `true` to use development mode from FastAPI and Plotly Dash.
- `DEPICTIO_MONGODB_WIPE`: Set to `true` to wipe the MongoDB database on startup (useful for development).
- `DEPICTIO_LOGGING_VERBOSITY_LEVEL`: Set to `DEBUG` for detailed logging during development.

## Project Structure

The Depictio codebase is organized into several key directories:

- `depictio/api/` - Backend microservice (FastAPI, port 8058)
      - `endpoints/` - API endpoints for workflows, dashboards, data collections
      - `models/` - Database models and validation
- `depictio/dash/` - Frontend microservice (Dash, port 5080)
      - `modules/` - Dash Component (see below)
      - `layouts/` - Dashboard layouts and stepper UI
- `depictio/models/` - Shared Pydantic models
- `depictio/cli/` - Command-line interface for data management
- `depictio/tests/` - Unit, integration and E2E tests
- `helm-charts/` - Kubernetes deployment manifests

### Component Development (Key Feature)

Depictio uses a modular component system in `depictio/dash/modules/`:

- `card_component/` - Text and summary cards
- `figure_component/` - Plotly visualizations
- `interactive_component/` - Sliders, filters, dropdowns
- `table_component/` - Data tables
- `text_component/` - Text display components

Each component follows this structure:

```plaintext
component_name/
├── frontend.py      # Dash callbacks and UI
└── utils.py         # Component building logic
```

## Development Workflow

1. Create a new branch for your feature or bugfix:

    ```bash
    git checkout -b <issue-type>/<issue-number>-<short-description>
    # Example: git checkout -b feature/123-add-new-component / bugfix/456-fix-data-processing
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Description of your changes"
    ```

3. Keep your branch updated with the upstream:

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

4. Push your branch to GitHub:

    ```bash
    git push origin <issue-type>/<issue-number>-<short-description>
    ```

5. Create a pull request on GitHub.

## Testing local changes

### Running Tests

Run the test suite to ensure your changes don't break existing functionality:

```bash
pytest
```

### Writing Tests

- Place tests in the `depictio/tests/` directory
- Follow the existing test structure (e.g., `depictio/tests/api/`, `depictio/tests/dash/`, `depictio/tests/cli/`)

## Code Style and Standards

Depictio follows these coding standards:

- **PEP 8** for Python code style
- **Type hints** for all function parameters and return values
- **Docstrings** for all modules, classes, and functions

We use pre-commit hooks to enforce code style, which includes:

- [`ruff`](https://github.com/astral-sh/ruff) for code formatting and linting with isort for import sorting
- [`ty`](https://github.com/astral-sh/ty) for static type checking

## Documentation

### Repository

The documentation for Depictio is maintained in the `depictio-docs` repository at the following location: <https://github.com/depictio/depictio-docs>.

### Pre-requisites

- Apply the same procedure as for the main repository to fork the `depictio-docs` repository, clone it locally, and set up the development environment.
- Install the

### Writing Documentation

- Documentation is built using MkDocs
- Source files are in the `docs/` directory
- Write in Markdown format
- Include code examples where appropriate

### Building Documentation

To build and preview the documentation locally:

```bash
cd docs
mkdocs serve
```

## Issue Reporting

### Bug Reports

When reporting a bug, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment information

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
- Follow the commit message format

### PR Template

Your PR description should include:

- What changes were made
- Why the changes were made
- How to test the changes
- Any additional context or notes

## Code Review Process

All submissions require review. The review process typically includes:

1. Automated checks (CI/CD pipeline)
2. Code review by maintainers
3. Addressing feedback
4. Final approval and merge

## Community

### Communication Channels

- GitHub Issues for bug reports and feature requests
- Discussions for general questions and ideas

## License

By contributing to Depictio, you agree that your contributions will be licensed under the [project's license](https://github.com/depictio/depictio/blob/main/LICENSE).
