// Tools Catalog embed: load the catalog site of the documented version.
//
// The catalog is its own static site (depictio/depictio-catalog), one
// directory per release plus latest/. The page's iframe carries the version it
// documents (hooks/catalog_site.py); this picks that directory when the site
// still keeps it (versions.json) and latest/ otherwise, passes the docs theme
// as ?theme=, and follows the palette toggle.

const CATALOG_SITE_SELECTOR = 'iframe[data-catalog-site]';

function catalogScheme() {
  return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
}

function catalogSlotFor(frame) {
  const base = frame.dataset.catalogSite;
  const wanted = frame.dataset.catalogVersion;
  if (!frame.__catalogSlot) {
    frame.__catalogSlot = fetch(base + 'versions.json', { cache: 'no-cache' })
      .then((r) => (r.ok ? r.json() : { versions: [] }))
      .then((v) => ((v.versions || []).includes(wanted) ? wanted : 'latest'))
      .catch(() => 'latest');
  }
  return frame.__catalogSlot;
}

function catalogSrc(frame, slot) {
  // The deep link (#tool=..., #output=...) of this docs URL rides along.
  const hash = window.location.hash.match(/^#(tool|output)=/) ? window.location.hash : '';
  return frame.dataset.catalogSite + slot + '/?theme=' + catalogScheme() + hash;
}

function loadCatalogFrame(frame) {
  catalogSlotFor(frame).then((slot) => {
    const src = catalogSrc(frame, slot);
    if (frame.getAttribute('src') !== src) frame.setAttribute('src', src);
    const open = frame.closest('.catalog-embed')?.querySelector('.catalog-open-link');
    if (open) open.setAttribute('href', src);
  });
}

function wireCatalogSite() {
  const frames = document.querySelectorAll(CATALOG_SITE_SELECTOR);
  if (!frames.length) return;
  frames.forEach(loadCatalogFrame);
  if (window.__catalogThemeObserver) return;
  // Material switches the palette by rewriting this attribute on <body>.
  window.__catalogThemeObserver = new MutationObserver(() => {
    document.querySelectorAll(CATALOG_SITE_SELECTOR).forEach(loadCatalogFrame);
  });
  window.__catalogThemeObserver.observe(document.body, {
    attributes: true,
    attributeFilter: ['data-md-color-scheme'],
  });
}

if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(wireCatalogSite);
} else {
  document.addEventListener('DOMContentLoaded', wireCatalogSite);
}
