# <span style="color: #45B8AC;">:material-puzzle:</span> Templates

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

- :material-cog:{ style="color: #45B8AC" } **Project configuration** — workflows, data collections, and cross-DC links with `{VAR_NAME}` placeholders
- :material-chef-hat:{ style="color: #45B8AC" } **Recipes** — Python transforms that convert raw pipeline outputs into dashboard-ready tables
- :material-view-dashboard:{ style="color: #45B8AC" } **Dashboard YAML** — imported automatically on first run, with template variable substitution
- :material-link:{ style="color: #45B8AC" } **Cross-DC links** — enable interactive filtering across data collections

See [Templates reference](../usage/projects/templates.md) for the full technical specification, and [Recipes](../usage/projects/recipes.md) for how data transformations work.

---

## Status levels

Each template carries a status badge reflecting its review level and trust.

| Status | Meaning |
|--------|---------|
| <span style="background:#4CAF50;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.85em;">🛡️ Certified</span> | Reviewed and validated by the **pipeline lead developer**. Highest trust — the pipeline author confirms the template correctly represents their outputs. |
| <span style="background:#45B8AC;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.85em;">✅ Supported</span> | Built and maintained by the **Depictio core team**. Tested against reference datasets. Fully supported. |
| <span style="background:#2196F3;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.85em;">☑️ Community</span> | **Community-contributed** and reviewed by a Depictio core team member. CI passes, recipe checkpoints validated. |
| <span style="background:#FF9800;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.85em;">🧪 Experimental</span> | **User-contributed**, shared as-is. A good starting point — feedback and PRs welcome. |

---

## Available templates

<div class="grid cards" markdown>

-   ![nf-core/ampliseq](../images/pipeline-templates/nf-core/ampliseq/nf-core-ampliseq_logo.png){ style="height:40px" }

    **nf-core/ampliseq**

    ---

    16S/ITS amplicon sequencing — microbial community analysis

    9 data collections · 6 recipes · 7 cross-DC links

    <span style="background:#4CAF50;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.8em;">🛡️ Certified</span>

    [:octicons-arrow-right-24: View template](nf-core/ampliseq.md)

</div>

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
