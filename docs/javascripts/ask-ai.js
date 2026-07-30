/* Ask-the-docs widget.
 *
 * Mounts once, directly on <body>. Material's instant navigation swaps the
 * contents of .md-content, so anything appended to <body> survives a page
 * change — which means the conversation survives clicking a citation, and that
 * is the whole point: read the cited section, come back, ask the follow-up.
 *
 * Answers are rendered with textContent, never innerHTML. The worker already
 * strips links and refuses an answer that still contains one, but the client
 * should not be the thing that trusts it.
 */

// Set after the first `wrangler deploy`; keep it stable, because every mike
// version deployed from here on bakes in whatever this says.
const ASKAI_ENDPOINT = 'https://depictio-docs-ai.weber8thomas.workers.dev';
const ASKAI_SOFT_LIMIT = 20;

function askaiCid() {
  let cid = localStorage.getItem('askai:cid');
  if (!cid) {
    cid = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    localStorage.setItem('askai:cid', cid);
  }
  return cid;
}

const quotaKey = () => 'askai:' + new Date().toISOString().slice(0, 10);
const quotaUsed = () => parseInt(localStorage.getItem(quotaKey()) || '0', 10);

/** The mike version from the path: /depictio-docs/<version>/...
 *  Empty when there is no version segment — `mkdocs serve` locally, or any
 *  deployment that isn't versioned. */
function docsVersion() {
  const parts = location.pathname.split('/').filter(Boolean);
  return parts.length > 1 ? parts[1] : '';
}

/** Is the reader on a pinned older version? Only then is the notice true.
 *  Anything that doesn't look like a mike directory (including no version at
 *  all) is treated as current, so the widget still works during local
 *  development. */
function isStaleVersion(version) {
  if (!version || version === 'stable' || version === 'latest') return false;
  return /^v?\d/.test(version) || version === 'beta';
}

function el(tag, attrs, text) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === 'class') node.className = v;
    else node.setAttribute(k, v);
  }
  if (text) node.textContent = text;
  return node;
}

/* Only two markdown constructs are rendered: fenced blocks and inline code.
   Everything else stays literal text. That keeps the XSS surface at zero
   without pulling in a markdown parser. */
function renderAnswer(target, text) {
  text.split('```').forEach((part, i) => {
    if (i % 2 === 1) {
      const pre = el('pre', { class: 'askai-code' });
      pre.appendChild(el('code', {}, part.replace(/^[a-z]*\n/i, '')));
      target.appendChild(pre);
      return;
    }
    part.split(/(`[^`]+`)/).forEach((piece) => {
      if (!piece) return;
      if (piece.startsWith('`') && piece.endsWith('`') && piece.length > 2) {
        target.appendChild(el('code', {}, piece.slice(1, -1)));
      } else {
        target.appendChild(document.createTextNode(piece));
      }
    });
  });
}

function mountAskAi() {
  if (window.__askAiMounted) return;
  if (/^REPLACE/.test(ASKAI_ENDPOINT)) return;
  window.__askAiMounted = true;

  const fab = el('button', {
    type: 'button',
    id: 'askai-fab',
    class: 'askai-fab',
    'aria-expanded': 'false',
    'aria-controls': 'askai-panel',
    'aria-label': 'Ask a question about the Depictio documentation',
  });
  // Reuse the real mark rather than approximating it: a hand-drawn pinwheel at
  // this size reads as a flower. The header <img> already carries a correctly
  // resolved src for whatever page and mike version we are on, and .src gives
  // it back absolute, so it stays valid across instant navigation.
  const icon = el('span', { class: 'askai-fab__icon' });
  const logo = document.querySelector('.md-logo img');
  if (logo && logo.src) {
    icon.appendChild(el('img', { src: logo.src, alt: '', 'aria-hidden': 'true' }));
  }
  fab.append(icon, el('span', { class: 'askai-fab__label' }, 'Ask the docs'));

  const panel = el('section', {
    id: 'askai-panel',
    class: 'askai-panel',
    role: 'dialog',
    'aria-modal': 'false',
    'aria-label': 'Ask the Depictio documentation',
    hidden: '',
  });

  const head = el('header', { class: 'askai-panel__head' });
  head.appendChild(el('h3', { id: 'askai-title' }, 'Ask the docs'));
  const close = el('button', { type: 'button', class: 'askai-panel__close', 'aria-label': 'Close' }, '✕');
  head.appendChild(close);

  const notice = el('p', { class: 'askai-notice', hidden: '' });
  const log = el('div', { id: 'askai-log', class: 'askai-log', 'aria-live': 'polite' });
  log.appendChild(
    el(
      'p',
      { class: 'askai-msg askai-msg--bot' },
      'Ask me about installing, configuring or using Depictio. I answer from this ' +
        'documentation and link to the sections I used.'
    )
  );

  const form = el('form', { class: 'askai-form' });
  const input = el('input', {
    type: 'text',
    class: 'askai-input',
    maxlength: '400',
    autocomplete: 'off',
    placeholder: 'e.g. how do I filter across data collections?',
    'aria-label': 'Your question',
  });
  const send = el('button', { type: 'submit', class: 'askai-send', 'aria-label': 'Send' }, '→');
  form.append(input, send);

  const quota = el('p', { class: 'askai-quota' });

  panel.append(head, notice, log, form, quota);
  document.body.append(fab, panel);

  let busy = false;

  const refreshQuota = () => {
    const left = Math.max(0, ASKAI_SOFT_LIMIT - quotaUsed());
    quota.textContent = left + (left === 1 ? ' question left today' : ' questions left today');
  };

  const addMsg = (text, kind) => {
    const p = el('p', { class: 'askai-msg askai-msg--' + kind });
    if (kind === 'bot') renderAnswer(p, text);
    else p.textContent = text;
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
    return p;
  };

  const addSources = (sources) => {
    if (!sources || !sources.length) return;
    const wrap = el('p', { class: 'askai-sources' });
    for (const s of sources) {
      // Same-origin check on top of the worker's mapping: a citation should
      // only ever point back into these docs.
      if (!s || !s.url || s.url.indexOf(location.origin) !== 0) continue;
      wrap.appendChild(el('a', { class: 'askai-source', href: s.url }, s.title || 'Source'));
    }
    if (wrap.childNodes.length) {
      log.appendChild(wrap);
      log.scrollTop = log.scrollHeight;
    }
  };

  const open = (yes) => {
    panel.hidden = !yes;
    fab.setAttribute('aria-expanded', String(yes));
    if (yes) {
      refreshQuota();
      setTimeout(() => input.focus(), 50);
    } else {
      fab.focus();
    }
  };

  fab.addEventListener('click', () => open(panel.hidden));
  close.addEventListener('click', () => open(false));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !panel.hidden) open(false);
    // Material owns "/" for search, so the toggle is on the slash chord.
    if ((e.metaKey || e.ctrlKey) && e.key === '/') {
      e.preventDefault();
      open(panel.hidden);
    }
    if (e.key !== 'Tab' || panel.hidden) return;
    // Focus trap, required by role="dialog".
    const focusables = panel.querySelectorAll('button, input, a[href]');
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question || busy) return;

    busy = true;
    send.disabled = true;
    input.value = '';
    addMsg(question, 'user');
    const typing = addMsg('…', 'typing');

    try {
      const r = await fetch(ASKAI_ENDPOINT + '/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          page: location.pathname,
          version: docsVersion(),
          cid: askaiCid(),
        }),
      });
      const data = await r.json();
      typing.remove();
      if (r.ok && data.answer) {
        addMsg(data.answer, 'bot');
        addSources(data.sources);
        localStorage.setItem(quotaKey(), String(quotaUsed() + 1));
        refreshQuota();
      } else {
        addMsg(data.error || 'Something went wrong. Please try again.', 'err');
      }
    } catch {
      typing.remove();
      addMsg('Could not reach the assistant. Please try again in a moment.', 'err');
    } finally {
      busy = false;
      send.disabled = false;
      input.focus();
    }
  });

  window.__askAiRefresh = () => {
    // The index tracks one version of the docs. On a pinned older one, say so
    // rather than answering from the latest as though it were what's on screen.
    const version = docsVersion();
    const stale = isStaleVersion(version);
    fab.hidden = version === '404.html';
    notice.hidden = !stale;
    if (stale) {
      notice.textContent =
        'Answers come from the latest documentation. You are reading ' +
        version +
        ', so some details may differ.';
    }
    refreshQuota();
  };
  window.__askAiRefresh();
}

function onPage() {
  mountAskAi();
  // The widget itself is never rebuilt — only the per-page state is refreshed.
  if (window.__askAiRefresh) window.__askAiRefresh();
}

if (typeof document$ !== 'undefined' && document$.subscribe) {
  document$.subscribe(onPage);
} else {
  document.addEventListener('DOMContentLoaded', onPage);
}
