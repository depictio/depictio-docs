# CLI command reference

`docs/depictio-cli/usage.md` is generated from the depictio CLI itself, in two steps, so the docs build never imports depictio.

| File | Role |
| --- | --- |
| `dump.py` | Runs where depictio is installed. Walks the Typer/Click command tree and writes `docs/depictio-cli/cli-reference.json`: every command and option, hidden ones marked. |
| `render.py` | Standard library only. Turns the JSON into `usage.md`; the same JSON always gives the same bytes. Holds what `--help` cannot say: icons, colours, guide links, and the anchors other pages link to (`ANCHOR_ALIASES`). |
| `docs/depictio-cli/_notes/*.md` | Hand-written sections the page includes (servers, refreshing a project, exit codes, watcher services). Edit them freely; links are relative to `usage.md`. |
| `docs/stylesheets/cli.css` | The page's look. |

Both scripts exit non-zero when the result looks wrong (too few commands or options, a command without a section, an alias anchor with no target).

## Automatically, on each release

`.github/workflows/update-on-release.yaml` runs `dump.py` inside the released `depictio-api` image, renders the page on the runner, and adds both files to the docs-update PR, next to the OpenAPI spec.

## By hand

```bash
# 1. Dump, in an environment with the new depictio installed
uv venv /tmp/cli && VIRTUAL_ENV=/tmp/cli uv pip install "git+https://github.com/depictio/depictio@v1.22.0"
/tmp/cli/bin/python scripts/cli-reference/dump.py

# 2. Render
python3 scripts/cli-reference/render.py
```

Never edit `usage.md` itself: the `check-cli-reference` pre-commit hook (`render.py --check`) fails when it differs from the render of the committed JSON. To change the wording of a command, change its `--help` in depictio; to change the layout, change `render.py` and render again.
