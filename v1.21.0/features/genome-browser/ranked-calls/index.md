# Ranked calls

[![](../../../images/guides/genome-browser/ranked_rows.webp)](../../../images/guides/genome-browser/ranked_rows.mp4)

`rank_track` adds a track of the best calls, numbered in `sort_by` order and coloured by a category. Pick one, zoom on it, click it: the panel shows its fields, inheritance and each family member's genotype, and the reads sit under it.

```
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

The ranked-variant counter and **Prev**/**Next** also work for visitors of a public dashboard.

Used in the nf-core/raredisease dashboard template.

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
