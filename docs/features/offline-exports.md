---
title: "Offline exports"
icon: material/export-variant
description: "Serverless exports: a dashboard as one self-contained HTML file that opens with no server, a Quarto report, or both in one file."
---

# :material-export-variant: Offline exports <small>(v1.23.0+)</small>

A dashboard can leave Depictio as a file. The **serverless** export is one self-contained
HTML file holding the dashboard and its data: it opens by double-clicking, from a USB stick
or a `file://` URL, with no server and no network, and its filters still work. It suits
supplementary material for a paper, a collaborator with no account, an archive snapshot or a
demo that cannot break. A **report** writes the same dashboard up as a document (Quarto,
HTML, PDF), and **Report + dashboard** puts both in one file.

!!! info "Off by default"
    The exports are off while they are finalised: the API answers `404` and the viewer
    hides them. Set these on the API and the worker, then restart both:

    ```bash
    DEPICTIO_STATIC_EXPORT_ENABLED=true      # the dashboard as one HTML file
    DEPICTIO_NOTEBOOK_EXPORT_ENABLED=true    # the Quarto document and the rendered report
    DEPICTIO_REPORT_EDITOR_ENABLED=true      # optional: the report editor (v1.24.0+)
    ```

    With Helm they go in `backend.env`; `depictio local up` passes them on from your shell.

## Export a dashboard

1. Open the dashboard and its **Settings** (the gear), then **Export**.
2. Pick a format card. **Report + dashboard** is the one to send.
3. Read the summary (which tiles stay interactive, the estimated size), then export.
4. Download the file when the job is done.

The file opens on the filters you had when you clicked (v1.24.0+), and a reader can change
them from there. Nothing in it can be saved back: it is a copy to send, not a workspace.

## What you get

| Card | File | Who may export |
|------|------|----------------|
| **Report (HTML / PDF)** | The dashboard as a document: cover, text around the figures, an optional PDF in colour or mono | A signed-in reader |
| **Report + dashboard** | One HTML file: the rendered report, and the whole interactive dashboard one click away | A project owner |
| **Dashboard only (serverless)** | The interactive dashboard alone, every tab of it | A project owner |
| **Quarto notebook (.qmd)** | The report's source, to render and keep working in yourself | Any reader |

**Report + dashboard** and **Dashboard only** need both switches. A non-owner sees those cards
disabled, with the reason. While you preview a past version, the dashboard export is
disabled: it draws today's data.

Each tile of a serverless file is one of:

- **Live**: filters recompute it in the browser from the data in the file. Cards, filters,
  text, tables, MultiQC, most figures and the data-driven advanced visualizations.
- **Frozen**: shown as it was at the exported filters, with a badge saying so. Clustered
  heatmaps, phylogenetic trees, non-OLS trendlines, whole-table plots, maps.
- **Omitted**: left out, with the reason. Image galleries and the genome browser, which
  read from a server.

The export window lists every tile with its verdict before anything is built.

<span class="ver-badge">v1.23.0+</span> The export window offers an optional **Python runtime**
(Pyodide, under **Advanced options**) that keeps more analysis tiles live (code figures,
group comparisons, PCA / PCoA / t-SNE), for about +50 MB and ~8 s more to open.

## Reports <span class="ver-badge">v1.23.0+</span> { #reports }

The report is rendered on the worker with Quarto, so the worker image needs it (the default
image ships it). In a report, every Depictio tile is drawn by the same engine as the
serverless file, with the dashboard's filter panel and a **Back to the exported state**
button. Wide tables and figures get landscape pages in the PDF (v1.24.0+).

A report with code-mode figures renders for any signed-in reader when every owner of the
dashboard is a project owner or editor. A viewer's own copy renders for owners and editors
only, and the export window says so.

### Report editor <span class="ver-badge">v1.24.0+</span> { #report-editor }

With `DEPICTIO_REPORT_EDITOR_ENABLED`, project owners and editors get **Customise report…**
on the report card. It opens a side-by-side page (`/dashboard-report/<id>`):

- **Left**: the report's structure. Write the cover, intro and conclusion; tick, drag,
  section and caption the tiles; send a tab to the appendix; set page breaks and orientation.
- **Right**: the rendered report, updated as you type. **Exact PDF** renders it in full.

The report layout is versioned with the dashboard, so a restore brings it back.

## Visitors of a public project <span class="ver-badge">v1.24.1+</span> { #public-visitors }

With `DEPICTIO_STATIC_EXPORT_PUBLIC_DOWNLOAD_ENABLED=true` as well, a public project's visitors
get its dashboards as files from the same **Settings › Export**. Each format opens on a
**Ready copy | My view** control:

- **Ready copy**: built by the server at the dashboard's default view (dashboard only,
  report + dashboard and its PDF), with its size and build date. Downloading it starts no
  job. Anonymous visitors get these only.
- **My view**: a signed-in visitor (a guest account too) builds a file at their own filters.

<span class="ver-badge">v1.24.2+</span> The Export section opens on the ready copy: the report +
dashboard file, its PDF and the dashboard alone as plain download links, with *Your own view*
folded below. While the report is still being prepared the card says so and checks again every
30 s. Owners see the same card, so they see what visitors get.

The owner controls it in **Project › Permissions › Offline copy for visitors**. It is on
for every public project unless the owner turns it off
(`DEPICTIO_STATIC_EXPORT_PUBLIC_DOWNLOAD_DEFAULT=false` makes each owner turn it on instead).
**What visitors can download** lists, per dashboard, the collections the file carries with
their columns and rows. A copy is rebuilt a couple of minutes after a save or an ingestion.
What a public file leaves out is under
[Security › Offline copies for visitors](security.md#public-offline-download).

## Limits

- **What a file carries**: the collections its tiles read, pruned to the columns they use,
  and the dashboard's whole tab family. Once downloaded, no access control follows it.
- **Size**: about 8 MB for the runtime in every file, then roughly 2 bytes per data cell.
  Past 25 MB the export warns (mail and load time suffer); past 100 MB it is refused.
- **Expiry**: a built file is kept 7 days for download, a rendered report 72 hours.
- **Rate limits**: 5 builds per user per 10 minutes and 20 waiting on the instance; 2 report
  renders at once and 20 an hour per user. Visitors are also counted per address: 10
  downloads a minute, 10 own-view exports per 10 minutes, 6 renders an hour.
- **Notebook data**: a `.qmd` reads its tables from the API, up to 1 million rows each.

??? note "Settings"
    The main switches. Every variable, with the timeouts and render limits, is in the
    [environment reference](../installation/env-reference.md#offline-exports).

    | Variable | Default | Effect |
    |----------|---------|--------|
    | `DEPICTIO_STATIC_EXPORT_ENABLED` | `false` | The serverless file, and the runtime a report embeds |
    | `DEPICTIO_NOTEBOOK_EXPORT_ENABLED` | `false` | The Quarto document and the rendered report |
    | `DEPICTIO_NOTEBOOK_EXPORT_RENDER_ENABLED` | `true` | Render reports on the worker. Turn off for a worker built without Quarto |
    | `DEPICTIO_REPORT_EDITOR_ENABLED` | `false` | The report editor. Needs the notebook export |
    | `DEPICTIO_STATIC_EXPORT_PUBLIC_DOWNLOAD_ENABLED` | `false` | Files for visitors of public projects. Needs the static export |
    | `DEPICTIO_STATIC_EXPORT_PUBLIC_DOWNLOAD_DEFAULT` | `true` | A public project offers them until its owner decides |
    | `DEPICTIO_PERFORMANCE_STATIC_BUNDLE_WARN_MB` | `25` | Size above which the export warns |
    | `DEPICTIO_PERFORMANCE_STATIC_BUNDLE_MAX_MB` | `100` | Size above which it is refused |
    | `DEPICTIO_PERFORMANCE_STATIC_EXPORT_RETENTION_DAYS` | `7` | Days a built file is kept. `0` keeps it |

## From the command line

`depictio dashboard export-static` builds the same file on the instance host, with
`--check` to print the tile verdicts first, and `depictio dashboard combine-report` turns a
rendered report into a report + dashboard file. Neither reads the server switches. See the
[CLI reference](../depictio-cli/usage.md#dashboard-export-static).

## Further reading

The design documents, at v1.24.1:
[serverless deployment](https://github.com/depictio/depictio/blob/v1.24.1/docs/design/rfc-serverless-deployment.md),
[engine spike](https://github.com/depictio/depictio/blob/v1.24.1/docs/design/serverless-engine-spike.md),
[notebook export](https://github.com/depictio/depictio/blob/v1.24.1/docs/design/rfc-notebook-export.md).
