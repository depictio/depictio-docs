---
title: "Depictio in the browser"
icon: material/account-group-outline
description: "A browser-only Depictio lesson: read a shared dashboard, edit your own copy, create a project from an nf-core run, browse the showcases; two optional episodes on files and on a new run."
glightbox: true
---

# :material-web: Depictio in the browser <small>(v1.24+)</small>

<p class="ws-lead">A <a href="../courses/">hands-on course</a>, done in the browser on a Depictio server. Four episodes make the timed session of Day 1 (15 December): read a shared dashboard, edit your own copy, create a project from an nf-core run, and browse the showcases. Two more episodes, creating a project from files and following a new run, are optional: do them after the workshop, on the same server while it runs.</p>

<figure markdown="span" class="ws-media"><video autoplay controls muted loop playsinline poster="../../images/tutorials/workshop/filter.webp" src="../../images/tutorials/workshop/filter.mp4"></video></figure>

<div class="ws-meta" markdown>
<span class="ws-chip" markdown="span">:material-account-school-outline: **No Depictio experience needed**</span> <span class="ws-chip" markdown="span">:material-web: **A browser, nothing to install**</span> <span class="ws-chip" markdown="span">:material-code-tags: **No programming; one optional Python exercise**</span>
</div>

## Episodes

<div class="grid cards ws-episodes" markdown>

-   <span class="ws-num ws-ep0">0</span> **[Setup](get-started.md)**

    ---

    <span class="ws-role">Everyone</span>

    How do I sign in, and where is everything?

-   <span class="ws-num ws-ep1">1</span> **[Read a shared dashboard](view.md)**

    ---

    <span class="ws-role">Reader · nf-core/ampliseq</span>

    How do I filter, select and compare samples on a dashboard I did not make?

-   <span class="ws-num ws-ep2">2</span> **[Make your own copy and edit it](edit-your-copy.md)**

    ---

    <span class="ws-role">Designer · nf-core/ampliseq</span>

    How do I change a dashboard without changing it for others?

-   <span class="ws-num ws-ep3">3</span> **[Create a project from an nf-core run](from-nf-core-run.md)**

    ---

    <span class="ws-role">Creator · run on S3</span>

    How do I turn a pipeline's results folder into a project and a dashboard?

-   <span class="ws-num ws-ep6">4</span> **[Showcases](showcases.md)**

    ---

    <span class="ws-role">Reader · 42 pipeline templates</span>

    What does a dashboard look like for the pipeline I use?

-   <span class="ws-num ws-ep4">+</span> **[Optional A · Create a project from files](from-a-file.md)**

    ---

    <span class="ws-role">Creator · two CSV files · optional</span>

    How do I start from my own tables, join them, and share them?

-   <span class="ws-num ws-ep5">+</span> **[Optional B · Follow a new run](new-run-and-versions.md)**

    ---

    <span class="ws-role">Creator · the 2009 season · optional, after the workshop</span>

    I added a season: what changed since I last looked, and how do I go back?

</div>

## Timetable { #timetable }

15 December, 10:00 to 12:00, in the browser. Each episode ends with a hands-on; the times include it.

| Time | Block | Min | Hands-on |
|---|---|---|---|
| 10:00 | Welcome, sign in | 5 | |
| 10:05 | Introducing Depictio | 15 | |
| 10:20 | [1 · Read a shared dashboard](view.md) | 20 | 10 min |
| 10:40 | [2 · Make your own copy and edit it](edit-your-copy.md) | 20 | 10 min |
| 11:00 | Break | 10 | |
| 11:10 | [3 · Create a project from an nf-core run](from-nf-core-run.md) | 20 | 10 min |
| 11:30 | [4 · Showcases](showcases.md) | 10 | 5 min |
| 11:40 | Wrap-up | 5 | |
| 11:45 | Your questions | 15 | |

The two optional episodes are for after the workshop.

## Three roles

After the setup, the episodes take you through three roles, one after the other.

| Role | Episodes | What you do |
|---|---|---|
| :material-account-eye-outline: **Reader** | 1 | Read a shared dashboard: filter, select, comment. You change nothing |
| :material-pencil-outline: **Designer** | 2 | Change a dashboard, in your own copy; never the data |
| :material-plus-box-outline: **Creator** | 3, then the two optional ones | Bring data in, from a pipeline run or from files; share the project; add new data and follow what changed |

## Two datasets

<div class="grid cards ws-data" markdown>

-   ![nf-core](../../images/pipeline-templates/nf-core/ampliseq/nf-core.png){ .ws-logo .off-glb } **nf-core/ampliseq 2.18.0**

    ---

    16S amplicon sequencing, the AWS megatest run: 12 samples from soil, sediment and water. In Depictio: 23 data collections and a dashboard of seven tabs.

    Episodes 1, 2, 3 and 4 · [nf-core/ampliseq](https://nf-co.re/ampliseq/2.18.0)

-   :material-penguin: **Palmer Penguins**

    ---

    Penguins from three islands in Antarctica. Two tables, a census and the measurements, joined on `individual_id` into a third: 223 penguins from the 2007 and 2008 seasons in the optional episode on files, then 119 more from 2009 in the optional episode on a new run, 342 in all.

    Optional episodes · [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/), CC0

</div>

## Requirements

<div class="grid cards" markdown>

-   :material-laptop: **Technical**

    ---

    - A recent browser: Firefox, Chrome, Edge or Safari. Nothing to install.
    - The workshop server address and a personal account, given by the instructor. Without them, the [workshop Codespace](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/workshop/devcontainer.json&quickstart=1) runs Depictio in a GitHub cloud workspace.
    - Zoom, with a second screen or window for the server.

-   :material-school-outline: **Skills**

    ---

    - Reading a table and a scatter plot.
    - Knowing roughly what a pipeline's results folder holds helps for episode 3; the lesson explains the rest.
    - No programming. A Bonus block of episode 2 shows a few lines of Python; it is optional.

</div>

!!! tip "Stuck?"
    Ask the docs assistant first: the chat button at the bottom right of these pages. Then ask in the Zoom chat. Known problems are in [Troubleshooting](troubleshooting.md).

<div class="ws-next ws-links" markdown>
[<span class="ws-k">Reference</span><span class="ws-t">The words of the lesson</span>](reference.md){ .ws-help .ws-ref }
[<span class="ws-k">Instructors</span><span class="ws-t">Instructor notes</span>](facilitators.md){ .ws-help .ws-inst }
[<span class="ws-k">Start here</span><span class="ws-t">0. Setup</span>](get-started.md){ .ws-go .ws-ep0 }
</div>
