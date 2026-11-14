---
title: "Genome browser: Browser to dashboard"
icon: material/cursor-default-click
description: A click on a feature filters the dashboard on its sample.
glightbox: true
---

# Browser to dashboard

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/browser_to_dashboard.webp" src="../../../images/guides/genome-browser/browser_to_dashboard.mp4"></video>
</figure>

Click a feature in the browser: the dashboard filters on the sample of its track, and the navigator above keeps that sample's calls. With `selection_mode: visible_tracks`, the set of open tracks is the selection instead.

```yaml
# on the jbrowse component
selection_enabled: true
selection_column: sample           # default: the collection's sample_column
```

Used in the [nf-core/viralrecon dashboard template](../../pipeline-templates/nf-core/viralrecon.md).

[:material-arrow-left: All examples](index.md#examples)
