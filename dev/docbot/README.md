# DocBot onboarding

[DocBot](https://ebi-wp.gitdocs.ebi.ac.uk/docbot_docs/docbot-overview.html) is the
EMBL-EBI documentation chatbot: it answers questions from a project's own docs, with
links to the sources. This folder holds what the depictio docs need to be added to it.
Nothing here is published on the site.

1. Submit the project through the Google Form linked from
   [Adding a new project to DocBot](https://ebi-wp.gitdocs.ebi.ac.uk/docbot_docs/adding-a-new-project-to-docbot.html),
   with the answers below and the pairs in [evaluation-qa.md](evaluation-qa.md).
2. Ask <docbot-team@ebi.ac.uk> to add `https://depictio.github.io` to the CORS allowed
   origins, since the site is not hosted on `ebi.ac.uk`.
3. Once DocBot confirms the team ID, turn the widget on (see
   [Turning the widget on](#turning-the-widget-on)).

## Form answers

### Documentation information

| Field | Answer |
|-------|--------|
| Source access | Public GitHub repository [`depictio/depictio-docs`](https://github.com/depictio/depictio-docs), branch `main`, folder `docs/` |
| Document format | Markdown (MkDocs Material) |
| Public documentation URL | <https://depictio.github.io/depictio-docs/stable/> |
| Source URL | <https://github.com/depictio/depictio-docs/tree/main/docs> |
| Evaluation Q&A | The 15 pairs in [evaluation-qa.md](evaluation-qa.md) |

Notes for the DocBot team, to paste where the form allows free text:

- **Path to public URL.** The site uses directory URLs and is versioned with `mike`;
  `stable` always points at the latest release.
  `docs/<path>/<page>.md` is published at
  `https://depictio.github.io/depictio-docs/stable/<path>/<page>/`, and
  `docs/<path>/README.md` or `docs/<path>/index.md` at
  `https://depictio.github.io/depictio-docs/stable/<path>/`.
  For example, `docs/installation/docker.md` →
  <https://depictio.github.io/depictio-docs/stable/installation/docker/>.
- **Folders and files to skip.** `docs/assets/`, `docs/images/`, `docs/fonts/`,
  `docs/javascripts/`, `docs/stylesheets/` (no prose), `docs/documentation_outline.md`
  and `docs/animated-logo.md` (internal), and `docs/api/reference.md` (renders the
  OpenAPI schema, empty as Markdown). The blog (`docs/blog/`) and changelog
  (`docs/changelog/`) are worth keeping: they answer "since which version" questions.
- **Snippet includes.** 26 pages, mostly the nf-core template pages under
  `docs/pipeline-templates/nf-core/`, pull shared text in with
  `--8<-- "<path>"` lines (pymdownx.snippets, paths relative to `docs/`). In the raw
  Markdown those lines stay unresolved.

### Project information

| Field | Answer |
|-------|--------|
| Project name | Depictio |
| Team ID wished | `depictio` |
| Short description | Depictio is an open-source platform for building interactive dashboards from bioinformatics workflow outputs, such as nf-core pipelines, for quality control monitoring and result exploration in omics. |
| Main contact | Thomas Weber, <thomas.weber@embl.de> |
| Development contact | Thomas Weber, <thomas.weber@embl.de> |
| Support contact | Support page: `https://github.com/depictio/depictio/issues/new` |
| Support page: message parameter | `body` |
| Support page: subject parameter | `title` |

The support page is GitHub's new-issue form: DocBot's link opens it with the
conversation as the issue body and its generated subject as the title, for example
`https://github.com/depictio/depictio/issues/new?title=<subject>&body=<message>`.
The user needs a GitHub account to submit it.

## Turning the widget on

The widget is already wired in `overrides/main.html`, on every page, with the team
selector locked. Its settings are under `extra.docbot` in `mkdocs.yml`:

| Key | Value |
|-----|-------|
| `enabled` | `!ENV [DEPICTIO_DOCS_DOCBOT, false]`: off unless the variable is set |
| `team` | `depictio`, a placeholder: replace it with the ID DocBot assigns |
| `backend` | Production, `https://www.ebi.ac.uk/docbot/api`. Development is `https://wwwdev.ebi.ac.uk/docbot/api` |
| `sdk` | Where the widget's script and stylesheet are served from |

To try it locally, against the development backend if production does not know the
team yet:

```bash
DEPICTIO_DOCS_DOCBOT=1 uv run mkdocs serve
```

To ship it, set `enabled: true` in `mkdocs.yml` (or `DEPICTIO_DOCS_DOCBOT: 1` in the
build step of `.github/workflows/deploy-docs.yaml`). Only versions deployed after that
carry the widget; older `mike` versions stay as they were built.

DocBot re-indexes git sources on weeknights, so doc changes reach it the next day.
Changes to the project itself go to <docbot-team@ebi.ac.uk>.
