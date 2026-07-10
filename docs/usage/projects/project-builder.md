---
title: "Project Builder"
icon: material/folder-wrench
description: "Turn a folder into an Advanced depictio_project.yaml with the local Project Builder wizard — no server, no hand-written YAML."
---

# :material-folder-wrench: Project Builder

**Point Project Builder at a folder and get a validated Advanced
`depictio_project.yaml` back.** It opens a local visual wizard — browse your
files, define data collections from live-previewed scan patterns, organise them
into workflows, and export the config. No YAML to hand-write, and no server:
the builder runs entirely on your machine (no MongoDB, Redis, or S3).

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../../images/guides/project-builder/overview-appshell.png" target="_blank">
        <img src="../../../images/guides/project-builder/overview-appshell.png" width="800" style="max-width: 100%;">
    </a>
</div>

!!! info "When to use this"
    Project Builder authors the config for an **Advanced** project — a
    workflow-based project pointing at files on disk. For the concepts behind
    project types, see the [Projects guide](guide.md#advanced-projects); for
    every field the generated file can contain, see the
    [Full Reference](reference.md).

## Launch

```bash
depictio project-builder /path/to/your/data   # serves http://127.0.0.1:8129/
```

| Option | Description |
|--------|-------------|
| `--port <n>` | Serve on a different port (default `8129`). |
| `--host <addr>` | Bind to a different host. |
| `--no-open` | Don't open the browser automatically. |

Your progress is persisted in the browser (`localStorage`, keyed by the launch
folder), so you can close the tab and resume where you left off.

## How it works

<div class="module-flow" markdown>

<div class="module-flow__step module-flow__step--file" markdown>
:material-file-tree:{ .lg } **Source**

Browse the folder and click a file to preview its rows and inferred schema.
</div>

<div class="module-flow__step module-flow__step--module" markdown>
:material-database-outline:{ .lg } **Data Collections**

Turn scan patterns into data collections and organise them under workflows.
</div>

<div class="module-flow__step module-flow__step--component" markdown>
:material-file-check-outline:{ .lg } **Create**

Name the project, review the tree, and export `depictio_project.yaml`.
</div>

</div>

### Step 1 — Source

Browse your folder in the left file tree. Click any file to preview its first
rows and the **inferred column schema** — the same schema the scan will bind
data collections against.

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../../images/guides/project-builder/step1-source-filetree.png" target="_blank">
        <img src="../../../images/guides/project-builder/step1-source-filetree.png" width="800" style="max-width: 100%;">
    </a>
</div>

### Step 2 — Data Collections

For each output you want to expose, give it a **tag**, pick a **scan mode**, and
confirm the pattern against the **live matches** list — file tags in the tree
show which data collection owns each match.

=== "Glob"
    Match files by a glob pattern on the basename (e.g. `*.coverage.tsv`).

=== "Regex"
    Match with a regular expression when a glob isn't expressive enough —
    for sequencing-runs, each run's `runs_regex` subdirectory is scanned per run.

Depictio runs a **cross-file schema-consistency check** across the matches and
warns (without blocking) when columns or dtypes disagree between files.

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../../images/guides/project-builder/step2-data-collections.png" target="_blank">
        <img src="../../../images/guides/project-builder/step2-data-collections.png" width="800" style="max-width: 100%;">
    </a>
</div>

A project can hold **multiple workflows**, each with its own engine and
`data_location`. Add each data collection to the workflow it belongs to.

!!! warning "Names must be unique"
    Workflow names must be unique within the project, and data-collection tags
    must be unique project-wide. The builder enforces both before you can export.

!!! tip "Advanced scanning — `max_depth` and `ignore`"
    Under the advanced options you can cap how deep the scan descends
    (`max_depth`) and exclude paths (`ignore`). These are wired end-to-end into
    ingestion, so a preview here matches what `data scan` resolves later.

    <div style="border: 1px solid grey; width: 602px; max-width: 100%; padding: 1px;">
        <a href="../../../images/guides/project-builder/step2-advanced-scan.png" target="_blank">
            <img src="../../../images/guides/project-builder/step2-advanced-scan.png" width="600" style="max-width: 100%;">
        </a>
    </div>

### Step 3 — Create

Name the project and review the **workflows → data-collections tree**. The
builder generates the `depictio_project.yaml` with syntax highlighting, ready to
**copy** or **download**.

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../../images/guides/project-builder/step3-yaml-output.png" target="_blank">
        <img src="../../../images/guides/project-builder/step3-yaml-output.png" width="800" style="max-width: 100%;">
    </a>
</div>

## Repository metadata auto-fill

If your data comes from a pipeline repository, paste its URL and the builder does
a **best-effort** fetch to pre-fill project metadata — reading
`ro-crate-metadata.json`, `nextflow.config`, and the GitHub API to fill in the
project name, engine, version, catalog, description, author, license, and
homepage (and inlining the nf-core pipeline logo where available).

!!! info "Works offline too"
    Metadata fetch is entirely optional and **degrades gracefully** — if you're
    offline or the repository has no metadata, you just fill the fields in
    yourself and everything else works unchanged.

<div style="border: 1px solid grey; width: 802px; max-width: 100%; padding: 1px;">
    <a href="../../../images/guides/project-builder/metadata-autofill.png" target="_blank">
        <img src="../../../images/guides/project-builder/metadata-autofill.png" width="800" style="max-width: 100%;">
    </a>
</div>

## Editing after creation

Because your session is persisted in `localStorage`, you can reopen the builder
on the same folder to **edit existing data collections** or add new ones.
Re-creating overwrites the generated YAML.

## From YAML to a running project

The generated file is a standard Advanced project config — hand it to the CLI to
validate, sync, and ingest:

```bash
depictio-cli config validate-project-config --project-config-path ./depictio_project.yaml
depictio-cli run --project-config-path ./depictio_project.yaml
```

`run` walks the full pipeline (validate → sync → scan → process). See the
[CLI Usage](../../depictio-cli/usage.md) reference for every command and option.

!!! note "See also"
    - [Projects — Advanced](guide.md#advanced-projects) — the concepts behind the config
    - [YAML project configuration breakdown](yaml-examples.md) — annotated example
    - [Full Reference Configuration](reference.md) — every field
    - [CLI Usage](../../depictio-cli/usage.md) — validate, sync, scan, process
