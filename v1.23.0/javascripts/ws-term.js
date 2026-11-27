/* Terminal blocks on the workshop pages.

   A ```console block (a `$ ` prompt, then the output) is drawn as a terminal,
   and each output line takes the colour the CLI prints it in, read from its
   first character: ✓ success, • information, ! warning, ✗ error, … elided.
   A ```diff block gets green added lines and red removed lines.
   Only the workshop pages are touched; the rest of the docs keeps its style.
*/
(function () {
  var KINDS = { '✓': 'ws-t-ok', '•': 'ws-t-info', '!': 'ws-t-warn', '✗': 'ws-t-err', '…': 'ws-t-dim' };

  /* Annotated code, as on the slides: a line ending in ` [[N]]` (N = 1..6) gets the
     band of group N and loses the marker; the first line of a group carries its number
     (drawn in CSS, so a copy of the block stays clean). The first numbered list or
     table right after the block becomes its legend, item i in the colour of group i. */
  var MARK = /\s*\[\[([1-6])\]\]\s*$/;

  function trimEnd(node, count) {
    var walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT), texts = [], t;
    while ((t = walker.nextNode())) texts.push(t);
    for (var i = texts.length - 1; i >= 0 && count > 0; i--) {
      var cut = Math.min(count, texts[i].data.length);
      texts[i].data = texts[i].data.slice(0, texts[i].data.length - cut);
      count -= cut;
    }
  }

  function annotate(block) {
    var code = block.querySelector('pre > code');
    if (!code || block.classList.contains('ws-ann') || code.textContent.indexOf(']]') === -1) return;
    var lines = [], cur = null;
    Array.prototype.slice.call(code.childNodes).forEach(function (n) {
      if (n.nodeType === 1 && n.tagName === 'A' && /^__codelineno/.test(n.id || '')) { cur = []; lines.push({ anchor: n, nodes: cur }); return; }
      if (cur) cur.push(n);
    });
    var seen = {}, found = false;
    lines.forEach(function (l) {
      var text = l.nodes.map(function (n) { return n.textContent; }).join('');
      var body = text.replace(/\n$/, ''), m = body.match(MARK);
      if (!m) return;
      found = true;
      var wrap = document.createElement('span');
      wrap.className = 'ws-ln ws-g' + m[1];
      if (!seen[m[1]]) { wrap.className += ' ws-gh'; wrap.setAttribute('data-n', m[1]); seen[m[1]] = true; }
      l.anchor.parentNode.insertBefore(wrap, l.nodes[0] || null);
      l.nodes.forEach(function (n) { wrap.appendChild(n); });
      var tail = /\n$/.test(text);
      if (tail) trimEnd(wrap, 1);
      trimEnd(wrap, m[0].length);
      if (tail) wrap.parentNode.insertBefore(document.createTextNode('\n'), wrap.nextSibling);
    });
    if (!found) return;
    block.classList.add('ws-ann');
    var host = block.closest('.highlight') || block;
    // A block inside a step of a list: its legend comes after the list.
    while (!host.nextElementSibling && host.parentElement && !host.parentElement.matches('article, .md-content__inner')) host = host.parentElement;
    var sib = host.nextElementSibling;
    for (var k = 0; sib && k < 3; k++, sib = sib.nextElementSibling) {
      if (sib.matches('ol, table, .md-typeset__scrollwrap')) { (sib.querySelector('table') || sib).classList.add('ws-ann-legend'); break; }
      if (sib.matches('h2, h3, .highlight, .admonition, details')) break;
    }
  }

  function init() {
    if (location.pathname.indexOf('/tutorials/workshop') === -1) return;
    document.querySelectorAll('.md-typeset .highlight').forEach(annotate);
    document.querySelectorAll('.md-typeset .highlight').forEach(function (block) {
      if (block.querySelector('.gi, .gd')) block.classList.add('ws-diff');
      if (!block.querySelector('.gp')) return;
      block.classList.add('ws-term');
      block.querySelectorAll('.go').forEach(function (line) {
        var text = line.textContent.replace(/^\s+/, '');
        var kind = KINDS[text.charAt(0)];
        if (kind) line.classList.add(kind);
      });
    });
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(init);
  } else {
    document.addEventListener('DOMContentLoaded', init);
  }
})();
