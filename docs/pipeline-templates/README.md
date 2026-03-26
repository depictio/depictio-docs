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

<div style="display:flex;flex-direction:column;gap:12px;margin:16px 0;">
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="background:#4CAF50;color:#fff;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600;min-width:120px;text-align:center;">🛡️ Certified</span>
    <span>Validated by the <strong>pipeline lead developer</strong>. Highest trust.</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="background:#2196F3;color:#fff;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600;min-width:120px;text-align:center;">☑️ Reviewed</span>
    <span>Tested, CI passes, reviewed by Depictio team or community.</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="background:#FF9800;color:#fff;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600;min-width:120px;text-align:center;">🧪 Experimental</span>
    <span>Shared as-is. Feedback and PRs welcome.</span>
  </div>
</div>

---

## Available templates

<div class="grid cards" markdown>

-   <a href="nf-core/ampliseq/" style="text-decoration:none;color:inherit;display:block;text-align:center;">
    <img src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq" style="height:60px;margin:16px auto;display:block;">
    <span style="background:#4CAF50;color:#fff;padding:3px 10px;border-radius:10px;font-size:0.8em;font-weight:600;">🛡️ Certified</span>
    </a>

</div>

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
