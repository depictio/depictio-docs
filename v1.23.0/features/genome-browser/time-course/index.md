# Time course

[![](../../../images/guides/genome-browser/genomespy_jbrowse.webp)](../../../images/guides/genome-browser/genomespy_jbrowse.mp4)

The tracks and the navigator lanes share one sequential ramp, so a time course reads down the browser, each library on its own scale. Zoomed out, a track shows the mean of each window.

```
# on the jbrowse component
color_scale:
  column: time_point               # a manifest column
  order_by: time_order
  scheme: viridis
display:
  autoscale: localsd
  summary: avg
```

Used in the nf-core/nascent dashboard template.

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
