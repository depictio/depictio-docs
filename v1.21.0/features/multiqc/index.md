# MultiQC

Depictio reads [MultiQC](https://multiqc.info/) reports and draws their plots as dashboard components. A collection can hold the reports of several runs, linked to your sample metadata and compared run against run.

## What Depictio reads

A MultiQC collection reads `multiqc_data/multiqc.parquet`, which MultiQC writes from **v1.29**. The HTML report is not used.

- Each parquet is one report. Its modules, plots and samples are listed from the report itself.
- A collection needs only `type: "MultiQC"`: no scan, metatype or properties. See [YAML examples](https://depictio.github.io/depictio-docs/latest/usage/projects/yaml-examples/index.md) and the [project reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md).
- Each run folder of a pipeline project is scanned for its own `multiqc.parquet`.

## Add reports

### In the browser

When you create a project or click **Add data** on its page, a file or folder holding `multiqc.parquet` is recognised as a MultiQC report. See [Add data to a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#add-data).

For an existing collection, the **Manage data** button opens **Manage Data Collection**:

| Action      | How                                                                                            |
| ----------- | ---------------------------------------------------------------------------------------------- |
| **Append**  | **Modify data**, drop one or more folders holding `multiqc.parquet`. The existing reports stay |
| **Replace** | **Modify data** with **Replace existing data** on: the collection is wiped and ingested again  |
| **Clear**   | **Clear contents**: the data goes, the collection definition stays                             |

Uploads take at most 50 MB per file and 500 MB in all. Only `multiqc.parquet` is extracted from a dropped folder.

### With the CLI

`depictio ingest` reads the reports of every run of the project. `depictio ingest --attach-run` adds a results folder as another run. See the [CLI usage](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/#ingest-command).

### Uniformity

Every create, append and replace checks that the reports agree:

1. the same modules;
1. the same plots in each module;
1. the same MultiQC major.minor version (a patch difference is only logged);
1. no sample name in two reports.

A mismatch is refused with a 422. See [Troubleshooting](#troubleshooting).

## The MultiQC component

In the dashboard editor, pick **MultiQC**, then a **Module** and a **Plot** inside it. Both lists come from the report. Each plot is its own component, and keeps the report's own controls, such as the General Stats read selector. See [Dashboard creation](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/#multiqc-integration).

In [YAML](https://depictio.github.io/depictio-docs/latest/features/yaml-sync/#multiqc-component), both `selected_module` and `selected_plot` are required:

```
- tag: fastqc-quality
  component_type: multiqc
  workflow_tag: python/nf_workflow
  data_collection_tag: multiqc_report
  selected_module: fastqc
  selected_plot: per_base_sequence_quality
```

The General Statistics table, one row per sample and one column per headline metric, uses `general_stats` for both:

```
- tag: general-stats
  component_type: multiqc
  workflow_tag: python/nf_workflow
  data_collection_tag: multiqc_report
  selected_module: general_stats
  selected_plot: general_stats
```

A [composed dashboard](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md) builds a **MultiQC** tab with every plot of the report, and puts General Statistics on its Overview tab. A run with several reports gets one tab each.

## Link to sample metadata

MultiQC sample names rarely match your sample ids (`S1` against `S1_R1`, `S1_R2`). A project-level link with the `sample_mapping` resolver connects a metadata table to the MultiQC collection, so a filter on the table narrows the MultiQC plots:

```
links:
  - source_dc_id: sample_metadata
    source_column: sample_id
    target_dc_id: multiqc_data
    target_type: multiqc
    link_config:
      resolver: sample_mapping
```

See [Cross-DC filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/#resolvers) for the resolvers, the link editor and the mapping inspector. A linked metadata table can also take session labels from the dashboard, which then split the MultiQC plots: see [Metadata panel](https://depictio.github.io/depictio-docs/latest/features/metadata-panel/index.md).

## Compare runs (v1.21.0+)

Append each new run to the same MultiQC collection, and Depictio tells you which samples are new. It needs the changes feature: `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true` ([*"What's new"*](https://depictio.github.io/depictio-docs/latest/features/whats-new/#turn-it-on)).

[![](../../images/guides/multiqc/multiqc-compare-runs.webp)](../../images/guides/multiqc/multiqc-compare-runs.mp4)

1. **Add the run.** Use **Add data** > **Add run**, `depictio ingest --attach-run`, or append its reports with **Manage data**. A run whose reports name samples the project already holds is held back, with the samples listed.
1. **Read the Runs tab.** Each scan lists, per report, the samples and modules it gained or lost. See [Runs and run comparison](https://depictio.github.io/depictio-docs/latest/features/runs/#scans-and-file-statuses).
1. **Open What's new on the dashboard.** The Data section lists the reports added, refreshed or removed, with the new samples and run tags.
1. **Overlay.** The samples you had seen fade, and the new ones keep their own colours. In General Stats, the rows of seen samples fade.
1. **Split.** Each MultiQC figure, General Stats included, is drawn twice: the new samples beside the samples you had seen.
1. **Hide what you had seen.** Only the new samples are drawn.
1. **Before | Now** on a tile draws the reports you saw beside the reports now.

Depictio records the report set a dashboard version was saved with, so a past version, or **Before**, draws the reports it had.

Limits:

- MultiQC rows carry no run column, so MultiQC figures split on samples, not runs.
- Split needs new samples beside seen ones. A report rewritten with the same samples shows only in **Before | Now**.
- A report overwritten in place keeps its storage key, so its **Before** shows today's report. The change is still flagged as refreshed.
- A mark lists at most 5000 samples per collection. Past that, new samples are counted but not listed.

## Performance

- Parsed reports stay resident in the worker across renders, so a dashboard with many MultiQC plots does not read the report again for each plot.
- Set `DEPICTIO_INGEST_MULTIQC_PRERENDER=1` on the CLI to build the figures at ingest and store them in S3. The first open then skips the cold build. It costs ingest time and storage, and applies to new ingests only.
- A refresh keeps the reports whose source did not change.

See [Performance](https://depictio.github.io/depictio-docs/latest/features/performance/#caching).

## Troubleshooting

A refused set of reports answers **422** with code `multiqc_report_mismatch`, a `kind`, a summary naming the two reports, and details:

| `kind`    | Meaning                                             | Fix                                                    |
| --------- | --------------------------------------------------- | ------------------------------------------------------ |
| `modules` | The reports have different module sets              | Run MultiQC with the same modules on every run         |
| `plots`   | A module has a plot in one report and not the other | Same MultiQC configuration on every run                |
| `version` | Different MultiQC major.minor versions              | Regenerate the reports with one MultiQC version        |
| `samples` | A sample name appears in two reports                | Rename the samples, or keep the run as its own project |

An append that fails drops only the new reports, and the collection keeps its data. A replace that fails leaves the collection empty, so append again or replace with a uniform set.

Other issues:

- **No modules to pick**: check that the run holds `multiqc_data/multiqc.parquet`, written by MultiQC 1.29 or later.
- **A filter on the metadata does not reach the plots**: the link needs the `sample_mapping` resolver. Check what it resolves with the [mapping inspector](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/#mapping-inspector).

## See also

- [Runs and run comparison](https://depictio.github.io/depictio-docs/latest/features/runs/index.md)
- [*"What's new"* since your last visit](https://depictio.github.io/depictio-docs/latest/features/whats-new/index.md)
- [Composed dashboards](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md)
- [Components](https://depictio.github.io/depictio-docs/latest/features/components/#multiqc-components)
