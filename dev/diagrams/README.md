# Hand-drawn figures

The diagrams on the [Data Model](../../docs/features/data-model.md) page are generated,
not drawn. Regenerate them with:

```bash
uv sync --group diagrams          # once — pulls playwright
uv run playwright install chromium # once
cd dev/diagrams && uv run python data_model.py
```

Each script writes `<name>_light` and `<name>_dark`, as both SVG and PNG, into
`docs/images/data-model/`. Pages embed the **PNG** with mkdocs-material's
`#only-light` / `#only-dark` fragments — an `<img>`-embedded SVG is an isolated
document that cannot see the page's `@font-face`, so Virgil would fall back to a
cursive substitute and the fixed text coordinates would overflow their boxes.
The SVG is committed as the reviewable artefact: it is what shows a real diff
when a figure changes.

## Why generated

A hand-made PNG goes stale silently. These describe things that move — which
objects are embedded, where a Delta table lives — so they are written as code,
reviewed as a diff, and corrected in the same commit as the thing they describe.

The jitter that gives the strokes their wobble comes from a fixed seed, so
re-running without editing a script leaves the working tree clean. If `git
status` is dirty after a regeneration, something in the figure actually changed.

## Files

| File | What |
| --- | --- |
| `sketch.py` | The toolkit: jittered strokes, boxes, arrows, the light and dark palettes, and the PNG pass. |
| `data_model.py` | The two Data Model figures. |

`sketch.py` is a port of the generator in the main
[depictio](https://github.com/depictio/depictio) repository, which produces the
schema figures attached to pull requests there. It is duplicated rather than
shared because the docs shouldn't depend on an unmerged branch of another repo;
if you fix a drawing bug here, it is worth carrying over.

## Adding a figure

Write a `build(theme) -> Sketch` function and hand it to `write_themed`. Name
fills semantically (`"blue"`, `"orange"`, `"grey"`) rather than by hex — the
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
