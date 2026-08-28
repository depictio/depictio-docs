# Advanced Visualizations — screenshots

Each advanced-viz subsection in [`docs/features/components.md`](../../../features/components.md#advanced-visualizations) references **two** WebP files per viz: `<viz>_light.webp#only-light` and `<viz>_dark.webp#only-dark`. The `#only-light` / `#only-dark` URL fragments are a mkdocs-material feature that swaps the image based on the active theme.

## File set (42 total)

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

### Phylogeny interaction (v1.8.0)

Three extra pairs referenced from [Reading and navigating the tree](../../../features/components.md#phylogeny-interaction), same `#only-light` / `#only-dark` convention:

| State | Filenames |
|---|---|
| A clade selected, rest of the tree dimmed | `phylogeny_selection_{light,dark}.webp` |
| Filter to subtree active, shown in the filter panel | `phylogeny_filter_{light,dark}.webp` |
| A collapsed clade drawn as a wedge | `phylogeny_collapsed_{light,dark}.webp` |

## How to regenerate

Captured automatically from the `advanced_viz_showcase` dashboards via the API endpoint `GET /depictio/api/v1/utils/screenshot-react-dual/{dashboard_id}?open_settings=true`.

Orchestration script (in the depictio repo at `/tmp/capture_react_screenshots.py` during development):

1. Loops over the 18 unique `viz_kind` dashboards
2. Triggers the endpoint for each (light + dark in a single Playwright session)
3. Converts the resulting PNGs to WebP (`cwebp -q 82 -m 6`) to keep this folder under ~2 MB

WebP rather than PNG because the dashboard chrome + Plotly canvases compress well — 4 MB of PNGs collapses to ~1.6 MB of WebP at visually identical quality.

## Captured by hand instead (v1.8.0)

`phylogenetic_{light,dark}.webp` and the three interaction pairs above were **not** produced by the
batch script. `GET /utils/screenshot-react-dual/...` times out after ~180s and returns a 500 against a
dev stack: the endpoint drives the SPA bundle FastAPI serves, and on a dev stack the viewer runs
separately under vite.

They were captured from the vite dev viewer instead, against the `advanced_viz_showcase` Phylogeny
dashboard (`646b0f3c1e4a2d7f8e5b8d18`), driving the UI to each state and taking the same shot in light
and dark, then `cwebp -q 82 -m 6` as usual. One wrinkle worth knowing: Plotly's hover label survives
moving the pointer off a node, so it lands in the shot. Inject
`.hoverlayer{display:none!important}` before capturing.
