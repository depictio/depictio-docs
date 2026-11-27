---
glightbox: true
title: "2. An nf-core run from the terminal"
description: "Turn an nf-core/ampliseq results folder into a Depictio project with no project file, the template detected from the run; a dry run first, then the ingestion."
---

# 2. An nf-core run from the terminal

<div class="ws-strip" markdown>
[**0** Setup](setup.md){ .ws-ep0 } [**1** Your tables](project-builder.md){ .ws-ep1 } [**2** nf-core run](nf-core-run.md){ .ws-ep2 .ws-here } [**3** Collaborate](collaborate-and-export.md){ .ws-ep3 } [**+** Going further](going-further.md){ .ws-ep4 }
</div>

<div class="ws-meta ws-ep2" markdown>
<span class="ws-chip" markdown="span">:material-console: **Creator, from the terminal**</span> <span class="ws-chip" markdown="span">![nf-core](../../images/pipeline-templates/nf-core/ampliseq/nf-core.png){ .ws-logo .off-glb } **nf-core/ampliseq 2.18.0**</span> <span class="ws-chip" markdown="span">:material-timer-outline: **Hands-on 2 · 15 min**</span>
</div>

!!! overview "Overview"
    **Objective**: send an nf-core run to Depictio from your terminal, with no project file: check what will happen with a dry run, then ingest it into a project of your own.

    The core of this page takes about 5 minutes to read. The rest is in the **Bonus** blocks at the end.

In episode 1 you described your own tables in the Project Builder. For a pipeline Depictio knows, a **template** writes it: the CLI recognises the pipeline and its version from the results folder, and brings the data collections, links and dashboards with it. This is the project of the browser course, episode 3, built here from the folder where the run is.

![depictio ingest in four steps: it finds the pipeline, picks the template (GROUP_COL guessed as name, set to habitat with --var), writes the tables (25 data collections, 2 of them empty) and builds the dashboard; --dry-run checks the same steps and sends nothing](../../images/tutorials/workshop-cli/diagrams/ingest-steps_light.png#only-light){ .ws-diagram }
![depictio ingest in four steps: it finds the pipeline, picks the template (GROUP_COL guessed as name, set to habitat with --var), writes the tables (25 data collections, 2 of them empty) and builds the dashboard; --dry-run checks the same steps and sends nothing](../../images/tutorials/workshop-cli/diagrams/ingest-steps_dark.png#only-dark){ .ws-diagram }

## :material-folder-download-outline: Hands-on 2 · Step 1: get the run { #get-the-run }

Download [`megatest.zip`](megatest.zip): your browser saves it in `~/Downloads`. Move it to the workshop folder and unzip it there:

```bash
mv ~/Downloads/megatest.zip ~/depictio-workshop/
cd ~/depictio-workshop
unzip megatest.zip
ls megatest
```

```console
input  multiqc  overall_summary.tsv  pipeline_info  qiime2
```

This episode runs in `~/depictio-workshop`, the folder that holds `megatest/`.

## :material-clipboard-check-outline: Step 2: dry run, then dry run with the variable { #dry-run }

You write no project file: the template of nf-core/ampliseq 2.18.0 is one, written once for every run of that version. Always pass `--project` with a name of your own, here `yourname-ampliseq`: without it, the template's default name is used, *Ampliseq Microbial Community Analysis*, which is also the name of the server's demo project.

```console
$ depictio ingest megatest/ --project yourname-ampliseq --dry-run
…
! 21 data collection(s) will ingest, 0 empty, 4 missing sources
…
✓ Dry run complete (8/8 steps): the configuration is valid, and nothing was changed.
```

It sends nothing to the server. The full output is in the Bonus block *The dry run, line by line*.

!!! challenge "Challenge 2.1: what is missing?"
    In the dry run's tables, find the **template variables** and the data collections marked **missing**. Which variable explains why `ancombc_results` finds no files?

    ??? solution "Solution"
        `GROUP_COL` reads `name`: the CLI took the first column after the sample ID in the sample metadata (`input/Metadata_full.tsv`), here `name`, as the group to compare. `name` holds one value per sample, so each group has a single sample and nothing can be compared. The differential abundance results of this run are per **habitat** (`qiime2/ancombc/differentials/Category-habitat-…`), so `ancombc_results`, and `ma_canonical` which is built from it, find nothing. Set the variable yourself, in the second dry run below.

Run the dry run again with the variable:

```console
$ depictio ingest megatest/ --project yourname-ampliseq --dry-run --var GROUP_COL=habitat
! 23 data collection(s) will ingest, 0 empty, 2 missing sources
```

The two left are the SIDLE collections, for multi-region runs: this run has none, and they are optional.

## :material-database-import-outline: Step 3: ingest and open the dashboard { #ingest }

The same command without `--dry-run`, with `--var GROUP_COL=habitat` from challenge 2.1: the differential abundance of this run compares habitats.

```console
$ depictio ingest megatest/ --var GROUP_COL=habitat --project yourname-ampliseq
…
✓ Data collection 'taxonomy_composition' processed successfully. Recipe 'qiime2/taxonomy_composition.py' result written to s3://…
…
✓ Processing completed! Total data collections processed: 23 (2 optional skipped: sidle_reconstructed, sidle_reconstruction_qc)
…
• Project: https://…/projects/…
• Dashboard 'nf-core/ampliseq' created: https://…/dashboard/…
! Skipped 2 optional data collection(s), their inputs are absent from this run: sidle_reconstructed, sidle_reconstruction_qc
✓ Ingestion completed successfully! (8/8 steps)
```

Each ✓ line is one table written to the server's storage; a recipe line names the script that computed it. Then the template's dashboard is created, and the CLI prints the addresses. Open the **Project** link:

![Your project: the pipeline and its version (1), 25 data collections (2), and the dashboard the template built (3)](../../images/tutorials/workshop-cli/ep4_project.webp){ .ws-shot }

From the project, open the **nf-core/ampliseq** dashboard (3).

!!! warning "Without `--var GROUP_COL=habitat`"
    The ingestion stops at `ma_canonical` with *Data processing failed*: always pass the variable for this run.

!!! question "Check your understanding"
    You run the same command twice, with and without `--dry-run`. What does the dry run change on the server? And why do you pass `--project` and `--var GROUP_COL=habitat`?

    ??? solution "Answer"
        Nothing: the dry run checks the same steps and sends nothing. `--project` names your project; without it, the template's default name is used, *Ampliseq Microbial Community Analysis*, which is also the name of the server's demo project. `--var GROUP_COL=habitat` sets the variable the CLI guessed wrong (`name`): without it, the ingestion stops at `ma_canonical`.

!!! keypoints "Key points"
    - `depictio ingest <folder>` detects the pipeline and its version, and picks the template.
    - `--dry-run` shows what each data collection finds, without sending anything: read it first.
    - `--var` sets a template variable the CLI guessed wrong; `--project` names the project: always pass it.

??? note "Bonus · The run: an nf-core megatest"
    nf-core tests each release of a pipeline on a full-size dataset, on cloud computers, and publishes the results on the pipeline's website (the **Results** tab of [nf-co.re/ampliseq/2.18.0](https://nf-co.re/ampliseq/2.18.0)). These runs are called **megatests**: real, public runs of a known version. The ampliseq 2.18.0 megatest sequenced 16S amplicons of 12 samples from soil, sediment and water. The browser course, episode 3, read the same run from its public storage.

    The full results are much larger: 13 folders, 3,557 files, 487 MB, with the trimming, denoising, FastQC, PICRUSt and placement outputs. The Depictio template reads only five parts of them, and `megatest.zip` (1.4 MB, 37 files) holds just those: `pipeline_info/`, `input/`, `multiqc/`, `overall_summary.tsv` and `qiime2/`. Nothing the template reads is left out, so you get the same tables as in the browser course.

    This is the run you unzipped in step 1. What each part of it holds, and what Depictio makes of it:

    | In `megatest/` | What the pipeline wrote | What Depictio reads in it |
    |---|---|---|
    | `pipeline_info/` | the run's parameters (`params.json`) and the versions of its tools (`software_versions.yml`) | which pipeline and which version this is; which options the run used |
    | `input/` | the sample sheet and the sample metadata, `Metadata_full.tsv` | the `samplesheet` and `metadata` tables, and the columns to group samples by |
    | `multiqc/` | the data of the MultiQC report: read quality, adapter trimming | the `multiqc_data` table |
    | `overall_summary.tsv` | how many reads each sample keeps at each step | the `read_tracking` table |
    | `qiime2/` | taxonomy, diversity, differential abundance, the phylogenetic tree | most of the other tables |

??? note "Bonus · The dry run, line by line"
    The full output of the first dry run, shortened: … marks the lines left out.

    ```console
    $ depictio ingest megatest/ --project yourname-ampliseq --dry-run
    • Detected nf-core/ampliseq 2.18.0 (nextflow, 20 tool(s)) [[1]]
    ✓ Auto-selected template: nf-core/ampliseq/2.18.0 [[1]]
    …
                              Resolved template variables
    ╭───────────────────┬──────────────────────────────────────────────────────────╮
    │ Variable          │ Value                                                    │ [[2]]
    ├───────────────────┼──────────────────────────────────────────────────────────┤
    │ ANNOTATION_COLS   │ name,habitat,Riv_vs_Gro,Sed_vs_Soil                      │ [[2]]
    │ GROUP_COL         │ name                                                     │ [[2]]
    │ GROUP_COL_DISPLAY │ Name                                                     │ [[2]]
    │ METADATA_ID_COL   │ ID                                                       │ [[2]]
    ╰───────────────────┴──────────────────────────────────────────────────────────╯
    …
                         Data collections under this data root
    ╭──────────────────────────────────────┬────────┬───────────┬───────┬─────────╮
    │ Data collection                      │ Kind   │ Mode      │ Files │ Status  │ [[3]]
    ├──────────────────────────────────────┼────────┼───────────┼───────┼─────────┤
    │ multiqc_data                         │ scan   │ recursive │ 1     │ ok      │ [[3]]
    │ samplesheet                          │ scan   │ single    │ 1     │ ok      │ [[3]]
    │ metadata                             │ scan   │ single    │ 1     │ ok      │ [[3]]
    │ …                                    │        │           │       │         │ [[3]]
    │ taxonomy_composition                 │ recipe │ -         │ 1     │ ok      │ [[3]]
    │ ancombc_results                      │ recipe │ -         │ 0     │ missing │ [[3]]
    │ ma_canonical                         │ recipe │ -         │ 1     │ missing │ [[3]]
    │ sidle_reconstructed                  │ recipe │ -         │ 0     │ missing │ [[3]]
    │ sidle_reconstruction_qc              │ recipe │ -         │ 0     │ missing │ [[3]]
    ╰──────────────────────────────────────┴────────┴───────────┴───────┴─────────╯
    ! Sources not found under this data root: [[4]]
    ! ancombc_results: qiime2/ancombc/differentials/Category-name-level-3/lfc_slice*.csv, qiime2/ancombc/differentials/Cat… [[4]]
    ! ma_canonical: collection 'ancombc_results' [[4]]
    ! sidle_reconstructed: sidle/reconstructed/reconstructed_merged.tsv [[4]]
    ! sidle_reconstruction_qc: sidle/DB/3_reconstructed/reconstruction_summary/metadata.tsv [[4]]
    ! 21 data collection(s) will ingest, 0 empty, 4 missing sources [[4]]
    …
    ✓ Dry run complete (8/8 steps): the configuration is valid, and nothing was changed.
    ```

    Read it from the top:

    1. **Detected nf-core/ampliseq 2.18.0**: the CLI read `pipeline_info/` and picked the template of that pipeline and version.
    2. **Resolved template variables**: the template has blanks the run fills in. `GROUP_COL` is the column of the sample metadata used to compare groups of samples; the CLI guessed `name`, the name of each sample: a group of one sample each, wrong for this run.
    3. **Data collections under this data root**: one line per table of the template, with the number of files it found. A `scan` table is a file read as it is; a `recipe` table is computed from one or more files of the run by a script that ships with the template (`taxonomy_composition` is built from the taxonomy tables in `qiime2/`).
    4. **4 missing sources**: four tables found no file. The `!` lines say which file each one looked for. Two of them, `sidle_reconstructed` and `sidle_reconstruction_qc`, are optional: SIDLE rebuilds one profile from several amplified regions, and this run has a single region, so there is nothing to find and the ingest skips them with a message. Why the other two, `ancombc_results` and `ma_canonical`, find nothing is challenge 2.1.

??? note "Bonus · Challenge 2.2: the same project as in the browser?"
    Open your project in the browser, **Projects → yourname-ampliseq**. How many data collections and links does it have? How many tabs has its dashboard? Compare with episode 3 of the browser course.

    ??? solution "Solution"
        25 data collections and 21 links; the dashboard has 7 tabs: Overview, MultiQC, Alpha Diversity, Ordination & Clustering, Community & Diversity, Differential Abundance, Phylogeny. The browser course counted 23 and 19 from the template, before the tables you added there: the CLI keeps the two optional SIDLE collections, empty, and the two links that reach them. The run is named `megatest`, after the folder.

??? note "Bonus · More options of `depictio ingest`"
    `depictio ingest --help` lists the other options: `--template` to force a template, `--update-config` to refresh a project after you change something.

<div class="ws-next" markdown>
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md#episode-2){ .ws-help }
[<span class="ws-k">Then</span><span class="ws-t">Collaborate and export</span>](collaborate-and-export.md){ .ws-go .ws-ep3 }
</div>
