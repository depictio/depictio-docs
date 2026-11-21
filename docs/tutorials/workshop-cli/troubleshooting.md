---
title: "Troubleshooting"
description: "Problems met in the Depictio command-line course, episode by episode, with their cause and fix."
---

# Troubleshooting

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-lifebuoy: **For learners**</span> <span class="ws-chip" markdown="span">:material-school-outline: **Instructors: see Instructor notes**</span>
</div>

When you ask for help in the chat, paste the **last lines** of the output, never your `CLI.yaml`.

## :material-numeric-0-circle-outline: Setup { #setup .ws-ep0 }

| Symptom | Cause | Fix |
|---|---|---|
| `depictio: command not found` | The environment is not active in this terminal | `source depictio-env/bin/activate` |
| `requires a different Python` | Python older than 3.11 | Install Python 3.12; with uv: `uv venv --python 3.12 depictio-env` |
| `pip install` fails on Python 3.14, on `beanie` | A dependency does not support Python 3.14 yet | Create the environment with Python 3.12: `python3.12 -m venv depictio-env`, or with uv `--python 3.12` |
| *No server configured…* | `CLI.yaml` is missing, or not in `~/.depictio/` | Download it again from **Account settings → CLI agents**, and move it to `~/.depictio/CLI.yaml` |
| `s3_storage.browser_access: Extra inputs are not permitted`, or HTTP 422 | The CLI and the server run different versions | Install the CLI at the server's exact version (ask the instructor) |
| `config check` cannot reach the server | `CLI.yaml` is not in `~/.depictio/`, or the network blocks the server | `ls ~/.depictio/CLI.yaml`; try another network, or ask the instructor |
| The server answers, the storage does not | The storage endpoint is blocked on your network | Tell the instructor: the CLI needs both |

## :material-numeric-1-circle-outline: Episode 1 { #episode-1 .ws-ep1 }

| Symptom | Cause | Fix |
|---|---|---|
| `✗ --project-config-path does not exist or is not a file: penguins-1.yaml` | The command runs outside `penguins-workshop/` | `cd penguins-workshop` |
| *The directory 'seasons/season_2007' does not exist.* | The command runs outside `penguins-workshop/` | `cd penguins-workshop` |
| *would match no file* in the dry run | The pattern has a typo | Check `pattern:` |
| *Project '…' already exists on this server* | The name is taken, by you or by someone else | Another `--project` name; for your own project, `--update-config` refreshes it |
| No dashboard in the project | `--dashboard starter.yaml` was left out | `depictio dashboard import starter.yaml --project <project ID>` |

## :material-numeric-2-circle-outline: Episode 2 { #episode-2 .ws-ep2 }

| Symptom | Cause | Fix |
|---|---|---|
| *Environment variable 'SEASON_DIR' is not set* | The variable goes on the same line as the command | `SEASON_DIR=seasons/season_2007 depictio ingest …` |
| Still one data collection after the refresh | `--update-config` was left out, or `penguins-1.yaml` was used | Run again with `penguins.yaml` and `--update-config` |
| An info line: *this data location is already one of the project's runs* | The same season was attached twice; the ingestion still succeeds | Nothing to fix; attach `season_2008` for the new season |
| **Compare** greyed on season_2007 | The first run has nothing before it | Expected; compare **season_2008** |

## :material-numeric-3-circle-outline: Episode 3 { #episode-3 .ws-ep3 }

| Symptom | Cause | Fix |
|---|---|---|
| *HTTP 409 … already exists in this project* | A dashboard with this title exists | A new title, or `--overwrite` |
| The project file `penguins.yaml` now holds a dashboard | It was given as the export's `-o` | Export to `dashboard.yaml`; download the zip again for `penguins.yaml` |
| *Either project_id parameter or project_tag in YAML is required* | The file has no `project_tag` | Keep the `project_tag` line of the export |
| A new figure stays empty | A column name in `figure_params` is wrong; validate does not check them | Check the column names |
| A wrong column only warns | Column checks count only with a server named | `depictio dashboard validate dashboard.yaml --server ~/.depictio/CLI.yaml` |

## :material-numeric-4-circle-outline: Episode 4 { #episode-4 .ws-ep4 }

| Symptom | Cause | Fix |
|---|---|---|
| *MultiQC is not installed* | `depictio` installed without the extra | `pip install "depictio[multiqc]~=1.23.0"` |
| *Failed to process data collection 'ma_canonical'* | `GROUP_COL` guessed as `name` | Run again with `--var GROUP_COL=habitat` and `--update-config` |
| *Project '…' already exists on this server* | The name is taken, by you or by someone else | Another `--project` name; for your own project, `--update-config` refreshes it |
| 25 data collections, not 23 | The CLI keeps the two optional SIDLE collections, empty | Expected |
