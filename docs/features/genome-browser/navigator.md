---
title: "Genome browser: Navigator"
icon: material/compass-outline
description: Brush a region on GenomeSpy lanes; the browser opens on it.
glightbox: true
---

# Navigator

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/chipseq_peaks.webp" src="../../../images/guides/genome-browser/chipseq_peaks.mp4"></video>
</figure>

A `genome_view` tile on the same tab draws the calls of every sample along the whole chromosome, with the browser's window as a band. Zoom on the calls, brush one: the browser opens on it. The browser does not filter on the region, so every track stays open.

```yaml
# a tile on the same tab as the browser
- component_type: advanced_viz
  viz_kind: genome_view
  data_collection_tag: peaks
  config:
    chr_col: chr
    pos_col: start
    end_col: end
    score_col: score
    mark: bar
    open_on_view_window: true      # whole chromosome, the browser's window as a band
    interaction_mode: select       # a drag brushes a region
```

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../../images/guides/genome-browser/atacseq_peaks.webp" src="../../../images/guides/genome-browser/atacseq_peaks.mp4"></video>
</figure>

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../../images/guides/genome-browser/cutandrun_peaks.webp" src="../../../images/guides/genome-browser/cutandrun_peaks.mp4"></video>
</figure>

Used in the [nf-core/chipseq dashboard template](../../pipeline-templates/nf-core/chipseq.md), [nf-core/atacseq dashboard template](../../pipeline-templates/nf-core/atacseq.md) and [nf-core/cutandrun dashboard template](../../pipeline-templates/nf-core/cutandrun.md).

[:material-arrow-left: All examples](index.md#examples)
