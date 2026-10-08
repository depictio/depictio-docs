/* Terminal recordings, played by asciinema-player (loaded from jsDelivr in
   mkdocs.yml) from .cast files kept in this repository under assets/casts/.

   A page embeds one with

     <div class="asciinema-cast" data-cast="assets/casts/<name>.cast"></div>

   where data-cast is relative to the docs root, so the same markup works on any
   page. It is resolved against the site root, which Material's #__config gives
   relative to the page first loaded: resolved once, here, it stays right on the
   pages navigation.instant swaps in afterwards, under /depictio-docs/, under a
   mike version prefix such as /depictio-docs/1.12/, and with `mkdocs serve`.

   Optional attributes: data-poster (default "npt:0:3", the frame shown before
   playing), data-theme (default "depictio", in stylesheets/asciinema.css) and
   data-idle-time-limit (seconds, default 1.5).

   navigation.instant is on, so players are mounted on every page swap through
   document$, and those of the page left behind are disposed of first. */
const SITE_ROOT = (() => {
  const config = document.getElementById('__config');
  const base = config ? JSON.parse(config.textContent).base : '.';
  return new URL(`${base}/`, window.location.href);
})();

let castPlayers = [];

function mountCasts() {
  castPlayers.forEach((player) => player.dispose());
  castPlayers = [];
  if (typeof AsciinemaPlayer === 'undefined') return;

  document.querySelectorAll('.asciinema-cast[data-cast]').forEach((el) => {
    const { cast, poster, theme, idleTimeLimit } = el.dataset;
    el.replaceChildren();
    castPlayers.push(
      AsciinemaPlayer.create(new URL(cast, SITE_ROOT).href, el, {
        fit: 'width',
        poster: poster || 'npt:0:3',
        theme: theme || 'depictio',
        idleTimeLimit: Number(idleTimeLimit) || 1.5,
      }),
    );
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(mountCasts);
} else {
  document.addEventListener('DOMContentLoaded', mountCasts);
}
