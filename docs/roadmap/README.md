---
title: "Roadmap"
icon: material/chart-timeline
description: "What Depictio has shipped, what is being built right now, and what is only an idea."
hide:
  - navigation
---

# Roadmap

Three sections, one question each:

<div class="grid cards roadmap-nav" markdown>

-   :material-check-circle:{ .lg .middle .rn-shipped } **[Shipped](#shipped)**

    ---

    Released and documented. Use it today.

-   :material-progress-wrench:{ .lg .middle .rn-progress } **[In progress](#in-progress)**

    ---

    Open pull requests, grouped by theme.

-   :material-lightbulb-outline:{ .lg .middle .rn-idea } **[Ideas](#ideas)**

    ---

    Wanted, not scheduled. No commitment.

</div>

!!! info "How to read this page"
    Every dated claim below is traceable to the [changelog](../changelog/README.md),
    which is also where you will find the current release.
    Dates are deliberately absent from *In progress* and *Ideas*: the pull request is
    the honest status, an estimate would not be.

---

## Big Picture

::timeline:: class="depictio-roadmap" center alternate

- title: "Foundations"
  content: "Dashboards, YAML-defined projects, Delta Lake ingestion, MultiQC and specialized components"
  icon: ":fontawesome-solid-chart-line:"
  key: "completed"
  sub_title: "→ v1.0.0 ✅"

- title: "React viewer"
  content: "Vite + Mantine SPA becomes the sole frontend on canonical URLs; Dash removed"
  icon: ":fontawesome-brands-react:"
  key: "completed"
  sub_title: "v1.0.0 ✅"

- title: "Live data & access"
  content: "Real-time dashboard events over WebSocket, magic-link login, pipeline provisioning"
  icon: ":fontawesome-solid-bolt:"
  key: "completed"
  sub_title: "v1.1.x ✅"

- title: "Operability"
  content: "Admin Log & Task monitoring, per-phase ingestion detail, pinned timeline footer"
  icon: ":fontawesome-solid-gauge-high:"
  key: "completed"
  sub_title: "v1.2.x ✅"

- title: "Performance"
  content: "Lazy panel loading, bounded payloads, query pushdown, benchmark harness"
  icon: ":fontawesome-solid-rocket:"
  key: "completed"
  sub_title: "v1.3.0 ✅"

- title: "Dashboard structure"
  content: "Dashboard sections, a dashboard-wide map panel, ten new card layouts"
  icon: ":fontawesome-solid-layer-group:"
  key: "completed"
  sub_title: "v1.4.0 ✅"

- title: "Cross-tab structure & selections"
  content: "Sections and filters that live on every tab, named selection groups, the Analysis panel, funnel filtering"
  icon: ":fontawesome-solid-object-group:"
  key: "completed"
  sub_title: "v1.6.0 – v1.7.0 ✅"

- title: "Identity & exploration"
  content: "Instance and dashboard brand themes, a navigable phylogeny, run provenance from the pipeline"
  icon: ":fontawesome-solid-palette:"
  key: "completed"
  sub_title: "v1.8.x ✅"

- title: "Authoring & the catalog"
  content: "In-app catalog picker, Tool Studio for contributing a tool, `use:` provenance on a component"
  icon: ":fontawesome-solid-screwdriver-wrench:"
  key: "completed"
  sub_title: "v1.9.0 ✅"

- title: "Backup & restore"
  content: "Backups created, validated and restored from the admin panel, scheduled, with a retention policy"
  icon: ":fontawesome-solid-box-archive:"
  key: "completed"
  sub_title: "v1.9.0 ✅"

- title: "Pipeline-triggered ingestion"
  content: "A Nextflow pipeline ingests its own results when it finishes"
  icon: ":fontawesome-solid-bolt:"
  key: "completed"
  sub_title: "v1.10.0 ✅"

- title: "Versioning & the ingestion watcher"
  content: "Dataset and dashboard versioning, time travel, a watcher that re-ingests on its own"
  icon: ":fontawesome-solid-clock-rotate-left:"
  key: "completed"
  sub_title: "v1.15.0 ✅"

- title: "Data where it lives, dashboards from a run"
  content: "Run folders read on S3, projects created from a folder in the web UI, and a dashboard composed from whatever the catalog recognises"
  icon: ":fontawesome-solid-wand-magic-sparkles:"
  key: "completed"
  sub_title: "v1.16.0 ✅"

- title: "Embedding & the Paper look"
  content: "A component embedded in another site, the Paper look, Account settings, viewers who comment"
  icon: ":fontawesome-solid-window-restore:"
  key: "completed"
  sub_title: "v1.17.x ✅"

- title: "Groups, SAML & shareable filters"
  content: "User groups, SAML 2.0 sign-in, filters that are remembered and travel as a link"
  icon: ":fontawesome-solid-users:"
  key: "completed"
  sub_title: "v1.18.0 ✅"

- title: "Proteins & linked views"
  content: "Protein tiles linked by residue, structures from AlphaFold DB, a section's tiles on one screen"
  icon: ":fontawesome-solid-dna:"
  key: "completed"
  sub_title: "v1.19.x ✅"

- title: "Genome browser"
  content: "An embedded JBrowse 2 view, linked to the dashboard both ways, in 16 nf-core templates"
  icon: ":fontawesome-solid-map-location-dot:"
  key: "completed"
  sub_title: "v1.20.0 ✅"

- title: "Imaging, AI & serverless"
  content: "Bioimage collections, an AI assistant and MCP agents, a dashboard as a single file, a project builder"
  icon: ":fontawesome-solid-hammer:"
  key: "inprogress"
  sub_title: "In progress 🚧"

- title: "Ideas"
  content: "Journeys through tabs, citable DOI snapshots, a Snakemake report plugin"
  icon: ":fontawesome-solid-lightbulb:"
  key: "idea"
  sub_title: "Unscheduled 💡"

::/timeline::

---

## :material-check-circle:{ .rn-shipped } Shipped

One row per capability, newest first, in sections that open on click. The
[feature docs](../features/README.md) are the reference; these tables only say *when*
something arrived.

???+ success "v1.17 to v1.20: embedding, groups and SAML, proteins, the genome browser"

    | Capability | Since | Docs |
    | ---------- | ----- | ---- |
    | An embedded genome browser (JBrowse 2) that filters the dashboard and is filtered by it, in 16 nf-core templates | v1.20.0 | [Genome browser](../features/genome-browser/index.md) |
    | Eleven more nf-core templates documented, 43 in all | v1.20.0 | [Pipeline Templates](../pipeline-templates/README.md) |
    | Option cards: a SegmentedControl drawn as cards | v1.19.2 | [Option cards](../features/components.md#option-cards) |
    | Scope banner on one-unit tabs, linked views, zoom synced across residue tiles | v1.19.1 | [Scope banner](../features/dashboards.md#scope-banner) · [Linked view](../features/dashboards.md#linked-view) |
    | Protein tiles linked by residue, with structures from the run, AlphaFold DB or ESMFold | v1.19.0 | [Proteins](../features/proteins.md) |
    | Add user: an administrator creates an account with an initial password | v1.19.0 | [Adding a user](../usage/guides/web_ui.md#add-a-user) |
    | SAML 2.0 sign-in, with groups from the identity provider | v1.18.0 | [Single sign-on (SAML)](../installation/sso.md) |
    | User groups: share a project with a whole lab | v1.18.0 | [Groups](../usage/administration/groups.md) |
    | Remembered filters, and filter links that carry the active filters | v1.18.0 | [Remembered filters](../usage/guides/dashboard_usage.md#remembered-filters) |
    | Viewers may comment | v1.17.2 | [Viewers can comment](../features/comments-annotations.md#viewers-can-comment) |
    | A component embedded in another site, as a Plotly spec or a self-contained page | v1.17.0 | [Component export and embedding](../features/component-export.md) |
    | The Paper look, Account settings, a sectioned Administration page | v1.17.0 | [Paper and Classic](../usage/guides/web_ui.md#looks) · [Account settings](../usage/guides/web_ui.md#account-settings) |

??? success "v1.13 to v1.16: comments, versioning, the watcher, data where it lives"

    | Capability | Since | Docs |
    | ---------- | ----- | ---- |
    | A dashboard composed from what the tools catalog recognises in a results directory, the way MultiQC builds its report | v1.16.0 | [Composed dashboards](../usage/projects/composed-dashboards.md) |
    | Data read where it is: an `s3://` run folder, a URL, a bucket prefix or a data manifest; projects created from a run folder in the web UI, refreshed in place, exported as a template | v1.16.0 | [Remote data and manifests](../usage/projects/remote-data.md) · [Export a project as a template](../usage/projects/templates.md#export-a-project-as-a-template) |
    | Dashboard version history: bookmarks, read-only previews, restoring a dashboard or one component | v1.15.0 | [Dashboard and data versions](../features/versioning.md#history) · [Component history](../features/versioning.md#component-history) |
    | Every write a Delta commit; dashboards, previews and datasets read as a past commit wrote them | v1.15.0 | [Data versions](../features/versioning.md#data-versions) |
    | `depictio watch` re-ingests on its own, with a Watchers pane and live ingestion steps | v1.15.0 | [Watch Command](../depictio-cli/usage.md#watch-command) · [Monitoring](../usage/administration/monitoring.md#watchers) |
    | Ingestion history on the project page, and an ingestion started from the browser | v1.15.0 | [Ingestion history](../features/dashboards.md#ingestion-history) · [Run ingestion](../features/dashboards.md#run-ingestion) |
    | Landing tabs: block markdown, tab links, filter bars, minimal figures, a phylogeny summary | v1.14.0 | [Landing tabs](../features/dashboards.md#landing-tabs) |
    | A built-in Guide on every dashboard | v1.14.0 | [The dashboard Guide](../usage/guides/dashboard-guide.md) |
    | Search every component of every tab with ⌘K | v1.14.0 | [Spotlight search](../usage/guides/spotlight-search.md) |
    | Comments and annotations on dashboard components, with agent proposals held for review | v1.13.0 | [Comments and Annotations](../features/comments-annotations.md) |
    | Thirteen more nf-core templates, ten advanced visualization kinds including a GenomeSpy genome view | v1.13.0 | [Pipeline Templates](../pipeline-templates/README.md) · [Components](../features/advanced-visualizations.md#genome-view) |
    | Genome regions carried between collections, record cards that follow a selection | v1.13.0 | [Cross-DC Filtering](../features/cross-dc-filtering.md#region-links) · [Interactive Selection Filtering](../features/interactive-selection-filtering.md#record-cards) |

??? success "v1.9 to v1.12: the catalog, backups, the Nextflow trigger, a pip-installable server"

    | Capability | Since | Docs |
    | ---------- | ----- | ---- |
    | The full server installed as a Python package, no containers: `depictio local up` | v1.12.0 | [Python package](../installation/local.md) |
    | One `depictio` package, `depictio ingest <results dir>`, refreshes that keep edited dashboards | v1.12.0 | [Ingest Command](../depictio-cli/usage.md#ingest-command) · [Refreshing a project](../depictio-cli/usage.md#refreshing-a-project) |
    | Recipes declare the schema of their inputs and their output, checked around the transform | v1.12.0 | [Recipes](../usage/projects/recipes.md#the-5-checkpoint-validation-pipeline) |
    | SeaweedFS as the bundled S3 store, replacing MinIO | v1.12.0 | [Upgrading to v1.12.0](../installation/upgrade/v1.12.0-seaweedfs.md) |
    | An opt-in feedback link that carries the dashboard and tab | v1.11.0 | [Feedback](../installation/env-reference.md#feedback) |
    | The funnel overview follows the values of one column | v1.11.0 | [Funnel filtering](../features/dashboards.md#funnel-filtering) |
    | Ingestion triggered by the pipeline itself, when it completes | v1.10.0 | [Nextflow trigger](../depictio-cli/nextflow-trigger.md) |
    | A run directory identifies its own pipeline, so a template needs no flag | v1.10.0 | [Templates](../usage/projects/templates.md#pipeline-id) |
    | nf-core/variantbenchmarking template and benchmarking viz kinds | v1.10.0 | [variantbenchmarking](../pipeline-templates/nf-core/variantbenchmarking.md) |
    | Backups created, scheduled and restored from the admin panel | v1.9.0 | [Backup & Restore](../usage/administration/backup.md#from-the-admin-panel) |
    | Pick a component from the catalog, with `use:` provenance on it | v1.9.0 | [Picking from the catalog](../usage/guides/catalog-picker.md) |
    | Tool Studio: contribute a catalog tool from the browser | v1.9.0 | [Tool Studio](../developer/tool-studio.md) |

??? success "v1.0 to v1.8: the React viewer, real-time events, sections, themes"

    | Capability | Since | Docs |
    | ---------- | ----- | ---- |
    | Run provenance, a real tab header, per-section grid packing | v1.8.3 | [Templates](../usage/projects/templates.md#run-provenance) · [Dashboards](../features/dashboards.md#dashboard-tabs) |
    | Password sign-in disabled, shared code for public mode | v1.8.2 | [Authentication Modes](../usage/guides/authentication-modes.md) |
    | Instance and dashboard brand themes, a navigable phylogeny | v1.8.0 | [Branding](../usage/administration/branding.md) · [Components](../features/advanced-visualizations.md#phylogenetic) |
    | Selection groups, the Analysis panel, funnel filtering | v1.7.0 | [Interactive Selection Filtering](../features/interactive-selection-filtering.md#analysis-panel) · [Dashboards](../features/dashboards.md#funnel-filtering) |
    | Sections and filters that span every tab of a dashboard | v1.6.0 | [Dashboards](../features/dashboards.md#persistent-sections) · [YAML Sync](../features/yaml-sync.md#persistent-sections) |
    | Filters carried into the component builder, bucket-scoped S3 startup | v1.5.2 | [Dashboard creation](../usage/guides/dashboard_creation.md#previewing-with-active-filters-v152) |
    | Cross-version backup compatibility guard | v1.5.2 | [Backup & Restore](../usage/administration/backup.md#restoring-across-versions) |
    | Anonymous installation telemetry | v1.5.0 | [Telemetry](../features/telemetry.md) |
    | Dashboard sections, dashboard-wide map panel, ten new card layouts | v1.4.0 | [Dashboards](../features/dashboards.md#sections) · [Components](../features/components.md#dashboard-wide-map-panel) |
    | Lazy panel loading, bounded payloads, *Load all*, benchmark harness | v1.3.0 | [Performance & Scaling](../features/performance.md) |
    | Pinned timeline footer, compact tables | v1.2.2 | [YAML Sync](../features/yaml-sync.md) |
    | Admin **Log & Task** monitoring, per-phase ingestion detail, run provenance | v1.2.0 – v1.2.1 | [Monitoring](../usage/administration/monitoring.md) |
    | Real-time dashboard events over WebSocket | v1.1.4 | [Real-time Events](../usage/guides/realtime-events.md) |
    | Passwordless magic-link login, pipeline provisioning | v1.1.3 | [Authentication Modes](../usage/guides/authentication-modes.md) |
    | Cross-DC linking UI, ingestion reports, self-adapting nf-core templates | v1.1.0 | [Cross-DC Filtering](../features/cross-dc-filtering.md) |
    | React viewer as sole frontend on canonical URLs | v1.0.0 | [Dashboards](../features/dashboards.md) |
    | Tools catalog — tool outputs become dashboard components | v1.0.0 | [Catalog](../catalog/index.md) |

??? success "v0.x: the foundations"

    | Capability | Since | Docs |
    | ---------- | ----- | ---- |
    | Advanced biology visualizations (volcano, Manhattan, sunburst…) | v0.13.0 | [Components](../features/advanced-visualizations.md) |
    | MultiQC data lifecycle, DC-level type config | v0.12.0 | [Projects Guide](../usage/projects/guide.md) |
    | Templates & recipes — one-command project setup | v0.10.0 | [Templates](../usage/projects/templates.md) · [Recipes](../usage/projects/recipes.md) |
    | Geospatial maps, choropleth & GeoJSON collections | v0.8.0 | [Components](../features/components.md#map-components) |
    | MultiQC report integration | v0.5.0 | [Components](../features/components.md#multiqc-components) |
    | YAML-defined projects & dashboards, Delta Lake ingestion via CLI | v0.0.5 | [CLI Usage](../depictio-cli/usage.md) · [YAML Sync](../features/yaml-sync.md) |
    | Docker Compose & Kubernetes/Helm deployment | v0.0.5 | [Installation](../installation/docker.md) |

---

## :material-progress-wrench:{ .rn-progress } In progress

Grouped by theme. Each item links the pull request that implements it, so its
real state is always one click away. The catalog picker, Tool Studio and composed dashboards
that lowered the cost of a project have shipped.

### :material-folder-plus-outline: Projects and data

| Item | What it would give you | Pull request |
| ---- | ---------------------- | ------------ |
| :material-hammer-wrench: **Project builder** | Define the collections of a project yourself, on a server or without one | [#1182](https://github.com/depictio/depictio/pull/1182) |
| :material-file-code-outline: **YAML and JSON samplesheets** | Samplesheets in YAML or JSON, next to the CSV and TSV ones | [#1289](https://github.com/depictio/depictio/pull/1289) |
| :material-google-cloud: **Google Cloud Storage** | Read pipeline results from a GCS bucket through its S3 API | [#1291](https://github.com/depictio/depictio/pull/1291) |

### :material-microscope: Imaging and spatial

| Item | What it would give you | Pull request |
| ---- | ---------------------- | ------------ |
| :material-image-multiple-outline: **Bioimage collections** | A data collection and a viewer tile for OME-TIFF and SpatialData, with four example dashboards | [#1118](https://github.com/depictio/depictio/pull/1118) |
| :material-database-eye-outline: **Stores read in place** | OME-TIFF, SpatialData images and zarr v3 / NGFF 0.5, read where they are | [#1121](https://github.com/depictio/depictio/pull/1121) |
| :material-table-eye: **SpatialData tables** | Table collections read straight from a SpatialData store | [#1122](https://github.com/depictio/depictio/pull/1122) |
| :material-microscope: **Imaging and spatial templates** | nf-core templates built on the bioimage module (draft) | [#1134](https://github.com/depictio/depictio/pull/1134) |

### :material-robot-outline: AI and agents

| Item | What it would give you | Pull request |
| ---- | ---------------------- | ------------ |
| :material-chat-processing-outline: **AI assistant** | Opt-in dashboard chat, component generation, typed suggestions and budgeted read-only analysis reports | [#964](https://github.com/depictio/depictio/pull/964) |
| :material-auto-fix: **Generated dashboards** | A whole dashboard from a project, reviewed tile by tile, every generated component checked | [#1028](https://github.com/depictio/depictio/pull/1028) |
| :material-server-network: **MCP server** | Scoped tokens and in-app agent teams (draft) | [#1125](https://github.com/depictio/depictio/pull/1125) |

### :material-file-export-outline: Export and sharing

| Item | What it would give you | Pull request |
| ---- | ---------------------- | ------------ |
| :material-file-export-outline: **Single-file dashboard** | A dashboard that opens without Depictio, deployed as one file | [#963](https://github.com/depictio/depictio/pull/963) |
| :material-notebook-outline: **Notebook and Quarto** | A dashboard as a notebook, and a Quarto report rendered for you | [#1034](https://github.com/depictio/depictio/pull/1034) |

---

## :material-lightbulb-outline:{ .rn-idea } Ideas

Wanted, discussed, not scheduled. Nothing here has a date, and some of it will never be
built. Open or upvote an [issue](https://github.com/depictio/depictio/issues) to push
something up.

### :material-database-cog-outline: Data and storage

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-file-question-outline: **Optional samplesheets** | A template that rebuilds its sample table from the run results when the pipeline does not publish the samplesheet | [#1321](https://github.com/depictio/depictio/issues/1321) |
| :material-cloud-upload-outline: **Cloud storage for the instance** | GCS as the instance's own store, not only a source, and a storage choice per project | [#1298](https://github.com/depictio/depictio/issues/1298) · [#383](https://github.com/depictio/depictio/issues/383) · [#1282](https://github.com/depictio/depictio/issues/1282) |
| :material-tune-variant: **Dashboard parameters** | Pick a value, such as the taxonomic rank to merge two runs at, and let computed columns follow it | [#1138](https://github.com/depictio/depictio/issues/1138) |

### :material-chart-box-outline: Figures and filters

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-sort-variant: **Figure axes and sorting** | Custom axis order (chromosomes in their natural order) and numerical or categorical sorting | [#361](https://github.com/depictio/depictio/issues/361) · [#360](https://github.com/depictio/depictio/issues/360) |
| :material-filter-variant: **Filters that know the result set** | Choose between all values and those still available, and restrict a picker to the current result set | [#278](https://github.com/depictio/depictio/issues/278) · [#327](https://github.com/depictio/depictio/issues/327) |
| :material-palette-outline: **Datawrapper-style reading quality** | The authoring touches a chart tool takes for granted, ranked by interest and difficulty | [#1106](https://github.com/depictio/depictio/issues/1106) |
| :material-speedometer: **Charts for very large point sets** | A WebGL renderer that stays flat from 10 thousand to 100 million points | [#945](https://github.com/depictio/depictio/issues/945) |
| :material-image-search-outline: **OME-Zarr viewer** | Pyramidal imaging in an advanced visualization, with an eye on Vitessce | [#1086](https://github.com/depictio/depictio/issues/1086) |
| :material-map-marker-radius-outline: **A lighter map location control** | Collapsible controls in a popover, better default size | [#930](https://github.com/depictio/depictio/issues/930) |
| :material-filter-multiple-outline: **Journeys** | Named paths through tabs. The two halves of this idea already shipped: filters promoted to dashboard scope in [v1.6.0](../features/dashboards.md#persistent-sections), and [funnel filtering](../features/dashboards.md#funnel-filtering) in v1.7.0 | [#756](https://github.com/depictio/depictio/pull/756) · [#690](https://github.com/depictio/depictio/issues/690) · [#691](https://github.com/depictio/depictio/issues/691) |
### :material-flask-outline: Reports and citable science

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-file-document-edit-outline: **Report while exploring** | Assemble what you find into a report with a live Quarto preview, no re-execution | [#1148](https://github.com/depictio/depictio/issues/1148) |
| :material-flask-outline: **Citable science** | Immutable, DOI-citable app releases on the public EMBL instance, and sample-to-viz provenance via [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/). A [Quarto](https://quarto.org/) export is [in progress](#export-and-sharing) | [#1303](https://github.com/depictio/depictio/issues/1303) · [#931](https://github.com/depictio/depictio/issues/931) |
| :material-snake: **Snakemake report plugin** | Depictio as a drop-in replacement for Snakemake's static HTML report | *none yet* |
### :material-robot-outline: Agents

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-robot-outline: **One interface for agents and the in-app AI** | Create data, dashboards and templates together, driven by the authoring rules, with an MCP use-case catalog | [#1315](https://github.com/depictio/depictio/issues/1315) · [#1087](https://github.com/depictio/depictio/issues/1087) · [#844](https://github.com/depictio/depictio/issues/844) |

### :material-cog-outline: Running an instance

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-chart-timeline-variant: **Admin usage panel** | Visitors, sessions and top dashboards, from the opt-in analytics | [#1293](https://github.com/depictio/depictio/issues/1293) |
| :material-tag-multiple-outline: **Tags** | Tags on projects and on dashboards | [#857](https://github.com/depictio/depictio/issues/857) |
| :material-view-grid-plus-outline: **Component groups** | Group components and give a data collection a view shared by the group | [#308](https://github.com/depictio/depictio/issues/308) |

---

## Reproducibility & FAIR

Depictio is built with the [FAIR principles](https://www.go-fair.org/fair-principles/) in
mind. Most of the reproducibility story is shipped; citability is not.

| Challenge | Status |
| --------- | ------ |
| Reproducing a setup takes manual work | :material-check-circle: nf-core templates, one-command project setup ([docs](../usage/projects/templates.md)) |
| A visualization can't be reproduced | :material-check-circle: YAML-defined dashboards over traceable data ([docs](../features/yaml-sync.md)) |
| Experiment data sits in silos | :material-check-circle: Cross-DC linking ([docs](../features/cross-dc-filtering.md)) |
| Dashboards disappear | :material-check-circle: Hosted on [SciLifeLab Serve](https://serve.scilifelab.se/) |
| No data lineage | :material-check-circle: [Run provenance](../usage/projects/templates.md#run-provenance) records the parameters a run used; each table write is a Delta commit that a dashboard can be read at ([docs](../features/versioning.md#data-versions)) |
| Not citable, no sample-to-viz traceability | :material-lightbulb-outline: DOI snapshots + LabID provenance — [an idea](#ideas) |

---

## Get involved

- [:material-github: Issues](https://github.com/depictio/depictio/issues) — feature requests and bug reports
- [:material-source-pull: Pull requests](https://github.com/depictio/depictio/pulls) — everything under *In progress*, live
- [Contributing Guide](../developer/contributing.md) — setup, conventions, how to add a tool
