"""Export the home page's live component examples with the component export API.

Each entry in PICKS is one dashboard component, named by its dashboard title
(and tab title) and its component id, so the same list works on any instance
that carries those dashboards. It is fetched as a self-contained page
(GET /export/dashboards/{id}/components/{cid}?format=html) in light and in
dark. Every export inlines the instance's JS and CSS bundle, so the bundle is
written once, as docs/images/landing/live/embed-<hash>.{js,css}, and each page
links to it: the browser downloads it once for all the examples. Exports from
one instance share one bundle.

An Image component's export still loads its pictures from the server
(/depictio/api/v1/files/serve/image?s3_path=...). Those are downloaded to
live/img/ as WebP and a small script in the page points the gallery at them.

    python dev/export_components.py                       # all picks
    python dev/export_components.py viz_volcano           # just these
    python dev/export_components.py linked                # the filtered example

Each pick names its instance, "main", "extra" or "trec", whose URLs come from
DEPICTIO_URL, DEPICTIO_EXTRA_URL and DEPICTIO_TREC_URL (all default to the
public showcases).
The instances need DEPICTIO_FASTAPI_EMBED_ENABLED=true. DEPICTIO_TOKEN is
sent as a bearer token when set (public dashboards need none).
"""

from __future__ import annotations

import hashlib
import io
import itertools
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

SHOWCASES = "https://showcases.depictio.embl.org"
INSTANCES = {
    "main": os.environ.get("DEPICTIO_URL", SHOWCASES).rstrip("/"),
    "extra": os.environ.get("DEPICTIO_EXTRA_URL", SHOWCASES).rstrip("/"),
    "trec": os.environ.get("DEPICTIO_TREC_URL", SHOWCASES).rstrip("/"),
}
TOKEN = os.environ.get("DEPICTIO_TOKEN")
OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "landing" / "live"
IMAGE_WIDTH = 900

AMPLISEQ = "nf-core/ampliseq"
VIRALRECON = "nf-core/viralrecon"
SAREK = "nf-core/sarek"
PENGUINS = "Penguins Species Analysis"
TREC = "TREC Advanced Mobile Lab 2024"
CELLPAINTING = "Cell Painting segmentation"

# name -> (instance, dashboard title, tab title or None for the main tab,
# component id[, dashboard id suffix]). A None component id picks the
# dashboard's Image component. The suffix pins one dashboard when several
# runs of a template share a title and the newest is not the one to show.
PICKS = {
    # Figure
    "fig_scatter": ("extra", PENGUINS, None, "a9c71416-ffe5-5c4d-b967-8470a1875a21"),
    "fig_box": ("extra", PENGUINS, None, "67990c25-0353-5b7e-adc1-24433c27e6cb"),
    "fig_stacked": ("main", AMPLISEQ, "Community & Diversity", "comm-composition-by-group"),
    "fig_grouped": ("main", SAREK, "Variant yield", "vy-spectrum-sbs", "180782"),
    "fig_annotated": ("main", "nf-core/atacseq", "ATAC quality", "aq-ladder"),
    "fig_subplots": ("main", VIRALRECON, "Sample QC", "qc-nextclade-load"),
    "fig_facets": ("main", "nf-core/nanoseq", "Isoform usage", "is-usage"),
    "fig_genome": ("main", SAREK, "Copy number & MSI", "cn-genome", "78f93b"),
    "fig_violin": ("extra", PENGUINS, None, "031c43fe-cb99-554e-9da1-1155ddafc4e5"),
    "fig_loh": ("main", SAREK, "Germline vs somatic", "gs-loh-genome", "78f905"),
    "fig_bands": ("main", SAREK, "Caller concordance", "cc-vaf-dist", "180784"),
    "fig_heatmap": ("main", "nf-core/nascent", "Genome signal", "gs-fig-chromosomes"),
    "fig_matrix": ("main", SAREK, "Structural variants", "sv-size-class", "78f902"),
    "fig_tss": ("main", "nf-core/atacseq", "ATAC quality", "aq-tss-coverage"),
    "fig_ma": ("main", "nf-core/quantms", "Reproducibility", "rep-pairs-scatter"),
    "fig_score_parts": ("main", "nf-core/raredisease", "Ranked", "rk-score-parts"),
    "fig_dot_bands": ("main", "nf-core/rnavar", "Alignment", "aln-unique-vs-dup"),
    # Advanced viz
    "viz_heatmap": ("extra", AMPLISEQ, "Ordination & Clustering", "ord-complex-heatmap"),
    "viz_upset": ("extra", AMPLISEQ, "Community & Diversity", "adv-upset"),
    "viz_oncoplot": ("main", VIRALRECON, "Variants", "var-oncoplot"),
    "viz_signal": ("main", "nf-core/cutandrun", "Peaks", "pk-pileup-matrix"),
    "viz_coverage": ("main", VIRALRECON, "Coverage & Depth", "cov-amplicon-track"),
    "viz_cnv": ("main", SAREK, "Copy number & MSI", "cn-profile", "9836d7"),
    "viz_chord": ("main", "nf-core/oncoanalyser", "Structural variants", "sx-chords"),
    "viz_ideogram": ("main", SAREK, "Structural variants", "sv-ideogram", "78f902"),
    "viz_lollipop": ("main", SAREK, "Protein", "pr-lollipop", "180787"),
    "viz_fusion": ("main", "nf-core/oncoanalyser", "Structural variants", "sx-fusion-exons"),
    "viz_volcano": ("main", "nf-core/riboseq", "Translational regulation", "tr-analysis-volcano"),
    "viz_manhattan": ("main", "nf-core/cutandrun", "Caller agreement", "ca-macs-manhattan"),
    "viz_ranked": ("main", "nf-core/raredisease", "Ranked", "rk-top-candidates"),
    "viz_dotplot": ("main", "nf-core/rnafusion", "Caller Evidence", "evid-dotplot"),
    "viz_sunburst": ("trec", TREC, "Community & Diversity", "adv-sunburst"),
    "viz_sankey": ("trec", TREC, "Community & Diversity", "adv-sankey"),
    "viz_stacked": ("trec", TREC, "Community & Diversity", "adv-stacked-taxonomy"),
    "viz_rarefaction": ("extra", AMPLISEQ, "Alpha Diversity", "alpha-rarefaction-multi"),
    "viz_hmm_logo": ("extra", "nf-core/proteinfamilies", "Profile HMM", "hmm-logo"),
    "viz_msa": ("extra", "nf-core/proteinfamilies", "Profile HMM", "hmm-msa"),
    # Card: overview rows, one style each
    "kpi_threshold": ("main", VIRALRECON, None, "ov-kf-samples", "3a7efa"),
    "kpi_box": ("main", VIRALRECON, None, "ov-kf-depth", "3a7efa"),
    "kpi_coverage": ("main", VIRALRECON, None, "ov-kf-genome-10x", "3a7efa"),
    "kpi_top_n": ("main", "nf-core/oncoanalyser", None, "ov-kf-drivers"),
    "kpi_composition": ("main", "nf-core/rnaseq", None, "ov-kf-samples"),
    "kpi_gauge": ("main", "nf-core/rnavar", None, "ov-kf-shared"),
    "kpi_donut": ("main", "nf-core/nascent", None, "nc-ov-kf-responsive"),
    "kpi_histogram": ("main", "nf-core/raredisease", None, "ov-kf-top"),
    # Interactive: the filters that drive the linked example below
    "link_species": ("extra", PENGUINS, None, "2835bba2-6fcf-585d-a735-d4167aeb0534"),
    "link_season": ("extra", PENGUINS, None, "567403ac-c087-5aee-9ab2-c4a36c6ec934"),
    # MultiQC
    "mqc_fastqc_status": ("main", VIRALRECON, "MultiQC", "mqc-fastqc-status"),
    "mqc_general_stats": ("main", VIRALRECON, "MultiQC", "mqc-general-stats"),
    "mqc_mosdepth": ("main", VIRALRECON, "MultiQC", "mqc-mosdepth-cumulative"),
    "mqc_bcftools": ("main", VIRALRECON, "MultiQC", "mqc-bcftools"),
    "mqc_vep_sift": ("main", SAREK, "MultiQC", "129c4c29-7ff3-5f80-97d4-fbb09a7754f9", "180780"),
    "mqc_insert_size": ("main", SAREK, "MultiQC", "c1778798-16e8-5e2e-8364-24b5b2a7bda3", "180780"),
    # Map
    "map_sites": ("extra", AMPLISEQ, None, "ref-sampling-sites"),
    # Text
    "text_about": ("extra", AMPLISEQ, None, "ov-about", "ed33"),
    "text_steps": ("extra", VIRALRECON, None, "ov-steps"),
    "text_study": ("main", "nf-core/raredisease", None, "ov-study"),
    "text_run": ("main", "nf-core/raredisease", None, "ov-run"),
    # Image
    "image_gallery": ("extra", CELLPAINTING, None, None),
}

# A filtered example: the components below are exported once per
# combination of the filters' values, and the home page swaps them when a
# filter frame posts a new value. Each pack is live/<name>_<theme>.json:
# {"shell": page with __PAYLOAD__ in place of the payload, "variants": {key:
# payload}}. The key is the sorted species joined by "+" (empty for all),
# then "|", then the season range "from-to".
LINKED = {
    "instance": "extra",
    "dashboard": PENGUINS,
    "species": ["Adelie", "Chinstrap", "Gentoo"],
    "seasons": [2007, 2008, 2009],
    "components": {
        "link_scatter": "a9c71416-ffe5-5c4d-b967-8470a1875a21",
        "link_mix": "67ca138c-c97f-58d7-a409-f2d8ab74d88d",
        "link_mass": "26afa8b1-d787-53b0-afcf-5ec153eeaba0",
        "link_trend": "216884aa-a73c-5c0f-9da9-18fd36ae4c2d",
        "link_sex": "6f6d29d7-ac37-5f9b-8f44-9e7aa87d2c86",
    },
}
PAYLOAD = re.compile(r'(<script id="embed-payload" type="application/json">)(.*?)(</script>)', re.S)

# Config overrides, as a dashboard author would set them in the YAML: the
# renderer reads the config from the payload, so the export carries them.
TWEAKS = {
    "viz_ideogram": {"orientation": "vertical"},
    "viz_chord": {"show_labels": True},
    "viz_upset": {
        "set_colors": {"Riverwater": "#1a4f8f", "Groundwater": "#22b8cf", "Sediment": "#f5a11b", "Soil": "#00a550"},
        "default_annotation_cols": ["Kingdom"],
    },
}
# Ranks a stacked taxonomy keeps: the deeper ones hold most of the rows.
STACKED_RANKS = {"Kingdom", "Phylum", "Class"}
# CSS added to an exported page, for a tile shown larger than on its dashboard.
# The media query keeps a narrow frame (a phone) at the dashboard's size.
PAGE_CSS = {
    "text_study": "@media (min-width: 480px) { html { font-size: 118%; } }",
    "text_run": "@media (min-width: 480px) { html { font-size: 118%; } }",
}
# Rows a ranked table keeps: enough for its top N and a few changes of it.
RANKED_ROWS = 200

SCRIPT = re.compile(r'<script type="module" crossorigin>(.*?)</script>', re.S)
STYLE = re.compile(r'<style rel="stylesheet" crossorigin>(.*?)</style>', re.S)

# Points the Image component's server URLs at the local copies, by file name.
IMAGE_SHIM = """<script>
(function () {
  var PREFIX = '/depictio/api/v1/files/serve/image?s3_path=';
  function local(img) {
    var src = img.getAttribute('src') || '';
    if (src.indexOf(PREFIX) !== 0) return;
    var name = decodeURIComponent(src.slice(PREFIX.length)).split('/').pop();
    img.setAttribute('src', 'img/' + name.replace(/\\.[^.]+$/, '') + '.webp');
  }
  new MutationObserver(function (records) {
    records.forEach(function (r) {
      if (r.type === 'attributes') local(r.target);
      r.addedNodes.forEach(function (n) {
        if (n.nodeType !== 1) return;
        if (n.tagName === 'IMG') local(n);
        if (n.querySelectorAll) n.querySelectorAll('img').forEach(local);
      });
    });
  }).observe(document.documentElement, { subtree: true, childList: true, attributes: true, attributeFilter: ['src'] });
})();
</script>"""


def get(base: str, path: str, body: dict | None = None) -> bytes:
    """GET a path of the API, or POST ``body`` to it as JSON."""
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"{base}/depictio/api/v1{path}", data=data)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(request, timeout=300) as response:
        return response.read()


def resolve(
    base: str, dashboards: list[dict], title: str, tab: str | None, component: str | None, pin: str | None = None
):
    """The (dashboard id, component listing) holding a component, by titles.

    Several dashboards can share a title (two runs of one template); the
    newest one that has the component wins.
    """
    roots = [d["dashboard_id"] for d in dashboards if d.get("title") == title and not d.get("parent_dashboard_id")]
    for root in reversed(roots):
        ids = [root] if tab is None else [
            d["dashboard_id"] for d in dashboards if d.get("parent_dashboard_id") == root and d.get("title") == tab
        ]
        for dashboard in ids:
            if pin and not dashboard.endswith(pin):
                continue
            listing = {c["component_id"]: c for c in json.loads(get(base, f"/export/dashboards/{dashboard}/components"))}
            if component in listing or (component is None and any(c["component_type"] == "image" for c in listing.values())):
                return dashboard, listing
    raise SystemExit(f"no {component!r} in {title!r} / {tab!r} on {base}")


def tweak(base: str, dashboard: str, component: str, page: str, overrides: dict) -> str:
    """Apply config overrides and fill in what the export leaves out.

    An UpSet plot ships a figure computed on the server from the stored
    config, without its annotation tracks, so it is computed again here from
    the overridden config. A ranked table ships only the columns bound by a
    ``*_col`` key, so its table is fetched again with every column it shows.
    """
    match = PAYLOAD.search(page)
    payload = json.loads(match.group(2))
    config = payload["component"].get("config") or {}
    config.update(overrides)
    kind = config.get("viz_kind")
    key = f"embed::{component}"
    if kind in ("upset_plot", "ranked_table", "stacked_taxonomy"):
        stored = next(
            c for c in json.loads(get(base, f"/dashboards/get/{dashboard}"))["stored_metadata"] if c["index"] == component
        )
        binding = {"wf_id": stored["wf_id"], "dc_id": stored["dc_id"], "filter_metadata": []}
        if kind == "upset_plot":
            payload["data"]["compute"][key] = upset(base, config, binding)
        elif kind == "stacked_taxonomy":
            keys = [config[k] for k in ("sample_id_col", "taxon_col", "rank_col")]
            keys += [strip["column"] for strip in config.get("annotation_strips") or []]
            columns = keys + [config["abundance_col"]]
            table = json.loads(get(base, "/advanced_viz/data", {**binding, "columns": columns, "viz_kind": kind}))
            rows = table["rows"]
            index = [i for i, r in enumerate(rows[config["rank_col"]]) if r in STACKED_RANKS]
            table["rows"] = {column: [values[i] for i in index] for column, values in rows.items()}
            payload["data"]["advancedVizData"][key] = summed(table, keys, config["abundance_col"])
        else:
            table = payload["data"]["advancedVizData"][key] = ranked_rows(base, config, binding)
            genotypes = payload["data"]["advancedVizData"].get(config.get("genotypes_dc_id") or "")
            if genotypes and config.get("genotypes_key_col") in table["rows"]:
                # The genotype grid only needs the kept variants.
                kept = set(table["rows"][config["genotypes_key_col"]])
                rows = genotypes["rows"]
                index = [i for i, v in enumerate(rows[config["genotypes_row_col"]]) if v in kept]
                genotypes["rows"] = {column: [values[i] for i in index] for column, values in rows.items()}
                genotypes["row_count"] = len(index)
    if kind == "sunburst":
        table = payload["data"]["advancedVizData"][key]
        payload["data"]["advancedVizData"][key] = summed(table, config["rank_cols"], config["abundance_col"])
    text = json.dumps(payload).replace("</", "<\\/")
    return page[: match.start(2)] + text + page[match.end(2) :]


def summed(table: dict, keys: list[str], value: str) -> dict:
    """``table`` with ``value`` summed per distinct ``keys``, zero sums dropped."""
    rows = table["rows"]
    sums: dict[tuple, float] = {}
    for i, amount in enumerate(rows[value]):
        group = tuple(rows[k][i] for k in keys)
        sums[group] = sums.get(group, 0.0) + (amount or 0.0)
    kept = [(group, total) for group, total in sums.items() if total > 0]
    columns = {k: [group[j] for group, _ in kept] for j, k in enumerate(keys)}
    columns[value] = [float(f"{total:.4g}") for _, total in kept]
    return {**table, "columns": keys + [value], "rows": columns, "row_count": len(kept), "total_rows": len(kept)}


def upset(base: str, config: dict, binding: dict) -> dict:
    """The UpSet figure for ``config``, as UpsetRenderer asks for it on first paint."""
    body = {
        **binding,
        "set_columns": config.get("set_columns"),
        "set_colors": config.get("set_colors"),
        "annotation_cols": config.get("default_annotation_cols") or None,
        "sort_by": config.get("sort_by", "cardinality"),
        "sort_order": config.get("sort_order", "descending"),
        "min_size": config.get("min_size", 1),
        "max_degree": config.get("max_degree"),
        "show_set_sizes": config.get("show_set_sizes", True),
        "show_values": config.get("show_values", False),
        "color_intersections_by": config.get("color_intersections_by", "none"),
    }
    job = json.loads(get(base, "/advanced_viz/compute_upset", body))
    for _ in range(120):
        if job.get("result"):
            return job["result"]
        if job.get("status") in ("failed", "error"):
            break
        time.sleep(1)
        job = json.loads(get(base, f"/advanced_viz/compute_upset/{job['job_id']}"))
    raise SystemExit(f"UpSet compute did not finish: {job.get('status')}")


def ranked_rows(base: str, config: dict, binding: dict) -> dict:
    """A ranked table's best RANKED_ROWS rows, with every column it shows."""
    keys = ("title_col", "subtitle_col", "score_col", "rank_col", "sort_col", "filter_col", "genotypes_key_col")
    columns = [config[k] for k in keys if config.get(k)]
    for column in config.get("columns") or []:
        columns += [column[k] for k in ("column", "max_from", "min_from") if column.get(k)]
    columns += config.get("popover_columns") or []
    columns = list(dict.fromkeys(columns))
    table = json.loads(get(base, "/advanced_viz/data", {**binding, "columns": columns, "viz_kind": "ranked_table"}))
    rows = table["rows"]
    score = rows[config.get("sort_col") or config["score_col"]]
    sign = -1 if config.get("descending", True) else 1
    order = sorted(range(len(score)), key=lambda i: (score[i] is None, sign * (score[i] or 0)))[:RANKED_ROWS]
    table["rows"] = {column: [values[i] for i in order] for column, values in rows.items()}
    table["row_count"] = len(order)
    return table


def add_tabs(page: str, dashboards: list[dict], dashboard: str) -> str:
    """Give a text tile its tab family, so its `tab:` links keep their icons.

    Its `section:` and `params:` links are reduced to their text.

    Image icons (a path on the server) are left out: the page cannot load them.
    """
    family = next(d for d in dashboards if d["dashboard_id"] == dashboard)
    root = family.get("parent_dashboard_id") or dashboard
    tabs = [
        {
            "label": (d.get("main_tab_name") or d["title"]) if d["dashboard_id"] == root else d["title"],
            "icon": d.get("tab_icon") if ":" in (d.get("tab_icon") or "") else None,
            "color": d.get("tab_icon_color"),
        }
        for d in dashboards
        if d["dashboard_id"] == root or d.get("parent_dashboard_id") == root
    ]
    match = PAYLOAD.search(page)
    payload = json.loads(match.group(2))
    payload["tabs"] = tabs
    # Links to a section or to the run parameters open panels of the
    # dashboard, which the page does not have: keep their text only.
    body = payload["component"].get("body")
    if body:
        payload["component"]["body"] = re.sub(r"\[([^\]]*)\]\((?:section|params):[^)]*\)", r"\1", body)
    text = json.dumps(payload).replace("</", "<\\/")
    return page[: match.start(2)] + text + page[match.end(2) :]


def split(page: str, bundles: dict[str, str]) -> str:
    """Swap the inlined bundle for links to shared files named by its hash."""
    js, css = SCRIPT.search(page), STYLE.search(page)
    if not js or not css:
        raise SystemExit("export page has no inlined bundle; did the export format change?")
    tag = hashlib.sha256((js.group(1) + css.group(1)).encode()).hexdigest()[:10]
    bundles[f"embed-{tag}.js"] = js.group(1)
    bundles[f"embed-{tag}.css"] = css.group(1)
    page = page[: js.start()] + f'<script type="module" crossorigin src="embed-{tag}.js"></script>' + page[js.end() :]
    css = STYLE.search(page)
    return page[: css.start()] + f'<link rel="stylesheet" href="embed-{tag}.css">' + page[css.end() :]


def localise_images(base: str, page: str) -> str:
    """Download the gallery's pictures and add the shim that serves them."""
    folder = re.search(r'"s3_base_folder":\s*"([^"]+)"', page)
    if not folder:
        raise SystemExit("image export carries no s3_base_folder")
    (OUT / "img").mkdir(exist_ok=True)
    for name in sorted(set(re.findall(r'"([^"/]+\.(?:png|jpe?g|webp|tiff?))"', page))):
        path = OUT / "img" / (Path(name).stem + ".webp")
        if path.exists():
            continue
        s3_path = folder.group(1).rstrip("/") + "/" + name
        im = Image.open(io.BytesIO(get(base, "/files/serve/image?s3_path=" + urllib.parse.quote(s3_path, safe=""))))
        im = im.convert("RGB")
        if im.width > IMAGE_WIDTH:
            im = im.resize((IMAGE_WIDTH, round(im.height * IMAGE_WIDTH / im.width)), Image.LANCZOS)
        im.save(path, "WEBP", quality=82, method=6)
        print(f"{path.relative_to(OUT.parents[3])}  {path.stat().st_size / 1024:.0f} KB")
    return page.replace("<head>", "<head>" + IMAGE_SHIM, 1)


def linked_variants():
    """Every (key, filters) pair of the linked example; "all" is the empty key."""
    species, seasons = LINKED["species"], LINKED["seasons"]
    picks = [list(c) for n in range(len(species)) for c in itertools.combinations(species, n)]
    for chosen in picks:
        for i, low in enumerate(seasons):
            for high in seasons[i:]:
                filters = []
                if chosen:
                    filters.append({"interactive_component_type": "MultiSelect", "column_name": "species", "value": chosen})
                if (low, high) != (seasons[0], seasons[-1]):
                    filters.append({"interactive_component_type": "RangeSlider", "column_name": "year", "value": [low, high]})
                yield f"{'+'.join(chosen)}|{low}-{high}", filters


def export_linked(bundles: dict[str, str]) -> None:
    base = INSTANCES[LINKED["instance"]]
    dashboards = json.loads(get(base, "/dashboards/list?include_child_tabs=true"))
    variants = list(linked_variants())
    for name, component in LINKED["components"].items():
        dashboard, _ = resolve(base, dashboards, LINKED["dashboard"], None, component)
        for theme in ("light", "dark"):
            pack: dict = {"variants": {}}
            for key, filters in variants:
                query = f"format=html&theme={theme}&filters=" + urllib.parse.quote(json.dumps(filters))
                page = split(get(base, f"/export/dashboards/{dashboard}/components/{component}?{query}").decode(), bundles)
                match = PAYLOAD.search(page)
                pack["variants"][key] = match.group(2)
                pack.setdefault("shell", page[: match.start(2)] + "__PAYLOAD__" + page[match.end(2) :])
            path = OUT / f"{name}_{theme}.json"
            path.write_text(json.dumps(pack, separators=(",", ":")))
            print(f"{path.relative_to(OUT.parents[3])}  {path.stat().st_size / 1024:.0f} KB")


def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dashboards: dict[str, list[dict]] = {}
    bundles: dict[str, str] = {}
    if not names or "linked" in names:
        export_linked(bundles)
    for name in [n for n in names if n != "linked"] or ([] if names else PICKS):
        instance, title, tab, component, *pin = PICKS[name]
        base = INSTANCES[instance]
        if base not in dashboards:
            dashboards[base] = json.loads(get(base, "/dashboards/list?include_child_tabs=true"))
        dashboard, listing = resolve(base, dashboards[base], title, tab, component, *pin)
        if component is None:
            component = next(cid for cid, c in listing.items() if c["component_type"] == "image")
        kind = listing[component]["component_type"]
        for theme in ("light", "dark"):
            page = get(base, f"/export/dashboards/{dashboard}/components/{component}?format=html&theme={theme}").decode()
            page = split(page, bundles)
            if kind == "advanced_viz":
                page = tweak(base, dashboard, component, page, TWEAKS.get(name, {}))
            if kind == "text":
                page = add_tabs(page, dashboards[base], dashboard)
            if kind == "image":
                page = localise_images(base, page)
            if name in PAGE_CSS:
                page = page.replace("</head>", f"<style>{PAGE_CSS[name]}</style></head>", 1)
            path = OUT / f"{name}_{theme}.html"
            path.write_text(page)
            print(f"{path.relative_to(OUT.parents[3])}  {path.stat().st_size / 1024:.0f} KB")
    for file, text in bundles.items():
        path = OUT / file
        path.write_text(text)
        print(f"{path.relative_to(OUT.parents[3])}  {path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
