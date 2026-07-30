---
url: ""
breadcrumb: "Depictio > Getting help"
---

# Reporting a bug or requesting a feature

Bugs, unexpected behaviour and feature requests belong in the issue tracker at
github.com/depictio/depictio/issues. There is no support email and no forum.

A useful report includes the Depictio version, how it is deployed (Docker Compose,
Kubernetes, or a local development stack), what was expected, what happened instead, and
the relevant API or CLI logs. For ingestion problems, the project YAML and the
`depictio-cli` output are usually what is needed to reproduce it.

Issue titles follow a bracketed prefix convention — `[BUG]`, `[FEATURE]`, `[TASK]` — so
check the existing list before opening a new one.

# What the documentation does not cover

The documentation describes released behaviour. If something is not documented, it may be
unreleased, undocumented, or not a feature. The changelog records what shipped in each
version, and the roadmap records what is planned. Questions about internals beyond that
are best asked as a GitHub issue or discussion.
