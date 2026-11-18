# Roadmap

Three sections, one question each:

- **[Shipped](#shipped)**

  ______________________________________________________________________

  Released and documented. Use it today.

- **[In progress](#in-progress)**

  ______________________________________________________________________

  Open pull requests, grouped by theme.

- **[Ideas](#ideas)**

  ______________________________________________________________________

  Wanted, not scheduled. No commitment.

How to read this page

Every dated claim below is traceable to the [changelog](https://depictio.github.io/depictio-docs/latest/changelog/index.md), which is also where you will find the current release. Dates are deliberately absent from *In progress* and *Ideas*: the pull request is the honest status, an estimate would not be.

______________________________________________________________________

## Big Picture

Foundations

→ v1.0.0 ✅

Dashboards, YAML-defined projects, Delta Lake ingestion, MultiQC and specialized components

React viewer

v1.0.0 ✅

Vite + Mantine SPA becomes the sole frontend on canonical URLs; Dash removed

Live data & access

v1.1.x ✅

Real-time dashboard events over WebSocket, magic-link login, pipeline provisioning

Operability

v1.2.x ✅

Admin Log & Task monitoring, per-phase ingestion detail, pinned timeline footer

Performance

v1.3.0 ✅

Lazy panel loading, bounded payloads, query pushdown, benchmark harness

Dashboard structure

v1.4.0 ✅

Dashboard sections, a dashboard-wide map panel, ten new card layouts

Cross-tab structure & selections

v1.6.0 – v1.7.0 ✅

Sections and filters that live on every tab, named selection groups, the Analysis panel, funnel filtering

Identity & exploration

v1.8.x ✅

Instance and dashboard brand themes, a navigable phylogeny, run provenance from the pipeline

Authoring & the catalog

v1.9.0 ✅

In-app catalog picker, Tool Studio for contributing a tool, `use:` provenance on a component

Backup & restore

v1.9.0 ✅

Backups created, validated and restored from the admin panel, scheduled, with a retention policy

Pipeline-triggered ingestion

v1.10.0 ✅

A Nextflow pipeline ingests its own results when it finishes

Versioning & the ingestion watcher

v1.15.0 ✅

Dataset and dashboard versioning, time travel, a watcher that re-ingests on its own

Data where it lives, dashboards from a run

v1.16.0 ✅

Run folders read on S3, projects created from a folder in the web UI, and a dashboard composed from whatever the catalog recognises

Embedding & the Paper look

v1.17.x ✅

A component embedded in another site, the Paper look, Account settings, viewers who comment

Groups, SAML & shareable filters

v1.18.0 ✅

User groups, SAML 2.0 sign-in, filters that are remembered and travel as a link

Proteins & linked views

v1.19.x ✅

Protein tiles linked by residue, structures from AlphaFold DB, a section's tiles on one screen

Genome browser

v1.20.0 ✅

An embedded JBrowse 2 view, linked to the dashboard both ways, in 16 nf-core templates

Projects from the data & what's new

v1.21.0 ✅

Projects start from their data, a project builder, runs compared, what changed since your last visit, projects sent between instances

Imaging, AI & serverless

In progress 🚧

Bioimage collections, an AI assistant and MCP agents, a dashboard as a single file

Ideas

Unscheduled 💡

Journeys through tabs, citable DOI snapshots, Galaxy, Snakemake and WorkflowHub, a central Depictio

______________________________________________________________________

## Shipped

One row per capability, newest first, in sections that open on click. The [feature docs](https://depictio.github.io/depictio-docs/latest/features/index.md) are the reference; these tables only say *when* something arrived.

v1.21: projects from the data, what's new, runs compared, Send / Receive

| Capability                                                                                                   | Since   | Docs                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Changed since your last visit: What's new, Overlay and Split, Before / Now, a notifications bell             | v1.21.0 | [*"What's new"*](https://depictio.github.io/depictio-docs/latest/features/whats-new/index.md)                                                                                                 |
| Runs compared: what each run produced and each scan changed, MultiQC split on the new samples                | v1.21.0 | [Runs and run comparison](https://depictio.github.io/depictio-docs/latest/features/runs/index.md) · [MultiQC](https://depictio.github.io/depictio-docs/latest/features/multiqc/#compare-runs) |
| A project starts from its data, with no Basic or Advanced choice; a Project Builder for your own collections | v1.21.0 | [Create a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#create-a-project)                                                                                    |
| Sample labels from the dashboard, saved to the table or exported as a sheet                                  | v1.21.0 | [Metadata panel](https://depictio.github.io/depictio-docs/latest/features/metadata-panel/index.md)                                                                                            |
| A project sent to another instance with an invite code, served read-only there                               | v1.21.0 | [Send to another instance](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/#send-to-another-instance)                                                            |
| OpenID Connect sign-in                                                                                       | v1.21.0 | [Single sign-on](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md)                                                                                                   |

v1.17 to v1.20: embedding, groups and SAML, proteins, the genome browser

| Capability                                                                                                       | Since   | Docs                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| An embedded genome browser (JBrowse 2) that filters the dashboard and is filtered by it, in 16 nf-core templates | v1.20.0 | [Genome browser](https://depictio.github.io/depictio-docs/latest/features/genome-browser/index.md)                                                                                                          |
| Eleven more nf-core templates documented, 43 in all                                                              | v1.20.0 | [Pipeline Templates](https://depictio.github.io/depictio-docs/latest/pipeline-templates/index.md)                                                                                                           |
| Option cards: a SegmentedControl drawn as cards                                                                  | v1.19.2 | [Option cards](https://depictio.github.io/depictio-docs/latest/features/components/#option-cards)                                                                                                           |
| Scope banner on one-unit tabs, linked views, zoom synced across residue tiles                                    | v1.19.1 | [Scope banner](https://depictio.github.io/depictio-docs/latest/features/dashboards/#scope-banner) · [Linked view](https://depictio.github.io/depictio-docs/latest/features/dashboards/#linked-view)         |
| Protein tiles linked by residue, with structures from the run, AlphaFold DB or ESMFold                           | v1.19.0 | [Proteins](https://depictio.github.io/depictio-docs/latest/features/proteins/index.md)                                                                                                                      |
| Add user: an administrator creates an account with an initial password                                           | v1.19.0 | [Adding a user](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#add-a-user)                                                                                                            |
| SAML 2.0 sign-in, with groups from the identity provider                                                         | v1.18.0 | [Single sign-on (SAML)](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md)                                                                                                          |
| User groups: share a project with a whole lab                                                                    | v1.18.0 | [Groups](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/index.md)                                                                                                              |
| Remembered filters, and filter links that carry the active filters                                               | v1.18.0 | [Remembered filters](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_usage/#remembered-filters)                                                                                      |
| Viewers may comment                                                                                              | v1.17.2 | [Viewers can comment](https://depictio.github.io/depictio-docs/latest/features/comments-annotations/#viewers-can-comment)                                                                                   |
| A component embedded in another site, as a Plotly spec or a self-contained page                                  | v1.17.0 | [Component export and embedding](https://depictio.github.io/depictio-docs/latest/features/component-export/index.md)                                                                                        |
| The Paper look, Account settings, a sectioned Administration page                                                | v1.17.0 | [Paper and Classic](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#looks) · [Account settings](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#account-settings) |

v1.13 to v1.16: comments, versioning, the watcher, data where it lives

| Capability                                                                                                                                                                            | Since   | Docs                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A dashboard composed from what the tools catalog recognises in a results directory, the way MultiQC builds its report                                                                 | v1.16.0 | [Composed dashboards](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md)                                                                                                                                            |
| Data read where it is: an `s3://` run folder, a URL, a bucket prefix or a data manifest; projects created from a run folder in the web UI, refreshed in place, exported as a template | v1.16.0 | [Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md) · [Export a project as a template](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#export-a-project-as-a-template) |
| Dashboard version history: bookmarks, read-only previews, restoring a dashboard or one component                                                                                      | v1.15.0 | [Dashboard and data versions](https://depictio.github.io/depictio-docs/latest/features/versioning/#history) · [Component history](https://depictio.github.io/depictio-docs/latest/features/versioning/#component-history)                                     |
| Every write a Delta commit; dashboards, previews and datasets read as a past commit wrote them                                                                                        | v1.15.0 | [Data versions](https://depictio.github.io/depictio-docs/latest/features/versioning/#data-versions)                                                                                                                                                           |
| `depictio watch` re-ingests on its own, with a Watchers pane and live ingestion steps                                                                                                 | v1.15.0 | [Watch Command](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#watch-command) · [Monitoring](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/#watchers)                                                  |
| Ingestion history on the project page, and an ingestion started from the browser                                                                                                      | v1.15.0 | [Ingestion history](https://depictio.github.io/depictio-docs/latest/features/dashboards/#ingestion-history) · [Run ingestion](https://depictio.github.io/depictio-docs/latest/features/dashboards/#run-ingestion)                                             |
| Landing tabs: block markdown, tab links, filter bars, minimal figures, a phylogeny summary                                                                                            | v1.14.0 | [Landing tabs](https://depictio.github.io/depictio-docs/latest/features/dashboards/#landing-tabs)                                                                                                                                                             |
| A built-in Guide on every dashboard                                                                                                                                                   | v1.14.0 | [The dashboard Guide](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/index.md)                                                                                                                                                  |
| Search every component of every tab with ⌘K                                                                                                                                           | v1.14.0 | [Spotlight search](https://depictio.github.io/depictio-docs/latest/usage/guides/spotlight-search/index.md)                                                                                                                                                    |
| Comments and annotations on dashboard components, with agent proposals held for review                                                                                                | v1.13.0 | [Comments and Annotations](https://depictio.github.io/depictio-docs/latest/features/comments-annotations/index.md)                                                                                                                                            |
| Thirteen more nf-core templates, ten advanced visualization kinds including a GenomeSpy genome view                                                                                   | v1.13.0 | [Pipeline Templates](https://depictio.github.io/depictio-docs/latest/pipeline-templates/index.md) · [Components](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#genome-view)                                               |
| Genome regions carried between collections, record cards that follow a selection                                                                                                      | v1.13.0 | [Cross-DC Filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/#region-links) · [Interactive Selection Filtering](https://depictio.github.io/depictio-docs/latest/features/interactive-selection-filtering/#record-cards)   |

v1.9 to v1.12: the catalog, backups, the Nextflow trigger, a pip-installable server

| Capability                                                                                     | Since   | Docs                                                                                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The full server installed as a Python package, no containers: `depictio local up`              | v1.12.0 | [Python package](https://depictio.github.io/depictio-docs/latest/installation/local/index.md)                                                                                                                           |
| One `depictio` package, `depictio ingest <results dir>`, refreshes that keep edited dashboards | v1.12.0 | [Ingest Command](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#ingest-command) · [Refreshing a project](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#refreshing-a-project) |
| Recipes declare the schema of their inputs and their output, checked around the transform      | v1.12.0 | [Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/#the-5-checkpoint-validation-pipeline)                                                                                                 |
| SeaweedFS as the bundled S3 store, replacing MinIO                                             | v1.12.0 | [Upgrading to v1.12.0](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/index.md)                                                                                                 |
| An opt-in feedback link that carries the dashboard and tab                                     | v1.11.0 | [Feedback](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#feedback)                                                                                                                        |
| The funnel overview follows the values of one column                                           | v1.11.0 | [Funnel filtering](https://depictio.github.io/depictio-docs/latest/features/dashboards/#funnel-filtering)                                                                                                               |
| Ingestion triggered by the pipeline itself, when it completes                                  | v1.10.0 | [Nextflow trigger](https://depictio.github.io/depictio-docs/latest/workflows/nextflow/trigger/index.md)                                                                                                                 |
| A run directory identifies its own pipeline, so a template needs no flag                       | v1.10.0 | [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#pipeline-id)                                                                                                                      |
| nf-core/variantbenchmarking template and benchmarking viz kinds                                | v1.10.0 | [variantbenchmarking](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/variantbenchmarking/index.md)                                                                                          |
| Backups created, scheduled and restored from the admin panel                                   | v1.9.0  | [Backup & Restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/#from-the-admin-panel)                                                                                                   |
| Pick a component from the catalog, with `use:` provenance on it                                | v1.9.0  | [Picking from the catalog](https://depictio.github.io/depictio-docs/latest/usage/guides/catalog-picker/index.md)                                                                                                        |
| Tool Studio: contribute a catalog tool from the browser                                        | v1.9.0  | [Tool Studio](https://depictio.github.io/depictio-docs/latest/developer/tool-studio/index.md)                                                                                                                           |

v1.0 to v1.8: the React viewer, real-time events, sections, themes

| Capability                                                                  | Since           | Docs                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Run provenance, a real tab header, per-section grid packing                 | v1.8.3          | [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#run-provenance) · [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/#dashboard-tabs)                                         |
| Password sign-in disabled, shared code for public mode                      | v1.8.2          | [Authentication Modes](https://depictio.github.io/depictio-docs/latest/usage/guides/authentication-modes/index.md)                                                                                                                                |
| Instance and dashboard brand themes, a navigable phylogeny                  | v1.8.0          | [Branding](https://depictio.github.io/depictio-docs/latest/usage/administration/branding/index.md) · [Components](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#phylogenetic)                                 |
| Selection groups, the Analysis panel, funnel filtering                      | v1.7.0          | [Interactive Selection Filtering](https://depictio.github.io/depictio-docs/latest/features/interactive-selection-filtering/#analysis-panel) · [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/#funnel-filtering) |
| Sections and filters that span every tab of a dashboard                     | v1.6.0          | [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/#persistent-sections) · [YAML Sync](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/#persistent-sections)                                     |
| Filters carried into the component builder, bucket-scoped S3 startup        | v1.5.2          | [Dashboard creation](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/#previewing-with-active-filters-v152)                                                                                                        |
| Cross-version backup compatibility guard                                    | v1.5.2          | [Backup & Restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/#restoring-across-versions)                                                                                                                        |
| Anonymous installation telemetry                                            | v1.5.0          | [Telemetry](https://depictio.github.io/depictio-docs/latest/features/telemetry/index.md)                                                                                                                                                          |
| Dashboard sections, dashboard-wide map panel, ten new card layouts          | v1.4.0          | [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/#sections) · [Components](https://depictio.github.io/depictio-docs/latest/features/components/#dashboard-wide-map-panel)                                         |
| Lazy panel loading, bounded payloads, *Load all*, benchmark harness         | v1.3.0          | [Performance & Scaling](https://depictio.github.io/depictio-docs/latest/features/performance/index.md)                                                                                                                                            |
| Pinned timeline footer, compact tables                                      | v1.2.2          | [YAML Sync](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md)                                                                                                                                                          |
| Admin **Log & Task** monitoring, per-phase ingestion detail, run provenance | v1.2.0 – v1.2.1 | [Monitoring](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/index.md)                                                                                                                                            |
| Real-time dashboard events over WebSocket                                   | v1.1.4          | [Real-time Events](https://depictio.github.io/depictio-docs/latest/usage/guides/realtime-events/index.md)                                                                                                                                         |
| Passwordless magic-link login, pipeline provisioning                        | v1.1.3          | [Authentication Modes](https://depictio.github.io/depictio-docs/latest/usage/guides/authentication-modes/index.md)                                                                                                                                |
| Cross-DC linking UI, ingestion reports, self-adapting nf-core templates     | v1.1.0          | [Cross-DC Filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md)                                                                                                                                        |
| React viewer as sole frontend on canonical URLs                             | v1.0.0          | [Dashboards](https://depictio.github.io/depictio-docs/latest/features/dashboards/index.md)                                                                                                                                                        |
| Tools catalog: tool outputs become dashboard components                     | v1.0.0          | [Catalog](https://depictio.github.io/depictio-docs/latest/catalog/index.md)                                                                                                                                                                       |

v0.x: the foundations

| Capability                                                       | Since   | Docs                                                                                                                                                                                        |
| ---------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Advanced biology visualizations (volcano, Manhattan, sunburst…)  | v0.13.0 | [Components](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/index.md)                                                                                     |
| MultiQC data lifecycle, DC-level type config                     | v0.12.0 | [Projects Guide](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md)                                                                                             |
| Templates & recipes: one-command project setup                   | v0.10.0 | [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md) · [Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md) |
| Geospatial maps, choropleth & GeoJSON collections                | v0.8.0  | [Components](https://depictio.github.io/depictio-docs/latest/features/components/#map-components)                                                                                           |
| MultiQC report integration                                       | v0.5.0  | [Components](https://depictio.github.io/depictio-docs/latest/features/components/#multiqc-components)                                                                                       |
| YAML-defined projects & dashboards, Delta Lake ingestion via CLI | v0.0.5  | [CLI Usage](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md) · [YAML Sync](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md)         |
| Docker Compose & Kubernetes/Helm deployment                      | v0.0.5  | [Installation](https://depictio.github.io/depictio-docs/latest/installation/docker/index.md)                                                                                                |

______________________________________________________________________

## In progress

Grouped by theme. Each item links the pull request that implements it, so its real state is always one click away. The catalog picker, Tool Studio and composed dashboards that lowered the cost of a project have shipped.

### Projects and data

| Item                           | What it would give you                                                   | Pull request                                            |
| ------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------- |
| **Project builder**            | Define the collections of a project yourself, on a server or without one | [#1182](https://github.com/depictio/depictio/pull/1182) |
| **YAML and JSON samplesheets** | Samplesheets in YAML or JSON, next to the CSV and TSV ones               | [#1289](https://github.com/depictio/depictio/pull/1289) |
| **Google Cloud Storage**       | Read pipeline results from a GCS bucket through its S3 API               | [#1291](https://github.com/depictio/depictio/pull/1291) |

### Imaging and spatial

| Item                              | What it would give you                                                                         | Pull request                                            |
| --------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Bioimage collections**          | A data collection and a viewer tile for OME-TIFF and SpatialData, with four example dashboards | [#1118](https://github.com/depictio/depictio/pull/1118) |
| **Stores read in place**          | OME-TIFF, SpatialData images and zarr v3 / NGFF 0.5, read where they are                       | [#1121](https://github.com/depictio/depictio/pull/1121) |
| **SpatialData tables**            | Table collections read straight from a SpatialData store                                       | [#1122](https://github.com/depictio/depictio/pull/1122) |
| **Imaging and spatial templates** | nf-core templates built on the bioimage module (draft)                                         | [#1134](https://github.com/depictio/depictio/pull/1134) |

### AI and agents

| Item                     | What it would give you                                                                                 | Pull request                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| **AI assistant**         | Opt-in dashboard chat, component generation, typed suggestions and budgeted read-only analysis reports | [#964](https://github.com/depictio/depictio/pull/964)   |
| **Generated dashboards** | A whole dashboard from a project, reviewed tile by tile, every generated component checked             | [#1028](https://github.com/depictio/depictio/pull/1028) |
| **MCP server**           | Scoped tokens and in-app agent teams (draft)                                                           | [#1125](https://github.com/depictio/depictio/pull/1125) |

### Export and sharing

| Item                      | What it would give you                                          | Pull request                                            |
| ------------------------- | --------------------------------------------------------------- | ------------------------------------------------------- |
| **Single-file dashboard** | A dashboard that opens without Depictio, deployed as one file   | [#963](https://github.com/depictio/depictio/pull/963)   |
| **Notebook and Quarto**   | A dashboard as a notebook, and a Quarto report rendered for you | [#1034](https://github.com/depictio/depictio/pull/1034) |

______________________________________________________________________

## Ideas

Wanted, discussed, not scheduled. Nothing here has a date, and some of it will never be built. Open or upvote an [issue](https://github.com/depictio/depictio/issues) to push something up.

### Data and storage

| Idea                               | What it would give you                                                                                            | Link                                                                                                                                                                            |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Optional samplesheets**          | A template that rebuilds its sample table from the run results when the pipeline does not publish the samplesheet | [#1321](https://github.com/depictio/depictio/issues/1321)                                                                                                                       |
| **Cloud storage for the instance** | GCS as the instance's own store, not only a source, and a storage choice per project                              | [#1298](https://github.com/depictio/depictio/issues/1298) · [#383](https://github.com/depictio/depictio/issues/383) · [#1282](https://github.com/depictio/depictio/issues/1282) |
| **Dashboard parameters**           | Pick a value, such as the taxonomic rank to merge two runs at, and let computed columns follow it                 | [#1138](https://github.com/depictio/depictio/issues/1138)                                                                                                                       |

### Figures and filters

| Idea                                  | What it would give you                                                                                                                                                                                                                                                                                                                    | Link                                                                                                                                                                      |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Figure axes and sorting**           | Custom axis order (chromosomes in their natural order) and numerical or categorical sorting                                                                                                                                                                                                                                               | [#361](https://github.com/depictio/depictio/issues/361) · [#360](https://github.com/depictio/depictio/issues/360)                                                         |
| **Filters that know the result set**  | Choose between all values and those still available, and restrict a picker to the current result set                                                                                                                                                                                                                                      | [#278](https://github.com/depictio/depictio/issues/278) · [#327](https://github.com/depictio/depictio/issues/327)                                                         |
| **Datawrapper-style reading quality** | The authoring touches a chart tool takes for granted, ranked by interest and difficulty                                                                                                                                                                                                                                                   | [#1106](https://github.com/depictio/depictio/issues/1106)                                                                                                                 |
| **Charts for very large point sets**  | A WebGL renderer that stays flat from 10 thousand to 100 million points                                                                                                                                                                                                                                                                   | [#945](https://github.com/depictio/depictio/issues/945)                                                                                                                   |
| **OME-Zarr viewer**                   | Pyramidal imaging in an advanced visualization, with an eye on Vitessce                                                                                                                                                                                                                                                                   | [#1086](https://github.com/depictio/depictio/issues/1086)                                                                                                                 |
| **A lighter map location control**    | Collapsible controls in a popover, better default size                                                                                                                                                                                                                                                                                    | [#930](https://github.com/depictio/depictio/issues/930)                                                                                                                   |
| **Journeys**                          | Named paths through tabs. The two halves of this idea already shipped: filters promoted to dashboard scope in [v1.6.0](https://depictio.github.io/depictio-docs/latest/features/dashboards/#persistent-sections), and [funnel filtering](https://depictio.github.io/depictio-docs/latest/features/dashboards/#funnel-filtering) in v1.7.0 | [#756](https://github.com/depictio/depictio/pull/756) · [#690](https://github.com/depictio/depictio/issues/690) · [#691](https://github.com/depictio/depictio/issues/691) |
| ### Reports and citable science       |                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                           |

| Idea                                   | What it would give you                                                                                                                                                                                                                       | Link                                                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Report while exploring**             | Assemble what you find into a report with a live Quarto preview, no re-execution                                                                                                                                                             | [#1148](https://github.com/depictio/depictio/issues/1148)                                                           |
| **Citable science**                    | Immutable, DOI-citable app releases on the public EMBL instance, and sample-to-viz provenance via [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/). A [Quarto](https://quarto.org/) export is [in progress](#export-and-sharing) | [#1303](https://github.com/depictio/depictio/issues/1303) · [#931](https://github.com/depictio/depictio/issues/931) |
| ### Workflow ecosystems and publishing |                                                                                                                                                                                                                                              |                                                                                                                     |

| Idea                                        | What it would give you                                                                                             | Link                                                      |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| **Galaxy**                                  | The results of a Galaxy workflow shown as a Depictio dashboard                                                     | *none yet*                                                |
| **Snakemake report plugin**                 | Depictio as a drop-in replacement for Snakemake's static HTML report                                               | *none yet*                                                |
| **WorkflowHub**                             | A dashboard template registered beside the workflow it reads, so the two are found and cited together              | *none yet*                                                |
| **A central Depictio**                      | One shared instance for a lab or an institute, that projects from local instances are sent to                      | *none yet*                                                |
| **Push to the public instance from the UI** | Publish a project and its dashboards to the public EMBL instance from the web UI, not only with `depictio migrate` | [#1303](https://github.com/depictio/depictio/issues/1303) |

### Agents

| Idea                                           | What it would give you                                                                                      | Link                                                                                                                                                                            |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **One interface for agents and the in-app AI** | Create data, dashboards and templates together, driven by the authoring rules, with an MCP use-case catalog | [#1315](https://github.com/depictio/depictio/issues/1315) · [#1087](https://github.com/depictio/depictio/issues/1087) · [#844](https://github.com/depictio/depictio/issues/844) |

### Running an instance

| Idea                  | What it would give you                                                 | Link                                                      |
| --------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------- |
| **Admin usage panel** | Visitors, sessions and top dashboards, from the opt-in analytics       | [#1293](https://github.com/depictio/depictio/issues/1293) |
| **Tags**              | Tags on projects and on dashboards                                     | [#857](https://github.com/depictio/depictio/issues/857)   |
| **Component groups**  | Group components and give a data collection a view shared by the group | [#308](https://github.com/depictio/depictio/issues/308)   |

______________________________________________________________________

## Reproducibility & FAIR

Depictio is built with the [FAIR principles](https://www.go-fair.org/fair-principles/) in mind. Most of the reproducibility story is shipped; citability is not.

| Challenge                                  | Status                                                                                                                                                                                                                                                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reproducing a setup takes manual work      | nf-core templates, one-command project setup ([docs](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md))                                                                                                                                                                      |
| A visualization can't be reproduced        | YAML-defined dashboards over traceable data ([docs](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md))                                                                                                                                                                             |
| Experiment data sits in silos              | Cross-DC linking ([docs](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md))                                                                                                                                                                                               |
| Dashboards disappear                       | Hosted on [SciLifeLab Serve](https://serve.scilifelab.se/)                                                                                                                                                                                                                                                    |
| No data lineage                            | [Run provenance](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#run-provenance) records the parameters a run used; each table write is a Delta commit that a dashboard can be read at ([docs](https://depictio.github.io/depictio-docs/latest/features/versioning/#data-versions)) |
| Not citable, no sample-to-viz traceability | DOI snapshots + LabID provenance: [an idea](#ideas)                                                                                                                                                                                                                                                           |

______________________________________________________________________

## Get involved

- [Issues](https://github.com/depictio/depictio/issues): feature requests and bug reports
- [Pull requests](https://github.com/depictio/depictio/pulls): everything under *In progress*, live
- [Contributing Guide](https://depictio.github.io/depictio-docs/latest/developer/contributing/index.md): setup, conventions, how to add a tool
