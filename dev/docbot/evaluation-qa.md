# DocBot evaluation questions

Question and answer pairs for DocBot to evaluate its answers on the depictio docs.
Each answer comes from the page named under it; the source is the file in this
repository, the link its published page. Each pair tests a different page or a
different fact. Check them against the docs before each submission: they follow the
docs as of v1.20.0.

Base URL of the published pages: `https://depictio.github.io/depictio-docs/stable/`.

## 1. How do I install Depictio with Docker Compose?

Depictio is open source (MIT License) and free to deploy on your own infrastructure.
Download the compose file with
`curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml`,
then run `docker compose up -d`. It starts MongoDB, Redis, the S3 store (SeaweedFS), the
backend, the viewer and the Celery worker. Depictio is then at <http://localhost:5080>
and the API docs at <http://localhost:8058/docs>, in single-user mode (no login). It
needs Docker 20.10+ and Docker Compose V2.

- Source: `docs/installation/docker.md` (install) and `docs/FAQ/general.md` (license)
- Page: <https://depictio.github.io/depictio-docs/stable/installation/docker/>

## 2. Can I run Depictio without Docker, and move to Docker later?

Yes, from the Python package, on Linux or macOS on Apple silicon with Python 3.11 to
3.14: `uv tool install "depictio[local]"`, then `depictio local up`. It runs MongoDB,
Redis and SeaweedFS fetched from conda-forge, in single-user mode, and serves the viewer
at `http://127.0.0.1:8058/dashboards`. `depictio local down` stops it, and
`depictio local export` copies its data into a directory that
`docker compose up -d` runs.

- Source: `docs/installation/local.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/local/>

## 3. Which login modes does Depictio have, and how do I switch between them?

Four, one active at a time: Auth (login and role-based access), Single-user
(`DEPICTIO_AUTH_SINGLE_USER_MODE=true`, no login, the anonymous user is an admin),
Public (`DEPICTIO_AUTH_PUBLIC_MODE=true`, visitors browse read-only with a 24-hour
temporary account and sign in to create) and Demo (public mode plus
`DEPICTIO_AUTH_DEMO_MODE=true`, which adds a guided tour). In Docker Compose, for a
team instance, set `DEPICTIO_AUTH_SINGLE_USER_MODE=false` in `.env`, together with
`DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` and `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD`.

- Source: `docs/usage/guides/authentication-modes.md`
- Page: <https://depictio.github.io/depictio-docs/stable/usage/guides/authentication-modes/>

## 4. How do I load my pipeline results into Depictio?

Run `depictio ingest <results_dir>`: the template is detected from the pipeline name and
version the run recorded, and `--template nf-core/rnaseq/latest` chooses one yourself.
For a pipeline with no template, pass a project YAML with `--project-config-path project.yaml`.
From v1.16.0, a local results directory that no template fits is composed from the
Tools Catalog instead, and `--dry-run` previews what would be ingested.

- Source: `docs/depictio-cli/usage.md`
- Page: <https://depictio.github.io/depictio-docs/stable/depictio-cli/usage/>

## 5. Which pipelines already have a Depictio template?

Many nf-core pipelines, among them rnaseq, sarek, ampliseq, taxprofiler, atacseq, chipseq,
methylseq and scrnaseq. Each template builds a complete project (data collections,
dashboards and links) from one `depictio ingest` command. The page lists every pipeline
with the versions its template covers.

- Source: `docs/pipeline-templates/nf-core/index.md`
- Page: <https://depictio.github.io/depictio-docs/stable/pipeline-templates/nf-core/>

## 6. How do I make a Nextflow pipeline send its results to Depictio when it finishes?

Set up the Nextflow trigger (v1.10.0+) once, on the machine that runs `nextflow`:
install the CLI with `pip install "depictio[multiqc]"`, save the server credentials to
`~/.depictio/CLI.yaml`, then run `depictio config nextflow --install` and
`depictio config check`. A failed pipeline is never ingested, and an error on
Depictio's side does not change the pipeline's exit status.

- Source: `docs/depictio-cli/nextflow-trigger.md`
- Page: <https://depictio.github.io/depictio-docs/stable/depictio-cli/nextflow-trigger/>

## 7. How do I create a dashboard?

On the landing page, click **+ New Dashboard**, enter a title and click **Create
Dashboard**. Then open it, click **Edit** and **Add component**: pick a component type
(Figure, Card, Interactive, Table, MultiQC, Image, Map, Text or Advanced viz), choose the
workflow and data collection it reads, and customise it. **Pick from catalog** offers
pre-configured visualizations recognised in the project's data instead.

- Source: `docs/usage/guides/web_ui.md` (creating the dashboard) and
  `docs/usage/guides/dashboard_creation.md` (adding components)
- Page: <https://depictio.github.io/depictio-docs/stable/usage/guides/dashboard_creation/>

## 8. What kinds of components can I put on a dashboard?

Figure (Plotly charts, built in UI mode or with Python code), Table, Card (a metric with
an aggregation), Text, Interactive (slider, dropdown, date picker, for filtering),
MultiQC, Image, Map, Genome browser and Advanced viz (ready-made charts such as volcano
plots, Manhattan plots, UMAP embeddings, coverage tracks or phylogenetic trees).

- Source: `docs/features/components.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/components/>

## 9. How do I filter the components of a dashboard?

Add Interactive components (slider, dropdown, date picker) or select on a graph: click a
point or box-select a region of a scatter plot, and the other components update. The
filter panel lists every applied filter with its own clear button, and **Reset all**
clears them.

- Source: `docs/usage/guides/dashboard_usage.md`
- Page: <https://depictio.github.io/depictio-docs/stable/usage/guides/dashboard_usage/>

## 10. Can I share a dashboard with colleagues?

Yes, on the same Depictio instance. A dashboard inherits the permissions of its project,
granted to users or groups with the roles Admin, Editor or Viewer. Send the viewer URL
(`/dashboard/{id}`) to share it. To share a filtered view, copy the filter link
(`#filters=…`) from the filter panel.

- Source: `docs/features/dashboards.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/dashboards/>

## 11. How do I filter MultiQC plots from a sample metadata table?

Link the two data collections, either in the web viewer (data collection actions menu,
**Manage Links**, **Add link**) or in the project YAML under `links`. A link takes the
source data collection (the metadata table), a source column (such as `sample_id`), the
target (the MultiQC data collection) and a resolver such as `sample_mapping`. A filter on
the metadata table then updates the linked plots, with no pre-computed join.

- Source: `docs/features/cross-dc-filtering.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/cross-dc-filtering/>

## 12. When should I use an advanced visualization instead of a normal figure?

When you need a ready-made chart for a common analysis, such as a volcano plot, a
Manhattan plot, an embedding or a coverage track. An advanced visualization knows what
its columns mean (a volcano needs a feature, an effect size and a significance): you map
your columns to those roles once, and the tile adds the thresholds, genomic axes or
linked selections. For a plain plot of any columns, use a Figure.

- Source: `docs/features/advanced-visualizations.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/advanced-visualizations/>

## 13. What is the Tools Catalog?

A browsable list of the bioinformatics tools Depictio integrates. For each tool it shows
the files it emits (data collections) and the dashboard components (renders) they
offer, previewed on real data, with a `use:` snippet to copy. Since v1.16.0,
`depictio ingest` uses it to compose a dashboard for results that no template fits.

- Source: `docs/catalog/index.md`
- Page: <https://depictio.github.io/depictio-docs/stable/catalog/>
## 14. Can I keep dashboards as YAML files under version control?

Yes, with the `depictio dashboard` commands: `export` writes a dashboard to YAML,
`validate` checks a file (schema and domain rules, then columns against the server, or
skip that with `--offline`) and `import` sends it to the server. Re-importing a title
the project already has needs `--overwrite`.

- Source: `docs/features/yaml-sync.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/yaml-sync/>

## 15. What kind of data can I use in Depictio?

Tables (CSV, TSV, Parquet, Excel), MultiQC reports, images (PNG, JPEG, GIF, WebP, SVG,
BMP, TIFF), GeoJSON boundaries for maps, phylogenetic trees (Newick or Nexus),
genome-browser tracks and indexed genomic files (VCF, BAM, bigWig, BED, GFF3, FASTA).
Each kind is a data collection type, and a table with latitude and longitude columns can
also feed a map. Tables become Delta Lake tables on the instance's S3 storage.

- Source: `docs/features/data-model.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/data-model/>
