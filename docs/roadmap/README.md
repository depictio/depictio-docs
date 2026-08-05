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

!!! info "Current release: [v1.4.0](https://github.com/depictio/depictio/releases/tag/v1.4.0) (5 August 2026)"
    Every dated claim below is traceable to the [changelog](../changelog/README.md).
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

- title: "Authoring & the catalog"
  content: "Tools catalog gallery, project builder, tools builder on GitHub Pages"
  icon: ":fontawesome-solid-screwdriver-wrench:"
  key: "inprogress"
  sub_title: "In progress 🚧"

- title: "Versioning & automation"
  content: "Dataset and dashboard versioning, time travel, ingestion watcher, remote triggering"
  icon: ":fontawesome-solid-clock-rotate-left:"
  key: "inprogress"
  sub_title: "In progress 🚧"

- title: "Ideas"
  content: "Serverless Depictio, journeys & funnels, citable DOI snapshots, AI-assisted analysis"
  icon: ":fontawesome-solid-lightbulb:"
  key: "idea"
  sub_title: "Unscheduled 💡"

::/timeline::

---

## :material-check-circle:{ .rn-shipped } Shipped

One row per capability, newest first. The [feature docs](../features/README.md) are the
reference; this table only says *when* something arrived.

| Capability | Since | Docs |
| ---------- | ----- | ---- |
| Dashboard sections, dashboard-wide map panel, ten new card layouts | v1.4.0 | [Dashboards](../features/dashboards.md#sections) · [Components](../features/components.md#dashboard-wide-map-panel) |
| Lazy panel loading, bounded payloads, *Load all*, benchmark harness | v1.3.0 | [Performance & Scaling](../features/performance.md) |
| Pinned timeline footer, compact tables | v1.2.2 | [YAML Sync](../features/yaml-sync.md) |
| Admin **Log & Task** monitoring, per-phase ingestion detail, run provenance | v1.2.0 – v1.2.1 | [Monitoring](../usage/administration/monitoring.md) |
| Real-time dashboard events over WebSocket | v1.1.4 | [Real-time Events](../usage/guides/realtime-events.md) |
| Passwordless magic-link login, pipeline provisioning | v1.1.3 | [Authentication Modes](../usage/guides/authentication-modes.md) |
| Cross-DC linking UI, ingestion reports, self-adapting nf-core templates | v1.1.0 | [Cross-DC Filtering](../features/cross-dc-filtering.md) |
| React viewer as sole frontend on canonical URLs | v1.0.0 | [Dashboards](../features/dashboards.md) |
| Tools catalog — tool outputs become dashboard components | v1.0.0 | [Catalog](../catalog/index.md) |
| Advanced biology visualizations (volcano, Manhattan, sunburst…) | v0.13.0 | [Components](../features/components.md#advanced-visualizations) |
| MultiQC data lifecycle, DC-level type config | v0.12.0 | [Projects Guide](../usage/projects/guide.md) |
| Templates & recipes — one-command project setup | v0.10.0 | [Templates](../usage/projects/templates.md) · [Recipes](../usage/projects/recipes.md) |
| Geospatial maps, choropleth & GeoJSON collections | v0.8.0 | [Components](../features/components.md#map-components) |
| MultiQC report integration | v0.5.0 | [Components](../features/components.md#multiqc-components) |
| YAML-defined projects & dashboards, Delta Lake ingestion via CLI | v0.0.5 | [CLI Usage](../depictio-cli/usage.md) · [YAML Sync](../features/yaml-sync.md) |
| Docker Compose & Kubernetes/Helm deployment | v0.0.5 | [Installation](../installation/docker.md) |

---

## :material-progress-wrench:{ .rn-progress } In progress

Grouped by theme. Each item links the pull request that implements it, so its
real state is always one click away.

### Telemetry & backup compatibility

- [ ] **Anonymous installation telemetry** — an opt-out, aggregate heartbeat so we can answer "how many installations exist, on what version?". Counts are bucketed (`2-5`, `200+`), never exact ([#916](https://github.com/depictio/depictio/pull/916))
- [ ] **Cross-version backup guard** — frozen backup fixtures validated against current models on every PR, so a model change cannot silently break restoring an older backup ([#871](https://github.com/depictio/depictio/pull/871))

### Authoring: catalog, project builder, tools builder

Lowering the cost of contributing a tool or standing up a project.

- [ ] **Catalog gallery + nf-core harmonization** — dashboards reference reusable catalog modules via `use: <tool>/<render>` instead of bespoke inline tiles, with a browsable live gallery ([#873](https://github.com/depictio/depictio/pull/873))
- [ ] **Project builder** — `depictio project-builder <folder>` turns a folder into a `project.yaml`, with live glob/regex matching and schema-consistency checks ([#901](https://github.com/depictio/depictio/pull/901))
- [ ] **Tools builder on GitHub Pages** — author a catalog entry in the browser using Depictio's real component builders, then open the PR in one click ([#902](https://github.com/depictio/depictio/pull/902))
- [ ] **Catalog component picker in the viewer** — pick a catalog render while building a dashboard. *No PR open yet* ([#859](https://github.com/depictio/depictio/issues/859))

### Pipeline templates

- [ ] **nf-core/variantbenchmarking template & modules** — germline small variants, somatic indels and structural variants as three per-variant-type projects, built from reusable catalog modules (hap.py, rtg-tools, som.py, truvari…) plus four benchmarking-specific visualization kinds ([#870](https://github.com/depictio/depictio/pull/870), closes [#865](https://github.com/depictio/depictio/issues/865))

### Component export & embedding

- [ ] **Embed a component in an external site** — serve one dashboard component either as a Plotly spec for your own `plotly.js`, or as a single self-contained offline page. Off by default ([#917](https://github.com/depictio/depictio/pull/917))

### Versioning, time travel & automated ingestion

Ingestion stops being a command someone has to remember, and nothing overwrites history.

- [ ] **Ingestion watcher** — `depictio watch` notices new files and re-ingests them, with native events plus polling as a backstop for network filesystems, and a *Run now* trigger from the UI ([#915](https://github.com/depictio/depictio/pull/915))
- [ ] **Delta dataset versioning & time travel** — every write becomes an inspectable Delta version carrying Depictio's own provenance; browse and read the table as it was ([#915](https://github.com/depictio/depictio/pull/915))
- [ ] **Dashboard version history** — every save is recorded, with a timeline, read-only preview of any past version, and a restore that cannot lose the present ([#919](https://github.com/depictio/depictio/pull/919), closes [#95](https://github.com/depictio/depictio/issues/95))
- [ ] **Remote triggering from Nextflow** — a `nextflow.config` snippet ingests into Depictio when the pipeline completes ([#813](https://github.com/depictio/depictio/pull/813))

---

## :material-lightbulb-outline:{ .rn-idea } Ideas

Wanted, discussed, not scheduled. Nothing here has a date, and some of it will never be
built. Open or upvote an [issue](https://github.com/depictio/depictio/issues) to push
something up.

| Idea | What it would give you | Link |
| ---- | ---------------------- | ---- |
| :material-cloud-off-outline: **Serverless Depictio** | Explore a dashboard with no server to deploy or maintain | — |
| :material-filter-multiple-outline: **Journeys, funnels & global filters** | Filters promoted to dashboard scope, named paths through tabs, live row counts as the data narrows | [#756](https://github.com/depictio/depictio/pull/756) |
| :material-magic-staff: **Auto-compose from a run** | Point Depictio at a pipeline output directory and get a dashboard, no template chosen by hand (nf-core + Snakemake) | [#811](https://github.com/depictio/depictio/pull/811) |
| :material-file-document-edit-outline: **Project → template via the UI** | Turn a working project and its dashboards into a reusable template without touching YAML | [#861](https://github.com/depictio/depictio/issues/861) |
| :material-flask-outline: **Citable science** | DOI-backed snapshots per dashboard version, sample-to-viz provenance via [LabID](https://grp-gbcs.embl-community.io/labid-user-docs/), static export to [Quarto](https://quarto.org/) | — |
| :material-robot-outline: **AI-assisted analysis** | Describe the analysis and get a proposed layout; anomaly detection, narration, and an MCP server for AI agents | [#844](https://github.com/depictio/depictio/issues/844) |
| :material-table-merge-cells: **Grain-aware joins** | Detect each table's grain so a cross-DC join cannot silently explode rows | [#877](https://github.com/depictio/depictio/pull/877) |
| :material-snake: **Snakemake report plugin** | Depictio as a drop-in replacement for Snakemake's static HTML report | — |

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
| No data lineage | :material-progress-wrench: Delta dataset versioning and time travel — [in progress](#versioning-time-travel-automated-ingestion) |
| Not citable, no sample-to-viz traceability | :material-lightbulb-outline: DOI snapshots + LabID provenance — [an idea](#ideas) |

---

## Get involved

- [:material-github: Issues](https://github.com/depictio/depictio/issues) — feature requests and bug reports
- [:material-source-pull: Pull requests](https://github.com/depictio/depictio/pulls) — everything under *In progress*, live
- [Contributing Guide](../developer/contributing.md) — setup, conventions, how to add a tool
