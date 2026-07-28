---
title: "Performance & Scaling"
icon: material/speedometer
description: "How Depictio keeps large data collections responsive — from the Delta scan to the browser — and the settings that tune it."
---

# :material-speedometer: Performance & Scaling

This page describes how Depictio handles **large data collections** — what the server
does to avoid reading rows it doesn't need, how much data reaches the browser, and which
settings let you tune that for your deployment. The [measured behaviour](#measured-behaviour)
section at the bottom records real numbers from a 17-million-row benchmark project.

The guiding idea is that a dashboard should stay usable at any collection size: work is
pushed as close to the stored data as possible, payloads are bounded by default, and when
a bound is applied it is made visible rather than hidden.

![Where the work got bounded: at each of the three stages — CLI ingest, API serve, viewer render — what used to be materialised in full, and what bounds it now](../images/v0.12/react/schema_perf_stages.png)

## Opening a dashboard

A dashboard can hold dozens of panels, each needing its own request. Rather than
requesting all of them up front, Depictio loads them as you reach them.

![Opening a 30-panel dashboard, before and after the viewport gate: every panel above and just below the fold used to start fetching at mount, where now only the ones actually on screen do](../images/v0.12/react/schema_panel_loading.png)

- **Panels load when they scroll into view.** A panel below the fold shows a placeholder
  and issues **no data request** until you scroll near it, so opening a large dashboard
  stays responsive instead of waiting on every panel first. Advanced-viz, MultiQC and
  JBrowse panels defer their **code chunk** as well, since their renderers fetch on mount;
  figure and table panels load their chunk when they mount but still gate the fetch.
- **Placeholders are skeletons, not spinners**, so the deferred → loading → rendered
  sequence reads as one continuous shimmer.
- **A progress ring and a count** (for example `6/8`) sit beside the dashboard title while
  panels load, then fade out once everything on screen is ready. Hover it for a breakdown:
  how many are still loading, how many failed, and how many are further down the page. If a
  panel failed, the ring stays visible with a red arc rather than fading out on a partly
  broken dashboard.
- **The count covers what is on screen**, not the whole dashboard, so it always reaches
  100%. Scrolling brings more panels in and the count grows to include them, which means
  it can briefly go backwards — that is work which has just started, not a problem.
- **While the dashboard document itself is being fetched**, the Depictio logo animates in
  the centre of the page; no panels are known yet, so there is nothing to count. Under
  `prefers-reduced-motion` the animation is softened rather than removed.

The viewer bundle is split along the same lines: route trees and the heavy visualisation
libraries (Plotly, AG Grid, Cytoscape) load as separate chunks on demand, so a page only
parses the code it actually renders.

!!! info "WebGL budget"
    Browsers allow only a handful of simultaneous WebGL contexts. Past roughly five
    accelerated plots the oldest ones used to lose their context and blank out. Depictio
    now budgets contexts and falls back to a lighter SVG renderer for the plots that miss
    out, so a dense dashboard degrades in quality rather than showing nothing.

## Bounded payloads and the Load-all control

By default every data panel is served a **bounded** slice rather than the whole
collection. Where a bound has been applied, the panel says so, and you can override it.

- **The Load-all button** — an action icon in each panel's hover cluster (alongside
  metadata, fullscreen and reset) toggles between the reduced view and a full load of every
  point or row. Its tooltip warns that this may be slow on large datasets. Pressing it
  again returns to the reduced view.
- **Figures** carry a badge reading e.g. `10,000 / 5,000,000 pts`, or `10,000 pts (all)`
  once fully loaded. Point plots are downsampled above `figure_max_points` (10,000 by
  default); a per-component `max_points` overrides it for a single figure.
- **Tables** page at scan level, so a deep page costs the same as a shallow one. Above
  `table_sort_max_rows` (1,000,000 by default) the server serves rows in natural scan
  order and the **sort control disappears from the column headers** — AG Grid drops the
  chevron and the click handler rather than offering a sort that silently does nothing.
- **Advanced visualisations** are reduced according to what their renderer can survive,
  not by a single global rule:

    | Policy | Applies to | What happens |
    | --- | --- | --- |
    | Uniform sample | embedding, QQ, lollipop, coverage track | The renderer draws one mark per row and reads no aggregate, so a uniform subset is a faithful, lower-resolution picture. |
    | Tail-preserving | volcano, MA, Manhattan | Significant rows are kept whole and the dense middle is strided. A uniform sample of a 17M-row DE table keeps almost none of the hits — the plot would become a cloud with nothing to label. |
    | Never sampled | stacked taxonomy, rarefaction, DA barplot, enrichment, sunburst, dot plot, oncoplot, UpSet, hierarchical heatmap, sankey, phylogenetic | These renderers aggregate client-side (per-sample sums, top-N rankings), so a sample changes the reported *values*, not their resolution. |

    The never-sampled kinds are served whole up to `advanced_viz_no_sample_max_rows`
    (2,000,000 by default). Past that ceiling the request falls back to a uniform sample
    and the chart is marked with an orange **estimated** badge, so an approximation is
    never presented as a total. The badge also appears on the lollipop plot whenever its
    rows were sampled — it is uniformly sampled by policy, but it still aggregates those
    rows into per-gene counts, so the counts are estimates.

## Server-side work

Most of the work happens server-side, in a Polars + Delta Lake + Celery pipeline, so the
browser receives compact, ready-to-draw payloads rather than raw data.

- **Aggregation pushdown** — figures whose result is an aggregate (box plots, histograms)
  are computed *as a query over the Delta scan*. The result is exact; the rows simply never
  leave storage. In the benchmark run below, 125 of 197 figure renders materialised **zero
  rows**.
- **Column projection** — figures and cards read only the columns they need, which reduces
  I/O on wide tables.
- **Filters pushed into the scan** — categorical and temporal filters are kept in a form
  the parquet reader can use, so row groups that cannot match are skipped instead of being
  read and discarded.
- **Delta clustering** — tables are sorted on the columns they actually get filtered by
  before being written, which makes that row-group skipping more effective. This sort is
  skipped when the CLI's opt-in streamed write is enabled, since sorting the whole dataset
  would materialise exactly what streaming avoids.
- **Cross-DC links resolved once** — a link filter is resolved a single time per fan-out and
  evaluated lazily, rather than re-derived for every component that depends on it.
- **Polars-native figure building** — figures are built directly from Polars frames,
  avoiding a second in-memory copy via pandas.
- **Compressed responses** — large figure/table JSON is gzip-compressed in transit.

## Render offload

Depictio renders figures **adaptively**: cheap figures render inline on the API process,
while figures over a source-size threshold are dispatched to Celery workers so the API
stays responsive under concurrent load.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DEPICTIO_CELERY_OFFLOAD_RENDERING` | `false` | Force dashboard render endpoints onto Celery. Left off, offloading is adaptive rather than unconditional. |
| `DEPICTIO_CELERY_OFFLOAD_SIZE_THRESHOLD_BYTES` | `50 MB` | Source-collection size above which a figure render is dispatched to Celery instead of run inline. |
| `DEPICTIO_CELERY_OFFLOAD_TIMEOUT_SECONDS` | `30.0` | Per-request offload timeout before the API returns `504`. |

Only figure renders have a Celery path. Tables, cards, interactive components and the
advanced-viz data endpoint are synchronous handlers, which FastAPI already runs in its own
thread pool — they never needed the escape hatch.

See the [environment reference](../installation/env-reference.md) for how to set these.

## Caching

- **Arrow IPC (LZ4) cache** — cached Polars frames are stored with Arrow IPC + LZ4
  compression in Redis, a more compact serialization than pickle. Frames above the
  per-item cap are skipped rather than cached, so large frames don't silently bloat Redis.
- **MultiQC resident report** — parsed MultiQC reports are kept resident in the worker
  process across renders, so prewarming a dashboard's MultiQC figures doesn't
  re-deserialize the full report for every plot.
- **MultiQC figures prerendered at ingest** *(opt-in)* — the CLI already parses every
  MultiQC report to extract metadata, so it can build the aggregated Plotly figures in that
  same pass and upload them to S3. The render endpoint then serves them directly instead of
  paying a `parse_logs` + `get_plot` build on the first cold open. Enable it with
  `DEPICTIO_INGEST_MULTIQC_PRERENDER=1` on the CLI side; it costs ingest time and S3 storage,
  and only runs on a fresh ingest (on an append the local files cannot reproduce the full
  aggregation, so the existing background build takes over). Collections that never opted in
  are not penalised — a short-lived marker records that a collection has no prerendered
  figures, so the server does a Redis lookup rather than an S3 round-trip per panel.

![A MultiQC figure request: the CLI builds and uploads the figures at ingest, the render endpoint probes the S3 prefix before enqueueing a build, and a Redis presence marker spares collections that never opted in](../images/v0.12/react/schema_multiqc_prerender.png)

<div style="max-width: 1200px; margin: 1.5rem auto 2rem auto;">
<div style="padding: 62.19% 0 0 0; position: relative">
  <iframe
    src="https://player.vimeo.com/video/1213726492?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479&amp;autoplay=1&amp;loop=1&amp;muted=1"
    frameborder="0"
    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
    title="Opening a MultiQC dashboard aggregating many reports in Depictio"
  ></iframe>
  </div>
  <p style="text-align: center; margin-top: 0.5rem; font-style: italic; color: #666;">🎬 Opening a MultiQC dashboard that aggregates <strong>many reports</strong>.</p>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

## Measured behaviour

The numbers below come from a single benchmark run on a linked 3-collection project. They
describe *this* setup — treat them as an order of magnitude for a comparably sized project,
not as a specification.

| | |
| --- | --- |
| Dataset | **17,232,000 rows** across 3 linked collections |
| Size | 0.997 GB raw / **1.492 GB Delta** |
| Host | Apple M1 Max, 10 CPU, 32 GB — Colima VM 8 vCPU / 20 GB |
| API container | 4 CPU, **1 uvicorn worker, dev mode** |
| Celery | 4 CPU / 4 workers |

The single dev worker matters: a production deployment runs several, so these figures are
pessimistic in that respect.

<div style="max-width: 1200px; margin: 1.5rem auto 2rem auto;">
<div style="padding: 62.19% 0 0 0; position: relative">
  <iframe
    src="https://player.vimeo.com/video/1213726629?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479&amp;autoplay=1&amp;loop=1&amp;muted=1"
    frameborder="0"
    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
    title="Opening a 30-component Depictio dashboard on a 17.2 million row project"
  ></iframe>
  </div>
  <p style="text-align: center; margin-top: 0.5rem; font-style: italic; color: #666;">🎬 Opening a <strong>30-component</strong> dashboard on the linked project described above. Captured in the browser, so what you see includes rendering and painting, not only the server timings tabulated below.</p>
</div>

### Opening a dashboard

Every component fetched at once. *First chart* is the first figure or advanced viz to
appear; from 8 components up, the first thing to land **is** a chart.

| Components (timed) | Cache | First component | First chart | All components |
| --- | --- | --- | --- | --- |
| 4 (9) | cold | 96 ms | 628 ms | 3.7 s |
| 4 (9) | warm | 65 ms | 522 ms | 2.2 s |
| 8 (13) | warm | 88 ms | 129 ms | 1.7 s |
| 16 (21) | warm | 141 ms | 141 ms | 3.3 s |
| 32 (37) | warm | 214 ms | 214 ms | 14.3 s |

The parenthesised number is the dashboard's full panel count; the leading number is how
many of those issue a timed render. Passive panels (text, interactive widgets reading
precomputed specs) are on the page but not measured — so the last row is a 37-panel
dashboard, not a 32-panel one.

### Changing a filter

Across the 3 linked collections, with no round hitting a cache.

| Components | Starts responding | Fully caught up | Worst round |
| --- | --- | --- | --- |
| 4 | 618 ms | **1.1 s** | 2.4 s |
| 8 | 529 ms | **1.8 s** | 3.3 s |
| 16 | 567 ms | **3.3 s** | 4.1 s |
| 32 | 843 ms | **8.1 s** | 10.3 s |

### Latency per component

All 718 successful renders, every phase. p50 is the median; p95 is the tail.

| Component | p50 | p95 |
| --- | --- | --- |
| interactive | 74 ms | 181 ms |
| card | 124 ms | 789 ms |
| figure · scatter | 486 ms | 3.8 s |
| figure · histogram | 775 ms | 3.3 s |
| table | 780 ms | 2.0 s |
| advanced viz · volcano | 931 ms | 5.5 s |
| advanced viz · MA | 1.1 s | 5.4 s |
| figure · box | 1.2 s | 7.9 s |

### How much data was touched

| | |
| --- | --- |
| Figure renders materialising **zero rows** | **125 of 197** (box, histogram) |
| Largest frame held in memory, any render | **1.5 MB** |
| Cross-collection filter translation | 69 ms median |

Median rows pulled into memory per render: **0** for box and histogram (computed as an
aggregation over the scan, exact), 100 for a table page, 40,000 for a scatter, and
5,741,054 for volcano/MA.

!!! warning "Read these numbers with their caveats"
    - One run, one sample per cell. The `32 (37)` *warm* full load (14.3 s) is slower than
      its cold equivalent and is unexplained — do not build a scaling claim on that row.
    - Only the `4 (9)` cold row is a genuine first visit; the other sizes shared an
      already-ingested project.
    - "Cold" means server caches are empty. Delta files may still sit in the OS or MinIO
      page cache, so it is a lower bound on a truly cold machine.
    - **No before/after comparison is claimed.** The pre-change baseline was measured on a
      differently loaded machine, so these are absolute measurements of the current build,
      not a speed-up.

## Tuning knobs

All are `DEPICTIO_PERFORMANCE_`-prefixed environment variables; see the
[environment reference](../installation/env-reference.md).

| Variable | Default | Purpose |
| --- | --- | --- |
| `FIGURE_MAX_POINTS` | `10000` | Target marker count for point plots before downsampling. Per-component `max_points` overrides it. |
| `FIGURE_MAX_LOAD_ROWS` | `500000` | Row ceiling loaded from Delta for a point-plot or code-mode figure. Bypassed on a full load. |
| `TABLE_SORT_MAX_ROWS` | `1000000` | Post-filter row count above which a table is served unsorted and the sort affordance is dropped. `0` disables the gate. |
| `ADVANCED_VIZ_NO_SAMPLE_MAX_ROWS` | `2000000` | Row ceiling for the never-sampled viz kinds. Past it they fall back to a sample and are badged *estimated*. `0` means unbounded. |
| `ADVANCED_VIZ_TAIL_P_THRESHOLD` | `0.05` | Significance cutoff below which a volcano/Manhattan row is kept whole. A renderer's own threshold wins over this fallback. |
| `ADVANCED_VIZ_TAIL_EFFECT_THRESHOLD` | `1.0` | Same, for kinds whose tail is a signed effect size (MA's log2 fold change). |
| `BOX_SAMPLE_ROWS_PER_GROUP` | `0` | Rows sampled per box-plot group before computing quartiles. `0` computes them exactly. |
| `BOX_SAMPLE_MAX_GROUPS` | `64` | Group count above which box quartiles are always computed exactly — grouped quantiles get cheaper as cardinality rises. |

## Tuning for your deployment

- **Scale workers, not the API** — heavy figure rendering is CPU-bound. Add Celery worker
  concurrency or replicas (and RAM, since each worker holds its own frame copies) rather
  than overloading the API process. Running more than one uvicorn worker matters too.
- **Project your columns** — narrower data collections (only the columns your components
  use) mean less data read and cached.
- **Leave the render caps at their defaults** unless a specific panel needs more. Raising
  `FIGURE_MAX_POINTS` costs payload size and browser draw time for every user, whereas the
  per-panel **Load all** button gives the one person who needs the full picture a way to
  ask for it.
- **`BOX_SAMPLE_ROWS_PER_GROUP` is not a free win.** It trades a sort for an *extra scan*:
  the exact extremes have to be read before the per-group strides are known. On warm local
  parquet that was worth it at 17M rows; on a cold S3-backed Delta table the extra read can
  cost more than the sort it removes. Enable it only where the sort has been measured to be
  the bottleneck.
