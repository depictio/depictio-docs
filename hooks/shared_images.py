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

_PREFIXES = tuple(f"images/{name}/" for name in SHARED_SUBTREES)

# Matches the output-relative form mkdocs emits ("../../images/guides/x.png")
# as well as a bare "images/guides/x.png".
_URL_RE = re.compile(
    r"(?:\.\./)*images/(" + "|".join(re.escape(n) for n in SHARED_SUBTREES) + r")/"
)


def _enabled() -> bool:
    return os.environ.get("DEPICTIO_DOCS_SHARED_IMAGES") == "1"


def _shared_base(config) -> str:
    """Absolute URL of the shared image root, e.g. https://host/docs/images/."""
    site_url = config.get("site_url") or "/"
    return site_url.rstrip("/") + "/images/"


def on_files(files: Files, config, **kwargs) -> Files:
    """Drop the shared subtrees so mike does not copy them into this version."""
    if not _enabled():
        return files
    kept = [f for f in files if not f.src_uri.startswith(_PREFIXES)]
    dropped = len(files) - len(kept)
    if dropped:
        print(f"[shared_images] excluded {dropped} image files from the versioned build")
    return Files(kept)


def on_post_page(output: str, page, config, **kwargs) -> str:
    """Repoint image URLs at the shared root."""
    if not _enabled():
        return output
    return _URL_RE.sub(_shared_base(config) + r"\1/", output)
