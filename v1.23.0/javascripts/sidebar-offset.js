/* Keep the sticky sidebars below the header. With navigation tabs the header
   is about 6rem tall, so the CSS reads its height from --dp-header-h instead of
   assuming 2.4rem. Updated when the header resizes (tabs wrapping, zoom). */
(function () {
  function apply() {
    const header = document.querySelector('.md-header');
    if (!header) return;
    const height = header.getBoundingClientRect().height;
    document.documentElement.style.setProperty('--dp-header-h', height + 'px');
  }
  function start() {
    apply();
    const header = document.querySelector('.md-header');
    if (header && 'ResizeObserver' in window) new ResizeObserver(apply).observe(header);
    window.addEventListener('resize', apply);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
