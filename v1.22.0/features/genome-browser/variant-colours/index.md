# Variant colours

Variant features take the dashboard's category colours, read from a VCF INFO field (an effect, an impact, a caller), so the browser and the other tiles agree. `variant_label_by` names them by part of an INFO field instead of the VCF ID.

```
# on the jbrowse component
variant_color_by:
  column: coding_effect            # colours from the dashboard's category_colors
  info_field: IMPACT               # the VCF INFO field holding the category
```

Used in the [nf-core/oncoanalyser dashboard template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/oncoanalyser/index.md).

[All examples](https://depictio.github.io/depictio-docs/latest/features/genome-browser/#examples)
