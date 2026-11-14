---
title: "Compare runs"
description: "Attach a second run to a project, read what it produced in the Runs tab, and open a dashboard with what that run changed marked."
glightbox: true
---

# Compare runs <small>(v1.21.0+)</small>

A project made from a pipeline can hold several runs of it. The **Runs** tab says what each run produced and what each scan changed, and **Compare** opens a dashboard with what one run changed marked.

<figure markdown="span"><video autoplay controls muted loop playsinline poster="../images/guides/compare-runs/compare-runs.webp" src="../images/guides/compare-runs/compare-runs.mp4"></video></figure>

## Before you start

- Depictio **v1.21.0** or later.
- A project made from a pipeline run, with at least one dashboard.
- **Compare** and the dot on new runs need the changes feature: `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true`. See [What's new since your last visit](whats-new.md#before-you-start).
- Attaching a run needs the owner or editor role.

## 1. Attach a second run

On the project page, click **Add data** and pick the folder of another run of the same pipeline. Depictio recognises it as a run, and the button reads **Add run**.

If the run's MultiQC reports name samples the project already holds, the dialog lists them and holds the run back until you resolve them.

## 2. Open the Runs tab

The **Runs** tab lists one row per run. New runs carry a dot. Unfold a run to see its folder, its files and its scans.

[![The project's Runs tab, one row per run, new runs marked with a dot](../images/guides/compare-runs/runs_tab_light.webp#only-light)](../images/guides/compare-runs/runs_tab_light.webp){target=_blank}
[![The project's Runs tab, one row per run, new runs marked with a dot](../images/guides/compare-runs/runs_tab_dark.webp#only-dark)](../images/guides/compare-runs/runs_tab_dark.webp){target=_blank}

Each run has a **Produced** block: its ingestions, the Delta commits it wrote and its MultiQC reports. Each Delta commit has **View rows**, which opens that collection's Data table with the run's rows on top.

[![A run unfolded: its files, scans and the Produced block with its ingestion and MultiQC report](../images/guides/compare-runs/run_produced_light.webp#only-light)](../images/guides/compare-runs/run_produced_light.webp){target=_blank}
[![A run unfolded: its files, scans and the Produced block with its ingestion and MultiQC report](../images/guides/compare-runs/run_produced_dark.webp#only-dark)](../images/guides/compare-runs/run_produced_dark.webp){target=_blank}

## 3. Read what a scan changed

Pick a scan under **Scans**. Each file then says what that scan did to it:

- **New**: this scan brought the file.
- **Changed**: this scan found the file changed and read it again.
- **Failed**: this scan could not read the file.
- **Unchanged**: brought by an earlier scan, not changed since.

A changed file shows its size and date before and after. A MultiQC report also lists the samples and modules it gained or lost. Turn on **Only what this scan changed** to hide the rest.

[![A run unfolded with the Scans picker, a changed file and Only what this scan changed switched on](../images/guides/compare-runs/scans_picker_light.webp#only-light)](../images/guides/compare-runs/scans_picker_light.webp){target=_blank}
[![A run unfolded with the Scans picker, a changed file and Only what this scan changed switched on](../images/guides/compare-runs/scans_picker_dark.webp#only-dark)](../images/guides/compare-runs/scans_picker_dark.webp){target=_blank}

## 4. Compare a dashboard with the run

Click **Compare** on the run. With several dashboards, a menu lists them under **What this ingestion changed in**.

[![The Compare button open on a run, listing the dashboards under What this ingestion changed in](../images/guides/compare-runs/runs_compare_menu_light.webp#only-light)](../images/guides/compare-runs/runs_compare_menu_light.webp){target=_blank}
[![The Compare button open on a run, listing the dashboards under What this ingestion changed in](../images/guides/compare-runs/runs_compare_menu_dark.webp#only-dark)](../images/guides/compare-runs/runs_compare_menu_dark.webp){target=_blank}

The dashboard opens read-only, at `?before_run=<run id>`, with what that run changed marked. The header key reads **This ingestion**. Each changed tile's **Before | Now** draws the data just before the run beside the data now.

This view never moves your own "last visit" mark.

[![A dashboard opened at ?before_run, the tiles the run changed marked with a dot](../images/guides/compare-runs/dashboard_before_run_light.webp#only-light)](../images/guides/compare-runs/dashboard_before_run_light.webp){target=_blank}
[![A dashboard opened at ?before_run, the tiles the run changed marked with a dot](../images/guides/compare-runs/dashboard_before_run_dark.webp#only-dark)](../images/guides/compare-runs/dashboard_before_run_dark.webp){target=_blank}

## 5. See the layout before the run

**Layout before &lt;run&gt;** opens each dashboard's definition as it last was before the run. It shows the layout and components, not the data: an ingestion records no dashboard version, so the preview's data is whatever that version pinned.

## 6. Find the new rows in a table

From **View rows**, or from **Open in project** in the What's new panel, the collection's Data table opens read-only at `?table=<collection>&new_runs=<runs>`. The new rows come first and are marked. The rows you had seen follow, faded.

Click **Back to full table** to return to the plain table.

[![The Data table opened on the new run's rows, with Back to full table and Hide what you had seen](../images/guides/compare-runs/new_rows_table_light.webp#only-light)](../images/guides/compare-runs/new_rows_table_light.webp){target=_blank}
[![The Data table opened on the new run's rows, with Back to full table and Hide what you had seen](../images/guides/compare-runs/new_rows_table_dark.webp#only-dark)](../images/guides/compare-runs/new_rows_table_dark.webp){target=_blank}

## Good to know

- Every Delta row carries the run that wrote it, in `depictio_run_id`. That is how Depictio tells runs apart.
- A run ingested again in place changes rows under the same run tag. **Before | Now** shows it; Split does not.
- MultiQC rows have no run column: MultiQC figures compare on new samples instead. See [MultiQC: compare runs](../features/multiqc.md#compare-runs).
- Run times use the server's local clock.
- The Runs tab reads a run's files only once you unfold it.

## See also

- [What's new since your last visit](whats-new.md)
- [Watch the data update](data-updates.md)
- [MultiQC: compare runs](../features/multiqc.md#compare-runs)
- [Data from a run folder](../usage/projects/remote-data.md)
- [Dashboard and data versions](../features/versioning.md#data-versions)
