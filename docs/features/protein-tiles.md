---
title: Protein tiles
description: The protein tiles are on the Proteins page and on the advanced visualizations page.
hide:
  - navigation
  - toc
search:
  exclude: true
---

# Protein tiles

This page moved to [Proteins](proteins.md). The settings of each tile are on the
[advanced visualizations](advanced-visualizations.md#proteins) page.

<script>
  // Keep the anchor of an old link: the shared sections moved to proteins/, the tiles to advanced-visualizations/.
  var shared = ["the-data", "residue-selection", "structure-resolver", "numbering-mismatch"];
  var hash = location.hash.replace("#", "");
  location.replace(!hash || shared.indexOf(hash) >= 0 ? "../proteins/" + location.hash : "../advanced-visualizations/#" + hash);
</script>
