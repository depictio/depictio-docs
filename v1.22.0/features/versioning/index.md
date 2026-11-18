# Dashboard and data versions

Depictio keeps two kinds of history. A **dashboard version** is a copy of a dashboard's content, recorded each time the dashboard changes. A **data version** is a commit of a data collection's Delta table, written each time the data is ingested. A dashboard version also records which data version each of its collections was at, so a past dashboard can be drawn from the data it showed at the time.

| You want to                                                           | Where                                                                                                                                                                                                                       |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| See, preview, restore or bookmark an earlier state of a dashboard     | Editor: **Settings → History**                                                                                                                                                                                              |
| Compare one component with an earlier version of it, or bring it back | Editor: the component's ⋮ menu → **History**                                                                                                                                                                                |
| Draw the editor from earlier data                                     | Editor: **Settings → Data version**                                                                                                                                                                                         |
| Show someone a past version, read-only                                | A preview link, `/dashboard/{id}?version={version id}`                                                                                                                                                                      |
| See the commits of a table                                            | Project page: the data collection's **Version history**                                                                                                                                                                     |
| List or clean up commits from a terminal                              | [`depictio data versions`](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#data-versions) and [`depictio data vacuum`](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#data-vacuum) |

______________________________________________________________________

## What a version holds

A version covers the whole dashboard: its main tab and every child tab, as one entry. Versions are numbered per dashboard, `v1`, `v2` and on, and the History list calls a version by its name when it has one.

A version holds what the tabs contain: layout, components, titles, icons, notes, sections, category colours, the brand theme, the settings saved for everyone (tab defaults, tiles, filtering, the Guide), and each tab's group and position.

| Not in a version                                                                                                   | What that means                                                                                               |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Permissions, public visibility, the project                                                                        | A restore never grants or removes access                                                                      |
| Uploaded logo files                                                                                                | A restore or a preview keeps the current logo                                                                 |
| [Comments and annotations](https://depictio.github.io/depictio-docs/latest/features/comments-annotations/index.md) | Stored apart from the dashboard. A restore leaves them in place                                               |
| The data                                                                                                           | A version records which commit each data collection was at, not its rows. See [Data versions](#data-versions) |

A version larger than 8 MiB is not recorded. The save itself always goes through.

______________________________________________________________________

## When a version is recorded

| Change                                                                                              | Recorded as                                                                                         |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| The editor's own saves, about half a second after you stop editing                                  | **Autosave**                                                                                        |
| Renaming the dashboard, editing or reordering tabs, branding                                        | **Autosave**                                                                                        |
| The **Save** button                                                                                 | **Saved**                                                                                           |
| Creating or duplicating a dashboard, adding or deleting a tab                                       | **Saved**                                                                                           |
| [**Bookmark the current state**](#bookmarks) in Settings → History                                  | **Saved**, bookmarked                                                                               |
| A restore                                                                                           | **Saved** for the state it replaces, then **Restored**                                              |
| Importing a dashboard (YAML or JSON, including the dashboards `depictio ingest` imports or tops up) | **Imported**. An import over an existing dashboard first records the state it replaces as **Saved** |

The first change to a dashboard that has no history yet first records its current state, labelled **Before first tracked change**, so the original is never out of reach.

Autosaves fold together. An autosave joins the previous version, rather than opening a new one, when both are autosaves by the same person, the previous one is neither bookmarked nor named, and it was created less than 5 minutes ago. The window is counted from the version's creation and does not slide, so a long editing session leaves one version every 5 minutes. Such a version says how many saves it holds, as in *4 saves over 3 min*.

A save that changes nothing records nothing, whatever its kind. **Save** then turns the newest version, if it is an autosave, into **Saved**, so later autosaves no longer fold into it, and **Bookmark the current state** names and bookmarks that newest version.

**How saves become versions.** Autosaves by the same person fold into one version for up to 5 minutes, a save that changes nothing records nothing, and *Save* or a bookmark seals the newest version so the next autosave opens a new one. Retention keeps bookmarked versions for good and prunes the rest after 90 days. The diagram says *pinned* where the History list says *bookmarked*.

______________________________________________________________________

## The History section

In the editor, **Settings → History** lists every version, newest first and grouped by day. Each row shows the version's name and kind icon and how long ago it was saved; its chevron opens the details: the kind (**Autosave**, **Saved**, **Restored** or **Imported**), the date, the author, the number of components and tabs, and a line on the data, such as *2 data collections pinned*. The version the dashboard is at is marked **Current**, and the one the editor's data comes from, **Data in use**. **Load older versions** pages further back.

**Editor → Settings → History.** The versions grouped by day, newest first, the top one marked *Current*. The open row shows its kind, date and author, its component and tab counts, and how many data collections it pinned; bookmarked versions show their name and a bookmark badge.

Each row has **Restore**, and a ⋮ menu with the other three actions:

| Action                   | What it does                                                                                                           |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **Preview in a new tab** | Opens the version read-only in a new browser tab. See [Preview](#preview)                                              |
| **Restore**              | Brings the dashboard back to this version. Unavailable on the current one. See [Restore](#restore)                     |
| **Bookmark**             | Names the version and keeps it for good. See [Bookmarks](#bookmarks)                                                   |
| **Delete**               | Removes the version for good. Only the dashboard's owners can, and not while its data is in use under **Data version** |

**A History row's actions.** The *Restore* button, with its tooltip, and the ⋮ menu with *Preview in a new tab*, *Bookmark* and *Delete*. *Restore* is unavailable on the current version.

Deleting a version cannot be undone

Every other action here, a restore included, can be undone by restoring an earlier version. Deleting a bookmarked version through the API needs `force=true`, and the only version a dashboard has cannot be deleted.

### Bookmarks

A bookmark gives a version a name, keeps it for good, and stops later autosaves from folding into it. **Bookmark** in a row's ⋮ menu opens a dialog with an optional **Name**; **Remove bookmark** takes it off again.

**⋮ → Bookmark on a History row.** The dialog names v2 *Before recalibration*. The name is optional; a bookmarked version is kept for good, and later autosaves no longer fold into it.

**Bookmark the current state**, at the top of the section, records the dashboard as it is now and bookmarks it in one step. It needs a name.

### Preview

A preview opens `/dashboard/{id}?version={version id}` in the viewer. A banner across the top says which version it is, who saved it and when, and, after *Layout and components are from this version*, where each data collection comes from:

| Banner                                                                | Meaning                                                                    |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| *Past data: {collection} (vN)*                                        | Drawn from the commit the version recorded                                 |
| *Latest data: {collection}*                                           | The version recorded no commit for it, such as a collection added since    |
| *No data version recorded, so the latest data is shown: {collection}* | A type that is never pinned. See [What can be pinned](#what-can-be-pinned) |

**⋮ → Preview in a new tab.** The read-only preview of v3 *Scale recalibrated*: its banner names the version, its author and the past data each collection is drawn from. *Back to current* leaves the preview; owners also get *Open in editor*, to restore it from History.

The preview is read-only: editing, live updates and the notes footer are off, and links between tabs keep the version. The tab list itself is today's: a tab deleted since the version is not listed, and opening a tab added since fails to load, as the version holds nothing for it.

Anyone who can open the dashboard can open a preview link. **Back to current** leaves the preview. Owners also see **Open in editor**, to restore the version from the editor's History.

### Restore

**Restore** first records the present state as a version, then writes the version's content back into every tab:

- tabs deleted since are recreated, with the main tab's current permissions;
- tabs added since are deleted (the main tab never is);
- permissions, visibility, comment threads and the logo are left as they are;
- a **Restored** version is recorded, and a fresh thumbnail queued.

A restore brings back the dashboard, not the data: after it, components read the latest data. To undo a restore, restore the version recorded just before it.

**What a restore does.** The present is recorded as a version first, then every tab is written back to match the version: tabs deleted since are recreated, tabs added since are deleted. Permissions, visibility, comments and the logo never come from the snapshot.

Before you confirm, the dialog checks the version against the data as it is now:

| Result                              | Meaning                                                                      |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| **Still matches the current data**  | Every column the version uses is still there, with the same type             |
| **Data has changed since**          | A column the version does not use was removed, or a column changed type      |
| **Some components will not render** | A data collection was deleted, or a column a component uses no longer exists |

Each changed collection is listed with the missing and retyped columns and the number of components affected. The check never blocks a restore: components whose data is gone render empty.

**A History row → Restore.** The dialog for v5 checks the version against today's data, here *Still matches the current data*, and says the current state is saved first. The other results, *Data has changed since* and *Some components will not render*, list the collections and columns concerned; none of them blocks the restore.

______________________________________________________________________

## Component history

In the editor, **History** in a component's ⋮ menu shows that one component across the dashboard's versions. It is offered on tiles and on filters, once the dashboard has at least one version.

Readers get a read-only view of it, without **Restore**, from the **Versions** part of the [dashboard Guide](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/#what-it-covers) (v1.17.4+).

**Editor → a component's ⋮ menu → History.** Here on a box plot, below *Edit*. It is offered on tiles and on filters once the dashboard has at least one version.

| Control             | What it does                                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| **Version**         | Picks the version to show, with **Older version** and **Newer version** to step through them        |
| **Compare**         | Shows the version on the left and the component as it is now, **Current**, on the right             |
| **Historical data** | On by default: draws the version from the data it recorded. Off, it uses the latest data            |
| **Data version**    | Picks the data for each side: *This version's data*, *Latest data*, or any commit of the collection |

**Component history, one version.** The box plot as it was in v2 *Before recalibration*, drawn through its own stored definition from the data that version recorded (commit v1). *Older version* and *Newer version* step through the others.

With **Compare** on and both sides reading the same commit, any difference comes from the component's configuration alone. A component that did not exist in a version says so.

**Component history with Compare on.** The stored version, *Before recalibration*, on the left, and the component as it is now, *Current*, on the right. Each side has its own *Data version*: set both to the same commit and any difference left comes from the configuration alone.

**Restore this component** puts back only this component, as it was in the selected version, and leaves the rest of the dashboard alone. **Also restore its position and size** brings back its place in the grid too, with its section, group or panel; off, it stays where it is now, in the same section. A component deleted since is added back at its old position. The present state is recorded as a version first, so this can be undone. A component whose tab no longer exists cannot be restored alone: restore the whole version instead.

**Component history → Restore this component.** Only this component goes back to the selected version. With *Also restore its position and size* off, as here, it keeps its current place in the grid. The present state is recorded first, so this can be undone.

Keep components matched across YAML imports

Versions match a component by its id within its tab. A component imported from YAML with a `tag` gets an id derived from that tag, so it keeps its history when the YAML is imported again. A component without a `tag` gets a new id at each import, and its history starts over. See [YAML Dashboard Sync](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md).

______________________________________________________________________

## Data versions

Every write to a `table` or `image` data collection is a commit of its Delta table on S3, numbered `v0`, `v1` and on. Depictio records on each commit which ingestion wrote it, what triggered it and how it was written. A dashboard version records, for each data collection it uses, the commit that was current when it was saved.

### What can be pinned

| Data collection type   | Pinned to a past commit | What a past version shows                                                              |
| ---------------------- | ----------------------- | -------------------------------------------------------------------------------------- |
| `table`                | Yes                     | The table as that commit wrote it                                                      |
| `image`                | Paths only              | The list of image paths as it was; the image files themselves as they are now          |
| `genomic_tracks`       | Track list only         | The track manifest as that commit wrote it; the track files themselves as they are now |
| `multiqc`              | No                      | Always the latest data                                                                 |
| `geojson`, `phylogeny` | No                      | Always the latest data                                                                 |

A table written before Depictio recorded commit numbers has no commit to pin either. Wherever a collection cannot be pinned, the latest data is shown: the History rows say how many collections are pinned, and the preview and editor banners name each one. MultiQC, advanced visualization and funnel components always read the latest data, and carry a **Current data** badge while earlier data is shown. A genome browser tile reads its track manifest at the pinned commit, but the files that manifest names are not versioned, so a track replaced on S3 or at its remote location shows its new content.

### Data version in the editor

**Settings → Data version** draws the editor from earlier data, for you only, until you reload. Nothing is saved: saving the dashboard still writes its layout and components, never its data.

| Field                         | What it does                                                                                                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **As of a dashboard version** | Every collection goes back to the data a dashboard version was saved with. Only versions that recorded a data version are listed. **Use this data** applies it        |
| **One collection**            | Pins one collection to one of its commits, such as today's layout against last month's data. Applies as you pick, and wins over the version above for that collection |

**Editor → Settings → Data version, after *Use this data*.** The editor reads the data of *Before recalibration*: that version is picked under *As of a dashboard version*, and each collection is at *This version's data (v1)*. One collection can also be set to any of its own commits.

While the editor shows earlier data, a banner above the grid says so (*Showing data as of {version}*), with a **Not current** badge and the commit each collection is drawn from, and **Back to current data** returns to the latest data.

**The editor drawn from earlier data.** The banner above the grid reads *Showing data as of Before recalibration*, with a *Not current* badge and one badge per collection naming the commit it is drawn from. *Back to current data* returns to the latest data.

### Dataset history

On a project's page, a data collection's details show its **Delta version** below **Last Aggregated**, or *Not recorded*. For a `table` collection, a **Version history** panel below the **Data Preview** lists its commits:

| Column              | Shows                                                                                          |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Version**         | The commit number. **unmatched** for an ingestion recorded before commit numbers were          |
| **When**            | When it was written                                                                            |
| **Operation**       | The Delta operation, with how Depictio wrote it: *full rewrite*, *runs replaced* or *appended* |
| **Rows**, **Files** | Rows added, files added and removed                                                            |
| **By**              | What triggered the ingestion (**Manual**, **Watch** or **UI**) and who ran it                  |

**Projects → a project → a data collection → Version history.** The eight commits of `physical_features`, v7 the current one: the latest four written by a watcher (*Watch*), the first four by hand (*Manual*), each with its operation and the rows and files it added.

When the object store cannot be reached, the panel shows only what Depictio recorded, and says so. Once the data preview is loaded, a table with two commits or more offers **At version**, which shows the table as an earlier commit wrote it, under a warning that it is not the current data.

**Data Preview → Load Data → At version.** The table as commit v2 wrote it: 223 rows instead of today's 342, under the warning *Viewing v2: this is not the current data*.

______________________________________________________________________

## How new data versions are written

Each `depictio ingest` writes one commit per data collection it processes. Two options decide how much of the table a commit rewrites:

| Option                             | Effect                                                                                                                                                                     |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--write-mode overwrite` (default) | Rewrites the whole table                                                                                                                                                   |
| `--write-mode replace-runs`        | Partitions the table by run and rewrites only the runs in this ingestion, leaving the others untouched                                                                     |
| `--incremental-write`              | With `replace-runs`, rewrites only the runs that changed. Falls back to a full rebuild whenever that cannot be done safely, such as a run removed or a column type changed |
| `--skip-unchanged`                 | Leaves a table alone when the scan found no new, changed or removed file for it                                                                                            |
| `--repartition`                    | Lets `replace-runs` partition a table that is not partitioned by run yet. This rewrites every row                                                                          |

`depictio watch` runs the same ingestion on a loop, whenever the results directory changes, so a project's data versions follow the pipeline without anyone running a command. Each watcher appears in the admin [**Watchers** pane](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/#watchers), where **Run now** asks it for a cycle at once.

**Run now, from the Watchers pane.** The server records the request and the watcher picks it up on its next poll, so *Run now* reaches a watcher on a machine the API cannot connect to.

See [`depictio watch`](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#watch-command) for its options, and [Running a watcher as a service](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#running-a-watcher-as-a-service) for systemd and Docker Compose.

Vacuuming removes past commits

Delta keeps the files of every past commit, so a table's footprint on S3 grows with each ingestion. [`depictio data vacuum`](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#data-vacuum) removes the files no commit newer than `--retention-hours` (168 by default) needs. A dashboard version, a preview or a pin that reads a commit older than that then has nothing to read. Nothing in Depictio vacuums on its own.

______________________________________________________________________

## Retention and configuration

| Kept                                  | For how long                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Bookmarked versions                   | For good                                                                                               |
| Saved, restored and imported versions | 90 days                                                                                                |
| Autosaves                             | The newest 100, thinned to the last one of each day once older than 30 days, and dropped after 90 days |

The pruning runs after a version is recorded, once a dashboard holds more than 120 autosaves that are not bookmarked (1.2 times the autosave cap), or once a version that is not bookmarked is older than the retention period (90 days).

Deleting a dashboard deletes its history, and deleting a project deletes the history of its dashboards. [Backups](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md) include it.

| Variable                                              | Default   | Description                                                               |
| ----------------------------------------------------- | --------- | ------------------------------------------------------------------------- |
| `DEPICTIO_DASHBOARD_VERSIONS_ENABLED`                 | `true`    | Record versions. Off, nothing new is recorded                             |
| `DEPICTIO_DASHBOARD_VERSIONS_COALESCE_WINDOW_SECONDS` | `300`     | How long autosaves by one person fold into one version, from its creation |
| `DEPICTIO_DASHBOARD_VERSIONS_MAX_VERSIONS_PER_FAMILY` | `100`     | Autosaves kept per dashboard                                              |
| `DEPICTIO_DASHBOARD_VERSIONS_RETENTION_DAYS`          | `90`      | Age after which versions that are not bookmarked are dropped              |
| `DEPICTIO_DASHBOARD_VERSIONS_KEEP_DAILY_FOR_DAYS`     | `30`      | Age after which autosaves thin to one per day                             |
| `DEPICTIO_DASHBOARD_VERSIONS_MAX_SNAPSHOT_BYTES`      | `8388608` | Largest version recorded, in bytes (8 MiB)                                |

______________________________________________________________________

## API

Under `/depictio/api/v1/dashboards`. Reading needs view access to the project, writing needs edit access to the dashboard, and deleting a version needs ownership.

| Method and path                                                        | What it does                                                                               |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `GET /{dashboard_id}/versions`                                         | Lists the versions, newest first. `limit` (1–200, default 50), `before_seq`, `pinned_only` |
| `GET /{dashboard_id}/versions/current`                                 | The version the dashboard is at                                                            |
| `POST /{dashboard_id}/versions`                                        | Records the current state, with an optional `label`                                        |
| `GET /versions/{version_id}`                                           | One version, with its content                                                              |
| `GET /versions/{version_id}/compatibility`                             | The check against the current data                                                         |
| `PATCH /versions/{version_id}`                                         | Renames it                                                                                 |
| `POST /versions/{version_id}/pin`, `DELETE /versions/{version_id}/pin` | Bookmarks it, or removes the bookmark                                                      |
| `DELETE /versions/{version_id}`                                        | Deletes it. `force=true` for a bookmarked one                                              |
| `POST /versions/{version_id}/restore`                                  | Restores the dashboard to it                                                               |
| `POST /versions/{version_id}/restore_component`                        | Restores one component: `component_index`, `tab_id`, `restore_layout`                      |
| `GET /get/{dashboard_id}?version_id=`                                  | The dashboard as that version holds it, as the preview reads it                            |

______________________________________________________________________

## Known limits

- `multiqc`, `geojson` and `phylogeny` collections always show their latest data, and so do image files, genome track files and the components marked **Current data**.
- A preview uses today's tab list. A tab deleted since the version is not listed until the version is restored, and a tab added since fails to load.
- Vacuumed commits can no longer be read. See the warning [above](#how-new-data-versions-are-written).
- The editor's data version lasts until you reload, and is never saved or shared.

______________________________________________________________________

## Related Documentation

- [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/index.md): tabs, layout and saving
- [Using the Dashboard](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_usage/#dashboard-settings-drawer): the Settings dialog
- [Depictio CLI](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#watch-command): `depictio watch` and the write options
- [Monitoring](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/#watchers): the Watchers pane and live ingestion steps
- [Backup & Restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md): what a backup covers
