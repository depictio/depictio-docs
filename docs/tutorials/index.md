---
title: "Tutorials"
icon: material/school-outline
description: "Recorded talks and video walkthroughs: watch Depictio being used end to end, from ingesting a dataset to sharing a dashboard by URL."
---

# :material-school-outline: Tutorials

Recorded talks and video walkthroughs. If you would rather read than watch, start with
[Getting Started](../usage/get_started.md).

---

## Talks & webinars

### Interactive multi-dataset dashboards with Depictio

<div class="video-embed">
  <iframe
    src="https://www.youtube-nocookie.com/embed/KWWHo4esUfg"
    title="Interactive multi dataset dashboards with Depictio: from creation to sharing through a public URL"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    allowfullscreen
  ></iframe>
</div>

<p class="video-caption">🎬 <strong>SciLifeLab Data Centre webinar, 2 June 2026</strong>: building a multi-dataset dashboard and sharing it through a public URL.</p>

A one-hour webinar in the SciLifeLab Data Centre's
[Tools for AI/ML research in life sciences](https://www.scilifelab.se/data-ai/tools-event-series/)
series, covering the full path from creating a project to sharing a dashboard publicly
via [SciLifeLab Serve](https://serve.scilifelab.se/).

!!! info "Recorded on v0.13.2"

    This was filmed shortly before the 1.0 release. The React viewer shown is the one
    still in use, but some URLs and menu labels moved in v1.0.0, so check the
    [changelog](../changelog/README.md) if something doesn't match what you see.

---

## Step by step <small>(v1.21.0+)</small> { #step-by-step }

Short written tutorials, with screenshots and clips, for what v1.21.0 added:

| Tutorial | What you do |
| --- | --- |
| [What's new since your last visit](whats-new.md) | Turn it on, then read what changed on a dashboard: Overlay, Split, Before / Now, the bell |
| [Compare runs](compare-runs.md) | Attach a second run and see what it produced, file by file and figure by figure |
| [Watch the data update](data-updates.md) | Refresh only what changed, read the Activity tab, find the new rows |
| [Label samples from the dashboard](metadata-panel.md) | Add labels to a samplesheet, use them as groups, save or export them |
| [Move a project to another instance](instance-migration.md) | Receive a code on one instance, send the project from another |
| [MultiQC: compare reports across runs](../features/multiqc.md#compare-runs) | Append runs to one MultiQC collection and split figures on the new samples |

---

## Video walkthroughs

Shorter clips, embedded alongside the documentation they belong to:

| Watch | Where | What it covers |
| --- | --- | --- |
| :material-play-circle: [Projects](../usage/projects/guide.md) | Projects guide | Starting a project from a source, and what a project holds |
| :material-play-circle: [Registering data with the CLI](../usage/get_started.md#video-tutorial) | Getting Started | Running the CLI against a YAML project configuration |
| :material-play-circle: [Building a dashboard](../usage/guides/dashboard_creation.md) | Dashboard creation | Adding components, wiring interactivity, saving |
| :material-play-circle: [Using a dashboard](../usage/guides/dashboard_usage.md) | Using the dashboard | Filters, selections and cross-collection filtering |

---

## Try it yourself

- **[Live demo](https://showcases.depictio.embl.org/)** is a running instance with example
  projects. No account needed, and it resets periodically.
- **[Open in Codespaces](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/try/devcontainer.json&quickstart=1)**
  runs the Python package in a GitHub cloud workspace, nothing to install.
- **[Hands-on workshop](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/workshop/devcontainer.json&quickstart=1)**
  opens a Codespace with an nf-core/ampliseq run already ingested, ready to follow these tutorials.
- **[Getting Started](../usage/get_started.md)** covers the same ground as the webinar, in
  written form, on your own machine.
