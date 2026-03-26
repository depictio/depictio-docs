---
icon: material/layers-outline
---

# Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run \
  --var SAMPLESHEET_FILE=samplesheet.csv \
  --var METADATA_FILE=Metadata.tsv
```

That's it. Depictio resolves your data directory, runs all data transformations, and imports ready-to-use dashboards automatically.

---

## How templates work

A template bundles:

- **Project configuration** — workflows, data collections, and cross-DC links with `{VAR_NAME}` placeholders
- **Recipes** — Python transforms that convert raw pipeline outputs into dashboard-ready tables
- **Dashboard YAML** — imported automatically on first run, with template variable substitution
- **Cross-DC links** — enable interactive filtering across data collections

See [Templates reference](../usage/projects/templates.md) for the full technical specification, and [Recipes](../usage/projects/recipes.md) for how data transformations work.

---

## Status levels

Each template carries a status reflecting its review level.

:material-shield-check:{ style="color:#4CAF50" } **Certified** — Validated by the **pipeline lead developer**. Highest trust.

:material-check-circle-outline:{ style="color:#2196F3" } **Reviewed** — Tested, CI passes, reviewed by Depictio team or community.

:material-flask-outline:{ style="color:#FF9800" } **Experimental** — Shared as-is. Feedback and PRs welcome.

---

## Available templates

<div style="display:flex;gap:16px;flex-wrap:wrap;">
  <a href="nf-core/ampliseq/" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;border:1px solid #ddd;border-radius:16px;padding:32px 40px;width:280px;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'" onmouseout="this.style.boxShadow='none'">
    <img src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq" style="height:64px;">
    <span style="background:#4CAF50;color:#fff;padding:4px 14px;border-radius:12px;font-size:0.85em;font-weight:600;">Certified</span>
  </a>
</div>

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
