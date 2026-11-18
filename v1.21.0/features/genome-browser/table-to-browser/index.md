# Table to browser

[![](../../../images/guides/genome-browser/table_to_browser.webp)](../../../images/guides/genome-browser/table_to_browser.mp4)

Pick a row in a table: the browser moves to its locus and its record card follows. With no row picked, the browser opens on the best row of the collection (`sort_by`). The toolbar steps through the rows, lists them in a picker, and shows where they fall along the genome. A contig spelled `21` in the table and `chr21` in the assembly (or the reverse) is matched.

```
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

Used in the [nf-core/riboseq dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/riboseq/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
