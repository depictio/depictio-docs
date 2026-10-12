/* Template pages ship one generated reference partial per template version.
   Rendering them as tabs put every version's headings in the table of contents
   three times over; a dropdown at the top of the page keeps one block visible
   and hides the table-of-contents entries belonging to the others, so the
   contents match what is on screen.

   navigation.instant is on, so the wiring runs on every page swap through
   document$ rather than once on DOMContentLoaded. */
function initTemplateVersionPicker() {
  const select = document.querySelector('.tpl-version-select');
  if (!select) return;
  const blocks = Array.from(document.querySelectorAll('.tpl-version-block'));
  if (!blocks.length) return;

  // Heading ids per block, resolved once: the partials are large and the
  // selection changes far more often than the page is built.
  const headingIds = new Map(
    blocks.map((block) => [
      block,
      Array.from(block.querySelectorAll('[id]')).map((el) => el.id),
    ]),
  );

  // The table of contents is rendered twice, once for the sidebar and once for
  // the drawer, so every id matches two entries. navigation.instant also
  // rewrites the hrefs to absolute URLs, hence matching on `hash`.
  const tocItems = (id) =>
    Array.from(document.querySelectorAll('.md-nav--secondary a'))
      .filter((link) => link.hash === `#${id}`)
      .map((link) => link.closest('.md-nav__item'))
      .filter(Boolean);

  const badge = document.querySelector('.tpl-version-badge');
  const latest = select.closest('.tpl-version-pick')?.dataset.latest;

  const apply = () => {
    if (badge) badge.hidden = select.value !== latest;
    blocks.forEach((block) => {
      const hidden = block.dataset.version !== select.value;
      block.hidden = hidden;
      headingIds.get(block).forEach((id) => {
        tocItems(id).forEach((item) => {
          item.hidden = hidden;
        });
      });
    });
  };

  select.addEventListener('change', apply);
  apply();
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(initTemplateVersionPicker);
} else {
  document.addEventListener('DOMContentLoaded', initTemplateVersionPicker);
}
