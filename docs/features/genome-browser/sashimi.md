---
title: "Genome browser: Sashimi"
description: Splice junctions as arcs over RNA coverage.
glightbox: true
---

# Sashimi

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/sashimi_junctions.webp" src="../../../images/guides/genome-browser/sashimi_junctions.mp4"></video>
</figure>

Splice junctions are drawn as arcs over the coverage of RNA alignments. Pick a locus in the landscape and the reads follow; the browser zooms with the other genome tiles.

```yaml
# on the jbrowse component
show_junctions: true
color_by: sample
ucsc_tracks: [mane]
follow_window: true
```

Used in the [nf-core/rnafusion dashboard template](../../pipeline-templates/nf-core/rnafusion.md).

[:material-arrow-left: All examples](../genome-browser.md#examples)
