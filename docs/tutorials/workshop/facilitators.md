---
title: "Instructor notes"
description: "Prepare a Depictio server for the Day 1 hands-on workshop and run it: schedule, settings, accounts, data, known pitfalls, checks."
---

# Instructor notes

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-school-outline: **For instructors**</span>
</div>

## :material-timer-outline: Schedule, Day 1 (15 December) { #schedule }

10:00 to 12:00, browser only, Depictio **1.24.0**.

| Time | Block | Min | What the instructor does |
|---|---|---|---|
| 10:00 | Welcome, sign in | 5 | Paste the server address in the chat. [0. Setup](get-started.md) |
| 10:05 | Introducing Depictio | 15 | Slides |
| 10:20 | Ep 1 Read a shared dashboard | 20 (hands-on 10) | Live demo: sidebar, **Guide**, **Show me**. [Page](view.md) |
| 10:40 | Ep 2 Make your own copy and edit it | 20 (hands-on 10) | Live demo: **Duplicate**, Edit mode, **Save**. Ask for the first name in the copy's title. [Page](edit-your-copy.md) |
| 11:00 | Break | 10 | |
| 11:10 | Ep 3 Create a project from an nf-core run | 20 (hands-on 10) | Live demo, then paste the run location **without a final `/`** in the chat; stagger the starts. [Page](from-nf-core-run.md) |
| 11:30 | Ep 4 Showcases | 10 (tour, hands-on 5) | Short tour (viralrecon), then learners explore the dashboard of their pipeline; ask in the chat what they noticed. [Page](showcases.md) |
| 11:40 | Wrap-up | 5 | Slides: 42 templates, next steps |
| 11:45 | Questions | 15 | |

After the workshop: **Optional · Create a project from files** ([page](from-a-file.md)); Day 2 is the command line.

## :material-clipboard-check-outline: Before the session { #before }

- Depictio **1.24.0**, [settings](#server-settings) and [accounts](#accounts) ready.
- Project *ampliseq-demo* created and **Public** ([Data](#data)).
- Showcases reachable outside the EMBL network; episodes 1 to 3 run once with a fresh learner account.
- Catch-up ready: your edited copy (ep 2), *ampliseq-demo* (ep 3). Codespace opened once.

## :material-server-outline: Server settings { #server-settings }

| Setting | For |
|---|---|
| `DEPICTIO_REMOTE_PUBLIC_S3_BUCKETS` lists `nf-core-awsmegatests/ampliseq` | Episode 3: reading the public bucket in place |
| `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT=true` | Day 2: readers comment |
| `DEPICTIO_STATIC_EXPORT_ENABLED=true`, `DEPICTIO_NOTEBOOK_EXPORT_ENABLED=true` | Day 2: exports (the worker needs Quarto) |

Figure code must stay open to non-admins.

## :material-account-multiple-outline: Accounts { #accounts }

- One account per learner (allowed to create projects), a few spares, one learner account for you.
- **Permanent**: reset nothing between Day 1 and Day 2.
- First sign-in forces a new password; until then the server refuses everything else.
- Copies of a public dashboard are public, with the owner's e-mail: ask for renaming (⋮ → **Edit** → **Dashboard Title**).

## :material-database-outline: Data { #data }

- **Eps 1, 2**: project *ampliseq-demo*, the nf-core/ampliseq 2.18.0 megatest at `s3://nf-core-awsmegatests/ampliseq/results-2723d4c298d48321594920d0324697e14d73ee94`. Create it in the web interface as in episode 3 (**Read in place**, **Group column** `habitat`), then switch to **Public**. Set the chart's example projects private.
- **Ep 3**: same location. Expected: 23 data collections, 19 links, 7 tabs.
- **Ep 4**: nothing on the server; learners open [showcases.depictio.embl.org/dashboards](https://showcases.depictio.embl.org/dashboards){target=_blank}.
- <span id="files"></span>**Files**: only for Bonus and optional pages, link the page in the chat. [`sampling_sites.tsv`](sampling_sites.tsv) (ep 3 Bonus); [`demographic_data.csv`](demographic_data.csv) and [`physical_features.csv`](physical_features.csv) (optional episode).

## :material-alert-outline: Known pitfalls { #pitfalls }

| Pitfall | What learners see | Fix |
|---|---|---|
| Trailing `/` on the run location | Phylogeny tab fails | Create the project again, without the `/` |
| **Group column** empty | 22 collections, no Differential Abundance tab | **Previous**, **More pipeline settings**, **Group column** `habitat` |
| Project name taken | *A project with this name already exists* | Another name |
| Welcome card on a fresh profile | Hides **Next** in the **New project** dialog | **I'll explore on my own** |
| First sign-in | *Choose your own password*, loops back | Set the new password first |

??? note "Details"

    **Episode 3 in a full room.** Ingestion takes 2 to 3 minutes for one learner, longer when everyone starts at once (workers read projects one after the other). Stagger the starts, for instance by row, and fill the wait with the **Activity** tab.

    **Running an episode.** Show the first action with the learner account; a helper answers in the chat, hard cases go to a breakout room.
