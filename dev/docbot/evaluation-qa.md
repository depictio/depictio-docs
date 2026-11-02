# DocBot evaluation questions

Question and answer pairs for DocBot to evaluate its answers on the depictio docs.
Each answer comes from the page named under it; the source is the file in this
repository, the link its published page. Check them against the docs before each
submission: they follow the docs as of v1.17.1.

Base URL of the published pages: `https://depictio.github.io/depictio-docs/stable/`.

## 1. How do I install Depictio with Docker Compose?

Download the compose file with
`curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml`,
then run `docker compose up -d`. It starts MongoDB, Redis, the S3 store (SeaweedFS), the
backend, the viewer and the Celery worker. Depictio is then at <http://localhost:5080>
and the API docs at <http://localhost:8058/docs>. It needs Docker 20.10+ and Docker
Compose V2.

- Source: `docs/installation/docker.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/docker/>

## 2. The Docker Compose install has no login. How do I switch it to multi-user mode?

It starts in single-user mode by default. In the `.env` file, set
`DEPICTIO_AUTH_SINGLE_USER_MODE=false`, along with
`DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` and `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD`, which are
required in multi-user mode and set on first boot, and a strong
`DEPICTIO_S3_ROOT_PASSWORD` (at least 8 characters, not a known default).

- Source: `docs/installation/docker.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/docker/>

## 3. Which authentication modes does Depictio support?

Four, one active at a time: **Auth** (multi-user with login and role-based access),
**Single-user** (no login, the anonymous user is an admin), **Public** (read-only
anonymous browsing, sign-in to create) and **Demo** (public mode plus a guided tour).
Google OAuth is optional in all of them.

- Source: `docs/usage/guides/authentication-modes.md`
- Page: <https://depictio.github.io/depictio-docs/stable/usage/guides/authentication-modes/>

## 4. How can visitors browse my dashboards without an account?

Set `DEPICTIO_AUTH_PUBLIC_MODE=true`. Anonymous visitors get read-only access to public
dashboards. To create or edit, they sign in, either as a temporary user (a 24-hour
session by default, set with `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS`) or with
Google OAuth if it is enabled.

- Source: `docs/usage/guides/authentication-modes.md`
- Page: <https://depictio.github.io/depictio-docs/stable/usage/guides/authentication-modes/>

## 5. How do I deploy Depictio on Kubernetes?

With the Helm chart in the depictio repository: clone `depictio/depictio`, then run
`helm install depictio helm-charts/depictio -f helm-charts/depictio/values.yaml -n depictio --create-namespace`,
and watch the pods with `kubectl get pods -n depictio --watch`. It needs Kubernetes
1.19+, Helm 3.2.0+ and a PV provisioner if persistence is enabled.

- Source: `docs/installation/kubernetes.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/kubernetes/>

## 6. Can I run Depictio without Docker?

Yes, from the Python package, on Linux or macOS on Apple silicon with Python 3.11 to
3.14: `uv tool install "depictio[local]"`, then `depictio local up`. It runs MongoDB,
Redis and SeaweedFS fetched from conda-forge, in single-user mode, and serves the viewer
at `http://127.0.0.1:8058/dashboards`. `depictio local down` stops it.

- Source: `docs/installation/local.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/local/>

## 7. How do I move a server started with `depictio local up` to Docker Compose?

Run `depictio local export`, then `cd depictio-docker && docker compose up -d`. The
export stops the local server and copies its projects, dashboards and table data into a
directory that Docker Compose runs.

- Source: `docs/installation/local.md`
- Page: <https://depictio.github.io/depictio-docs/stable/installation/local/>

## 8. How do I load nf-core/rnaseq results into Depictio?

With the CLI and the bundled template:
`depictio ingest /path/to/rnaseq_results/aligner_star_salmon --template nf-core/rnaseq/latest`.
The template builds the project and its dashboards from the results directory.

- Source: `docs/pipeline-templates/nf-core/rnaseq.md`
- Page: <https://depictio.github.io/depictio-docs/stable/pipeline-templates/nf-core/rnaseq/>

## 9. My pipeline has no Depictio template. How can I still ingest its results?

Pass a project YAML with `depictio ingest <DATA_DIR> --project-config-path project.yaml`.
From v1.16.0, without `--template` or `--project-config-path`, a local results
directory that no bundled template fits is composed from the catalog instead.

- Source: `docs/depictio-cli/usage.md`
- Page: <https://depictio.github.io/depictio-docs/stable/depictio-cli/usage/>

## 10. How do I make a Nextflow pipeline send its results to Depictio when it finishes?

Set up the Nextflow trigger (v1.10.0+) once, on the machine that runs `nextflow`:
install the CLI with `pip install "depictio[multiqc]"`, save the server credentials to
`~/.depictio/CLI.yaml`, then run `depictio config nextflow --install` and
`depictio config check`. A failed pipeline is never ingested, and an error on
Depictio's side does not change the pipeline's exit status.

- Source: `docs/depictio-cli/nextflow-trigger.md`
- Page: <https://depictio.github.io/depictio-docs/stable/depictio-cli/nextflow-trigger/>

## 11. How do I filter MultiQC plots from a sample metadata table?

Link the two data collections in the project YAML, under `links`, with
`source_dc_id` (the metadata table), `source_column` (such as `sample_id`),
`target_dc_id` (the MultiQC data collection), `target_type: multiqc` and a
`link_config` resolver such as `sample_mapping`. A filter on the metadata table then
updates the linked plots, with no pre-computed join.

- Source: `docs/features/cross-dc-filtering.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/cross-dc-filtering/>

## 12. Do Depictio backups include my data tables?

No. A backup snapshots MongoDB: users, projects, dashboards, data collection
definitions, file records, the locations of the Delta tables and the instance settings.
The Delta tables and files in object storage are not included. To copy them too, use
`depictio backup create --include-s3-data --s3-backup-prefix backup`, or back up the
object store itself. Backups need an administrator account.

- Source: `docs/usage/administration/backup.md`
- Page: <https://depictio.github.io/depictio-docs/stable/usage/administration/backup/>

## 13. How do I embed a dashboard component in another website?

Since v1.17.0, an administrator turns the export API on with
`DEPICTIO_FASTAPI_EMBED_ENABLED=true`, and lists the sites allowed to frame it in
`DEPICTIO_FASTAPI_EMBED_ALLOWED_ORIGINS`. Each tile then has an **Export / embed**
action that gives a Plotly spec (JSON) for the site's own plotly.js, or a
self-contained HTML page for an `<iframe>`.

- Source: `docs/features/component-export.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/component-export/>

## 14. Can I keep dashboards as YAML files under version control?

Yes, with the `depictio dashboard` commands: `export` writes a dashboard to YAML,
`validate` checks a file (schema and domain rules, then columns against the server, or
skip that with `--offline`) and `import` sends it to the server.

- Source: `docs/features/yaml-sync.md`
- Page: <https://depictio.github.io/depictio-docs/stable/features/yaml-sync/>

## 15. Is Depictio free and open source?

Yes. Depictio is open source under the MIT License and free to deploy on your own
infrastructure. It is developed at the EMBL Data Science Centre in Heidelberg.

- Source: `docs/FAQ/general.md`
- Page: <https://depictio.github.io/depictio-docs/stable/FAQ/general/>
