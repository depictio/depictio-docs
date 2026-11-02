/* A sidebar group whose title is its own page (navigation.indexes) normally
   keeps a chevron that collapses it. The Genome browser group is meant to stay
   open: the title opens the overview and the examples stay listed below. Marking
   it here lets the stylesheet drop the chevron.

   navigation.instant swaps the page without a reload, so the marking runs on
   every page change through document$ rather than once on DOMContentLoaded. */
const PINNED_NAV_GROUPS = ['Genome browser'];

function pinNavGroups() {
  document
    .querySelectorAll('.md-nav--primary .md-nav__item--nested > .md-nav__container > a')
    .forEach((link) => {
      if (!PINNED_NAV_GROUPS.includes(link.textContent.trim())) return;
      const group = link.closest('.md-nav__item--nested');
      group.classList.add('nav-pinned');
      const toggle = group.querySelector(':scope > .md-nav__toggle');
      if (toggle) toggle.checked = true;
    });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(pinNavGroups);
} else {
  document.addEventListener('DOMContentLoaded', pinNavGroups);
}
