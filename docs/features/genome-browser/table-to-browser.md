---
title: "Genome browser: Table to browser"
description: A row picked in a table frames the browser on it.
glightbox: true
---

# Table to browser

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../../images/guides/genome-browser/table_to_browser.webp" src="../../../images/guides/genome-browser/table_to_browser.mp4"></video>
</figure>

Pick a row in a table: the browser moves to its locus and its record card follows. With no row picked, the browser opens on the best row of the collection (`sort_by`). The toolbar steps through the rows, lists them in a picker, and shows where they fall along the genome.

```yaml
# on the jbrowse component
locus_from:
  data_collection_tag: orfs        # a table on the same dashboard
  chrom_column: chrom
  start_column: start
  end_column: end
  sort_by: score                   # opens on the best row
# on the table: one picked row at a time
row_selection_mode: single
```

Used in the [nf-core/riboseq dashboard template](../../pipeline-templates/nf-core/riboseq.md).

[:material-arrow-left: All examples](../genome-browser.md#examples)
