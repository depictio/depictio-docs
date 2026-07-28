---
title: "Real-time Events"
description: "Enable live, WebSocket-driven dashboard refresh so dashboards update automatically as new data is ingested."
---

# :material-lightning-bolt: Real-time Events

Real-time events let a dashboard **refresh itself over a WebSocket** the moment the data
behind it changes — no manual reload, no polling. When new data is ingested into a data
collection, subscribed dashboards refetch and re-render automatically: new rows appear,
figures recompute, and updated items briefly highlight.

This makes Depictio suitable for **live feeds** — an instrument streaming acquisitions, a
pipeline emitting results batch by batch, or any process that keeps appending to a data
collection.

---

## <span style="color: #E53935;">:material-video:</span> Video example

<div style="max-width: 1200px; margin: 1rem auto 2rem auto;">
  <div style="padding: 62.19% 0 0 0; position: relative">
    <iframe
      src="https://player.vimeo.com/video/1213687131?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
      frameborder="0"
      allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
      title="Real-time events streaming into a Depictio dashboard"
    ></iframe>
  </div>
  <p style="text-align: center; margin-top: 0.5rem; font-style: italic; color: #666;">🎬 <strong>Real-time events in action:</strong> a virtual-microscopy simulator streams acquisitions into a live dashboard</p>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

In this recording, a virtual-microscopy acquisition simulator stands in for the instrument.
Each acquisition is segmented and pushed to Depictio through `/deltatables/upsert`, which
broadcasts an event on the WebSocket. The dashboard on the left is open the whole time and is
never reloaded: it refetches on every broadcast, so its figures and cards keep up with the
acquisitions streaming in the terminal on the right.

---

## How it works

The refresh is driven entirely by data ingestion — there is no separate "push" API to call:

```text
producer ingests / upserts a data collection
        │  (depictio-cli run …, or a POST to /deltatables/upsert)
        ▼
API re-reads the Delta table, recomputes column specs, bumps its version
        │
        ▼
broadcasts a `data_collection_updated` event on the WebSocket channel
        │  (/depictio/api/v1/events/ws)
        ▼
subscribed dashboards refetch and re-render (updated items highlight)
```

Any producer that re-ingests or upserts a data collection triggers this — the CLI does it on
every `depictio-cli run`, and an external instrument or pipeline can do the same by POSTing to
the `/deltatables/upsert` endpoint.

---

## Enable it

Real-time refresh activates only when **all** of the following hold.

### 1. Turn the system on (server)

Set the master switch and make sure a Redis instance is reachable (events are fanned out to
viewers via Redis pub/sub):

```bash
DEPICTIO_EVENTS_ENABLED=true
```

The most relevant variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEPICTIO_EVENTS_ENABLED` | `false` | Master switch — nothing happens until this is `true` |
| `DEPICTIO_EVENTS_REDIS_HOST` | `redis` | Redis host used for pub/sub |
| `DEPICTIO_EVENTS_DEBOUNCE_MS` | `1000` | Coalesce bursts of rapid updates (ms) |

See the [Environment Variables Reference](../../installation/env-reference.md#real-time-events)
for the full `DEPICTIO_EVENTS_*` list (Redis port/password/db, WebSocket heartbeat and
timeout, change streams).

### 2. Opt the project in

Real-time is **opt-in per project**. Add a top-level `realtime` block to the project's
`project.yaml`:

```yaml
realtime:
  enabled: true
  debounce_ms: 500   # optional; overrides the server default for this project
```

Projects without this block never open a WebSocket, and their dashboards show no live
indicator.

### 3. Open the dashboard

Open any dashboard in an opted-in project. A **real-time indicator** appears and turns green
once the viewer has subscribed. From then on the dashboard updates on its own whenever the
underlying data collection is re-ingested.

---

## Driving updates

Once enabled, any of these will move a live dashboard:

- **Re-ingest with the CLI** — `depictio-cli run --project-config-path <project.yaml> …`
  re-scans and upserts the data collection, which broadcasts the refresh.
- **An external producer** — an instrument or pipeline that POSTs new data to the
  `/deltatables/upsert` API endpoint (with a valid token) triggers the same path. This is the
  intended integration point for a live experimental feed.

### Try it locally

The bundled `adapt_feedb_ms` demo project ships with the `realtime` block already set and a
small synthetic driver that needs no extra dependencies — just the CLI and a token:

```bash
cd depictio/projects/test/adapt_feedb_ms
./stream_test.sh reset       # seed a couple of rows and ingest
./stream_test.sh stream 3    # append one row every 3s until Ctrl+C
```

Open the project's dashboard and watch each tick land live: new gallery items, recomputed
cards, and a moving timeline — with no manual refresh.

---

## Requirements & notes

- **Redis** is required for pub/sub when events are enabled.
- **MongoDB change streams** (`DEPICTIO_EVENTS_MONGODB_CHANGE_STREAMS_ENABLED`, on by default)
  require MongoDB to run as a **replica set**.
- **Reverse proxy** — the WebSocket route `/depictio/api/v1/events/ws` needs the HTTP upgrade
  proxied. If you front Depictio with nginx, forward the `Upgrade` and `Connection` headers on
  that path, and allow `connect-src 'self' ws: wss:` in your Content-Security-Policy.
- **Authentication** — the WebSocket carries its JWT as a `token` query parameter (browsers
  can't set `Authorization` headers on WS connections) and is permission-checked against the
  dashboard's project at viewer level before any events are delivered.
