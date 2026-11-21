---
title: "Instructor notes"
description: "Prepare a throwaway Depictio server for Day 2 of the hands-on workshop, the files learners download, and the checks before the session."
---

# Instructor notes

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-school-outline: **For instructors**</span>
</div>

## :material-server-outline: A server for this day only { #server }

Every learner downloads a `CLI.yaml` from their account. That file carries the **access key of the server's object storage**: the CLI writes the tables there itself. On a shared server, every learner can then read and change everything in that storage.

Run Day 2 on a server set up for it, and delete it afterwards:

| What | Why |
|---|---|
| Depictio **v1.23** or later, with its own object storage, empty at the start | Nothing else is reachable with the storage key |
| The API **and** the storage endpoint reachable from the learners' laptops | The CLI talks to both |
| One account per learner, allowed to create projects, plus a few spares; **not** single-user or public mode | Projects are created from the command line; in those modes only the admin can download a `CLI.yaml` |
| Storage keys rotated just before the session | Keys from a test run do not work on the day |
| Server and storage deleted after the session | The keys handed out stop mattering |

Tell learners at the start that the server and everything on it are deleted after the session.

!!! danger "Version pins"
    The pins read `~=1.23.0`: any 1.23 release, the line the server runs. If the server runs another minor version, change every pin to it. A 1.21 CLI cannot read the `CLI.yaml` of a 1.22.0 to 1.22.2 server: every command after `depictio --version` fails with *s3_storage.browser_access: Extra inputs are not permitted*. Later servers leave that setting out of the file, and later CLIs skip keys they do not know with a warning, but the same version on both sides is the only setup the lesson was rehearsed with. The pins are in [Setup](setup.md) (the uv and pip install lines, and the expected `depictio --version`), in [Going further](going-further.md) (the `[local]` install, with uv and pip), and in this lesson's [Troubleshooting](troubleshooting.md) (the MultiQC row).

## :material-download-outline: Files learners download

All are linked from the episode pages:

| Episode | File |
|---|---|
| 1, 2, 3 | [`penguins-workshop.zip`](penguins-workshop.zip), 6 KB: `penguins-1.yaml` (episode 1), `penguins.yaml` (episode 2), `starter.yaml`, `seasons/season_2007/`, `seasons/season_2008/` |
| 4 | [`megatest.zip`](megatest.zip), 1.4 MB: the nf-core/ampliseq 2.18.0 megatest outputs (`input/`, `multiqc/`, `pipeline_info/`, `qiime2/`, `overall_summary.tsv`) |

## :material-alert-outline: Known behaviours

- Episode 2 relies on `--update-config` keeping the single `season_2007` run when its location changes from `seasons/season_2007` to `{SEASON_DIR}`, and on `--attach-run` for `season_2008`: the first run never offers **Compare**.
- Episode 4 needs `--var GROUP_COL=habitat`: with the run's raw metadata the CLI picks `name`, and the ingestion stops at `ma_canonical`.
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
- Episodes 1 and 2 with many accounts at once, and episode 4 if it is run: every learner sends the same files.
