---
title: "Instructor notes"
description: "Prepare a Depictio server for the hands-on workshop and run the episodes: settings, accounts, files to hand out, the demo of episode 5, known pitfalls, checks."
---

# Instructor notes

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-school-outline: **For instructors**</span>
</div>

## :material-server-outline: Server settings { #server-settings }

Depictio **v1.22.0** or later, with the fix of the links permission check: on v1.22.0 a learner (non-admin) gets *Access denied to project* when creating a link, and their episode-4 project shows 0 links. Check it with a learner account. Settings:

| Setting | For |
|---|---|
| `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT=true` | Episode 1: readers comment on the shared dashboard |
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true` | Episode 5: *What's new*, **Before \| Now** and the Runs tab marks. Without it, episode 5 shows nothing new |
| `DEPICTIO_EVENTS_ENABLED=true` | Episode 5: the dashboard learns live that new data arrived |

Figure code must stay open to non-admins for challenge 2.2.

!!! danger "Release-blocking: the release deployed for the workshop"
    Two changes are not released yet, and the workshop needs both in the release it runs on:

    - **Add join** in the web interface (branch `feat/ui-join`): episodes 3 and 5 are built on it.
    - **The upload-token fix**: on **v1.22.2**, an upload from the web interface fails with HTTP 500 once the oldest login token of the user has expired. Episodes 3 and 5 both upload files, after the learners have been signed in for a while.

    Check both with a learner account: **Add join** on the project page, and an upload once the account's first login token has expired.

## :material-account-multiple-outline: Accounts

- One personal account per learner, allowed to create projects, plus a few spares.
- One learner account for the instructor besides the admin, so the shared screen looks like the learners'.
- Accounts are created by an admin (**Administration → Users**, or `POST /auth/admin/create_user`); learners change their password at first sign-in.
- Two user groups for the sharing step of episode 3: **Administration → Groups**, create *Tea lovers* and *Coffee lovers*, split the learner accounts between them, and post the list in the chat. Only an admin creates groups; each learner shares their own project with theirs. Do not use the built-in `users` group for "everyone": accounts created by an admin are not in it. **Public** is the way to reach every account.
- A copy of a dashboard of a public project is public too: every learner sees every *(copy)*, with its owner's e-mail. Ask everyone to rename their copy with their first name (⋮ → **Edit** → **Dashboard Title**): thirty *nf-core/ampliseq (copy)* in a row are hard to tell apart. Comments show their author's e-mail. Say so at the start.

## :material-database-outline: Data

| Episode | What to prepare |
|---|---|
| 1, 2 | Project *ampliseq-demo*, the nf-core/ampliseq 2.18.0 megatest at `s3://nf-core-awsmegatests/ampliseq/results-2723d4c298d48321594920d0324697e14d73ee94`. Create it **in the web interface**, as learners do in episode 4: **Read in place**, the location without a final `/`, **Group column** `habitat`. The server's own CLI cannot read the public bucket on this setup. Then switch the project to **Public**. Its dashboard is *nf-core/ampliseq*, with 7 tabs: Overview, MultiQC, Alpha Diversity, Ordination & Clustering, Community & Diversity, Differential Abundance, Phylogeny. Set the chart's example projects private: one of them has another dashboard named *nf-core/ampliseq* |
| 3 | Nothing on the server. Learners download the two CSV files [below](#files), link them and join them |
| 4 | The same location, given in the chat **without a final `/`** (with it, the phylogeny tree fails). The server lists `nf-core-awsmegatests/ampliseq` in `DEPICTIO_REMOTE_PUBLIC_S3_BUCKETS`. Learners set **Group column** to `habitat` (episode 4, step 3): 23 data collections, 19 links, 7 tabs. These counts are for the web interface; the CLI with `--var GROUP_COL=habitat` gives 25 data collections and 21 links (Day 2) |
| 5 | Learners use their own episode 3 project and the two 2009 files. For the demo: the prebuilt project *Penguin Field Survey*, see [Episode 5](#episode-5-demo) |
| Catch-up | Episode 2: the instructor's own edited copy. Episode 3: project *catchup-ep4-penguins*, rebuilt with the 2007–2008 files: both tables, the link, the join `joined_penguins`, and a dashboard on it with the species filter and the coloured figure. Episode 4: *ampliseq-demo*. All public. A learner without their own episode 3 project cannot append in episode 5: they follow on the shared screen |

## :material-download-outline: Files to hand out { #files }

Link the episode page in the chat; the files are on it.

| Episode | Files | Rows |
|---|---|---|
| 3 | [`demographic_data.csv`](demographic_data.csv), [`physical_features.csv`](physical_features.csv): the 2007 and 2008 seasons | 223 each; Adelie 99, Chinstrap 44, Gentoo 80; 7 empty `sex` |
| 5 | [`physical_features_2009.csv`](physical_features_2009.csv) (measurements), then [`demographic_data_2009.csv`](demographic_data_2009.csv) (census only): the 2009 season | 119 each; 43 Gentoo |

After episode 5: 223 + 119 = 342 rows in each table and in `joined_penguins`, 80 + 43 = 123 Gentoo.

## :material-presentation-play: Live demo after episode 4: where the project comes from { #behind-the-project }

The slide *Where your project comes from* is a live demo on the shared screen, after challenge 4.2. Learners watch. Open three browser tabs beforehand, in this order:

| Tab | Open | Show |
|---|---|---|
| 1 | [`template.yaml`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/ampliseq/2.18.0/template.yaml){target=_blank} of nf-core/ampliseq 2.18.0, on GitHub | Search for `ancombc_results`: the run files it reads (`qiime2/ancombc/differentials/…`) and its recipe, `qiime2/ancombc.py`. The **Differential Abundance** tab of `dashboards/base.yaml` is built on it |
| 2 | [`ancombc.yaml`](https://github.com/depictio/depictio/blob/main/depictio/catalog/qiime2/ancombc.yaml){target=_blank} in the Tools catalog | The same recipe; `find` recognises the file, `nf_core_url` points to the nf-core module, `renders_as` lists a volcano, two other omics plots, four cards and a table |
| 3 | [Tool Studio](https://depictio.github.io/depictio-tool-studio/){target=_blank}, with the ANCOM-BC entry imported | **Import an entry**, then select together the four files of [`catalog/qiime2/`](https://github.com/depictio/depictio/tree/main/depictio/catalog/qiime2){target=_blank}: `module.yaml`, `ancombc.yaml`, `ancombc.py`, `ancombc.tsv`. The Studio opens on **Export**: **Back** to **Visualizations** shows the volcano drawn from `ancombc.tsv`; **Fixture** shows the path run files → recipe → table → dashboard |

- In Tool Studio, *1 left to fill in: run the recipe* is expected: the demo loads no raw file. Do not run the recipe, and do not click **Contribute on GitHub**.
- The demo needs the Tool Studio of December, the one that writes recipes: its start screen has a card *Anything else, with a recipe*.

## :material-folder-clock-outline: Episode 5 { #episode-5-demo }

**Hands-on.** Each learner appends the 2009 season to the two tables of their own episode 3 project, measurements first; Depictio rebuilds `joined_penguins` after each append. They open their dashboard **once before** appending, so that Depictio records the visit: *What's new* compares with it.

What learners see, in the right order:

- After `physical_features_2009.csv`: `joined_penguins` stays at 223 rows, no new version of it is written, **What's new** shows no data change (its badge may count episode 3 comments), and the Gentoo figure stays at 80.
- After `demographic_data_2009.csv`: 342 rows, 123 Gentoo, no empty measurements. **What's new**: *DATA 1*, *joined_penguins*, *Refreshed · 223 → 342 rows*; **Split** greyed out; **Before | Now** 80 → 123, *+43*, *NEW (43)*.
- **Activity → History** lists the two appends as *Ingested · from Add data*, without table names; the rebuilds of the join are not listed. The project's **What's new** lists the three tables, `demographic_data`, `physical_features` and `joined_penguins`, each *223 → 342*.

In the census-first order, the dashboard's *What's new* groups the change under an upload label, `depictio_upload_…`, *1 collection*, and **Split** is not greyed out. Say so if a learner's panel looks different.

**Demo.** Runs and **Compare** are shown on the shared screen, on the prebuilt project *Penguin Field Survey*, which holds one run per season. Build it before the session with the CLI, one season folder per run:

1. A project file with the two tables, `physical_features` and `demographic_data`, a location written as `{SEASON_DIR}`, and the join of the two tables (see [Day 2, episode 2](../workshop-cli/own-tables.md) for the same layout).
2. The first season: `SEASON_DIR=season_2007 depictio ingest --project-config-path <project file>`.
3. The next two: the same command with `SEASON_DIR=season_2008`, then `season_2009`, adding `--project "Penguin Field Survey" --attach-run`. Each attach records a run with its ingestion, so **Compare** works.
4. Import its dashboard, then share the project read-only with every learner, for the optional challenges 5.3 and 5.4 (**Data version**, **History**). Its `physical_features` versions are v0 109 rows, v1 223, v2 342.
5. Check **Runs**, `season_2009` unfolded, and **Compare** with a learner account.

!!! warning "The join needs an `id:`"
    In the project file, give the join an `id:`. Without one, each `--attach-run` creates another joined table. A fix is in progress.

Do not use `rebuild_demo.py` (project *Penguins Versioned Demo*) for this demo: it stages the seasons into the project's existing folder, records no ingestion for them, and **Compare** stays greyed.

No ingestion happens live during the session.

## :material-alert-outline: Known pitfalls { #pitfalls }

| Pitfall | What learners see | What to say |
|---|---|---|
| Append order | The census appended first: `joined_penguins` gets the 119 new penguins at once with empty measurements, until the measurements are appended. Row counts and the filter jump before the figure does | Append `physical_features_2009.csv` first, then `demographic_data_2009.csv`. If done the other way, append the second file: the result is the same, 342 rows with no empty measurements |
| No **What's new** after the first append | Expected: the measurements alone do not change `joined_penguins` | Append the census, then reload |
| Double append | A second **Append folders** of the same file is accepted silently: the table holds 461 rows, 119 duplicated ids, and the join follows | Unlock the table; in its **Data** panel, **Past versions**, **At version** the version with 342 rows, **Restore vN**, **Restore**; the join is rebuilt. **Version history** only lists versions. Header counts may stay stale until reload. Name the version by its rows, never "v1". **Replace all data** also works |
| *Append folders* | The button of **Manage Data Collection** says *folders* for a single CSV file | It is the right button |
| Manage data greyed on `joined_penguins` | Append, replace and clear are refused on a joined table | Append to `demographic_data` and `physical_features`; the join follows |
| Deleting a source table | *Join(s) … read this table: delete them first.* | Delete the join first, in the **Joins** list, if that is really meant |
| Joined table name | The table is `joined_<name>`: name `penguins` gives `joined_penguins` | Build the dashboard on `joined_penguins` |
| *Not rebuilt* badge | A red *Not rebuilt* badge next to the result table in the **Joins** list: the last rebuild of the join failed. Its tooltip gives the error | Read the tooltip; tell the instructor |
| `depictio_run_id` dropped | After an append, the table no longer has the `depictio_run_id` column | Known; do not build a component on that column |
| Restore refused | *Unlock the table to restore a past version* | Switch **Unlock cell edits** first |
| Trailing `/` on the run location (episode 4) | The Phylogeny tab fails. The location field's own placeholder ends in `/`, so learners copy that habit | Give the location without a final `/`; if it happened, create the project again |
| Gentoo cleared (episode 5) | The dashboard reopens with the last filter, *Gentoo*, selected; clicking *Gentoo* again in the single-choice Select clears it: 342 points, **Before \| Now** *+119* instead of *+43*. The only signs are *1 filter active*, a *1* badge and the chip | Tell learners to check the filter, not click it; if cleared, pick *Gentoo* again |
| *Mark as seen* too early (episode 5) | The blue dot on the figure is gone, so **Before \| Now** cannot be opened from it | Mark as seen last, after **Before \| Now** |
| Welcome card (episode 3) | On a fresh browser profile, the **Welcome** card sits bottom right on Projects, over the **New project** dialog, and hides its **Next** button on screens up to about laptop size (not on a full HD screen) | Close it: **I'll explore on my own** |
| First sign-in | *Choose your own password*; **Dashboards** sends learners back to it until they set one | Set the new password first |

## :material-timer-sand: Episode 4 in a full room { #episode-4-timing }

An ingestion from the web interface takes about a minute for one learner alone, and several minutes when the whole room starts at once: the server's workers read the projects one after the other. Stagger the starts, for instance by group or by row, and fill the wait with the **Activity** tab of the project.

## :material-human-male-board: Running an episode

1. **Before**: show the first action on the server, with the learner account.
2. **During**: learners signal done or stuck. A helper answers in the chat with a link to the step; hard cases go to a breakout room with screen sharing.
3. **After**: go through the challenges' solutions on the shared screen. Who did not finish continues from the catch-up copy or project.

## :material-clipboard-check-outline: Checks before the day

- With a fresh learner account, never the admin: the welcome screen, then each episode as written, checking each solution. In particular **Link your tables** (*223 of 223 values found*) and **Add join** in episode 3 (*Join created*, *joined_penguins: 223 rows*), and the link count of an episode-4 project.
- As many uploads at once in episode 3, and episode 4 with many accounts at once: projects are read one after the other by the server's workers.
- An upload from the web interface with a learner account whose first login token has expired (see the release-blocking note above).
- Episode 5 end to end with a learner account: the episode 3 project with its join, open its dashboard, append `physical_features_2009.csv` then `demographic_data_2009.csv`, reload: *What's new* lists *joined_penguins 223 → 342 rows*, and **Before | Now** on the Gentoo figure reads 80 and 123. Then a double append and its restore.
- The prebuilt *Penguin Field Survey*: **Runs** and **Compare** on `season_2009`.
- The demo [after episode 4](#behind-the-project): the three tabs open, the ANCOM-BC entry imported in Tool Studio.
- Episode 3's sharing with two learner accounts from different groups: after **Add group**, a member of the same group sees the dashboard in **Dashboards**, a member of the other group does not; after **Public**, both do.
- Open the Codespace once as a backup.
