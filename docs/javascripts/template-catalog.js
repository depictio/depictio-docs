/* Two views over the template catalogue: the card grid, and a compact table for
   scanning many templates at once. Both are driven by the same search box and
   status filter, and the table is built from the cards so the page has a single
   source of truth for what a template is.

   navigation.instant is on, so the wiring runs through document$. */
const TPL_STATUS_ICON = {
  certified: 'mdi-shield-check',
  reviewed: 'mdi-check-circle-outline',
  experimental: 'mdi-flask-outline',
};

function tplCardFields(card) {
  const logos = card.querySelector('.template-card-logo');
  return {
    href: card.getAttribute('href'),
    name: card.dataset.tplName || '',
    status: card.dataset.tplStatus || '',
    version: card.dataset.tplVersion || '',
    keywords: card.dataset.tplKeywords || '',
    description: card.querySelector('.template-card-desc')?.textContent.trim() || '',
    logo: logos ? logos.innerHTML : '',
  };
}

function tplBuildTable(container, cards) {
  const rows = cards
    .map((card) => {
      const f = tplCardFields(card);
      const icon = TPL_STATUS_ICON[f.status] || 'mdi-help-circle-outline';
      return `<tr data-tpl-row="${f.name}">
        <td class="tpl-table-name">
          <a href="${f.href}"><span class="tpl-table-logo">${f.logo}</span><code>${f.name}</code></a>
        </td>
        <td class="tpl-table-desc">${f.description}</td>
        <td class="tpl-table-version"><span class="template-version">v${f.version}</span></td>
        <td class="tpl-table-status">
          <span class="template-status-${f.status}"><i class="mdi ${icon}"></i> ${f.status}</span>
        </td>
      </tr>`;
    })
    .join('');
  container.innerHTML = `<table>
    <thead><tr><th>Template</th><th>What it covers</th><th>Version</th><th>Status</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function initTemplateCatalog() {
  const root = document.querySelector('[data-tpl-catalog]');
  if (!root || root.dataset.wired === 'on') return;
  root.dataset.wired = 'on';

  const cards = Array.from(root.querySelectorAll('.template-card'));
  const table = root.querySelector('[data-tpl-table]');
  const grid = root.querySelector('[data-tpl-grid]');
  const search = root.querySelector('[data-tpl-search]');
  const empty = root.querySelector('[data-tpl-empty]');
  if (!cards.length || !table || !grid) return;

  tplBuildTable(table, cards);
  const rows = new Map(
    Array.from(table.querySelectorAll('[data-tpl-row]')).map((row) => [row.dataset.tplRow, row]),
  );

  let status = 'all';

  const filter = () => {
    const query = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    cards.forEach((card) => {
      const f = tplCardFields(card);
      const haystack = `${f.name} ${f.description} ${f.keywords} ${f.version}`.toLowerCase();
      const match = (status === 'all' || f.status === status) && (!query || haystack.includes(query));
      card.hidden = !match;
      const row = rows.get(f.name);
      if (row) row.hidden = !match;
      if (match) shown += 1;
    });
    if (empty) empty.hidden = shown > 0;
  };

  search?.addEventListener('input', filter);

  root.querySelectorAll('[data-tpl-status]').forEach((chip) => {
    chip.addEventListener('click', () => {
      status = chip.dataset.tplStatus;
      root.querySelectorAll('[data-tpl-status]').forEach((other) => {
        other.classList.toggle('is-active', other === chip);
      });
      filter();
    });
  });

  const setView = (view) => {
    grid.hidden = view !== 'grid';
    table.hidden = view !== 'table';
    root.querySelectorAll('[data-tpl-view]').forEach((button) => {
      button.classList.toggle('is-active', button.dataset.tplView === view);
    });
    try {
      localStorage.setItem('depictio-template-view', view);
    } catch (error) {
      /* private browsing: the choice just does not persist */
    }
  };

  root.querySelectorAll('[data-tpl-view]').forEach((button) => {
    button.addEventListener('click', () => setView(button.dataset.tplView));
  });

  let stored = null;
  try {
    stored = localStorage.getItem('depictio-template-view');
  } catch (error) {
    stored = null;
  }
  setView(stored === 'table' ? 'table' : 'grid');
  filter();
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(initTemplateCatalog);
} else {
  document.addEventListener('DOMContentLoaded', initTemplateCatalog);
}
