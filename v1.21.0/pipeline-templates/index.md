# Depictio Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project, dashboards included, with a single command.

```
depictio ingest /data/my_ampliseq_run \
  --template nf-core/ampliseq/latest
```

______________________________________________________________________

## Available templates

All Certified Reviewed Experimental Draft

No template matches that search.

______________________________________________________________________

## Status levels

Draft

Generated and not yet reviewed. Expect it to need fixes before it is usable.

Experimental

Shared as-is. Feedback and PRs welcome.

Reviewed

Tested, CI passes, reviewed by the Depictio team or community.

Certified

Validated by the **pipeline lead developer**. Highest trust level.

______________________________________________________________________

## How templates work

A template bundles:

- **[Project configuration](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#template-yaml-structure)**: workflows, data collections and cross-DC links, with [`{VAR_NAME}` placeholders](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#template-variables)
- **[Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md)**: Python transforms that turn raw pipeline outputs into dashboard-ready tables
- **[Dashboard YAML](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/index.md)**: imported on the first run, with the template variables substituted
- **[Cross-DC links](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#cross-dc-links)**: interactive filtering across data collections
- **[Recipe seeds](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#recipe-seeds)**: each recipe's output committed as a `.tsv`, so the bundled project can be explored, and re-ingested, without the pipeline run behind it (v1.6.0+)

______________________________________________________________________

## Pipeline version and template version

A template carries two version numbers. They move independently.

- **Pipeline version**

  ______________________________________________________________________

  The pipeline release the template reads, last in its id: `nf-core/rnaseq/3.26.0`.

  *Choose it* with `--template`, or the **Pipeline version** picker on a template's page.

- **Template version**

  ______________________________________________________________________

  The revision of the template itself, such as `2.0.0` to `2.1.0`, for one pipeline release.

  *Find it* beside the picker, in the ingest log, and in the project and dashboard settings.

When the template version moves, what you need to do depends on which number changed:

Major `2.1.0 → 3.0.0`

**The data collections changed.** A collection, a column or a template variable was added, removed or renamed.

Ingest the run again.

Minor `2.0.0 → 2.1.0`

**The dashboards changed.** Figures, tabs or recipes moved; every collection keeps its columns.

Import the dashboards again.

Patch `2.1.0 → 2.1.1`

**Only text changed.** Titles, captions and descriptions.

Nothing to do; import again to get the new wording.

Depictio records the template version a project was ingested with, and the one each dashboard was imported from. The viewer warns when a newer one is available.

______________________________________________________________________

## Contributing a template

Want to add a template for another pipeline? The contributing guide covers the directory layout, recipe requirements, and review process.

[Read the contributing guide](https://depictio.github.io/depictio-docs/latest/developer/contributing-templates/index.md)
