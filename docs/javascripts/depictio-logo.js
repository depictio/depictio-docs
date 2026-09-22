/* Site logo: the Depictio rose.

   Swaps the static logo (theme.logo, kept as the no-JS fallback) in the header
   and in the mobile navigation drawer for <depictio-rose mode="logo">, the mark
   drawn by depictio-rose.js. It rests on the logo shape; hovering it for a
   moment plays the fan, leaving puts it back.

   navigation.instant replaces the header logo ([data-md-component=logo]) on
   every page swap, so the swap runs on each document$ emission rather than
   once on DOMContentLoaded. The same hook keeps the page-specific body classes
   that extra.css targets in step with the current page. */
(function () {
  const FAN_DELAY_MS = 400;

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

  function initDepictioHeader() {
    updatePageBodyClass();
    document.querySelectorAll(LOGO_BUTTONS).forEach(replaceLogo);
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(initDepictioHeader);
  } else {
    document.addEventListener('DOMContentLoaded', initDepictioHeader);
  }
})();
