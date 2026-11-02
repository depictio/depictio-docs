/* Template pages embed the template's live dashboard from
   showcases.depictio.embl.org. Templates with several showcase runs (viralrecon
   Illumina and Nanopore, the variantbenchmarking categories) get one button per
   run; a click repoints the iframe and the Open link.

   navigation.instant is on, so the wiring runs on every page swap through
   document$ rather than once on DOMContentLoaded.

   When the showcase server cannot be reached, the frame gives way to the
   page's first dashboard screenshot. The probe loads the viewer's favicon: an
   image request needs no CORS, and an error page fails it like a dead host. */
const PROBE_TIMEOUT_MS = 8000;

function probeShowcase(src) {
  return new Promise((resolve) => {
    const img = new Image();
    const done = (ok) => {
      clearTimeout(timer);
      resolve(ok);
    };
    const timer = setTimeout(() => done(false), PROBE_TIMEOUT_MS);
    img.onload = () => done(true);
    img.onerror = () => done(false);
    img.src = new URL('/dashboard/favicon.svg', src).href;
  });
}

function showScreenshot(box, frame) {
  const shots = [...document.querySelectorAll('.tpl-shot img')];
  const light = shots.find((img) => img.getAttribute('src').endsWith('#only-light'));
  const dark = shots.find((img) => img.getAttribute('src').endsWith('#only-dark'));
  const picks = light || dark ? [light, dark].filter(Boolean) : shots.slice(0, 1);
  if (!picks.length) return;
  const fallback = document.createElement('div');
  fallback.className = 'tpl-showcase-fallback';
  picks.forEach((img) => {
    const copy = img.cloneNode();
    copy.removeAttribute('loading');
    fallback.appendChild(copy);
  });
  frame.replaceWith(fallback);
  box.classList.add('is-offline');
  box.querySelector('.tpl-showcase-label').textContent = 'Showcase offline, screenshot';
}

function initTemplateShowcase() {
  document.querySelectorAll('.tpl-showcase').forEach((box) => {
    const frame = box.querySelector('.tpl-showcase-frame');
    const open = box.querySelector('.tpl-showcase-open');
    probeShowcase(frame.src).then((ok) => ok || showScreenshot(box, frame));
    box.querySelectorAll('.tpl-showcase-run').forEach((btn) => {
      btn.addEventListener('click', () => {
        box.querySelectorAll('.tpl-showcase-run').forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        frame.src = btn.dataset.src;
        open.href = btn.dataset.src;
      });
    });
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(initTemplateShowcase);
} else {
  document.addEventListener('DOMContentLoaded', initTemplateShowcase);
}
