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
  return {
    href: card.getAttribute('href'),
    name: card.dataset.tplName || '',
    status: card.dataset.tplStatus || '',
    version: card.dataset.tplVersion || '',
    keywords: card.dataset.tplKeywords || '',
    description: card.querySelector('.template-card-desc')?.textContent.trim() || '',
  };
}

/* Statuses sort by trust rather than alphabetically, which is the order the
   status-levels section explains them in. */
const TPL_STATUS_RANK = { certified: 0, reviewed: 1, experimental: 2 };

function tplCompareVersions(a, b) {
  const parse = (v) => v.split('.').map((part) => parseInt(part, 10) || 0);
  const [x, y] = [parse(a), parse(b)];
  for (let i = 0; i < Math.max(x.length, y.length); i += 1) {
    const diff = (x[i] || 0) - (y[i] || 0);
    if (diff) return diff;
  }
  return 0;
}

function tplBuildTable(container, cards) {
  const rows = cards
    .map((card) => {
      const f = tplCardFields(card);
      const icon = TPL_STATUS_ICON[f.status] || 'mdi-help-circle-outline';
      return `<tr data-tpl-row="${f.name}">
        <td class="tpl-table-name"><a href="${f.href}">${f.name}</a></td>
        <td class="tpl-table-desc">${f.description}</td>
        <td class="tpl-table-version"><span class="template-version">v${f.version}</span></td>
        <td class="tpl-table-status">
          <span class="template-status-${f.status}"><i class="mdi ${icon}"></i> ${f.status}</span>
        </td>
      </tr>`;
    })
    .join('');
  container.innerHTML = `<table>
    <thead><tr>
      <th><button type="button" class="tpl-sort" data-tpl-sort="name">Template <i class="mdi mdi-unfold-more-horizontal"></i></button></th>
      <th>What it covers</th>
      <th><button type="button" class="tpl-sort" data-tpl-sort="version">Version <i class="mdi mdi-unfold-more-horizontal"></i></button></th>
      <th><button type="button" class="tpl-sort" data-tpl-sort="status">Status <i class="mdi mdi-unfold-more-horizontal"></i></button></th>
    </tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function tplWireSort(table, cards) {
  const body = table.querySelector('tbody');
  const fields = new Map(cards.map((card) => [card.dataset.tplName, tplCardFields(card)]));
  let key = null;
  let ascending = true;

  const compare = (a, b) => {
    const [x, y] = [fields.get(a.dataset.tplRow), fields.get(b.dataset.tplRow)];
    if (!x || !y) return 0;
    if (key === 'version') return tplCompareVersions(x.version, y.version);
    if (key === 'status') return (TPL_STATUS_RANK[x.status] ?? 9) - (TPL_STATUS_RANK[y.status] ?? 9);
    return x.name.localeCompare(y.name);
  };

  table.querySelectorAll('[data-tpl-sort]').forEach((button) => {
    button.addEventListener('click', () => {
      const next = button.dataset.tplSort;
      ascending = next === key ? !ascending : true;
      key = next;
      table.querySelectorAll('[data-tpl-sort]').forEach((other) => {
        const active = other === button;
        other.classList.toggle('is-active', active);
        const icon = other.querySelector('.mdi');
        if (icon) {
          icon.className = active
            ? `mdi ${ascending ? 'mdi-arrow-up' : 'mdi-arrow-down'}`
            : 'mdi mdi-unfold-more-horizontal';
        }
      });
      const sorted = Array.from(body.children).sort(compare);
      if (!ascending) sorted.reverse();
      sorted.forEach((row) => body.appendChild(row));
    });
  });
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
  tplWireSort(table, cards);
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
