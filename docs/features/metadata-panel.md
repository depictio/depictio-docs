---
title: "Metadata panel"
icon: material/tag-multiple-outline
description: "Sample labels from the dashboard: the Metadata panel, label columns, Compare in the charts, where labels live, sharing, Save to table and export as a metadata sheet."
glightbox: true
---

# :material-tag-multiple-outline: Metadata panel <small>(v1.21.0+)</small>

The **Metadata** panel opens the project's sample table beside the dashboard, where you add label columns such as `response` = *responder* / *non-responder*. Each label becomes a group that filters, colours and splits the linked charts. The table itself does not change unless you save to it.

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../images/guides/metadata-panel/metadata-labels.webp" src="../../images/guides/metadata-panel/metadata-labels.mp4"></video></figure>

## Eligible tables

No switch is needed: the **Metadata** button shows in the dock when the project has at least one eligible table. A table is eligible when:

- it is the source of at least one enabled [link](cross-dc-filtering.md);
- it is not built by a join or a transform, and is not a join input;
- its metatype is `metadata`, or it has none;
- it has at most 10,000 rows.

## Open the panel

**Metadata** in the dock opens the panel on the right. It shares that edge with **Analysis**, so opening one closes the other. Its badge counts your label columns.

[![The dock with the Metadata button](../images/guides/metadata-panel/metadata_dock_button_light.webp#only-light){ width="326" }](../images/guides/metadata-panel/metadata_dock_button_light.webp){target=_blank}
[![The dock with the Metadata button](../images/guides/metadata-panel/metadata_dock_button_dark.webp#only-dark){ width="326" }](../images/guides/metadata-panel/metadata_dock_button_dark.webp){target=_blank}

The header row shows the table (a picker when there are several) and the key column the labels are keyed on: the one the table links by. A table with several rows per key shows the first row per key.

The dashboard's [Guide](../usage/guides/dashboard-guide.md) has a **Label your samples** part <small>(v1.22.0+)</small>: a live demo on the dashboard's own table, where labels typed are not saved, and a button that opens this panel.

[![The Metadata drawer: table, key column, + column, label column and the File import and export icons](../images/guides/metadata-panel/metadata_panel_labels_light.webp#only-light){ width="540" }](../images/guides/metadata-panel/metadata_panel_labels_light.webp){target=_blank}
[![The Metadata drawer: table, key column, + column, label column and the File import and export icons](../images/guides/metadata-panel/metadata_panel_labels_dark.webp#only-dark){ width="540" }](../images/guides/metadata-panel/metadata_panel_labels_dark.webp){target=_blank}

## Label columns

The **+** column adds a label column: name it, then type labels in its cells. Paste works too: tab-separated values fill down from the focused cell.

**Import**, or a CSV or TSV dropped on the panel, labels from a file. Pick **As labels**, then a mode:

| Mode | Effect |
|------|--------|
| **Add columns** | Each new column of the file becomes a label column |
| **Fill missing** | Labels go into same-named columns where a row has none |
| **Replace** | The file becomes the whole set |

The file is read in your browser and never sent to the server. Rows that match no key are reported and left out. Excel and Parquet files are not read.

## Compare in the charts

**Compare in the charts** in a label column's menu, or the chart icon in its header, turns each label value into a group in **Analysis**, which filters, colours and splits the linked charts. See [The Analysis panel](interactive-selection-filtering.md#analysis-panel).

[![The Analysis panel with groups derived from labels, charts coloured by My groups](../images/guides/metadata-panel/metadata_groups_analysis_light.webp#only-light)](../images/guides/metadata-panel/metadata_groups_analysis_light.webp){target=_blank}
[![The Analysis panel with groups derived from labels, charts coloured by My groups](../images/guides/metadata-panel/metadata_groups_analysis_dark.webp#only-dark)](../images/guides/metadata-panel/metadata_groups_analysis_dark.webp){target=_blank}

**Compare groups in cards**, under **In cards** in **Analysis**, adds each group's value to the cards. Closed, **Analysis** leaves the figures coloured and the cards comparing the groups.

[![The Alpha Diversity cards with each review group's value, and the rarefaction curves coloured by fail, pass and recheck](../images/guides/metadata-panel/labels_on_dashboard_light.webp#only-light){ width="644" }](../images/guides/metadata-panel/labels_on_dashboard_light.webp){target=_blank}
[![The Alpha Diversity cards with each review group's value, and the rarefaction curves coloured by fail, pass and recheck](../images/guides/metadata-panel/labels_on_dashboard_dark.webp#only-dark){ width="644" }](../images/guides/metadata-panel/labels_on_dashboard_dark.webp){target=_blank}

Groups from labels carry a tag icon in **Analysis**: rename or delete them from Metadata, not there. **Analysis** is a temporary view: colours, groups and card comparisons are never saved with the dashboard.

## The column menu

[![A label column's menu: Stop comparing, Rename, Share on this dashboard, Save to table, Delete](../images/guides/metadata-panel/metadata_column_menu_light.webp#only-light){ width="540" }](../images/guides/metadata-panel/metadata_column_menu_light.webp){target=_blank}
[![A label column's menu: Stop comparing, Rename, Share on this dashboard, Save to table, Delete](../images/guides/metadata-panel/metadata_column_menu_dark.webp#only-dark){ width="540" }](../images/guides/metadata-panel/metadata_column_menu_dark.webp){target=_blank}

| Item | What it does |
|------|--------------|
| **Compare in the charts** / **Stop comparing** | Adds or removes the column's groups in **Analysis** |
| **Rename**, **Delete** | On the column |
| **Keep on my account** | Moves a column from the browser to your account |
| **Share on this dashboard** | Every reader sees the column, read-only, and can **Copy to my labels** |
| **Save to table** | Writes the column into the table, see [below](#save-to-table) |

### Where labels live

A column's header icon says where it is kept:

| Where | When |
|-------|------|
| Browser | Anonymous and temporary accounts, and a column imported from a file until you choose **Keep on my account** |
| Account | Signed in |
| Shared on the dashboard | After **Share on this dashboard**. Editors of the project and the dashboard's owner can share |

The YAML (Lite) export of a dashboard does not carry shared labels.

### Save to table { #save-to-table }

**Save to table** writes the column into the table as a new table version, after a dry run you confirm. It needs:

- the owner or editor role;
- a table a user added, not a pipeline or URL table;
- the table unlocked on its page in the project: **Read-only** by default, **Editable** once switched.

[![The table's page in the project, Read-only with the unlock switch](../images/guides/metadata-panel/table_locked_light.webp#only-light)](../images/guides/metadata-panel/table_locked_light.webp){target=_blank}
[![The table's page in the project, Read-only with the unlock switch](../images/guides/metadata-panel/table_locked_dark.webp#only-dark)](../images/guides/metadata-panel/table_locked_dark.webp){target=_blank}

Every save is a new version, listed under **Past versions**, and **Restore v&lt;N&gt;** writes a past version back as a new one. See [Edit a table](../usage/projects/guide.md#edit-a-table).

## Export as a metadata sheet

**Export** in the panel header (**Export as metadata sheet**) downloads the table's rows with the label columns you pick, as a TSV built in the browser. For a pipeline table, add those columns to the pipeline's sample sheet and ingest again.

## Limits

| Limit | Value |
|-------|-------|
| Groups in **Analysis**, lasso and table groups included | 24. A column with more labels cannot be compared, and its menu says why |
| Label columns | 20 |
| Keys per column | 10,000 |
| Characters per label | 80 |
| Imported file | 5 MB |

On a past dashboard version (`?version=`), the grid reads that version's rows and writes are disabled.

## See also

- [Selection groups and the Analysis panel](interactive-selection-filtering.md#analysis-panel)
- [Cross-DC filtering](cross-dc-filtering.md)
- [MultiQC: link to sample metadata](multiqc.md#link-to-sample-metadata)
- [Dashboard and data versions](versioning.md#data-versions)
- [Edit a table](../usage/projects/guide.md#edit-a-table)
