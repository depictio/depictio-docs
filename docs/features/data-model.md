---
title: "Data Model"
icon: material/database-outline
description: "How Depictio's domain objects fit together: what a project document actually contains, how a data collection reaches the storage it is served from, and how joins differ from links."
---

# :material-database-outline: Data Model

A **project** is the unit everything else hangs off. It names one or more
**workflows**, each workflow declares the **data collections** it produces, and every
data collection becomes one thing a dashboard can read.

Two details are worth having in mind before reading further, because neither is visible
from the object names alone:

1. **Almost none of that hierarchy is stored as separate documents.** Workflows and data
   collections are fields inside the project document, not rows in their own collections.
   One read gets you the whole configuration.
2. **The configuration contains no storage paths.** Nothing in a project says where its
   data ended up; that is recorded separately, at ingestion, and added back when the API
   serves the project. Which is what lets the same YAML file be ingested on a laptop and
   on a cluster without editing a line of it.

---

## The two shapes of a project

[![The two shapes of a project](../images/data-model/project-shape_light.png#only-light)](../images/data-model/project-shape_light.png){target=_blank}

[![The two shapes of a project](../images/data-model/project-shape_dark.png#only-dark)](../images/data-model/project-shape_dark.png){target=_blank}

| | Structure | Typical use |
| --- | --- | --- |
| **`advanced`** | Project :material-arrow-right: Workflow :material-arrow-right: DataCollection | Pipeline output. Defined in a YAML file and ingested by the CLI. |
| **`basic`** | Project :material-arrow-right: DataCollection | A few files you want on a dashboard. Created in the web UI, or with the CLI. |

Nothing else changes between the two. The same data collection types, joins, links,
permissions and dashboards apply either way. The workflow layer only exists to answer
"which pipeline produced this, and in which of its runs".

The word **workflow** is used in the sense [nf-core](https://nf-co.re/) and
[WorkflowHub](https://workflowhub.eu/) use it: the pipeline definition, not a particular
execution of it. Executions are **runs**, and they are the subject of the next section.

---

## How files become dashboard data

[![How files become dashboard data](../images/data-model/files-to-data_light.png#only-light)](../images/data-model/files-to-data_light.png){target=_blank}

[![How files become dashboard data](../images/data-model/files-to-data_dark.png#only-dark)](../images/data-model/files-to-data_dark.png){target=_blank}

A **run** is one execution of a workflow: an output folder, produced by processing one or
many samples. Re-running a pipeline adds a run rather than replacing one, so a project
accumulates runs over time.

Each run's output folder is scanned, and every matching file becomes a **File** record
holding its path, size and checksum. A **data collection** then gathers every file of the
same type, across every run, into the one thing a dashboard reads. The checksum is what
keeps re-ingestion incremental: an unchanged file is recognised and skipped rather than
processed again.

What that "one thing" is depends on the type, and it is not always a table. Tabular data
gets a [Delta Lake](https://delta.io/) table on S3, because Delta is what turns a
re-ingestion into an append with history rather than an overwrite. A MultiQC report gets
its parsed data copied as Parquet, a GeoJSON file is copied unchanged, and a phylogeny is
not copied at all: the tree is read from wherever the scan found it. The
[types table](#data-collection-types) below has the full mapping.

None of those destinations appear in the project you configured. For table-like
collections the location and the schema of each aggregation live in a separate
`deltatables` document; for the rest they are recorded on the file entries. Either way the
API joins them in as it serves the project, which is why `delta_location` and
`last_aggregation` show up in API responses and nowhere in your YAML.

---

## Data collection types

| | Type | Content | Materialised as |
| --- | --- | --- | --- |
| :material-table: | `table` | Tabular data: CSV, TSV, Parquet, Excel | A Delta Lake table on S3 |
| :material-image-multiple: | `image` | Image files | A Delta Lake table whose `image_column` holds the S3 paths |
| ![MultiQC](../images/logos/multiqc_light.svg#only-light){ width="18" }![MultiQC](../images/logos/multiqc_dark.svg#only-dark){ width="18" } | `multiqc` | MultiQC report data | The report's parsed data, as Parquet on S3 |
| :material-map-marker: | `geojson` | GeoJSON boundaries for choropleth maps | The file, copied to S3 unchanged |
| :material-family-tree: | `phylogeny` | Newick or Nexus trees | Nothing. The file is read where it was found |

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

Two mechanisms that sound alike and behave nothing alike. The difference that matters most
is *when* and *to what* each one applies:

- A **JoinDefinition** (`Project.joins`) runs in the CLI, at ingestion. It reads two Delta
  tables, merges them on shared columns (`left_dc`, `right_dc`, `on_columns`, `how`, plus a
  granularity policy) and writes the result to S3 as a new data collection with
  `source: joined`. Because it merges rows, it only works between `table` collections.
- A **DCLink** (`Project.links`) merges nothing and writes nothing. It runs in the
  dashboard, at render time, propagating *filters* from one data collection to another and
  resolving identifiers between them by one of several strategies (`direct`,
  `sample_mapping`, `pattern`, `regex`, `wildcard`). Since it only has to translate
  identifiers, it works across types: a selection on a metadata table can narrow a MultiQC
  report and an image gallery at the same time.

Use a join when you want one table. Use a link when you want to keep several things
separate and filter them together. [Cross-DC Filtering](cross-dc-filtering.md) covers the
resolver strategies in depth.

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

A project also carries an `is_public` flag, which is what opens it to readers with no
account. See [Authentication Modes](../usage/guides/authentication-modes.md) for how that
interacts with anonymous and unauthenticated deployments.

---

## Related Documentation

- :material-sitemap: [Architecture](architecture.md) - Microservices stack and data flow
- :material-filter: [Cross-DC Filtering](cross-dc-filtering.md) - DCLink resolver strategies in depth
- :material-sync: [YAML Dashboard Sync](yaml-sync.md) - Declarative dashboard export and import
- :material-code-braces: [Contributing](../developer/contributing.md) - How to extend the platform
