---
title: "Data Model"
icon: material/database-outline
description: "How Depictio's domain objects fit together: what a project document actually contains, how a data collection reaches its Delta table, and which MongoDB collection holds what."
---

# :material-database-outline: Data Model

A **project** is the unit everything else hangs off. It names one or more
**workflows**, each workflow declares the **data collections** it produces, and every
data collection becomes one table that dashboards read from.

Two details are worth having in mind before reading further, because neither is visible
from the object names alone:

1. **Almost none of that hierarchy is stored as separate documents.** Workflows and data
   collections are fields inside the project document, not rows in their own collections.
2. **A data collection does not record where its table is.** The location lives in a
   separate document, and the API stitches the two together when it answers a request.

---

## The two shapes of a project

[![The two shapes of a project](../images/data-model/project-shape_light.png#only-light)](../images/data-model/project-shape_light.png){target=_blank}

[![The two shapes of a project](../images/data-model/project-shape_dark.png#only-dark)](../images/data-model/project-shape_dark.png){target=_blank}

| `project_type` | Structure | Typical use |
| --- | --- | --- |
| **`advanced`** | Project :material-arrow-right: Workflow :material-arrow-right: DataCollection | Pipeline output. Defined in a YAML configuration file, ingested by the CLI. |
| **`basic`** | Project :material-arrow-right: DataCollection | A few files you want on a dashboard. No pipeline, no runs. |

Nothing else changes between the two. The same data collection types, joins, links,
permissions and dashboards apply either way. The workflow layer only exists to answer
"which pipeline produced this, and in which of its runs".

### Workflow and run are different things

The words are used precisely here, in the sense that
[nf-core](https://nf-co.re/) and [WorkflowHub](https://workflowhub.eu/) use them:

- A **Workflow** is the *definition*: `nf-core/ampliseq`, a Snakemake catalog entry, a
  pipeline you wrote yourself. It says what the pipeline produces and where to look for
  it. A project can define several.
- A **WorkflowRun** is one *execution* of that definition: an output folder produced by
  processing one or many samples. Runs live in their own `runs` collection, and re-running
  a pipeline adds a run rather than replacing anything.

### Tags and IDs

Everything a user types is a **tag**: `project_tag`, `workflow_tag`,
`data_collection_tag`. Everything the system joins on is an **ObjectId**. YAML and the CLI
speak tags; the API and the stored dashboard components speak IDs. When a component records
which data it renders, it stores `dc_id` and `wf_id`.

`workflow_tag` is derived rather than typed. An nf-core catalog entry always yields
`nf-core/{name}`.

### Dashboards

A **Dashboard** is a genuinely separate document, and it points at its project with
`project_id`. What the user experiences as one multi-tab dashboard is stored as several
documents: a main one (`is_main_tab`) plus one per additional tab, each carrying
`parent_dashboard_id` and `tab_order`. Components live inside each tab's
`stored_metadata`.

---

## From configuration to data

[![From configuration to data](../images/data-model/config-to-data_light.png#only-light)](../images/data-model/config-to-data_light.png){target=_blank}

[![From configuration to data](../images/data-model/config-to-data_dark.png#only-dark)](../images/data-model/config-to-data_dark.png){target=_blank}

A run's output folder is scanned, and every matching file becomes a **File** record with
its location, size and hash. A **data collection** then gathers every file of the same
type, across every run of the workflow, into a single table. The table itself is written
to S3 in [Delta Lake](https://delta.io/) format, which is what makes a re-ingestion an
append with history rather than an overwrite.

The piece that is easy to miss is that the data collection never names that table. Its
location and the schema of every aggregation run are held in a separate document in the
`deltatables` collection, one per data collection (the model is called
`DeltaTableAggregated`). This is why `delta_location` and `last_aggregation` appear in API
responses but nowhere in the project you configured: the API joins them in as it serves
the project.

`file_hash` is what keeps re-ingestion incremental. An unchanged file is recognised and
skipped rather than aggregated again.

---

## Objects at a glance

| Object | Lives in | Key fields | Notes |
| --- | --- | --- | --- |
| **Project** | `projects` | `name`, `project_type`, `workflows`, `data_collections`, `joins`, `links`, `permissions`, `is_public` | The aggregate root. |
| **Workflow** | embedded in Project | `name`, `engine`, `catalog`, `data_location`, `data_collections` | The pipeline definition. |
| **WorkflowRun** | `runs` | `run_tag`, `run_location`, `workflow_id`, `files_id`, `creation_time`, `last_modification_time`, `run_hash`, `scan_results` | One execution. `scan_results` holds per-scan file counts. |
| **DataCollection** | embedded in Workflow or Project | `data_collection_tag`, `config`, `optional` | `config` carries the type, the scan and the type-specific properties. |
| **File** | `files` | `filename`, `file_location`, `file_hash`, `filesize`, `data_collection_id`, `run_id` | One per ingested file. |
| **DeltaTableAggregated** | `deltatables` | `data_collection_id`, `delta_table_location`, `aggregation` | One per table-like data collection. |
| **Dashboard** | `dashboards` | `dashboard_id`, `project_id`, `title`, `permissions`, `stored_metadata`, `is_main_tab`, `parent_dashboard_id`, `tab_order` | One document per tab. |
| **User** | `users` | `email`, `is_admin`, `is_anonymous`, `is_temporary` | Group membership lives on the group, not the user. |
| **Group** | `groups` | `name`, `users_ids` | |

### Data collection types

| Type | Content |
| --- | --- |
| `table` | Tabular data (CSV/TSV/Parquet/Excel, stored as Delta Lake) |
| `multiqc` | MultiQC report data |
| `image` | Image files, served from S3 with thumbnails |
| `geojson` | GeoJSON boundaries for choropleth maps |
| `phylogeny` | Newick or Nexus trees |

A `table` collection that declares latitude and longitude columns becomes map-capable
without changing its type. See [Components](components.md#map-components).

### Where a data collection came from

| Source | Meaning |
| --- | --- |
| `native` | Scanned directly from workflow output files. Requires a `scan` configuration. |
| `joined` | Produced by a [join](#joining-and-linking) merging two other collections. |
| `transformed` | Produced by a [Python recipe](../usage/projects/recipes.md). |
| `aggregated` | Reserved. |

Only `native` collections need a scan. Derived ones are written by whatever process
creates them.

---

## Joining and linking

[![Joining and linking](../images/data-model/join-vs-link_light.png#only-light)](../images/data-model/join-vs-link_light.png){target=_blank}

[![Joining and linking](../images/data-model/join-vs-link_dark.png#only-dark)](../images/data-model/join-vs-link_dark.png){target=_blank}

Two mechanisms that sound alike and behave nothing alike:

- A **JoinDefinition** (`Project.joins`) physically merges two data collections on shared
  columns (`left_dc`, `right_dc`, `on_columns`, `how`, plus a granularity policy) and
  writes the result as a new data collection with `source: joined`. One table from then on.
- A **DCLink** (`Project.links`) merges nothing. It propagates *filters* between two data
  collections at query time, resolving identifiers between them by one of several
  strategies (`direct`, `sample_mapping`, `pattern`, `regex`, `wildcard`).

Use a join when you want one table. Use a link when you want two tables that filter each
other. [Cross-DC Filtering](cross-dc-filtering.md) covers the resolver strategies in
depth.

!!! note "Legacy join configuration"

    A `join` block on an individual data collection's config still deserialises, but it is
    superseded by project-level `joins` and is no longer read.

---

## Access control

Permissions are not a separate document. A `Permission` object is **embedded** into every
Project, Dashboard, WorkflowRun and File, holding three disjoint sets of users:

| Tier | Can do |
| --- | --- |
| **owners** | Full control: edit, share, delete |
| **editors** | Modify dashboard content, run data updates |
| **viewers** | Read-only access to dashboards and data |

`viewers` additionally accepts the wildcard `*`, which is how a project or dashboard is
made public. See [Authentication Modes](../usage/guides/authentication-modes.md) for how
this interacts with anonymous and unauthenticated deployments.

---

## Where it all lands in MongoDB

The collections you are likely to care about, whether you are writing a backup script or
inspecting a database by hand:

| Collection | Holds | Rebuildable? |
| --- | --- | --- |
| `projects` | Projects, with their workflows, data collections, joins, links and permissions embedded | No |
| `dashboards` | Dashboards and their tabs | No |
| `users`, `groups`, `tokens` | Accounts, membership, access and refresh token pairs | No |
| `runs`, `files` | Workflow runs and one record per ingested file | Yes, if the source files are still there |
| `deltatables` | Delta table location and aggregation history, one per data collection | Yes, if the source files are still there |

Everything else is derived, operational or short-lived: parsed and pre-rendered MultiQC
output, cached advanced-visualisation results, generated genome-browser configurations,
task and ingestion progress, application logs, usage analytics, expiring login tickets,
and a startup lock that lets concurrent API replicas seed the database exactly once. Losing
any of it costs a recomputation, not data.

`show collections` in `mongosh` gives you the current list at any time, which is more
reliable than a table here. See
[Backup & Restore](../usage/administration/backup.md) for what the CLI dumps, and
[Monitoring](../usage/administration/monitoring.md) for what the operational collections
drive in the admin UI.

!!! note "Legacy collections"

    `workflows` and `data_collections` still exist in older databases. Both are embedded in
    `projects` now. They are read during migration and cleaned up, never written to.

---

## Related Documentation

- :material-sitemap: [Architecture](architecture.md) - Microservices stack and data flow
- :material-filter: [Cross-DC Filtering](cross-dc-filtering.md) - DCLink resolver strategies in depth
- :material-sync: [YAML Dashboard Sync](yaml-sync.md) - Declarative dashboard export and import
- :material-code-braces: [Contributing](../developer/contributing.md) - How to extend the platform
