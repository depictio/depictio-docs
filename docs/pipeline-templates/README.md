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

Each template carries a status reflecting its review level.

!!! success "🛡️ Certified"
    Reviewed and validated by the **pipeline lead developer**. Highest trust — the pipeline author confirms the template correctly represents their outputs.

!!! info "☑️ Reviewed"
    Tested against reference datasets, CI passes, recipe checkpoints validated. Reviewed by Depictio team or community maintainers.

!!! warning "🧪 Experimental"
    Shared as-is. A good starting point — feedback and PRs welcome.

---

## Available templates

<div class="grid cards" markdown>

-   <a href="nf-core/ampliseq/" style="text-decoration:none;color:inherit;">
    <img src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="ampliseq" style="height:36px;margin-bottom:8px;">

    **nf-core/ampliseq**{ style="font-size:1.1em" }

    ---

    16S/ITS amplicon sequencing — microbial community analysis

    :material-database: 9 DCs · :material-chef-hat: 6 recipes · :material-link: 7 links

    !!! success inline end ""
        🛡️ Certified

    </a>

</div>

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
