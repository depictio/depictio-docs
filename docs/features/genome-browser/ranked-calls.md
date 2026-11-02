---
title: "Genome browser: Ranked calls"
icon: material/format-list-numbered
description: A numbered track of the best calls, picked and zoomed.
glightbox: true
---

# Ranked calls

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/ranked_rows.webp" src="../../../images/guides/genome-browser/ranked_rows.mp4"></video>
</figure>

`rank_track` adds a track of the best calls, numbered in `sort_by` order and coloured by a category. Pick one, zoom on it, click it: the panel shows its fields, inheritance and each family member's genotype, and the reads sit under it.

```yaml
# on the jbrowse component
locus_from:
  data_collection_tag: ranked_variants
  chrom_column: chrom
  start_column: pos
  sort_by: rank_score
  label_column: call_label
  rank_track: 20                   # the 20 best calls, numbered
  rank_color_by: model_class
```

Used in the nf-core/raredisease dashboard template.

[:material-arrow-left: All examples](index.md#examples)
