---
title: "Label samples from the dashboard"
description: "Add label columns to a samplesheet from the dashboard's Metadata panel, compare the charts by them, then keep, share, save or export them."
glightbox: true
---

# Label samples from the dashboard <small>(v1.21.0+)</small>

The **Metadata** panel opens the project's sample table beside the dashboard, where you add label columns such as `response` = *responder* / *non-responder*. Each label becomes a group that filters, colours and splits the linked charts, and the real table does not change.

<!-- video: metadata-panel/metadata-labels | open Metadata, add a label column, fill a few cells, Compare in the charts, the charts colour and split by label -->

## Before you start

- Depictio **v1.21.0** or later. No switch is needed.
- The project needs an eligible table, and the **Metadata** button shows only then. A table is eligible when:
    - it is the source of at least one enabled [link](../features/cross-dc-filtering.md);
    - it is not built by a join or a transform, and is not a join input;
    - its metatype is `metadata`, or it has none;
    - it has at most 10,000 rows.

## 1. Open the Metadata panel

Click **Metadata** in the dock. The panel opens on the right; it and **Analysis** share that edge, so opening one closes the other. Its badge counts your label columns.

<!-- shot: metadata-panel/dock-button | the dock with the Metadata button and its label-count badge -->

The header row shows the table (a picker when there are several) and the key column the labels are keyed on, the one the table links by.

<!-- shot: metadata-panel/panel | the Metadata drawer: table picker, key column, + column, label columns, Import and Export icons -->

## 2. Add a label column

Click the **+** column, name it, then type labels in its cells. Paste works too: tab-separated values fill down from the focused cell.

To label from a file, click **Import** or drop a CSV or TSV on the panel. Pick **As labels**, then a mode:

- **Add columns**: each new column of the file becomes a label column.
- **Fill missing**: labels go into same-named columns where a row has none.
- **Replace**: the file becomes the whole set.

The file is read in your browser and never sent to the server. Rows that match no key are reported and left out.

## 3. Compare the charts by a label

Open the label column's menu and click **Compare in the charts**, or click the chart icon in its header. Each label value becomes a group in **Analysis**, which filters, colours and splits the linked charts.

<!-- shot: metadata-panel/groups | the Analysis panel with groups derived from labels (tag icon), charts coloured by them -->

Groups from labels carry a tag icon in **Analysis**. Rename or delete them from Metadata, not there.

## 4. Keep, share or write the labels

The column menu holds every action on a label column.

<!-- shot: metadata-panel/column-menu | a label column's menu: Compare in the charts, Rename, Keep on my account, Share on this dashboard, Save to table, Delete -->

- **Rename** and **Delete**.
- **Keep on my account**: a column from a file stays in the browser until you choose this.
- **Share on this dashboard**: every reader sees the column, read-only, and can **Copy to my labels**. Editors of the project and the dashboard's owner can share.
- **Save to table**: writes the column into the table, as a new table version, after a dry run you confirm.

**Export** in the panel header downloads the table's rows with the label columns you pick, as a TSV built in the browser (**Export as metadata sheet**). For a pipeline table, add those columns to the pipeline's sample sheet and ingest again.

## 5. Unlock the table for real edits

**Save to table** and cell edits need an owner or editor, and a table a user added, not a pipeline or URL table. The table must also be unlocked on its page in the project.

That page shows **Read-only** or **Editable** above the table, with a switch to unlock cell edits. Every save is a new version, and **Restore v&lt;N&gt;** writes a past version back as a new one.

<!-- shot: metadata-panel/edit-lock | the table's page in the project, Read-only with the unlock switch, then Editable -->

## Good to know

- Where labels live: in the browser for anonymous and temporary accounts, on your account once you sign in, or on the dashboard when shared. A column's header icon says which.
- **Analysis** is a temporary view: colours, groups and card comparisons are never saved with the dashboard.
- At most 24 groups in all, lasso and table groups included. A column with more labels cannot be compared, and its menu says why.
- Caps: 20 label columns, 10,000 keys per column, 80 characters per label, 5 MB per imported file.
- Excel and Parquet files are not read in the browser.
- On a past version (`?version=`), the grid reads that version's rows, and writes are disabled.
- A table with several rows per key shows the first row per key.
- The YAML (Lite) export does not carry shared labels.

## See also

- [Selection groups and the Analysis panel](../features/interactive-selection-filtering.md#analysis-panel)
- [Cross-DC filtering](../features/cross-dc-filtering.md)
- [Dashboard and data versions](../features/versioning.md#data-versions)
- [Edit a table](../usage/projects/guide.md#edit-a-table)
