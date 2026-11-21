---
title: "1. Read a shared dashboard"
description: "Read a shared nf-core/ampliseq dashboard: check the run in MultiQC, pick samples from a filter, a table, a figure or a map, then save groups, compare them and comment."
glightbox: true
---

# 1. Read a shared dashboard

<div class="ws-strip" markdown>
[**0** Setup](get-started.md){ .ws-ep0 } [**1** Read](view.md){ .ws-ep1 .ws-here } [**2** Edit](edit-your-copy.md){ .ws-ep2 } [**3** From files](from-a-file.md){ .ws-ep3 } [**4** From a run](from-nf-core-run.md){ .ws-ep4 } [**5** New run](new-run-and-versions.md){ .ws-ep5 }
</div>

<div class="ws-meta ws-ep1" markdown>
<span class="ws-chip" markdown="span">:material-account-eye-outline: **Reader**</span> <span class="ws-chip" markdown="span">:material-database-outline: **nf-core/ampliseq**</span> <span class="ws-chip" markdown="span">:material-flag-outline: **After episode 0**</span>
</div>

!!! overview "Overview"
    **Questions**

    - Why Depictio after a pipeline, rather than a static report or an app coded from scratch?
    - How do I check the quality of the run before reading its results?
    - How do I narrow a dashboard to the samples I care about?
    - How do I compare two groups of samples?
    - What do others see of what I do?

    **Objectives**

    - Find a MultiQC value with the dashboard search.
    - Filter a dashboard, MultiQC included, and share the filtered view.
    - Pick samples from a table, a map and a figure, and see the other data collections follow.
    - Save two groups and compare them in the cards.
    - Leave a comment on a figure.

Someone shared a finished dashboard with you: you are a **reader**. You cannot change the dashboard or its data. You can filter it, select samples and compare groups: that changes only your own view. Your filters and selections are kept for your account, in any browser you sign in on; your groups stay in this browser. Others see your view only if you send them its link.

![As a reader, the dashboard and its data are read only. Your view is yours: filters and selections kept for your account, groups kept in this browser, shown to others only by a view link](../../images/tutorials/workshop/diagrams/yours-and-shared_light.png#only-light){ .ws-diagram }
![As a reader, the dashboard and its data are read only. Your view is yours: filters and selections kept for your account, groups kept in this browser, shown to others only by a view link](../../images/tutorials/workshop/diagrams/yours-and-shared_dark.png#only-dark){ .ws-diagram }

<figure markdown="span" class="ws-media"><video autoplay controls muted loop playsinline poster="../../../images/tutorials/workshop/filter.webp" src="../../../images/tutorials/workshop/filter.mp4"></video></figure>

Open **nf-core/ampliseq** from **Dashboards**.

## :material-transit-connection-variant: Why Depictio: the step after the pipeline { #why }

A pipeline usually stops at its outputs: files opened one by one, a static HTML report, or an app coded from scratch for one dataset. Depictio is the step after: **one platform, reused and standardised across pipelines**, with the same tools while you build the dashboard and after you share it: with collaborators, with everyone, or as one HTML file that opens without a server, as a MultiQC report does.

![Usually, one pipeline's results end as output files, and/or a static HTML report (MultiQC, Quarto, Jupyter), or an app coded from scratch (Shiny, Streamlit, Plotly Dash). With Depictio, the results of any pipeline go through one platform (a template per pipeline version, components from the Tools catalog, editing in the interface, in code or YAML, every save a version) to a dashboard shared with collaborators or with everyone](../../images/tutorials/workshop/diagrams/why-depictio_light.png#only-light){ .ws-diagram }
![Usually, one pipeline's results end as output files, and/or a static HTML report (MultiQC, Quarto, Jupyter), or an app coded from scratch (Shiny, Streamlit, Plotly Dash). With Depictio, the results of any pipeline go through one platform (a template per pipeline version, components from the Tools catalog, editing in the interface, in code or YAML, every save a version) to a dashboard shared with collaborators or with everyone](../../images/tutorials/workshop/diagrams/why-depictio_dark.png#only-dark){ .ws-diagram }

You see each of them today: editing and versions in [episode 2](edit-your-copy.md), sharing in [episode 3](from-a-file.md#share-it-your-group-then-everyone), templates in [episode 4](from-nf-core-run.md). 42 nf-core pipelines have a template; the Tools catalog maps 471 outputs of 136 tools to components.

<p class="ws-src">Templates: Depictio documentation; tools and outputs: Depictio code; both November 2026.</p>

??? info "Compared, as a reader: a static report, a spreadsheet, your own code"

    <div class="ws-compare" markdown>

    | As a reader, you can… | :material-file-document-outline:<br>Static HTML report | :material-table-large:<br>Spreadsheet | :material-code-braces:<br>Your code, an app | ![Depictio](../../images/logo/favicon_lite.png){ .ws-logo .off-glb }<br>Depictio | Try it |
    |---|:-:|:-:|:-:|:-:|---|
    | Filter every view at once: MultiQC, tables, figures | <span class="ws-part">Within some reports</span> | :material-close-thick:{ .ws-no } | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | [Filter](#filter) |
    | Pick samples on a table, a figure or a map | :material-close-thick:{ .ws-no } | <span class="ws-part">Rows only</span> | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | [Four ways](#four-ways) |
    | Send the filtered view as a link | :material-close-thick:{ .ws-no } | :material-close-thick:{ .ws-no } | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | [Challenge 1.3](#filter) |
    | Define your own groups and compare them | :material-close-thick:{ .ws-no } | <span class="ws-part">By hand</span> | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | [Analysis mode](#groups) |
    | Comment on a figure | :material-close-thick:{ .ws-no } | <span class="ws-part">On cells</span> | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | [Challenge 1.7](#groups) |
    | Open it as one file, without a server | :material-check-bold:{ .ws-yes } | :material-check-bold:{ .ws-yes } | <span class="ws-part">If you code it</span> | :material-check-bold:{ .ws-yes } | |

    </div>

## :material-magnify: First, the quality of the run { #multiqc }

Before reading the results, check the run. The ![MultiQC](../../images/tutorials/workshop/multiqc-icon.svg){ .ws-logo .ws-logo-mono .off-glb } MultiQC report of the pipeline is on the dashboard. To find a plot, click **Search this dashboard**, the magnifier :material-magnify: in the bottom toolbar (**Ctrl+K**, or **⌘K** on a Mac). The search covers every tile of every tab and opens the tab that holds what you pick.

!!! challenge "Challenge 1.1: the most trimmed sample"
    Search for *General Stats* and open it. In the column **Trimmed bases** (cutadapt, % of base pairs trimmed), which sample lost the most?

    ??? solution "Solution"
        SRR10070132: 13.9 % of its bases trimmed, against 9.3 to 11.8 % for the other samples. It is a groundwater sample.

## :material-filter-outline: Pick samples: four ways in { #four-ways }

On this dashboard you pick samples in four ways: the **Filters** panel, rows of a table, points of a figure, markers of a map. The four used here read the sample metadata; the links carry the samples you picked to the other data collections, so every component that reads them follows.

![Four ways to pick samples: the Filters panel, rows of Sample sheet, points of a scatter plot, markers of Sampling sites, all on the metadata; the links carry the 3 picked samples to the other data collections. A pinned filter reaches every tab, a selection its own tab](../../images/tutorials/workshop/diagrams/filter-flow_light.png#only-light){ .ws-diagram }
![Four ways to pick samples: the Filters panel, rows of Sample sheet, points of a scatter plot, markers of Sampling sites, all on the metadata; the links carry the 3 picked samples to the other data collections. A pinned filter reaches every tab, a selection its own tab](../../images/tutorials/workshop/diagrams/filter-flow_dark.png#only-dark){ .ws-diagram }

How links carry a filter: [Cross-DC filtering](../../features/cross-dc-filtering.md).

### :material-filter-variant: From the Filters panel { #filter }

1. Open the **Community & Diversity** tab.
2. The **Filters** panel is open on the left; if it is not, click **Filters**, near the bottom of the left sidebar. Under **Sample filters**, set **Habitat** to *Soil*.
3. Open another tab: the filter is still set. **Sample filters** carries a pin :material-pin:: it is a pinned section, drawn on every tab, so its filters reach every tab. A section without a pin, such as **Community filters** on this tab, belongs to its tab.

!!! challenge "Challenge 1.2: what does the filter change?"
    With Habitat set to *Soil*, how many phyla does the **Phyla** card show? How many without the filter?

    ??? solution "Solution"
        26 with *Soil*, 57 without. The card reads the taxonomy, another data collection than the metadata: the link carries the three soil samples to it.

To share this view, copy its link: the link icon next to *1 filter active* in the Filters panel, or the gear icon in the header, then **Filters → Share this view**.

!!! challenge "Challenge 1.3: what does the link carry?"
    Copy the link of your filtered view. Clear the filter with the red eraser icon at the top of the Filters panel, then paste the link in a new browser tab. What is filtered?

    ??? solution "Solution"
        *Habitat: Soil* is back, and the Phyla card shows 26 again. The link carries the filters: whoever opens it sees this view, and what they change afterwards does not change yours.

The MultiQC report follows the same filters: a link matches its sample names to the metadata.

1. In **Habitat**, remove *Soil*, then pick *Groundwater*. Habitat takes several values: with *Soil* still in, you get six samples, not three.
2. Open **General Stats** again, with the search. Three samples are left: SRR10070132, the most trimmed sample, beside SRR10070133 and SRR10070141.

### :material-table: From a table { #select-table }

1. Clear the filter. Open **Overview**, the first tab.
2. At the bottom of Overview, expand the collapsed **Sample sheet** section. Click a row, then hold **Ctrl** (**⌘** on a Mac) and click more rows. The cards at the top follow: **Samples**, **Phyla**, **Shannon diversity**, **Reads kept (%)**. Each reads a different data collection.
3. **Clear selection**, in the table's action row, drops the selection.

!!! challenge "Challenge 1.4: the least diverse habitat"
    Select the three *Groundwater* rows of **Sample sheet**. What does the **Shannon diversity** card show, before and after?

    ??? solution "Solution"
        About 7.7 for all twelve samples (the card shows the median), about 5.4 for SRR10070132, SRR10070133 and SRR10070141: groundwater is the least diverse habitat of the run.

### :material-map-marker-multiple: From a map { #select-map }

!!! note "Only if your instructor's dashboard has the Sampling sites map"
    The dashboard built from the nf-core/ampliseq template has seven tabs: Overview, MultiQC, Alpha Diversity, Ordination & Clustering, Community & Diversity, Differential Abundance, Phylogeny. The **Sampling sites** map is only on an extended version of it. Without the map, skip to the next section, [From a figure](#select).

    1. Clear the table's selection. On **Overview**, hover the **Sampling sites** map: its toolbar appears at the top right.
    2. Pick **Lasso Select** and draw around the markers of one site. The cards and **Sample sheet** follow.

    !!! challenge "Challenge 1.5: one site, two habitats"
        Lasso the southernmost site, Pfäffingen. How many samples does the **Samples** card count, and from which habitats?

        ??? solution "Solution"
            4: two *Riverwater* (SRR10070130, SRR10070131) and two *Sediment* (SRR10070149, SRR10070150). The river water and its sediment were sampled at the same place, so their markers sit on top of each other: hovering shows only one.

### :material-chart-box-outline: From a figure { #select }

!!! note "Only if your instructor's dashboard has the Environment (CTD) tab"
    The **Environment (CTD)** tab is only on the extended version of the dashboard, like the map. Without it, you select points on a figure in the [Analysis mode](#groups) section below, on the PCoA.

    1. Clear any selection. Open **Environment (CTD)**.
    2. On **Temperature × conductivity**, hover the plot, pick **Box Select** in its toolbar and draw a box around a few points. The cards and the **Shannon diversity** figure of the tab follow.

    !!! challenge "Challenge 1.6: the coldest samples"
        Box the three coldest points, near 3 °C. Which habitat are they from, and how diverse?

        ??? solution "Solution"
            *Soil*: SRR10102392, SRR10102393 and SRR10102394, between 3.1 and 3.7 °C. Their Shannon diversity, 8.6 to 8.7, sits between groundwater (about 5.4) and sediment (about 9.4).

!!! callout "Links go one way"
    A link goes from the metadata to the other data collections. A selection on a figure that reads another collection, such as the PCoA on **Ordination & Clustering**, narrows only the components that read that same collection.

!!! callout "How to read a tile"
    The **(i)** next to a tile's title says how to read it and where its data comes from.

![The Community & Diversity tab of the nf-core/ampliseq dashboard](../../images/tutorials/workshop/app_community.webp){ .ws-shot }

## :material-chart-scatter-plot: Analysis mode { #groups .ws-analysis }

**Analysis**, in the bottom toolbar, keeps selections as named groups and compares them. Groups are kept in your browser: nobody else sees them. Unlike a selection, a group reaches every data collection, even from the PCoA: groups also follow the links backwards.

<figure markdown="span" class="ws-media"><video autoplay controls muted loop playsinline poster="../../../images/tutorials/workshop/groups.webp" src="../../../images/tutorials/workshop/groups.mp4"></video></figure>

1. Open **Ordination & Clustering**, then click **Analysis** in the bottom toolbar.
2. On the PCoA, pick **Box select** in the figure's toolbar and box the water samples: the six points on the left (hover a point to read its sample ID). Scroll down the **Analysis** panel to type the group's name, then click **Save group**.
3. Box-select the soil and sediment samples together, and save them as a second group.
4. Turn on **Compare groups in cards**, then open **Alpha Diversity**. Each card now shows one value per group, beside **All**.

!!! challenge "Challenge 1.7: compare and comment"
    Do your two groups differ in diversity? Click the comment icon in the corner of a figure and write your answer. Readers can comment only where the server allows it; this workshop's server does.

    ??? solution "Solution"
        The answer depends on your groups. The comment keeps the filters and the selection it was written with: whoever opens it sees what you saw.

![Two saved groups compared on the Alpha Diversity tab](../../images/tutorials/workshop/hands_groups.webp){ .ws-shot }

!!! further "Going further"
    In the **Analysis** panel, **Color figures by → A column → habitat** colours every figure by a column of the sample metadata.

!!! keypoints "Key points"
    - Depictio is the step after the pipeline: one platform for every pipeline, with the same tools while you build and after you share.
    - Check the run first: the dashboard search finds a MultiQC plot on any tab.
    - The Filters panel, a table, a figure or a map can pick samples. From the metadata, the links carry them to every data collection, MultiQC included.
    - A filter of a pinned section reaches every tab; a selection acts on its own tab. A view link carries the filters, so it shares a view.
    - As a reader, the dashboard and its data are read only. Filters and selections are kept for your account, groups in this browser; others see them only through a view link.

<div class="ws-next" markdown>
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md#episode-1){ .ws-help }
[<span class="ws-k">Next episode</span><span class="ws-t">2. Make your own copy and edit it</span>](edit-your-copy.md){ .ws-go .ws-ep2 }
</div>
