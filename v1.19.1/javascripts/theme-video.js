/* Videos recorded twice, once per colour scheme, played in one frame.

   A page embeds one with

     <iframe data-src-light="<player URL>" data-src-dark="<player URL>"></iframe>

   and no src: the frame gets the take matching the docs scheme, and the other
   take on each palette toggle. Two frames hidden by CSS would not do, as a
   browser loads a hidden iframe even when it is lazy, so both videos would
   download and play.

   Material stores the palette as data-md-color-scheme on <body>: 'slate' is
   the dark scheme, anything else is light. */
(function () {
  const SELECTOR = 'iframe[data-src-light][data-src-dark]';

  function currentScheme() {
    return document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'light';
  }

  // Assigning src reloads the frame, so it is only written when the take changes.
  function syncFrames() {
    const scheme = currentScheme();
    document.querySelectorAll(SELECTOR).forEach(function (iframe) {
      const src = scheme === 'dark' ? iframe.dataset.srcDark : iframe.dataset.srcLight;
      if (iframe.getAttribute('src') !== src) iframe.setAttribute('src', src);
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
      syncFrames();
    });
    paletteObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['data-md-color-scheme'],
    });
  }

  function init() {
    syncFrames();
    watchPalette();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(init);
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
