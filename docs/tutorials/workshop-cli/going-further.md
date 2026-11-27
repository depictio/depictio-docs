---
glightbox: true
title: "Going further"
description: "After the command-line course: hand your project to a colleague as a template, re-ingest a folder when it changes, trigger Depictio at the end of a Nextflow run, compose a dashboard from the tools catalog, run Depictio on your own machine."
---

# Going further

<div class="ws-strip" markdown>
[**0** Setup](setup.md){ .ws-ep0 } [**1** Your tables](project-builder.md){ .ws-ep1 } [**2** nf-core run](nf-core-run.md){ .ws-ep2 } [**3** Together](collaborate-and-export.md){ .ws-ep3 } [**+** Going further](going-further.md){ .ws-ep4 .ws-here }
</div>

Three longer lessons from the first version of this course, then five things to try after the workshop. None of them is timed.

<div class="grid cards" markdown>

-   :material-file-code-outline: **[A project file by hand](first-project.md)**

    ---

    Describe one table in a short project file, check it with a dry run, and create a project and a dashboard from your laptop.

-   :material-calendar-plus: **[A new season](own-tables.md)**

    ---

    Add a second table and its link, then bring the next field season as a new run and compare.

-   :material-code-braces: **[A dashboard as code](dashboard-as-code.md)**

    ---

    Export a dashboard to YAML, change it, check it with `validate`, and import it back.

</div>

Five things to try after the workshop, each from your penguins project or the nf-core run. The outputs below come from the CLI version of the workshop; `watch` and the Nextflow trigger are described from their help and were not run during the workshop rehearsal.

## :material-share-variant-outline: Hand your project to a colleague

A **template** is your project file and its dashboards, packed so that someone else can run them on their own folder. After the lessons A new season and A dashboard as code, your project has two dashboards.

1. Export it. The project ID is the last part of the project's address, `…/projects/<ID>`:

    ```console
    $ depictio template export <ID> -t mylab/penguins/1 -o templates
    ✓ Template bundle written to: templates/mylab/penguins/1
    ```

    ```console
    templates/mylab/penguins/1/
    ├── template.yaml                      the project: workflows, data collections, links
    └── dashboards/                        one file per dashboard
        ├── penguin_field_survey.yaml
        └── penguins_two_seasons.yaml
    ```

2. Check the folders it names. The export writes the locations as they were: `seasons/season_2007` and `seasons/season_2008`, and `{SEASON_DIR}` is gone. A colleague's folder is passed on the command line, so these lines do not stop them; `--data-dir <prefix>` turns a path prefix into a variable instead.

3. Your colleague runs it on their folder, with `--template` pointing at the bundle:

    ```console
    $ depictio ingest seasons/season_2008 --template templates/mylab/penguins/1 \
        --project colleague-penguins --dry-run
    ✓ Template 'mylab/penguins/1' loaded successfully
    • Template provides 2 default dashboard(s)
    ✓ 2 data collection(s) will ingest, 0 empty, 0 missing sources
    • Would create project 'colleague-penguins'
    • Would import 2 dashboard(s)
    ✓ Dry run complete (8/8 steps): the configuration is valid, and nothing was changed.
    ```

See [Templates](../../usage/projects/templates.md).

## :material-folder-sync-outline: Re-ingest a folder when it changes

`depictio watch` runs `ingest` on a loop: on a folder where new results land, the project follows. It takes the options of `ingest` (`--project-config-path`, `--project`) and:

| Option | Does |
|---|---|
| `--once` | One pass, then stop |
| `--interval` | Seconds between two checks when polling (default 300) |
| `--debounce`, `--settle` | Wait for files to stop changing before ingesting (defaults 30 s and 5 s) |
| `--dry-run` | Report what would be ingested |

See `depictio watch --help`.

## :simple-nextflow: Trigger Depictio when a Nextflow run ends

`depictio config nextflow` prints the path of a configuration snippet shipped with the CLI. Given to Nextflow with `-c`, it runs `depictio ingest` on the output folder when the pipeline finishes **successfully**:

```bash
nextflow run nf-core/ampliseq -r 2.18.0 -profile test,docker --outdir results \
    -c $(depictio config nextflow) --depictio_project yourname-ampliseq
```

| Command or parameter | Does |
|---|---|
| `depictio config nextflow --print` | Shows the snippet, to read or copy |
| `depictio config nextflow --install` | Adds it to every `nextflow run` on this machine; `--uninstall` removes it |
| `--depictio_enabled true/false` | Turns it on or off for one run |
| `--depictio_project`, `--depictio_attach`, `--depictio_update` | The same as `--project`, `--attach-run`, `--update-config` |

The CLI reads its server from `~/.depictio/CLI.yaml`, as in the workshop. See [Nextflow trigger](../../workflows/nextflow/trigger.md).

## :material-hammer-wrench: No template for your pipeline

Depictio knows the outputs of 136 tools, from ![MultiQC](../../images/tutorials/workshop/multiqc-icon.svg){ .ws-logo .ws-logo-mono .off-glb } MultiQC, DESeq2, QIIME 2 and MACS2 to Salmon and Kallisto.

```console
$ depictio catalog list
Catalog tools (136)
 Tool            Output                   Keyword   Source   Renders as
 adapterremoval  adapterremoval_settings  …
 agat            agat_gene_models         …
```

`depictio catalog info <tool>` describes one tool. `ingest --compose` builds a project and a dashboard from what the catalog recognises in a folder. On the `multiqc/` folder of the megatest, from `~/depictio-workshop`:

```console
$ depictio ingest megatest/multiqc --compose --project yourname-composed --dry-run
Tabs: Overview, MultiQC
✓ 2 data collection(s) will ingest
• Would import 1 dashboard(s)
✓ Dry run complete (8/8 steps): the configuration is valid, and nothing was changed.
```

Read the list of data collections in the dry run before you ingest. A composed dashboard is a starting point, to export and edit as in [A dashboard as code](dashboard-as-code.md). See [Composed dashboards](../../usage/projects/composed-dashboards.md).

## :material-server-outline: Depictio on your own machine

`depictio local up` starts a complete server on macOS or Linux, without Docker, for your own projects. Install the `[local]` extra in the environment of the workshop, at the version of your CLI, so that there is only one `depictio` command (with pip: `pip install "depictio[local]==1.24.0"`):

```bash
uv pip install "depictio[local]==1.24.0"     # in the active depictio-env, same version as the CLI: the server, and MongoDB, Redis, SeaweedFS from conda-forge
depictio local up --examples penguins        # starts it and opens the browser
depictio ingest --project-config-path penguins-1.yaml --project penguins --server local
depictio local down                          # stops it; your data stays
```

| Command | Does |
|---|---|
| `local up --port 8058` | The port, kept for later runs |
| `local up --examples none` | No demo projects (default: iris and penguins) |
| `local status`, `local open` | Is it running; open it in the browser |
| `local wipe` | Stops it and deletes its data |

Its data lives in `~/.depictio/local`, or in `$DEPICTIO_LOCAL_HOME`. See [Python package installation](../../installation/local.md).

<div class="ws-next" markdown>
[<span class="ws-k">Back to</span><span class="ws-t">The command-line course</span>](index.md){ .ws-help }
[<span class="ws-k">The browser side</span><span class="ws-t">Depictio in the browser</span>](../workshop/index.md){ .ws-go .ws-ep0 }
</div>
