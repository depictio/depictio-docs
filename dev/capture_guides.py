"""Screenshots and short videos of the guide pages' UI, from a running Depictio.

Each @shot flow drives the instance at BASE_URL to the state a guide describes
and returns what to capture: an element, a clip of the viewport (CSS pixels)
or None for the whole viewport. It runs twice at 2x, light then dark, the theme
set in the app's own localStorage key before the page loads. Each @video flow
is recorded in light theme at 1x and kept as H.264, minus its idle waits.

    BASE_URL=http://127.0.0.1:8058 python dev/capture_guides.py         # every shot
    python dev/capture_guides.py whats_new_panel runs_compare_menu     # just these
    python dev/capture_guides.py --videos [compare-runs ...]           # videos

Writes docs/images/guides/<topic>/<name>_{light,dark}.webp, and <name>.mp4 with
a <name>.webp poster. Needs Playwright with Chromium, Pillow and ffmpeg.

The instance holds the demo state the flows find by name: "Sequencing QC study"
(dev/multiqc-multi-reports runs as run_NN folders: a sample_qc table, a
samplesheet linked to the MultiQC collection, an uploaded library_prep table,
a run_summary read from a URL, and the "Sequencing QC overview" dashboard,
visited before its newest runs came in), "Soil microbiome 16S" (nf-core/ampliseq
2.18.0 megatest split by SRA batch into water_2019 and sediment_2019, visited, then
soil_2019 attached, with the template's dashboard) and, for migration, a second instance at TARGET_URL. Videos create
what they show (a project, a run, a send): run them on a fresh state.
"""

from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image
from playwright.sync_api import Locator, Page, sync_playwright

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8058").rstrip("/")
TARGET_URL = os.environ.get("TARGET_URL", "http://127.0.0.1:8059").rstrip("/")
OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "guides"
VIEWPORT = {"width": 1440, "height": 900}
MAX_WIDTH, QUALITY = 1600, 80
QC, QC_DASH, SOIL = "Sequencing QC study", "Sequencing QC overview", "Soil microbiome 16S"
NEW = "Lake sediment 16S"  # the name typed in New project (not a project of the instance)
SCATTER, BOX = "Reads vs GC content", "Duplicate reads by condition"
# What's new and the Metadata panel run on the ampliseq template dashboard of SOIL: the megatest
# split by SRA batch into water_2019 and sediment_2019 (seen) and soil_2019 (attached after the mark).
NEW_RUN = "soil_2019"
AMP, ALPHA, ORD, COMM = "nf-core/ampliseq", "Alpha Diversity", "Ordination & Clustering", "Community & Diversity"
SHANNON_BOX, RAREFACTION, COMPOSITION = "Shannon diversity per group", "Rarefaction curves", "Composition per sample"
PHYLUM_BAR, PCOA = "Phylum composition per group", "Sample ordination"
# The QC review of every sample, from its read tracking (overall_summary.tsv): fail when Cutadapt
# kept under 85 % of the reads or DADA2 under 70 %, recheck when DADA2 kept under 80 %.
LABEL, LABELS = "review", {
    "SRR10070130": "pass", "SRR10070131": "pass", "SRR10070132": "fail", "SRR10070133": "fail",
    "SRR10070134": "pass", "SRR10070141": "recheck", "SRR10070149": "pass", "SRR10070150": "recheck",
    "SRR10070151": "pass", "SRR10102392": "pass", "SRR10102393": "pass", "SRR10102394": "pass"}
DRAWER = {"x": 640, "y": 70, "width": 800, "height": 830}  # the docked panel on the right
HEADER = {"x": 270, "y": 80, "width": 1150, "height": 250}  # a project page's title and facts

# Tours done and theme chosen before the first paint (the app's own keys).
SETUP = """try{for (const [k, v] of [['builder','v4'],['public','v6']])
  localStorage.setItem('depictio.walkthrough.' + k, JSON.stringify({status:'completed',step:99,version:v}));
localStorage.setItem('theme-store', JSON.stringify('%s'));}catch(e){}"""

SHOTS: list = []  # (topic, name, flow)
VIDEOS: list = []  # (topic, name, flow, speed)


def shot(topic: str, name: str):
    return lambda fn: SHOTS.append((topic, name, fn)) or fn


def video(topic: str, name: str, speed: float = 1.0):
    return lambda fn: VIDEOS.append((topic, name, fn, speed)) or fn


# ── helpers ──────────────────────────────────────────────────────────────────


def goto(page: Page, path: str, settle: int = 4000, base: str = BASE_URL) -> Page:
    page.goto(base + path, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.add_style_tag(content=".mantine-Notifications-root{display:none!important}")
    page.wait_for_timeout(settle)
    return page


def api(page: Page, path: str):
    """GET from the API as the signed-in viewer (the SPA's own token)."""
    if not page.url.startswith(BASE_URL):
        goto(page, "/projects", settle=1500)
    return page.evaluate("""async p => {
        const t = JSON.parse(localStorage.getItem('local-store') || '{}').access_token;
        const r = await fetch('/depictio/api/v1' + p, {headers: t ? {Authorization: 'Bearer ' + t} : {}});
        return r.ok ? r.json() : null; }""", path)


_ids: dict[str, str] = {}


def project_id(page: Page, name: str) -> str:
    if name not in _ids:
        _ids.update({p["name"]: p.get("_id") or p["id"] for p in api(page, "/projects/get/all")})
    return _ids[name]


def dashboard_id(page: Page, title: str) -> str:
    if title not in _ids:
        _ids.update({d["title"]: d["dashboard_id"] for d in api(page, "/dashboards/list")})
    return _ids[title]


def dc_id(page: Page, project: str, tag: str) -> str:
    doc = api(page, f"/projects/get/from_id?project_id={project_id(page, project)}")
    return next(c["_id"] for w in doc["workflows"] for c in w["data_collections"] if c["data_collection_tag"] == tag)


def glide(page: Page, target: Locator, click: bool = True, pause: int = 600) -> None:
    """Move the pointer to the target in visible steps, then click it."""
    target.scroll_into_view_if_needed()
    box = target.bounding_box()
    if box:
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=18)
    page.wait_for_timeout(pause // 2)
    if click:
        target.click()
    page.wait_for_timeout(pause)


def type_slowly(page: Page, target: Locator, text: str) -> None:
    glide(page, target)
    target.press_sequentially(text, delay=30)
    page.wait_for_timeout(600)


def scroll(page: Page, dy: int, steps: int = 12) -> None:
    for _ in range(steps):
        page.mouse.wheel(0, dy / steps)
        page.wait_for_timeout(40)
    page.wait_for_timeout(900)


def dialog(page: Page) -> Locator:
    return page.locator("[role=dialog]").last


def modal(page: Page) -> Locator:
    return page.locator(".mantine-Modal-content").last


def popover(page: Page) -> Locator:
    return page.locator(".mantine-Popover-dropdown:visible").last


def union(page: Page, *targets: Locator, pad: int = 10) -> dict:
    """The clip around all targets, inside the viewport."""
    boxes = [t.bounding_box() for t in targets]
    x0 = max(min(b["x"] for b in boxes) - pad, 0)
    y0 = max(min(b["y"] for b in boxes) - pad, 0)
    x1 = min(max(b["x"] + b["width"] for b in boxes) + pad, page.viewport_size["width"])
    y1 = min(max(b["y"] + b["height"] for b in boxes) + pad, page.viewport_size["height"])
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def save(png: bytes, path: Path) -> None:
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(OUT.parent.parent)}  {im.width}x{im.height}  {path.stat().st_size / 1024:.0f} KB")


# ── project creation ─────────────────────────────────────────────────────────


def new_project(page: Page, name: str = NEW, folder: str | None = None, add_data: bool = True) -> Locator:
    goto(page, "/projects").get_by_role("button", name="New project").click()
    page.get_by_placeholder("Enter project name").fill(name)
    if add_data:
        dialog(page).get_by_role("button", name="Add data").first.click()
        page.wait_for_timeout(1000)
    if folder:
        page.get_by_placeholder("~/results/run42").fill(folder)
        page.get_by_test_id("read-level-template").wait_for(timeout=30000)
        page.wait_for_timeout(5000)
    return modal(page)


def attach(page: Page, folder: str) -> Locator:
    goto(page, f"/projects/{project_id(page, SOIL)}").get_by_role("button", name="Add data").first.click()
    page.get_by_role("textbox", name="Folder or bucket").fill(folder)
    page.wait_for_timeout(9000)
    page.get_by_text("What Depictio found").first.scroll_into_view_if_needed()
    return modal(page)


def settings(page: Page, project: str, section: str) -> Locator:
    goto(page, f"/projects/{project_id(page, project)}").get_by_role("button", name="Project settings").click()
    dialog(page).get_by_text(section, exact=True).first.click()
    page.wait_for_timeout(1500)
    return modal(page)


def import_dialog(page: Page, tab: str) -> Locator:
    new_project(page, "", add_data=False)
    dialog(page).get_by_role("button", name="Import a project").click()
    page.get_by_role("tab", name=tab).click()
    page.wait_for_timeout(800)
    return modal(page)


def builder(page: Page, step: int) -> None:
    """1: source; 2: a collection being defined (sequencing runs, sample_qc.tsv); 3: review."""
    new_project(page, "QC study, read by the builder", "~/runs/qc_study")
    page.get_by_role("button", name="Open the Project Builder").click()
    page.wait_for_timeout(4000)
    if step == 1:
        return
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Structure").click()
    page.get_by_role("option", name="Sequencing runs").click()
    page.get_by_text("run_01", exact=True).first.click()
    page.get_by_text("sample_qc.tsv", exact=True).first.click()
    page.get_by_text("Scan (pattern)", exact=True).click()
    page.get_by_role("textbox", name="Tag").fill("sample_qc")
    page.wait_for_timeout(2000)
    if step == 3:
        page.get_by_role("button", name="Add to main").click()
        page.get_by_role("button", name="Review & create").last.click()
        page.wait_for_timeout(4000)


@shot("project-creation", "read_in_place_url")
def read_in_place_url(page):
    new_project(page)
    page.get_by_text("One file URL", exact=True).click()
    page.get_by_role("textbox", name="File URL").fill("http://127.0.0.1:8099/run_summary.tsv")
    page.wait_for_timeout(4000)
    return modal(page)


@shot("project-creation", "what_depictio_found")
def what_found(page):
    new_project(page, folder="~/runs/soil_spring_2025")
    dialog(page).get_by_role("button", name="Next").click()
    page.wait_for_timeout(4000)
    return modal(page)


for _topic, _name, _flow in [
    ("project-creation", "projects_page", lambda p: goto(p, "/projects") and None),
    ("project-creation", "new_project_dialog", lambda p: new_project(p, add_data=False)),
    ("project-creation", "your_data_step", lambda p: new_project(p)),
    ("project-creation", "read_levels", lambda p: new_project(p, folder="~/runs/soil_spring_2025")),
    ("project-creation", "project_header_found",
     lambda p: goto(p, f"/projects/{project_id(p, SOIL)}") and {**HEADER, "height": 210}),
    ("project-creation", "add_data_run", lambda p: attach(p, "~/runs/soil_autumn_2025")),
    ("project-creation", "duplicate_samples", lambda p: attach(p, "~/runs/soil_spring_2025_rerun")),
    ("project-creation", "export_zip", lambda p: settings(p, SOIL, "Export")),
    ("project-creation", "import_from_instance", lambda p: import_dialog(p, "From another instance")),
    ("project-creation", "import_from_zip", lambda p: import_dialog(p, "From a ZIP file")),
    ("project-creation", "builder_source", lambda p: builder(p, 1)),
    ("project-creation", "builder_collections", lambda p: builder(p, 2)),
    ("project-creation", "builder_review", lambda p: builder(p, 3)),
]:
    shot(_topic, _name)(_flow)


# ── what's new, multiqc ──────────────────────────────────────────────────────


def dashboard(page: Page, query: str = "", settle: int = 9000, title: str = QC_DASH) -> Page:
    return goto(page, f"/dashboard/{dashboard_id(page, title)}{query}", settle=settle)


def amp(page: Page, tab: str = ALPHA, settle: int = 9000) -> Page:
    """A tab of the ampliseq dashboard, its filter panel closed."""
    if tab not in _ids:
        tabs = api(page, f"/dashboards/tabs/{dashboard_id(page, AMP)}")["child_tabs"]
        _ids.update({t["title"]: t["dashboard_id"] for t in tabs})
    goto(page, f"/dashboard/{_ids[tab]}", settle=settle)
    close = page.get_by_role("button", name="Close filters")
    if close.is_visible():
        close.click()
        page.wait_for_timeout(1500)
    return page


def tile(page: Page, title: str) -> Locator:
    """The tile titled `title`; else the first whose text holds it (a prefix of a long title)."""
    exact = page.locator(".react-grid-item").filter(has=page.get_by_text(title, exact=True))
    return exact.first if exact.count() else page.locator(".react-grid-item").filter(has_text=title).first


def wide(page: Page, width: int = 2100) -> Page:
    """A wider window, for tiles whose labels need the room."""
    page.set_viewport_size({"width": width, "height": 1000})
    return page


def mqc_tile(page: Page, plot: str, dash: str = QC_DASH) -> Locator:
    """A MultiQC tile by its plot ("general_stats" for General Stats), rendered once in view."""
    doc = api(page, f"/dashboards/get/{dashboard_id(page, dash)}")
    index = next(c["index"] for c in doc["stored_metadata"] if c.get("selected_plot") == plot)
    target = page.locator(f'.react-grid-item:has([data-component-index="{index}"])').first
    target.scroll_into_view_if_needed()
    page.wait_for_timeout(6000)
    return target


def whats_new(page: Page, view: str | None = None, hide_seen: bool = False, close: bool = False,
              run: str | None = None, tab: str | None = None) -> Page:
    """The dashboard with its What's new panel open, Off | Overlay | Split picked,
    on all the new runs or on one (`run`)."""
    (amp(page, tab) if tab else dashboard(page)).get_by_test_id("changes-pill").first.click()
    page.wait_for_timeout(1500)
    if view:
        page.get_by_test_id("changes-view").get_by_text(view, exact=True).click()
    if run:
        page.wait_for_timeout(800)
        page.get_by_test_id("changes-run-focus").get_by_text(run, exact=True).click()
    if hide_seen:
        page.get_by_test_id("changes-hide-seen").locator("..").click()
    page.wait_for_timeout(8500 if view else 0)
    if close:
        page.keyboard.press("Escape")
        page.mouse.move(1439, 450)
        page.wait_for_timeout(1200)
    return page


def tall(page: Page, height: int = 1200) -> Page:
    """A taller window, so two rows of tiles clear the dock."""
    page.set_viewport_size({"width": VIEWPORT["width"], "height": height})
    return page


def tiles(page: Page, *titles: str) -> dict:
    """The clip around these tiles, the first scrolled near the top, once drawn."""
    tile(page, titles[0]).evaluate("e => e.scrollIntoView({block: 'start'})")
    page.mouse.wheel(0, -90)
    page.wait_for_timeout(6000)
    return union(page, *(tile(page, t) for t in titles), pad=2)


def dot_menu(page: Page, title: str = SCATTER, tab: str | None = None) -> Page:
    tile(amp(page, tab) if tab else dashboard(page), title).get_by_test_id("component-updated-dot").click()
    page.wait_for_timeout(1000)
    return page


@shot("whats-new", "before_now")
def before_now(page):
    dot_menu(page, SHANNON_BOX, ALPHA).get_by_test_id("component-updated-before-now").click()
    page.wait_for_timeout(9000)
    return modal(page)


@shot("whats-new", "profile_mark_mode")
def profile_mark_mode(page):
    section = goto(page, "/profile#preferences").get_by_test_id("settings-section-preferences")
    if not page.get_by_test_id("changes-since-pref").is_visible():
        section.get_by_text("Preferences", exact=True).first.click()
    page.get_by_test_id("changes-since-pref").scroll_into_view_if_needed()
    return section


@shot("whats-new", "editor_history")
def editor_history(page):
    goto(page, f"/dashboard-edit/{dashboard_id(page, AMP)}", 7000).get_by_role("button", name="Settings").first.click()
    dialog(page).get_by_text("History", exact=True).first.click()
    page.wait_for_timeout(3000)
    return modal(page)


@shot("whats-new", "project_whats_new")
def project_whats_new(page):
    goto(page, f"/projects/{project_id(page, QC)}", 5000).get_by_text("What's new", exact=True).first.click()
    page.wait_for_timeout(2500)


@shot("whats-new", "notifications_bell")
def bell(page):
    goto(page, "/projects").get_by_role("button", name="Notifications").first.click()
    page.wait_for_timeout(2500)


def manage_dc(page: Page, tab: str) -> Locator:
    """Manage Data Collection on the ampliseq metadata table, on one of its tabs."""
    row = goto(page, f"/projects/{project_id(page, SOIL)}", 5000).locator("tr").filter(has=page.get_by_text("metadata", exact=True)).first
    row.scroll_into_view_if_needed()
    row.get_by_test_id("manage-dc-btn").click()
    page.wait_for_timeout(2000)
    modal(page).get_by_text(tab, exact=True).first.click()
    page.wait_for_timeout(1200)
    return modal(page)


shot("project-creation", "manage_dc_modify")(lambda p: manage_dc(p, "Modify data"))
shot("project-creation", "manage_dc_clear")(lambda p: manage_dc(p, "Clear contents"))


@shot("multiqc", "manage_collection")
def multiqc_manage(page):
    row = goto(page, f"/projects/{project_id(page, QC)}", 5000).locator("tr").filter(has_text="multiqc_data").first
    row.scroll_into_view_if_needed()
    row.get_by_test_id("manage-dc-btn").click()
    page.wait_for_timeout(2000)
    return modal(page)


for _topic, _name, _flow in [
    ("whats-new", "whats_new_key", lambda p: amp(p) and {"x": 940, "y": 4, "width": 496, "height": 76}),
    ("whats-new", "whats_new_panel", lambda p: whats_new(p, tab=ALPHA).get_by_test_id("changes-panel")),
    ("whats-new", "overlay_scatter", lambda p: tile(whats_new(p, "Overlay", close=True, tab=ORD), PCOA)),
    ("whats-new", "overlay_figures", lambda p: tiles(
        whats_new(tall(p, 1300), "Overlay", close=True, tab=COMM), PHYLUM_BAR, COMPOSITION)),
    ("whats-new", "split_view", lambda p: tiles(
        whats_new(tall(p), "Split", close=True, tab=ALPHA), "Observed ASVs", "Evenness", RAREFACTION)),
    ("whats-new", "split_figures", lambda p: tiles(
        whats_new(tall(p, 1300), "Split", close=True, tab=COMM), PHYLUM_BAR, COMPOSITION)),
    ("whats-new", "hide_seen", lambda p: whats_new(p, "Overlay", hide_seen=True, tab=ALPHA) and None),
    ("whats-new", "tile_dot_menu", lambda p: dot_menu(p, "Observed ASVs", ALPHA) and None),
    ("multiqc", "multiqc_figure", lambda p: mqc_tile(dashboard(p), "Sequence Counts")),
    ("multiqc", "general_stats", lambda p: mqc_tile(dashboard(p), "general_stats")),
    ("multiqc", "overlay_multiqc", lambda p: mqc_tile(whats_new(p, "Overlay", close=True), "Sequence Counts")),
    ("multiqc", "overlay_general_stats", lambda p: mqc_tile(whats_new(p, "Overlay", close=True), "general_stats")),
    # A wider window widens the tile, so the sample names are not clipped.
    ("multiqc", "split_multiqc", lambda p: mqc_tile(whats_new(wide(p), "Split", close=True), "Sequence Counts")),
]:
    shot(_topic, _name)(_flow)


# ── compare runs, data updates ───────────────────────────────────────────────


def runs_tab(page: Page, run: str | None = None, project: str = SOIL) -> Locator:
    goto(page, f"/projects/{project_id(page, project)}?tab=runs", settle=5000)
    if not run:
        return page.get_by_test_id("runs-panel")
    page.get_by_test_id(f"run-row-{run}").locator("td").first.click()
    page.wait_for_timeout(3500)
    details = page.get_by_test_id(f"run-details-{run}")
    details.scroll_into_view_if_needed()
    return short_path(details, run)


def short_path(details: Locator, run: str) -> Locator:
    """The runs live in a scratch folder: show the short path a reader would have."""
    details.evaluate("""(el, run) => { const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        for (let n; (n = w.nextNode());) if (n.nodeValue.includes('/runs/' + run))
            n.nodeValue = '~/runs/' + run; }""", run)
    return details


def key_figures(page: Page) -> Page:
    """The ampliseq Overview scrolled to its headline cards."""
    page.get_by_text("Key figures", exact=True).first.evaluate("e => e.scrollIntoView({block: 'start'})")
    page.mouse.wheel(0, -60)
    page.wait_for_timeout(4000)
    return page


def samples_card(page: Page) -> Locator:
    return page.locator(".react-grid-item").filter(has_text="in the sample sheet, by").first


def ingestion_of(page: Page, run: str, project: str = SOIL) -> str:
    """The ingestion that brought `run`, else the newest one (a CLI refresh records no run tags)."""
    events = [e for e in api(page, f"/changes/project/{project_id(page, project)}/timeline")["events"]
              if e["type"] == "ingestion"]
    return next((e["id"] for e in events if run in e.get("run_tags", [])), events[0]["id"])


@shot("compare-runs", "runs_compare_menu")
def runs_compare_menu(page):
    """One dashboard: Compare opens it, and its tooltip names the dashboard (several get a menu)."""
    details = runs_tab(page, NEW_RUN)
    button = details.get_by_text("Compare", exact=True)
    button.evaluate("e => e.scrollIntoView({block: 'center'})")
    page.wait_for_timeout(800)
    box, b = details.bounding_box(), button.bounding_box()
    return {"keep_hover": button, "x": box["x"], "y": b["y"] - 216, "width": box["width"], "height": 266}


@shot("compare-runs", "scans_picker")
def scans_picker(page, all_files: bool = False):
    details = runs_tab(page, NEW_RUN)
    details.get_by_test_id("run-scan").filter(has_text=re.compile(r"\d+ (changed|new)")).last.click()
    if all_files:
        details.get_by_text("Only what this scan changed").click()
    page.wait_for_timeout(2000)
    box = details.bounding_box()
    end = details.get_by_text(re.compile("computed for this run", re.I)).first.bounding_box()
    return {"x": box["x"], "y": box["y"], "width": box["width"], "height": end["y"] - box["y"] - 8}


@shot("compare-runs", "new_rows_table")
def new_rows_table(page):
    dc = dc_id(page, SOIL, "alpha_diversity_multi_canonical")
    goto(page, f"/projects/{project_id(page, SOIL)}?table={dc}&new_runs={NEW_RUN}", 6000)
    page.get_by_text("Back to full table").first.scroll_into_view_if_needed()
    page.wait_for_timeout(1500)


def activity(page: Page, view: str) -> dict:
    goto(page, f"/projects/{project_id(page, SOIL)}?tab=activity", 5000).get_by_text(view, exact=True).first.click()
    page.wait_for_timeout(3000)
    page.get_by_text("Latest ingestion", exact=True).first.evaluate("e => e.scrollIntoView({block: 'start'})")
    page.wait_for_timeout(800)
    return {"x": 270, "y": 0, "width": 1170, "height": 900}


@shot("data-updates", "data_refresh")
def data_refresh(page):
    target = settings(page, QC, "Data refresh")
    page.get_by_test_id("manifest-refresh-full").locator("..").click()
    return target


for _topic, _name, _flow in [
    ("compare-runs", "runs_tab", lambda p: runs_tab(p)),
    ("compare-runs", "run_produced", lambda p: runs_tab(p, NEW_RUN)),
    ("compare-runs", "scans_all_files", lambda p: scans_picker(p, all_files=True)),
    ("compare-runs", "dashboard_before_run", lambda p: key_figures(dashboard(
        p, f"?before_run={ingestion_of(p, NEW_RUN)}", 10000, AMP)) and None),
    ("data-updates", "activity_latest", lambda p: activity(p, "Latest ingestion")),
    ("data-updates", "activity_history", lambda p: activity(p, "History")),
]:
    shot(_topic, _name)(_flow)


# ── metadata panel (session labels on the samplesheet) ───────────────────────


def metadata_panel(page: Page, labels: bool = True) -> Page:
    amp(page, settle=7000).get_by_test_id("metadata-button").click()
    page.locator("[data-testid=annotation-grid] .ag-row").first.wait_for(timeout=30000)
    page.wait_for_timeout(1500)
    if labels:
        add_labels(page)
    return page


def paste(page: Page, cell: Locator, values: list[str]) -> None:
    """Paste `values` down a column from `cell`, as from a spreadsheet."""
    cell.click()
    page.evaluate("""t => { const d = new DataTransfer(); d.setData('text/plain', t);
        document.dispatchEvent(new ClipboardEvent('paste', {clipboardData: d, bubbles: true})); }""", "\n".join(values))


def add_labels(page: Page, slow: bool = False) -> None:
    """Add the label column, label every sample (a few typed, the rest pasted) and
    compare the labels in the charts (once)."""
    if page.get_by_test_id(f"label-menu-{LABEL}").count():
        return
    page.get_by_test_id("label-add").click()
    page.get_by_test_id("label-name-input").press_sequentially(LABEL, delay=60 if slow else 0)
    page.get_by_test_id("label-name-save").click()
    page.wait_for_timeout(800)
    grid = page.get_by_test_id("annotation-grid")
    col = grid.locator(".ag-header-cell", has_text=LABEL).first.get_attribute("col-id")
    keys = grid.locator(".ag-cell[col-id=__key]").evaluate_all(  # the key column may be pinned
        "cs => cs.map(c => [+c.closest('.ag-row').getAttribute('row-index'), c.innerText.trim()])"
        ".sort((a, b) => a[0] - b[0]).map(r => r[1])")
    values = [LABELS[k] for k in keys]  # the grid's rows, in its order
    typed = 3 if slow else 0
    cell = lambda row: grid.locator(f".ag-center-cols-container [row-index='{row}'] [col-id='{col}']")  # noqa: E731
    for row in range(typed):
        glide(page, cell(row), click=False, pause=200)
        cell(row).dblclick()
        page.keyboard.press("ControlOrMeta+A")
        page.keyboard.type(values[row], delay=60)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
    if slow:
        glide(page, cell(typed), click=False, pause=300)
    paste(page, cell(typed), values[typed:])
    page.wait_for_timeout(1500 if slow else 600)
    column_menu(page, slow)
    page.get_by_role("menuitem", name="Compare in the charts").click()
    page.wait_for_timeout(1500)


def column_menu(page: Page, slow: bool = False) -> Page:
    target = page.get_by_test_id(f"label-menu-{LABEL}")
    glide(page, target, pause=800) if slow else target.click()
    page.wait_for_timeout(600)
    return page


def coloured_by_groups(page: Page, close: bool = False) -> Page:
    """The labels as groups: the figures coloured by them, the cards comparing them."""
    metadata_panel(page).get_by_test_id("analysis-button").click()
    page.get_by_text("My groups", exact=True).first.click()
    page.wait_for_timeout(1500)
    page.get_by_text("Compare groups in cards", exact=True).click()
    page.wait_for_timeout(7000)
    if close:
        page.get_by_test_id("analysis-button").click()
        page.wait_for_timeout(5000)
    return page


def library_table(page: Page, mode: str) -> None:
    """The uploaded library_prep table, its edit lock flipped to `mode` (locked/editing)."""
    goto(page, f"/projects/{project_id(page, QC)}?table={dc_id(page, QC, 'library_prep')}", 6000)
    section = page.get_by_test_id("table-data-section")
    if section.get_attribute("data-mode") != mode:
        section.locator(".mantine-Switch-track").first.click()
        page.wait_for_timeout(4000)
    section.evaluate("e => e.scrollIntoView({block: 'start'})")
    page.mouse.wheel(0, -60)
    page.wait_for_timeout(1500)


for _topic, _name, _flow in [
    ("metadata-panel", "metadata_dock_button", lambda p: union(p, amp(p, settle=7000).get_by_test_id(
        "metadata-button").locator("xpath=ancestor::*[contains(@class,'hy-dock')][1]"), pad=14)),
    ("metadata-panel", "metadata_panel_labels", lambda p: metadata_panel(p) and DRAWER),
    ("metadata-panel", "metadata_column_menu", lambda p: column_menu(metadata_panel(p)) and DRAWER),
    ("metadata-panel", "metadata_groups_analysis", lambda p: coloured_by_groups(p) and None),
    ("metadata-panel", "labels_on_dashboard", lambda p: tiles(
        coloured_by_groups(tall(p), close=True), "Observed ASVs", "Evenness", RAREFACTION)),
    ("metadata-panel", "table_locked", lambda p: library_table(p, "locked")),
    ("metadata-panel", "table_edit_mode", lambda p: library_table(p, "editing")),
]:
    shot(_topic, _name)(_flow)


# ── migration (the target is a second instance at TARGET_URL), admin ─────────


def receive_dialog(page: Page) -> Locator:
    goto(page, "/projects", base=TARGET_URL).get_by_role("button", name="New project").click()
    page.get_by_role("button", name="Import a project").click()
    page.get_by_test_id("receive-note").fill("Sequencing QC study, from lab-a")
    page.get_by_test_id("receive-create").click()
    page.get_by_test_id("receive-code").wait_for()
    page.wait_for_timeout(800)
    return modal(page)


def new_code(page: Page) -> str:
    """A fresh invite code from the target, read off its Receive dialog."""
    receive_dialog(page)
    return page.get_by_test_id("receive-code").input_value().strip()


def send_modal(page: Page, code: str, check: bool = False) -> Locator:
    settings(page, QC, "Send").get_by_role("button", name="Send to another instance").click()
    page.get_by_test_id("migrate-url").fill(TARGET_URL)
    page.get_by_test_id("migrate-code").fill(code)
    if check:
        page.get_by_test_id("migrate-check").click()
        page.get_by_test_id("migrate-preflight").wait_for(timeout=60000)
        page.wait_for_timeout(1000)
    return modal(page)


@shot("migration", "request_sheet")
def request_sheet(page):
    goto(page, "/projects", 5000, TARGET_URL).get_by_test_id("migration-banner").get_by_role("button", name="Details").click()
    page.wait_for_timeout(2500)


@shot("migration", "read_only_badge")
def read_only_badge(page):
    goto(page, "/projects", base=TARGET_URL).locator("tr").filter(has_text=QC).first.locator("td").nth(1).click()
    page.wait_for_timeout(6000)
    return HEADER


def admin_table(page: Page, tab: str) -> None:
    goto(page, f"/admin/{tab}", 5000).get_by_role("button", name="Table display").first.click()
    page.wait_for_timeout(1200)


for _topic, _name, _flow in [
    ("migration", "receive_project_dialog", receive_dialog),
    ("migration", "send_destination", lambda p: send_modal(p, "7KQ2-M9XD-4TRF-H8WA-2BNC-QE5V")),
    ("migration", "send_checked", lambda p: send_modal(p, new_code(p.context.new_page()), check=True)),
    ("migration", "received_projects", lambda p: goto(p, "/projects", 5000, TARGET_URL) and {
        "x": 270, "y": 80, "width": 1170, "height": 360}),
    ("admin", "admin_projects_columns", lambda p: admin_table(p, "projects")),
    ("admin", "admin_dashboards_columns", lambda p: admin_table(p, "dashboards")),
    ("admin", "activity_page", lambda p: goto(p, "/activity", 6000) and None),
    ("admin", "activity_page_ingestion", lambda p: goto(p, "/activity").get_by_text(
        "Ingestion", exact=True).first.click() or p.wait_for_timeout(3000)),
]:
    shot(_topic, _name)(_flow)


# ── dashboard guide: tile chrome on the ampliseq Alpha Diversity tab ─────────


def alpha_tile(page: Page, edit: bool = False, title: str = "Shannon diversity per group") -> Locator:
    dashboard(page, settle=3000, title="nf-core/ampliseq").get_by_text("Alpha Diversity", exact=True).first.click()
    page.wait_for_timeout(8000)
    if edit:
        page.goto(page.url.replace("/dashboard/", "/dashboard-edit/"))
        page.wait_for_timeout(9000)
    target = page.locator(".react-grid-item").filter(has_text=title).first
    target.evaluate("e => e.scrollIntoView({block: 'start'})")
    page.mouse.wheel(0, -120)
    page.wait_for_timeout(2500)
    return target


@shot("dashboard-guide", "tile_info_popover")
def tile_info(page):
    page.set_viewport_size({"width": 1440, "height": 1200})  # room for the whole popover
    target = alpha_tile(page)
    target.get_by_test_id("component-info-icon").click()
    page.wait_for_timeout(1500)
    return union(page, target, popover(page))


@shot("dashboard-guide", "tile_data_source_popover")
def tile_data_source(page):
    page.set_viewport_size({"width": 1440, "height": 1200})
    target = alpha_tile(page, edit=True)
    page.add_style_tag(content=".hy-dock{display:none!important}")
    target.hover()
    target.get_by_role("button", name="Data source and settings").click()
    page.wait_for_timeout(1500)
    popover(page).evaluate("""d => { for (const e of [d, ...d.querySelectorAll('*')])
        if (e.scrollHeight > e.clientHeight + 4) e.scrollTop = e.scrollHeight; }""")  # down to Code
    page.wait_for_timeout(500)
    return union(page, target, popover(page))


@shot("dashboard-guide", "tile_toolbar_icons")
def tile_toolbar(page):
    target = alpha_tile(page, edit=True)
    title = target.get_by_text("Shannon diversity per group").first
    title.hover()
    page.wait_for_timeout(1000)
    clip = union(page, target.locator(".modebar").first, target.get_by_role("button", name="Drag to move"),
                 target.get_by_role("button", name="Component actions"), pad=12)
    return {"keep_hover": title, **clip}


# ── videos: clock.start() at the first action, cut()…resume() around a wait ──


@video("project-creation", "create-project-from-folder", speed=1.3)
def create_project_video(page, clock):
    goto(page, "/projects", settle=2500)
    clock.start()
    glide(page, page.get_by_role("button", name="New project"))
    type_slowly(page, page.get_by_placeholder("Enter project name"), SOIL)
    glide(page, dialog(page).get_by_role("button", name="Add data").first)
    type_slowly(page, page.get_by_placeholder("~/results/run42"), "~/runs/soil_spring_2025")
    page.get_by_test_id("read-level-template").wait_for(timeout=30000)
    page.wait_for_timeout(1500)
    glide(page, page.get_by_test_id("read-level-template"), click=False, pause=800)
    glide(page, dialog(page).get_by_role("button", name="Next"), pause=2000)
    glide(page, dialog(page).get_by_role("button", name="Next"), pause=1500)
    glide(page, dialog(page).get_by_role("button", name="Create Project"), pause=3000)
    clock.cut()
    page.locator("[data-testid=run-created-status]:not([data-state=running]):not([data-state=creating])").wait_for(
        timeout=900000)
    clock.resume()
    page.wait_for_timeout(2000)
    glide(page, page.get_by_test_id("run-created-open-dashboard"), pause=5000)


@video("project-creation", "add-run")
def add_run_video(page, clock):
    goto(page, f"/projects/{project_id(page, SOIL)}", settle=3000)
    clock.start()
    glide(page, page.get_by_role("button", name="Add data").first)
    type_slowly(page, page.get_by_role("textbox", name="Folder or bucket"), "~/runs/soil_summer_2025")
    page.get_by_test_id("attach-run-found").wait_for(timeout=60000)
    glide(page, page.get_by_test_id("attach-run-found"), click=False, pause=2500)
    glide(page, page.get_by_test_id("add-data-submit"), pause=3000)
    clock.cut()
    page.locator("[data-testid=attach-run-progress][data-state=running]").wait_for(state="detached", timeout=900000)
    clock.resume()
    page.wait_for_timeout(2500)
    if page.get_by_test_id("add-data-done").is_visible():
        glide(page, page.get_by_test_id("add-data-done"), pause=1500)
    glide(page, page.get_by_text("Each run and what it holds"), pause=3000)


def pick_view(page: Page, view: str, settle: int = 6000, run: str | None = None) -> None:
    glide(page, page.get_by_test_id("changes-pill").first, pause=1200)
    glide(page, page.get_by_test_id("changes-view").get_by_text(view, exact=True), pause=1500)
    if run:
        glide(page, page.get_by_test_id("changes-run-focus").get_by_text(run, exact=True), pause=1200)
    page.keyboard.press("Escape")
    page.mouse.move(1400, 500, steps=10)
    page.wait_for_timeout(settle)


@video("whats-new", "whats-new-overlay-split", speed=1.2)
def overlay_split_video(page, clock):
    """Alpha Diversity: Overlay down the rarefaction curves to the box plot, then Split
    and back up to the cards. The wheel turns in the margin: over a figure it would ask
    for the zoom key."""
    amp(page, settle=8000).mouse.move(1400, 500)
    clock.start()
    pick_view(page, "Overlay")
    page.mouse.move(1425, 600, steps=10)
    scroll(page, 560)
    page.wait_for_timeout(2500)
    scroll(page, 560)
    page.wait_for_timeout(2000)
    pick_view(page, "Split", settle=5000)
    page.mouse.move(1425, 600, steps=10)
    scroll(page, -560)
    page.wait_for_timeout(2000)
    scroll(page, -560)
    page.wait_for_timeout(3000)


@video("whats-new", "before-now")
def before_now_video(page, clock):
    dot = tile(amp(page, settle=8000), SHANNON_BOX).get_by_test_id("component-updated-dot")
    dot.scroll_into_view_if_needed()
    page.wait_for_timeout(3000)
    clock.start()
    glide(page, dot, pause=1200)
    glide(page, page.get_by_test_id("component-updated-before-now"), pause=7000)
    page.mouse.move(900, 860, steps=10)
    page.wait_for_timeout(2000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)
    glide(page, dot, pause=1000)
    glide(page, page.get_by_test_id("component-updated-compare"), pause=4000)


@video("compare-runs", "compare-runs")
def compare_runs_video(page, clock):
    """The new run's Compare, then Before | Now on the phylum bars: the Soil group is new."""
    runs_tab(page)
    clock.start()
    glide(page, page.get_by_test_id(f"run-row-{NEW_RUN}").locator("td").first, pause=300)
    details = page.get_by_test_id(f"run-details-{NEW_RUN}")
    details.wait_for()
    short_path(details, NEW_RUN)
    page.wait_for_timeout(2000)
    glide(page, details.get_by_text("Compare", exact=True), pause=1500)
    clock.cut()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(8000)
    clock.resume()
    page.mouse.move(1425, 500, steps=8)
    scroll(page, 700, steps=20)
    page.wait_for_timeout(2500)
    clock.cut()  # the same ?before_run view, on the tab whose figures the run changed
    run_q = page.url.split("?", 1)[1]
    amp(page, COMM, settle=2000)
    goto(page, f"{urlparse(page.url).path}?{run_q}", settle=10000)
    target = tile(page, PHYLUM_BAR)
    target.evaluate("e => e.scrollIntoView({block: 'center'})")
    page.wait_for_timeout(2500)
    clock.resume()
    page.wait_for_timeout(1500)
    glide(page, target.get_by_test_id("component-updated-dot"), pause=1200)
    glide(page, page.get_by_test_id("component-updated-before-now"), pause=300)
    page.mouse.move(700, 860, steps=10)
    page.wait_for_timeout(8000)


@video("multiqc", "multiqc-compare-runs", speed=1.2)
def multiqc_video(page, clock):
    mqc_tile(dashboard(page, settle=8000), "Sequence Counts")
    page.mouse.move(1400, 500)
    clock.start()
    pick_view(page, "Overlay", settle=5000)
    scroll(page, -350)
    page.wait_for_timeout(2500)
    pick_view(page, "Split", settle=7000)
    scroll(page, 350)
    page.wait_for_timeout(3000)


@video("metadata-panel", "metadata-labels", speed=1.25)
def metadata_video(page, clock):
    """Needs no review column yet (labels are kept on the account): delete it first."""
    amp(page, settle=8000)
    clock.start()
    glide(page, page.get_by_test_id("metadata-button"), pause=600)
    page.locator("[data-testid=annotation-grid] .ag-row").first.wait_for(timeout=30000)
    page.wait_for_timeout(1200)
    add_labels(page, slow=True)
    page.wait_for_timeout(1000)
    glide(page, page.get_by_test_id("analysis-button"), pause=1200)
    glide(page, page.get_by_text("My groups", exact=True).first, pause=1500)
    glide(page, page.get_by_text("Compare groups in cards", exact=True), pause=3000)
    glide(page, page.get_by_test_id("analysis-button"), pause=2500)
    page.mouse.move(1425, 550, steps=12)
    scroll(page, 560)
    page.wait_for_timeout(2200)
    scroll(page, 560)
    page.wait_for_timeout(2500)


@video("data-updates", "refresh-new-rows")
def refresh_video(page, clock):
    """Needs a new row in the served run_summary.tsv first: the refresh reads it again."""
    goto(page, f"/projects/{project_id(page, QC)}", settle=4000)
    clock.start()
    glide(page, page.get_by_role("button", name="Project settings"), pause=900)
    glide(page, dialog(page).get_by_text("Data refresh", exact=True).first, pause=1500)
    glide(page, page.get_by_test_id("manifest-refresh-button"), pause=2000)
    clock.cut()
    page.get_by_text("Refreshing (").wait_for(state="detached", timeout=600000)
    clock.resume()
    page.wait_for_timeout(1000)
    glide(page, page.get_by_test_id("manifest-refresh-results"), click=False, pause=5000)


@video("migration", "send-receive")
def send_receive_video(page, clock):
    code = new_code(page.context.new_page())
    settings(page, QC, "Send")
    clock.start()
    glide(page, dialog(page).get_by_role("button", name="Send to another instance"), pause=900)
    type_slowly(page, page.get_by_test_id("migrate-url"), TARGET_URL)
    glide(page, page.get_by_test_id("migrate-code"), pause=300)
    page.get_by_test_id("migrate-code").fill(code)
    glide(page, page.get_by_test_id("migrate-check"), pause=500)
    page.get_by_test_id("migrate-preflight").wait_for(timeout=60000)
    page.wait_for_timeout(2500)
    glide(page, page.get_by_test_id("migrate-push-button"), pause=2500)
    clock.cut()
    page.locator("[data-testid=push-status][data-remote-status]").first.wait_for(timeout=300000)
    page.wait_for_timeout(5000)
    clock.resume()
    page.wait_for_timeout(2500)
    goto(page, "/projects", 6000, TARGET_URL)


# ── runner ───────────────────────────────────────────────────────────────────


class Clock:
    def __init__(self) -> None:
        self.t0, self.marks = time.monotonic(), []

    def mark(self) -> None:
        self.marks.append(time.monotonic() - self.t0)

    start = lambda self: setattr(self, "marks", [time.monotonic() - self.t0 - 0.3])  # noqa: E731
    cut = resume = mark

    def spans(self) -> list[tuple[float, float | None]]:
        m = self.marks + [None]
        return [(m[i], m[i + 1]) for i in range(0, len(m) - 1, 2)]


def context(browser, theme: str, **extra):
    ctx = browser.new_context(viewport=VIEWPORT, **extra)
    ctx.add_init_script(SETUP % theme)
    return ctx


def run_shots(browser, names: list[str]) -> None:
    for topic, name, flow in SHOTS:
        for theme in ("light", "dark") if not names or name in names else ():
            ctx = context(browser, theme, device_scale_factor=2)
            page = ctx.new_page()
            page.set_default_timeout(20000)
            try:
                target = flow(page)
                if isinstance(target, dict) and "keep_hover" in target:  # the shot is of a hover
                    target.pop("keep_hover").hover()
                else:
                    page.mouse.move(1439, 450)  # no hover toolbars in the shot
                page.wait_for_timeout(800)
                if isinstance(target, dict):
                    png = page.screenshot(clip=target, animations="disabled")
                else:
                    png = (target or page).screenshot(animations="disabled")
                save(png, OUT / topic / f"{name}_{theme}.webp")
            except Exception as exc:  # one broken shot must not stop the rest
                print(f"FAILED {topic}/{name} ({theme}): {str(exc).splitlines()[0]}")
            finally:
                ctx.close()


def encode(raw: Path, keep: list[tuple[float, float | None]], out: Path, speed: float = 1.0) -> None:
    """Keep the spans (seconds; None: to the end) `speed` times faster, 1280 wide, H.264;
    the poster is the last frame."""
    trims = "".join(f"[0:v]trim=start={a:.2f}{'' if b is None else f':end={b:.2f}'},setpts=PTS-STARTPTS[v{i}];"
                    for i, (a, b) in enumerate(keep))
    graph = trims + "".join(f"[v{i}]" for i in range(len(keep)))
    graph += f"concat=n={len(keep)}:v=1[c];[c]setpts=PTS/{speed},scale=1280:-2[o]"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-filter_complex", graph, "-map", "[o]",
                    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "28", "-preset", "slow",
                    "-movflags", "+faststart", str(out)], check=True)
    poster = out.with_suffix(".png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-1", "-i", str(out), "-frames:v", "1",
                    "-update", "1", str(poster)], check=True)
    save(poster.read_bytes(), out.with_suffix(".webp"))
    poster.unlink()
    print(f"{out.relative_to(OUT.parent.parent)}  {out.stat().st_size / 1024:.0f} KB")


def run_videos(browser, names: list[str]) -> None:
    for topic, name, flow, speed in VIDEOS:
        if names and name not in names:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            ctx = context(browser, "light", record_video_dir=tmp, record_video_size=VIEWPORT)
            page, clock = ctx.new_page(), Clock()
            page.set_default_timeout(30000)
            try:
                flow(page, clock)
                page.wait_for_timeout(1500)
            except Exception as exc:
                print(f"FAILED video {name}: {str(exc).splitlines()[0]}")
                continue
            finally:
                ctx.close()
            raw = Path(page.video.path())
            if os.environ.get("KEEP_RAW"):  # to re-encode later without replaying the flow
                Path(os.environ["KEEP_RAW"], f"{name}.webm").write_bytes(raw.read_bytes())
                Path(os.environ["KEEP_RAW"], f"{name}.spans").write_text(repr(clock.spans()))
            encode(raw, clock.spans(), OUT / topic / f"{name}.mp4", speed)


if __name__ == "__main__":
    args = sys.argv[1:]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        (run_videos if "--videos" in args else run_shots)(browser, [a for a in args if not a.startswith("--")])
        browser.close()
