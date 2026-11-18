# UCSC tracks

[![](../../../images/guides/genome-browser/ucsc_and_tracks.webp)](../../../images/guides/genome-browser/ucsc_and_tracks.mp4)

Any bigWig, bigBed or VCF track of the UCSC Genome Browser catalogue for the assembly opens next to the collection's tracks. The builder searches the catalogue by name; each track keeps its own menu, and force load lifts the download limit.

```
# on the jbrowse component
ucsc_tracks: [clinvarMain, dbSnp155Common]
fetch_size_limit_mb: 5
```

[![](../../../images/guides/genome-browser/ucsc_builder.webp)](../../../images/guides/genome-browser/ucsc_builder.mp4)

Used in the [nf-core/viralrecon dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/viralrecon/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
