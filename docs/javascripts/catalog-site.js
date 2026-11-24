// Tools Catalog window: the live catalog site of the documented version.
//
// The catalog is its own static site (depictio/depictio-catalog), one
// directory per release plus latest/. The iframe and the "Open the full
// catalog" link carry the version the page documents (hooks/catalog_site.py);
// this picks that directory when the site still keeps it (versions.json) and
// latest/ otherwise, shows which one in the version chip, passes the docs
// theme as ?theme=, and follows the palette toggle.

const CATALOG_SELECTOR = 'iframe[data-catalog-site], a[data-catalog-site]';

function catalogScheme() {
  return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
}

const catalogSlots = {};

function catalogSlotFor(base, wanted) {
  const key = base + '|' + wanted;
  if (!catalogSlots[key]) {
    // A slow or failing versions.json must not leave the window blank.
    const signal = typeof AbortSignal !== 'undefined' && AbortSignal.timeout
      ? AbortSignal.timeout(5000) : undefined;
    catalogSlots[key] = fetch(base + 'versions.json', { cache: 'no-cache', signal })
      .then((r) => (r.ok ? r.json() : {}))
      .then((v) => (Array.isArray(v.versions) && v.versions.includes(wanted) ? wanted : 'latest'))
      .catch(() => 'latest');
  }
  return catalogSlots[key];
}

// Where the reader is inside the catalog (#tool=..., #output=...), so a theme
// switch reloads the same view. Readable only from the same origin, which is
// the case on depictio.github.io; anywhere else, the docs URL's own hash.
function catalogHash(frame) {
  try {
    const inner = frame && frame.contentWindow && frame.contentWindow.location.hash;
    if (inner) return inner;
  } catch (e) {
    // cross-origin (local preview): fall through
  }
  return window.location.hash.match(/^#(tool|output)=/) ? window.location.hash : '';
}

function pointCatalog(el) {
  const base = el.dataset.catalogSite;
  catalogSlotFor(base, el.dataset.catalogVersion).then((slot) => {
    const isFrame = el.tagName === 'IFRAME';
    const url = base + slot + '/?theme=' + catalogScheme() + catalogHash(isFrame ? el : null);
    if (isFrame) {
      // An unchanged src is left alone so instant navigation does not reload it.
      if (el.getAttribute('src') !== url) el.setAttribute('src', url);
    } else {
      el.setAttribute('href', url);
    }
    const label = el.closest('.catalog-window')?.querySelector('[data-catalog-version-label]');
    if (label) label.textContent = slot;
  });
}

function wireCatalog() {
  const els = document.querySelectorAll(CATALOG_SELECTOR);
  if (!els.length) return;
  els.forEach(pointCatalog);
  if (window.__catalogThemeObserver) return;
  // Material switches the palette by rewriting this attribute on <body>.
  window.__catalogThemeObserver = new MutationObserver(() => {
    document.querySelectorAll(CATALOG_SELECTOR).forEach(pointCatalog);
  });
  window.__catalogThemeObserver.observe(document.body, {
    attributes: true,
    attributeFilter: ['data-md-color-scheme'],
  });
}

if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(wireCatalog);
} else {
  document.addEventListener('DOMContentLoaded', wireCatalog);
}
