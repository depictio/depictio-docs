# Browser to dashboard

[![](../../../images/guides/genome-browser/browser_to_dashboard.webp)](../../../images/guides/genome-browser/browser_to_dashboard.mp4)

Click a feature in the browser: the dashboard filters on the sample of its track, and the navigator above keeps that sample's calls. With `selection_mode: visible_tracks`, the set of open tracks is the selection instead.

```
# on the jbrowse component
selection_enabled: true
selection_column: sample           # default: the collection's sample_column
```

Used in the [nf-core/viralrecon dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/viralrecon/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
