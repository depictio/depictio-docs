"""Screenshot the home page's component examples from the public showcases.

Each entry in PICKS is one component tile of a dashboard on
https://showcases.depictio.embl.org, which opens in anonymous public mode, so
no login is needed. Every dashboard is loaded once, at 2x, and each picked
tile is captured in light, then again after the app's own theme toggle in dark.

    python dev/capture_components.py            # all picks
    python dev/capture_components.py map_sites  # just these

Writes docs/images/landing/components/<name>_{light,dark}.webp, the full-size
shots the home page's component showcase shows and its lightbox opens.
dev/make_thumbs.py then composes the card grids.
Needs Playwright with Chromium (the depictio venv has both).
"""

from __future__ import annotations

import asyncio
import io
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageChops
from playwright.async_api import async_playwright

BASE = "https://showcases.depictio.embl.org"
OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "landing" / "components"
MAX_WIDTH = 1600
QUALITY = 80

PENGUINS = "6824cb3b89d2b72169309738"
VIRALRECON = "6accf00cfe17adcb30c3f090"
AMPLISEQ_MQC = "6ace2a5035f38069731af615"

# name -> (dashboard id, data-component-index). "@filters" is the filter panel.
# The showcases still run the old demo data for the sunburst, oncoplot,
# heatmap, sankey and volcano; the Advanced viz panel uses the v1.19.3
# captures in images/guides/advanced-visualizations/ for those instead.
PICKS = {
    "figure_bill_shape": (PENGUINS, "0417c281-0316-50d2-af63-b1203e41b2e8"),
    "figure_mass_season": (PENGUINS, "33a8e07c-059d-5249-8e5f-ec4f6e966005"),
    "figure_mass_violin": (PENGUINS, "5473d989-833d-5da1-b142-2cc19a64ea59"),
    "figure_af_histogram": ("6accf00dfe17adcb30c3f094", "var-af-histogram"),
    "viz_genome_track": ("6accf00dfe17adcb30c3f093", "cov-genome-track"),
    "viz_structure": ("6ad105ac376d37f865da6032", "pr-structure"),
    "card_species": (PENGUINS, "29fbcfbc-07ce-5397-a68f-4d211554ee16"),
    "card_mass": (PENGUINS, "2c886b36-5892-5161-813f-6d4eb0b082d8"),
    "card_season": (PENGUINS, "6c89aba3-31f9-55e8-a880-0326db38cc2a"),
    "card_flipper": (PENGUINS, "aa825d52-ea02-5dd7-be66-7d16b6e3c18a"),
    "card_bills": (PENGUINS, "938c7080-b193-5529-8dcd-673f4fa917ae"),
    "card_island": (PENGUINS, "3888f006-d014-5dda-a638-9cfa4c1ad775"),
    "card_sex": (PENGUINS, "8cef95a3-cb86-5894-aa1c-7d419d990046"),
    "card_individuals": (PENGUINS, "c6d99bc3-2ad2-5add-9715-8ecf5df848f3"),
    "multiqc_quality": (AMPLISEQ_MQC, "446efea5-c61a-5696-ad3f-2e98abb2b8c3"),
    "multiqc_stats": (AMPLISEQ_MQC, "9eae5ad5-a13f-5b30-88dd-cfa4e7e6db2a"),
    "multiqc_status": (AMPLISEQ_MQC, "f6589248-783b-5233-9ef0-0581ef5fd320"),
    "multiqc_cutadapt": (AMPLISEQ_MQC, "c083a3cb-d2f2-5293-8410-33a3826a2dc3"),
    "map_sites": ("646b0f3c1e4a2d7f8e5b8cc3", "ref-campaign-grid"),
    "table_abundance": ("646b0f3c1e4a2d7f8e5b8cb3", "comm-table-rel-abundance"),
    "interactive_da": ("6accea29a57cdb54ef9a220b", "@filters"),
    "interactive_alpha": ("6accea28a57cdb54ef9a2208", "@filters"),
    "text_run": (VIRALRECON, "ov-run"),
    "text_steps": (VIRALRECON, "ov-steps"),
    "text_about": (VIRALRECON, "ov-about"),
}

# The public-mode tour, the notes button and the floating dock sit over tiles.
SETUP = "try{localStorage.setItem('depictio.walkthrough.public',JSON.stringify({status:'completed',step:0,version:'v6'}))}catch(e){}"
HIDE = ".dc-notes-toggle,.hy-dock,.mantine-Popover-dropdown{display:none!important}"


def trim_bottom(im: Image.Image) -> Image.Image:
    """Cut the empty tail of the filter panel, keeping a small margin."""
    # Look inside the card's side borders, which run the full height.
    inner = im.convert("RGB").crop((40, 0, im.width - 40, im.height))
    bg = Image.new("RGB", inner.size, inner.getpixel((inner.width // 2, inner.height - 4)))
    box = ImageChops.difference(inner, bg).point(lambda v: 255 if v > 24 else 0).getbbox()
    if not box:
        return im
    return im.crop((0, 0, im.width, min(im.height, box[3] + 48)))


def save(png: bytes, name: str, theme: str, filters: bool) -> None:
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if filters:
        im = trim_bottom(im)
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
    path = OUT / f"{name}_{theme}.webp"
    im.save(path, "WEBP", quality=QUALITY, method=6)
    print(f"{path.relative_to(OUT.parent.parent.parent)}  {im.width}x{im.height}  {path.stat().st_size / 1024:.0f} KB")


async def expand_sections(page) -> None:
    """Open folded sections, whose tiles are not rendered until then."""
    for _ in range(3):
        closed = await page.query_selector_all(
            '.depictio-dashboard-grid button.mantine-Accordion-control[aria-expanded="false"]'
        )
        if not closed:
            return
        for button in closed:
            try:
                await button.click(timeout=2000)
            except Exception:
                pass
        await page.wait_for_timeout(1500)


async def settle(page) -> None:
    """Scroll through the page so every lazy tile renders, then wait."""
    await expand_sections(page)
    height = await page.evaluate("document.scrollingElement.scrollHeight")
    for y in range(0, height, 600):
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(150)
    await page.wait_for_timeout(2500)


async def capture(page, picks: list[tuple[str, str]], theme: str) -> None:
    await settle(page)
    for name, index in picks:
        if index == "@filters":
            await page.evaluate("window.scrollTo(0, 0)")
            el = await page.query_selector(".hy-drawer-card")
        else:
            el = await page.query_selector(f'.depictio-component-chrome[data-component-index="{index}"]')
        if el is None:
            print(f"MISSING {name} ({index})")
            continue
        await el.evaluate("e => e.scrollIntoView({block: 'center'})")
        await page.wait_for_timeout(700)
        save(await el.screenshot(animations="disabled"), name, theme, index == "@filters")


async def dashboard(browser, dash: str, picks: list[tuple[str, str]]) -> None:
    # A tall viewport keeps the biggest tiles whole on screen while captured.
    ctx = await browser.new_context(viewport={"width": 1680, "height": 2400}, device_scale_factor=2)
    await ctx.add_init_script(SETUP)
    page = await ctx.new_page()
    await page.goto(f"{BASE}/dashboard/{dash}", wait_until="networkidle", timeout=120000)
    await page.add_style_tag(content=HIDE)
    await page.wait_for_timeout(6000)
    await capture(page, picks, "light")
    await page.locator('button[aria-label="Switch to dark theme"]').first.click()
    await page.wait_for_timeout(5000)
    await capture(page, picks, "dark")
    await ctx.close()


async def main(names: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    by_dash: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for name, (dash, index) in PICKS.items():
        if not names or name in names:
            by_dash[dash].append((name, index))
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        gate = asyncio.Semaphore(3)

        async def one(dash, picks):
            async with gate:
                await dashboard(browser, dash, picks)

        await asyncio.gather(*(one(d, p) for d, p in by_dash.items()))
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
