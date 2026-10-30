---
title: Advanced visualizations
icon: material/chart-box-multiple-outline
description: Domain charts that know their column roles, from volcano plots and genome tracks to linked protein structures, with the data each one reads, its controls and a YAML example.
glightbox: true
---

# :material-chart-multiline: Advanced visualizations

An advanced visualization is a domain chart that knows what its columns mean. A volcano
knows it needs a feature, an effect size and a significance; a genome view knows chromosome
and position. You bind your columns to those roles once, and the tile brings the domain logic:
thresholds, tiers, genomic axes, linked selections.

Pick one over a generic [Figure](components.md#figure-components) when your table matches a
known shape (the output of DESeq2, mosdepth, QIIME2, AlphaFold...). Pick a Figure for a plain
plot of any columns.

**How to use one**

1. In the dashboard editor, add a component, pick a data collection, then the **Advanced viz** type.
2. Pick a kind. The builder ranks the kinds by how well they fit the collection (see [the kind picker](#kind-picker)).
3. Bind each role to a column under **Column bindings**. Required roles must be bound; the builder checks the column types.
4. Optionally choose where the controls go under **Viz controls**, then add the tile.

In a [dashboard YAML file](yaml-sync.md), the same tile is a `component_type: advanced_viz`
entry. A role `x` binds through the `config` key `x_col`:

```yaml
- tag: viz-de
  component_type: advanced_viz
  workflow_tag: my_workflow
  data_collection_tag: de_results
  viz_kind: volcano
  config:
    viz_kind: volcano
    feature_id_col: gene_id
    effect_size_col: log2FoldChange
    significance_col: padj
```

Every entry below follows the same layout: a version badge (<span class="ver-badge">v1.19.0+</span>
means available since that release), a screenshot, a few rows of the input table it expects
(column names as in its YAML example, <small>optional</small> marks a column it can do
without), the tools whose output fits, its controls and a YAML example.

## :material-view-grid-outline: Catalog { #catalog }

Click a thumbnail to enlarge it, or its name to jump to the entry.

<p class="viz-grid__family">Differential analysis</p>

<div class="viz-grid" markdown>

<div markdown>
![Volcano](../images/guides/advanced-visualizations/volcano_light.webp#only-light){ data-title="Volcano" loading=lazy }
![Volcano](../images/guides/advanced-visualizations/volcano_dark.webp#only-dark){ data-title="Volcano" loading=lazy }
[Volcano](#volcano){ .viz-grid__name }
</div>

<div markdown>
![DA barplot](../images/guides/advanced-visualizations/da_barplot_light.webp#only-light){ data-title="DA barplot" loading=lazy }
![DA barplot](../images/guides/advanced-visualizations/da_barplot_dark.webp#only-dark){ data-title="DA barplot" loading=lazy }
[DA barplot](#da-barplot){ .viz-grid__name }
</div>

<div markdown>
![GSEA running score](../images/guides/advanced-visualizations/gsea_running_score_light.webp#only-light){ data-title="GSEA running score" loading=lazy }
![GSEA running score](../images/guides/advanced-visualizations/gsea_running_score_dark.webp#only-dark){ data-title="GSEA running score" loading=lazy }
[GSEA running score](#gsea-running-score){ .viz-grid__name }
</div>

<div markdown>
![Group compare](../images/guides/advanced-visualizations/group_compare_light.webp#only-light){ data-title="Group compare" loading=lazy }
![Group compare](../images/guides/advanced-visualizations/group_compare_dark.webp#only-dark){ data-title="Group compare" loading=lazy }
[Group compare](#group-compare){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Single cell & embeddings</p>

<div class="viz-grid" markdown>

<div markdown>
![Embedding](../images/guides/advanced-visualizations/embedding_light.webp#only-light){ data-title="Embedding" loading=lazy }
![Embedding](../images/guides/advanced-visualizations/embedding_dark.webp#only-dark){ data-title="Embedding" loading=lazy }
[Embedding](#embedding){ .viz-grid__name }
</div>

<div markdown>
![Dot plot](../images/guides/advanced-visualizations/dot_plot_light.webp#only-light){ data-title="Dot plot" loading=lazy }
![Dot plot](../images/guides/advanced-visualizations/dot_plot_dark.webp#only-dark){ data-title="Dot plot" loading=lazy }
[Dot plot](#dot-plot){ .viz-grid__name }
</div>

<div markdown>
![Knee plot](../images/guides/advanced-visualizations/knee_plot_light.webp#only-light){ data-title="Knee plot" loading=lazy }
![Knee plot](../images/guides/advanced-visualizations/knee_plot_dark.webp#only-dark){ data-title="Knee plot" loading=lazy }
[Knee plot](#knee-plot){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Genome tracks</p>

<div class="viz-grid" markdown>

<div markdown>
![Coverage track](../images/guides/advanced-visualizations/coverage_track_light.webp#only-light){ data-title="Coverage track" loading=lazy }
![Coverage track](../images/guides/advanced-visualizations/coverage_track_dark.webp#only-dark){ data-title="Coverage track" loading=lazy }
[Coverage track](#coverage-track){ .viz-grid__name }
</div>

<div markdown>
![Genome view](../images/guides/advanced-visualizations/genome_view_light.webp#only-light){ data-title="Genome view" loading=lazy }
![Genome view](../images/guides/advanced-visualizations/genome_view_dark.webp#only-dark){ data-title="Genome view" loading=lazy }
[Genome view](#genome-view){ .viz-grid__name }
</div>

<div markdown>
![Copy-number profile](../images/guides/advanced-visualizations/cnv_profile_light.webp#only-light){ data-title="Copy-number profile" loading=lazy }
![Copy-number profile](../images/guides/advanced-visualizations/cnv_profile_dark.webp#only-dark){ data-title="Copy-number profile" loading=lazy }
[Copy-number profile](#cnv-profile){ .viz-grid__name }
</div>

<div markdown>
![Contact map](../images/guides/advanced-visualizations/contact_map_light.webp#only-light){ data-title="Contact map" loading=lazy }
![Contact map](../images/guides/advanced-visualizations/contact_map_dark.webp#only-dark){ data-title="Contact map" loading=lazy }
[Contact map](#contact-map){ .viz-grid__name }
</div>

<div markdown>
![Transcript structure](../images/guides/advanced-visualizations/transcript_structure_light.webp#only-light){ data-title="Transcript structure" loading=lazy }
![Transcript structure](../images/guides/advanced-visualizations/transcript_structure_dark.webp#only-dark){ data-title="Transcript structure" loading=lazy }
[Transcript structure](#transcript-structure){ .viz-grid__name }
</div>

<div markdown>
![Sashimi](../images/guides/advanced-visualizations/sashimi_light.webp#only-light){ data-title="Sashimi" loading=lazy }
![Sashimi](../images/guides/advanced-visualizations/sashimi_dark.webp#only-dark){ data-title="Sashimi" loading=lazy }
[Sashimi](#sashimi){ .viz-grid__name }
</div>

<div markdown>
![Gene arrow track](../images/guides/advanced-visualizations/gene_arrow_track_light.webp#only-light){ data-title="Gene arrow track" loading=lazy }
![Gene arrow track](../images/guides/advanced-visualizations/gene_arrow_track_dark.webp#only-dark){ data-title="Gene arrow track" loading=lazy }
[Gene arrow track](#gene-arrow-track){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Variants & rearrangements</p>

<div class="viz-grid" markdown>

<div markdown>
![Manhattan](../images/guides/advanced-visualizations/manhattan_light.webp#only-light){ data-title="Manhattan" loading=lazy }
![Manhattan](../images/guides/advanced-visualizations/manhattan_dark.webp#only-dark){ data-title="Manhattan" loading=lazy }
[Manhattan](#manhattan){ .viz-grid__name }
</div>

<div markdown>
![Lollipop](../images/guides/advanced-visualizations/lollipop_light.webp#only-light){ data-title="Lollipop" loading=lazy }
![Lollipop](../images/guides/advanced-visualizations/lollipop_dark.webp#only-dark){ data-title="Lollipop" loading=lazy }
[Lollipop](#lollipop){ .viz-grid__name }
</div>

<div markdown>
![Oncoplot](../images/guides/advanced-visualizations/oncoplot_light.webp#only-light){ data-title="Oncoplot" loading=lazy }
![Oncoplot](../images/guides/advanced-visualizations/oncoplot_dark.webp#only-dark){ data-title="Oncoplot" loading=lazy }
[Oncoplot](#oncoplot){ .viz-grid__name }
</div>

<div markdown>
![Genome chord](../images/guides/advanced-visualizations/genome_chord_light.webp#only-light){ data-title="Genome chord" loading=lazy }
![Genome chord](../images/guides/advanced-visualizations/genome_chord_dark.webp#only-dark){ data-title="Genome chord" loading=lazy }
[Genome chord](#genome-chord){ .viz-grid__name }
</div>

<div markdown>
![Fusion structure](../images/guides/advanced-visualizations/fusion_structure_light.webp#only-light){ data-title="Fusion structure" loading=lazy }
![Fusion structure](../images/guides/advanced-visualizations/fusion_structure_dark.webp#only-dark){ data-title="Fusion structure" loading=lazy }
[Fusion structure](#fusion-structure){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Signal & read profiles</p>

<div class="viz-grid" markdown>

<div markdown>
![Profile](../images/guides/advanced-visualizations/profile_light.webp#only-light){ data-title="Profile" loading=lazy }
![Profile](../images/guides/advanced-visualizations/profile_dark.webp#only-dark){ data-title="Profile" loading=lazy }
[Profile](#profile){ .viz-grid__name }
</div>

<div markdown>
![Signal matrix](../images/guides/advanced-visualizations/signal_matrix_light.webp#only-light){ data-title="Signal matrix" loading=lazy }
![Signal matrix](../images/guides/advanced-visualizations/signal_matrix_dark.webp#only-dark){ data-title="Signal matrix" loading=lazy }
[Signal matrix](#signal-matrix){ .viz-grid__name }
</div>

<div markdown>
![Damage profile](../images/guides/advanced-visualizations/damage_profile_light.webp#only-light){ data-title="Damage profile" loading=lazy }
![Damage profile](../images/guides/advanced-visualizations/damage_profile_dark.webp#only-dark){ data-title="Damage profile" loading=lazy }
[Damage profile](#damage-profile){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Microbiome & ecology</p>

<div class="viz-grid" markdown>

<div markdown>
![Stacked taxonomy](../images/guides/advanced-visualizations/stacked_taxonomy_light.webp#only-light){ data-title="Stacked taxonomy" loading=lazy }
![Stacked taxonomy](../images/guides/advanced-visualizations/stacked_taxonomy_dark.webp#only-dark){ data-title="Stacked taxonomy" loading=lazy }
[Stacked taxonomy](#stacked-taxonomy){ .viz-grid__name }
</div>

<div markdown>
![Sunburst](../images/guides/advanced-visualizations/sunburst_light.webp#only-light){ data-title="Sunburst" loading=lazy }
![Sunburst](../images/guides/advanced-visualizations/sunburst_dark.webp#only-dark){ data-title="Sunburst" loading=lazy }
[Sunburst](#sunburst){ .viz-grid__name }
</div>

<div markdown>
![Rarefaction](../images/guides/advanced-visualizations/rarefaction_light.webp#only-light){ data-title="Rarefaction" loading=lazy }
![Rarefaction](../images/guides/advanced-visualizations/rarefaction_dark.webp#only-dark){ data-title="Rarefaction" loading=lazy }
[Rarefaction](#rarefaction){ .viz-grid__name }
</div>

<div markdown>
![Phylogenetic tree](../images/guides/advanced-visualizations/phylogenetic_light.webp#only-light){ data-title="Phylogenetic tree" loading=lazy }
![Phylogenetic tree](../images/guides/advanced-visualizations/phylogenetic_dark.webp#only-dark){ data-title="Phylogenetic tree" loading=lazy }
[Phylogenetic tree](#phylogenetic){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">General purpose</p>

<div class="viz-grid" markdown>

<div markdown>
![Scatter (X/Y)](../images/guides/advanced-visualizations/scatter_xy_light.webp#only-light){ data-title="Scatter (X/Y)" loading=lazy }
![Scatter (X/Y)](../images/guides/advanced-visualizations/scatter_xy_dark.webp#only-dark){ data-title="Scatter (X/Y)" loading=lazy }
[Scatter (X/Y)](#scatter-xy){ .viz-grid__name }
</div>

<div markdown>
![Hierarchical heatmap](../images/guides/advanced-visualizations/complex_heatmap_light.webp#only-light){ data-title="Hierarchical heatmap" loading=lazy }
![Hierarchical heatmap](../images/guides/advanced-visualizations/complex_heatmap_dark.webp#only-dark){ data-title="Hierarchical heatmap" loading=lazy }
[Hierarchical heatmap](#hierarchical-heatmap){ .viz-grid__name }
</div>

<div markdown>
![UpSet](../images/guides/advanced-visualizations/upset_plot_light.webp#only-light){ data-title="UpSet" loading=lazy }
![UpSet](../images/guides/advanced-visualizations/upset_plot_dark.webp#only-dark){ data-title="UpSet" loading=lazy }
[UpSet](#upset){ .viz-grid__name }
</div>

<div markdown>
![Sankey](../images/guides/advanced-visualizations/sankey_light.webp#only-light){ data-title="Sankey" loading=lazy }
![Sankey](../images/guides/advanced-visualizations/sankey_dark.webp#only-dark){ data-title="Sankey" loading=lazy }
[Sankey](#sankey){ .viz-grid__name }
</div>

<div markdown>
![Parallel coordinates](../images/guides/advanced-visualizations/parallel_coordinates_light.webp#only-light){ data-title="Parallel coordinates" loading=lazy }
![Parallel coordinates](../images/guides/advanced-visualizations/parallel_coordinates_dark.webp#only-dark){ data-title="Parallel coordinates" loading=lazy }
[Parallel coordinates](#parallel-coordinates){ .viz-grid__name }
</div>

<div markdown>
![Record card](../images/guides/advanced-visualizations/record_card_light.webp#only-light){ data-title="Record card" loading=lazy }
![Record card](../images/guides/advanced-visualizations/record_card_dark.webp#only-dark){ data-title="Record card" loading=lazy }
[Record card](#record-card){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Benchmarking</p>

<div class="viz-grid" markdown>

<div markdown>
![PR benchmark](../images/guides/advanced-visualizations/pr_benchmark_light.webp#only-light){ data-title="PR benchmark" loading=lazy }
![PR benchmark](../images/guides/advanced-visualizations/pr_benchmark_dark.webp#only-dark){ data-title="PR benchmark" loading=lazy }
[PR benchmark](#pr-benchmark){ .viz-grid__name }
</div>

<div markdown>
![Confusion matrix](../images/guides/advanced-visualizations/confusion_matrix_light.webp#only-light){ data-title="Confusion matrix" loading=lazy }
![Confusion matrix](../images/guides/advanced-visualizations/confusion_matrix_dark.webp#only-dark){ data-title="Confusion matrix" loading=lazy }
[Confusion matrix](#confusion-matrix){ .viz-grid__name }
</div>

<div markdown>
![Metric with CI](../images/guides/advanced-visualizations/metric_ci_bars_light.webp#only-light){ data-title="Metric with CI" loading=lazy }
![Metric with CI](../images/guides/advanced-visualizations/metric_ci_bars_dark.webp#only-dark){ data-title="Metric with CI" loading=lazy }
[Metric with CI](#metric-ci-bars){ .viz-grid__name }
</div>

</div>

<p class="viz-grid__family">Proteins</p>

<div class="viz-grid" markdown>

<div markdown>
![3D structure](../images/guides/advanced-visualizations/molecule_3d_light.webp#only-light){ data-title="3D structure" loading=lazy }
![3D structure](../images/guides/advanced-visualizations/molecule_3d_dark.webp#only-dark){ data-title="3D structure" loading=lazy }
[3D structure](#molecule-3d){ .viz-grid__name }
</div>

<div markdown>
![Alignment](../images/guides/advanced-visualizations/msa_light.webp#only-light){ data-title="Alignment" loading=lazy }
![Alignment](../images/guides/advanced-visualizations/msa_dark.webp#only-dark){ data-title="Alignment" loading=lazy }
[Alignment](#msa){ .viz-grid__name }
</div>

<div markdown>
![Sequence track](../images/guides/advanced-visualizations/sequence_track_light.webp#only-light){ data-title="Sequence track" loading=lazy }
![Sequence track](../images/guides/advanced-visualizations/sequence_track_dark.webp#only-dark){ data-title="Sequence track" loading=lazy }
[Sequence track](#sequence-track){ .viz-grid__name }
</div>

<div markdown>
![HMM logo](../images/guides/advanced-visualizations/hmm_logo_light.webp#only-light){ data-title="HMM logo" loading=lazy }
![HMM logo](../images/guides/advanced-visualizations/hmm_logo_dark.webp#only-dark){ data-title="HMM logo" loading=lazy }
[HMM logo](#hmm-logo){ .viz-grid__name }
</div>

<div markdown>
![Domain architecture](../images/guides/advanced-visualizations/domain_architecture_light.webp#only-light){ data-title="Domain architecture" loading=lazy }
![Domain architecture](../images/guides/advanced-visualizations/domain_architecture_dark.webp#only-dark){ data-title="Domain architecture" loading=lazy }
[Domain architecture](#domain-architecture){ .viz-grid__name }
</div>

<div markdown>
![Secondary structure](../images/guides/advanced-visualizations/secondary_structure_light.webp#only-light){ data-title="Secondary structure" loading=lazy }
![Secondary structure](../images/guides/advanced-visualizations/secondary_structure_dark.webp#only-dark){ data-title="Secondary structure" loading=lazy }
[Secondary structure](#secondary-structure){ .viz-grid__name }
</div>

<div markdown>
![Predicted aligned error](../images/guides/advanced-visualizations/pae_matrix_light.webp#only-light){ data-title="Predicted aligned error" loading=lazy }
![Predicted aligned error](../images/guides/advanced-visualizations/pae_matrix_dark.webp#only-dark){ data-title="Predicted aligned error" loading=lazy }
[Predicted aligned error](#pae-matrix){ .viz-grid__name }
</div>

<div markdown>
![Ramachandran](../images/guides/advanced-visualizations/ramachandran_light.webp#only-light){ data-title="Ramachandran" loading=lazy }
![Ramachandran](../images/guides/advanced-visualizations/ramachandran_dark.webp#only-dark){ data-title="Ramachandran" loading=lazy }
[Ramachandran](#ramachandran){ .viz-grid__name }
</div>

</div>

---

## :material-tune-variant: Shared settings { #shared-settings }

### Controls and where they go { #controls }

Each tile splits its controls in two tiers. **Primary** controls change what is shown: the
view switch, thresholds, colour by, a gene or sample picker. **Cosmetic** controls change how
it is drawn: marker sizes, palettes, labels, legend. The config key `controls_placement` sets
where they go <span class="ver-badge">v1.13.0+</span>:

| `controls_placement` | Where |
|----------------------|-------|
| `popover` (default) | Behind the settings icon, or docked beside or above the plot when the tile has room <span class="ver-badge">v1.14.0+</span> |
| `header` | Primary controls in a strip under the title, cosmetic ones in the popover |
| `rail` | All controls in a column right of the plot, no popover |

=== "popover"

    ![Volcano tile with its controls in the settings popover](../images/guides/advanced-visualizations/controls_popover_light.webp#only-light){ data-title="Volcano tile with its controls in the settings popover" .viz-shot loading=lazy }
    ![Volcano tile with its controls in the settings popover](../images/guides/advanced-visualizations/controls_popover_dark.webp#only-dark){ data-title="Volcano tile with its controls in the settings popover" .viz-shot loading=lazy }

=== "header"

    ![Volcano tile with its primary controls under the title](../images/guides/advanced-visualizations/controls_header_light.webp#only-light){ data-title="Volcano tile with its primary controls under the title" .viz-shot loading=lazy }
    ![Volcano tile with its primary controls under the title](../images/guides/advanced-visualizations/controls_header_dark.webp#only-dark){ data-title="Volcano tile with its primary controls under the title" .viz-shot loading=lazy }

=== "rail"

    ![Volcano tile with its controls in a rail beside the plot](../images/guides/advanced-visualizations/controls_rail_light.webp#only-light){ data-title="Volcano tile with its controls in a rail beside the plot" .viz-shot loading=lazy }
    ![Volcano tile with its controls in a rail beside the plot](../images/guides/advanced-visualizations/controls_rail_dark.webp#only-dark){ data-title="Volcano tile with its controls in a rail beside the plot" .viz-shot loading=lazy }

- A docked panel shows the first three controls and folds the rest under **More options**.
  The component-level `controls_placement` (`auto`, `right`, `top`, `popover`), the builder's
  **Viz controls** section, forces the dock side or keeps the icon.
- A reader can move the controls with the placement picker; the choice lasts the session.
- A dashboard sets a default for every tile with `advanced_viz_controls`. See
  [Tile height and control placement](yaml-sync.md#tile-height).
- Every tile also offers **Show underlying data**: the rows behind the plot.

### Switchable views { #views }

Some kinds draw the same rows several ways. `view` is the view the tile opens on, `views` the
views it offers. A view is only offered when its columns are bound.

| Kind | Views (default first) |
|------|-----------------------|
| [Volcano](#volcano) | `volcano`, `ma`, `qq` |
| [Dot plot](#dot-plot) | `dotplot`, `enrichment` |
| [PR benchmark](#pr-benchmark) | `pr`, `roc`, `both` |
| [Coverage track](#coverage-track) | `track`, `locus` |
| [Copy-number profile](#cnv-profile) | `plotly`, `locus` |
| [Sashimi](#sashimi) | `plotly`, `genomespy` |

!!! info "Retired kinds still load"
    `viz_kind: ma`, `qq`, `enrichment` and `roc_pr_curve` became views in v1.13.0. They still
    load and open on the matching view of `volcano`, `dot_plot` or `pr_benchmark`; the builder
    no longer offers them. `ancombc_differentials` loads as a [DA barplot](#da-barplot).

### The kind picker { #kind-picker }

The builder lists the tile's current kind first, then **Recommended** kinds, then the others,
folded. A badge says what a suggestion rests on:

| Badge | Meaning |
|-------|---------|
| **Named match** | Columns are named for the kind's roles (`log2FoldChange`, `padj`...) |
| **Shape match** | Columns have the right types and shape, without matching names |
| **Fits your selection** | Another tile on the tab emits a selection the kind can follow, as for a [Record card](#record-card) |
| **Weak** | Pickable, but a required role has no good column |

---

## Differential analysis { #differential-analysis }

### :material-chart-scatter-plot: Volcano { #volcano }

<span class="ver-badge">v0.13.0+</span> `viz_kind: volcano`

Effect size against significance for a differential test. The same table also reads as an MA plot and a QQ plot from the view switch.

![Volcano](../images/guides/advanced-visualizations/volcano_light.webp#only-light){ data-title="Volcano" .viz-shot loading=lazy }
![Volcano](../images/guides/advanced-visualizations/volcano_dark.webp#only-dark){ data-title="Volcano" .viz-shot loading=lazy }

**Input:** one row per gene.

| gene_id | log2FoldChange | padj | log2_baseMean <small>optional</small> | pvalue <small>optional</small> |
|---|---|---|---|---|
| ENSG00000141510 | -1.84 | 3.2e-08 | 11.2 | 1.1e-09 |
| ENSG00000146648 | 2.47 | 4.5e-12 | 9.8 | 8.0e-14 |
| ENSG00000136997 | 0.31 | 0.42 | 12.6 | 0.21 |

Also optional: `label_col`, `category_col`. `log2_baseMean` adds the MA view, `pvalue` the QQ view.

**Compatible inputs:** DESeq2, limma or edgeR results tables, as nf-core/differentialabundance publishes them.

**Controls**

- Primary: View (Volcano, MA, QQ), p / padj threshold, |effect| or |log2 FC| threshold, Top-N labels, Search
- Cosmetic: Show top-N labels; in the QQ view: identity line, 95% null band, point size

??? example "YAML"
    ```yaml
    - tag: viz-volcano
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: de_results
      viz_kind: volcano
      config:
        viz_kind: volcano
        feature_id_col: gene_id
        effect_size_col: log2FoldChange
        significance_col: padj
        avg_log_intensity_col: log2_baseMean
        p_value_col: pvalue
        views: [volcano, ma, qq]
    ```

### :material-view-grid-plus-outline: DA barplot { #da-barplot }

<span class="ver-badge">v0.13.0+</span> `viz_kind: da_barplot`

Ranked signed log fold changes per feature, one panel per contrast or one contrast at a time.

![DA barplot](../images/guides/advanced-visualizations/da_barplot_light.webp#only-light){ data-title="DA barplot" .viz-shot loading=lazy }
![DA barplot](../images/guides/advanced-visualizations/da_barplot_dark.webp#only-dark){ data-title="DA barplot" .viz-shot loading=lazy }

**Input:** one row per taxon and contrast (long format).

| taxon | contrast | lfc | q_val <small>optional</small> |
|---|---|---|---|
| Bacteroides | treatment_vs_control | 1.92 | 0.003 |
| Bacteroides | day14_vs_day0 | -0.41 | 0.38 |
| Faecalibacterium | treatment_vs_control | -2.35 | 0.0007 |

Also optional: `label_col`.

**Compatible inputs:** ANCOM-BC, ALDEx2 or MaAsLin2 differentials (nf-core/ampliseq).

**Controls**

- Primary: Contrast tabs (All or one contrast), Top-N per panel, Significance threshold
- Cosmetic: None

??? example "YAML"
    ```yaml
    - tag: viz-da-barplot
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: ancombc_results
      viz_kind: da_barplot
      config:
        viz_kind: da_barplot
        feature_id_col: taxon
        contrast_col: contrast
        lfc_col: lfc
        significance_col: q_val
        contrast_view: all
    ```

### :material-chart-bell-curve-cumulative: GSEA running score { #gsea-running-score }

<span class="ver-badge">v1.11.0+</span> `viz_kind: gsea_running_score`

The running enrichment score along the ranked gene list, one curve per gene set, with the set members as a rug.

![GSEA running score](../images/guides/advanced-visualizations/gsea_running_score_light.webp#only-light){ data-title="GSEA running score" .viz-shot loading=lazy }
![GSEA running score](../images/guides/advanced-visualizations/gsea_running_score_dark.webp#only-dark){ data-title="GSEA running score" .viz-shot loading=lazy }

**Input:** one row per gene set and rank.

| gene_set | rank | running_es | member <small>optional</small> | metric <small>optional</small> |
|---|---|---|---|---|
| HALLMARK_E2F_TARGETS | 1 | 0.012 | true | 3.21 |
| HALLMARK_E2F_TARGETS | 2 | 0.010 | false | 3.05 |
| HALLMARK_G2M_CHECKPOINT | 1 | 0.015 | true | 3.21 |

`member` is a boolean or 0/1.

**Compatible inputs:** GSEA output of nf-core/differentialabundance.

**Controls**

- Primary: Top-N gene sets, Layout
- Cosmetic: Shade the leading edge, Hit rug, Ranked metric

??? example "YAML"
    ```yaml
    - tag: viz-gsea-running-score
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: gsea_running
      viz_kind: gsea_running_score
      config:
        viz_kind: gsea_running_score
        gene_set_col: gene_set
        rank_col: rank
        running_es_col: running_es
        member_col: member
        metric_col: metric
        top_n_sets: 5
    ```

### :material-compare-horizontal: Group compare { #group-compare }

<span class="ver-badge">v1.13.0+</span> `viz_kind: group_compare`

Two groups of rows tested feature by feature on demand, drawn as a volcano over a ranked table. The groups come from the dashboard's [selection groups](interactive-selection-filtering.md#selection-groups) or from `group` values.

![Group compare](../images/guides/advanced-visualizations/group_compare_light.webp#only-light){ data-title="Group compare" .viz-shot loading=lazy }
![Group compare](../images/guides/advanced-visualizations/group_compare_dark.webp#only-dark){ data-title="Group compare" .viz-shot loading=lazy }

**Input:** one row per cell or sample, one numeric column per feature (wide format).

| cell_id | cluster <small>optional</small> | CD3E | MS4A1 | LYZ | ... |
|---|---|---|---|---|---|
| AAACCTGAGAAGGCCT-1 | cluster_1 | 2.31 | 0.0 | 0.0 | ... |
| AAACCTGAGACAGACC-1 | cluster_2 | 0.0 | 1.87 | 0.0 | ... |
| AAACCTGAGCGATAGC-1 | cluster_3 | 0.0 | 0.0 | 3.45 | ... |

Every numeric column is a feature to test.

**Compatible inputs:** Per-cell matrices from nf-core/scrnaseq, or per-sample normalised counts from nf-core/rnaseq.

**Controls**

- Primary: Group A, Group B, Test (Wilcoxon or t-test)
- Cosmetic: log1p before testing, FDR threshold, |log2FC| threshold, Top-N labels

??? example "YAML"
    ```yaml
    - tag: viz-group-compare
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: cell_by_gene
      viz_kind: group_compare
      config:
        viz_kind: group_compare
        index_col: cell_id
        group_col: cluster
        test: wilcoxon
        default_group_a: cluster_1
        default_group_b: cluster_2
        auto_run: true
    ```

---

## Single cell & embeddings { #single-cell }

### :material-atom: Embedding { #embedding }

<span class="ver-badge">v0.13.0+</span> `viz_kind: embedding`

Samples or cells in 2D or 3D, from precomputed coordinates or a PCA, UMAP, t-SNE or PCoA computed live on the server.

![Embedding](../images/guides/advanced-visualizations/embedding_light.webp#only-light){ data-title="Embedding" .viz-shot loading=lazy }
![Embedding](../images/guides/advanced-visualizations/embedding_dark.webp#only-dark){ data-title="Embedding" .viz-shot loading=lazy }

**Input:** one row per cell or sample.

| cell_id | umap_1 | umap_2 | cluster <small>optional</small> |
|---|---|---|---|
| AAACCTGAGAAGGCCT-1 | 4.12 | -1.37 | T cells |
| AAACCTGAGACAGACC-1 | -6.80 | 2.95 | B cells |
| AAACCTGAGCGATAGC-1 | 1.04 | 8.21 | Monocytes |

Also optional: `dim_3_col` (3D), `color_col`. With `compute_method` set, the coordinates are computed from the numeric columns instead.

**Compatible inputs:** scanpy or Seurat coordinates (nf-core/scrnaseq), or any sample by feature matrix with `compute_method` set.

**Controls**

- Primary: Method (live mode), View (2D, 3D), Colour by
- Cosmetic: Method parameters, plot style, legend, hover columns, point size, outline, density overlay, centroids

??? example "YAML"
    ```yaml
    - tag: viz-embedding
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: umap_coords
      viz_kind: embedding
      config:
        viz_kind: embedding
        sample_id_col: cell_id
        dim_1_col: umap_1
        dim_2_col: umap_2
        cluster_col: cluster
        selection_enabled: true
    ```

### :material-circle-multiple-outline: Dot plot { #dot-plot }

<span class="ver-badge">v0.13.0+</span> `viz_kind: dot_plot`

Marker genes by cluster: size is the fraction expressing, colour the mean expression. The `enrichment` view draws the same marks over a gene-set table.

![Dot plot](../images/guides/advanced-visualizations/dot_plot_light.webp#only-light){ data-title="Dot plot" .viz-shot loading=lazy }
![Dot plot](../images/guides/advanced-visualizations/dot_plot_dark.webp#only-dark){ data-title="Dot plot" .viz-shot loading=lazy }

**Input:** one row per cluster and gene (long format).

| cluster | gene | mean_expression | frac_expressing |
|---|---|---|---|
| T cells | CD3E | 2.14 | 0.87 |
| T cells | MS4A1 | 0.05 | 0.03 |
| B cells | MS4A1 | 1.92 | 0.81 |

The `enrichment` view reads one row per term instead: `term_col`, `nes_col`, optionally `padj_col`, `gene_count_col`, `source_col`.

**Compatible inputs:** scanpy aggregates per cluster (`sc.get.aggregate`); clusterProfiler, GSEA or g:Profiler results for the enrichment view.

**Controls**

- Primary: View (Dot plot, Enrichment); dot plot: Sort genes, Sort clusters, Max genes; enrichment: Source, Top-N pathways, padj threshold, Colour by, Sort terms
- Cosmetic: Colourscale, reverse colourscale, max and min dot size, outline, labels

??? example "YAML"
    ```yaml
    - tag: viz-dot-plot
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: marker_means
      viz_kind: dot_plot
      config:
        viz_kind: dot_plot
        cluster_col: cluster
        gene_col: gene
        mean_expression_col: mean_expression
        frac_expressing_col: frac_expressing
        views: [dotplot]
    ```

### :material-trending-down: Knee plot { #knee-plot }

<span class="ver-badge">v1.13.0+</span> `viz_kind: knee_plot`

Barcode rank against UMI count, one curve per library, with the cell-calling cutoff.

![Knee plot](../images/guides/advanced-visualizations/knee_plot_light.webp#only-light){ data-title="Knee plot" .viz-shot loading=lazy }
![Knee plot](../images/guides/advanced-visualizations/knee_plot_dark.webp#only-dark){ data-title="Knee plot" .viz-shot loading=lazy }

**Input:** one row per library and barcode rank.

| sample | rank | umi_count | is_cell <small>optional</small> |
|---|---|---|---|
| pbmc_1k | 1 | 48213 | true |
| pbmc_1k | 2 | 45120 | true |
| pbmc_1k | 1250 | 312 | false |

**Compatible inputs:** STARsolo, alevin-fry or Cell Ranger barcode counts (nf-core/scrnaseq).

**Controls**

- Primary: Log rank (x), Log UMI count (y)
- Cosmetic: Show cell-calling cutoff

??? example "YAML"
    ```yaml
    - tag: viz-knee-plot
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: barcode_ranks
      viz_kind: knee_plot
      config:
        viz_kind: knee_plot
        sample_col: sample
        rank_col: rank
        umi_count_col: umi_count
        is_cell_col: is_cell
    ```

---

## Genome tracks { #genome-tracks }

### :material-chart-areaspline: Coverage track { #coverage-track }

<span class="ver-badge">v0.13.0+</span> `viz_kind: coverage_track`

Depth or signal along a chromosome, per sample or as a cohort median. The `locus` view redraws it as a zoomable GenomeSpy track.

![Coverage track](../images/guides/advanced-visualizations/coverage_track_light.webp#only-light){ data-title="Coverage track" .viz-shot loading=lazy }
![Coverage track](../images/guides/advanced-visualizations/coverage_track_dark.webp#only-dark){ data-title="Coverage track" .viz-shot loading=lazy }

**Input:** one row per sample and bin (or base).

| chrom | start | end <small>optional</small> | depth | sample <small>optional</small> |
|---|---|---|---|---|
| MN908947.3 | 0 | 100 | 812 | SAMPLE_01 |
| MN908947.3 | 100 | 200 | 1450 | SAMPLE_01 |
| MN908947.3 | 0 | 100 | 37 | SAMPLE_02 |

Also optional: `category_col`.

**Compatible inputs:** mosdepth per-base or per-bin depth (nf-core/viralrecon, sarek, rnaseq), bigWig-derived bins.

**Controls**

- Primary: View (Track, Locus), Sample layout, Y scale, Smoothing, Chromosomes, Samples
- Cosmetic: Mark, Colour by, Show individual traces, gene strip

??? example "YAML"
    ```yaml
    - tag: viz-coverage-track
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: depth_bins
      viz_kind: coverage_track
      config:
        viz_kind: coverage_track
        chromosome_col: chrom
        position_col: start
        end_col: end
        value_col: depth
        sample_col: sample
        views: [track, locus]
    ```

### :material-chart-timeline: Genome view { #genome-view }

<span class="ver-badge">v1.13.0+</span> `viz_kind: genome_view`

A [GenomeSpy](https://genomespy.app/){ target="_blank" } track on a chromosome axis: scroll to zoom, drag to pan, brush or type a locus to filter the dashboard by region.

![Genome view](../images/guides/advanced-visualizations/genome_view_light.webp#only-light){ data-title="Genome view" .viz-shot loading=lazy }
![Genome view](../images/guides/advanced-visualizations/genome_view_dark.webp#only-dark){ data-title="Genome view" .viz-shot loading=lazy }

**Input:** one row per position, or per interval with `end`.

| chrom | start | end <small>optional</small> | score | peak_class <small>optional</small> |
|---|---|---|---|---|
| chr8 | 127735800 | 127736600 | 42.7 | promoter |
| chr8 | 127790100 | 127790900 | 11.3 | enhancer |
| chr8 | 127982400 | 127983000 | 6.9 | enhancer |

Also optional: `feature_col`, `sample_col` (one lane per sample).

**Compatible inputs:** Any chr / pos / score table: peaks, depth bins, association scores.

**Controls**

- Primary: Chromosome, Locus or gene
- Cosmetic: Mark, point size, opacity, threshold rule, one lane per sample, max lanes, assembly, gene annotation lane, zoom to an incoming region

??? example "YAML"
    ```yaml
    - tag: viz-genome-view
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: peaks
      viz_kind: genome_view
      config:
        viz_kind: genome_view
        chr_col: chrom
        pos_col: start
        end_col: end
        score_col: score
        category_col: peak_class
        mark: bar
        assembly: hg38
        default_region: "chr8:127,400,000-128,100,000"
    ```

### :material-chart-scatter-plot-hexbin: Copy-number profile { #cnv-profile }

<span class="ver-badge">v1.13.0+</span> `viz_kind: cnv_profile`

Log2 ratio per bin with the called segments over it and the B-allele frequency underneath. The `locus` view draws the allele-specific layout.

![Copy-number profile](../images/guides/advanced-visualizations/cnv_profile_light.webp#only-light){ data-title="Copy-number profile" .viz-shot loading=lazy }
![Copy-number profile](../images/guides/advanced-visualizations/cnv_profile_dark.webp#only-dark){ data-title="Copy-number profile" .viz-shot loading=lazy }

**Input:** one row per bin or called segment, both in one table.

| sample | chrom | start | end | log2 | segment <small>optional</small> |
|---|---|---|---|---|---|
| TUMOUR_A | chr1 | 1000000 | 1100000 | 0.14 | bin |
| TUMOUR_A | chr1 | 1100000 | 1200000 | 0.06 | bin |
| TUMOUR_A | chr1 | 1000000 | 52000000 | 0.10 | segment |

Rows whose `segment` value is `segment` draw as segments, the rest as bins. Also optional: `baf_col`, `copy_number_col`, `label_col`.

**Compatible inputs:** CNVkit, ASCAT or Control-FREEC bins and segments (nf-core/sarek).

**Controls**

- Primary: View (Plotly, Locus), Sample, Chromosome
- Cosmetic: log2 axis limit, bin marker size, Show BAF panel, gene lane

??? example "YAML"
    ```yaml
    - tag: viz-cnv-profile
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: cnv_bins_segments
      viz_kind: cnv_profile
      config:
        viz_kind: cnv_profile
        sample_col: sample
        chrom_col: chrom
        start_col: start
        end_col: end
        log2_col: log2
        baf_col: baf
        segment_col: segment
        views: [plotly, locus]
    ```

### :material-triangle-outline: Contact map { #contact-map }

<span class="ver-badge">v1.13.0+</span> `viz_kind: contact_map`

A binned Hi-C matrix, square or as a triangle under a genome track. Zooming re-reads the best resolution for the window.

![Contact map](../images/guides/advanced-visualizations/contact_map_light.webp#only-light){ data-title="Contact map" .viz-shot loading=lazy }
![Contact map](../images/guides/advanced-visualizations/contact_map_dark.webp#only-dark){ data-title="Contact map" .viz-shot loading=lazy }

**Input:** one row per pair of bins.

| chrom | start | chrom2 | start2 | count | resolution <small>optional</small> |
|---|---|---|---|---|---|
| chr1 | 0 | chr1 | 0 | 2841 | 100000 |
| chr1 | 0 | chr1 | 100000 | 932 | 100000 |
| chr1 | 0 | chr1 | 0 | 10520 | 500000 |

Also optional: `end1_col`, `end2_col`, `sample_col`.

**Compatible inputs:** cooler `.mcool` pixels dumped per resolution (nf-core/hic).

**Controls**

- Primary: Chromosome, Display (square, triangle), Resolution
- Cosmetic: Colour scale, log colour scale, row/column balance, separation drawn

??? example "YAML"
    ```yaml
    - tag: viz-contact-map
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: hic_pixels
      viz_kind: contact_map
      config:
        viz_kind: contact_map
        chrom1_col: chrom
        start1_col: start
        chrom2_col: chrom2
        start2_col: start2
        count_col: count
        resolution_col: resolution
        display: triangle
    ```

### :material-reorder-horizontal: Transcript structure { #transcript-structure }

<span class="ver-badge">v1.13.0+</span> `viz_kind: transcript_structure`

The isoforms of one gene, one lane per transcript, exons as blocks and coding parts taller.

![Transcript structure](../images/guides/advanced-visualizations/transcript_structure_light.webp#only-light){ data-title="Transcript structure" .viz-shot loading=lazy }
![Transcript structure](../images/guides/advanced-visualizations/transcript_structure_dark.webp#only-dark){ data-title="Transcript structure" .viz-shot loading=lazy }

**Input:** one row per exon or CDS block.

| transcript_id | gene_id | chrom | start | end | feature | strand |
|---|---|---|---|---|---|---|
| ENST00000269305 | ENSG00000141510 | chr17 | 7661779 | 7662014 | exon | - |
| ENST00000269305 | ENSG00000141510 | chr17 | 7669609 | 7669690 | CDS | - |
| ENST00000413465 | ENSG00000141510 | chr17 | 7668421 | 7669690 | exon | - |

Also optional: `transcript_class_col`, `sample_col`, `gene_name_col`, `expression_col`.

**Compatible inputs:** StringTie or bambu GTF exon and CDS rows (nf-core/nanoseq, rnaseq).

**Controls**

- Primary: Gene, Sample, Colour lanes by
- Cosmetic: Colour scale, bar beside each lane, isoforms drawn

??? example "YAML"
    ```yaml
    - tag: viz-transcript-structure
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: transcript_blocks
      viz_kind: transcript_structure
      config:
        viz_kind: transcript_structure
        transcript_id_col: transcript_id
        gene_id_col: gene_id
        chrom_col: chrom
        start_col: start
        end_col: end
        feature_col: feature
        strand_col: strand
        transcript_class_col: transcript_class
    ```

### :material-vector-curve: Sashimi { #sashimi }

<span class="ver-badge">v1.11.0+</span> `viz_kind: sashimi`

Splice junctions as arcs over a region, weighted by read support, with coverage and an exon model underneath.

![Sashimi](../images/guides/advanced-visualizations/sashimi_light.webp#only-light){ data-title="Sashimi" .viz-shot loading=lazy }
![Sashimi](../images/guides/advanced-visualizations/sashimi_dark.webp#only-dark){ data-title="Sashimi" .viz-shot loading=lazy }

**Input:** one row per junction and sample.

| chrom | start | end | count | sample <small>optional</small> | annotation <small>optional</small> |
|---|---|---|---|---|---|
| chr17 | 7670715 | 7673534 | 412 | WT_REP1 | known |
| chr17 | 7673609 | 7673700 | 198 | WT_REP1 | known |
| chr17 | 7670715 | 7673700 | 23 | KD_REP1 | novel |

The optional coverage collection (`coverage_dc_tag`) has one row per bin: `chrom`, `start`, `end`, `depth`, `sample`, bound by the `coverage_*_col` keys.

**Compatible inputs:** STAR `SJ.out.tab` junctions plus binned coverage (nf-core/rnaseq, rnafusion, nanoseq).

**Controls**

- Primary: View (Plotly, GenomeSpy), Locus
- Cosmetic: Junctions kept, zoom, read depth under the arcs, log depth axis, exon support, exon model lane, arc width and colour

??? example "YAML"
    ```yaml
    - tag: viz-sashimi
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: junctions
      viz_kind: sashimi
      config:
        viz_kind: sashimi
        chr_col: chrom
        start_col: start
        end_col: end
        count_col: count
        sample_col: sample
        annotation_col: annotation
        coverage_dc_tag: binned_coverage
        coverage_chr_col: chrom
        coverage_position_col: start
        coverage_end_col: end
        coverage_value_col: depth
        coverage_sample_col: sample
        views: [genomespy, plotly]
    ```

### :material-arrow-right-bold-outline: Gene arrow track { #gene-arrow-track }

<span class="ver-badge">v1.11.0+</span> `viz_kind: gene_arrow_track`

One arrow per coding sequence along a contig, the way a gene cluster or a resistance cassette is read.

![Gene arrow track](../images/guides/advanced-visualizations/gene_arrow_track_light.webp#only-light){ data-title="Gene arrow track" .viz-shot loading=lazy }
![Gene arrow track](../images/guides/advanced-visualizations/gene_arrow_track_dark.webp#only-dark){ data-title="Gene arrow track" .viz-shot loading=lazy }

**Input:** one row per gene.

| contig | feature_id | start | end | strand | gene_class <small>optional</small> |
|---|---|---|---|---|---|
| NODE_12_length_84211 | PROKKA_01234 | 1200 | 2850 | + | biosynthetic |
| NODE_12_length_84211 | PROKKA_01235 | 2990 | 4410 | + | transport |
| NODE_12_length_84211 | PROKKA_01236 | 4620 | 5300 | - | regulatory |

Also optional: `label_col` (`label` above), `region_start_col`, `region_end_col`.

**Compatible inputs:** antiSMASH or nf-core/funcscan BGC calls, Prokka or Bakta annotations (nf-core/mag, bacass).

**Controls**

- Primary: Lanes shown, Lane order, Align lanes
- Cosmetic: Highlight region, feature labels, arrow height

??? example "YAML"
    ```yaml
    - tag: viz-gene-arrow-track
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: bgc_genes
      viz_kind: gene_arrow_track
      config:
        viz_kind: gene_arrow_track
        contig_col: contig
        feature_id_col: feature_id
        start_col: start
        end_col: end
        strand_col: strand
        class_col: gene_class
        label_col: label
    ```

---

## Variants & rearrangements { #variants }

### :material-chart-histogram: Manhattan { #manhattan }

<span class="ver-badge">v0.13.0+</span> `viz_kind: manhattan`

A score along the genome, chromosomes end to end. `mode: rainfall` plots the distance between variants instead, so mutation clusters sink.

![Manhattan](../images/guides/advanced-visualizations/manhattan_light.webp#only-light){ data-title="Manhattan" .viz-shot loading=lazy }
![Manhattan](../images/guides/advanced-visualizations/manhattan_dark.webp#only-dark){ data-title="Manhattan" .viz-shot loading=lazy }

**Input:** one row per variant.

| chr | pos | score | feature <small>optional</small> |
|---|---|---|---|
| chr1 | 109274968 | 12.4 | rs12740374 |
| chr19 | 44908684 | 30.2 | rs429358 |
| chr2 | 21001429 | 4.1 | rs693 |

`score` is usually -log10(p). Also optional: `effect_col`.

**Compatible inputs:** PLINK `.assoc`, GWAS or QTL summary statistics, somatic VCFs (nf-core/sarek).

**Controls**

- Primary: Figure (Score, Rainfall), Colour by, Chromosomes, Threshold, Highlight
- Cosmetic: Top-N labels, marker size

??? example "YAML"
    ```yaml
    - tag: viz-manhattan
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: gwas_hits
      viz_kind: manhattan
      config:
        viz_kind: manhattan
        chr_col: chr
        pos_col: pos
        score_col: score
        feature_col: feature
        score_threshold: 5.0
        selection_enabled: true
        selection_column: feature
    ```

### :material-chart-timeline-variant: Lollipop { #lollipop }

<span class="ver-badge">v0.13.0+</span> `viz_kind: lollipop`

Variants as stems along a gene or protein, coloured by consequence. With `selection_enabled` a click also picks the residue for the [protein tiles](#residue-selection).

![Lollipop](../images/guides/advanced-visualizations/lollipop_light.webp#only-light){ data-title="Lollipop" .viz-shot loading=lazy }
![Lollipop](../images/guides/advanced-visualizations/lollipop_dark.webp#only-dark){ data-title="Lollipop" .viz-shot loading=lazy }

**Input:** one row per variant.

| Hugo_Symbol | Protein_position | Variant_Classification | VAF <small>optional</small> | HGVSp_Short <small>optional</small> |
|---|---|---|---|---|
| TP53 | 175 | Missense_Mutation | 0.42 | p.R175H |
| TP53 | 196 | Nonsense_Mutation | 0.31 | p.R196* |
| KRAS | 12 | Missense_Mutation | 0.21 | p.G12D |

**Compatible inputs:** Mutation Annotation Format tables (maftools, vcf2maf) or VEP / snpEff annotated VCFs (nf-core/sarek).

**Controls**

- Primary: Gene, Sort genes
- Cosmetic: Point size, stem width, scale points by |effect|, show stems, marker outline, palette, label top-N

??? example "YAML"
    ```yaml
    - tag: viz-lollipop
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: variants
      viz_kind: lollipop
      config:
        viz_kind: lollipop
        feature_id_col: Hugo_Symbol
        position_col: Protein_position
        category_col: Variant_Classification
        effect_col: VAF
        label_col: HGVSp_Short
    ```

### :material-grid-large: Oncoplot { #oncoplot }

<span class="ver-badge">v0.13.0+</span> `viz_kind: oncoplot`

A sample by gene mutation matrix, cells coloured by mutation type, with frequency strips.

![Oncoplot](../images/guides/advanced-visualizations/oncoplot_light.webp#only-light){ data-title="Oncoplot" .viz-shot loading=lazy }
![Oncoplot](../images/guides/advanced-visualizations/oncoplot_dark.webp#only-dark){ data-title="Oncoplot" .viz-shot loading=lazy }

**Input:** one row per mutation (sample and gene).

| Tumor_Sample_Barcode | Hugo_Symbol | Variant_Classification |
|---|---|---|
| TCGA-A1-A0SB-01 | TP53 | Missense_Mutation |
| TCGA-A1-A0SB-01 | PIK3CA | Missense_Mutation |
| TCGA-A2-A0CM-01 | TP53 | Frame_Shift_Del |

**Compatible inputs:** Mutation Annotation Format tables: `Tumor_Sample_Barcode`, `Hugo_Symbol`, `Variant_Classification` (nf-core/sarek).

**Controls**

- Primary: Sort by mutation frequency
- Cosmetic: None

??? example "YAML"
    ```yaml
    - tag: viz-oncoplot
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: somatic_maf
      viz_kind: oncoplot
      config:
        viz_kind: oncoplot
        sample_id_col: Tumor_Sample_Barcode
        gene_col: Hugo_Symbol
        mutation_type_col: Variant_Classification
    ```

### :material-circle-double: Genome chord { #genome-chord }

<span class="ver-badge">v1.13.0+</span> `viz_kind: genome_chord`

Chromosomes on a ring, one chord per link between two loci: fusions, breakends, translocations.

![Genome chord](../images/guides/advanced-visualizations/genome_chord_light.webp#only-light){ data-title="Genome chord" .viz-shot loading=lazy }
![Genome chord](../images/guides/advanced-visualizations/genome_chord_dark.webp#only-dark){ data-title="Genome chord" .viz-shot loading=lazy }

**Input:** one row per link between two loci.

| chrom_a | pos_a | chrom_b | pos_b | support <small>optional</small> | sv_type <small>optional</small> |
|---|---|---|---|---|---|
| chr9 | 130714000 | chr22 | 23290000 | 54 | BND |
| chr2 | 29223000 | chr2 | 42299000 | 18 | INV |
| chr7 | 55019000 | chr7 | 55211000 | 9 | DEL |

Also optional: `label_col`, `sample_col`.

**Compatible inputs:** Manta, TIDDIT or SvABA breakends (nf-core/sarek), arriba or STAR-Fusion fusions (nf-core/rnafusion).

**Controls**

- Primary: Assembly, Colour by
- Cosmetic: Links drawn, minimum weight, intra-chromosomal links, chromosome labels

??? example "YAML"
    ```yaml
    - tag: viz-genome-chord
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: sv_links
      viz_kind: genome_chord
      config:
        viz_kind: genome_chord
        chrom_a_col: chrom_a
        pos_a_col: pos_a
        chrom_b_col: chrom_b
        pos_b_col: pos_b
        weight_col: support
        category_col: sv_type
        assembly: hg38
    ```

### :material-call-merge: Fusion structure { #fusion-structure }

<span class="ver-badge">v1.11.0+</span> `viz_kind: fusion_structure`

A fusion drawn as its two partners, with the protein domains kept or lost at the breakpoint.

![Fusion structure](../images/guides/advanced-visualizations/fusion_structure_light.webp#only-light){ data-title="Fusion structure" .viz-shot loading=lazy }
![Fusion structure](../images/guides/advanced-visualizations/fusion_structure_dark.webp#only-dark){ data-title="Fusion structure" .viz-shot loading=lazy }

**Input:** one row per domain of each partner.

| fusion_id | partner | feature | start | end | breakpoint <small>optional</small> |
|---|---|---|---|---|---|
| BCR::ABL1 | BCR | Bcr-Abl oncoprotein oligomerization | 1 | 72 | 426 |
| BCR::ABL1 | ABL1 | SH3 | 61 | 121 | 27 |
| BCR::ABL1 | ABL1 | Protein kinase | 242 | 493 | 27 |

Also optional: `retained_col` (fraction kept, 0 to 1), `colour_by_col`.

**Compatible inputs:** Arriba or STAR-Fusion calls (nf-core/rnafusion).

**Controls**

- Primary: Fusions (how many)
- Cosmetic: Bar height, mark the breakpoint, name each domain, position axis

??? example "YAML"
    ```yaml
    - tag: viz-fusion-structure
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: fusion_domains
      viz_kind: fusion_structure
      config:
        viz_kind: fusion_structure
        fusion_id_col: fusion_id
        partner_col: partner
        feature_col: feature
        start_col: start
        end_col: end
        breakpoint_col: breakpoint
        retained_col: retained
    ```

---

## Signal & read profiles { #profiles }

### :material-chart-bell-curve: Profile { #profile }

<span class="ver-badge">v1.11.0+</span> `viz_kind: profile`

One curve per series over an ordered numeric axis, with an optional band. A TSS profile, a fragment-length ladder or a per-residue pLDDT curve.

![Profile](../images/guides/advanced-visualizations/profile_light.webp#only-light){ data-title="Profile" .viz-shot loading=lazy }
![Profile](../images/guides/advanced-visualizations/profile_dark.webp#only-dark){ data-title="Profile" .viz-shot loading=lazy }

**Input:** one row per series and x value (long format).

| sample | distance | signal |
|---|---|---|
| H3K4me3_rep1 | -1000 | 0.82 |
| H3K4me3_rep1 | 0 | 6.41 |
| Input | 0 | 0.95 |

Also optional: `lower_col`, `upper_col` (the band).

**Compatible inputs:** deepTools profiles (nf-core/atacseq, chipseq), riboWaltz, crisprseq.

**Controls**

- Primary: Log x, Log y, Local log-log slope panel
- Cosmetic: Line width, band opacity, legend

??? example "YAML"
    ```yaml
    - tag: viz-profile
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: tss_profile
      viz_kind: profile
      config:
        viz_kind: profile
        series_col: sample
        x_col: distance
        y_col: signal
        reference_x: 0
        reference_label: TSS
    ```

### :material-view-grid-outline: Signal matrix { #signal-matrix }

<span class="ver-badge">v1.11.0+</span> `viz_kind: signal_matrix`

The heatmap under a profile: one row per region, one column per offset, rows ordered by signal.

![Signal matrix](../images/guides/advanced-visualizations/signal_matrix_light.webp#only-light){ data-title="Signal matrix" .viz-shot loading=lazy }
![Signal matrix](../images/guides/advanced-visualizations/signal_matrix_dark.webp#only-dark){ data-title="Signal matrix" .viz-shot loading=lazy }

**Input:** one row per region and offset (long format).

| region_id | position | value | group <small>optional</small> |
|---|---|---|---|
| peak_00412 | -500 | 1.2 | H3K27ac |
| peak_00412 | 0 | 8.7 | H3K27ac |
| peak_01877 | 0 | 5.3 | H3K4me1 |

**Compatible inputs:** deepTools `computeMatrix` output in long form (nf-core/atacseq, chipseq, cutandrun).

**Controls**

- Primary: Row order, Max rows
- Cosmetic: Colour scale, mean profile above the matrix

??? example "YAML"
    ```yaml
    - tag: viz-signal-matrix
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: peak_matrix
      viz_kind: signal_matrix
      config:
        viz_kind: signal_matrix
        region_id_col: region_id
        position_col: position
        value_col: value
        group_col: group
        reference_label: Peak summit
    ```

### :material-dna: Damage profile { #damage-profile }

<span class="ver-badge">v1.13.0+</span> `viz_kind: damage_profile`

Ancient-DNA misincorporation by distance from the read end. C>T at 5' and G>A at 3' are highlighted.

![Damage profile](../images/guides/advanced-visualizations/damage_profile_light.webp#only-light){ data-title="Damage profile" .viz-shot loading=lazy }
![Damage profile](../images/guides/advanced-visualizations/damage_profile_dark.webp#only-dark){ data-title="Damage profile" .viz-shot loading=lazy }

**Input:** one row per sample, read end, position and substitution.

| sample | end | position | base_change | frequency |
|---|---|---|---|---|
| Lib_01 | 5p | 1 | C>T | 0.231 |
| Lib_01 | 5p | 1 | G>A | 0.012 |
| Lib_01 | 3p | 1 | G>A | 0.198 |

`end` is `5p` or `3p`. Also optional: a `length_bin` column, read with `facet_by: length_bin`.

**Compatible inputs:** DamageProfiler or mapDamage substitution tables (nf-core/eager).

**Controls**

- Primary: Ends, Highlight, One lane per read-length bin
- Cosmetic: Max position

??? example "YAML"
    ```yaml
    - tag: viz-damage-profile
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: misincorporation
      viz_kind: damage_profile
      config:
        viz_kind: damage_profile
        sample_col: sample
        end_col: end
        position_col: position
        base_change_col: base_change
        frequency_col: frequency
    ```

---

## Microbiome & ecology { #microbiome }

### :material-chart-bar-stacked: Stacked taxonomy { #stacked-taxonomy }

<span class="ver-badge">v0.13.0+</span> `viz_kind: stacked_taxonomy`

Per-sample composition at one taxonomic rank, the tail folded into `Other`, with optional metadata strips.

![Stacked taxonomy](../images/guides/advanced-visualizations/stacked_taxonomy_light.webp#only-light){ data-title="Stacked taxonomy" .viz-shot loading=lazy }
![Stacked taxonomy](../images/guides/advanced-visualizations/stacked_taxonomy_dark.webp#only-dark){ data-title="Stacked taxonomy" .viz-shot loading=lazy }

**Input:** one row per sample, taxon and rank (long format).

| sample_id | taxon | rank | abundance |
|---|---|---|---|
| S01 | Bacteroidota | Phylum | 0.42 |
| S01 | Bacillota | Phylum | 0.35 |
| S01 | Bacteroides | Genus | 0.21 |

**Compatible inputs:** QIIME2 `taxa-collapse` tables (nf-core/ampliseq), taxprofiler or mag abundance tables.

**Controls**

- Primary: Rank, Top-N taxa, Sort samples, Normalise
- Cosmetic: Legend, log y

??? example "YAML"
    ```yaml
    - tag: viz-stacked-taxonomy
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: taxa_long
      viz_kind: stacked_taxonomy
      config:
        viz_kind: stacked_taxonomy
        sample_id_col: sample_id
        taxon_col: taxon
        rank_col: rank
        abundance_col: abundance
        default_rank: Phylum
        top_n: 12
    ```

### :material-sun-wireless: Sunburst { #sunburst }

<span class="ver-badge">v0.13.0+</span> `viz_kind: sunburst`

A taxonomy or pathway hierarchy as rings from root to leaf, each ring a shade of its lineage.

![Sunburst](../images/guides/advanced-visualizations/sunburst_light.webp#only-light){ data-title="Sunburst" .viz-shot loading=lazy }
![Sunburst](../images/guides/advanced-visualizations/sunburst_dark.webp#only-dark){ data-title="Sunburst" .viz-shot loading=lazy }

**Input:** one row per leaf, one column per rank (wide format), root first.

| Kingdom | Phylum | Class | ... | Genus | abundance |
|---|---|---|---|---|---|
| Bacteria | Bacteroidota | Bacteroidia | ... | Bacteroides | 1520 |
| Bacteria | Bacillota | Clostridia | ... | Faecalibacterium | 980 |
| Bacteria | Pseudomonadota | Gammaproteobacteria | ... | Escherichia | 211 |

**Compatible inputs:** Kraken2 `.kreport` pivoted to rank columns, nf-core/ampliseq or taxprofiler classifications.

**Controls**

- Primary: Start from rank, Max depth, Colour by rank
- Cosmetic: Palette, min arc (% of root), show % on arcs

??? example "YAML"
    ```yaml
    - tag: viz-sunburst
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: taxa_wide
      viz_kind: sunburst
      config:
        viz_kind: sunburst
        rank_cols: [Kingdom, Phylum, Class, Order, Family, Genus]
        abundance_col: abundance
    ```

### :material-chart-line: Rarefaction { #rarefaction }

<span class="ver-badge">v0.13.0+</span> `viz_kind: rarefaction`

Alpha diversity against sequencing depth, one curve per sample, mean and SE over iterations.

![Rarefaction](../images/guides/advanced-visualizations/rarefaction_light.webp#only-light){ data-title="Rarefaction" .viz-shot loading=lazy }
![Rarefaction](../images/guides/advanced-visualizations/rarefaction_dark.webp#only-dark){ data-title="Rarefaction" .viz-shot loading=lazy }

**Input:** one row per sample, depth and iteration, one column per metric.

| sample_id | depth | iter <small>optional</small> | shannon | observed_features | habitat <small>optional</small> |
|---|---|---|---|---|---|
| S01 | 1000 | 1 | 3.82 | 212 | soil |
| S01 | 1000 | 2 | 3.79 | 205 | soil |
| S02 | 1000 | 1 | 2.41 | 98 | marine |

Each name in `metric_options` (here also `faith_pd`) is a numeric column; `metric_col` is the one shown first.

**Compatible inputs:** QIIME2 `alpha-rarefaction` tables (nf-core/ampliseq).

**Controls**

- Primary: Metric tabs, Group by, Top-N samples
- Cosmetic: Error bars (±SE)

??? example "YAML"
    ```yaml
    - tag: viz-rarefaction
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: rarefaction_long
      viz_kind: rarefaction
      config:
        viz_kind: rarefaction
        sample_id_col: sample_id
        depth_col: depth
        metric_col: shannon
        metric_options: [shannon, observed_features, faith_pd]
        iter_col: iter
        group_col: habitat
    ```

### :material-family-tree: Phylogenetic tree { #phylogenetic }

<span class="ver-badge">v0.13.0+</span> `viz_kind: phylogenetic`

A Newick tree with tip metadata, five layouts, clade selection, filter and collapse. `collapse_rank` turns it into a summary by rank.

![Phylogenetic tree](../images/guides/advanced-visualizations/phylogenetic_light.webp#only-light){ data-title="Phylogenetic tree" .viz-shot loading=lazy }
![Phylogenetic tree](../images/guides/advanced-visualizations/phylogenetic_dark.webp#only-dark){ data-title="Phylogenetic tree" .viz-shot loading=lazy }

**Input:** a Newick tree (a `phylogeny` collection, `tree_dc_tag`) plus a tip table, one row per tip.

| taxon | Phylum <small>optional</small> |
|---|---|
| ASV_0001 | Bacteroidota |
| ASV_0002 | Bacillota |
| ASV_0003 | Pseudomonadota |

`taxon` matches the tip labels of the tree. Also optional: `label_col`, `extra_color_cols`, and an abundance table (`abundance_dc_tag`) to size a summary by reads.

**Compatible inputs:** IQ-TREE or FastTree Newick plus a tip metadata table (nf-core/bactmap, pathogensurveillance, ampliseq).

**Controls**

- Primary: View (Full tree, Summary), Colour by, Search tip, Layout, Ladderise; summary: Collapse to, Top N
- Cosmetic: Label by, metadata strips, legend, support values, scale bar; toolbar: undo, redo, zoom and pan, reset, focus mode

??? example "YAML"
    ```yaml
    - tag: viz-phylogenetic
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: tree_metadata
      viz_kind: phylogenetic
      config:
        viz_kind: phylogenetic
        tree_wf_id: 646b0f3c1e4a2d7f8e5b8ca3   # placeholder ids, rewritten
        tree_dc_id: 646b0f3c1e4a2d7f8e5b8cdb   # from tree_dc_tag at import
        tree_dc_tag: phylogenetic_tree
        metadata_dc_tag: tree_metadata
        taxon_col: taxon
        color_col: Phylum
    ```

---

## General purpose { #general }

### :material-scatter-plot: Scatter (X/Y) { #scatter-xy }

<span class="ver-badge">v1.11.0+</span> `viz_kind: scatter_xy`

Numeric against numeric, with a size column, a reference line, log axes and a selection key.

![Scatter (X/Y)](../images/guides/advanced-visualizations/scatter_xy_light.webp#only-light){ data-title="Scatter (X/Y)" .viz-shot loading=lazy }
![Scatter (X/Y)](../images/guides/advanced-visualizations/scatter_xy_dark.webp#only-dark){ data-title="Scatter (X/Y)" .viz-shot loading=lazy }

**Input:** one row per point.

| rep_a | rep_b | gene <small>optional</small> | mean_expression <small>optional</small> |
|---|---|---|---|
| 812.4 | 790.1 | GAPDH | 801.3 |
| 15.2 | 22.8 | IL6 | 19.0 |
| 0.4 | 3.1 | FOXP3 | 1.8 |

Also optional: `color_col`.

**Compatible inputs:** Any table with two numeric columns: replicate concordance, QC metric pairs.

**Controls**

- Primary: Cloud (Points, Density), Log x, Log y, Reference line, Reference value, Highlight
- Cosmetic: Marker size, opacity, marker outline, top-N labels, colourscale, legend

??? example "YAML"
    ```yaml
    - tag: viz-scatter-xy
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: normalised_counts
      viz_kind: scatter_xy
      config:
        viz_kind: scatter_xy
        x_col: rep_a
        y_col: rep_b
        label_col: gene
        size_col: mean_expression
        reference_line: diagonal
        log_x: true
        log_y: true
    ```

### :material-grid: Hierarchical heatmap { #hierarchical-heatmap }

<span class="ver-badge">v0.13.0+</span> `viz_kind: complex_heatmap`

A clustered matrix with dendrograms and annotation tracks, computed on the server.

![Hierarchical heatmap](../images/guides/advanced-visualizations/complex_heatmap_light.webp#only-light){ data-title="Hierarchical heatmap" .viz-shot loading=lazy }
![Hierarchical heatmap](../images/guides/advanced-visualizations/complex_heatmap_dark.webp#only-dark){ data-title="Hierarchical heatmap" .viz-shot loading=lazy }

**Input:** one row per sample, one numeric column per gene (wide format).

| sample_id | condition <small>optional</small> | TP53 | EGFR | MYC | ... |
|---|---|---|---|---|---|
| ctrl_1 | control | 9.81 | 7.42 | 11.03 | ... |
| ctrl_2 | control | 9.76 | 7.55 | 10.96 | ... |
| treat_1 | treated | 8.12 | 9.87 | 12.40 | ... |

Every numeric column is a heatmap column, or only those listed in `value_columns`.

**Compatible inputs:** A normalised count matrix such as DESeq2 `vst()` (nf-core/rnaseq, differentialabundance).

**Controls**

- Primary: Normalisation, Clustering method, Cluster rows, Cluster columns
- Cosmetic: Row annotations, column annotations

??? example "YAML"
    ```yaml
    - tag: viz-complex-heatmap
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: vst_matrix
      viz_kind: complex_heatmap
      config:
        viz_kind: complex_heatmap
        index_column: sample_id
        row_annotation_cols: [condition]
        normalize: row_z
        cluster_method: ward
    ```

### :material-set-center: UpSet { #upset }

<span class="ver-badge">v0.13.0+</span> `viz_kind: upset_plot`

Set intersections as bars over a dot matrix: the readable alternative to a Venn diagram.

![UpSet](../images/guides/advanced-visualizations/upset_plot_light.webp#only-light){ data-title="UpSet" .viz-shot loading=lazy }
![UpSet](../images/guides/advanced-visualizations/upset_plot_dark.webp#only-dark){ data-title="UpSet" .viz-shot loading=lazy }

**Input:** one row per item, one 0/1 column per set.

| contrastA | contrastB | contrastC |
|---|---|---|
| 1 | 0 | 1 |
| 1 | 1 | 0 |
| 0 | 0 | 1 |

With `set_columns` unset, the 0/1 columns are detected.

**Compatible inputs:** Any binary membership table: features called per contrast, taxa per site.

**Controls**

- Primary: Sort by, Order, Min intersection size, Colour intersections by
- Cosmetic: Show annotations, set-size bars, intersection count labels, annotation tracks

??? example "YAML"
    ```yaml
    - tag: viz-upset-plot
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: membership
      viz_kind: upset_plot
      config:
        viz_kind: upset_plot
        set_columns: [contrastA, contrastB, contrastC]
        sort_by: cardinality
        min_size: 1
    ```

### :material-chart-sankey: Sankey { #sankey }

<span class="ver-badge">v0.13.0+</span> `viz_kind: sankey`

Categorical flow across ordered levels, such as sample to lineage to clade.

![Sankey](../images/guides/advanced-visualizations/sankey_light.webp#only-light){ data-title="Sankey" .viz-shot loading=lazy }
![Sankey](../images/guides/advanced-visualizations/sankey_dark.webp#only-dark){ data-title="Sankey" .viz-shot loading=lazy }

**Input:** one row per item, one categorical column per level, in order.

| qc_status | lineage | clade |
|---|---|---|
| pass | XBB.1.5 | 23A |
| pass | JN.1 | 24A |
| fail | unassigned | unassigned |

Also optional: `value_col`, a numeric weight; unset counts rows.

**Compatible inputs:** Any tidy table with ordered categorical columns (nf-core/viralrecon QC, Pangolin and Nextclade).

**Controls**

- Primary: Depth, Colour links by, Sort nodes
- Cosmetic: Link opacity, node labels, min link value

??? example "YAML"
    ```yaml
    - tag: viz-sankey
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: lineage_calls
      viz_kind: sankey
      config:
        viz_kind: sankey
        step_cols: [qc_status, lineage, clade]
    ```

### :material-chart-line-variant: Parallel coordinates { #parallel-coordinates }

<span class="ver-badge">v1.13.0+</span> `viz_kind: parallel_coordinates`

One polyline per sample across many metric axes. A brush on an axis becomes a range filter.

![Parallel coordinates](../images/guides/advanced-visualizations/parallel_coordinates_light.webp#only-light){ data-title="Parallel coordinates" .viz-shot loading=lazy }
![Parallel coordinates](../images/guides/advanced-visualizations/parallel_coordinates_dark.webp#only-dark){ data-title="Parallel coordinates" .viz-shot loading=lazy }

**Input:** one row per sample.

| sample | group <small>optional</small> | total_reads | percent_duplicates | percent_gc | percent_aligned |
|---|---|---|---|---|---|
| WT_REP1 | WT | 24813402 | 18.2 | 48.9 | 94.1 |
| WT_REP2 | WT | 22104377 | 17.5 | 49.2 | 93.8 |
| KO_REP1 | KO | 26990218 | 31.4 | 51.0 | 88.6 |

With `metric_cols` unset, every numeric column is an axis.

**Compatible inputs:** Any per-sample QC table, such as MultiQC general statistics.

**Controls**

- Primary: Axis scale, Colour by, Reset brushes
- Cosmetic: Colourscale, line opacity

??? example "YAML"
    ```yaml
    - tag: viz-parallel-coordinates
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: qc_metrics
      viz_kind: parallel_coordinates
      config:
        viz_kind: parallel_coordinates
        sample_col: sample
        group_col: group
        metric_cols: [total_reads, percent_duplicates, percent_gc, percent_aligned]
    ```

### :material-card-account-details-outline: Record card { #record-card }

<span class="ver-badge">v1.13.0+</span> `viz_kind: record_card`

One row of a collection as labelled fields and links, following a selection made in another tile.

![Record card](../images/guides/advanced-visualizations/record_card_light.webp#only-light){ data-title="Record card" .viz-shot loading=lazy }
![Record card](../images/guides/advanced-visualizations/record_card_dark.webp#only-dark){ data-title="Record card" .viz-shot loading=lazy }

**Input:** one row per record.

| feature_id | gene_symbol <small>optional</small> | biotype | chromosome | start | end |
|---|---|---|---|---|---|
| ENSG00000141510 | TP53 | protein_coding | 17 | 7661779 | 7687538 |
| ENSG00000146648 | EGFR | protein_coding | 7 | 55019017 | 55211628 |
| ENSG00000251562 | MALAT1 | lncRNA | 11 | 65497688 | 65506516 |

Every other column is a field; `sections` groups them, `link_templates` turns one into a link.

**Compatible inputs:** Any table with an identifier column.

**Controls**

- Primary: Record picker (when a selection holds several records)
- Cosmetic: Fields per card

??? example "YAML"
    ```yaml
    - tag: viz-record-card
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: gene_summary
      viz_kind: record_card
      config:
        viz_kind: record_card
        id_col: feature_id
        title_col: gene_symbol
        linked_component: viz-scatter-xy
        sections:
          Identity: [gene_symbol, biotype]
          Location: [chromosome, start, end]
        link_templates:
          feature_id: "https://www.ensembl.org/id/{value}"
    ```

---

## Benchmarking { #benchmarking }

### :material-target: PR benchmark { #pr-benchmark }

<span class="ver-badge">v1.10.0+</span> `viz_kind: pr_benchmark`

Each callset at its precision and recall, with F1 contours. The `roc` view sweeps a threshold into curves.

![PR benchmark](../images/guides/advanced-visualizations/pr_benchmark_light.webp#only-light){ data-title="PR benchmark" .viz-shot loading=lazy }
![PR benchmark](../images/guides/advanced-visualizations/pr_benchmark_dark.webp#only-dark){ data-title="PR benchmark" .viz-shot loading=lazy }

**Input:** one row per callset.

| tool | recall | precision | f1 | tp <small>optional</small> |
|---|---|---|---|---|
| DeepVariant | 0.9962 | 0.9978 | 0.9970 | 3891204 |
| GATK HaplotypeCaller | 0.9917 | 0.9941 | 0.9929 | 3873552 |
| Strelka2 | 0.9893 | 0.9952 | 0.9922 | 3864180 |

Also optional: `category_col`. The `roc` and `both` views need one row per callset and threshold, bound with `threshold_col` (and `fpr_col`, `group_col`).

**Compatible inputs:** hap.py or RTG vcfeval summaries (nf-core/variantbenchmarking, sarek).

**Controls**

- Primary: View (PR, ROC, both), Size, Colour scale
- Cosmetic: F1 iso-contours, y = x diagonal, fixed 0-1 axes, marker size, colour bar, point labels; curves: legend, markers, shade area, show AUC

??? example "YAML"
    ```yaml
    - tag: viz-pr-benchmark
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: benchmark_summary
      viz_kind: pr_benchmark
      config:
        viz_kind: pr_benchmark
        label_col: tool
        recall_col: recall
        precision_col: precision
        f1_col: f1
        support_col: tp
    ```

### :material-table-large: Confusion matrix { #confusion-matrix }

<span class="ver-badge">v1.10.0+</span> `viz_kind: confusion_matrix`

True positives, false positives and false negatives per callset as a heatmap.

![Confusion matrix](../images/guides/advanced-visualizations/confusion_matrix_light.webp#only-light){ data-title="Confusion matrix" .viz-shot loading=lazy }
![Confusion matrix](../images/guides/advanced-visualizations/confusion_matrix_dark.webp#only-dark){ data-title="Confusion matrix" .viz-shot loading=lazy }

**Input:** one row per callset.

| tool | tp | fp | fn |
|---|---|---|---|
| DeepVariant | 3891204 | 8592 | 14810 |
| GATK HaplotypeCaller | 3873552 | 22931 | 32462 |
| Strelka2 | 3864180 | 18630 | 41834 |

Also optional: `tn_col`.

**Compatible inputs:** Benchmark counts as nf-core/variantbenchmarking reports them.

**Controls**

- Primary: Normalise
- Cosmetic: Colour scale, colour bar, show fractions, font size

??? example "YAML"
    ```yaml
    - tag: viz-confusion-matrix
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: benchmark_summary
      viz_kind: confusion_matrix
      config:
        viz_kind: confusion_matrix
        label_col: tool
        tp_col: tp
        fp_col: fp
        fn_col: fn
    ```

### :material-chart-gantt: Metric with CI { #metric-ci-bars }

<span class="ver-badge">v1.10.0+</span> `viz_kind: metric_ci_bars`

One metric per callset with its 95% confidence interval, as a forest plot.

![Metric with CI](../images/guides/advanced-visualizations/metric_ci_bars_light.webp#only-light){ data-title="Metric with CI" .viz-shot loading=lazy }
![Metric with CI](../images/guides/advanced-visualizations/metric_ci_bars_dark.webp#only-dark){ data-title="Metric with CI" .viz-shot loading=lazy }

**Input:** one row per callset.

| tool | precision | precision_lower | precision_upper |
|---|---|---|---|
| DeepVariant | 0.9978 | 0.9976 | 0.9980 |
| GATK HaplotypeCaller | 0.9941 | 0.9938 | 0.9944 |
| Strelka2 | 0.9952 | 0.9949 | 0.9955 |

**Compatible inputs:** Precision or recall intervals from hap.py, som.py or vcfeval counts (nf-core/variantbenchmarking).

**Controls**

- Primary: Sort by value
- Cosmetic: Value labels, colour scale, point size

??? example "YAML"
    ```yaml
    - tag: viz-metric-ci-bars
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: benchmark_summary
      viz_kind: metric_ci_bars
      config:
        viz_kind: metric_ci_bars
        label_col: tool
        value_col: precision
        lower_col: precision_lower
        upper_col: precision_upper
        metric_name: Precision
    ```

---

## Proteins { #proteins }

Structure prediction, protein annotation and protein family runs publish a model, the
alignment behind it and per-residue facts. Eight kinds draw them and stay
[linked by residue](#residue-selection). The nf-core
[proteinfold](../pipeline-templates/nf-core/proteinfold.md),
[proteinannotator](../pipeline-templates/nf-core/proteinannotator.md) and
[proteinfamilies](../pipeline-templates/nf-core/proteinfamilies.md) templates are built on them.

### :material-molecule: 3D structure { #molecule-3d }

<span class="ver-badge">v1.19.0+</span> `viz_kind: molecule_3d`

The model in [3Dmol.js](https://3dmol.csb.pitt.edu/){ target="_blank" }, coloured by confidence, chain or a value, variants as spheres. A click picks a residue, shift-click a range.

![3D structure](../images/guides/advanced-visualizations/molecule_3d_light.webp#only-light){ data-title="3D structure" .viz-shot loading=lazy }
![3D structure](../images/guides/advanced-visualizations/molecule_3d_dark.webp#only-dark){ data-title="3D structure" .viz-shot loading=lazy }

**Input:** one PDB or mmCIF file per protein (`structure_dc_tag`, pLDDT in the B-factor column), plus a residue table, one row per residue.

| entity | position |
|---|---|
| P04637 | 175 |
| P04637 | 176 |
| P00533 | 858 |

Also optional: `chain_col`, `value_col`, `category_col`, `ref_aa_col`, `alt_aa_col`, `label_col`; `uniprot_col`, `gene_col` or `sequence_col` with `structure_source: resolve`, which needs no file. See [The data](#the-data).

**Compatible inputs:** AlphaFold, ColabFold or ESMFold PDB / mmCIF (nf-core/proteinfold), or a model from AlphaFold DB.

**Controls**

- Primary: Protein, Colour by, Style, Layout (structure alone, with sequence, alignment or text)
- Cosmetic: Colour scale, variants, labels, follow selection, spin

??? example "YAML"
    ```yaml
    - tag: viz-molecule-3d
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: residues
      viz_kind: molecule_3d
      config:
        viz_kind: molecule_3d
        structure_dc_tag: structures
        entity_col: entity
        position_col: position
        color_mode: plddt
        layout: structure_sequence
        selection_enabled: true
    ```

### :material-text-box-outline: Alignment { #msa }

<span class="ver-badge">v1.19.0+</span> `viz_kind: msa`

A multiple sequence alignment with consensus and conservation rows. A row click selects a sequence, a column brush picks residues.

![Alignment](../images/guides/advanced-visualizations/msa_light.webp#only-light){ data-title="Alignment" .viz-shot loading=lazy }
![Alignment](../images/guides/advanced-visualizations/msa_dark.webp#only-dark){ data-title="Alignment" .viz-shot loading=lazy }

**Input:** one row per aligned sequence; rows of one `msa_id` have the same length.

| msa_id | seq_id | aligned_sequence | rank <small>optional</small> |
|---|---|---|---|
| P04637 | query | MEEPQSDPSVEPPLSQETFSDLWKLL | 0 |
| P04637 | UniRef90_P02340 | MEEPQSDLSVEPPLSQETFS-LWKLL | 1 |
| P04637 | UniRef90_Q29537 | MEESQSDISLELPLSQETFS-LWKLL | 2 |

Rank 0 is the query. Also optional: `identity_col`.

**Compatible inputs:** proteinfold MSAs, A3M, Stockholm or aligned FASTA.

**Controls**

- Primary: Alignment, Colour scheme, Sort rows
- Cosmetic: Column width, consensus row, conservation bars, max rows

??? example "YAML"
    ```yaml
    - tag: viz-msa
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: alignments
      viz_kind: msa
      config:
        viz_kind: msa
        msa_id_col: msa_id
        seq_id_col: seq_id
        sequence_col: aligned_sequence
        rank_col: rank
        selection_enabled: true
    ```

### :material-format-letter-matches: Sequence track { #sequence-track }

<span class="ver-badge">v1.19.0+</span> `viz_kind: sequence_track`

The sequence on a ruler with a value lane, secondary structure, domains and variants. One strip per chain on a complex.

![Sequence track](../images/guides/advanced-visualizations/sequence_track_light.webp#only-light){ data-title="Sequence track" .viz-shot loading=lazy }
![Sequence track](../images/guides/advanced-visualizations/sequence_track_dark.webp#only-dark){ data-title="Sequence track" .viz-shot loading=lazy }

**Input:** a residue table, one row per residue.

| entity | position | residue | plddt <small>optional</small> |
|---|---|---|---|
| P04637 | 1 | M | 41.2 |
| P04637 | 2 | E | 45.8 |
| P04637 | 3 | E | 52.3 |

Also optional: `category_col`; a domains table (`domains_dc_tag`: `start`, `end`, `label`) and a variants table (`variants_dc_tag`: `position`, `label`, `category`), as in [The data](#the-data).

**Compatible inputs:** Per-residue tables built from a structure (pLDDT), S4PRED or domain hits.

**Controls**

- Primary: Entity, Chain
- Cosmetic: Residue width, letters, value colours

??? example "YAML"
    ```yaml
    - tag: viz-sequence-track
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: residues
      viz_kind: sequence_track
      config:
        viz_kind: sequence_track
        entity_col: entity
        position_col: position
        residue_col: residue
        value_col: plddt
        value_label: pLDDT
        domains_dc_tag: domains
        selection_enabled: true
    ```

### :material-format-letter-case: HMM logo { #hmm-logo }

<span class="ver-badge">v1.19.0+</span> `viz_kind: hmm_logo`

The logo of a profile HMM with insert and occupancy lanes, and where `hmmsearch` hits land on it. `profile_source: msa` computes it from an alignment instead.

![HMM logo](../images/guides/advanced-visualizations/hmm_logo_light.webp#only-light){ data-title="HMM logo" .viz-shot loading=lazy }
![HMM logo](../images/guides/advanced-visualizations/hmm_logo_dark.webp#only-dark){ data-title="HMM logo" .viz-shot loading=lazy }

**Input:** one row per match state and letter (long format).

| hmm_name <small>optional</small> | hmm_position | hmm_letter | emission |
|---|---|---|---|
| Pkinase | 1 | A | 0.031 |
| Pkinase | 1 | C | 0.012 |
| Pkinase | 2 | A | 0.064 |

Also optional, read when present: `entity`, `position`, `insert_prob`, `insert_length`, `occupancy`, `consensus`, `rf`, `cs`. The hits (`hits_dc_tag`) are a [domain hit table](#domain-architecture) with `hmm_from` and `hmm_to`. `profile_source: msa` reads an [alignment table](#msa) instead.

**Compatible inputs:** HMMER `hmmbuild` profiles and `hmmsearch` domain tables (`hits_dc_tag`), nf-core/proteinfamilies.

**Controls**

- Primary: Heights, Colour scheme
- Cosmetic: State width, consensus and insert rows, shown tracks, state window, fold below (bits), hits E-value, max hits

??? example "YAML"
    ```yaml
    - tag: viz-hmm-logo
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: hmm_profile
      viz_kind: hmm_logo
      config:
        viz_kind: hmm_logo
        state_col: hmm_position
        letter_col: hmm_letter
        emission_col: emission
        model_col: hmm_name
        hits_dc_tag: domain_hits
    ```

### :material-view-sequential-outline: Domain architecture { #domain-architecture }

<span class="ver-badge">v1.19.0+</span> `viz_kind: domain_architecture`

The domains of many proteins, one row each, or grouped by architecture. A partial match has a zigzag edge.

![Domain architecture](../images/guides/advanced-visualizations/domain_architecture_light.webp#only-light){ data-title="Domain architecture" .viz-shot loading=lazy }
![Domain architecture](../images/guides/advanced-visualizations/domain_architecture_dark.webp#only-dark){ data-title="Domain architecture" .viz-shot loading=lazy }

**Input:** one row per domain hit.

| entity | start | end | label | protein_length <small>optional</small> |
|---|---|---|---|---|
| P00533 | 57 | 167 | Recep_L_domain | 1210 |
| P00533 | 712 | 968 | Pkinase_Tyr | 1210 |
| P04637 | 95 | 288 | P53 | 393 |

Also optional, read when present: `hmm_from`, `hmm_to`, `hmm_length`, `hmm_coverage`, `i_evalue`, `source`, `description`, `accession`.

**Compatible inputs:** InterProScan or `hmmsearch` domain hits (nf-core/proteinannotator, proteinfamilies).

**Controls**

- Primary: View (Proteins, Architectures), Colour by
- Cosmetic: Sources, scale, residue width, architectures, max proteins

??? example "YAML"
    ```yaml
    - tag: viz-domain-architecture
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: domain_hits
      viz_kind: domain_architecture
      config:
        viz_kind: domain_architecture
        entity_col: entity
        start_col: start
        end_col: end
        label_col: label
        protein_length_col: protein_length
        view: proteins
    ```

### :material-cosine-wave: Secondary structure { #secondary-structure }

<span class="ver-badge">v1.19.0+</span> `viz_kind: secondary_structure`

Helices, strands and coil as a ribbon, with the probabilities behind the call and the agreement between sources.

![Secondary structure](../images/guides/advanced-visualizations/secondary_structure_light.webp#only-light){ data-title="Secondary structure" .viz-shot loading=lazy }
![Secondary structure](../images/guides/advanced-visualizations/secondary_structure_dark.webp#only-dark){ data-title="Secondary structure" .viz-shot loading=lazy }

**Input:** one row per residue, and per source when several are compared.

| entity <small>optional</small> | position | ss_code | p_helix <small>optional</small> | p_strand <small>optional</small> | p_coil <small>optional</small> |
|---|---|---|---|---|---|
| P04637 | 110 | C | 0.08 | 0.21 | 0.71 |
| P04637 | 111 | E | 0.04 | 0.83 | 0.13 |
| P04637 | 112 | E | 0.03 | 0.88 | 0.09 |

`ss_code` is a DSSP or S4PRED code (H, E, C). Also optional: `source_col` (`ss_source` above, one ribbon per source), `residue_col`, `confidence_col`.

**Compatible inputs:** S4PRED `.ss2` predictions.

**Controls**

- Primary: Entity, Reference
- Cosmetic: Residue width, ribbon height, letters, confidence shading, coil segments, min segment, colours

??? example "YAML"
    ```yaml
    - tag: viz-secondary-structure
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: ss_calls
      viz_kind: secondary_structure
      config:
        viz_kind: secondary_structure
        entity_col: entity
        position_col: position
        state_col: ss_code
        source_col: ss_source
        reference_source: S4PRED
        p_helix_col: p_helix
        p_strand_col: p_strand
        p_coil_col: p_coil
    ```

### :material-grid: Predicted aligned error { #pae-matrix }

<span class="ver-badge">v1.19.0+</span> `viz_kind: pae_matrix`

A model's PAE matrix with pLDDT strips. A low-error block on the diagonal is a confident domain. A brush picks the scored range.

![Predicted aligned error](../images/guides/advanced-visualizations/pae_matrix_light.webp#only-light){ data-title="Predicted aligned error" .viz-shot loading=lazy }
![Predicted aligned error](../images/guides/advanced-visualizations/pae_matrix_dark.webp#only-dark){ data-title="Predicted aligned error" .viz-shot loading=lazy }

**Input:** one PAE file per protein (a `pae` file collection, `pae_dc_tag`), plus a residue table, one row per residue.

| entity <small>optional</small> | position | plddt <small>optional</small> |
|---|---|---|
| P04637 | 1 | 41.2 |
| P04637 | 2 | 45.8 |
| P04637 | 3 | 52.3 |

Also optional: `chain_col`. See [The data](#the-data).

**Compatible inputs:** proteinfold PAE TSV, AlphaFold DB or ColabFold JSON.

**Controls**

- Primary: Entity, Colours
- Cosmetic: pLDDT strips, brush (diagonal, rectangle)

??? example "YAML"
    ```yaml
    - tag: viz-pae-matrix
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: residues
      viz_kind: pae_matrix
      config:
        viz_kind: pae_matrix
        pae_dc_tag: pae_files
        entity_col: entity
        position_col: position
        value_col: plddt
    ```

### :material-scatter-plot-outline: Ramachandran { #ramachandran }

<span class="ver-badge">v1.19.0+</span> `viz_kind: ramachandran`

Backbone phi and psi of the model, computed in the browser from the 3D tile's file. The favoured regions are a guide, not MolProbity contours.

![Ramachandran](../images/guides/advanced-visualizations/ramachandran_light.webp#only-light){ data-title="Ramachandran" .viz-shot loading=lazy }
![Ramachandran](../images/guides/advanced-visualizations/ramachandran_dark.webp#only-dark){ data-title="Ramachandran" .viz-shot loading=lazy }

**Input:** the structure file of the [3D structure](#molecule-3d) tile, plus a residue table, one row per residue.

| entity <small>optional</small> | position |
|---|---|
| P04637 | 175 |
| P04637 | 176 |
| P00533 | 858 |

Also optional: `chain_col`, `value_col`, `category_col`; `uniprot_col`, `gene_col` or `sequence_col` with `structure_source: resolve`.

**Compatible inputs:** The structure file the 3D tile reads.

**Controls**

- Primary: Protein, Colour by, Residue classes
- Cosmetic: Approximate favoured regions, marker size, follow selection

??? example "YAML"
    ```yaml
    - tag: viz-ramachandran
      component_type: advanced_viz
      workflow_tag: my_workflow
      data_collection_tag: residues
      viz_kind: ramachandran
      config:
        viz_kind: ramachandran
        structure_dc_tag: structures
        entity_col: entity
        position_col: position
        color_mode: plddt
    ```

### The data { #the-data }

Every protein tile reads tables joined on two column names: `entity` (which protein) and
`position` (the 1-based residue number in the structure's numbering). A tile shows one entity
at a time: the one the filters name, else the reader's pick, else the first.

| Input | Shape |
|-------|-------|
| Structure files | `indexed_file` collection, `format: pdb` or `mmcif`, one file per entity, the sample id equal to the `entity` value. Predictors write pLDDT in the B-factor column |
| Residue table | `entity`, `position`, optionally `chain`, `residue`, `value`, `category` |
| Variants | `entity`, `position`, `ref_aa`, `alt_aa`, a consequence and a label |
| Domains | `entity`, `start`, `end`, `label`, optionally `source` |
| Alignment | `msa_id` (the `entity` it aligns), `seq_id`, `rank` (0 is the query), `aligned_sequence` |
| PAE files | `indexed_file` collection, `format: pae`: proteinfold TSV, AlphaFold DB or ColabFold JSON |

The helpers in `depictio/recipes/lib/` (`protein_structure`, `msa`, `hmm`,
`secondary_structure`, `pae`) build these tables. See [Recipes](../usage/projects/recipes.md).

### Linked by residue { #residue-selection }

![Protein tiles linked by residue: a click or brush becomes a filter on entity and position that narrows every table, a hover is only published in the browser; the model comes from a file of the run or from the resolver](../images/guides/protein-tiles/schema_residue_linking.svg){ .viz-shot loading=lazy }

- **A pick is a filter.** A click or brush emits a `residue_selection`: the entity, a
  `position` range and, on a complex, the chain. Every table with those columns narrows, and
  every protein tile shows the range. The last gesture wins.
- **A hover is not.** Pointing at a residue marks it in every protein tile, in the browser only.
- A [lollipop](#lollipop) joins with `selection_enabled: true`, a [profile](#profile) with
  `residue_axis: true`. Cards and figures that do not draw the position column ignore the range.

### Where the structure comes from { #structure-resolver }

`structure_source: file` reads the run's own files and makes no outbound call.
`structure_source: resolve` asks the server for a model by UniProt accession, by gene and
taxon, or by sequence. The resolver is off until `DEPICTIO_STRUCTURE_RESOLVER_ENABLED=true`,
and tries, first hit wins:

1. its cache in the instance bucket;
2. AlphaFold DB, by accession;
3. UniProt, gene and taxon to an accession, then AlphaFold DB;
4. ESMFold, for a sequence of at most 400 residues.

The tile credits the service it used. A `pae_matrix` has no resolver path. See
[External structure services](security.md#structure-resolver) for what leaves the server and
the [environment reference](../installation/env-reference.md#structure-resolver) for the settings.

### Numbering mismatch { #numbering-mismatch }

A variant table and a model do not always number residues alike (a construct, an isoform, an
off-by-one). A variant whose `ref_aa` disagrees with the model is listed under a *numbering
mismatch* badge instead of being drawn on the wrong residue; one past the end of the model is
counted under *outside the model*.
