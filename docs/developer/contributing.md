# Contributing to Depictio

Thank you for your interest in contributing to Depictio! This guide outlines the process for contributing to the project and provides resources to help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Style and Standards](#code-style-and-standards)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Pull Requests](#pull-requests)
- [Code Review Process](#code-review-process)
- [Community](#community)
- [License](#license)

## Code of Conduct

All contributors are expected to adhere to our Code of Conduct. Please read it before participating.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
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

### Setting Up

1. Create a virtual environment:

   ```bash
   python -m venv depictio-dev-venv
   source depictio-dev-venv/bin/activate  # On Windows: depictio-dev-venv\Scripts\activate
   ```

2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Set up pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Running Locally

1. Start the development environment:

   ```bash
   docker-compose up -d
   ```

2. Run the backend:

   ```bash
   python -m depictio.api
   ```

3. Run the frontend:

   ```bash
   python -m depictio.dash
   ```

## Project Structure

The Depictio codebase is organized into several key directories:

- `depictio/api/` - Backend microservice built with FastAPI
- `depictio/dash/` - Frontend microservice built with Plotly Dash
- `depictio/models/` - Common Pydantic models shared between server and CLI
- `depictio/cli/` - Command-line interface
- `depictio/tests/` - Test suite

## Development Workflow

1. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
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
   git push origin feature/your-feature-name
   ```

5. Create a pull request on GitHub.

## Testing

### Running Tests

Run the test suite to ensure your changes don't break existing functionality:

```bash
pytest
```

### Writing Tests

- Place tests in the `depictio/tests/` directory
- Follow the existing test structure
- Aim for high test coverage for new features

## Code Style and Standards

Depictio follows these coding standards:

- **PEP 8** for Python code style
- **Type hints** for all function parameters and return values
- **Docstrings** for all modules, classes, and functions

We use pre-commit hooks to enforce code style, which includes:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

## Documentation

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
- Potential implementation approach if you have one

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
- [Community Chat] for real-time communication

### Meetings

- Community meetings are held [schedule]
- Meeting notes are posted [location]

## License

By contributing to Depictio, you agree that your contributions will be licensed under the project's license.
