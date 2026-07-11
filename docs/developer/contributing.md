# Contributing to Depictio

Thanks for your interest in contributing! This guide gets you from a fresh clone
to an open pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Quick Start](#quick-start)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing & Code Quality](#testing--code-quality)
- [Frontend Guidelines](#frontend-guidelines)
- [Documentation](#documentation)
- [Issues & Pull Requests](#issues--pull-requests)
- [Areas Needing Help](#areas-needing-help)
- [Community](#community)
- [License](#license)

## Code of Conduct

Depictio adopts the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
In short: be respectful, assume good faith, keep feedback constructive and
focused on the work. Report unacceptable behaviour privately to the maintainers
(see [Community](#community)) — reports are handled confidentially.

## Quick Start

```bash
# 1. Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/depictio.git
cd depictio
git remote add upstream https://github.com/depictio/depictio.git

# 2. Run the full stack with hot-reload (MongoDB, Redis, MinIO, API, viewer)
docker compose -f docker-compose.dev.yaml up --build -d

# 3. Install local Python tooling for tests & pre-commit
uv sync --all-extras
uv run pre-commit install
```

Then open the app at **<http://localhost:5080>** and the API docs at
**<http://localhost:8058/docs>**.

> **Prerequisites:** Python 3.11+ (3.12 recommended), Docker + Docker Compose,
> Git, and [`uv`](https://docs.astral.sh/uv/). The React viewer dev server also
> needs [`pnpm`](https://pnpm.io/) 10+.

## Development Environment

### Recommended — Docker dev (hot-reload)

`docker-compose.dev.yaml` mounts your local source and reloads on change. All
critical defaults are baked into the compose file, so no `.env` is required.

```bash
docker compose -f docker-compose.dev.yaml up --build -d
```

| Service | URL |
|---------|-----|
| Frontend | `http://localhost:5080` |
| Backend API | `http://localhost:8058` |
| API Docs | `http://localhost:8058/docs` |
| MinIO Console | `http://localhost:9001` |

Useful environment overrides (set in `docker-compose/.env`, already populated for
local dev):

| Variable | Description |
|----------|-------------|
| `DEPICTIO_CONTEXT` | Runtime context — `server` for the API |
| `DEPICTIO_MONGODB_WIPE` | `true` resets the database on startup |
| `DEPICTIO_LOGGING_VERBOSITY_LEVEL` | `DEBUG` for detailed logs |
| `DEPICTIO_AUTH_SINGLE_USER_MODE` | `true` by default — disables the login prompt |

### Quickstart — pre-built images

To run released images from GHCR without building (MinIO bundled by default):

```bash
docker compose up -d
# Bring your own S3 / external MinIO:
docker compose -f docker-compose/docker-compose.no-minio.yaml up -d
```

### Local Python (tests, pre-commit, CLI)

You need a local Python environment for tests, pre-commit hooks, and the CLI —
even when running the app in Docker.

```bash
# Install uv: https://docs.astral.sh/uv/
curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync --all-extras                 # main package + all dev dependencies
uv run playwright install chromium   # E2E browser
uv run pre-commit install            # git hooks
```

The CLI is a standalone package with its own `pyproject.toml`:

```bash
cd depictio/cli && uv sync && uv run depictio --help
```

> Prefer a different tool? `pixi install` (bundles MongoDB/Redis/MinIO) or
> `pip install -e ".[dev]"` both work as alternatives to `uv`.

### React viewer dev server

For live frontend work, run Vite against the running backend:

```bash
pnpm -C depictio/viewer dev   # http://localhost:5173, hot-reload
```

### DevContainer / Codespaces

A pre-configured environment is available via the
[Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
("Reopen in Container") or **Codespaces** ("Code" → "Codespaces" → "Create
codespace on main") on the [repository](https://github.com/depictio/depictio).

## Project Structure

```
depictio/
├── api/                 # FastAPI backend (port 8058)
│   ├── main.py          # Application entry point
│   └── v1/
│       ├── configs/     # Settings models and logging config
│       ├── endpoints/   # One sub-package per resource domain
│       ├── services/    # Business logic, background tasks, lifespan
│       └── db.py        # MongoDB / Beanie setup
├── viewer/              # React + Vite SPA (dev port 5173) — sole frontend
├── models/              # Shared Pydantic models (API + CLI + viewer client)
├── cli/                 # Standalone CLI package (own pyproject.toml)
└── tests/               # Test suites (api/, cli/, models/, e2e)

packages/
└── depictio-react-core/ # Shared React renderers / types consumed by depictio/viewer
```

Each API resource domain lives in `depictio/api/v1/endpoints/<domain>_endpoints/`
with `routes.py` (FastAPI router), `models.py` (request/response models), and
`utils.py` (helpers). Dashboard renderers live in
`packages/depictio-react-core/src/renderers/` (`CardRenderer`, `FigureRenderer`,
`TableRenderer`, `InteractiveRenderer`, `AdvancedVizRenderer`, …); viewer-specific
wrappers (edit mode, drag handles, builder) live in `depictio/viewer/src/components/`.

## Development Workflow

1. Branch off `main`:

   ```bash
   git checkout -b <type>/<issue-number>-<short-description>
   # e.g. feature/123-add-new-component  •  bugfix/456-fix-data-processing
   ```

2. Commit using [Conventional Commits](https://www.conventionalcommits.org/) with
   a scope, matching the repo history:

   ```bash
   git commit -m "feat(viewer): add markdown renderer"
   # types: feat, fix, chore, refactor, docs  •  scopes: api, viewer, cli, helm, …
   ```

3. Keep up to date with upstream, then push and open a PR:

   ```bash
   git fetch upstream && git rebase upstream/main
   git push origin <type>/<issue-number>-<short-description>
   ```

## Testing & Code Quality

Run before pushing — these are the same checks CI enforces:

```bash
# Tests (-n auto for parallel)
uv run pytest depictio/tests/ -xvs -n auto

# Format, lint, type-check
uv run ruff format .
uv run ruff check .
uv run ty check depictio/

# Or run everything via the hooks
uv run pre-commit run --all-files
```

Place new tests under `depictio/tests/` following the existing layout
(`tests/api/`, `tests/cli/`, `tests/models/`), and include both unit and
integration coverage where relevant.

Coding standards: PEP 8, type hints on public functions, and docstrings for
modules/classes/functions. Formatting and linting are enforced by
[`ruff`](https://github.com/astral-sh/ruff); types by
[`ty`](https://github.com/astral-sh/ty).

## Frontend Guidelines

All frontend work targets the **React viewer** — the legacy Dash frontend was
removed in the v1.0 release.

The viewer lives in `depictio/viewer/` and `packages/depictio-react-core/`.
Stack: **Vite + React + Mantine 7 + `pnpm@10`**.

- **Use default Mantine theming** — avoid hardcoded color literals and custom CSS
  unless there's a strong reason; Mantine tokens handle light/dark automatically.
- **Run the dev server** with `pnpm -C depictio/viewer dev` (port `5173`) against
  the existing FastAPI backend.
- **Shared logic** belongs in `packages/depictio-react-core/`, not in the viewer.

The viewer serves three surfaces from a single SPA, with shared state in Zustand
stores under `depictio/viewer/src/stores/`:

| Surface | URL Pattern | Purpose |
|---------|-------------|---------|
| **Management** | `/dashboards`, `/projects` | Dashboard and project listing |
| **Viewer** | `/dashboard/{id}` | Read-only dashboard viewing |
| **Editor** | `/dashboard-edit/{id}` | Dashboard editing and save |

> Detailed architecture notes and design decisions are maintained in a private
> repository. If you need access for a significant contribution, reach out to the
> maintainers.

## Documentation

Docs live in the [depictio-docs](https://github.com/depictio/depictio-docs) repo
and are built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
To preview locally:

```bash
cd depictio-docs && pip install -r requirements.txt && mkdocs serve
# open http://127.0.0.1:8000
```

Building something specific?

- **A catalog tool** (turn a pipeline's outputs into dashboard renders) → [Contributing a Tool](contributing-a-tool.md)
- **A pipeline template** → [Contributing Templates](contributing-templates.md)

## Issues & Pull Requests

**Reporting issues** — for bugs, include a descriptive title, reproduction steps,
expected vs actual behaviour, screenshots if relevant, and your environment
(OS, browser, Python version). For features, describe the proposal and its
rationale.

**Pull requests** — keep each PR focused on a single feature or fix, add tests for
new behaviour, update docs as needed, reference related issues, and make sure CI
passes. In the description, cover **what** changed, **why**, and **how to test**.

All submissions are reviewed: automated CI runs tests and linting, a maintainer
reviews the change, you address feedback, and it's merged on approval.

## Areas Needing Help

We welcome contributions in these areas. See the [Roadmap](../roadmap/README.md)
for the current priorities and open issues.

| Area | What's Needed | Difficulty |
|------|---------------|------------|
| **Catalog tools** | Wire a bioinformatics tool's outputs to dashboard renders — see [Contributing a Tool](contributing-a-tool.md) | Easy → Medium |
| **Advanced-viz plots** | Biology-specific plots (volcano, embeddings, oncoplot, …) under `advanced_viz` | Medium |
| **Templates** | nf-core workflow dashboard templates — see [Contributing Templates](contributing-templates.md) | Medium |
| **Documentation** | Guides, tutorials, examples — start with [`good-first-issue`](https://github.com/depictio/depictio/labels/good%20first%20issue) | Easy |
| **Testing** | E2E coverage, edge cases, fixtures | Medium |

**Picking up an issue:** browse the
[`good-first-issue`](https://github.com/depictio/depictio/labels/good%20first%20issue)
label or an *Easy* row above, comment to claim it (or open one if it doesn't
exist), and ping [Discussions](https://github.com/depictio/depictio/discussions)
if there's no response within ~5 working days. We're a small team — don't be shy.

## Community

- [GitHub Issues](https://github.com/depictio/depictio/issues) — bugs and feature requests
- [GitHub Discussions](https://github.com/depictio/depictio/discussions) — questions, ideas, contribution check-ins

Maintainers respond best-effort within **5 working days**. If your PR has been
idle longer, bump it — it's not intentional.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](https://github.com/depictio/depictio/blob/main/LICENSE).
