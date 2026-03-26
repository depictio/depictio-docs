# <span style="color: #45B8AC;">:material-puzzle:</span> Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio run --template nf-core/ampliseq/2.16.0 --data-root /data/my_ampliseq_run \
  --var SAMPLESHEET_FILE=samplesheet.csv
```

That's it. Depictio resolves your data directory, runs all data transformations, and imports ready-to-use dashboards automatically.

---

## How templates work

A template bundles:

- :material-cog:{ style="color: #45B8AC" } **Project configuration** — workflows, data collections, and cross-DC links with `{VAR_NAME}` placeholders
- :material-chef-hat:{ style="color: #45B8AC" } **Recipes** — Python transforms that convert raw pipeline outputs into dashboard-ready tables
- :material-view-dashboard:{ style="color: #45B8AC" } **Dashboard YAML** — imported automatically on first run, with template variable substitution
- :material-link:{ style="color: #45B8AC" } **Cross-DC links** — enable interactive filtering across data collections

See [Templates reference](../usage/projects/templates.md) for the full technical specification, and [Recipes](../usage/projects/recipes.md) for how data transformations work.

---

## Badge system

Each template carries a quality badge reflecting how it was developed and reviewed.

:material-check-decagram:{ style="color: #45B8AC" } **Official** — Built by the Depictio core team. Tested against reference datasets. Fully supported.
&nbsp;&nbsp;
:material-shield-check:{ style="color: #4CAF50" } **Pipeline-reviewed** — Reviewed and validated by the pipeline lead developer. Confirms the template correctly represents pipeline outputs.
&nbsp;&nbsp;
:material-check-circle:{ style="color: #2196F3" } **Verified** — Community-contributed and reviewed by a Depictio core team member. CI passes, recipe checkpoints validated.
&nbsp;&nbsp;
:material-flask:{ style="color: #FF9800" } **Experimental** — User-contributed, shared as-is. A good starting point — feedback and PRs welcome.

---

## Available templates

| Template | Pipeline | Versions | Badge | Content |
|----------|----------|----------|-------|---------|
| [nf-core/ampliseq](nf-core/ampliseq.md) | 16S/ITS amplicon sequencing | 2.14.0, 2.16.0 | :material-shield-check:{ style="color: #4CAF50" } Pipeline-reviewed | 9 DCs · 6 recipes · 7 links |

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
