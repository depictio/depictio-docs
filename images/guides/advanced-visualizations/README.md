# Advanced Visualizations — screenshots

Each advanced-viz subsection in [`docs/features/components.md`](../../../features/components.md#advanced-visualizations) references **two** WebP files per viz: `<viz>_light.webp#only-light` and `<viz>_dark.webp#only-dark`. The `#only-light` / `#only-dark` URL fragments are a mkdocs-material feature that swaps the image based on the active theme.

## File set (36 total)

| Viz | Filenames |
|---|---|
| Volcano | `volcano_{light,dark}.webp` |
| MA | `ma_{light,dark}.webp` |
| DA barplot | `da_barplot_{light,dark}.webp` |
| Enrichment | `enrichment_{light,dark}.webp` |
| Manhattan | `manhattan_{light,dark}.webp` |
| Lollipop | `lollipop_{light,dark}.webp` |
| Coverage track | `coverage_track_{light,dark}.webp` |
| Stacked taxonomy | `stacked_taxonomy_{light,dark}.webp` |
| Sunburst | `sunburst_{light,dark}.webp` |
| Rarefaction | `rarefaction_{light,dark}.webp` |
| Phylogenetic | `phylogenetic_{light,dark}.webp` |
| Dot plot | `dot_plot_{light,dark}.webp` |
| Embedding | `embedding_{light,dark}.webp` |
| ComplexHeatmap | `complex_heatmap_{light,dark}.webp` |
| QQ | `qq_{light,dark}.webp` |
| UpSet | `upset_plot_{light,dark}.webp` |
| Sankey | `sankey_{light,dark}.webp` |
| Oncoplot | `oncoplot_{light,dark}.webp` |

## How to regenerate

Captured automatically from the `advanced_viz_showcase` dashboards via the API endpoint `GET /depictio/api/v1/utils/screenshot-react-dual/{dashboard_id}?open_settings=true`.

Orchestration script (in the depictio repo at `/tmp/capture_react_screenshots.py` during development):

1. Loops over the 18 unique `viz_kind` dashboards
2. Triggers the endpoint for each (light + dark in a single Playwright session)
3. Converts the resulting PNGs to WebP (`cwebp -q 82 -m 6`) to keep this folder under ~2 MB

WebP rather than PNG because the dashboard chrome + Plotly canvases compress well — 4 MB of PNGs collapses to ~1.6 MB of WebP at visually identical quality.
