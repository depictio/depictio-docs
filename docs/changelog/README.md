---
title: "Changelog"
icon: material/update
description: "Track changes and updates to Depictio across different versions."
hide:
  - navigation
---

# Changelog

??? docker "Docker images"

    Every release publishes four images, tagged with the version without its `v`:

    ```bash
    ghcr.io/depictio/depictio-api:1.24.2
    ghcr.io/depictio/depictio-viewer:1.24.2
    ghcr.io/depictio/depictio-worker:1.24.2
    ghcr.io/depictio/depictio-cli:1.24.2     # from v1.10.0
    ```

    Before v1.0.0, a single `ghcr.io/depictio/depictio:<version>` image shipped, with `latest`, `stable` and `edge` tags.

---

## **[v1.24.2](https://github.com/depictio/depictio/releases/tag/v1.24.2)** (November 27, 2026)

!!! success "Patch: advanced viz controls left unset, public builds after a worker dies, the ready copy first in Export"

### **🐛 Bug Fixes**

* **An unset advanced viz control falls back to its default**: a stored `point_size: null` no longer fails the embedding figure. [Advanced visualizations](../features/advanced-visualizations.md) ([afa41cb](https://github.com/depictio/depictio/commit/afa41cbf8))
* **A public build whose worker dies is queued again**, and given up as failed after repeated interruptions, so its report no longer stays "being prepared" forever. ([00ebb95](https://github.com/depictio/depictio/commit/00ebb959b))
* **The Export section offers the ready copy first**: where a public project keeps one, its report, PDF and dashboard are plain download links; building your own view is folded below. ([50cfc31](https://github.com/depictio/depictio/commit/50cfc31ba))

---

## **[v1.23.0](https://github.com/depictio/depictio/releases/tag/v1.23.0)** (November 22, 2026)

!!! success "Minor: table joins from the web interface, a redesigned Tool Studio and a security review"

### **♻️ Migration**

* **Quick-start compose binds to 127.0.0.1**: set `DEPICTIO_BIND_ADDRESS=0.0.0.0` for a multi-user deployment. ([#1465](https://github.com/depictio/depictio/pull/1465))
* **WebSockets authenticate with a first message** (`?token=` is deprecated), and `GET /auth/list_tokens` no longer returns token values. ([#1465](https://github.com/depictio/depictio/pull/1465))
* **Notebook export off by default**; the single-file dashboard export sits behind `DEPICTIO_STATIC_EXPORT_ENABLED`. ([#1460](https://github.com/depictio/depictio/pull/1460))

### **✨ New Features**

* **Table joins from the web interface**: preview, then a `joined_<name>` table rebuilt when a source changes. [Join two tables](../usage/projects/guide.md#join-two-tables) ([#1462](https://github.com/depictio/depictio/pull/1462))
* **Tool Studio redesign**: recipes run in the browser, several outputs per tool, checks at parity with the CLI. [Tool Studio](../developer/tool-studio.md) ([#1441](https://github.com/depictio/depictio/pull/1441))
* **Offline engine** (behind both export switches): a dashboard as one HTML file, sharing its runtime with Quarto reports. ([#963](https://github.com/depictio/depictio/pull/963), [#1409](https://github.com/depictio/depictio/pull/1409))
* **Tools Catalog front page** with a tool grid and 16 categories. [Tools Catalog](https://depictio.github.io/depictio-catalog/latest/) ([#1461](https://github.com/depictio/depictio/pull/1461))

### **🔒 Security**

* **Sessions and sign-in**: rotating refresh tokens, server-side sign-out, no empty passwords, rate-limited access codes. [Security](../features/security.md#session-hardening) ([#1465](https://github.com/depictio/depictio/pull/1465))
* **Access and secrets**: signed URLs for private images, editor rights and a memory cap for code mode, no password hash or S3 key in responses and logs. [Security](../features/security.md#code-sent-with-a-render) ([#1464](https://github.com/depictio/depictio/pull/1464), [#1465](https://github.com/depictio/depictio/pull/1465))

### **🐛 Bug Fixes**

* **An older CLI reads a newer server's `CLI.yaml`**, with one warning. ([#1463](https://github.com/depictio/depictio/pull/1463))
* **Uploads no longer fail after an hour** (expired login token). ([#1462](https://github.com/depictio/depictio/pull/1462))
* **No WebSocket retries when realtime events are off**. ([#1465](https://github.com/depictio/depictio/pull/1465))

---

## **[v1.22.2](https://github.com/depictio/depictio/releases/tag/v1.22.2)** (November 19, 2026)

!!! success "Patch: the Tools Catalog becomes its own site, and raw text collections keep their line order"

### **✨ New Features**

* **Tools Catalog site**: the catalog is published as its own static site, one directory per release plus `latest/`, and loads each output only when it is shown. A module's page lists its versions across releases, with a YAML diff and a release switcher. [Tools Catalog](https://depictio.github.io/depictio-catalog/latest/) ([#1439](https://github.com/depictio/depictio/pull/1439), [#1451](https://github.com/depictio/depictio/pull/1451), [#1455](https://github.com/depictio/depictio/pull/1455))
* **Finer catalog versions**: an output or a render may carry the module version it last changed in, and `module.yaml` may keep a changelog. [Tools Catalog](../catalog/index.md) ([#1447](https://github.com/depictio/depictio/pull/1447))

### **🚀 Improvements**

* **Catalog figures audited**: every render has a title and a description, figures no longer add up rows of different metrics, and reference lines can show a statistic of the table (median, mean, quantiles). ([#1447](https://github.com/depictio/depictio/pull/1447))
* **`depictio dev catalog validate` loads an output's recipe even when it has a fixture**, and checks the fixture holds every column the recipe produces. ([#1440](https://github.com/depictio/depictio/pull/1440))

### **🐛 Bug Fixes**

* **Raw text collections keep their line order**: since 1.22.0, Delta writes could store a table's rows out of order, so recipes rebuilt broken alignments and HMM models (nf-core/proteinfamilies). Writes keep the order again, and every raw scan now numbers its lines (`source_line`), so recipes read each file back in order whatever the storage does. Re-ingest a raw collection ingested with 1.22.0. ([#1448](https://github.com/depictio/depictio/pull/1448), [#1449](https://github.com/depictio/depictio/pull/1449))
* **The Helm off-site backup CronJob passes stricter admission policies**: `backups.offsite.imagePullPolicy` defaults to `Always` and the job sets CPU and memory limits, both overridable. ([#1442](https://github.com/depictio/depictio/pull/1442))

---

## **[v1.22.1](https://github.com/depictio/depictio/releases/tag/v1.22.1)** (November 19, 2026)

!!! success "Patch: cross-tab filters on private projects, `depictio local up` with an older pnpm, Helm backups"

### **✨ New Features**

* **Helm backups**: the chart can mount a backups volume, run scheduled MongoDB backups, and copy backups and S3 data off the cluster every night with rclone. [Helm backups](../installation/kubernetes.md#backups) ([#1438](https://github.com/depictio/depictio/pull/1438))

### **🐛 Bug Fixes**

* **Links work for non-admin owners and editors**: the links API refused every non-admin owner of a private project, so cross-tab filters failed there with a server error, and only an admin could create or edit a link. Owners, editors and group roles are now checked like everywhere else. [Cross-DC filtering](../features/cross-dc-filtering.md) ([9c6cca9](https://github.com/depictio/depictio/commit/9c6cca9ac))
* **`depictio local up` builds the viewer with pnpm 10**, through corepack when the `pnpm` on `PATH` is older; the server no longer starts without a viewer. [Python package](../installation/local.md) ([df02ea0](https://github.com/depictio/depictio/commit/df02ea0c6))

---

## **[v1.22.0](https://github.com/depictio/depictio/releases/tag/v1.22.0)** (November 18, 2026)

!!! success "Minor: one Nextflow subworkflow publishes any nf-core run, templates read their routes from the run, and nine new pipeline releases"

### **♻️ Migration**

* **Genome Tracks Showcase is opt-in**: a fresh instance no longer seeds it; set `DEPICTIO_SEED_EXTRA_PROJECTS=genome_tracks_examples` to keep it. Existing instances keep theirs. [Example projects](../installation/configuration.md#example-projects) ([#1421](https://github.com/depictio/depictio/pull/1421))
* **Helm picks how browsers read indexed files**: the chart sets `DEPICTIO_S3_BROWSER_ACCESS=proxy` when it does not route the S3 store (no ingress or gateway, or no `global.domain`); `s3.browserAccess` forces a mode. ([#1426](https://github.com/depictio/depictio/pull/1426))
* **Helm pods get an egress label**: `backend.podLabels` and `celery.podLabels` default to `networking/allow-internet-egress: "true"`, which SciLifeLab Serve needs; set it to `"false"` to opt out. [Kubernetes](../installation/kubernetes.md) ([#1425](https://github.com/depictio/depictio/pull/1425))
* **The `depictio/ingest` Nextflow module uses the all-in-one image**: `ghcr.io/depictio/depictio-allinone:1.22.0` (CLI, server and databases in one image) instead of `depictio-cli`, so a pipeline task downloads nothing. ([#1407](https://github.com/depictio/depictio/pull/1407))

### **✨ New Features**

* **A pipeline can ship its own dashboards**: add the `depictio/publish` subworkflow to an nf-core pipeline, and its last step ingests the run into a temporary Depictio and publishes it as a folder (`results/depictio/`). Anyone reopens that folder with `depictio local up`, no server needed. [Publish from a pipeline](../workflows/nextflow/subworkflow.md) ([#1407](https://github.com/depictio/depictio/pull/1407))
* **Template routes read from the run**: templates set their route variables (`--skip_*`, platform, tools) from the run's `params_<timestamp>.json`, so no `--var` is needed; `--var NAME=false` unsets one. ([#1408](https://github.com/depictio/depictio/pull/1408))
* **`depictio template check`**: checks a template's variables against a run, a release's `nextflow_schema.json` or the next release, offline. [`template check`](../depictio-cli/usage.md#template-check) ([#1408](https://github.com/depictio/depictio/pull/1408))
* **YAML and JSON samplesheets**: `depictio ingest` and `manifest from-table` read a YAML or JSON list of records exactly as the same CSV. [`manifest from-table`](../depictio-cli/usage.md#manifest-from-table) ([#1289](https://github.com/depictio/depictio/pull/1289))
* **Onboarding coach**: short, non-blocking cards replace the walkthrough, one chapter per page; *Account settings* › *Getting started* replays or stops them. [Account settings](../usage/guides/web_ui.md#account-settings) ([#1423](https://github.com/depictio/depictio/pull/1423))
* **Indexed files through the API**: `DEPICTIO_S3_BROWSER_ACCESS=proxy` streams 3D structures and GenomeSpy tracks through the API when browsers cannot reach S3. [S3 Storage](../installation/env-reference.md#s3-storage) ([#1426](https://github.com/depictio/depictio/pull/1426))

### **🚀 Improvements**

* **Landing card and Guide**: the landing card greets any reader who does not own the dashboard and names new runs; the Guide adds *Label your samples* and *What's new*. [Landing hint](../usage/guides/dashboard-guide.md#landing-hint) ([#1423](https://github.com/depictio/depictio/pull/1423))
* **Large recipe tables in less memory**: Delta tables are written in slices and recipes can yield batches; the `hmm_profile` ingest peaks at 2.2 GB instead of 10.2 GB. ([#1424](https://github.com/depictio/depictio/pull/1424))
* **A partial shared-samples check says so**: the *Checks* table and the attach card show *Needs a look* when only some MultiQC reports could be read. [Add data](../usage/projects/guide.md#add-data) ([#1424](https://github.com/depictio/depictio/pull/1424))

### **🧬 Pipeline Templates**

* **nf-core/ampliseq 3.1.0**: reads the renamed samplesheet columns (`sample`, `fastq_1`, `fastq_2`) and `Domain` as top rank; the seeded ampliseq project now comes from 3.1.0. [ampliseq](../pipeline-templates/nf-core/ampliseq.md) ([#1411](https://github.com/depictio/depictio/pull/1411))
* **nf-core/rnasplice 2.0.0**: reads the new DEXSeq, SUPPA and rMATS layouts, with dPSI oriented from SUPPA's own header. [rnasplice](../pipeline-templates/nf-core/rnasplice.md) ([#1413](https://github.com/depictio/depictio/pull/1413))
* **nf-core/rnaseq 3.28.0, sarek 3.12.0, mhcquant 3.3.0 and variantbenchmarking 1.6.1**: checked on each release's megatest; rnaseq's `pct_trimmed` now comes from MultiQC's Trim Galore data. ([#1410](https://github.com/depictio/depictio/pull/1410))
* **nf-core/quantms 1.2.0, eager 2.5.3 and proteinfamilies 2.6.0**: validated on real runs; quantms reads the renamed `_ms_info.tsv`, and eager's genotyping collections are optional. ([#1415](https://github.com/depictio/depictio/pull/1415), [#1414](https://github.com/depictio/depictio/pull/1414), [#1412](https://github.com/depictio/depictio/pull/1412))
* **Release drift checks**: a PR adding a template version runs both templates on both releases' runs and reports lost files, columns and params. ([#1417](https://github.com/depictio/depictio/pull/1417))

### **🐛 Bug Fixes**

* **The Runs tab keeps two workflows apart** when their runs share a tag. [The Runs tab](../features/runs.md#the-runs-tab) ([#1424](https://github.com/depictio/depictio/pull/1424))
* **A sent project carries its indexed files** (VCF, BAM, structures); send again a project migrated before 1.22.0. [S3 Data Scope](../usage/administration/migrate.md#s3-data-scope) ([#1422](https://github.com/depictio/depictio/pull/1422))
* **GeoJSON maps draw their regions again.** [Map Components](../features/components.md#map-components) ([#1422](https://github.com/depictio/depictio/pull/1422))
* **Sending to a target behind a login page** fails with where it redirects, instead of "not JSON". [Send to another instance](../usage/administration/migrate.md#send-to-another-instance) ([#1422](https://github.com/depictio/depictio/pull/1422))

---

## **[v1.21.0](https://github.com/depictio/depictio/releases/tag/v1.21.0)** (November 16, 2026)

!!! success "Minor: projects start from their data, show what changed since your last visit, and move between instances"

### **♻️ Migration**

* **No more Basic or Advanced projects**: *New project* no longer asks for a type; `project_type` is still read from YAML but ignored. [Create a project](../usage/projects/guide.md#create-a-project) ([196c0d1](https://github.com/depictio/depictio/commit/196c0d17882ad92f6718fd0aa712ecdef2c47c11))
* **Single sign-on moves to OpenID Connect**: providers go in `DEPICTIO_AUTH_OIDC_PROVIDERS` and SAML is removed; `DEPICTIO_AUTH_GOOGLE_OAUTH_*` still works for this release. [Single sign-on](../installation/sso/index.md) ([#1356](https://github.com/depictio/depictio/pull/1356))

### **✨ New Features**

* **_"What's new"_ since your last visit**: the dashboard header lists what changed since you last opened it, with *Overlay*, *Split* and *Before | Now* views. Off by default (`DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED`). [_"What's new"_](../features/whats-new.md) ([#1398](https://github.com/depictio/depictio/pull/1398))
* **Compare runs**: the *Runs* tab lists each run's files and reports, and *Compare* opens a dashboard with that run's new samples marked. [Runs and run comparison](../features/runs.md) ([#1182](https://github.com/depictio/depictio/pull/1182), [#1398](https://github.com/depictio/depictio/pull/1398))
* **Start a project from its data**: upload, or read a folder, bucket or file URL in place; Depictio detects the pipeline and offers flat tables, custom workflows (also `depictio project-builder`) or a template. [Create a project](../usage/projects/guide.md#create-a-project) ([#1182](https://github.com/depictio/depictio/pull/1182), [#1382](https://github.com/depictio/depictio/pull/1382))
* **Add data to a project**: add tables from a folder or another run, unlock a table for cell edits, and restore past versions. [Add data](../usage/projects/guide.md#add-data) ([#1382](https://github.com/depictio/depictio/pull/1382))
* **Label samples from the dashboard**: the *Metadata* panel adds label columns that become groups in *Analysis* and colour the linked figures. [Metadata panel](../features/metadata-panel.md) ([#1375](https://github.com/depictio/depictio/pull/1375))
* **Send a project to another instance**: a code moves a project with its data, dashboards and images, served read-only; *Export as ZIP* covers the offline case. [Send to another instance](../usage/administration/migrate.md#send-to-another-instance) ([#1334](https://github.com/depictio/depictio/pull/1334), [#1361](https://github.com/depictio/depictio/pull/1361), [#1387](https://github.com/depictio/depictio/pull/1387))

### **🚀 Improvements**

* **Refresh reads only what changed**: *Read everything again* forces a full pass, and the *Activity* tab shows ingestion history. [Data refresh](../features/runs.md#data-refresh) ([#1182](https://github.com/depictio/depictio/pull/1182))
* **Admin tables and an `/activity` page**: searchable admin tables with multi-select delete; `/activity` shows members their tasks without admin rights. [Administration](../usage/administration/index.md#admin-tables) ([#1390](https://github.com/depictio/depictio/pull/1390))
* **Also new**: a regex TextInput filter ([#1365](https://github.com/depictio/depictio/pull/1365)), map coordinates on tables ([#1389](https://github.com/depictio/depictio/pull/1389)), Google Cloud Storage reads ([#1291](https://github.com/depictio/depictio/pull/1291)) and a workshop Codespace ([#1372](https://github.com/depictio/depictio/pull/1372)).

### **🔒 Security**

* **Figure code can be limited to admins** (`DEPICTIO_VIEWER_CODE_FIGURES_LOCKED`), and new projects are private by default ([#1374](https://github.com/depictio/depictio/pull/1374)).

### **🧬 Pipeline Templates**

* **nf-core/crisprseq** guide comparison and **nf-core/sarek 3.11.0** genome browser ([e06f055](https://github.com/depictio/depictio/commit/e06f055ddaea2e64821df1b261547a9828dc1168)).

### **🐛 Bug Fixes**

* A sent project carries its images and logos, and multi-GB bundles go through ([#1383](https://github.com/depictio/depictio/pull/1383)); owners and P.I.s can find people to share a project with ([#1378](https://github.com/depictio/depictio/pull/1378)).

??? info "Beta releases leading up to v1.21.0"

    * **[b1](https://github.com/depictio/depictio/releases/tag/v1.21.0-b1)** (Nov 5): OpenID Connect, send to another instance, Google Cloud Storage.
    * **[b2](https://github.com/depictio/depictio/releases/tag/v1.21.0-b2)** (Nov 10): projects start from their data, ZIP export and import.
    * **[b3](https://github.com/depictio/depictio/releases/tag/v1.21.0-b3)** (Nov 11): editable tables, Metadata panel.
    * **[b4](https://github.com/depictio/depictio/releases/tag/v1.21.0-b4)** (Nov 11): dashboard import in public mode.
    * **[b5](https://github.com/depictio/depictio/releases/tag/v1.21.0-b5)** (Nov 11): admin tables, map coordinates.
    * **[b6](https://github.com/depictio/depictio/releases/tag/v1.21.0-b6)** (Nov 12): regex TextInput, crisprseq and sarek templates.

---

## **[v1.20.5](https://github.com/depictio/depictio/releases/tag/v1.20.5)** (November 4, 2026)

!!! success "Patch: `stacked_taxonomy` renamed `stacked_bar`, sturdier genome views and sections"

### **♻️ Migration**

* **`stacked_taxonomy` is now `stacked_bar`**: the old name still loads the same config, and a bar click can filter the dashboard (`selection_enabled`). [Stacked bar](../features/advanced-visualizations.md#stacked-bar) ([#1339](https://github.com/depictio/depictio/pull/1339))

### **🧬 Pipeline Templates**

* **Thresholds and windows follow their tool or a cited source** across the nf-core templates ([#1340](https://github.com/depictio/depictio/pull/1340)), and the ampliseq `reference_extended` dashboard is regenerated ([#1341](https://github.com/depictio/depictio/pull/1341)).

### **🐛 Bug Fixes**

* A genome view keeps its strongest rows when scores in [0, 1] are not p-values ([#1338](https://github.com/depictio/depictio/pull/1338)); a section keeps its highlights when its one data-bound tile is pruned ([#1337](https://github.com/depictio/depictio/pull/1337)).

---

## **[v1.20.4](https://github.com/depictio/depictio/releases/tag/v1.20.4)** (November 3, 2026)

!!! success "Patch: tiles that describe themselves, colour codes in tables and text, one error card"

### **✨ New Features**

* **A structured info popover describes a tile**: the (i) icon opens a lead, notes, warnings and a source written in the `description`; metadata and code move to **Data source and settings**. [Describe a tile](../usage/guides/dashboard_usage.md#describe-a-tile) ([#1328](https://github.com/depictio/depictio/pull/1328))
* **Colour codes in tables and text tiles**: `category_colors` columns draw a dot before each value, and `{{legend:column}}` prints a colour key. [Category colours](../features/dashboards.md#category-colors) ([95d49c3](https://github.com/depictio/depictio/commit/95d49c3b7c53cec4d9236ddd17fa733cb01b107c))

### **🚀 Improvements**

* **One error card for a page that cannot load**, with **Try again** when it can help. [Right Panel](../features/dashboards.md#right-panel) ([#1329](https://github.com/depictio/depictio/pull/1329))
* **A text line citing a missing column is removed on import** instead of printing a dash. [YAML Sync](../features/yaml-sync.md#text-live-values) ([305ad14](https://github.com/depictio/depictio/commit/305ad1413be2142502f481206d21db8887fb0797))
* **Stacked bar zoom draws an axis break, and the allele grid recolours cells and groups rows**. [Allele grid](../features/advanced-visualizations.md#allele-grid) ([95d49c3](https://github.com/depictio/depictio/commit/95d49c3b7c53cec4d9236ddd17fa733cb01b107c))

### **🧬 Pipeline Templates**

* **Colour keys and chart descriptions across the Overview templates**, and a review of hlatyping, viralmetagenome, genomeqc, epitopeprediction and stableexpression ([155bca6](https://github.com/depictio/depictio/commit/155bca6e866330658e305329a9952f66b3817b59)).

---

## **[v1.20.3](https://github.com/depictio/depictio/releases/tag/v1.20.3)** (November 3, 2026)

!!! success "Patch: the genome browser on the latest atacseq, chipseq and cutandrun templates"

* **🧬 Genome browser on the Locus tab** of atacseq 2.1.2, chipseq 2.1.0 and cutandrun 3.2.2, read in place with the optional `TRACKS_URI` variable. [Templates with a genome browser](../features/genome-browser/index.md#templates-with-a-genome-browser) ([#1324](https://github.com/depictio/depictio/pull/1324))

---

## **[v1.20.2](https://github.com/depictio/depictio/releases/tag/v1.20.2)** (November 2, 2026)

!!! success "Patch: the genome browser's ranked-variant counter on public dashboards"

* **🐛 Bug Fixes**: the ranked-variant counter and Prev/Next work for visitors of a public dashboard. [Genome browser](../features/genome-browser/index.md) ([#1323](https://github.com/depictio/depictio/pull/1323))

---

## **[v1.20.1](https://github.com/depictio/depictio/releases/tag/v1.20.1)** (November 2, 2026)

!!! success "Patch: genome views keep rows when table and assembly spell a contig differently"

* **🐛 Bug Fixes**: genome views keep rows on contigs the assembly spells differently (`21` and `chr21`) instead of showing "No rows" ([#1322](https://github.com/depictio/depictio/pull/1322)).

---

## **[v1.20.0](https://github.com/depictio/depictio/releases/tag/v1.20.0)** (November 2026)

!!! success "Minor: an embedded genome browser, linked to the dashboard both ways"

### **♻️ Migration**

* **The JBrowse iframe is removed**: the JBrowse server (port 3000), its session watcher (port 9010) and the `jbrowse2` collection type are gone; tracks are a `genomic_tracks` collection shown by the `jbrowse` component. [Genome browser](../features/genome-browser/index.md) ([#1123](https://github.com/depictio/depictio/pull/1123))
* **Template version changes**: a major version needs a re-ingest, a minor one only a dashboard re-import; nf-core/nascent moves to 2.0.0 ([#1311](https://github.com/depictio/depictio/pull/1311)).

### **✨ New Features**

* **An embedded genome browser**: JBrowse 2 shows the run's coverage, peaks, variants and alignments on 11 built-in assemblies or a custom one. [Genome browser](../features/genome-browser/index.md) ([#1123](https://github.com/depictio/depictio/pull/1123))
* **Two-way cross-filtering**: dashboard filters open matching tracks and move to a picked row (`locus_from`); a feature click filters the dashboard. [Examples](../features/genome-browser/index.md#examples) ([#1123](https://github.com/depictio/depictio/pull/1123))
* **A genome view navigates the browser**: a brushed region or another tab's genomic tile opens the browser on its locus. [Examples](../features/genome-browser/index.md#examples) ([#1123](https://github.com/depictio/depictio/pull/1123), [#1311](https://github.com/depictio/depictio/pull/1311))
* **UCSC tracks, breakpoint and circular views**, ranked calls, sashimi arcs and per-dashboard display defaults. [Examples](../features/genome-browser/index.md#examples) ([#1123](https://github.com/depictio/depictio/pull/1123))
* **A floating data table** on volcano and scatter tiles, linked to the points both ways ([#1308](https://github.com/depictio/depictio/pull/1308)).
* **A `depictio/ingest` Nextflow module** publishes a depictio folder with the run, and an **all-in-one image** reopens it with one `docker run` ([#1290](https://github.com/depictio/depictio/pull/1290), [#1300](https://github.com/depictio/depictio/pull/1300)).

### **🧬 Pipeline Templates**

* **A genome browser in 16 nf-core templates**. [Templates with a genome browser](../features/genome-browser/index.md#templates-with-a-genome-browser) ([#1123](https://github.com/depictio/depictio/pull/1123))
* **Ten more nf-core templates documented**: drop, epitopeprediction, genomeqc, hlatyping, nascent, quantms, raredisease, rnavar, stableexpression, viralmetagenome. [nf-core templates](../pipeline-templates/nf-core/index.md)
* **Template pages show the template version and last update**, and the `latest` aliases of hic, sarek and airrflow show the right pipeline version.
* **Thirty templates move from Draft to Experimental**: all but ampliseq and viralrecon (Reviewed); the catalog counts all 43 templates.
* **New pipeline versions**: airrflow 5.1.2, hic 2.1.0 and sarek 3.11.0 ([#1294](https://github.com/depictio/depictio/pull/1294), [#1302](https://github.com/depictio/depictio/pull/1302)).
* **Overview study cards**, and an Overview genome view in eleven templates ([#1306](https://github.com/depictio/depictio/pull/1306), [#1308](https://github.com/depictio/depictio/pull/1308)).

### **🐛 Bug Fixes**

* MongoDB starts on Linux 6.19+ kernels under Docker Compose ([#1297](https://github.com/depictio/depictio/pull/1297)); genome views keep rows on contigs spelled `20` or `chr20` ([#1308](https://github.com/depictio/depictio/pull/1308), [#1311](https://github.com/depictio/depictio/pull/1311)).

---

## **[v1.19.3](https://github.com/depictio/depictio/releases/tag/v1.19.3)** (October 28, 2026)

!!! success "Patch: faster dashboards, heatmaps that keep their height, and a larger UpSet"

### **♻️ Migration**

* **A heatmap keeps its authored height**: set `max_rows` to let it grow with a large matrix again. [Hierarchical Heatmap](../features/advanced-visualizations.md#hierarchical-heatmap) ([#1285](https://github.com/depictio/depictio/pull/1285))

### **🚀 Improvements**

* **Faster dashboard loads and filter changes** ([#1286](https://github.com/depictio/depictio/pull/1286)), a **larger UpSet** ([#1287](https://github.com/depictio/depictio/pull/1287)) and **compact docked controls** ([#1285](https://github.com/depictio/depictio/pull/1285)).

### **🧬 Pipeline Templates**

* **A Kingdom filter on the ampliseq Ordination tab**. [ampliseq](../pipeline-templates/nf-core/ampliseq.md#dashboard-tabs) ([#1292](https://github.com/depictio/depictio/pull/1292))

### **🐛 Bug Fixes**

* The figure code editor loads on a served instance ([#1283](https://github.com/depictio/depictio/pull/1283)); `depictio ingest` reads run tags on Python 3.15 ([#1281](https://github.com/depictio/depictio/pull/1281)).

---

## **[v1.19.2](https://github.com/depictio/depictio/releases/tag/v1.19.2)** (October 23, 2026)

!!! success "Patch: option cards"

* **Option cards**: a SegmentedControl drawn as cards, optionally at the top of the tab. [Option cards](../features/components.md#option-cards) ([#1264](https://github.com/depictio/depictio/pull/1264))
* **An optional glob that matches nothing is skipped**. [`RecipeSource` Reference](../usage/projects/recipes.md#recipesource-reference) ([#1264](https://github.com/depictio/depictio/pull/1264))

---

## **[v1.19.1](https://github.com/depictio/depictio/releases/tag/v1.19.1)** (October 16, 2026)

!!! success "Patch: protein tabs on one screen, and exports that keep card strips"

### **✨ New Features**

* **Scope banner** on one-unit tabs. [Scope banner](../features/dashboards.md#scope-banner) ([#1262](https://github.com/depictio/depictio/pull/1262))
* **Linked views**: a section's tiles as panes on one screen. [Linked view](../features/dashboards.md#linked-view) ([#1262](https://github.com/depictio/depictio/pull/1262))
* **Residue tiles sync their zoom**. [Linked by residue](../features/proteins.md#residue-selection) ([#1262](https://github.com/depictio/depictio/pull/1262))
* **Floating 3D structure** across tabs. [Floating structure](../features/advanced-visualizations.md#floating-structure) ([#1262](https://github.com/depictio/depictio/pull/1262))

### **🚀 Improvements**

* **Figures zoom on Ctrl or Cmd and the wheel**, or a pinch. [Right Panel](../features/dashboards.md#right-panel-visualizations) ([#1262](https://github.com/depictio/depictio/pull/1262))
* **proteinannotator, proteinfamilies and proteinfold** use these. [nf-core templates](../pipeline-templates/nf-core/index.md) ([#1262](https://github.com/depictio/depictio/pull/1262))

### **🐛 Bug Fixes**

* Export keeps card secondary strips and table row selection ([#1263](https://github.com/depictio/depictio/pull/1263)); builds and CI no longer count as installations in telemetry ([#1258](https://github.com/depictio/depictio/pull/1258)).

---

## **[v1.19.0](https://github.com/depictio/depictio/releases/tag/v1.19.0)** (October 15, 2026)

!!! success "Minor: protein tiles, seven nf-core templates, and Add user"

### **✨ New Features**

* **Protein tiles**: eight advanced visualizations for structures, alignments and protein families. [Proteins](../features/proteins.md) ([#1130](https://github.com/depictio/depictio/pull/1130))
* **Tiles linked by residue**: a pick filters every table, a hover marks every tile. [Linked by residue](../features/proteins.md#residue-selection) ([#1130](https://github.com/depictio/depictio/pull/1130))
* **Structures from AlphaFold DB or ESMFold**, off until `DEPICTIO_STRUCTURE_RESOLVER_ENABLED` is set. [Where the structure comes from](../features/proteins.md#structure-resolver) ([#1130](https://github.com/depictio/depictio/pull/1130), [#1254](https://github.com/depictio/depictio/pull/1254))
* **Add user**: an administrator creates an account with an initial password. [Adding a user](../usage/guides/web_ui.md#add-a-user) ([#1251](https://github.com/depictio/depictio/pull/1251))
* **Everyone with access** on a project's permissions. [Everyone with access](../usage/projects/guide.md#everyone-with-access) ([#1252](https://github.com/depictio/depictio/pull/1252))

### **🚀 Improvements**

* **`always_selected` and `default_by`** for pickers that hold one value. [Initial values](../features/yaml-sync.md#interactive-defaults) ([#1131](https://github.com/depictio/depictio/pull/1131), [#1257](https://github.com/depictio/depictio/pull/1257))
* **Protein tiles zoom and fold**. [The tiles](../features/advanced-visualizations.md#proteins) ([#1256](https://github.com/depictio/depictio/pull/1256))
* **Structure and PAE files as indexed-file collections**. [Indexed-file DCs](../usage/projects/guide.md#example-indexed-file-dcs) ([#1130](https://github.com/depictio/depictio/pull/1130))
* **27 catalog tools** for the new pipelines. [Tools Catalog](../catalog/index.md) ([#1131](https://github.com/depictio/depictio/pull/1131))

### **🔒 Security**

* **The structure resolver is off by default** and names the service it calls. [External structure services](../features/security.md#structure-resolver) ([#1130](https://github.com/depictio/depictio/pull/1130), [#1256](https://github.com/depictio/depictio/pull/1256))
* **SAML counts as single sign-on** for `DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED`. [Password sign-in](../usage/guides/authentication-modes.md#password-login) ([#1246](https://github.com/depictio/depictio/pull/1246))

### **🧬 Pipeline Templates**

* **Seven nf-core templates**, and a Protein tab on sarek. [nf-core templates](../pipeline-templates/nf-core/index.md) ([#1131](https://github.com/depictio/depictio/pull/1131))

### **🐛 Bug Fixes**

* SAML sign-in reads the identity provider's response ([#1247](https://github.com/depictio/depictio/pull/1247)); the API image builds again ([#1244](https://github.com/depictio/depictio/pull/1244)); dashboards with advanced visualizations export again ([#1239](https://github.com/depictio/depictio/pull/1239)).

---

## **[v1.18.1](https://github.com/depictio/depictio/releases/tag/v1.18.1)** (October 14, 2026)

!!! success "Patch: SAML in the API image, genome tracks with sign-in"

* **No images**: the API image failed to build; use v1.19.0 ([#1244](https://github.com/depictio/depictio/pull/1244)).
* **🐛 Bug Fixes**: SAML routes no longer answer 500 ([#1243](https://github.com/depictio/depictio/pull/1243)), file-backed genome tracks render with sign-in ([#1242](https://github.com/depictio/depictio/pull/1242)).

---

## **[v1.18.0](https://github.com/depictio/depictio/releases/tag/v1.18.0)** (October 14, 2026)

!!! success "Minor: SAML sign-in, user groups, shareable filters"

### **♻️ Migration**

* **Access changes go through Permissions**, not project updates. [Project permissions](../usage/projects/guide.md#project-permissions) ([#972](https://github.com/depictio/depictio/pull/972))
* **Data-collection writes follow the role**: editor renames or edits, owner deletes. [Group-Based Access](../features/security.md#group-based-access) ([#972](https://github.com/depictio/depictio/pull/972))

### **✨ New Features**

* **SAML 2.0 sign-in** with `DEPICTIO_AUTH_SAML_ENABLED` (use v1.19.0+). [SSO](../installation/sso/index.md) ([#968](https://github.com/depictio/depictio/pull/968))
* **User groups**, synced from the identity provider with `DEPICTIO_AUTH_SAML_ATTRIBUTE_GROUPS`. [Groups](../usage/administration/groups.md) ([#972](https://github.com/depictio/depictio/pull/972))
* **Remembered filters and filter links**. [Filter links](../usage/guides/dashboard_usage.md#filter-links) ([#967](https://github.com/depictio/depictio/pull/967))
* **Also new**: Create Data Collection on CLI projects ([#1039](https://github.com/depictio/depictio/pull/1039)), Log & Task for public-instance admins ([#1236](https://github.com/depictio/depictio/pull/1236)).

### **🔒 Security**

* **One permission check for every resource**; SAML ends on a single-use ticket. [Security](../features/security.md#group-based-access) ([#972](https://github.com/depictio/depictio/pull/972), [#968](https://github.com/depictio/depictio/pull/968))
* **Phylogeny trees read only from allowed locations** ([#1237](https://github.com/depictio/depictio/pull/1237)).

### **🐛 Bug Fixes**

* CLI refresh keeps browser-added collections ([#1038](https://github.com/depictio/depictio/pull/1038)), release check after upgrade ([#1236](https://github.com/depictio/depictio/pull/1236)), telemetry ID survives a wipe ([#1237](https://github.com/depictio/depictio/pull/1237)).

---

## **[v1.17.4](https://github.com/depictio/depictio/releases/tag/v1.17.4)** (October 13, 2026)

!!! success "Patch: landing hint, Comments and Versions in the Guide"

* **Landing hint for public guests**; the Guide covers Comments and Versions. [Landing hint](../usage/guides/dashboard-guide.md#landing-hint) ([#1208](https://github.com/depictio/depictio/pull/1208))
* **🐛 Bug Fixes**: Show me rings only a visible comments button ([#1209](https://github.com/depictio/depictio/pull/1209)).

---

## **[v1.17.3](https://github.com/depictio/depictio/releases/tag/v1.17.3)** (October 13, 2026)

!!! success "Patch: guests sign in where they would comment"

* **Guest sign-in from comments** on public instances with an identity provider. [Guest sign-in](../usage/guides/authentication-modes.md#guest-sign-in) ([#1207](https://github.com/depictio/depictio/pull/1207))
* **🐛 Bug Fixes**: table actions stay visible on narrow screens ([7d1ec740](https://github.com/depictio/depictio/commit/7d1ec740)).

---

## **[v1.17.2](https://github.com/depictio/depictio/releases/tag/v1.17.2)** (October 12, 2026)

!!! success "Patch: viewer comments, pinned filters reach MultiQC"

* **Viewers may comment** with `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT`. [Viewers can comment](../features/comments-annotations.md#viewers-can-comment) ([#1204](https://github.com/depictio/depictio/pull/1204), [#1206](https://github.com/depictio/depictio/pull/1206))
* **🧬 Templates**: 14 nf-core templates share one sample filter across tabs ([#1203](https://github.com/depictio/depictio/pull/1203)).
* **🐛 Bug Fixes**: pinned filters reach MultiQC panels ([#1201](https://github.com/depictio/depictio/pull/1201), [#1202](https://github.com/depictio/depictio/pull/1202)), all nf-core dashboards listed ([#1199](https://github.com/depictio/depictio/pull/1199)), readable Google sign-in errors ([#1198](https://github.com/depictio/depictio/pull/1198)).

---

## **[v1.17.1](https://github.com/depictio/depictio/releases/tag/v1.17.1)** (October 12, 2026)

!!! success "Patch: full-width section filter bars"

* **🐛 Bug Fixes**: section filter bars use their full width in the Paper look ([#1184](https://github.com/depictio/depictio/pull/1184)).

---

## **[v1.17.0](https://github.com/depictio/depictio/releases/tag/v1.17.0)** (October 12, 2026)

!!! success "Minor: embeddable components, Paper look, Account settings"

### **✨ New Features**

* **Embeddable components** as a Plotly spec (`plotly.js`), `<iframe>` or `curl` snippet, listed by `GET …/components`, enabled by `DEPICTIO_FASTAPI_EMBED_ENABLED`. [Component export](../features/component-export.md) ([#917](https://github.com/depictio/depictio/pull/917))
* **The Paper look** is the default; **Classic** keeps the old layout. [Looks](../usage/guides/web_ui.md#looks) ([#1174](https://github.com/depictio/depictio/pull/1174))
* **Account settings** replace the profile page. [Account settings](../usage/guides/web_ui.md#account-settings) ([#1180](https://github.com/depictio/depictio/pull/1180))
* **Release check** for admins; `DEPICTIO_VERSION_CHECK_ENABLED` disables it. [Release check](../usage/guides/web_ui.md#release-check) ([#1180](https://github.com/depictio/depictio/pull/1180))
* **Also new**: instance default look, sectioned Administration, `~/.depictio/CLI.yaml` plus `depictio config check`, `show_mark_labels: false` ([#1180](https://github.com/depictio/depictio/pull/1180)), faster codespace ([#1183](https://github.com/depictio/depictio/pull/1183)).

### **🐛 Bug Fixes**

* GitHub Releases published again, backfilled from v1.14.1 ([#1179](https://github.com/depictio/depictio/pull/1179)).

---

## **[v1.16.0](https://github.com/depictio/depictio/releases/tag/v1.16.0)** (October 11, 2026)

!!! success "Minor: remote data, run-folder projects, composed dashboards"

### **♻️ Migration**

* **`depictio ingest` no longer exits 2** when no template fits: it composes a dashboard. [Exit codes](../depictio-cli/usage.md#exit-codes) ([#1147](https://github.com/depictio/depictio/pull/1147))

### **✨ New Features**

* **Remote data**: `https://`, `s3://`, manifests; `--bind TAG=LOCATION` per collection; `--template <path>` runs a shared bundle. [Remote data](../usage/projects/remote-data.md#bind-a-data-collection-to-a-location) ([#965](https://github.com/depictio/depictio/pull/965))
* **S3 run folders** as `DATA_DIR` (`depictio ingest s3://bucket/run42`) or **From a run folder** (also under `depictio local`), with per-project bucket keys. [From a run folder](../usage/projects/remote-data.md#from-a-run-folder) ([#1047](https://github.com/depictio/depictio/pull/1047))
* **Sharing**: **From Manifest**, `depictio template export`, `depictio manifest from-table`. [Sharing a project](../usage/projects/remote-data.md#sharing-a-project) ([#965](https://github.com/depictio/depictio/pull/965))
* **Catalog-composed dashboards**: `depictio template compose`, `--include-unknown`, `--include GLOB`. [Composed dashboards](../usage/projects/composed-dashboards.md) ([#1147](https://github.com/depictio/depictio/pull/1147))
* **Also new**: `--result-json FILE`, catalog `stage`, `headline` and `priority` hints, `{name}` wildcards as columns ([#1147](https://github.com/depictio/depictio/pull/1147)).

### **🔒 Security**

* **Remote reads gated**: `https://` via `DEPICTIO_REMOTE_URL_ALLOWLIST`, never instance S3 keys; reports no longer probe the disk. [Remote data sources](../features/security.md#remote-data-sources) ([#965](https://github.com/depictio/depictio/pull/965), [#1047](https://github.com/depictio/depictio/pull/1047))

### **🐛 Bug Fixes**

* Refresh keeps every run's files ([#1047](https://github.com/depictio/depictio/pull/1047)), correct General Statistics offer ([#1147](https://github.com/depictio/depictio/pull/1147)).

---

## **[v1.15.1](https://github.com/depictio/depictio/releases/tag/v1.15.1)** (October 11, 2026)

!!! success "Patch: Codespaces demo, safer startup and S3 cleanup"

* **Try Depictio codespace** from the badge. [Installation](../installation/README.md#quickstart) ([#1176](https://github.com/depictio/depictio/pull/1176))
* **🐛 Bug Fixes**: S3 cleanup spares seeding tables ([#1175](https://github.com/depictio/depictio/pull/1175)), clean worker start after a MongoDB wipe ([#1177](https://github.com/depictio/depictio/pull/1177), [#1178](https://github.com/depictio/depictio/pull/1178)).

---

## **[v1.15.0](https://github.com/depictio/depictio/releases/tag/v1.15.0)** (October 9, 2026)

!!! success "Minor: version history, data time travel, ingestion automation"

### **♻️ Migration**

* **Scans apply `max_depth` and `ignore`**; `--legacy-scan-depth` ignores them for one release. [Scan bounds](../usage/projects/yaml-examples.md#scan-bounds) ([#915](https://github.com/depictio/depictio/pull/915))
* **Component tags must be unique per tab**; missing `index` derives from the tag. [Component Naming](../features/yaml-sync.md#component-naming) ([#1164](https://github.com/depictio/depictio/pull/1164))

### **✨ New Features**

* **Dashboard and component history** with restore. [History](../features/versioning.md#history) ([#919](https://github.com/depictio/depictio/pull/919), [#1164](https://github.com/depictio/depictio/pull/1164))
* **Data versions and time travel**; `depictio data versions` and `depictio data vacuum`. [Data versions](../features/versioning.md#data-versions) ([#915](https://github.com/depictio/depictio/pull/915), [#1164](https://github.com/depictio/depictio/pull/1164))
* **Ingestion automation**: `depictio watch`, server-side **Run ingestion**, an `ingestion` worker for `--async-upsert`, and a `/jobs` API. [Watch Command](../depictio-cli/usage.md#watch-command) ([#915](https://github.com/depictio/depictio/pull/915))
* **Also new**: `--write-mode replace-runs`, `--incremental-write`, `--skip-unchanged`, `--state-cache`, `--sync-changed`, Watchers pane, YAML `ecdf`, `strip`, `area`, `funnel`, `density_heatmap` and `density_contour` figures ([#915](https://github.com/depictio/depictio/pull/915), [#1164](https://github.com/depictio/depictio/pull/1164)).

### **🔒 Security**

* **Past versions rendered from the server record**: named by `definition_version`; `component_overrides` refused. [Past versions](../features/security.md#past-versions-in-a-render) ([#1164](https://github.com/depictio/depictio/pull/1164))

### **🐛 Bug Fixes**

* Slow profiles no longer stall the server; API timeout 120 to 300 s ([#915](https://github.com/depictio/depictio/pull/915)).

---

## **[v1.14.1](https://github.com/depictio/depictio/releases/tag/v1.14.1)** (October 9, 2026)

!!! success "Patch: nf-core templates v2, preview access checks"

* **`category_colors: auto` and live text values**. [Category colours](../features/yaml-sync.md#category-colors) ([#1160](https://github.com/depictio/depictio/pull/1160))
* **🧬 Templates**: nf-core v2 with Overview tabs; atacseq 2.1.2, chipseq 2.1.0, airrflow 5.1.1, cutandrun 3.2.2 ([#1160](https://github.com/depictio/depictio/pull/1160), [#1161](https://github.com/depictio/depictio/pull/1161)).
* **🐛 Bug Fixes**: figure previews and exports check project access ([#1166](https://github.com/depictio/depictio/pull/1166)).

---

## **[v1.14.0](https://github.com/depictio/depictio/releases/tag/v1.14.0)** (October 8, 2026)

!!! success "Minor: YAML landing tabs, dashboard Guide, Spotlight search"

### **♻️ Migration**

* **Advanced viz controls dock by the plot**; `controls_placement: popover` restores the popover. [Shared settings](../features/advanced-visualizations.md#shared-settings) ([#1145](https://github.com/depictio/depictio/pull/1145))

### **✨ New Features**

* **Landing-tab YAML**: markdown tiles (`tab:`, `params:` links, `surface`), `appearance: plain`, `display: strip` or `filter_bar: true`, `category_colors`, `figure_style: minimal`. [Markdown](../features/components.md#markdown) ([#1145](https://github.com/depictio/depictio/pull/1145))
* **Dashboard Guide and Spotlight search** (**⌘K** / **Ctrl+K**). [Spotlight](../usage/guides/spotlight-search.md) ([#1145](https://github.com/depictio/depictio/pull/1145), [#1152](https://github.com/depictio/depictio/pull/1152))
* **Also new**: card `variant` (`headline`, `compact`, `minimal`, `accent`, `split`) with `card_variant`, `caption`, `decimals` and `link`; `tab_group`, `filter_panel_default`, `content_width_default` and `show_tab_header` keys; **Copy to tab…**, Highlight components, `collapse_rank`, UpSet `selection_column`, `exclude_tabs`, Settings dialog ([#1145](https://github.com/depictio/depictio/pull/1145)).

### **🐛 Bug Fixes**

* YAML export keeps configs, narrow editors, string booleans (ampliseq `--ancombc true`), menus, maps ([#1145](https://github.com/depictio/depictio/pull/1145)).

---

## **[v1.13.2](https://github.com/depictio/depictio/releases/tag/v1.13.2)** (October 8, 2026)

!!! success "Patch: empty scans warn, dry run previews"

* **🐛 Bug Fixes**: empty scans warn; `--dry-run` counts matches per collection ([#1040](https://github.com/depictio/depictio/pull/1040)).

---

## **[v1.13.1](https://github.com/depictio/depictio/releases/tag/v1.13.1)** (October 8, 2026)

!!! success "Patch: refreshes keep attached runs"

* **🐛 Bug Fixes**: refresh keeps `--attach-run` runs (`--drop-missing-runs`) and adds template tabs, two `--dashboard` files stay two; `-v` and AWS tokens stay private ([#1157](https://github.com/depictio/depictio/pull/1157)).

---

## **[v1.13.0](https://github.com/depictio/depictio/releases/tag/v1.13.0)** (October 7, 2026)

!!! success "Minor: comments, ten viz kinds, thirteen nf-core templates"

### **♻️ Migration**

* **`Slider` filters are thresholds**; `slider_mode: eq` keeps exact match. [Slider options](../features/yaml-sync.md#interactive-defaults) ([#1102](https://github.com/depictio/depictio/pull/1102))
* **`threshold_warn`** on the passing side of `threshold_value` fails validation ([#1102](https://github.com/depictio/depictio/pull/1102)).
* **`ma`, `qq`, `enrichment`, `roc_pr_curve` become views** of volcano, dot plot, `pr_benchmark`. [Views](../features/advanced-visualizations.md#views) ([#1102](https://github.com/depictio/depictio/pull/1102))
* **`module.yaml` requires `description` and `homepage`** (optional `biotools_url`). [`module.yaml`](../developer/contributing-a-tool.md#step-1-moduleyaml-identity) ([#1102](https://github.com/depictio/depictio/pull/1102))
* **Reworked templates**: delete the old dashboard, then refresh ([#1102](https://github.com/depictio/depictio/pull/1102)).

### **✨ New Features**

* **Comments and annotations** on components. [Comments](../features/comments-annotations.md) ([#1109](https://github.com/depictio/depictio/pull/1109))
* **Ten visualization kinds**: contact map, knee plot, damage profile, genome view, group compare, transcript structure, copy-number profile, genome chord, parallel coordinates, record card. Record cards follow a `linked_component`, and `region` links filter by genome region. [Advanced visualizations](../features/advanced-visualizations.md#contact-map) ([#1102](https://github.com/depictio/depictio/pull/1102))
* **`indexed_file` collections** (VCF, BAM, bigWig, GFF3, tabix). [Indexed files](../usage/projects/guide.md#example-indexed-file-dcs) ([#1102](https://github.com/depictio/depictio/pull/1102))
* **Also new**: `transform.params`, `source_path`, variable `default`, `default_value`, `default_range`, `show_histogram`, `autofit: false` or `fit: fixed`, `controls_placement` and `advanced_viz_controls`, 56 catalog tools ([#1102](https://github.com/depictio/depictio/pull/1102)), view-bound annotations ([#1113](https://github.com/depictio/depictio/pull/1113)).

### **🧬 Pipeline Templates**

* **Thirteen new nf-core templates**: mag, nanoseq, riboseq, rnasplice (Experimental); demultiplex, eager, genomeassembler, hic, methylseq, mhcquant, sarek, scrnaseq, smrnaseq (Draft). Airrflow, cutandrun, differentialabundance, funcscan, rnaseq, taxprofiler and variantbenchmarking move to Experimental; atacseq, chipseq and rnafusion are reworked. Refresh a project to rebuild reshaped outputs (`sample`, `caller`, `truth_set`, MACS2 cards at q 0.05). [Pipeline Templates](../pipeline-templates/README.md) ([#1102](https://github.com/depictio/depictio/pull/1102))

### **🐛 Bug Fixes**

* Numeric table filters accept 0, `visu_type: violin` validates ([#1102](https://github.com/depictio/depictio/pull/1102)).

---

## **[v1.12.0](https://github.com/depictio/depictio/releases/tag/v1.12.0)** (October 7, 2026)

!!! success "Minor: server without Docker, `depictio` CLI, SeaweedFS"

### **♻️ Migration**

* **SeaweedFS replaces MinIO and starts empty**: copy the bucket (Helm: **before** `helm upgrade`). [Upgrading to v1.12.0](../installation/upgrade/v1.12.0-seaweedfs.md) ([#1061](https://github.com/depictio/depictio/pull/1061))
* **`DEPICTIO_MINIO_*` → `DEPICTIO_S3_*`**, Compose service `s3`, Helm key `s3:`. [Renamed settings](../installation/upgrade/v1.12.0-seaweedfs.md#renamed-settings) ([b729d9bf](https://github.com/depictio/depictio/commit/b729d9bf))
* **CLI package is `depictio`**: `pip install depictio` (`[multiqc]`, `[local]`); `depictio-cli` stays an alias; never `pip uninstall depictio-cli` alone. [CLI Installation](../installation/cli.md#install-via-pip) ([#1146](https://github.com/depictio/depictio/pull/1146))
* **CLI renames**: `run` → `ingest <results dir>` (no `--data-root`), `--project-name` → `--project`, `--skip-*` → `--skip`, `--CLI-config-path` → `--server`, `images push` → `data push-images`. [Quick Reference](../depictio-cli/usage.md#quick-reference) ([#1149](https://github.com/depictio/depictio/pull/1149))
* **`ingest --update-config` keeps edited dashboards** and rewrites tables as `--overwrite` did; `--reset-dashboards` starts over ([#1149](https://github.com/depictio/depictio/pull/1149)).
* **`EXPECTED_SCHEMA` → `OUTPUT_SCHEMA`**, `OPTIONAL_SCHEMA` → `OPTIONAL_OUTPUT_SCHEMA`. [Recipes](../usage/projects/recipes.md#what-is-a-recipe) ([#1128](https://github.com/depictio/depictio/pull/1128))
* **Listing opens on the table**; `DEPICTIO_VIEWER_DASHBOARDS_DEFAULT_VIEW=thumbnails` restores it ([#1139](https://github.com/depictio/depictio/pull/1139)).
* **`local export-compose` is `local export`**; `local up` no longer ingests (b1 `--template`, `--data-root` exit 2) ([#1110](https://github.com/depictio/depictio/pull/1110)).

### **✨ New Features**

* **`depictio local up`**: the full server without Docker, only `uv` needed. [Python package](../installation/local.md) ([#1110](https://github.com/depictio/depictio/pull/1110))
* **`depictio ingest <results dir>`** detects the template without `--template`; one `--server` option (`local` or a config file). [Ingest Command](../depictio-cli/usage.md#ingest-command) ([#1149](https://github.com/depictio/depictio/pull/1149))
* **Also new**: recipe `input_schema` checked before `transform()` ([#1132](https://github.com/depictio/depictio/pull/1132)), `DEPICTIO_PERFORMANCE_SCREENSHOTS_ENABLED` / `_DIR` ([#1110](https://github.com/depictio/depictio/pull/1110)), `taxon_palette` ([#1140](https://github.com/depictio/depictio/pull/1140)).

### **🐛 Bug Fixes**

* Taxonomy colours ([#1140](https://github.com/depictio/depictio/pull/1140)), stuck MultiQC ([#1110](https://github.com/depictio/depictio/pull/1110)), visitor file list ([#1144](https://github.com/depictio/depictio/pull/1144)), exit 1 with `--continue-on-error`, secrets in `-v` ([#1149](https://github.com/depictio/depictio/pull/1149)).

---

## **[v1.11.2](https://github.com/depictio/depictio/releases/tag/v1.11.2)** (September 24, 2026)

!!! success "Patch: sticky builder preview, tidier listing"

* **Listing and builder**: sticky preview ([#1105](https://github.com/depictio/depictio/pull/1105)), Card display menu, `DEPICTIO_VIEWER_DASHBOARDS_DEFAULT_VIEW`, `DEPICTIO_PERFORMANCE_SCREENSHOT_*` ([#1108](https://github.com/depictio/depictio/pull/1108)).

---

## **[v1.11.1](https://github.com/depictio/depictio/releases/tag/v1.11.1)** (September 17, 2026)

!!! success "Patch: opt-in Nextflow trigger"

* **Opt-in Nextflow trigger**: `depictio-cli config nextflow --install --default-disabled` ([#1103](https://github.com/depictio/depictio/pull/1103)).
* **🐛 Bug Fixes**: General Stats offer ([#1104](https://github.com/depictio/depictio/pull/1104)), catalog table rows ([#1101](https://github.com/depictio/depictio/pull/1101)).

---

## **[v1.11.0](https://github.com/depictio/depictio/releases/tag/v1.11.0)** (September 14, 2026)

!!! success "Minor: feedback link, column funnel"

### **✨ New Features**

* **Opt-in feedback link**: `DEPICTIO_FEEDBACK_ENABLED`, `DEPICTIO_FEEDBACK_URL`. [Feedback](../installation/env-reference.md#feedback) ([#1066](https://github.com/depictio/depictio/pull/1066))
* **Funnel by column values**. [Funnel filtering](../features/dashboards.md#funnel-filtering) ([#1095](https://github.com/depictio/depictio/pull/1095))
* **Also new**: Last viewed column ([f3152736](https://github.com/depictio/depictio/commit/f3152736)), analysis groups per kind ([#1093](https://github.com/depictio/depictio/pull/1093)), closed ingestion runs ([#1097](https://github.com/depictio/depictio/pull/1097)), UpSet and heatmap `set_columns_pattern` and `value_columns_pattern` regexes ([#1094](https://github.com/depictio/depictio/pull/1094), [#1098](https://github.com/depictio/depictio/pull/1098)).

### **🧬 Pipeline Templates**

* **variantbenchmarking** routes split ([#1081](https://github.com/depictio/depictio/pull/1081)); **ampliseq 2.18.0** phylogeny from S3, re-ingest trees ([#1096](https://github.com/depictio/depictio/pull/1096)).

### **🐛 Bug Fixes**

* Manhattan lasso ([#1093](https://github.com/depictio/depictio/pull/1093)), UpSet names ([#1098](https://github.com/depictio/depictio/pull/1098)), MultiQC prerender ([ecd5207d](https://github.com/depictio/depictio/commit/ecd5207d)).

---

## **[v1.10.1](https://github.com/depictio/depictio/releases/tag/v1.10.1)** (September 13, 2026)

!!! success "Patch: share a filtered listing by link"

* **Shareable listings**: filters live in the URL of `/dashboards` and projects, plus **Template** and **Workflow system** filters. [Share a filtered listing](../usage/guides/web_ui.md#share-a-filtered-listing) ([#1069](https://github.com/depictio/depictio/pull/1069))
* **MinIO from `quay.io/minio/minio`**: update mirrors that name the Docker Hub image ([#1080](https://github.com/depictio/depictio/pull/1080)).

---

## **[v1.10.0](https://github.com/depictio/depictio/releases/tag/v1.10.0)** (September 11, 2026)

!!! success "Minor: the pipeline ingests its own results"

### **✨ New Features**

* **Nextflow trigger**: a `workflow.onComplete` snippet runs `depictio-cli run`, set up with `depictio-cli config nextflow --install`. [Nextflow trigger](../workflows/nextflow/trigger.md) ([#1037](https://github.com/depictio/depictio/pull/1037))
* **`--pipeline-id <name>/<version>`**: picks the bundled template and stamps run versions. [Templates](../usage/projects/templates.md#pipeline-id) ([#1035](https://github.com/depictio/depictio/pull/1035), [#1036](https://github.com/depictio/depictio/pull/1036))
* **`--triggered-by`**: shown as a badge on the ingestion tab. [Ingestion Report & Health](../features/dashboards.md#triggered-by)
* **`--attach-run`** and env credentials `DEPICTIO_CLI_TOKEN`, `DEPICTIO_CLI_API_BASE_URL`, `DEPICTIO_CLI_CONFIG_PATH` overriding `CLI.yaml`. [CLI Usage](../depictio-cli/usage.md#environment-variables)

### **🚀 Improvements**

* **CLI container image** `ghcr.io/depictio/depictio-cli`, and templates ship in the `depictio-cli` package, so `--pipeline-id` needs no checkout. [CLI Installation](../installation/cli.md#container-image)
* **Also new**: `--dashboard` without a template; `run` and `config check` name the API URL on connection errors.

### **🧬 Pipeline Templates**

* **nf-core/variantbenchmarking 1.4.0** ([#870](https://github.com/depictio/depictio/pull/870)) and **ampliseq 2.18.0** with `sbdi-gtdb` ([#1027](https://github.com/depictio/depictio/pull/1027)). [variantbenchmarking](../pipeline-templates/nf-core/variantbenchmarking.md)

### **🐛 Bug Fixes**

* Repeat triggers, rescans deleting runs, false creation success, late expired-token errors, `-resume` parameters.

---

## **[v1.9.2](https://github.com/depictio/depictio/releases/tag/v1.9.2)** (September 1, 2026)

!!! success "Patch: MultiQC and ampliseq on full-size runs"

* **🐛 Bug Fixes**: MultiQC sections survive a bad anchor ([#1015](https://github.com/depictio/depictio/pull/1015)), ampliseq tiles on full runs ([#1014](https://github.com/depictio/depictio/pull/1014)), catalog preview in the API image ([#1019](https://github.com/depictio/depictio/pull/1019)).

---

## **[v1.9.1](https://github.com/depictio/depictio/releases/tag/v1.9.1)** (August 30, 2026)

!!! success "Patch: reworked demos, grouping in advanced viz"

* **Grouping in advanced visualizations**. [Analysis panel](../features/interactive-selection-filtering.md#analysis-panel) ([#1013](https://github.com/depictio/depictio/pull/1013))
* **Also new**: sign-in returns to the shared link ([#1012](https://github.com/depictio/depictio/pull/1012)), seeded demos reworked ([#1011](https://github.com/depictio/depictio/pull/1011)), Tool Studio footer fix ([#1010](https://github.com/depictio/depictio/pull/1010)).

---

## **[v1.9.0](https://github.com/depictio/depictio/releases/tag/v1.9.0)** (August 28, 2026)

!!! success "Minor: UI backups, catalog picker, Tool Studio"

### **✨ New Features**

* **Backups tab in `/admin`**: snapshot, download, upload, restore (typed `RESTORE`), scheduled backups (`HH:MM` UTC) with retention; covers MongoDB, not object storage. [Backup & Restore](../usage/administration/backup.md#from-the-admin-panel) ([#976](https://github.com/depictio/depictio/pull/976))
* **Pick from catalog**, with `use: <tool>/<render-id>` snippets and a `catalog_source` stamp. [Catalog picker](../usage/guides/catalog-picker.md) ([#988](https://github.com/depictio/depictio/pull/988))
* **Tool Studio**: contribute a tool to the catalog as a pull request. [Tool Studio](../developer/tool-studio.md) ([#902](https://github.com/depictio/depictio/pull/902))

### **🚀 Improvements**

* **Helm sign-in gates**: `password_login_disabled`, and `public_access_code` as `secrets.publicAccessCode`. [Kubernetes](../installation/kubernetes.md) ([#1008](https://github.com/depictio/depictio/pull/1008))

### **🐛 Bug Fixes**

* ZIP import answers `502` for object-store failures, not `400 Invalid ZIP bundle` ([#1009](https://github.com/depictio/depictio/pull/1009)), branding reaches every worker ([#1003](https://github.com/depictio/depictio/pull/1003)).

---

## **[v1.8.3](https://github.com/depictio/depictio/releases/tag/v1.8.3)** (August 28, 2026)

!!! success "Patch: fixes from a real ampliseq run"

* **Run provenance**: a template `provenance:` block fills `template_origin`, and tab headers on the canvas. [Run provenance](../usage/projects/templates.md#run-provenance) ([#1002](https://github.com/depictio/depictio/pull/1002))
* **🧬 ampliseq**: rarefaction pre-aggregated into `alpha_rarefaction_summary`. [ampliseq](../pipeline-templates/nf-core/ampliseq.md)
* **🐛 Bug Fixes**: silent UpSet, heatmap and `tag:` filters, code-mode preprocessing, `tab_order`, `box_plot_stats`, `pin: top`, section packing.

---

## **[v1.8.2](https://github.com/depictio/depictio/releases/tag/v1.8.2)** (August 28, 2026)

!!! success "Patch: two sign-in gates, durable logos"

* **Sign-in gates**: `DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED` and `DEPICTIO_AUTH_PUBLIC_ACCESS_CODE`. [Authentication Modes](../usage/guides/authentication-modes.md#password-login) ([#1007](https://github.com/depictio/depictio/pull/1007))
* **Logos stored in the database** (`branding_assets`), surviving redeploys. [Branding](../usage/administration/branding.md#logo-storage)

---

## **[v1.8.1](https://github.com/depictio/depictio/releases/tag/v1.8.1)** (August 28, 2026)

!!! success "Patch: branding reaches Kubernetes"

* **🐛 Bug Fixes**: Helm forwards `DEPICTIO_BRANDING_*`; EMBL overlay `values-embl-internal-dev-trec.yaml` added. [Branding](../usage/administration/branding.md) ([#1005](https://github.com/depictio/depictio/pull/1005))

---

## **[v1.8.0](https://github.com/depictio/depictio/releases/tag/v1.8.0)** (August 27, 2026)

!!! success "Minor: instance branding, navigable phylogeny"

### **✨ New Features**

* **Brand themes**: logo, colours and fonts from `DEPICTIO_BRANDING_*`, an `/admin` panel, or per-dashboard `brand_theme:`; `tint_mode` sets their reach, never remapping `gray`, `red`, `green`, `yellow`. [Branding](../usage/administration/branding.md) ([#1003](https://github.com/depictio/depictio/pull/1003))
* **Font size**: **A-** / **A+** and per-tile `font_scale`. [Components](../features/components.md#figure-components)
* **Navigable phylogeny**: zoom, collapse clades, filter by clade. [Phylogenetic](../features/advanced-visualizations.md#phylogenetic) ([#981](https://github.com/depictio/depictio/pull/981))

### **🐛 Bug Fixes**

* Brand shades, inherited overrides, Theme picker; legacy `logo_url` and `plot_theme` fold into `brand_theme`.

---

## **[v1.7.0](https://github.com/depictio/depictio/releases/tag/v1.7.0)** (August 26, 2026)

!!! success "Minor: selection groups, funnel filtering"

### **✨ New Features**

* **Selection groups** and the **Analysis panel** (Overlay or Split). [Selection groups](../features/interactive-selection-filtering.md#selection-groups) ([#962](https://github.com/depictio/depictio/pull/962))
* **Funnel filtering**, on by default with `n/N available` badges, plus a cross-DC mapping inspector. [Funnel filtering](../features/dashboards.md#funnel-filtering) ([#975](https://github.com/depictio/depictio/pull/975))

### **🐛 Bug Fixes**

* MultiQC filters intersect, all linked metadata DCs honoured, symmetric sample matching, filters at `0` count, `sample_mapping` links stay fresh, export keeps `selection_column` with `selection_enabled`.

---

## **[v1.6.1](https://github.com/depictio/depictio/releases/tag/v1.6.1)** (August 26, 2026)

!!! success "Patch: geo tables keep their type, visibility fix"

* **🔒 Visibility follows the project**: `is_public` cascades to dashboards, closing a privilege escalation ([#982](https://github.com/depictio/depictio/pull/982)).
* **Also new**: `lat_column`/`lon_column` in project YAML, Geomap badge, EMBL HA MongoDB ([#999](https://github.com/depictio/depictio/pull/999)), `mongodump` script ([#1000](https://github.com/depictio/depictio/pull/1000)).

---

## **[v1.6.0](https://github.com/depictio/depictio/releases/tag/v1.6.0)** (August 26, 2026)

!!! success "Minor: sections on every tab"

* **Persistent sections**: `persistent` and `pin` share a section across tabs. [Persistent sections](../features/dashboards.md#persistent-sections) ([#969](https://github.com/depictio/depictio/pull/969))
* **Also new**: ingestion report on every project, one `Add` menu, `Placement` and `Performance` builder panels, `--template` reads recipe seeds ([#997](https://github.com/depictio/depictio/pull/997)).
* **🐛 Bug Fixes**: fresh deployments start ([#993](https://github.com/depictio/depictio/pull/993)), MultiQC badge ([#996](https://github.com/depictio/depictio/pull/996)), thumbnails ([#994](https://github.com/depictio/depictio/pull/994)), export re-import.

---

## **[v1.5.2](https://github.com/depictio/depictio/releases/tag/v1.5.2)** (August 24, 2026)

!!! success "Patch: filtered previews, two deployment unblocks"

### **♻️ Migration**

* **`DEPICTIO_DEV_MODE` removed**: OAuth state now lives in MongoDB. [Security](../features/security.md#oauth-callback-security) ([#991](https://github.com/depictio/depictio/pull/991))

### **✨ New Features**

* **Apply to preview** ([#977](https://github.com/depictio/depictio/pull/977)), `latest` or version-less `nf-core/ampliseq` template ids ([#973](https://github.com/depictio/depictio/pull/973)), restores from v1.0.0 on ([#871](https://github.com/depictio/depictio/pull/871)). [Dashboard creation](../usage/guides/dashboard_creation.md#previewing-with-active-filters-v152)

### **🐛 Bug Fixes**

* No `ListBuckets` needed ([#990](https://github.com/depictio/depictio/pull/990)), multi-worker Google OAuth, real card names, not `Bucket 1/2/3` ([#836](https://github.com/depictio/depictio/pull/836)), `depictio run` reports the resolved template.

---

## **[v1.5.1](https://github.com/depictio/depictio/releases/tag/v1.5.1)** (August 6, 2026)

!!! success "Patch: telemetry counts real installations"

* **CLI install event** `cli_install`, Depictio User-Agent, CI runs (`CI`, `GITHUB_ACTIONS`) no longer counted ([#961](https://github.com/depictio/depictio/pull/961)).

---

## **[v1.5.0](https://github.com/depictio/depictio/releases/tag/v1.5.0)** (August 6, 2026)

!!! success "Minor: installation telemetry, Google Analytics wired"

* **Anonymous telemetry**: opt out with `DEPICTIO_TELEMETRY_ENABLED=false` or `DO_NOT_TRACK=1`; preview at `GET /utils/telemetry/preview`. [Telemetry](../features/telemetry.md) ([#916](https://github.com/depictio/depictio/pull/916))
* **Also new**: `depictio-cli --version` / `-V`; `DEPICTIO_GOOGLE_ANALYTICS_*` now works; `instance_label` populates `X-Depictio-CLI-Instance` ([#837](https://github.com/depictio/depictio/pull/837)).

---

## **[v1.4.0](https://github.com/depictio/depictio/releases/tag/v1.4.0)** (August 5, 2026)

!!! success "Minor: sections, map panel, ten card layouts"

### **♻️ Migration**

* **CSP `connect-src`** needs `https://basemaps.cartocdn.com`, `https://*.basemaps.cartocdn.com`, `https://tile.openstreetmap.org`. [Security](../features/security.md#basemap-origins) ([#951](https://github.com/depictio/depictio/pull/951))
* **`vertical_alignment`** defaults to `center`; set `top` for the old look. [Components](../features/components.md#text-components) ([#954](https://github.com/depictio/depictio/pull/954))
* **Helm `enableServiceLinks: false`** on every pod. [Kubernetes](../installation/kubernetes.md#service-link-environment-variables) ([#946](https://github.com/depictio/depictio/pull/946))

### **✨ New Features**

* **`grid_sections` and `filter_sections`**. [YAML Sync](../features/yaml-sync.md#dashboard-sections)
* **Map panel** (`placement: floating`) and `secondary_layout` cards `histogram`, `threshold`, `completeness`, `uniqueness`, `attrition`, `trend`, `gauge`, `grid`, `composition`, `donut`. [Components](../features/components.md#dashboard-wide-map-panel)
* **Also new**: component inspector via `DEPICTIO_VIEWER_INSPECTOR_ENABLED`, dependency refresh ([#947](https://github.com/depictio/depictio/pull/947), [#942](https://github.com/depictio/depictio/pull/942)).

### **🐛 Bug Fixes**

* Sessions refresh ([#940](https://github.com/depictio/depictio/pull/940)), `skewness`/`kurtosis`/`percentile` cards and `filter_expr` under filters, axis margins, dashboard saves.

---

## **[v1.3.1](https://github.com/depictio/depictio/releases/tag/v1.3.1)** (July 30, 2026)

!!! success "Patch: date columns, seeded thumbnails"

* **🐛 Bug Fixes**: Date columns ingest ([#925](https://github.com/depictio/depictio/pull/925)), seeded thumbnails restored ([#926](https://github.com/depictio/depictio/pull/926), [#927](https://github.com/depictio/depictio/pull/927)).

---

## **[v1.3.0](https://github.com/depictio/depictio/releases/tag/v1.3.0)** (July 29, 2026)

!!! success "Minor: performance across ingest, serve and render"

### **♻️ Migration**

* **`DEPICTIO_MULTIQC_PRERENDER`** and **`DEPICTIO_MULTIQC_PARSE_WORKERS`** become `DEPICTIO_INGEST_MULTIQC_PRERENDER` and `DEPICTIO_INGEST_MULTIQC_PARSE_WORKERS`.

### **✨ New Features**

* **Lazy panels** (progress like `6/8`) and **Load all**; tables default to 100 rows; cheaper `/deltatables/upsert`. [Performance & Scaling](../features/performance.md)
* **Also new**: pushed-down queries, `DEPICTIO_INGEST_*` tuning, a `benchmark/` suite.

### **🐛 Bug Fixes**

* CSP `script-src 'self'` allows WebGL, icons bundled, monitoring checks `events_enabled`, MultiQC sample filter, temporal pushdown.

---

## **[v1.2.2](https://github.com/depictio/depictio/releases/tag/v1.2.2)** (July 27, 2026)

!!! success "Patch: timeline footer, table columns"

* **Pinned timeline footer** for top-placed components, and `compact: true` tables. [YAML Sync](../features/yaml-sync.md#table-component)
* **🐛 Bug Fixes**: table `columns` restricts the grid and keeps `compact`, single-timestamp timelines.

---

## **[v1.2.1](https://github.com/depictio/depictio/releases/tag/v1.2.1)** (July 20, 2026)

!!! success "Patch: richer Log & Task"

* **Runtime log level** (`DEBUG` to `CRITICAL`, reset to `DEPICTIO_MONITORING_APP_LOG_MIN_LEVEL`), per-phase ingestion steps, `CLI` or `UI` source badges. [Monitoring](../usage/administration/monitoring.md)

---

## **[v1.2.0](https://github.com/depictio/depictio/releases/tag/v1.2.0)** (July 15, 2026)

!!! success "Minor: admin Log & Task monitoring"

* **Log & Task panel** with live updates. [Monitoring](../usage/administration/monitoring.md)
* **🐛 Bug Fixes**: MultiQC and JBrowse in project migration, single-user tab, "Start editing" targets `/dashboard-edit`.

---

## **[v1.1.4](https://github.com/depictio/depictio/releases/tag/v1.1.4)** (July 9, 2026)

!!! success "Patch: real-time dashboard events"

* **Real-time events**: `realtime.enabled` in `project.yaml` plus `DEPICTIO_EVENTS_ENABLED`; demo driver `stream_test.sh`. [Real-time Events](../usage/guides/realtime-events.md) ([#899](https://github.com/depictio/depictio/pull/899), [#900](https://github.com/depictio/depictio/pull/900))
* **🐛 Bug Fixes**: arro3 schemas in `polars_schema` ([#897](https://github.com/depictio/depictio/pull/897)).

---

## **[v1.1.3](https://github.com/depictio/depictio/releases/tag/v1.1.3)** (June 29, 2026)

!!! success "Patch: magic-link login, pipeline provisioning"

* **Magic-link login**: `depictio-cli run --user` provisions an account and links to `/dashboard/{id}`; disabled in single-user mode.
* **🐛 Bug Fixes**: the ampliseq seed provides `METADATA_FILE`.

---

## **[v1.1.2](https://github.com/depictio/depictio/releases/tag/v1.1.2)** (June 28, 2026)

!!! success "Patch: auth, links, template seeds"

* **`DEPICTIO_AUTH_REGISTRATION_DISABLED`** also gates Google sign-in; titles open in new tabs; ampliseq tree read from `qiime2/`.

---

## **[v1.1.1](https://github.com/depictio/depictio/releases/tag/v1.1.1)** (June 27, 2026)

!!! success "Patch: registration control, advanced-viz fixes"

* **`DEPICTIO_AUTH_REGISTRATION_DISABLED`** blocks new sign-ups; anonymous users see public dashboards.

---

## **[v1.1.0](https://github.com/depictio/depictio/releases/tag/v1.1.0)** (June 23, 2026)

!!! success "Minor: ingestion reports, DC linking UI, nf-core templates"

* **DC linking UI**, ingestion reports, health banner, project detail view.
* **Self-adapting nf-core templates** for ampliseq (SIDLE, `skip_qiime`) and viralrecon (Nanopore/ARTIC).
* **Also new**: `--dashboard-name`, MinIO and API ingresses, performance pass.
* **🐛 Bug Fixes**: cross-DC `target_column=None` ([#776](https://github.com/depictio/depictio/pull/776)), public-mode "Sign In" ([#784](https://github.com/depictio/depictio/pull/784)), viralrecon mean depth.

---

## **[v1.0.1](https://github.com/depictio/depictio/releases/tag/v1.0.1)** (June 11, 2026)

!!! success "Patch: quickstart hardening"

* **Zero-config quickstart**: `docker compose up -d` needs no `.env`; multi-arch images; admin seeded in single-user mode.
* **Pinned compose**: `docker-compose.yaml` pins each service to its release tag.
* **🐛 Bug Fixes**: MongoDB runs under `cap_drop: [ALL]`; viewer and backend get writable paths.

---

## **[v1.0.0](https://github.com/depictio/depictio/releases/tag/v1.0.0)** (June 10, 2026)

!!! success "Major: React is the sole frontend"

### **♻️ Migration**

* **Dash removed**: `depictio/dash/` deleted; `DashConfig` -> `ViewerConfig`; `DEPICTIO_DASH_` -> `DEPICTIO_VIEWER_`.
* **Canonical URLs**: `*-beta` paths 301 to `/dashboards`, `/dashboard/{id}`, `/dashboard-edit/{id}`, `/projects`, `/profile`, `/admin`, `/cli-agents`, `/about` ([#785](https://github.com/depictio/depictio/pull/785)).
* **Admin from env**: `initial_users.yaml` removed; set `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD`, or startup fails with no admin.

### **✨ New Features**

* **Split images**: `depictio-api`, `depictio-worker`, `depictio-viewer`.
* **Tool to viz catalog**: from nf-core, bio.tools and EDAM ([#783](https://github.com/depictio/depictio/pull/783)).
* **CLI**: `depictio commands` table, cleaner `catalog list`, parallel image uploads.
* **Advanced viz**: richer sankey and heatmap bindings, graded suggestions.

### **🚀 Improvements**

* **Helm chart 1.0**: `image.tag` defaults to `1.x`; nginx viewer; no default MinIO credentials.
* **MongoDB HA**: Percona PSMDB Operator replaces the Community Operator ([#788](https://github.com/depictio/depictio/pull/788), [#792](https://github.com/depictio/depictio/pull/792)).
* **Rate limiter**: Redis-backed, per IP via `X-Real-IP` ([#787](https://github.com/depictio/depictio/pull/787)).
* **Dependencies**: deltalake, pandas, polars majors.

### **🔒 Security**

* **MinIO password**: 8+ chars, no default, out of the ConfigMap.
* **Pods**: `mongo:8.0.5` and MinIO pinned; `runAsNonRoot`, `drop ALL`.
* **API**: env CORS allowlist replaces `allow_origins=["*"]`; JWT checks RS256/RS512 and `exp` (no alg=none); `/register` cannot set `is_admin`; import needs a user, zip-slip guard; IDOR file delete fixed.
* **Frontend**: JBrowse drops `allow-same-origin`; OAuth open redirect closed; CSP, HSTS, Permissions-Policy headers.
* **S3 and visibility**: `verify=False` -> `settings.minio.verify_tls`; reference dashboards default `is_public=False`.
* **Passwords**: 8+ chars (was 16); `changeme` allowed for the bootstrap admin only; none enforced in single-user mode ([#786](https://github.com/depictio/depictio/pull/786)).
* **Dependencies**: `python-jose` CVEs fixed; `redis` held at 5.2.1 (8.0 starves the event loop).
* **Release scripts**: shell injection fixed ([#790](https://github.com/depictio/depictio/pull/790)).

### **🐛 Bug Fixes**

* Screenshot fonts and timing ([#784](https://github.com/depictio/depictio/pull/784), [#794](https://github.com/depictio/depictio/pull/794)), public mode: Sign In hidden, demo dashboards and sessions kept, anonymous export ([#789](https://github.com/depictio/depictio/pull/789), [#793](https://github.com/depictio/depictio/pull/793)), API key race on replicas ([#791](https://github.com/depictio/depictio/pull/791)), tab menu and modal icons ([#795](https://github.com/depictio/depictio/pull/795)), pandas 3.0 `str` columns, ANSI on piped CLI output; CI and test work ([#782](https://github.com/depictio/depictio/pull/782), [#796](https://github.com/depictio/depictio/pull/796), [#797](https://github.com/depictio/depictio/pull/797)).

---

## Older releases

Releases before v1.0.0, collapsed by series.

??? note "v0.13.x: v0.13.0 to v0.13.12"

    ### **[v0.13.12](https://github.com/depictio/depictio/releases/tag/v0.13.12)** (June 4, 2026)

    !!! success "Patch: cross-DC filter fix"

    * **🐛 Bug Fixes**: cross-DC filters join on the link column instead of returning every row.

    ### **[v0.13.11](https://github.com/depictio/depictio/releases/tag/v0.13.11)** (May 29, 2026)

    !!! success "Patch: cross-DC filter target column"

    * **🐛 Bug Fixes**: a null `target_field` no longer breaks advanced viz or figures.

    ### **[v0.13.10](https://github.com/depictio/depictio/releases/tag/v0.13.10)** (May 29, 2026)

    !!! success "Patch: builder fixes"

    * **🐛 Bug Fixes**: viz suggestions for rarefaction, sankey, sunburst, alpha diversity; text Type step no longer freezes; Save refreshes the screenshot.

    ### **[v0.13.9](https://github.com/depictio/depictio/releases/tag/v0.13.9)** (May 28, 2026)

    !!! success "Patch: admin writes in public mode"

    * **🐛 Bug Fixes**: admins can create projects, CLI tokens and agent configs on public and demo instances.

    ### **[v0.13.8](https://github.com/depictio/depictio/releases/tag/v0.13.8)** (May 28, 2026)

    !!! success "Patch: import, screenshots, Helm ingress"

    * **Helm ingress**: separate `Ingress` objects for MinIO and the API.
    * **🐛 Bug Fixes**: React project import 404, shared creation timestamps, screenshots of duplicated dashboards.

    ### **[v0.13.7](https://github.com/depictio/depictio/releases/tag/v0.13.7)** (May 22, 2026)

    !!! success "Patch: viralrecon Lineage tab"

    * **🐛 Bug Fixes**: the Lineage tab no longer answers 500.

    ### **[v0.13.6](https://github.com/depictio/depictio/releases/tag/v0.13.6)** (May 22, 2026)

    !!! success "Patch: recipe format, screenshot queue"

    * **🐛 Bug Fixes**: viralrecon recipe tables read as TSV; saves skip screenshots under an hour old.

    ### **[v0.13.5](https://github.com/depictio/depictio/releases/tag/v0.13.5)** (May 21, 2026)

    !!! success "Patch: viralrecon seed TSVs"

    * **viralrecon seeds**: 15 recipe outputs bundled, plus `variants_long` and `variant_feature_matrix_canonical` recipes.

    ### **[v0.13.4](https://github.com/depictio/depictio/releases/tag/v0.13.4)** (May 21, 2026)

    !!! success "Patch: bundled viralrecon data"

    * **viralrecon data**: MultiQC and mosdepth files bundled; Coverage and MultiQC tabs need no `kubectl cp`.

    ### **[v0.13.3](https://github.com/depictio/depictio/releases/tag/v0.13.3)** (May 21, 2026)

    !!! success "Patch: seed IDs, public pinning"

    * **Public pinning**: pins stored in `localStorage`.
    * **🐛 Bug Fixes**: viralrecon and two advanced viz demo dashboards no longer 404.

    ### **[v0.13.2](https://github.com/depictio/depictio/releases/tag/v0.13.2)** (May 21, 2026)

    !!! success "Patch: K8s init containers, seeds"

    * **🐛 Bug Fixes**: Helm stuck at `0 READY` (new `initContainerImage.pullPolicy: Always`), viralrecon `DATA_ROOT`, 13 ampliseq transforms, ampliseq 2.16.0 MultiQC filters.

    ### **[v0.13.1](https://github.com/depictio/depictio/releases/tag/v0.13.1)** (May 21, 2026)

    !!! success "Stable: viralrecon seed, MultiQC filters"

    #### **✨ New Features**

    * **nf-core/viralrecon**: fifth bundled seed, 5 dashboards.
    * **`DEPICTIO_DISABLE_EXAMPLE_DASHBOARDS`**: skips seeding reference projects.
    * **`DEPICTIO_WALKTHROUGH_DISABLED`**: hides the onboarding overlay.
    * **Upload hints**: known table shapes get a "Looks like X" badge.

    #### **🚀 Improvements**

    * **Dashboards list**: Owned, Accessed, Public, nf-core, Demo sections; Cmd+Click opens a new tab.
    * **Admin page**: per-project lists, Maintenance card for all seeds.

    #### **🐛 Bug Fixes**

    * Cross-DC filters narrow MultiQC and rarefaction, full-range date picker, reset icon state, non-sample options no longer greyed out.

    ### **[v0.13.0](https://github.com/depictio/depictio/releases/tag/v0.13.0)** (May 20, 2026)

    !!! success "Stable: Advanced Visualization component"

    #### **✨ New Features**

    * **Advanced Visualization (React beta)**: ComplexHeatmap, UpSet, GSEA, rarefaction, ancombc, DA barplot, MA, Lollipop, Dot, QQ, Sunburst, Oncoplot. [Advanced Visualizations](../features/advanced-visualizations.md)
    * **Cards**: `text` variants and multi-metric layouts such as `box_plot`.
    * **Table API**: append, replace and clear endpoints.

    #### **🚀 Improvements**

    * Reset moved to the filters header (React beta); auto screenshots about 2x faster.

??? note "v0.12.x: v0.12.0 to v0.12.2"

    ### **[v0.12.2](https://github.com/depictio/depictio/releases/tag/v0.12.2)** (May 18, 2026)

    !!! success "Stable: Code Mode polish, cross-filter fixes"

    * **Figure Code Mode (React beta)**: help, resizable editor, cross-filter preview, owner only.
    * **Joined tables (React beta)**: marked in the builder; filter-source badge on components.
    * **🐛 Bug Fixes**: no silent fallback to scatter, cross-filtering on scatter only, Plotly reset clears selection, MultiQC samples fall back to `canonical_samples`.

    ### **[v0.12.1](https://github.com/depictio/depictio/releases/tag/v0.12.1)** (May 18, 2026)

    !!! success "Stable: text component, walkthrough"

    * **Text component (React beta)**: rich text plus a **Notes** footer drawer.
    * **Guided walkthrough (React beta)**: first-run tour adapted to each page.
    * **Ownership gating**: only owners see edit controls.

    ### **[v0.12.0](https://github.com/depictio/depictio/releases/tag/v0.12.0)** (May 15, 2026)

    !!! success "Stable: MultiQC lifecycle, cross-DC links"

    #### **♻️ Migration**

    * **Dash to React**: React ships in Beta at `/*-beta`; Dash goes in v0.13.12; canonical URLs in v1.0.0. [Frontend Guidelines](../developer/contributing.md#frontend-guidelines)

    #### **✨ New Features**

    * **MultiQC data collections**: create, append, replace, clear, with a uniformity check.
    * **Cross-DC links**: managed from the viewer.
    * **Map-ready tables (React beta)**: lat/lon **Coordinates** tab in Create DC.
    * **Dashboards and Projects (React beta)**: toolbar, table view, pins, filters.

    #### **🚀 Improvements**

    * Persistent MultiQC prerender store, safer append; Helm rolls pods on ConfigMap or Secret change.

??? note "v0.11.x: v0.11.0 to v0.11.2"

    ### **[v0.11.2](https://github.com/depictio/depictio/releases/tag/v0.11.2)** (May 7, 2026)

    !!! success "Stable: viewer build fixes"

    * **🐛 Bug Fixes**: viewer Docker production bundle, Vite HMR in dev compose.

    ### **[v0.11.1](https://github.com/depictio/depictio/releases/tag/v0.11.1)** (May 6, 2026)

    !!! success "Stable: housekeeping, no user-facing changes"

    ### **[v0.11.0](https://github.com/depictio/depictio/releases/tag/v0.11.0)** (May 6, 2026)

    !!! success "Major: React viewer in Beta"

    #### **✨ New Features**

    * **React viewer (Beta)**: at `/dashboard-beta/{id}`, `/dashboard-beta-edit/{id}` and other `*-beta` pages; linked from Dash.
    * **Realtime refresh (opt-in)**: WebSocket and SSE under `/depictio/api/v1/events/`.
    * **Upload a data collection**: `POST /depictio/api/v1/datacollections/create_from_upload`, no CLI needed.
    * **Dash 4.1**: `dash[async]>=4.1,<5`.

    #### **🚀 Improvements**

    * Public mode disables write actions instead of hiding them; filter-aware MultiQC caching.

    #### **🐛 Bug Fixes**

    * Duplicated components, heatmap nulls and dates, `/projects` 500, map filtering.

??? note "v0.10.x: v0.10.0 to v0.10.3"

    ### **[v0.10.3](https://github.com/depictio/depictio/releases/tag/v0.10.3)** (May 4, 2026)

    !!! success "Stable: extra OCI tags for the Helm chart"

    ### **[v0.10.2](https://github.com/depictio/depictio/releases/tag/v0.10.2)** (May 4, 2026)

    !!! success "Stable: Helm rollouts, CLI Agents"

    * **Helm config checksums**: `helm upgrade` rolls pods on ConfigMap change.
    * **🐛 Bug Fixes**: CLI Agents button works in single-user mode.

    ### **[v0.10.1](https://github.com/depictio/depictio/releases/tag/v0.10.1)** (April 30, 2026)

    !!! success "Stable: nf-core/viralrecon template"

    * **nf-core/viralrecon 3.0.0**: eight data collections, four-tab dashboard. [nf-core/viralrecon](../pipeline-templates/nf-core/viralrecon.md)
    * **Recipes**: `glob_pattern` on `RecipeSource`; `metatype: "Aggregated"` for cross-sample tables. [Recipes](../usage/projects/recipes.md#glob_pattern-per-sample-inputs)

    ### **[v0.10.0](https://github.com/depictio/depictio/releases/tag/v0.10.0)** (April 30, 2026)

    !!! success "Stable: templates, recipes, ampliseq, ingress"

    #### **✨ New Features**

    * **Project templates**: `template_origin`, variables like `DATA_ROOT` and `METADATA_FILE`, dashboard import. [Project Templates](../usage/projects/templates.md)
    * **nf-core/ampliseq 2.16.0**: first reference template, with bundled data.
    * **Python recipes**: Polars, `dc_ref` dependencies, new `source: "transformed"`. [Recipes](../usage/projects/recipes.md)
    * **Helm ingress**: separate MinIO and API ingress, `values-serve.yaml` for [SciLifeLab Serve](https://serve.scilifelab.se/). [Kubernetes installation](../installation/kubernetes.md#ingress)

    #### **🐛 Bug Fixes**

    * Cross-DC link filtering, `/projects` 500, recipe path resolution, stale file cleanup.

??? note "v0.9.x: v0.9.0"

    ### **[v0.9.0](https://github.com/depictio/depictio/releases/tag/v0.9.0)** (March 21, 2026)

    !!! success "Stable: project migrate and cascade delete"

    #### **✨ New Features**

    * **Project migrate**: `depictio-cli migrate` moves a project between instances as a ZIP bundle, with `--overwrite` and a UI flow. [Migrate](../usage/administration/migrate.md)
    * **Cascade delete**: deleting a project removes its workflows, data collections, dashboards and S3 objects. [Project deletion](../usage/projects/guide.md#project-deletion)

    #### **🐛 Bug Fixes**

    * Spurious `migrate` sub-prompt, self-migration S3 copy, export bundle dates and `project_id` mismatch.

??? note "v0.8.x: v0.8.0 to v0.8.2"

    ### **[v0.8.2](https://github.com/depictio/depictio/releases/tag/v0.8.2)** (March 4, 2026)

    !!! success "Stable: CLI config generation off in demo mode"

    #### **🔒 Security**

    * **No CLI configs in public, demo or single-user mode**: `/cli_configs` exposed MinIO root credentials; now disabled, and `POST /generate_agent_config` answers 403.

    ### **[v0.8.1](https://github.com/depictio/depictio/releases/tag/v0.8.1)** (March 4, 2026)

    !!! success "Stable: no blank `/auth` page on fresh installs"

    * **Heatmap title and description**: taxonomy heatmaps accept `title` and `description`.
    * **🐛 Bug Fixes**: blank `/auth` page on a fresh Docker install (shared `depictio_keys` volume, random internal API key), stray `/auth` landings, sidebar burger icon, duplicated data on K8s, Faith PD axis label.

    ### **[v0.8.0](https://github.com/depictio/depictio/releases/tag/v0.8.0)** (March 3, 2026)

    !!! success "Stable: maps, clustered heatmaps, multi-metric cards"

    #### **✨ New Features**

    * **Map component**: scatter, density and choropleth maps with cross-filtering, no API key needed.
    * **GeoJSON data collection type**: boundary files from S3 for choropleth maps.
    * **ComplexHeatmap**: clustered heatmaps with dendrograms as `visu_type: heatmap`, via [plotly-complexheatmap](https://github.com/weber8thomas/plotly-complexheatmap){ target="_blank" }.
    * **Multi-metric cards**: a hero metric plus secondary aggregations in one card.
    * **Filter expressions**: `filter_expr` Polars expressions pre-filter card aggregations and scope interactive component options.
    * **Table title and description**: `title`, `description`, `title_size` and `title_align` above tables.
    * **Debug UI toggle**: `DEPICTIO_DASH_DEBUG_UI` shows the Dash debug UI, hidden by default.
    * **Reference projects**: moved under `depictio/projects/`; ampliseq shows the new map and heatmap.

    #### **🚀 Improvements**

    * **Faster MultiQC loading** through caching.

    #### **🐛 Bug Fixes**

    * Cross-DC filtering for figures, MultiQC and heatmaps, map viewport and theme resets, General Statistics dark mode, screenshot timeouts (now configurable), alpha diversity error bars.

??? note "v0.7.x: v0.7.0 to v0.7.6"

    ### **[v0.7.6](https://github.com/depictio/depictio/releases/tag/v0.7.6)** (February 26, 2026)

    !!! success "Stable: version bump only"

    No user-facing changes.

    ### **[v0.7.5](https://github.com/depictio/depictio/releases/tag/v0.7.5)** (February 25, 2026)

    !!! success "Stable: MultiQC General Statistics table"

    * **MultiQC General Statistics table**: an interactive, searchable table from `multiqc.parquet` general stats.
    * **🐛 Bug Fixes**: endless re-render with linked interactive components.

    ### **[v0.7.4](https://github.com/depictio/depictio/releases/tag/v0.7.4)** (February 25, 2026)

    !!! success "Stable: single-user mode and YAML import fixes"

    #### **✨ New Features**

    * **Ampliseq dashboards**: use relative abundance and ANCOM-BC data.

    #### **🚀 Improvements**

    * **GitHub Codespaces replaces Gitpod**.
    * **Multi-arch Docker images**: arm64 and amd64 in one image.

    #### **🐛 Bug Fixes**

    * YAML import HTTP 400, MultiQC plots ignoring filters, single-user mode (auto-created admin, auto-login, `/auth` redirects to `/dashboards`), stale tokens, docker-compose healthchecks.

    ### **[v0.7.3](https://github.com/depictio/depictio/releases/tag/v0.7.3)** (February 18, 2026)

    !!! success "Stable: demo and public modes, YAML sync overhaul"

    #### **♻️ Migration**

    * **Unauthenticated mode replaced**: a demo mode (guided tour, temporary users) and a read-only public mode take its place.

    #### **✨ New Features**

    * **YAML dashboard sync**: multi-tab export and import, validation in CLI `validate` and `import`, stable component tags.
    * **YAML reference dashboards**: iris, penguins and ampliseq ship YAML definitions.
    * **MultiQC**: DateRangePicker filter, theme switching, readable filter titles.
    * **Fullscreen mode**: native browser fullscreen.

    #### **🚀 Improvements**

    * **Docker Compose**: MinIO embedded, `.env` optional, named MongoDB volume, pinned image versions.
    * **WebSocket on K8s**: connection fixed.
    * **Screenshots**: owner-only, allowed in single-user mode.

    #### **🐛 Bug Fixes**

    * Demo mode glitches, cross-DC filtering for cards, MultiQC stepper metadata, dashboard duplication, duplicate/remove component, missing Add/Edit Tab in single-user mode.

    ### **[v0.7.2](https://github.com/depictio/depictio/releases/tag/v0.7.2)** (February 8, 2026)

    !!! success "Stable: auth mode improvements and a guided tour"

    #### **✨ New Features**

    * **Guided tour** for demo mode.
    * **Dashboard import and export** from the New Dashboard modal.
    * **WebSocket events**: real-time dashboard updates.
    * **Tab management**: create, edit, delete and reorder tabs.
    * **Single User Mode badge** opens `/profile`.

    #### **🐛 Bug Fixes**

    * Scatter selection lost on re-render, dashboard creation in single-user mode, public/demo dashboard visibility.

    ### **[v0.7.1](https://github.com/depictio/depictio/releases/tag/v0.7.1)** (February 4, 2026)

    !!! success "Stable: tab management"

    * **Tab management**: drag-and-drop tab reordering, a smart sidebar and a dashboard/tab breadcrumb.
    * **🐛 Bug Fixes**: the header shows the parent dashboard title.

    ### **[v0.7.0](https://github.com/depictio/depictio/releases/tag/v0.7.0)** (February 3, 2026)

    !!! success "Stable: Image component"

    #### **✨ New Features**

    * **Image component**: Image data collections with gallery and modal views, cross-filtering, CLI registration and YAML import.
    * **API health endpoint**: `/health` for Kubernetes readiness checks (from v0.6.3-b1).

    #### **🐛 Bug Fixes**

    * `DEPICTIO_MONGODB_WIPE` off by default, S3 bucket and cleanup errors on startup.

??? note "v0.6.x: v0.6.0 to v0.6.2"

    ### **[v0.6.2](https://github.com/depictio/depictio/releases/tag/v0.6.2)** (January 29, 2026)

    !!! success "Stable: MultiQC, Kubernetes and screenshot fixes"

    * **🐛 Bug Fixes**: MultiQC re-processing HTTP 400, missing dashboard screenshots on Kubernetes, auth error on stale tokens, duplicate reference projects at startup, reference dashboards now public.

    ### **[v0.6.1](https://github.com/depictio/depictio/releases/tag/v0.6.1)** (January 28, 2026)

    !!! success "Stable: dashboard gallery with screenshots"

    #### **✨ New Features**

    * **Dashboard gallery**: categories, tab count badges and a screenshot carousel with zoom preview.
    * **Auto-screenshots**: the viewer captures dashboard screenshots automatically.

    #### **🚀 Improvements**

    * **Reference projects**: penguins and MultiQC register automatically.

    #### **🐛 Bug Fixes**

    * K8s CORS and screenshots, a Helm switch to disable YAML dashboard sync, premature auth modal error, "Back to Dashboards" link theming.

    ### **[v0.6.0](https://github.com/depictio/depictio/releases/tag/v0.6.0)** (January 25, 2026)

    !!! success "Stable release based on v0.6.0-b18"

    #### **✨ New Features**

    * **Multi-app frontend**: Management (`/`), Viewer (`/dashboard/`) and Editor (`/dashboard-edit/`) apps. ([#615](https://github.com/depictio/depictio/pull/615), [#616](https://github.com/depictio/depictio/pull/616))
    * **Two-panel layout and tabs**: filters left, charts right, tabs with icons and colors.
    * **Universal DC linking**: filter linked data collections without pre-computed joins. ([#640](https://github.com/depictio/depictio/pull/640))
    * **Figure code mode**: live preview, resizable editor, clearer syntax errors. ([#639](https://github.com/depictio/depictio/pull/639))
    * **Table CSV export** with filters and sorting applied. ([#625](https://github.com/depictio/depictio/pull/625))
    * **Celery background jobs** for heavy design-mode computations, on by default, with a Helm worker.
    * **Also new**: YAML dashboard validation, table joins in the CLI ([#634](https://github.com/depictio/depictio/pull/634)), local Delta table caching, faster cards and interactive components ([#616](https://github.com/depictio/depictio/pull/616)), fullscreen button, figure loading indicator ([#622](https://github.com/depictio/depictio/pull/622)), Docker health checks.

    #### **🔒 Security**

    * **Tokens masked in Gunicorn access logs**. ([e22778d9](https://github.com/depictio/depictio/commit/e22778d9))

    #### **🐛 Bug Fixes**

    * **Kubernetes**: `DEPICTIO_FASTAPI_PUBLIC_URL` overridable in ConfigMaps, `api_internal_key.pem` generated at startup, init containers wait for `private_key.pem`, YAML auto-export and watcher off.
    * **Dashboard**: dark-mode slider labels, single scrollbar in edit mode, Ace editor theme switching.

??? note "v0.5.x: v0.5.0 to v0.5.3"

    ### **[v0.5.3](https://github.com/depictio/depictio/releases/tag/v0.5.3)**

    * **🐛 Bug Fixes**: project creation keeps original IDs across K8s instances ([d4a57a5d](https://github.com/depictio/depictio/commit/d4a57a5d)).

    ### **[v0.5.2](https://github.com/depictio/depictio/releases/tag/v0.5.2)**

    #### **✨ New Features**

    * **S3 and projects**: Delta table checks on S3, data collection IDs promoted for joins. ([bc31ff79](https://github.com/depictio/depictio/commit/bc31ff79))
    * **Dashboards**: better filtering, permission checks, resizing, MultiQC metadata, new icons. ([3e259297](https://github.com/depictio/depictio/commit/3e259297))
    * **Helm**: URL pattern helpers for the API and MinIO. ([5a7850f1](https://github.com/depictio/depictio/commit/5a7850f1))

    #### **🐛 Bug Fixes**

    * No horizontal scrollbar, theme switch, Iris demo names ([310a8d9f](https://github.com/depictio/depictio/commit/310a8d9f)).

    ### **[v0.5.1](https://github.com/depictio/depictio/releases/tag/v0.5.1)**

    * **Redis on Kubernetes**, with connectivity tests. ([f86b4f10](https://github.com/depictio/depictio/commit/f86b4f10))
    * **Dashboard UI**: better header and modals, custom subtitle and icon, visible resize handles. ([ba99f97b](https://github.com/depictio/depictio/commit/ba99f97b))

    ### **[v0.5.0](https://github.com/depictio/depictio/releases/tag/v0.5.0)**

    #### **✨ New Features**

    * **MultiQC component**: MultiQC reports in a dashboard, linked to sample metadata. ([2f1e9d31](https://github.com/depictio/depictio/commit/2f1e9d31))
    * **Table column selector and filters**. ([d53caae1](https://github.com/depictio/depictio/commit/d53caae1))
    * **Live updates, new header and faster rendering** of dashboards. ([f8e2f5a1](https://github.com/depictio/depictio/commit/f8e2f5a1))

    #### **🐛 Bug Fixes**

    * Inconsistent plot rendering, theme switch flicker ([02c5e7e4](https://github.com/depictio/depictio/commit/02c5e7e4)).

??? note "v0.4.x: v0.4.0"

    ### **[v0.4.0](https://github.com/depictio/depictio/releases/tag/v0.4.0)**

    * **Faster dashboards** with `flask-caching` and `orjson`, dock-style animations, a live mode toggle, smoother edit mode and theme updates. ([b3bdd21f](https://github.com/depictio/depictio/commit/b3bdd21f))

??? note "v0.3.x: v0.3.0 to v0.3.2"

    ### **[v0.3.2](https://github.com/depictio/depictio/releases/tag/v0.3.2)**

    * **Analytics**: in-house and Google Analytics, plus an admin analytics dashboard. ([956d35f3](https://github.com/depictio/depictio/commit/956d35f3))
    * **Helm**: tuned MinIO and backend resource limits and security context. ([9e681bfc](https://github.com/depictio/depictio/commit/9e681bfc))

    ### **[v0.3.1](https://github.com/depictio/depictio/releases/tag/v0.3.1)**

    * **🐛 Bug Fixes**: Helm limits and auth defaults, joins keep runs apart ([e21ef1eb](https://github.com/depictio/depictio/commit/e21ef1eb)); UMAP disabled for now.

    ### **[v0.3.0](https://github.com/depictio/depictio/releases/tag/v0.3.0)**

    * **Project and data collection management** from modals, with storage size and progress. ([b9cb4727](https://github.com/depictio/depictio/commit/b9cb4727))
    * **Also new**: CLI ASCII logo, temporary user cleanup.
    * **🐛 Bug Fixes**: user code can no longer reassign `df`, figure edit mode ([318c7ae9](https://github.com/depictio/depictio/commit/318c7ae9)).

??? note "v0.2.x: v0.2.0 to v0.2.1"

    ### **[v0.2.1](https://github.com/depictio/depictio/releases/tag/v0.2.1)**

    * **Theming**: `mantine_light` and `mantine_dark` Plotly templates, theme-aware AG Grid. ([04e4069e](https://github.com/depictio/depictio/commit/04e4069e))
    * **Interactive components** restore saved values. ([892de076](https://github.com/depictio/depictio/commit/892de076))
    * **🔒 Security**: EMBL security contexts for unauthenticated mode ([08a6e311](https://github.com/depictio/depictio/commit/08a6e311)), seccompProfile update ([1b18d95a](https://github.com/depictio/depictio/commit/1b18d95a)).
    * **🐛 Bug Fixes**: footer position.

    ### **[v0.2.0](https://github.com/depictio/depictio/releases/tag/v0.2.0)**

    #### **✨ New Features**

    * **Dark and light theme**, new grid, progressive dashboard loading. ([68af2cc0](https://github.com/depictio/depictio/commit/68af2cc0))
    * **Figure code mode**: user code runs restricted (RestrictedPython). ([691a2678](https://github.com/depictio/depictio/commit/691a2678))
    * **Components**: table pagination, inline text, card trends, log sliders, reset buttons. ([99f8e5a2](https://github.com/depictio/depictio/commit/99f8e5a2))
    * **Notes footer** with rich text. ([d226f52b](https://github.com/depictio/depictio/commit/d226f52b))

    #### **🐛 Bug Fixes**

    * AG Grid popups, dark-mode draggables, Google OAuth routes ([19396605](https://github.com/depictio/depictio/commit/19396605)).

??? note "v0.1.x: v0.1.0 to v0.1.1"

    ### **[v0.1.1](https://github.com/depictio/depictio/releases/tag/v0.1.1)**

    * **♻️ Migration**: user upgrade calls no longer take `expiry_minutes` ([b9c5241f](https://github.com/depictio/depictio/commit/b9c5241f)).
    * **Dark and light modes** with auto-theming. ([a851f175](https://github.com/depictio/depictio/commit/a851f175))
    * **🐛 Bug Fixes**: CLI configuration field names, Dash v3 compatibility ([ce91c581](https://github.com/depictio/depictio/commit/ce91c581)).

    ### **[v0.1.0](https://github.com/depictio/depictio/releases/tag/v0.1.0)**

    * **S3 backup and restore**, with CLI commands. ([92ce14ff](https://github.com/depictio/depictio/commit/92ce14ff))
    * **Unauthenticated mode**: anonymous login and upgradable temporary users. ([38ff59d7](https://github.com/depictio/depictio/commit/38ff59d7))
    * **Google OAuth sign-in** and faster cached joins. ([a07364cb](https://github.com/depictio/depictio/commit/a07364cb))

??? note "v0.0.x: v0.0.6"

    ### **[v0.0.6](https://github.com/depictio/depictio/releases/tag/v0.0.6)**

    * **Refresh tokens**, optional user IDs and groups, Flask security scanner. ([6a198be9](https://github.com/depictio/depictio/commit/6a198be9))
    * **🐛 Bug Fixes**: Gunicorn single worker, Helm URLs, MongoDB and MinIO settings ([16d3a92d](https://github.com/depictio/depictio/commit/16d3a92d)).

    ### [v0.0.5](https://github.com/depictio/depictio/releases/tag/v0.0.5)

    * **CLI `run` and `standalone` commands**, clearer S3 service URLs. ([0bad4848](https://github.com/depictio/depictio/commit/0bad4848))
    * **Helm chart**: persistent volumes for keys, ingress defaults and timeouts, Palmer Penguins test data. ([fc0926ac](https://github.com/depictio/depictio/commit/fc0926ac))

    ### [v0.0.4](https://github.com/depictio/depictio/releases/tag/v0.0.4)

    * **Project permissions, users and groups**, first version. ([d17f3690](https://github.com/depictio/depictio/commit/d17f3690))
    * **Authentication**: SAML, token management, API key checks, password editing, registration. ([47e9cd43](https://github.com/depictio/depictio/commit/47e9cd43))
    * **Dashboards**: public or private, screenshots; AMD64 and ARM64 images. ([532e9b7c](https://github.com/depictio/depictio/commit/532e9b7c))
    * **Project-centric backend** on shared depictio-models and Pydantic v2. ([2170ae17](https://github.com/depictio/depictio/commit/2170ae17))

    ### [v0.0.3](https://github.com/depictio/depictio/releases/tag/v0.0.3)

    * **New**: edit components, show or hide component options, reset filters, graph selection, admin dashboard list, copyable public dashboards.

    ### [v0.0.2](https://github.com/depictio/depictio/releases/tag/v0.0.2)

    * **New**: autosave, duplicate and rename dashboards, admin user list; UUID ids.

    ### [v0.0.1](https://github.com/depictio/depictio/releases/tag/v0.0.1)

    * **Initial release**: dashboards with figure, card, interactive and table components, drag and layout, delete.
