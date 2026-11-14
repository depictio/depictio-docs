---
title: "Genome browser: Variant colours"
icon: material/palette
description: Variants coloured by a category of the dashboard.
glightbox: true
---

# Variant colours

Variant features take the dashboard's category colours, read from a VCF INFO field (an effect, an impact, a caller), so the browser and the other tiles agree. `variant_label_by` names them by part of an INFO field instead of the VCF ID.

```yaml
# on the jbrowse component
variant_color_by:
  column: coding_effect            # colours from the dashboard's category_colors
  info_field: IMPACT               # the VCF INFO field holding the category
```

Used in the [nf-core/oncoanalyser dashboard template](../../pipeline-templates/nf-core/oncoanalyser.md).

[:material-arrow-left: All examples](index.md#examples)
