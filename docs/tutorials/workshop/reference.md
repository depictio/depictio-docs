---
title: "Reference"
description: "The words used in the Depictio workshop, in one table."
glightbox: true
---

# Reference

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-book-alphabet: **For learners**</span>
</div>

Each concept keeps one colour in every figure of the lesson and of the docs:

![Depictio's concepts in the app's colours and icons: project and data collection teal, dashboard orange, run and version yellow, link grey, you blue](../../images/data-model/concepts_light.png#only-light){ .ws-diagram }
![Depictio's concepts in the app's colours and icons: project and data collection teal, dashboard orange, run and version yellow, link grey, you blue](../../images/data-model/concepts_dark.png#only-dark){ .ws-diagram }

| Word | Meaning | Episode |
|---|---|---|
| :material-jira:{ .ws-ic .ws-ic-project } **Project** | Where the data and its dashboards live, with who can open them. Built from one or more pipeline runs, or from files you add | 0, 3, 4 |
| :material-table:{ .ws-ic .ws-ic-dc } **Data collection** | One kind of data in a project, read from one file or several. Its type says what it holds: table, MultiQC report, images, phylogenetic tree, genome tracks, GeoJSON… | 0, 3, 4 |
| :material-link-variant:{ .ws-ic .ws-ic-link } **Link** (Cross-DC link) | Says which identifiers match between two data collections, so that a filter on the source narrows the target. It goes one way. The column names may differ, and a MultiQC report is matched on its sample names. Nothing is copied or merged | 0, 3 |
| :material-set-center:{ .ws-ic .ws-ic-dc } **Join** | Two table data collections merged, on shared columns, into a new one, `joined_<name>`. The two stay as they are, and the joined table is rebuilt whenever one of them changes. Made in the browser with **Add join**, or written in `project.yaml` (`joins:`) for the command-line client | 3, 5 |
| :material-table-column-plus-after:{ .ws-ic .ws-ic-other } **Add columns** | Copies columns from a file onto an existing table data collection, in place, matched on a column, as a new version of that table. No new table. For owners and editors, on uploaded tables | 3 |
| :material-view-dashboard:{ .ws-ic .ws-ic-dash } **Dashboard** | A set of components, in tabs, that read the data collections of one project | 1, 2 |
| :material-chart-scatter-plot:{ .ws-ic .ws-ic-other } **Component** | One tile of a dashboard, reading one data collection: figure, table, card, filter, map, text, ![MultiQC](../../images/tutorials/workshop/multiqc-icon.svg){ .ws-logo .ws-logo-mono .off-glb } MultiQC plot | 2, 3 |
| :material-folder-play-outline:{ .ws-ic .ws-ic-run } **Run** | One batch of results added to a project: one execution of a pipeline, one upload, one field season. A project can hold several | 3, 4, 5 |
| :material-database-plus-outline:{ .ws-ic .ws-ic-other } **Append** | New rows added to a table with **Manage data**. A new version of the table, not a new run; the joins that read it are rebuilt | 5 |
| :material-folder-search-outline:{ .ws-ic .ws-ic-other } **Read in place** | Depictio reads the files where they are (S3, a shared folder); nothing is copied | 4 |
| :material-upload:{ .ws-ic .ws-ic-other } **Upload** | The files are copied into Depictio | 3 |
| :material-file-cog-outline:{ .ws-ic .ws-ic-other } **Template** | What Depictio knows about a pipeline: which outputs to read, how to link them, which dashboard to build | 4 |
| :material-history:{ .ws-ic .ws-ic-version } **Version** | Each change of a table (an edit, an append, **Add columns**) and each save of a dashboard is kept; earlier ones can be shown or restored | 3, 5 |
| :material-clock-outline:{ .ws-ic .ws-ic-you } **What's new** | What changed in a dashboard's data since your last visit | 5 |
| :material-account-key-outline:{ .ws-ic .ws-ic-other } **Owner, editor, reader** | Who can change a project or dashboard (owner, editor) and who can only open it (reader, *Viewer* on the Permissions page) | 1, 2, 3 |
| :material-account-multiple-outline:{ .ws-ic .ws-ic-you } **Group** | A named selection of samples, kept in your browser, compared in the cards | 1 |
| :material-account-group-outline:{ .ws-ic .ws-ic-other } **User group** | A set of accounts, created by an administrator. A project shared with it is open to all its members | 3 |
| :material-earth:{ .ws-ic .ws-ic-other } **Public** | A project every signed-in account can open | 3 |
