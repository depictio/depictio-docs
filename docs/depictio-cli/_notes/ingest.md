<!-- Hand-written, included in usage.md by scripts/cli-reference/render.py. Links are relative to usage.md. -->

Variables: `DEPICTIO_INGEST_STREAMING_WRITE` (as `--streaming`), `DEPICTIO_INGEST_DC_WORKERS` (collections in parallel, 1 to 4), `DEPICTIO_INGEST_JOB_TIMEOUT_SECONDS` (`--async-upsert` wait, 3600).

### Refreshing a project { #refreshing-a-project }

If the project exists, `ingest` changes nothing and exits 2. Say what you meant:

| Option | What happens |
| --- | --- |
| `--update-config` | Configuration updated, every run rescanned, tables rebuilt, dashboards kept as edited and missing template ones added. Creates an absent project, so scripts can always pass it |
| `--attach-run` | `DATA_DIR` added as another run, tables rebuilt, dashboards kept |
| `--reset-dashboards` | As `--update-config`, then the template's dashboards replace the edited ones, titles kept |

- Workflows and collections the project file does not name, such as ones added in the web UI, are kept.
- Dashboards are matched by the file they came from, not their title, and gain the template tabs they lack. Subtitle, icons and tab order edited in the viewer are reset.
- Runs of `DATA_DIR` and of attached folders are kept, others removed. An attached folder missing here stops the refresh (exit 1) unless `--drop-missing-runs`.

### Result file { #result-json }

`--result-json FILE` writes `status` (`success`, `partial` or `exists`), `project` (`name`, `id`, `url`), `dashboards` in import order with their `status` (`created`, `kept`, `replaced`), `template_id`, and `composed` (`template_dir`, `tabs`, `unrecognised`) for a composed template. A failed step writes no file.

### Exit codes { #exit-codes }

| Code | Meaning |
| --- | --- |
| `0` | Every step completed |
| `1` | A step failed (even under `--continue-on-error`), unusable configuration, attached run missing, or nothing to compose |
| `2` | Nothing done: no template found, project exists, `--attach-run` project absent, or usage error |
