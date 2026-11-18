# Sashimi

[![](../../../images/guides/genome-browser/sashimi_junctions.webp)](../../../images/guides/genome-browser/sashimi_junctions.mp4)

Splice junctions are drawn as arcs over the coverage of RNA alignments. Pick a locus in the landscape and the reads follow; the browser zooms with the other genome tiles.

```
# on the jbrowse component
show_junctions: true
color_by: sample
ucsc_tracks: [mane]
follow_window: true
```

Used in the [nf-core/rnafusion dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/rnafusion/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
