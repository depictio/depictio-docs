---
glightbox: true
title: "Troubleshooting"
description: "Problems met in the Depictio command-line course, with their cause and fix."
---

# Troubleshooting

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-lifebuoy: **For learners**</span> <span class="ws-chip" markdown="span">:material-school-outline: **Instructors: see Instructor notes**</span>
</div>

When you ask for help in the chat, paste the **last lines** of the output, never your `CLI.yaml`.

## :material-numeric-0-circle-outline: Setup { #setup .ws-ep0 }

| Symptom | Cause | Fix |
|---|---|---|
| `depictio: command not found` | The environment is not active in this terminal | `source ~/depictio-workshop/depictio-env/bin/activate` |
| `requires a different Python` | Python older than 3.11 | Install Python 3.12; with uv, in `~/depictio-workshop`: `uv venv --python 3.12 depictio-env` |
| `pip install` fails on Python 3.14, on `beanie` | A dependency does not support Python 3.14 yet | Create the environment with Python 3.12, in `~/depictio-workshop`: `python3.12 -m venv depictio-env`, or with uv `--python 3.12` |
| *Change your password first.* (HTTP 403) | The account still has the password from the e-mail | Sign in in the browser and set your own password, then run the command again |
| *No server configured…* | `CLI.yaml` is missing, or not in `~/.depictio/` | Download it again from **Account settings → CLI agents**, and move it to `~/.depictio/CLI.yaml` |
| `s3_storage.browser_access: Extra inputs are not permitted`, or HTTP 422 | The CLI and the server run different versions | Install the CLI at the server's exact version (ask the instructor) |
| `config check` cannot reach the server | `CLI.yaml` is not in `~/.depictio/`, or the network blocks the server | `ls ~/.depictio/CLI.yaml`; try another network, or ask the instructor |
| The server answers, the storage does not | The storage endpoint is blocked on your network | Tell the instructor: the CLI needs both |

## :material-numeric-1-circle-outline: Episode 1 · Your own tables { #project-builder .ws-ep1 }

| Symptom | Cause | Fix |
|---|---|---|
| The form asks for an Endpoint, an Access key and a Secret | The bucket is not public: the switch **This bucket needs credentials** turned on by itself | Fill them in with the values the instructor gives, then **Test connection** |
| **Test connection** fails | A wrong endpoint, key or secret, or the network blocks the storage endpoint | Check the three values; tell the instructor if they are right |
| *Project name already exists* | Names are unique on the server | Another name: your own |
| **Create project** is greyed | The ingestion was not previewed | Click **Preview the ingestion** first |
| The collection matches 1 file, not 2 | The second season's file was not ticked | Tick `physical_features.csv` of the other season too |

## :material-numeric-2-circle-outline: Episode 2 · An nf-core run { #episode-2 .ws-ep2 }

| Symptom | Cause | Fix |
|---|---|---|
| *MultiQC is not installed* | `depictio` installed without the extra | `pip install "depictio[multiqc]==1.24.0"` |
| *Failed to process data collection 'ma_canonical'* | `GROUP_COL` guessed as `name` | Run again with `--var GROUP_COL=habitat` and `--update-config` |
| *Project '…' already exists on this server* | The name is taken, by you or by someone else | Another `--project` name; for your own project, `--update-config` refreshes it |
| 25 data collections, not 23 | The CLI keeps the two optional SIDLE collections, empty | Expected |

## :material-numeric-3-circle-outline: Episode 3 · Collaborate and export { #collaborate-and-export .ws-ep3 }

| Symptom | Cause | Fix |
|---|---|---|
| No **Metadata** button in the dock | The project has no eligible table (a source of a link, at most 10,000 rows) | Use your copy of nf-core/ampliseq, which has one |
| Cannot write a comment | You are not signed in, or the server does not let readers comment | Sign in; tell the instructor |
| No **Annotate** in the figure's action bar | The figure type takes comments only (3D, polar, pie), or you are not an editor or owner | Use a scatter or a bar figure on your own copy |
| No **History** in the component's menu | It is offered in **Edit** mode, once the dashboard has at least one version | Edit your copy, change something and click **Save** |
| No **Export** page | The exports are off on the server, or you do not own the dashboard | Export your own copy; tell the instructor |

## :material-file-code-outline: Going further · A project file by hand { #project-file .ws-ep1 }

| Symptom | Cause | Fix |
|---|---|---|
| `✗ --project-config-path does not exist or is not a file: penguins-1.yaml` | The command runs outside `penguins-workshop/` | `cd ~/depictio-workshop/penguins-workshop` |
| *The directory 'seasons/season_2007' does not exist.* | The command runs outside `penguins-workshop/`: the season folders are read from the folder you are in | `cd ~/depictio-workshop/penguins-workshop` |
| *would match no file* in the dry run | The pattern has a typo | Check `pattern:` |
| *Project '…' already exists on this server* | The name is taken, by you or by someone else | Another `--project` name; for your own project, `--update-config` refreshes it |
| No dashboard in the project | `--dashboard starter.yaml` was left out | `depictio dashboard import starter.yaml --project <project ID>` |

## :material-calendar-plus: Going further · A new season { #new-season .ws-ep2 }

| Symptom | Cause | Fix |
|---|---|---|
| *Environment variable 'SEASON_DIR' is not set* | The variable goes on the same line as the command | `SEASON_DIR=seasons/season_2007 depictio ingest …` |
| Still one data collection after the refresh | `--update-config` was left out, or `penguins-1.yaml` was used | Run again with `penguins.yaml` and `--update-config` |
| An info line: *this data location is already one of the project's runs* | The same season was attached twice; the ingestion still succeeds | Nothing to fix; attach `season_2008` for the new season |
| **Compare** greyed on season_2007 | The first run has nothing before it | Expected; compare **season_2008** |

## :material-code-braces: Going further · A dashboard as code { #dashboard-as-code .ws-ep3 }

| Symptom | Cause | Fix |
|---|---|---|
| *HTTP 409 … already exists in this project* | A dashboard with this title exists | A new title, or `--overwrite` |
| The project file `penguins.yaml` now holds a dashboard | It was given as the export's `-o` | Export to `dashboard.yaml`; download the zip again for `penguins.yaml` |
| *Either project_id parameter or project_tag in YAML is required* | The file has no `project_tag` | Keep the `project_tag` line of the export |
| A new figure stays empty | A column name in `figure_params` is wrong; validate does not check them | Check the column names |
| A wrong column only warns | Column checks count only with a server named | `depictio dashboard validate dashboard.yaml --server ~/.depictio/CLI.yaml` |
