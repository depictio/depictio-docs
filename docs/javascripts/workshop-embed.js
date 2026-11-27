/* Workshop deck embedding. In an iframe (or with ?embed=1) a page drops the site
   header, tabs, sidebars and footer, so a slide shows only the lesson.
   ?only=<anchor> keeps one section: its heading and what follows, up to the next
   heading of the same or a higher level. */
(function () {
  var framed;
  try { framed = window.self !== window.top; } catch (e) { framed = true; }
  var embed = framed || new URLSearchParams(location.search).get("embed") === "1";
  if (!embed) return;
  document.documentElement.classList.add("ws-embed");

  function only() {
    var art = document.querySelector(".md-content__inner");
    if (!art) return;
    art.querySelectorAll(".ws-only-hide").forEach(function (el) { el.classList.remove("ws-only-hide"); });
    var id = new URLSearchParams(location.search).get("only");
    var head = id && document.getElementById(id);
    if (!head || head.parentElement !== art) return;
    var level = head.tagName, keep = false;
    Array.prototype.forEach.call(art.children, function (el) {
      if (el === head) keep = true;
      else if (keep && /^H[1-6]$/.test(el.tagName) && el.tagName <= level) keep = false;
      if (!keep) el.classList.add("ws-only-hide");
    });
    window.scrollTo(0, 0);
  }
  if (window.document$) window.document$.subscribe(only);
  else document.addEventListener("DOMContentLoaded", only);
})();
