---
title: "Developer"
icon: material/code-tags
description: "Learn how to contribute to the Depictio project and become part of our community."
---

# Developer Documentation

This section provides information for developers who want to contribute to Depictio. Whether you're interested in fixing bugs, adding new features, or improving documentation, you'll find guidance to help you get started.

## Contributing to Depictio

Depictio is an open-source project that welcomes contributions from the community. There are many ways to contribute:

- **Code contributions**: Implement new features, develop new components, or fix bugs
- **Testing**: Help test features or report bugs
- **Design**: Contribute to the UI/UX design
- **Documentation**: Improve or expand the documentation
- **Community support**: Help answer questions and support other users

For detailed information on how to contribute, see the [Contributing Guide](contributing.md).

## In This Section

| Page | Description |
|------|-------------|
| [Modularity](modularity.md) | Code architecture, object model, and API structure |
| [Contributing Guide](contributing.md) | How to set up development environment and contribute |

## Getting Started

To begin contributing to Depictio, we recommend:

1. Familiarize yourself with the [project architecture](../features/architecture.md)
2. Understand the [code modularity](modularity.md) and object model
3. Read the [contributing guidelines](contributing.md)
4. Set up your development environment
5. Start with small, manageable contributions

## Quick Start

```bash
# Clone the repository
git clone https://github.com/depictio/depictio.git
cd depictio

# Install with pixi (recommended)
pixi install

# Or with uv
uv sync

# Run tests
pytest depictio/tests/ -xvs

# Start development server
pixi run api      # FastAPI backend
pixi run dash     # Dash frontend
```

See the [Contributing Guide](contributing.md) for detailed setup instructions.

We look forward to your contributions and are here to help you get started!
