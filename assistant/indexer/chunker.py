"""Turn the docs tree into retrievable chunks.

Pure functions, no I/O and no network, so the interesting parts can be checked
against the real built site rather than reasoned about.

The one rule that matters: a citation is only useful if its anchor resolves, so
heading ids are produced by the *same* slugify mkdocs uses rather than a
lookalike. `build_index.py --verify` diffs what this module produces against the
ids in `site/`, and that check is a CI gate.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from markdown.extensions.toc import slugify, unique

# A section longer than this is re-split at the next heading level down.
MAX_CHUNK = 3500
# Where a hard split (no headings left to use) cuts, and how much it repeats so
# a sentence straddling the cut still reads whole in one of the halves.
HARD_SPLIT = 3000
HARD_OVERLAP = 200
# Below this a "section" is a heading with no body — a table of contents entry,
# not something worth retrieving.
MIN_CHUNK = 80

FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
# attr_list on a heading: `{ #custom-id .class }`. Only the id interests us.
ATTR_LIST_RE = re.compile(r"\{:?\s*([^}]*)\}\s*$")
ATTR_ID_RE = re.compile(r"#([A-Za-z0-9_\-.:]+)")
# An attr_list anywhere in the line, e.g. `:icon:{ style="color: #009688" }`.
# Deliberately narrow — it must look like attributes, so a literal `{DATA_ROOT}`
# in a heading is left alone the way Python-Markdown leaves it.
ATTR_BLOCK_RE = re.compile(r"\{:?\s*[.#][^}]*\}|\{:?\s*[^}]*=[^}]*\}")
HTML_TAG_RE = re.compile(r"<[^>]+>")
# `:material-video:` and friends. Bounded so "Step 1: install" survives.
EMOJI_SHORTCODE_RE = re.compile(r"(?<![\w:]):[a-z][a-z0-9_+\-]*:(?!\w)")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
BLOCK_HTML_RE = re.compile(r"<(style|script)\b.*?</\1>", re.S | re.I)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
SNIPPET_RE = re.compile(r"^\s*--8<--.*$", re.M)


@dataclass(frozen=True)
class Chunk:
    id: str
    url: str  # site-relative page path, e.g. "features/components/"
    anchor: str  # "" for the page-level chunk
    title: str
    breadcrumb: str
    section: str  # top-level docs directory, for metadata filtering
    part: int  # >0 only when a section had to be hard-split
    text: str

    @property
    def href(self) -> str:
        return f"{self.url}#{self.anchor}" if self.anchor else self.url


@dataclass
class _Node:
    level: int
    title: str
    anchor: str
    lines: list[str] = field(default_factory=list)
    children: list["_Node"] = field(default_factory=list)

    def body(self) -> str:
        return "\n".join(self.lines).strip()

    def full_text(self) -> str:
        out = [self.body()]
        out += [c.full_text() for c in self.children]
        return "\n\n".join(p for p in out if p)


# -- headings -----------------------------------------------------------------


def clean_heading(raw: str) -> str:
    """The text mkdocs slugifies: what a reader would see, minus the markup.

    The toc extension slugifies the *rendered* element's text, so inline HTML
    contributes its content but not its tags, emoji shortcodes render to an
    image and contribute nothing, and a link contributes only its label.

    Two cases here are not obvious, and both were found by `--verify` rather
    than by reading the source:

    - `:icon:{ style="…" }` puts an attr_list in the *middle* of a heading, not
      at the end, so trailing-only removal leaves `stylecolor-009688-` glued to
      the front of the slug.
    - Inline code is text, not markup: ``` `<output>.yaml` ``` slugifies to
      `outputyaml`, so stripping HTML tags blindly eats the `<output>`.
    """
    text = ATTR_LIST_RE.sub("", raw)

    # Park inline code so the HTML strip below cannot reach inside it.
    spans: list[str] = []

    def park(m: re.Match) -> str:
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]*)`", park, text)

    text = ATTR_BLOCK_RE.sub("", text)
    text = EMOJI_SHORTCODE_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub("", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)
    return text.strip()


def explicit_id(raw: str) -> str | None:
    m = ATTR_LIST_RE.search(raw)
    if not m:
        return None
    found = ATTR_ID_RE.search(m.group(1))
    return found.group(1) if found else None


def heading_id(raw: str, used: set[str]) -> str:
    """Mirror `TocTreeprocessor`: an explicit id wins and does not reserve a slug."""
    given = explicit_id(raw)
    if given:
        return given
    return unique(slugify(clean_heading(raw), "-"), used)


def iter_headings(body: str):
    """Yield `(line_index, level, raw_text)`, ignoring anything inside a fence.

    Without the fence tracking, a `# comment` in a Python block reads as an h1
    and shifts every later duplicate-id counter by one.
    """
    fence: str | None = None
    for i, line in enumerate(body.splitlines()):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(2)[0] * 3
            if fence is None:
                fence = marker
            elif line.strip().startswith(fence):
                fence = None
            continue
        if fence is not None:
            continue
        h = HEADING_RE.match(line)
        if h:
            yield i, len(h.group(1)), h.group(2)


def page_anchors(body: str) -> list[tuple[int, int, str, str]]:
    """`(line, level, title, anchor)` for every heading, ids assigned as mkdocs would."""
    used: set[str] = set()
    out = []
    for line, level, raw in iter_headings(body):
        out.append((line, level, clean_heading(raw), heading_id(raw, used)))
    return out


# -- urls ---------------------------------------------------------------------


def page_url(rel_path: str) -> str:
    """`features/components.md` -> `features/components/` (mkdocs directory URLs)."""
    path = rel_path[:-3] if rel_path.endswith(".md") else rel_path
    parts = path.split("/")
    if parts[-1] in ("index", "README"):
        parts.pop()
    return "/".join(parts) + "/" if parts else ""


def top_section(rel_path: str) -> str:
    head, _, tail = rel_path.partition("/")
    return head if tail else "root"


# -- splitting ----------------------------------------------------------------


def strip_noise(text: str) -> str:
    text = FRONT_MATTER_RE.sub("", text)
    text = BLOCK_HTML_RE.sub("", text)
    text = HTML_COMMENT_RE.sub("", text)
    return SNIPPET_RE.sub("", text)


def _build_tree(body: str, headings: list[tuple[int, int, str, str]]) -> _Node:
    lines = body.splitlines()
    root = _Node(level=0, title="", anchor="")
    stack = [root]
    bounds = [h[0] for h in headings] + [len(lines)]

    root.lines = lines[: bounds[0]]
    for idx, (line, level, title, anchor) in enumerate(headings):
        node = _Node(level=level, title=title, anchor=anchor)
        node.lines = lines[line : bounds[idx + 1]]
        while stack and stack[-1].level >= level:
            stack.pop()
        (stack[-1] if stack else root).children.append(node)
        stack.append(node)
    return root


def _prune(node: _Node, drop: tuple[str, ...]) -> None:
    node.children = [c for c in node.children if not any(d in c.title for d in drop)]
    for child in node.children:
        _prune(child, drop)


def _blocks(text: str) -> list[str]:
    """Paragraphs, but a paragraph longer than a chunk is cut by line.

    A long reference page is often one uninterrupted YAML or table block with no
    blank line in it, which paragraph splitting alone cannot cut at all.
    """
    out = []
    for para in text.split("\n\n"):
        if len(para) <= HARD_SPLIT:
            out.append(para)
            continue
        buf = ""
        for line in para.splitlines():
            if buf and len(buf) + len(line) + 1 > HARD_SPLIT:
                out.append(buf)
                buf = line
            else:
                buf = f"{buf}\n{line}" if buf else line
        if buf:
            out.append(buf)
    return out


def _hard_split(text: str) -> list[str]:
    if len(text) <= MAX_CHUNK:
        return [text]
    parts, buf = [], ""
    for block in _blocks(text):
        if buf and len(buf) + len(block) + 2 > HARD_SPLIT:
            parts.append(buf)
            buf = buf[-HARD_OVERLAP:] + "\n\n" + block
        else:
            buf = f"{buf}\n\n{block}" if buf else block
    if buf:
        parts.append(buf)
    return parts


def _emit(node: _Node, ctx: dict, trail: list[str], out: list[Chunk]) -> None:
    text = node.full_text()
    here = trail + ([node.title] if node.title else [])
    can_descend = node.children and node.level < ctx["max_depth"]

    if len(text) <= MAX_CHUNK or not can_descend:
        for part, piece in enumerate(_hard_split(text)):
            if len(piece.strip()) < MIN_CHUNK:
                continue
            out.append(_chunk(node, ctx, here, part, piece))
        return

    # The section's own text, above its first subsection. Still needs splitting:
    # a reference page's h2 lead can be a single enormous YAML block.
    for part, piece in enumerate(_hard_split(node.body())):
        if len(piece.strip()) >= MIN_CHUNK:
            out.append(_chunk(node, ctx, here, part, piece))
    for child in node.children:
        _emit(child, ctx, here, out)


def _chunk(node: _Node, ctx: dict, trail: list[str], part: int, text: str) -> Chunk:
    url = ctx["url"]
    anchor = node.anchor
    crumb = " > ".join([c for c in [ctx["breadcrumb"]] + trail[:-1] if c][:4]) or ctx["breadcrumb"]
    raw_id = f"{url}#{anchor}#{part}"
    return Chunk(
        id=hashlib.blake2b(raw_id.encode(), digest_size=12).hexdigest(),
        url=url,
        anchor=anchor,
        title=trail[-1] if trail else ctx["breadcrumb"],
        breadcrumb=crumb,
        section=ctx["section"],
        part=part,
        text=text.strip(),
    )


def chunk_page(
    rel_path: str,
    raw: str,
    breadcrumb: str = "",
    *,
    max_depth: int = 4,
    drop_headings: tuple[str, ...] = (),
) -> list[Chunk]:
    """Split one markdown file into chunks.

    Sections are cut at h2, then at h3 and h4 only when a section is too long to
    embed usefully, so a short page stays one chunk and a reference page is cut
    where its own structure already says to cut it.

    `max_depth` stops that descent early, and `drop_headings` removes a section
    and its children by title substring — both exist for pages whose structure
    fights the default rule. See `config.yaml`.
    """
    body = strip_noise(raw)
    headings = page_anchors(body)
    tree = _build_tree(body, headings)
    if drop_headings:
        _prune(tree, drop_headings)
    ctx = {
        "url": page_url(rel_path),
        "section": top_section(rel_path),
        "breadcrumb": breadcrumb or page_url(rel_path).strip("/") or "Home",
        "max_depth": max_depth,
    }

    out: list[Chunk] = []
    lead = tree.body()
    if len(lead.strip()) >= MIN_CHUNK:
        # Content above the first heading, anchored at the page rather than a
        # section — usually the intro paragraph, which is often the best answer
        # to "what is X".
        top = tree.children[0] if tree.children and tree.children[0].level == 1 else None
        node = _Node(level=1, title=top.title if top else ctx["breadcrumb"], anchor="")
        node.lines = lead.splitlines()
        for part, piece in enumerate(_hard_split(lead)):
            if len(piece.strip()) >= MIN_CHUNK:
                out.append(_chunk(node, ctx, [node.title], part, piece))

    for child in tree.children:
        _emit(child, ctx, [], out)

    # Two headings can collide on a hard-split boundary; ids must stay unique.
    seen: set[str] = set()
    unique_out = []
    for c in out:
        if c.id in seen:
            continue
        seen.add(c.id)
        unique_out.append(c)
    return unique_out
