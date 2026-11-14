---
title: "What's new since your last visit"
description: "Turn on changes since your last visit, then read what moved on a dashboard: the What's new panel, Overlay and Split, Before | Now on a tile, and the notifications bell."
glightbox: true
---

# What's new since your last visit <small>(v1.21.0+)</small>

When you come back to a dashboard, Depictio shows what changed since you last looked: new data, edited components and new comments. On most figures it also marks which points, bars or samples are new.

<!-- video: whats-new/whats-new-overlay-split | a returning reader opens What's new, switches Off, Overlay, Split, then turns on Hide what you had seen -->

## Before you start

- Depictio **v1.21.0** or later.
- The feature is off by default. An administrator turns it on with `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true`.
- `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_MARK_MODE` sets the default mark mode: `sticky` (the default) or `previous_visit`.
- On Kubernetes, set both in the chart's `backend.env`. `depictio local up` passes them through from your shell.
- The live toast of the bell also needs `DEPICTIO_EVENTS_ENABLED=true` ([Realtime events](../usage/guides/realtime-events.md)). Without it, the bell still polls.

```bash
DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true depictio local up
```

## 1. Open the What's new panel

Open a dashboard you have visited before. The **What's new** key sits in the header, beside settings and theme, with the number of changes on its corner.

<!-- shot: whats-new/key | dashboard header with the What's new key and its count badge -->

Click it. The panel lists the changes in three sections: **Data**, **Dashboard** and **Comments**. A Dashboard row links to the version that made the change, and a Comment row opens its thread.

<!-- shot: whats-new/panel | the What's new panel with Data, Dashboard and Comments sections and Mark as seen -->

## 2. See the changes on the figures

Under **Show on the dashboard**, pick **Off**, **Overlay** or **Split**.

- **Overlay** marks what is new on every changed figure. New points are ringed, removed points are ghosted, and a bar's previous value is outlined. What was already there fades.
- **Split** draws each figure twice: what is new beside what you had seen. Cards compare the two sides.

<!-- shot: whats-new/overlay-scatter | a scatter under Overlay, new points ringed and old ones faded -->
<!-- shot: whats-new/overlay-multiqc | a MultiQC figure under Overlay, new samples in colour and seen samples faded -->
<!-- shot: whats-new/split | figures under Split, one panel per side with the split legend -->

Under Overlay, turn on **Hide what you had seen** to draw only the new runs or new MultiQC samples.

<!-- shot: whats-new/hide-seen | Overlay with Hide what you had seen switched on, only new rows drawn -->

When a table gained runs, its Data row offers **View new rows**: the new rows on top, the rows you had seen faded below. **Open in project** opens the same rows in the project's Data table.

## 3. Compare one tile

A changed tile carries a dot. Its menu holds **Mark as seen**, **Compare with last visit** and **Before | Now**.

<!-- shot: whats-new/tile-menu | the dot menu of a changed tile with Mark as seen, Compare with last visit, Before | Now -->

**Compare with last visit** turns the overlay on for that tile only. **Before | Now** opens a read-only modal with **Before (your last visit)** beside **Now**, both drawn with the same filters.

<!-- shot: whats-new/before-now | the Before | Now modal, Before (your last visit) on the left, Now on the right -->
<!-- video: whats-new/before-now | open Before | Now from a tile's dot menu and compare the two panes -->

## 4. Mark the changes as seen

Click **Mark as seen** in the panel once you have read everything. The count goes back to zero, and the next changes start from here.

Under **Show changes**, choose when the baseline moves:

- **Until I mark them seen**: changes stay listed until you click **Mark as seen**.
- **Since my previous visit**: each visit moves the baseline.

The same choice sits in your profile, under **Changes since your last visit**.

<!-- shot: whats-new/mark-mode | the Show changes select with Until I mark them seen and Since my previous visit -->

## 5. Follow changes from the bell

The notifications bell in the sidebar lists the dashboards and projects with changes. It checks every 60 seconds and shows a toast when an ingestion finishes. Each item links to the dashboard, or to the project's **Runs** tab on that run.

Clear one item with its check mark, or all of them with **Mark all as seen**.

<!-- shot: whats-new/bell | the notifications bell open, with items and Mark all as seen -->

## 6. Find your last visit in History

In the editor, the History section tags the version you last viewed **Last viewed**.

<!-- shot: whats-new/history-last-viewed | editor History with a version tagged Last viewed -->

## Good to know

- The first visit shows nothing: it sets the baseline.
- A visit is recorded 10 seconds after the page opens.
- Your own edits and comments never count. Ingestions do, even ones you ran.
- Moving or resizing a tile is not a change.
- An ingestion that rewrites identical rows is not a change.
- Anonymous and public readers keep their mark in the browser. The bell is hidden for them.
- Code-mode figures cannot be overlaid. Split draws them once per side.
- Split and **Hide what you had seen** need something new beside something seen: a new run, or new MultiQC samples. A run ingested again in place shows only in **Before | Now**.
- A MultiQC report overwritten in place keeps its storage key, so its **Before** shows today's report.
- A mark lists at most 5000 samples per collection. Past that, new samples are counted but not listed.
- The editor, a `?version=` preview and the read-only `?before_run=` view never move your mark.

## See also

- [Compare runs](compare-runs.md)
- [Watch the data update](data-updates.md)
- [MultiQC: compare runs](../features/multiqc.md#compare-runs)
- [Dashboard and data versions](../features/versioning.md#history)
- [Comments and annotations](../features/comments-annotations.md)
