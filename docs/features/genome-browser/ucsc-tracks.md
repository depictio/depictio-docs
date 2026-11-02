---
title: "Genome browser: UCSC tracks"
description: Tracks of the UCSC catalogue next to the run's own.
glightbox: true
---

# UCSC tracks

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/ucsc_and_tracks.webp" src="../../../images/guides/genome-browser/ucsc_and_tracks.mp4"></video>
</figure>

Any bigWig, bigBed or VCF track of the UCSC Genome Browser catalogue for the assembly opens next to the collection's tracks. The builder searches the catalogue by name; each track keeps its own menu, and force load lifts the download limit.

```yaml
# on the jbrowse component
ucsc_tracks: [clinvarMain, dbSnp155Common]
fetch_size_limit_mb: 5
```

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../../images/guides/genome-browser/ucsc_builder.webp" src="../../../images/guides/genome-browser/ucsc_builder.mp4"></video>
</figure>

Used in the [nf-core/viralrecon dashboard template](../../pipeline-templates/nf-core/viralrecon.md).

[:material-arrow-left: All examples](../genome-browser.md#examples)
