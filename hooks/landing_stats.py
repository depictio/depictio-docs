"""Fill the landing page's "Depictio in numbers" tiles from docs/data/landing_stats.json.

docs/index.md carries placeholders instead of numbers, so a release refreshes
the page by rerunning dev/landing_stats.py and nothing else:

- {{ stats.KEY }}           a scalar from the JSON; integers get a thousands comma
- {{ stats.pipeline_marquee }} the nf-core template logos, three rows, each
                              linked to its page (dev/fetch_template_logos.py)
- {{ stats.tool_marquee }}     well-known catalog tools, three rows: the official
                              logo where dev/fetch_tool_logos.py found one,
                              else the name
- {{ stats.viz_marquee }}      a thumbnail of every advanced visualization, two
                              rows, read from the catalog of its page
- {{ stats.renders_bar }}    the stacked bar segments of renders by component
- {{ stats.renders_legend }} its legend

An unknown placeholder fails the build rather than shipping "{{ ... }}".
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from mkdocs.exceptions import PluginError

DATA = "data/landing_stats.json"
PAGE = "index.md"
_PLACEHOLDER = re.compile(r"\{\{\s*stats\.([a-z_]+)\s*\}\}")


def _fmt(value) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    return html.escape(str(value))


LOGOS = "images/landing/logos"


def _marquee(items: list[str], rows: int = 3, extra_class: str = "") -> str:
    """Rows scrolling in turn the opposite way. Each row prints its list twice
    so the loop has no seam; the copy is inert and hidden from screen readers."""
    size = -(-len(items) // rows)
    out = []
    for i in range(rows):
        ul = "".join(items[i * size:(i + 1) * size])
        if not ul:
            continue
        out.append(
            f'<div class="kpi-marquee-row{" kpi-marquee-reverse" if i % 2 else ""}">'
            f'<div class="kpi-marquee-track"><ul class="kpi-logos">{ul}</ul>'
            f'<ul class="kpi-logos" aria-hidden="true" inert>{ul}</ul></div></div>'
        )
    return f'<div class="kpi-marquee{extra_class}">{"".join(out)}</div>'


VIZ_PAGE = "features/advanced-visualizations.md"
_VIZ_TILE = re.compile(
    r"thumbs/([a-z0-9_]+)_light\.webp#only-light.*?\[([^\]]+)\]\(#([a-z0-9-]+)\)\{ \.viz-tile__name", re.S
)


def _viz_items(docs_dir: Path) -> list[str]:
    """One thumbnail per tile of the advanced visualizations catalog, in its order."""
    text = (docs_dir / VIZ_PAGE).read_text()
    items = []
    for kind, name, anchor in _VIZ_TILE.findall(text):
        imgs = "".join(
            f'<img class="kpi-viz-{theme}" src="images/guides/advanced-visualizations/thumbs/{kind}_{theme}.webp" '
            f'alt="" width="112" height="84" loading="lazy" decoding="async">'
            for theme in ("light", "dark")
        )
        items.append(
            f'<li><a href="features/advanced-visualizations/#{anchor}" title="{html.escape(name)}">{imgs}</a></li>'
        )
    if not items:
        raise PluginError(f"landing_stats: no catalog tiles found in {VIZ_PAGE}")
    return items


def _img(src: str, alt: str, size: dict, cls: str = "") -> str:
    # The files are 2x; print the CSS size so the row never shifts.
    w, h = round(size["width"] / 2), round(size["height"] / 2)
    klass = f' class="{cls}"' if cls else ""
    return (
        f'<img{klass} src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}" '
        f'loading="lazy" decoding="async">'
    )


def _fragments(stats: dict, docs_dir: Path) -> dict[str, str]:
    sizes = json.loads((docs_dir / LOGOS / "templates" / "sizes.json").read_text())
    pipelines = []
    for name in stats["pipelines"]:
        if name not in sizes:
            raise PluginError(f"landing_stats: no logo for {name}; rerun dev/fetch_template_logos.py")
        imgs = "".join(
            _img(f"{LOGOS}/templates/{name}_{theme}.webp", f"nf-core/{name}" if theme == "light" else "",
                 sizes[name], f"kpi-logo-{theme}")
            for theme in ("light", "dark")
        )
        pipelines.append(
            f'<li><a href="pipeline-templates/nf-core/{name}/" title="nf-core/{name}">{imgs}</a></li>'
        )
    tool_logos = json.loads((docs_dir / LOGOS / "tools" / "sources.json").read_text())
    tools = []
    for name in stats["tool_chips"]:
        logo = tool_logos.get(name)
        if logo is None:
            tools.append(f'<li class="kpi-tool">{html.escape(name)}</li>')
            continue
        img = _img(f"{LOGOS}/tools/{logo['file']}", name, logo)
        label = "" if logo["wordmark"] else f"<span>{html.escape(name)}</span>"
        tools.append(f'<li class="kpi-tool kpi-tool-logo" title="{html.escape(name)}">{img}{label}</li>')
    total = stats["renders"]
    bar, legend = [], []
    for part in stats["renders_by_component"]:
        share = 100 * part["count"] / total
        title = f'{part["label"]}: {part["count"]:,}'
        bar.append(
            f'<span class="kpi-seg kpi-seg-{part["id"]}" style="width:{share:.2f}%" '
            f'title="{title}"></span>'
        )
        legend.append(
            f'<li><span class="kpi-dot kpi-seg-{part["id"]}"></span>'
            f'<span class="kpi-legend-name">{html.escape(part["label"])}</span> <b>{part["count"]:,}</b></li>'
        )
    return {
        "pipeline_marquee": _marquee(pipelines),
        "tool_marquee": _marquee(tools),
        "viz_marquee": _marquee(_viz_items(docs_dir), rows=2, extra_class=" kpi-marquee-viz"),
        "renders_bar": "".join(bar),
        "renders_legend": "".join(legend),
    }


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    if page.file.src_uri != PAGE or "{{" not in markdown:
        return markdown
    docs_dir = Path(config["docs_dir"])
    stats = json.loads((docs_dir / DATA).read_text())
    fragments = _fragments(stats, docs_dir)

    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key in fragments:
            return fragments[key]
        if key in stats and not isinstance(stats[key], (list, dict)):
            return _fmt(stats[key])
        raise PluginError(f"landing_stats: unknown placeholder stats.{key} in {PAGE}")

    return _PLACEHOLDER.sub(replace, markdown)
