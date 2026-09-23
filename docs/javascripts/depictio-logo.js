/* Site logo: the Depictio rose.

   Swaps the static logo (theme.logo, kept as the no-JS fallback) in the header
   and in the mobile navigation drawer for <depictio-rose mode="logo">, the mark
   drawn by depictio-rose.js. It rests on the logo shape; hovering it for a
   moment plays the fan, leaving puts it back.

   The home page hero gets the same treatment, one size up: its wordmark keeps
   the lettering and the mark is replaced by a rose running the endless
   clockwise sweep, so the logo turns instead of sitting still.

   navigation.instant replaces the header logo ([data-md-component=logo]) on
   every page swap, so the swap runs on each document$ emission rather than
   once on DOMContentLoaded. The same hook keeps the page-specific body classes
   that extra.css targets in step with the current page. */
(function () {
  const FAN_DELAY_MS = 400;
  /** The hero's resting animation: an endless clockwise wave around the mark. */
  const IDLE_MODE = 'sweep';

  // The body element survives instant navigation, so the class is recomputed
  // on every page view instead of only being added.
  function updatePageBodyClass() {
    document.body.classList.toggle('page-changelog', window.location.pathname.includes('/changelog'));
  }

  function setMode(rose, mode) {
    // Every attribute write restarts the animation, so only write on a change.
    if (rose.getAttribute('mode') !== mode) rose.setAttribute('mode', mode);
  }

  function wireFanOnHover(rose) {
    let timer = null;
    rose.addEventListener('mouseenter', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { setMode(rose, 'fan'); }, FAN_DELAY_MS);
    });
    rose.addEventListener('mouseleave', function () {
      clearTimeout(timer);
      timer = null;
      setMode(rose, 'logo');
    });
  }

  const LOGO_BUTTONS = '.md-header__button.md-logo, .md-nav__button.md-logo';

  function replaceLogo(button) {
    // Without the custom element (depictio-rose.js missing, or no Custom
    // Elements support) the static logo stays.
    const canSwap = window.customElements && customElements.get('depictio-rose');

    if (canSwap && !button.querySelector('depictio-rose')) {
      const rose = document.createElement('depictio-rose');
      rose.setAttribute('mode', 'logo');
      rose.setAttribute('label', '');  // the link around it already carries the site name
      wireFanOnHover(rose);

      // theme.logo renders an <img>; an <svg> is there when the logo was
      // inlined by an earlier script or comes from theme.icon.logo.
      const current = button.querySelector(':scope > img, :scope > svg');
      if (current) current.replaceWith(rose);
      else button.prepend(rose);
    }

    // extra.css keeps the logo transparent until this class is set, so the
    // static logo does not flash before the swap. Set it on every path.
    button.classList.add('logo-ready');
  }


  /* The hero wordmark (images/logo/logo_hd*.svg, 3600x809) draws the mark in
     its left quarter. These fractions of the rendered HEIGHT give the mark's
     centre and outer radius, measured on the asset; the lettering starts well
     after it, so hiding the left quarter hides the mark and nothing else.
     depictio/viewer/src/chrome/DepictioWordmark.tsx does the same for the
     app's copy of the same artwork. */
  const RASTER_W = 3600;
  const RASTER_H = 809;
  const MARK_CX = 0.582;
  const MARK_CY = 0.58;
  const MARK_R = 0.58;
  /* <depictio-rose> draws its circle (r = 300) inside a 640-wide viewBox. */
  const ROSE_BOX_PER_RADIUS = 640 / 300;

  /* Position the rose over whichever of the two theme images is on screen. */
  function placeHeroRose(wrap, rose) {
    const img = Array.prototype.find.call(
      wrap.querySelectorAll('img'),
      function (candidate) { return candidate.getBoundingClientRect().height > 0; }
    );
    if (!img) return;
    const w = img.clientWidth, h = img.clientHeight;
    if (!w || !h) return;
    const scale = Math.min(w / RASTER_W, h / RASTER_H);
    const drawnW = RASTER_W * scale, drawnH = RASTER_H * scale;
    const side = MARK_R * ROSE_BOX_PER_RADIUS * drawnH;
    rose.style.width = Math.round(side) + 'px';
    rose.style.height = Math.round(side) + 'px';
    rose.style.left = ((w - drawnW) / 2 + MARK_CX * drawnH - side / 2) + 'px';
    rose.style.top = ((h - drawnH) / 2 + MARK_CY * drawnH - side / 2) + 'px';
    wrap.classList.add('rose-ready');
  }

  function enhanceHeroLogo() {
    const wrap = document.querySelector('.hero-logo');
    if (!wrap) return;
    const canSwap = window.customElements && customElements.get('depictio-rose');
    if (!canSwap || wrap.querySelector('depictio-rose')) return;

    const rose = document.createElement('depictio-rose');
    rose.setAttribute('mode', IDLE_MODE);
    rose.setAttribute('label', '');  // the images already carry the alt text
    wrap.appendChild(rose);

    const place = function () { placeHeroRose(wrap, rose); };
    place();
    // The palette switch swaps which image is displayed, and a resize changes
    // the box, so the overlay is re-measured rather than placed once.
    if (window.ResizeObserver) new ResizeObserver(place).observe(wrap);
    window.addEventListener('load', place);
    new MutationObserver(place).observe(document.body, {
      attributes: true,
      attributeFilter: ['data-md-color-scheme'],
    });
  }

  function initDepictioHeader() {
    updatePageBodyClass();
    document.querySelectorAll(LOGO_BUTTONS).forEach(replaceLogo);
    enhanceHeroLogo();
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(initDepictioHeader);
  } else {
    document.addEventListener('DOMContentLoaded', initDepictioHeader);
  }
})();
