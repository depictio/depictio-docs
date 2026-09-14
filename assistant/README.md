# Docs assistant

A Cloudflare Worker that answers questions about Depictio from this
documentation, and the indexer that feeds it.

```
question ─▶ Workers AI (embed) ─▶ Vectorize (top-k) ─▶ relevance floor ─▶ OpenRouter ─▶ answer
                                                             │
                                                             └─▶ nothing relevant: "not documented",
                                                                 no model call, no cost
```

| Piece | Where |
| --- | --- |
| Worker | `src/worker.js` — one file, no bundler, no runtime dependencies |
| Indexer | `indexer/build_index.py`, `indexer/chunker.py`, `indexer/config.yaml` |
| Seed chunks | `indexer/seed/*.md` — context the docs tree cannot supply |
| Widget | `../docs/javascripts/ask-ai.js`, `../docs/stylesheets/ask-ai.css` |
| CI | `../.github/workflows/deploy-assistant.yaml` |

## Two design decisions worth knowing

**Citations cannot be hallucinated.** The prompt forbids the model from writing
URLs. It returns the ids of the excerpts it used; the worker maps those to the
URLs it retrieved a moment earlier. Unknown ids are dropped, any surviving link
is stripped, and an answer that still contains one is replaced with a fallback.
The client then re-checks that every citation is same-origin before rendering it
as a link.

**A question that retrieves nothing never reaches the model.** `MIN_SCORE` is a
cosine floor; below it the worker returns "not documented" directly. This is both
the strongest guard against invention and the reason an off-topic question costs
nothing.

`MIN_SCORE = 0.45` is a **starting guess**. Every request logs its per-match
scores precisely so it can be set from real traffic — check `/report` in the
first week and move it. Too high and the assistant denies things that are
documented; too low and it answers off-topic questions from tangential chunks.

## Setup

One-time, from this directory:

```bash
# 1. The index. bge-m3 is 1024-dimensional.
npx wrangler vectorize create depictio-docs --dimensions=1024 --metric=cosine

# 2. Metadata index. MUST exist before the first upsert — Vectorize does not
#    backfill, so adding it later means re-indexing everything.
npx wrangler vectorize create-metadata-index depictio-docs \
    --property-name=s --type=string

# 3. KV, for quotas, the question archive, and the index id set.
#    Paste the printed id into wrangler.toml.
npx wrangler kv namespace create QUOTA

# 4. Secrets. Never in wrangler.toml, never in CI.
npx wrangler secret put OPENROUTER_KEY
npx wrangler secret put LOG_TOKEN

# 5. Pick a model — see wrangler.toml, MODEL is deliberately empty.

npx wrangler deploy
```

Then in GitHub → Settings → Secrets: `CLOUDFLARE_ACCOUNT_ID`,
`CLOUDFLARE_KV_NAMESPACE_ID`, and a `CLOUDFLARE_API_TOKEN` scoped to *Workers
Scripts: Edit*, *Workers AI: Read + Edit*, *Vectorize: Edit*, *Workers KV: Edit*
— nothing more.

Finally, set `ASKAI_ENDPOINT` in `docs/javascripts/ask-ai.js` to the deployed
URL. **Keep it stable forever**: every mike version deployed from then on bakes
in whatever it says, and changing it later will not fix versions already
published.

## Indexing

```bash
uv run python assistant/indexer/build_index.py --dry-run     # chunk + report
uv run mkdocs build
uv run python assistant/indexer/build_index.py --verify      # anchors resolve?
uv run python assistant/indexer/build_index.py --upsert      # embed + push
```

`--verify` is a CI gate on pull requests, not a convenience. It parses the built
HTML and fails if any generated anchor is missing. It has already caught a real
docs bug — a code fence inside an HTML comment that silently swallowed a whole
section of `usage/projects/yaml-examples.md`.

Anchors come from `markdown.extensions.toc.slugify`, the same function mkdocs
uses, rather than a lookalike. Heading cleaning has to reproduce what the toc
extension sees *after* rendering, which is subtler than it looks: an attr_list
can sit in the middle of a heading (`:icon:{ style="…" }`), and inline code is
text rather than markup, so `` `<output>.yaml` `` slugifies to `outputyaml`.

Re-indexing re-embeds everything — 550 chunks is about 0.2 neurons against a
10,000/day free allowance, so the cost of being simple here is nil. Vectorize
can neither list ids nor bulk-delete, so the id set lives in KV under
`index:ids`; without it, a deleted page's chunks would stay in the index
forever, still retrievable and still cited. A run that would delete more than
30% of the index aborts unless `--force` is passed — that is a broken chunker,
not a shrinking docs site.

## Endpoints

| Method | Path | Auth |
| --- | --- | --- |
| `POST` | `/ask` | none — CORS pinned to the docs origin, plus quotas |
| `GET` | `/health` | none |
| `GET` | `/report` | `?token=` |
| `GET` | `/logs` | `?token=` |
| `POST` | `/logs/clear`, `/logs/delete` | `?token=` |

The console endpoints allow any origin, because the token is the barrier and
CORS is not one — `curl` ignores it. Keeping them open lets the console page
live anywhere without widening CORS on `/ask`.

`/report` includes an **ungrounded rate**: the share of questions that retrieved
nothing relevant. That list is a documentation-gap backlog derived from what
people actually ask, and is arguably the most valuable output here.

## Cost, and what breaks first

| | |
| --- | --- |
| Index | ~550 chunks × 1024 dims ≈ **0.56M stored dimensions**, ~11% of the Vectorize free tier |
| Embeddings | ~0.0001 neurons per question against 10,000/day free — not the constraint |
| OpenRouter | ~7k input + ~250 output tokens ≈ **$0.002/question**; at realistic traffic, a couple of dollars a month, hard-capped by `GLOBAL_LIMIT` |

**KV writes are the first real limit.** Workers Free allows 1,000/day, and each
answered question writes three keys (per-IP quota, global counter, archive
entry), so the practical ceiling is around 330 questions/day — below
`GLOBAL_LIMIT`. The 10 ms CPU limit also bites on `/report` once the archive
grows into the thousands, which is why `readLogs` is capped at 2,000 entries.

**Budget $5/month for Workers Paid** if the assistant sees real use. It removes
the KV cliff, raises CPU to 30 s, and makes `/report` usable — for less than the
OpenRouter spend.

Abuse is bounded by design: 5 questions/minute per IP (rate-limit binding) and
20/day (KV) caps a single abuser at a few cents; a distributed attacker rotating
IPs is capped by `GLOBAL_LIMIT` at under a dollar a day.

## Versioning

The index reflects **one** version of the docs — whatever `DOCS_BASE` points at.
On any other mike version the widget still renders, but shows a notice saying
answers come from the latest docs, and citations point at `stable/`.

Indexing every version was considered and rejected: 40 versions × 550 chunks ×
1024 dims is roughly 5× the free tier, for content nobody asks about.

## Why not AutoRAG / AI Search

Cloudflare's managed option looks like it would remove most of this, and does
not. Its website crawler only works on domains onboarded to the same Cloudflare
account, and `depictio.github.io` is GitHub Pages. The R2 path puts the upload
step straight back, gives worse citations — source keys are file paths, so the
heading anchor is lost — caps custom metadata at 5 fields, and its
`chatCompletions()` cannot call OpenRouter. You would keep about 90% of this
worker and lose anchor-level citations.

Worth revisiting only if the docs ever move onto a Cloudflare-hosted domain.
