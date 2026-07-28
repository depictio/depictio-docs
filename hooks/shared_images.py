"""Serve documentation images from one unversioned copy.

mike copies the whole docs tree into a directory per released version, so the
screenshot set is republished once per release. On gh-pages that turned into
~2 GB of images that hold only ~42 MB of distinct bytes: the same files, 48
times over. GitHub Pages caps a published site at 1 GB.

With DEPICTIO_DOCS_SHARED_IMAGES=1 this hook keeps the bulky image subtrees
out of the per-version build and points the rendered pages at a single copy
published at the site root. Without it (local `mkdocs serve`) nothing changes
and relative image paths resolve normally, so authoring is unaffected.

Trade-off: an archived version renders the current screenshots rather than the
ones it shipped with. images/logo/ deliberately stays per-version because
theme.logo, theme.favicon and the inline-select-svg plugin resolve those at
build time, and they are small.
"""

from __future__ import annotations

import os
import re

from mkdocs.structure.files import Files

# Image subtrees served from the shared root. Everything else under images/
# (logo assets, one-off icons) is small and stays inside each version.
SHARED_SUBTREES = (
    "architecture",
    "data-model",
    "guides",
    "modularity",
    "pipeline-templates",
    "react",
)

# Generated catalog gallery, ~16 MB per theme. Regenerated on every deploy and
# identical across versions until the catalog itself changes, so it is by far
# the largest thing a version was carrying. Shared like the images, with the
# same drift caveat, which docs/catalog/index.md states on the page.
SHARED_FILES = (
    "assets/component-catalog-light.html",
    "assets/component-catalog-dark.html",
)

_PREFIXES = tuple(f"images/{name}/" for name in SHARED_SUBTREES)

# Matches the output-relative form mkdocs emits ("../../images/guides/x.png")
# as well as a bare "images/guides/x.png".
_URL_RE = re.compile(
    r"(?:\.\./)*images/(" + "|".join(re.escape(n) for n in SHARED_SUBTREES) + r")/"
)

# Same, for the individually shared files: "../assets/component-catalog-*.html".
_FILE_RE = re.compile(
    r"(?:\.\./)*(" + "|".join(re.escape(f) for f in SHARED_FILES) + r")"
)


def _enabled() -> bool:
    return os.environ.get("DEPICTIO_DOCS_SHARED_IMAGES") == "1"


def _site_root(config) -> str:
    """Absolute URL of the site root, e.g. https://host/depictio-docs/.

    Not simply config["site_url"]: mike's mkdocs plugin rewrites that to
    urljoin(site_url, version) so each version gets its own canonical URL. The
    shared copies live at the root, above every version, so the version segment
    mike appended has to come back off.
    """
    site_url = (config.get("site_url") or "/").rstrip("/") + "/"
    version = os.environ.get("MIKE_DOCS_VERSION", "").strip("/")
    if version and site_url.endswith(f"/{version}/"):
        site_url = site_url[: -len(version) - 1]
    return site_url


def on_files(files: Files, config, **kwargs) -> Files:
    """Drop the shared content so mike does not copy it into this version."""
    if not _enabled():
        return files
    kept = [
        f
        for f in files
        if not f.src_uri.startswith(_PREFIXES) and f.src_uri not in SHARED_FILES
    ]
    dropped = len(files) - len(kept)
    if dropped:
        print(f"[shared_images] excluded {dropped} files from the versioned build")
    return Files(kept)


def on_post_page(output: str, page, config, **kwargs) -> str:
    """Repoint URLs at the shared copies."""
    if not _enabled():
        return output
    root = _site_root(config)
    output = _URL_RE.sub(root + r"images/\1/", output)
    return _FILE_RE.sub(root + r"\1", output)
