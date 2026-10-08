---
title: "Spotlight search"
description: "Search every component of every tab of a dashboard from the keyboard, and land on the one you pick."
---

# :material-magnify: Spotlight search <small>(v1.14.0+)</small>

A dashboard with a dozen tabs of thirty components each used to mean opening tabs until
the right plot showed up. **⌘K** on a Mac, **Ctrl+K** elsewhere, or the magnifier in the
header, opens a search across every component of every tab of the dashboard. Picking a
result takes you to that component.

[![Searching "phylum": results on this tab first, then on Community & Diversity](../../images/guides/spotlight/spotlight-phylum.webp)](../../images/guides/spotlight/spotlight-phylum.webp){target=_blank}

---

## What it searches

The search reads what the dashboard already says about itself:

- tab names and descriptions;
- component titles, subtitles and descriptions;
- type and chart-kind labels (*filter*, *card*, *phylogenetic*, *sankey*);
- the columns a component binds;
- the prose of text tiles, without its markdown;
- section names.

A word is found where a field starts with it, then where one of its words does, then
anywhere inside it. A hit in a title ranks above the same hit in a text body. There is no
typo tolerance: a misspelt word finds nothing rather than a list of near misses.

---

## Results

Results are grouped by tab, the tab you are on first. Each row shows the component's
type, its title with the match highlighted, and a dimmed *tab · section · snippet* line.
**↑** and **↓** move, **Enter** opens, **Esc** closes. A tab with many matches shows the
first few and says how many more there are.

[![Searching "fastqc": the MultiQC panels of the Sequencing QC tab](../../images/guides/spotlight/spotlight-fastqc.webp)](../../images/guides/spotlight/spotlight-fastqc.webp){target=_blank}

---

## Where it lands

1. Whatever hides the component opens first: a folded section, a filter group, the
   collapsed filter panel, a [section shown on every tab](../../features/dashboards.md#persistent-sections),
   or the filter drawer on a phone.
2. The page scrolls to the component and rings it for a moment.

A result on another tab opens that tab with `?component=` in the address, which the tab
acts on and then removes. In the editor, pending changes are saved before leaving the
tab; if the save fails, you stay on the tab and a notification says so.

Search works in view mode, in edit mode and on public dashboards. The shortcut is
ignored while you type in a field or in the code editor.

!!! note "Known limits"
    - A filter folded under a filter bar's **More filters**, or a map floating above the
      canvas, is not uncovered. You get a *That component is not on screen* notice
      instead.
    - A tile that grows once its data has loaded is scrolled to a second time, to
      correct the landing.
