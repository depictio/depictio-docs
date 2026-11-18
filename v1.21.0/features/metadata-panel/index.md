# Metadata panel (v1.21.0+)

The **Metadata** panel opens the project's sample table beside the dashboard, where you add label columns such as `response` = *responder* / *non-responder*. Each label becomes a group that filters, colours and splits the linked charts. The table itself does not change unless you save to it.

[![](../../images/guides/metadata-panel/metadata-labels.webp)](../../images/guides/metadata-panel/metadata-labels.mp4)

## Eligible tables

No switch is needed: the **Metadata** button shows in the dock when the project has at least one eligible table. A table is eligible when:

- it is the source of at least one enabled [link](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md);
- it is not built by a join or a transform, and is not a join input;
- its metatype is `metadata`, or it has none;
- it has at most 10,000 rows.

## Open the panel

**Metadata** in the dock opens the panel on the right. It shares that edge with **Analysis**, so opening one closes the other. Its badge counts your label columns.

The header row shows the table (a picker when there are several) and the key column the labels are keyed on: the one the table links by. A table with several rows per key shows the first row per key.

## Label columns

The **+** column adds a label column: name it, then type labels in its cells. Paste works too: tab-separated values fill down from the focused cell.

**Import**, or a CSV or TSV dropped on the panel, labels from a file. Pick **As labels**, then a mode:

| Mode             | Effect                                                 |
| ---------------- | ------------------------------------------------------ |
| **Add columns**  | Each new column of the file becomes a label column     |
| **Fill missing** | Labels go into same-named columns where a row has none |
| **Replace**      | The file becomes the whole set                         |

The file is read in your browser and never sent to the server. Rows that match no key are reported and left out. Excel and Parquet files are not read.

## Compare in the charts

**Compare in the charts** in a label column's menu, or the chart icon in its header, turns each label value into a group in **Analysis**, which filters, colours and splits the linked charts. See [The Analysis panel](https://depictio.github.io/depictio-docs/latest/features/interactive-selection-filtering/#analysis-panel).

**Compare groups in cards**, under **In cards** in **Analysis**, adds each group's value to the cards. Closed, **Analysis** leaves the figures coloured and the cards comparing the groups.

Groups from labels carry a tag icon in **Analysis**: rename or delete them from Metadata, not there. **Analysis** is a temporary view: colours, groups and card comparisons are never saved with the dashboard.

## The column menu

| Item                                           | What it does                                                           |
| ---------------------------------------------- | ---------------------------------------------------------------------- |
| **Compare in the charts** / **Stop comparing** | Adds or removes the column's groups in **Analysis**                    |
| **Rename**, **Delete**                         | On the column                                                          |
| **Keep on my account**                         | Moves a column from the browser to your account                        |
| **Share on this dashboard**                    | Every reader sees the column, read-only, and can **Copy to my labels** |
| **Save to table**                              | Writes the column into the table, see [below](#save-to-table)          |

### Where labels live

A column's header icon says where it is kept:

| Where                   | When                                                                                                        |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| Browser                 | Anonymous and temporary accounts, and a column imported from a file until you choose **Keep on my account** |
| Account                 | Signed in                                                                                                   |
| Shared on the dashboard | After **Share on this dashboard**. Editors of the project and the dashboard's owner can share               |

The YAML (Lite) export of a dashboard does not carry shared labels.

### Save to table

**Save to table** writes the column into the table as a new table version, after a dry run you confirm. It needs:

- the owner or editor role;
- a table a user added, not a pipeline or URL table;
- the table unlocked on its page in the project: **Read-only** by default, **Editable** once switched.

Every save is a new version, listed under **Past versions**, and **Restore v<N>** writes a past version back as a new one. See [Edit a table](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#edit-a-table).

## Export as a metadata sheet

**Export** in the panel header (**Export as metadata sheet**) downloads the table's rows with the label columns you pick, as a TSV built in the browser. For a pipeline table, add those columns to the pipeline's sample sheet and ingest again.

## Limits

| Limit                                                   | Value                                                                   |
| ------------------------------------------------------- | ----------------------------------------------------------------------- |
| Groups in **Analysis**, lasso and table groups included | 24. A column with more labels cannot be compared, and its menu says why |
| Label columns                                           | 20                                                                      |
| Keys per column                                         | 10,000                                                                  |
| Characters per label                                    | 80                                                                      |
| Imported file                                           | 5 MB                                                                    |

On a past dashboard version (`?version=`), the grid reads that version's rows and writes are disabled.

## See also

- [Selection groups and the Analysis panel](https://depictio.github.io/depictio-docs/latest/features/interactive-selection-filtering/#analysis-panel)
- [Cross-DC filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md)
- [MultiQC: link to sample metadata](https://depictio.github.io/depictio-docs/latest/features/multiqc/#link-to-sample-metadata)
- [Dashboard and data versions](https://depictio.github.io/depictio-docs/latest/features/versioning/#data-versions)
- [Edit a table](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#edit-a-table)
