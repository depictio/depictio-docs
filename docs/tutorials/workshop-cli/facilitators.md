---
glightbox: true
title: "Instructor notes"
description: "Prepare a throwaway Depictio server for Day 2 of the hands-on workshop, the files learners download, and the checks before the session."
---

# Instructor notes

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-school-outline: **For instructors**</span>
</div>

## :material-timer-outline: Schedule, Day 2 (16 December) { #schedule }

| Time | Block | What happens | Page |
|---|---|---|---|
| 10:00 | Welcome | 5 min | [0. Setup](setup.md) |
| 10:05 | Episode 1: your own tables, the Project Builder (browser), **Hands-on 1** (10 min) | Source and project, two collections that scan both seasons, preview, create; on the project page **Add join** on `individual_id`; a figure on the joined table | [1. Your own tables, no template](project-builder.md) |
| 10:25 | The command line (10 min) | `CLI.yaml`, `depictio config check`, `depictio ingest` | [0. Setup](setup.md) |
| 10:35 | Episode 2: an nf-core run from the terminal, **Hands-on 2** (15 min) | `depictio ingest` on a run, with its template | [2. An nf-core run from the terminal](nf-core-run.md) |
| 11:00 | Break | 10 min | |
| 11:10 | Episode 3: collaborate and export (browser), **Hands-on 3** (15 min) | On the learner's copy of the ampliseq dashboard: label in Metadata mode, comment and annotate, a component's History, export **Dashboard only** and open it offline | [3. Collaborate and export](collaborate-and-export.md) |
| 11:35 | Wrap-up | The Nextflow end-of-run demo | [Going further](going-further.md) |
| 11:45 | Questions | 15 min | |

The three older episodes, a project file by hand, a new season and a dashboard as code, are now under [Going further](going-further.md): they are not timed.

## :material-server-outline: A server for this day only { #server }

Every learner downloads a `CLI.yaml` from their account. That file carries the **access key of the server's object storage**: the CLI writes the tables there itself. On a shared server, every learner can then read and change everything in that storage.

Run Day 2 on a server set up for it, and delete it afterwards:

| What | Why |
|---|---|
| Depictio **1.24.0**, with its own object storage, empty at the start | Nothing else is reachable with the storage key |
| The API **and** the storage endpoint reachable from the learners' laptops | The CLI talks to both |
| One account per learner, allowed to create projects, plus a few spares; **not** single-user or public mode | Projects are created from the command line; in those modes only the admin can download a `CLI.yaml` |
| Learners set their own password at the first sign-in | The accounts are new on this server; until the password is changed, the server refuses the CLI too (*Change your password first.*) |
| Storage keys rotated just before the session | Keys from a test run do not work on the day |
| Server and storage deleted after the session | The keys handed out stop mattering |

Tell learners at the start that the server and everything on it are deleted after the session.

!!! danger "Version pins"
    The pins read `==1.24.0`, the exact version of the server: learners check that `depictio --version` prints it. If the server is upgraded, even to a patch release, change every pin and that line of setup.md. A 1.21 CLI cannot read the `CLI.yaml` of a 1.22.0 to 1.22.2 server: every command after `depictio --version` fails with *s3_storage.browser_access: Extra inputs are not permitted*. Later servers leave that setting out of the file, and later CLIs skip keys they do not know with a warning, but the same version on both sides is the only setup the lesson was rehearsed with. The pins are in [Setup](setup.md) (the uv and pip install lines, and the expected `depictio --version`), in [Going further](going-further.md) (the `[local]` install, with uv and pip), and in this lesson's [Troubleshooting](troubleshooting.md) (the MultiQC row).

## :material-folder-network-outline: The penguins folder for the Project Builder { #penguins-bucket }

Episode 1 reads a **folder in a bucket**, not files from a laptop. Before the day, upload the two season folders of [`penguins-workshop.zip`](penguins-workshop.zip) (`seasons/season_2007/` and `seasons/season_2008/`, two CSV files each) to a bucket the server can reach, as `s3://<workshop-bucket>/penguins/`, and announce the location in the chat. If the bucket is private, give the endpoint, the access key and the secret too: the form asks for them and **Test connection** checks them. Replace the screenshot of step 1 on the episode page (it shows a local test endpoint) once the location is decided.

The learner page says the location is in the chat: paste it there at the start of the hands-on. Tested on 1.24.0: the builder ingests both collections in about 4 s; **Add join** previews *223 rows → joined: 223 rows · 12 columns* and creates `joined_physical_features_demographic_data` in a few seconds. On 1.24.0 the builder's review step still says joins go through the YAML and **Download YAML** gives a template (`template:` block, `{DATA_ROOT}`): both are fixed in 1.24.1 ([PR #1493](https://github.com/depictio/depictio/pull/1493)). If the server is still on 1.24.0, tell the room to use **Add join** on the project page.

For episode 3, every learner needs a dashboard of their own to work on: their copy of **nf-core/ampliseq** from Day 1, or a duplicate made on the spot. The exports (`DEPICTIO_STATIC_EXPORT_ENABLED=true`) and viewers' comments (`DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT=true`) must be on, as on Day 1's server.

## :material-download-outline: Files learners download

All are linked from the episode pages:

| Episode | File |
|---|---|
| Going further, and episode 1 as a local copy | [`penguins-workshop.zip`](penguins-workshop.zip), 6 KB: `penguins-1.yaml` (a project file by hand), `penguins.yaml` (a new season), `starter.yaml`, `seasons/season_2007/`, `seasons/season_2008/` |
| 2 | [`megatest.zip`](megatest.zip), 1.4 MB: the nf-core/ampliseq 2.18.0 megatest outputs (`input/`, `multiqc/`, `pipeline_info/`, `qiime2/`, `overall_summary.tsv`) |

## :material-alert-outline: Known behaviours

- Episode 2 needs `--var GROUP_COL=habitat`: with the run's raw metadata the CLI picks `name`, and the ingestion stops at `ma_canonical`.
- The CLI keeps the two optional SIDLE collections, empty: 25 data collections and 21 links, against 23 and 19 on Day 1.
- `dashboard validate` checks card and filter columns only with `--server`; columns in `figure_params` are never checked.
- `dashboard import` matches by title: a new title makes a new dashboard, `--overwrite` updates one.

## :material-human-male-board: Running an episode

1. **Before**: run the episode's first command on the shared screen, with a learner account.
2. **During**: learners signal done or stuck in the chat. A helper answers with a link to the step; errors are easiest to read when the learner pastes the last lines of the output.
3. **After**: go through the challenges' solutions on the shared screen.

## :material-clipboard-check-outline: Checks before the day

- With a fresh learner account and a fresh Python environment: [Setup](setup.md), then each episode as written, checking each solution.
- `depictio config check` from a laptop on the EMBL network and from one outside it.
- Episodes 1 and 2 with many accounts at once: every learner sends the same files.
