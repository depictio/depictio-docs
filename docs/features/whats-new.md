---
title: "What's new since your last visit"
icon: material/new-box
description: "What changed on a dashboard since you last looked: the What's new key and panel, Off, Overlay and Split, the changed-tile dot, Before | Now, mark modes, the notifications bell and the read-only views."
glightbox: true
---

# :material-new-box: _"What's new"_ since your last visit <small>(v1.21.0+)</small>

When you come back to a dashboard, _"What's new"_ lists what changed since you last looked: new data, edited components and new comments. On most figures it also marks which points, bars or samples are new.

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../images/guides/whats-new/whats-new-overlay-split.webp" src="../../images/guides/whats-new/whats-new-overlay-split.mp4"></video></figure>

## Turn it on { #turn-it-on }

_"What's new"_ is off by default. An administrator turns it on on the backend:

| Variable | Default | Effect |
|----------|---------|--------|
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED` | `false` | Master switch. Off, nothing on this page shows |
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_MARK_MODE` | `sticky` | Default [mark mode](#mark-modes) for readers who have not chosen one: `sticky` or `previous_visit` |
| `DEPICTIO_EVENTS_ENABLED` | `false` | Optional. Adds the live toast of the [bell](#notifications-bell) when an ingestion finishes. Without it, the bell still polls |

On Kubernetes, set them in the chart's `backend.env`. `depictio local up` passes them through from your shell:

```bash
DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true depictio local up
```

See [Dashboard Versions](../installation/env-reference.md#dashboard-versions) and [Real-time Events](../usage/guides/realtime-events.md).

## The What's new key and panel { #panel }

The **What's new** key sits in the dashboard header, beside settings and theme, with the number of changes on its corner. It shows only when something changed since your mark. The project page has the same key among its header actions.

[![Dashboard header with the What's new key and its count badge](../images/guides/whats-new/whats_new_key_light.webp#only-light){ width="496" }](../images/guides/whats-new/whats_new_key_light.webp){target=_blank}
[![Dashboard header with the What's new key and its count badge](../images/guides/whats-new/whats_new_key_dark.webp#only-dark){ width="496" }](../images/guides/whats-new/whats_new_key_dark.webp){target=_blank}

[![The What's new panel: Off, Overlay and Split, the run chips, new runs under Data, and Mark as seen](../images/guides/whats-new/whats_new_panel_light.webp#only-light){ width="265" }](../images/guides/whats-new/whats_new_panel_light.webp){target=_blank}
[![The What's new panel: Off, Overlay and Split, the run chips, new runs under Data, and Mark as seen](../images/guides/whats-new/whats_new_panel_dark.webp#only-dark){ width="265" }](../images/guides/whats-new/whats_new_panel_dark.webp){target=_blank}

The panel lists the changes in three sections:

| Section | Lists | Row action |
|---------|-------|------------|
| **Data** | New runs and rows per collection, MultiQC reports added, refreshed or removed, failed ingestions | **View new rows**: the new rows on top, the rows you had seen faded below. **Open in project**: the same rows in the project's Data table |
| **Dashboard** | Components and tabs added, edited or removed, with who made the change | Links to the version that made it |
| **Comments** | New threads and replies | Opens the thread |

**Mark as seen** in the panel header resets the count: the next changes start from here.

## Off, Overlay and Split

**Show on the dashboard** draws the changes on every changed figure at once:

| Mode | What the figures show |
|------|-----------------------|
| **Off** | The figures as they are now |
| **Overlay** | Each new run in its own colour, the runs you had seen in grey, in one panel. In a MultiQC figure the samples you had seen fade, and in a table the rows of runs you had seen fade |
| **Split** | Each figure drawn once per side: all runs, each new run, and what you had seen. Cards compare the sides |

The chips under the modes pick the runs: **All new runs**, or one run. With one run picked, Split draws **All**, that run and the **Other runs**.

[![A scatter under Overlay, each new run in its colour and the runs seen before in grey](../images/guides/whats-new/overlay_scatter_light.webp#only-light){ width="560" }](../images/guides/whats-new/overlay_scatter_light.webp){target=_blank}
[![A scatter under Overlay, each new run in its colour and the runs seen before in grey](../images/guides/whats-new/overlay_scatter_dark.webp#only-dark){ width="560" }](../images/guides/whats-new/overlay_scatter_dark.webp){target=_blank}

[![A bar chart and a violin plot under Overlay, the new runs coloured and the runs seen before in grey](../images/guides/whats-new/overlay_figures_light.webp#only-light){ width="800" }](../images/guides/whats-new/overlay_figures_light.webp){target=_blank}
[![A bar chart and a violin plot under Overlay, the new runs coloured and the runs seen before in grey](../images/guides/whats-new/overlay_figures_dark.webp#only-dark){ width="800" }](../images/guides/whats-new/overlay_figures_dark.webp){target=_blank}

[![Cards and figures under Split on run_09: All, New: run_09 and Other runs side by side](../images/guides/whats-new/split_view_light.webp#only-light){ width="800" }](../images/guides/whats-new/split_view_light.webp){target=_blank}
[![Cards and figures under Split on run_09: All, New: run_09 and Other runs side by side](../images/guides/whats-new/split_view_dark.webp#only-dark){ width="800" }](../images/guides/whats-new/split_view_dark.webp){target=_blank}

[![A bar chart and a violin plot under Split on run_09, one panel per side](../images/guides/whats-new/split_figures_light.webp#only-light){ width="800" }](../images/guides/whats-new/split_figures_light.webp){target=_blank}
[![A bar chart and a violin plot under Split on run_09, one panel per side](../images/guides/whats-new/split_figures_dark.webp#only-dark){ width="800" }](../images/guides/whats-new/split_figures_dark.webp){target=_blank}

Split compares runs: every Delta row carries the run that wrote it (`depictio_run_id`), so the two sides are the new runs and the runs you had seen. MultiQC rows have no run column and split on new samples instead (see [MultiQC: compare runs](multiqc.md#compare-runs)). The two sides are temporary groups: never saved and never applied as a filter.

### Hide what you had seen

Under **Overlay**, the **Hide what you had seen** switch draws only the new runs or the new MultiQC samples. It needs the same two sides as Split.

[![Overlay with Hide what you had seen switched on, only new rows drawn](../images/guides/whats-new/hide_seen_light.webp#only-light)](../images/guides/whats-new/hide_seen_light.webp){target=_blank}
[![Overlay with Hide what you had seen switched on, only new rows drawn](../images/guides/whats-new/hide_seen_dark.webp#only-dark)](../images/guides/whats-new/hide_seen_dark.webp){target=_blank}

## The changed-tile dot

A tile whose definition or data changed carries a dot. Hover it for what changed; click it for its menu.

[![The dot menu of a changed tile with Mark as seen, Compare with last visit, Before | Now](../images/guides/whats-new/tile_dot_menu_light.webp#only-light)](../images/guides/whats-new/tile_dot_menu_light.webp){target=_blank}
[![The dot menu of a changed tile with Mark as seen, Compare with last visit, Before | Now](../images/guides/whats-new/tile_dot_menu_dark.webp#only-dark)](../images/guides/whats-new/tile_dot_menu_dark.webp){target=_blank}

| Item | What it does |
|------|--------------|
| **Mark as seen** | Dismisses this tile only. It stays dismissed while its definition and data stay the same |
| **Compare with last visit** | Turns the overlay on for this tile only. Figures, MultiQC and advanced visualisations |
| **Before \| Now** | A read-only modal with **Before (your last visit)** beside **Now**, both drawn with the same filters |

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../images/guides/whats-new/before-now.webp" src="../../images/guides/whats-new/before-now.mp4"></video></figure>

## Mark modes

Your mark is the state you last acknowledged. **Show changes** in the panel, or **Changes since your last visit** in your profile, chooses when it moves:

| Choice | Value | The mark moves |
|--------|-------|----------------|
| **Until I mark them seen** | `sticky` | Only on **Mark as seen** |
| **Since my previous visit** | `previous_visit` | On every visit |

[![The Changes since your last visit setting with Until I mark them seen and Since my previous visit](../images/guides/whats-new/profile_mark_mode_light.webp#only-light)](../images/guides/whats-new/profile_mark_mode_light.webp){target=_blank}
[![The Changes since your last visit setting with Until I mark them seen and Since my previous visit](../images/guides/whats-new/profile_mark_mode_dark.webp#only-dark)](../images/guides/whats-new/profile_mark_mode_dark.webp){target=_blank}

The first visit sets the mark and shows nothing. A visit is recorded 10 seconds after the page opens. The editor, a `?version=` preview and the [read-only views](#read-only-views) never move it.

## Notifications bell { #notifications-bell }

The bell in the sidebar lists the dashboards and projects that changed since your mark. It checks every 60 seconds, and shows a toast when an ingestion finishes (with `DEPICTIO_EVENTS_ENABLED`). Each item links to the dashboard, or to the project's **Runs** tab on that run. Its check mark clears one item, **Mark all as seen** clears them all.

[![The notifications bell open, with items and Mark all as seen](../images/guides/whats-new/notifications_bell_light.webp#only-light)](../images/guides/whats-new/notifications_bell_light.webp){target=_blank}
[![The notifications bell open, with items and Mark all as seen](../images/guides/whats-new/notifications_bell_dark.webp#only-dark)](../images/guides/whats-new/notifications_bell_dark.webp){target=_blank}

## Last viewed in History

In the editor, **Settings → History** tags the version you last viewed **Last viewed**. See [The History section](versioning.md#history).

[![Editor History with a version tagged Last viewed](../images/guides/whats-new/editor_history_light.webp#only-light){ width="685" }](../images/guides/whats-new/editor_history_light.webp){target=_blank}
[![Editor History with a version tagged Last viewed](../images/guides/whats-new/editor_history_dark.webp#only-dark){ width="685" }](../images/guides/whats-new/editor_history_dark.webp){target=_blank}

## Read-only views { #read-only-views }

Two URL parameters open a dashboard with changes marked, without touching anyone's mark. **Mark as seen** is absent there.

| URL | Shows | Header key |
|-----|-------|------------|
| `/dashboard/<id>?since=<ISO date>` | What changed since that date | **Changes** |
| `/dashboard/<id>?before_run=<run id>` | What one ingestion run changed. Opened by **Compare** in the project's Runs tab, see [Runs and run comparison](runs.md#compare-a-dashboard-with-a-run) | **This ingestion** |

## Who holds the mark

| Reader | Where the mark lives |
|--------|----------------------|
| Signed in | On the server, per dashboard and per project |
| Anonymous, temporary or public-mode guest | In the browser. The bell is hidden |

Deleting a dashboard or a project deletes its marks.

## What counts as a change

- Your own edits and comments never count. Ingestions do, even ones you ran.
- Moving or resizing a tile is not a change.
- An ingestion that rewrites identical rows is not a change.

## Limits

- **Overlay** covers standard figures, MultiQC and advanced visualisations. Code-mode figures cannot be overlaid; **Split** draws them once per side.
- **Before | Now** draws standard figures and MultiQC. For an advanced visualisation it is disabled (**Standard figures only, for now**).
- **Split** and **Hide what you had seen** need something new beside something seen: a new run, or new MultiQC samples. A run ingested again in place shows only in **Before | Now**.
- A MultiQC report overwritten in place keeps its storage key, so its **Before** shows today's report.
- A mark lists at most 5000 samples per collection. Past that, new samples are counted but not listed.

## See also

- [Runs and run comparison](runs.md)
- [MultiQC: compare runs](multiqc.md#compare-runs)
- [Dashboard and data versions](versioning.md#history)
- [Comments and annotations](comments-annotations.md)
