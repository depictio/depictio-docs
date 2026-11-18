# Breakpoints

[![](../../../images/guides/genome-browser/fusion_chord.webp)](../../../images/guides/genome-browser/fusion_chord.mp4)

With a `mate`, the browser shows both sides of a call side by side. The breakpoint view joins them by their split reads and discordant pairs, and the circular view draws every structural variant of the tracks as a chord. In the clip, a chord tile picks the fusions and both breakpoints follow.

```
# on the jbrowse component
read_pairs_display: arcs         # discordant pairs as arcs
views: [breakpoint, circular]
circular_categories: [Structural variants]   # manifest categories the circle draws
locus_from:
  data_collection_tag: fusions
  chrom_column: chrom_a
  start_column: pos_a
  mate: {chrom_column: chrom_b, start_column: pos_b}
```

Used in the [nf-core/rnafusion dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/rnafusion/index.md) and [nf-core/oncoanalyser dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/oncoanalyser/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
