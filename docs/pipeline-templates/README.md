# <span style="color: #45B8AC;">:material-puzzle:</span> Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio run --template nf-core/ampliseq/2.16.0 --data-root /data/my_ampliseq_run
```

That's it. Depictio resolves your data directory, runs all data transformations, and imports ready-to-use dashboards automatically.

---

## How templates work

A template bundles:

- **Project configuration** (workflows, data collections, cross-DC links) with `{DATA_ROOT}` placeholders
- **Recipes** for transforming raw pipeline output into dashboard-ready tables
- **Dashboard YAML** files imported automatically on first run

See [Templates reference](../usage/projects/templates.md) for the full technical specification, and [Recipes](../usage/projects/recipes.md) for how data transformations work.

---

## Badge system

Each template carries a quality badge reflecting how it was developed and tested.

<div class="grid cards" markdown>

-   :material-check-decagram:{ style="color: #45B8AC" } **Official**

    ---

    Developed by the **Depictio core team**. Tested against real pipeline outputs from an official reference run (e.g. nf-core AWS test datasets). Peer-reviewed before every CLI release. Fully supported.

-   :material-check-circle:{ style="color: #4CAF50" } **Verified**

    ---

    **Community-contributed** and reviewed by a Depictio core team member. CI passes, recipe checkpoints validated, schema tested. Not necessarily backed by a reference dataset.

-   :material-flask:{ style="color: #FF9800" } **Experimental**

    ---

    **User-contributed**, shared as-is. May not cover all pipeline versions or edge cases. A good starting point — feedback and PRs welcome via GitHub.

</div>

---

## Available templates

| Template | Pipeline | Versions | Badge | Recipes | One-liner |
|----------|----------|----------|-------|---------|-----------|
| [nf-core/ampliseq](nf-core/ampliseq.md) | 16S/ITS amplicon sequencing | 2.14.0, 2.16.0 | :material-check-decagram:{ style="color: #45B8AC" title="Official" } Official | 5 | `depictio run --template nf-core/ampliseq/2.16.0 --data-root <path>` |

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
