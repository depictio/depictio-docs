# Advanced Visualizations — screenshots

Each advanced-viz subsection in [`docs/features/components.md`](../../../features/components.md#advanced-visualizations) references **two** WebP files per viz: `<viz>_light.webp#only-light` and `<viz>_dark.webp#only-dark`. The `#only-light` / `#only-dark` URL fragments are a mkdocs-material feature that swaps the image based on the active theme.

## File set (68 total)

| Viz | Filenames |
|---|---|
| Volcano | `volcano_{light,dark}.webp` |
| Volcano, MA view | `ma_{light,dark}.webp` |
| Volcano, QQ view | `qq_{light,dark}.webp` |
| DA barplot | `da_barplot_{light,dark}.webp` |
| Dot plot | `dot_plot_{light,dark}.webp` |
| Dot plot, enrichment view | `enrichment_{light,dark}.webp` |
| Manhattan | `manhattan_{light,dark}.webp` |
| Lollipop | `lollipop_{light,dark}.webp` |
| Coverage track | `coverage_track_{light,dark}.webp` |
| Stacked taxonomy | `stacked_taxonomy_{light,dark}.webp` |
| Sunburst | `sunburst_{light,dark}.webp` |
| Rarefaction | `rarefaction_{light,dark}.webp` |
| Phylogenetic | `phylogenetic_{light,dark}.webp` |
| Embedding | `embedding_{light,dark}.webp` |
| ComplexHeatmap | `complex_heatmap_{light,dark}.webp` |
| UpSet | `upset_plot_{light,dark}.webp` |
| Sankey | `sankey_{light,dark}.webp` |
| Oncoplot | `oncoplot_{light,dark}.webp` |
| Contact map (v1.13.0) | `contact_map_{light,dark}.webp` |
| Knee plot (v1.13.0) | `knee_plot_{light,dark}.webp` |
| Damage profile (v1.13.0) | `damage_profile_{light,dark}.webp` |
| Genome view (v1.13.0) | `genome_view_{light,dark}.webp` |
| Group compare (v1.13.0) | `group_compare_{light,dark}.webp` |
| Transcript structure (v1.13.0) | `transcript_structure_{light,dark}.webp` |
| Copy-number profile (v1.13.0) | `cnv_profile_{light,dark}.webp` |
| Genome chord (v1.13.0) | `genome_chord_{light,dark}.webp` |
| Parallel coordinates (v1.13.0) | `parallel_coordinates_{light,dark}.webp` |
| Record card (v1.13.0) | `record_card_{light,dark}.webp` |

### Controls placement (v1.13.0)

The volcano tile with `controls_placement` set to each value, referenced from [Shared settings](../../../features/components.md#advanced-viz-shared-settings): `controls_popover_{light,dark}.webp` (popover open), `controls_rail_{light,dark}.webp`, `controls_header_{light,dark}.webp`.

### Phylogeny interaction (v1.8.0)

Three extra pairs referenced from [Reading and navigating the tree](../../../features/components.md#phylogeny-interaction), same `#only-light` / `#only-dark` convention:

| State | Filenames |
|---|---|
| A clade selected, rest of the tree dimmed | `phylogeny_selection_{light,dark}.webp` |
| Filter to subtree active, shown in the filter panel | `phylogeny_filter_{light,dark}.webp` |
| A collapsed clade drawn as a wedge | `phylogeny_collapsed_{light,dark}.webp` |

## How to regenerate

Recaptured for v1.13.0 from the `advanced_viz_showcase` dashboards (ids `646b0f3c1e4a2d7f8e5b8…`), served by a throwaway `depictio local up` instance of the release with its own `HOME`, so no real instance or token is involved. The local stack seeds only the bundled examples, so the showcase project has to be added to its seed list for the capture.

A Playwright script then, for each viz, in light and dark (`theme-store` in localStorage):

1. opens `/dashboard/<id>?no-walkthrough=1`, hides the tab sidebar and the filter panel;
2. injects `.hoverlayer, .modebar-container, .mantine-Notifications-root {display:none!important}` so neither a stale hover label nor the Plotly toolbar lands in the shot;
3. picks the view (MA, QQ, CNV *Profile*) and the controls placement where needed, and opens the settings popover (`aria-label="Viz settings"`, clicked from script because the placement picker overlaps it) for the kinds whose cosmetic settings are worth showing;
4. clips the tile (plus the open popover) with 10 px of padding, at a 1440 px viewport (2000 px for half-width tiles);
5. converts each PNG with `cwebp -q 82 -m 6`.

The three phylogeny interaction pairs are driven the same way: the script reads the internal nodes from the Plotly figure, clicks one holding 4–6 tips, then **Filter** (with the filter panel left open) or **Collapse**.
