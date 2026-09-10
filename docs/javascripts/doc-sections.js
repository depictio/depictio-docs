/* Two small enhancements that Markdown alone cannot express.

   1. Icons in the table of contents. Headings carry a Material icon, but the
      toc extension strips markup from the titles it builds, so the entries
      arrive as plain text. Each entry gets its heading's icon cloned back in.

   2. Collapsible sections on template pages. Every `##` becomes a toggle that
      folds away everything up to the next `##`, so a long template page can be
      skimmed section by section. Sections start open.

   navigation.instant is on, so both run on every page swap through document$
   rather than once on DOMContentLoaded. */

const CHEVRON =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">' +
  '<path d="M7.41 8.59 12 13.17l4.59-4.58L18 10l-6 6-6-6z"/></svg>';

/* Template pages are long. Only the two sections a reader almost always wants
   start open; the rest fold away until asked for. */
const OPEN_BY_DEFAULT = new Set(['quick-start', 'dashboard-tabs']);

function articleRoot() {
  return document.querySelector('article.md-content__inner') || document.querySelector('.md-content__inner');
}

function injectTocIcons() {
  // navigation.instant rewrites table-of-contents hrefs to absolute URLs, so
  // the fragment comes off the link's `hash` rather than its href attribute.
  const links = document.querySelectorAll('.md-nav--secondary .md-nav__link');
  links.forEach((link) => {
    if (!link.hash || link.querySelector('.toc-icon')) return;
    const heading = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (!heading) return;
    const source = heading.firstElementChild;
    if (!source || !source.classList.contains('twemoji')) return;
    const icon = source.cloneNode(true);
    icon.classList.add('toc-icon');
    icon.setAttribute('aria-hidden', 'true');
    const target = link.querySelector('.md-ellipsis') || link;
    target.insertBefore(icon, target.firstChild);
  });
}

function setSection(heading, open) {
  const body = heading.nextElementSibling;
  if (!body || !body.classList.contains('doc-section-body')) return;
  body.hidden = !open;
  heading.classList.toggle('doc-section--collapsed', !open);
  const toggle = heading.querySelector('.doc-section-toggle');
  if (toggle) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', (open ? 'Collapse ' : 'Expand ') + heading.textContent.trim());
  }
}

function makeSectionsCollapsible() {
  const article = articleRoot();
  if (!article || !article.querySelector('.template-banner')) return;

  Array.from(article.children)
    .filter((el) => el.tagName === 'H2')
    .forEach((heading) => {
      if (heading.dataset.docSection === 'on') return;
      heading.dataset.docSection = 'on';

      // Everything between this heading and the next one moves into a wrapper
      // that can be hidden in one go.
      const body = document.createElement('div');
      body.className = 'doc-section-body';
      let node = heading.nextElementSibling;
      while (node && node.tagName !== 'H2') {
        const next = node.nextElementSibling;
        body.appendChild(node);
        node = next;
      }
      heading.after(body);

      const toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'doc-section-toggle';
      toggle.innerHTML = CHEVRON;
      heading.appendChild(toggle);

      heading.classList.add('doc-section-head');
      heading.addEventListener('click', (event) => {
        // The anchor link still copies a permalink rather than folding.
        if (event.target.closest('.headerlink')) return;
        setSection(heading, body.hidden);
      });
      setSection(heading, OPEN_BY_DEFAULT.has(heading.id));
    });
}

/* A link into a folded section opens it, otherwise the browser would jump to a
   heading with nothing under it. */
function revealHash(hash) {
  if (!hash) return;
  let target;
  try {
    target = document.querySelector(hash);
  } catch (error) {
    return;
  }
  if (!target) return;
  const body = target.closest('.doc-section-body');
  if (body && body.hidden) setSection(body.previousElementSibling, true);
}

function revealHashTarget() {
  revealHash(window.location.hash);
}

/* Material scrolls table-of-contents links through the History API, which does
   not fire hashchange, so the section has to be opened on the click itself. */
document.addEventListener(
  'click',
  (event) => {
    const link = event.target.closest && event.target.closest('a[href]');
    if (link && link.hash && link.pathname === window.location.pathname) revealHash(link.hash);
  },
  true,
);

function initDocSections() {
  makeSectionsCollapsible();
  injectTocIcons();
  revealHashTarget();
}

window.addEventListener('hashchange', revealHashTarget);

if (typeof document$ !== 'undefined') {
  document$.subscribe(initDocSections);
} else {
  document.addEventListener('DOMContentLoaded', initDocSections);
}
