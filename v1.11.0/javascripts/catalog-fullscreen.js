// Page-fill "fullscreen" toggle for the component-catalog gallery embed.
// Toggles a fixed-position overlay class instead of the native Fullscreen API:
// the gallery fills the browser viewport (tab), not the whole screen.

// Icon paths (Material Design Icons): expand <-> collapse.
const CATALOG_FS_EXPAND = 'M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z';
const CATALOG_FS_COLLAPSE = 'M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z';

const CATALOG_FS_CLASS = 'catalog-embed--fs';
const CATALOG_FS_LOCK = 'catalog-fs-lock';

function activeCatalogEmbed() {
  return document.querySelector('.catalog-embed.' + CATALOG_FS_CLASS);
}

function setCatalogFullscreen(container, on) {
  container.classList.toggle(CATALOG_FS_CLASS, on);
  // Freeze the page behind the overlay while it is open.
  document.body.classList.toggle(CATALOG_FS_LOCK, on);
  const button = container.querySelector('.catalog-fs-btn');
  if (!button) return;
  const icon = button.querySelector('svg path');
  if (icon) icon.setAttribute('d', on ? CATALOG_FS_COLLAPSE : CATALOG_FS_EXPAND);
  button.setAttribute('title', on ? 'Exit fullscreen' : 'Toggle fullscreen');
  button.setAttribute('aria-label', on ? 'Exit fullscreen' : 'Toggle fullscreen');
}

function toggleCatalogFullscreen(el) {
  const container = el.closest('.catalog-embed');
  if (!container) return;
  const active = activeCatalogEmbed();
  if (active && active !== container) setCatalogFullscreen(active, false);
  setCatalogFullscreen(container, !container.classList.contains(CATALOG_FS_CLASS));
}

// Expose for the inline onclick handlers (kept global like the live demo).
window.toggleCatalogFullscreen = toggleCatalogFullscreen;

// ESC exits the overlay (the native API gave this for free; replicate it).
function wireCatalogFs() {
  if (window.__catalogFsWired) return;
  window.__catalogFsWired = true;
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    const active = activeCatalogEmbed();
    if (active) setCatalogFullscreen(active, false);
  });
}

function resetCatalogFs() {
  // Material instant navigation swaps the page content: drop a stale scroll
  // lock if the user navigated away while the overlay was open.
  document.body.classList.remove(CATALOG_FS_LOCK);
  wireCatalogFs();
}

if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(resetCatalogFs);
} else {
  document.addEventListener('DOMContentLoaded', resetCatalogFs);
}
