# Navigator

[![](../../../images/guides/genome-browser/chipseq_peaks.webp)](../../../images/guides/genome-browser/chipseq_peaks.mp4)

A `genome_view` tile on the same tab draws the calls of every sample along the whole chromosome, with the browser's window as a band. Zoom on the calls, brush one: the browser opens on it. The browser does not filter on the region, so every track stays open.

```
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

[![](../../../images/guides/genome-browser/atacseq_peaks.webp)](../../../images/guides/genome-browser/atacseq_peaks.mp4)

[![](../../../images/guides/genome-browser/cutandrun_peaks.webp)](../../../images/guides/genome-browser/cutandrun_peaks.mp4)

Used in the [nf-core/chipseq dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/chipseq/index.md), [nf-core/atacseq dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/atacseq/index.md) and [nf-core/cutandrun dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/cutandrun/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
