/* Keeps embedded Depictio viewers in the docs colour scheme.

   Contract with the viewer, for every iframe[data-depictio-embed]:
   - at boot the viewer reads ?theme=dark|light from its URL, so the frame URL
     carries the scheme the page had when the frame was set up;
   - afterwards it re-themes live on a message from its parent frame,
       { type: 'depictio:set-color-scheme', scheme: 'dark' | 'light' },
     posted to the viewer's own origin. It is sent on each frame load and on
     each palette toggle, so the frame follows the toggle without reloading.

   Material stores the palette as data-md-color-scheme on <body>: 'slate' is
   the dark scheme, anything else is light. */
(function () {
  const MESSAGE_TYPE = 'depictio:set-color-scheme';
  const SELECTOR = 'iframe[data-depictio-embed]';

  function currentScheme() {
    return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
  }

  function postScheme(iframe, scheme) {
    try {
      iframe.contentWindow.postMessage({ type: MESSAGE_TYPE, scheme: scheme }, new URL(iframe.src).origin);
    } catch (e) {
      // No window yet, or a src with no origin to target: the next load posts again.
    }
  }

  // Assigning src reloads the frame, so it is only written when the value changes.
  function syncSrcTheme(iframe, scheme) {
    let url;
    try {
      url = new URL(iframe.src);
    } catch (e) {
      return;
    }
    if (url.searchParams.get('theme') === scheme) return;
    url.searchParams.set('theme', scheme);
    iframe.src = url.toString();
  }

  function scanEmbeds() {
    const scheme = currentScheme();
    document.querySelectorAll(SELECTOR).forEach(function (iframe) {
      if (iframe.dataset.depictioThemeSync) return;
      iframe.dataset.depictioThemeSync = 'bound';
      // Bound before src changes, so the load that change triggers is caught.
      iframe.addEventListener('load', function () { postScheme(iframe, currentScheme()); });
      syncSrcTheme(iframe, scheme);
    });
  }

  // <body> survives instant navigation, so a single observer covers every page.
  let paletteObserver = null;
  function watchPalette() {
    if (paletteObserver) return;
    let lastScheme = currentScheme();
    paletteObserver = new MutationObserver(function () {
      const scheme = currentScheme();
      if (scheme === lastScheme) return;
      lastScheme = scheme;
      document.querySelectorAll(SELECTOR).forEach(function (iframe) { postScheme(iframe, scheme); });
    });
    paletteObserver.observe(document.body, { attributes: true, attributeFilter: ['data-md-color-scheme'] });
  }

  function initThemeSync() {
    watchPalette();
    scanEmbeds();
  }

  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(initThemeSync);
  } else {
    document.addEventListener('DOMContentLoaded', initThemeSync);
  }
})();
