---
title: "Genome browser: Time course"
icon: material/timeline-clock-outline
description: One colour ramp from the earliest library to the latest.
glightbox: true
---

# Time course

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/genomespy_jbrowse.webp" src="../../../images/guides/genome-browser/genomespy_jbrowse.mp4"></video>
</figure>

The tracks and the navigator lanes share one sequential ramp, so a time course reads down the browser, each library on its own scale. Zoomed out, a track shows the mean of each window.

```yaml
# on the jbrowse component
color_scale:
  column: time_point               # a manifest column
  order_by: time_order
  scheme: viridis
display:
  autoscale: localsd
  summary: avg
```

Used in the nf-core/nascent dashboard template.

[:material-arrow-left: All examples](index.md#examples)
