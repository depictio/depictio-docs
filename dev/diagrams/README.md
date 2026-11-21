# Hand-drawn figures

The figures on the [Data Model](../../docs/features/data-model.md) and
[Features](../../docs/features/README.md) pages are generated, not drawn.
Regenerate them with:

```bash
uv sync --group diagrams           # once, pulls playwright
uv run playwright install chromium # once
cd dev/diagrams && uv run python data_model.py && uv run python architecture.py
uv run python nextflow_trigger.py
uv run python protein_tiles.py
uv run python migration.py
uv run python project_lifecycle.py
uv run python security.py
uv run python workshop.py
```

Each script writes `<name>_light` and `<name>_dark`, as both SVG and PNG, into
`docs/images/`. Pages embed the **PNG** with mkdocs-material's
`#only-light` / `#only-dark` fragments. An `<img>`-embedded SVG is an isolated
document that cannot see the page's `@font-face`, so Virgil would fall back to a
cursive substitute and the fixed text coordinates would overflow their boxes.
The SVG is committed as the reviewable artefact: it is what shows a real diff
when a figure changes.

## Why generated

A hand-made PNG goes stale silently. These describe things that move (which
objects are embedded, where a Delta table lives), so they are written as code,
reviewed as a diff, and corrected in the same commit as the thing they describe.

The jitter that gives the strokes their wobble comes from a fixed seed, so
re-running without editing a script leaves the working tree clean. If `git
status` is dirty after a regeneration, something in the figure actually changed.

## Files

| File | What |
| --- | --- |
| `sketch.py` | The toolkit: jittered strokes, boxes, arrows, the light and dark palettes, and the PNG pass. |
| `mdi_icons.py` | The icon paths the figures draw: mdi (Apache 2.0) and the formkit, bx and octicon icons (MIT) the app uses for component types. |
| `data_model.py` | Data Model: the two project shapes, config to data, join vs link. |
| `architecture.py` | The system architecture (Features overview and Architecture), the Celery task round trip, and live updates (Architecture and the Real-time events guide). |
| `security.py` | Signing in and every request, how a role is resolved, and what a code figure goes through, on the Security page. |
| `brand.py` | The app's brand colours as fill keys, and the card helpers `architecture.py` and `security.py` share. |
| `nextflow_trigger.py` | The trigger flow on the Nextflow trigger page. |
| `migration.py` | The three ways to move a project, on the Project Migration page. |
| `project_lifecycle.py` | A project's life, from its data to shared dashboards and every new run, on the Projects overview. |
| `protein_tiles.py` | Linking by residue and the structure resolver, the two figures on the Protein tiles page. |
| `concepts.py` | The app's colours and icons per concept (project, data collection, link...) and the drawing helpers built on them, shared with the workshop figures. |
| `cross_dc_filtering.py` | A filter travelling along two ampliseq links, on the Cross-DC Filtering page. |
| `component_types.py` | The app's colour and icon per component type (figure, card, interactive, table, MultiQC...), shared by the dashboard figures. |
| `dashboard_layout.py` | The three panels of a dashboard, on the iris demo's Petal tab, on the Dashboards page. |
| `components_figures.py` | A card's three stat-list layouts and a filter reaching a table and MultiQC through links, on the Components page. |
| `filter_expressions.py` | Where `filter_expr` narrows the rows of a card and of an interactive, on the Filter Expressions page. |
| `selection_filtering.py` | Three tiles writing to the dashboard's filter list and every tile reading it, on the Interactive Selection Filtering page. |
| `auth_modes.py` | What a visitor gets in each authentication mode, on the Authentication Modes page. |
| `workshop.py` | The concept figures of the hands-on workshop, also on Cross-DC filtering and Runs. |

`sketch.py` is a port of the generator in the main
[depictio](https://github.com/depictio/depictio) repository, which produces the
schema figures attached to pull requests there. It is duplicated rather than
shared because the docs shouldn't depend on an unmerged branch of another repo;
if you fix a drawing bug here, it is worth carrying over.

## Adding a figure

Write a `build(theme) -> Sketch` function and hand it to `write_themed`. Name
fills semantically (`"blue"`, `"orange"`, `"grey"`) rather than by hex. The
theme resolves them, which is what lets one function render both palettes.

```python
def my_figure(theme: Theme) -> Sketch:
    s = Sketch(1080, 600, theme=theme)
    s.heading(46, 52, "Title", "subtitle")
    s.box(Box(70, 140, 250, 110, "blue", "Thing", ("a detail",)))
    return s

write_themed(my_figure, OUT, "my-figure")
```

Two things Virgil does not draw well: braces (`{}`) come out as ornaments, and
long strings of punctuation get noisy. Spell paths out in prose instead.
