---
title: "Performance & Scaling"
icon: material/speedometer
description: "Mechanisms Depictio uses in the render path to handle larger data collections."
---

# :material-speedometer: Performance & Scaling

This page describes the mechanisms in Depictio's render path aimed at handling **larger
data collections**, and the settings that let you tune them for your deployment.

!!! note "Work in progress"
    These changes target the render and caching paths to reduce redundant work; they are
    recent and have **not yet been extensively benchmarked**, so this page describes *what
    each mechanism does* rather than promising specific speed-ups. Real-world figures will
    be added as they are measured.

## Rendering

Most of the work happens server-side, in a Polars + Delta Lake + Celery pipeline, so the
browser receives compact, pre-rendered payloads rather than raw data.

- **Column projection on Delta tables** — figures and cards read only the columns they
  need from the Delta table rather than the full frame, which reduces I/O on wide tables.
- **Polars-native figure building** — figures are built directly from Polars frames,
  avoiding a second in-memory copy of the frame via pandas.
- **Scatter downsampling + WebGL** — scatter-type figures above **50,000 points** are
  downsampled and switched to WebGL rendering, intended to keep large scatter plots
  renderable in the browser rather than sending a multi-megabyte trace.
- **Server-side table pagination** — tables stream rows on demand (capped per request)
  and mount lazily as they scroll into view, so large tables aren't loaded into the
  browser all at once.
- **Compressed responses** — large figure/table JSON is gzip-compressed in transit.

## Render offload

By default Depictio renders figures **adaptively**: cheap, interactive figures render
inline on the API worker, while heavy figures (large frames, MultiQC) are offloaded to
Celery workers so the API stays responsive under concurrent load.

| Setting | Default | Purpose |
| --- | --- | --- |
| `offload_rendering` | `true` | Offload heavy figure rendering to Celery workers instead of building them on the API worker thread. |
| `offload_size_threshold_bytes` | `50 MB` | Frame size above which a render is offloaded rather than run inline. |

These are standard Depictio settings — see the
[environment reference](../installation/env-reference.md) for how to set them
(`DEPICTIO_...` environment variables or the settings file).

## Caching

- **Arrow IPC (LZ4) cache** — cached Polars frames are stored with Arrow IPC + LZ4
  compression in Redis, a more compact serialization than the previous pickle format.
  Frames above the per-item cap are skipped rather than cached, so large frames don't
  silently bloat Redis.
- **MultiQC resident report** — parsed MultiQC reports are kept resident in the worker
  process across renders, so prewarming a dashboard's MultiQC figures no longer
  re-deserializes the full report for every plot.

## Tuning for your deployment

- **Scale workers, not the API** — heavy rendering is CPU-bound. Add Celery worker
  concurrency / replicas (and RAM, since each worker holds its own frame copies) rather
  than overloading the API process.
- **Keep `offload_rendering` on** for multi-user deployments serving large data
  collections; inline rendering only makes sense for small single-user setups.
- **Project your columns** — narrower data collections (only the columns your components
  use) mean less data read and cached.
