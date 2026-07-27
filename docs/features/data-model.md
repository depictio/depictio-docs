---
title: "Data Model"
icon: material/database-outline
description: "How Depictio's domain objects fit together — what a project document actually contains, how a data collection reaches its Delta table, and which MongoDB collection holds what."
---

# :material-database-outline: Data Model

Depictio's object model mirrors how pipelines actually run: a project describes one or
more workflows, each execution of a workflow produces files, and those files are
aggregated into typed **data collections** that dashboards read from.

Two things about the model surprise people, and both are worth getting straight before
anything else: most of the hierarchy is **embedded in a single document** rather than
spread across collections, and a data collection's actual table lives somewhere the data
collection itself never mentions.

---

## The shape of a project

[![The shape of a project](../images/data-model/project-shape_light.png#only-light)](../images/data-model/project-shape_light.png){target=_blank}

[![The shape of a project](../images/data-model/project-shape_dark.png#only-dark)](../images/data-model/project-shape_dark.png){target=_blank}

A **Project** is one document in the `projects` collection, and it carries the entire
configuration tree with it. Workflows are a field of the project; data collections are a
field of the workflow. Neither is a document of its own in the current write path, and
neither holds a pointer back up — the hierarchy is positional, so finding a data
collection's parent means querying the project that contains it.

Projects come in two shapes:

- **`advanced`** projects have the workflow layer shown above, and are defined by a YAML
  configuration file.
- **`basic`** projects skip it. Data collections hang directly off
  `Project.data_collections`, which is the dashed box in the figure.

Everything a user types is a **tag** — `data_collection_tag`, `workflow_tag`,
`project_tag`. Everything the system joins on is an **ObjectId**. YAML and the CLI speak
tags; the API and stored dashboard components speak IDs. When a dashboard component
records which data it renders, it stores `dc_id` and `wf_id`, not the tags.

A **Dashboard** is the one part of the picture that is genuinely a separate document. It
points at its project with `project_id`, and multi-tab dashboards point at their parent
tab with `parent_dashboard_id`. Note that `dashboard_id` is the business key used in
queries, and is distinct from Mongo's `_id`.

---

## From configuration to data

[![From configuration to data](../images/data-model/config-to-data_light.png#only-light)](../images/data-model/config-to-data_light.png){target=_blank}

[![From configuration to data](../images/data-model/config-to-data_dark.png#only-dark)](../images/data-model/config-to-data_dark.png){target=_blank}

A DataCollection describes *what* a table is — its tag, its type, the scan that finds its
source files. It does not say where the table is. That lives in a separate
`DeltaTableAggregated` document in the `deltatables` collection, one per data collection,
holding the Delta table's location plus the history of every aggregation run against it
(including the column schema the UI displays).

This is why `delta_location` and `last_aggregation` show up in API responses but appear
nowhere in the stored project: the API joins them in from `deltatables` at read time.

The ingestion path in between: a **WorkflowRun** records one pipeline execution and scans
its output directory; each matching file becomes a **File** record; the files belonging to
a data collection are then aggregated into its Delta table.

---

## Objects at a glance

| Object | Lives in | Key fields | Notes |
| --- | --- | --- | --- |
| **Project** | `projects` | `name`, `project_type`, `workflows`, `data_collections`, `joins`, `links`, `permissions`, `is_public` | The aggregate root. `project_type` is `basic` or `advanced`. |
| **Workflow** | embedded in Project | `name`, `engine`, `catalog`, `data_location`, `data_collections` | `workflow_tag` is derived — an nf-core catalog entry always yields `nf-core/{name}`. |
| **WorkflowRun** | `runs` | `run_tag`, `run_location`, `workflow_id`, `files_id`, `creation_time`, `last_modification_time`, `run_hash`, `scan_results` | One pipeline execution. `scan_results` holds per-scan file counts. |
| **DataCollection** | embedded in Workflow or Project | `data_collection_tag`, `config`, `optional` | `config` carries the type, the scan and the type-specific properties. |
| **File** | `files` | `filename`, `file_location`, `file_hash`, `filesize`, `data_collection_id`, `run_id` | `file_hash` is what makes re-ingestion incremental. |
| **DeltaTableAggregated** | `deltatables` | `data_collection_id`, `delta_table_location`, `aggregation` | One per table-like data collection. |
| **Dashboard** | `dashboards` | `dashboard_id`, `project_id`, `title`, `permissions`, `stored_metadata`, `is_main_tab`, `parent_dashboard_id`, `tab_order` | Components are records inside `stored_metadata`. |
| **User** | `users` | `email`, `is_admin`, `is_anonymous`, `is_temporary` | Group membership lives on the group, not the user. |
| **Group** | `groups` | `name`, `users_ids` | |

### Data collection types

| Type | Content |
| --- | --- |
| `table` | Tabular data (CSV/TSV/Parquet/Excel → Delta Lake) |
| `multiqc` | MultiQC report data |
| `image` | Image files, served from S3 with thumbnails |
| `geojson` | GeoJSON boundaries for choropleth maps |
| `phylogeny` | Newick or Nexus trees |
| `jbrowse2` | JBrowse2 genome browser tracks |

A table data collection that declares latitude and longitude columns becomes map-capable
without changing its type — see [Components](components.md#map-components).

### Where a data collection came from

| Source | Meaning |
| --- | --- |
| `native` | Scanned directly from workflow output files. Requires a `scan` configuration. |
| `joined` | Produced by a [JoinDefinition](#joining-and-linking) merging two other collections. |
| `transformed` | Produced by a [Python recipe](../usage/projects/recipes.md). |
| `aggregated` | Reserved. |

Only `native` collections need a scan — derived ones are written by whatever process
creates them.

---

## Access control

Permissions are not a separate document. A `Permission` object is **embedded** into every
Project, Dashboard, WorkflowRun and File, holding three disjoint sets of users:

| Tier | Can do |
| --- | --- |
| **owners** | Full control — edit, share, delete |
| **editors** | Modify dashboard content, run data updates |
| **viewers** | Read-only access to dashboards and data |

`viewers` additionally accepts the wildcard `*`, which is how a project or dashboard is
made public. See [Authentication Modes](../usage/guides/authentication-modes.md) for how
this interacts with anonymous and unauthenticated deployments.

---

## Joining and linking

Two different mechanisms, easily confused:

- A **JoinDefinition** (`Project.joins`) physically merges two data collections on shared
  columns — `left_dc`, `right_dc`, `on_columns`, `how`, plus a granularity policy — and
  writes the result as a new data collection with `source: joined`.
- A **DCLink** (`Project.links`) merges nothing. It propagates *filters* between data
  collections at query time, resolving identifiers between them by one of several
  strategies (`direct`, `sample_mapping`, `pattern`, `regex`, `wildcard`).

Use a join when you want one table; use a link when you want two tables that filter each
other. [Cross-DC Filtering](cross-dc-filtering.md) covers the resolver strategies in
depth.

!!! note "Legacy join configuration"

    A `join` block on an individual data collection's config still deserialises, but it is
    superseded by project-level `joins` and is no longer read.

---

## MongoDB collections

**Configuration**

| Collection | Holds |
| --- | --- |
| `projects` | Projects, with their workflows, data collections, joins, links and permissions embedded |
| `dashboards` | Dashboards and dashboard tabs |
| `workflows`, `data_collections` | Legacy. Both are embedded in `projects` now; these are read and cleaned up, not written to |

**Ingested data**

| Collection | Holds |
| --- | --- |
| `runs` | Workflow runs and their scan results |
| `files` | One record per ingested file |
| `deltatables` | Delta table location and aggregation history, one per data collection |
| `multiqc` | Parsed MultiQC report metadata |
| `multiqc_prerender` | Pre-rendered MultiQC figures, keyed by data collection |
| `compute_results` | Cached results of advanced-visualisation computations |
| `jbrowse` | Generated JBrowse2 track configurations |

**Users and access**

| Collection | Holds |
| --- | --- |
| `users` | User accounts |
| `groups` | Groups and their membership |
| `tokens` | Access and refresh token pairs |
| `magic_link_tickets` | Short-lived passwordless login tickets, TTL-expiring |

**Operations**

| Collection | Holds |
| --- | --- |
| `task_events` | Background task lifecycle events |
| `ingestion_runs` | Per-ingestion progress and step timings |
| `app_logs` | Application logs (capped collection) |
| `user_sessions`, `user_activities` | Usage analytics |
| `initialization` | Startup lock, so concurrent API replicas seed the database once |

See [Monitoring](../usage/administration/monitoring.md) for what the operations
collections drive in the admin UI.

---

## Related Documentation

- :material-sitemap: [Architecture](architecture.md) — Microservices stack and data flow
- :material-filter: [Cross-DC Filtering](cross-dc-filtering.md) — DCLink resolver strategies in depth
- :material-sync: [YAML Dashboard Sync](yaml-sync.md) — Declarative dashboard export/import
- :material-code-braces: [Contributing](../developer/contributing.md) — How to extend the platform
