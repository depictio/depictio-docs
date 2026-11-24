// Tools Catalog links: open the catalog site of the documented version.
//
// The catalog is its own static site (depictio/depictio-catalog), one
// directory per release plus latest/. Links carry the version the page
// documents (hooks/catalog_site.py); this points them at that directory when
// the site still keeps it (versions.json), at latest/ otherwise, and passes
// the docs theme as ?theme=.

const CATALOG_LINK_SELECTOR = 'a[data-catalog-site]';

function catalogScheme() {
  return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
}

const catalogSlots = {};

function catalogSlotFor(base, wanted) {
  const key = base + '|' + wanted;
  if (!catalogSlots[key]) {
    // A slow or failing versions.json must not leave a dead link.
    const signal = typeof AbortSignal !== 'undefined' && AbortSignal.timeout
      ? AbortSignal.timeout(5000) : undefined;
    catalogSlots[key] = fetch(base + 'versions.json', { cache: 'no-cache', signal })
      .then((r) => (r.ok ? r.json() : {}))
      .then((v) => (Array.isArray(v.versions) && v.versions.includes(wanted) ? wanted : 'latest'))
      .catch(() => 'latest');
  }
  return catalogSlots[key];
}

function pointCatalogLink(link) {
  const base = link.dataset.catalogSite;
  catalogSlotFor(base, link.dataset.catalogVersion).then((slot) => {
    link.setAttribute('href', base + slot + '/?theme=' + catalogScheme());
  });
}

function wireCatalogLinks() {
  const links = document.querySelectorAll(CATALOG_LINK_SELECTOR);
  if (!links.length) return;
  links.forEach(pointCatalogLink);
  if (window.__catalogThemeObserver) return;
  // Material switches the palette by rewriting this attribute on <body>.
  window.__catalogThemeObserver = new MutationObserver(() => {
    document.querySelectorAll(CATALOG_LINK_SELECTOR).forEach(pointCatalogLink);
  });
  window.__catalogThemeObserver.observe(document.body, {
    attributes: true,
    attributeFilter: ['data-md-color-scheme'],
  });
}

if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(wireCatalogLinks);
} else {
  document.addEventListener('DOMContentLoaded', wireCatalogLinks);
}
