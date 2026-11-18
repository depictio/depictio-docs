"""Point the Tools Catalog page at the catalog site of the version it documents.

The catalog is no longer built into the documentation. depictio publishes it
as its own static site (depictio/depictio-catalog on GitHub Pages, workflow
deploy-catalog.yaml in depictio/depictio), one directory per release plus
``latest/``:

    https://depictio.github.io/depictio-catalog/v1.22.0/
    https://depictio.github.io/depictio-catalog/latest/

docs/catalog/index.md carries placeholders instead of a URL:

- {{ catalog_site.base }}     the site root, ending in "/"
- {{ catalog_site.version }}  "v" + the version in pyproject.toml, e.g. v1.22.0

docs/javascripts/catalog-site.js then picks that version's directory when the
site still has it (versions.json), and ``latest/`` otherwise: a release older
than the ones kept, or a version not released yet when building locally.

DEPICTIO_CATALOG_SITE overrides the root, e.g. a local
``depictio catalog export-site`` served on localhost (point it at the directory
holding the slot directories).

An unknown placeholder fails the build rather than shipping "{{ ... }}".
"""

from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path

from mkdocs.exceptions import PluginError

PAGE = "catalog/index.md"
DEFAULT_BASE = "https://depictio.github.io/depictio-catalog/"
_PLACEHOLDER = re.compile(r"\{\{\s*catalog_site\.([a-z_]+)\s*\}\}")


def _values(config) -> dict[str, str]:
    pyproject = Path(config["config_file_path"]).parent / "pyproject.toml"
    version = tomllib.loads(pyproject.read_text())["project"]["version"]
    base = os.environ.get("DEPICTIO_CATALOG_SITE", DEFAULT_BASE).rstrip("/") + "/"
    return {"base": base, "version": f"v{version}"}


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    if page.file.src_uri != PAGE:
        return markdown
    values = _values(config)

    def fill(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise PluginError(f"catalog_site: unknown placeholder {{{{ catalog_site.{key} }}}}")
        return values[key]

    return _PLACEHOLDER.sub(fill, markdown)
