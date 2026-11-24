# Tutorials

Recorded talks and video walkthroughs. If you would rather read than watch, start with [Getting Started](https://depictio.github.io/depictio-docs/latest/usage/get_started/index.md).

______________________________________________________________________

## Talks & webinars

### Interactive multi-dataset dashboards with Depictio

🎬 **SciLifeLab Data Centre webinar, 2 June 2026**: building a multi-dataset dashboard and sharing it through a public URL.

A one-hour webinar in the SciLifeLab Data Centre's [Tools for AI/ML research in life sciences](https://www.scilifelab.se/data-ai/tools-event-series/) series, covering the full path from creating a project to sharing a dashboard publicly via [SciLifeLab Serve](https://serve.scilifelab.se/).

Recorded on v0.13.2

This was filmed shortly before the 1.0 release. The React viewer shown is the one still in use, but some URLs and menu labels moved in v1.0.0, so check the [changelog](https://depictio.github.io/depictio-docs/latest/changelog/index.md) if something doesn't match what you see.

______________________________________________________________________

## Step by step (v1.21.0+)

Short written tutorials, with screenshots and clips, for what v1.21.0 added:

| Tutorial                                                                                                                    | What you do                                                                               | Reference                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [What's new since your last visit](https://depictio.github.io/depictio-docs/latest/tutorials/whats-new/index.md)            | Turn it on, then read what changed on a dashboard: Overlay, Split, Before / Now, the bell | [*"What's new"*](https://depictio.github.io/depictio-docs/latest/features/whats-new/index.md)      |
| [Compare runs](https://depictio.github.io/depictio-docs/latest/tutorials/compare-runs/index.md)                             | Attach a second run and see what it produced, file by file and figure by figure           | [Runs](https://depictio.github.io/depictio-docs/latest/features/runs/index.md)                     |
| [Watch the data update](https://depictio.github.io/depictio-docs/latest/tutorials/data-updates/index.md)                    | Refresh only what changed, read the Activity tab, find the new rows                       | [Data refresh](https://depictio.github.io/depictio-docs/latest/features/runs/#data-refresh)        |
| [Label samples from the dashboard](https://depictio.github.io/depictio-docs/latest/tutorials/metadata-panel/index.md)       | Add labels to a samplesheet, use them as groups, save or export them                      | [Metadata panel](https://depictio.github.io/depictio-docs/latest/features/metadata-panel/index.md) |
| [Move a project to another instance](https://depictio.github.io/depictio-docs/latest/tutorials/instance-migration/index.md) | Receive a code on one instance, send the project from another                             | [Migrate](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/index.md)   |
| [MultiQC: compare reports across runs](https://depictio.github.io/depictio-docs/latest/features/multiqc/#compare-runs)      | Append runs to one MultiQC collection and split figures on the new samples                | [MultiQC](https://depictio.github.io/depictio-docs/latest/features/multiqc/index.md)               |

______________________________________________________________________

## Video walkthroughs

Shorter clips, embedded alongside the documentation they belong to:

| Watch                                                                                                              | Where               | What it covers                                             |
| ------------------------------------------------------------------------------------------------------------------ | ------------------- | ---------------------------------------------------------- |
| [Projects](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md)                          | Projects guide      | Starting a project from a source, and what a project holds |
| [Registering data with the CLI](https://depictio.github.io/depictio-docs/latest/usage/get_started/#video-tutorial) | Getting Started     | Running the CLI against a YAML project configuration       |
| [Building a dashboard](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md)   | Dashboard creation  | Adding components, wiring interactivity, saving            |
| [Using a dashboard](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_usage/index.md)         | Using the dashboard | Filters, selections and cross-collection filtering         |

______________________________________________________________________

## Try it yourself

- **[Live demo](https://showcases.depictio.embl.org/)** is a running instance with example projects. No account needed, and it resets periodically.
- **[Open in Codespaces](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/try/devcontainer.json&quickstart=1)** runs the Python package in a GitHub cloud workspace, nothing to install.
- **[Hands-on workshop](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/workshop/devcontainer.json&quickstart=1)** opens a Codespace with an nf-core/ampliseq run already ingested, ready to follow these tutorials.
- **[Getting Started](https://depictio.github.io/depictio-docs/latest/usage/get_started/index.md)** covers the same ground as the webinar, in written form, on your own machine.
