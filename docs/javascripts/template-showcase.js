/* Template pages embed the template's live dashboard from
   showcases.depictio.embl.org. Templates with several showcase runs (viralrecon
   Illumina and Nanopore, the variantbenchmarking categories) get one button per
   run; a click repoints the iframe and the Open link.

   navigation.instant is on, so the wiring runs on every page swap through
   document$ rather than once on DOMContentLoaded. */
function initTemplateShowcase() {
  document.querySelectorAll('.tpl-showcase').forEach((box) => {
    const frame = box.querySelector('.tpl-showcase-frame');
    const open = box.querySelector('.tpl-showcase-open');
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
