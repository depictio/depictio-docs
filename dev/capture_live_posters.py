"""Capture the posters of the home page's live component examples.

A live example (data-live-src, -grid or -linked in docs/index.md) shows a
screenshot until its exported component has loaded, and that screenshot is
what the lightbox opens and what a reader without JS sees. This script opens
the home page from a running `mkdocs serve`, selects every live example in
turn, waits for it to load and saves the showcase stage as
docs/images/landing/live/poster/<name>_{light,dark}.webp, the name being the
one in the example's poster link. Run it after dev/export_components.py.
The files are written once the browser is done: `mkdocs serve` reloads the
page on every change under docs/.

    python dev/capture_live_posters.py http://127.0.0.1:8194/depictio-docs/

Needs Playwright with Chromium (the depictio venv has both).
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "landing" / "live" / "poster"
QUALITY = 80


def main(url: str) -> None:
    shots: dict[str, bytes] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1100})
        page.goto(url)
        page.wait_for_timeout(1500)
        page.locator(".cshow").scroll_into_view_if_needed()
        for theme, scheme in (("light", "default"), ("dark", "slate")):
            page.evaluate(f"document.body.setAttribute('data-md-color-scheme', '{scheme}')")
            for tab in page.locator(".cshow-tab").all():
                tab.click()
                panel = page.locator(".cshow-panel:not([hidden])")
                for pill in panel.locator(".cshow-ex").all():
                    pill.click()
                    shot = panel.locator(".cshow-shot:not([hidden])")
                    if not any(shot.get_attribute(a) for a in ("data-live-src", "data-live-grid", "data-live-linked")):
                        continue
                    href = shot.locator(f"a.cshow-{theme}").get_attribute("href")
                    name = re.sub(r"_(light|dark)\.webp$", "", href.rsplit("/", 1)[1])
                    print(theme, name, flush=True)
                    page.wait_for_function(
                        "el => el.classList.contains('is-live')", arg=shot.element_handle(), timeout=60000
                    )
                    page.wait_for_timeout(3000)
                    shots[f"{name}_{theme}"] = panel.locator(".cshow-stage").screenshot()
        browser.close()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, png in shots.items():
        path = OUT / f"{name}.webp"
        Image.open(io.BytesIO(png)).convert("RGB").save(path, "WEBP", quality=QUALITY, method=6)
        print(f"{path.relative_to(OUT.parents[3])}  {path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/depictio-docs/")
