/* Videos that play only once they are on screen.

   A page embeds one with

     <video data-autoplay controls muted loop playsinline preload="none" poster="…" src="…">

   preload="none" keeps the browser from fetching the clip with the page, so a
   page shows posters until a clip scrolls into view: it then downloads and
   plays, and pauses again once off screen. Without JavaScript the poster and
   the controls remain, and a click plays it. */
(function () {
  const SELECTOR = 'video[data-autoplay]';
  let observer = null;

  function watch() {
    if (!('IntersectionObserver' in window)) return;
    if (!observer) {
      observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          const video = entry.target;
          if (entry.isIntersecting) {
            const played = video.play();
            if (played && played.catch) played.catch(function () {});
          } else if (!video.paused) {
            video.pause();
          }
        });
      }, { threshold: 0.4 });
    }
    document.querySelectorAll(SELECTOR).forEach(function (video) { observer.observe(video); });
  }

  // Material's instant navigation swaps the page content without a reload.
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(watch);
  else document.addEventListener('DOMContentLoaded', watch);
})();
