---
title: "Instructor notes"
description: "Prepare a Depictio server for the Day 1 hands-on workshop and run it: schedule, settings, accounts, data, known pitfalls, checks."
---

# Instructor notes

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-school-outline: **For instructors**</span>
</div>

## :material-timer-outline: Schedule, Day 1 (15 December) { #schedule }

10:00 to 12:00, browser only, Depictio **1.24.0**. Each hands-on is the one shown on the slide, and each page has the same shape: the steps, one **Check your understanding**, one challenge, then **Bonus** blocks that are not timed.

| Time | Block | Min | What happens | Page |
|---|---|---|---|---|
| 10:00 | Welcome | 5 | Zoom, polls, sign-in, the server address | [0. Setup](get-started.md) |
| 10:05 | Introducing Depictio | 15 | Why Depictio, the three roles, today's dataset | slides |
| 10:20 | Episode 1: Read a shared ampliseq dashboard | 20 (**Hands-on 1**: 10) | Together: sidebar, **Guide**, **Show me**. Then alone: **Ctrl+K**, General Stats, the most trimmed sample; filter Habitat = Soil, Phyla 57 to 26; Analysis mode, two groups, then **Compare** | [1. Read a shared dashboard](view.md) |
| 10:40 | Episode 2: Edit your copy | 20 (**Hands-on 2**: 10) | **Duplicate**, Edit mode, add a figure (interface or Code), **Save** | [2. Make your own copy and edit it](edit-your-copy.md) |
| 11:00 | Break | 10 | | |
| 11:10 | Episode 3: From an nf-core run | 20 (**Hands-on 3**: 10) | The ampliseq megatest on S3, create only: name the project; point at the run (**Group column** `habitat`); check, create (2 to 3 min of ingestion), open the dashboard | [3. Create a project from an nf-core run](from-nf-core-run.md) |
| 11:30 | Showcases | 10 (**Hands-on 4**: 5) | Short tour, then 5 min: find your pipeline, open its dashboard, try a filter | [4. Showcases](showcases.md) |
| 11:40 | Wrap-up | 5 | What you did, 42 templates, next steps | slides |
| 11:45 | Questions | 15 | | |

Not in the timed session: sharing, the sample table and its link, the table from a URL, the Project Builder, several MultiQC reports in one collection (Bonus blocks of episode 3); creating a project from files and following a new run ([Optional](from-a-file.md) and [Optional B](new-run-and-versions.md), for after the workshop). Metadata mode, comments, annotations, versions, exports and the command line are Day 2 ([Collaborate and export](../workshop-cli/collaborate-and-export.md)).

## :material-server-outline: Server settings { #server-settings }

Depictio **1.24.0**, exactly. Check with a learner account (not the admin) that a project created in the web interface has its links: on v1.22.0 a learner gets *Access denied to project* when creating a link, and their episode 3 project shows 0 links.

| Setting | For |
|---|---|
| `DEPICTIO_REMOTE_PUBLIC_S3_BUCKETS` lists `nf-core-awsmegatests/ampliseq` | Episode 3: reading the public bucket in place |
| `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT=true` | Day 2: readers comment on the dashboard |
| `DEPICTIO_STATIC_EXPORT_ENABLED=true`, `DEPICTIO_NOTEBOOK_EXPORT_ENABLED=true` | Day 2: the exports. Off by default; the worker needs Quarto for the rendered report |
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED=true`, `DEPICTIO_EVENTS_ENABLED=true` | Optional B only: *What's new*, **Before \| Now**, live updates |

Figure code must stay open to non-admins for the optional Python bonus of episode 2.

!!! danger "Release-blocking"
    **The upload-token fix.** On v1.22.2 an upload from the web interface fails with HTTP 500 once the oldest login token of the user has expired. No upload is part of the Day 1 core, but Optional A and Day 2 upload files. Check an upload with an account whose first token has expired.

## :material-account-multiple-outline: Accounts

- One personal account per learner, allowed to create projects, plus a few spares.
- **Accounts are permanent.** What learners build on Day 1, their copy and their project, is still there on Day 2. Do not reset or delete anything between the two days.
- One learner account for the instructor besides the admin, so the shared screen looks like the learners'.
- Accounts are created by an admin (**Administration → Users**, or `POST /auth/admin/create_user`). Learners change their password at first sign-in. Until they do, the server refuses every other request, from the web interface, the API or the CLI (*Change your password first.*).
- User groups are needed only for the sharing step of Optional A: **Administration → Groups**, then split the learner accounts. Do not use the built-in `users` group for "everyone": accounts created by an admin are not in it.
- A copy of a dashboard of a public project is public too: every learner sees every *(copy)*, with its owner's e-mail. Ask everyone to rename their copy with their first name (⋮ → **Edit** → **Dashboard Title**). Say so at the start.

## :material-database-outline: Data

| Episode | What to prepare |
|---|---|
| 1, 2 | Project *ampliseq-demo*, the nf-core/ampliseq 2.18.0 megatest at `s3://nf-core-awsmegatests/ampliseq/results-2723d4c298d48321594920d0324697e14d73ee94`. Create it **in the web interface**, as learners do in episode 3: **Read in place**, the location without a final `/`, **Group column** `habitat`. The server's own CLI cannot read the public bucket on this setup. Then switch the project to **Public**. Its dashboard is *nf-core/ampliseq*, with 7 tabs. Set the chart's example projects private: one of them has another dashboard named *nf-core/ampliseq* |
| 3 | The same location, given in the chat **without a final `/`**: with it, the phylogeny tree fails. Expected result: 23 data collections, the 19 links of the template, 7 tabs |
| Showcases | Nothing on the workshop server: learners open [showcases.depictio.embl.org/dashboards](https://showcases.depictio.embl.org/dashboards){target=_blank}, which must be reachable from their laptops. Say "42 pipeline templates", not a number of dashboards |
| Optional A, B | Nothing on the server. Learners download the files [below](#files) |
| Catch-up | Episode 2: the instructor's own edited copy. Episode 3: *ampliseq-demo* |

## :material-download-outline: Files to hand out { #files }

Only for the Bonus and optional pages. Link the page in the chat; the files are on it.

| Page | Files | Rows |
|---|---|---|
| Episode 3, Bonus | [`sampling_sites.tsv`](sampling_sites.tsv): where and when each of the 12 samples was taken | 12; 4 sites near Tübingen; `ID` matches `multiqc_data` (12 of 12) |
| Optional A | [`demographic_data.csv`](demographic_data.csv), [`physical_features.csv`](physical_features.csv): the 2007 and 2008 seasons | 223 each; Adelie 99, Chinstrap 44, Gentoo 80; 7 empty `sex` |
| Optional B | [`physical_features_2009.csv`](physical_features_2009.csv) (measurements), then [`demographic_data_2009.csv`](demographic_data_2009.csv) (census only) | 119 each; 43 Gentoo. After both: 342 rows, 123 Gentoo |

## :material-timer-sand: Episode 3 in a full room { #episode-3-timing }

An ingestion of the ampliseq megatest from S3 takes 2 to 3 minutes (2 min 27 s in our test, one learner alone). It takes longer when the whole room starts at once: the server's workers read the projects one after the other. Stagger the starts, for instance by row, and fill the wait with the **Activity** tab of the project. Hands-on 3 runs until about 11:28.

## :material-alert-outline: Known pitfalls { #pitfalls }

| Pitfall | What learners see | What to say |
|---|---|---|
| Trailing `/` on the run location (episode 3) | The Phylogeny tab fails. The location field's own placeholder ends in `/`, so learners copy that habit | Give the location without a final `/`; if it happened, create the project again |
| **Group column** left empty (episode 3) | 22 collections instead of 23, no Differential Abundance tab | **Previous**, **More pipeline settings**, **Group column** `habitat` |
| Project name taken | *A project with this name already exists* | Another name |
| Welcome card (episode 3) | On a fresh browser profile, the **Welcome** card sits bottom right over the **New project** dialog and hides its **Next** button on screens up to about laptop size | Close it: **I'll explore on my own** |
| First sign-in | *Choose your own password*; **Dashboards** sends learners back to it until they set one | Set the new password first |
| Append order (Optional B) | The census appended first: `joined_penguins` gets the 119 new penguins with empty measurements until the measurements are appended | Append `physical_features_2009.csv` first, then `demographic_data_2009.csv` |
| Double append (Optional B) | A second **Append folders** of the same file is accepted silently: 461 rows, and the join follows | Unlock the table; **Past versions**, **At version** the version with 342 rows, **Restore vN**, **Restore** |
| Manage data greyed on `joined_penguins` (Optional B) | Append, replace and clear are refused on a joined table | Append to `demographic_data` and `physical_features`; the join follows |

## :material-human-male-board: Running an episode

1. **Before**: show the first action on the server, with the learner account.
2. **During**: learners signal done or stuck. A helper answers in the chat with a link to the step; hard cases go to a breakout room with screen sharing.
3. **After**: go through the challenges' solutions on the shared screen. Who did not finish continues from the catch-up copy or project.

## :material-clipboard-check-outline: Checks before the day

- With a fresh learner account, never the admin: the welcome screen, then episodes 1 to 3 as written, checking each solution.
- Episode 3 with many accounts at once: the ingestion stays within 2 to 3 minutes for a staggered start.
- Showcases reachable from outside the EMBL network, on a laptop.
- Optional A end to end with a learner account: **Link your tables** (*223 of 223 values found*), **Add join** (*Join created*, *joined_penguins: 223 rows*), and an upload once the first login token has expired.
- DocBot is turned on in the published docs (`DEPICTIO_DOCS_DOCBOT`, see `dev/docbot/`): the chat button shows at the bottom right of every page.
- Open the Codespace once as a backup.
