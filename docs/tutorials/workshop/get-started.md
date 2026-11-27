---
title: "0. Setup"
description: "Sign in on the workshop server, find your way around, and learn the four words of the data model."
glightbox: true
---

# 0. Setup

<div class="ws-strip" markdown>
[**0** Setup](get-started.md){ .ws-ep0 .ws-here } [**1** Read](view.md){ .ws-ep1 } [**2** Edit](edit-your-copy.md){ .ws-ep2 } [**3** From a run](from-nf-core-run.md){ .ws-ep3 } [**4** Showcases](showcases.md){ .ws-ep6 } [**+** From files](from-a-file.md){ .ws-ep4 } [**+** New run](new-run-and-versions.md){ .ws-ep5 }
</div>

<div class="ws-meta ws-ep0" markdown>
<span class="ws-chip" markdown="span">:material-account-group-outline: **Everyone**</span> <span class="ws-chip" markdown="span">:material-timer-sand-empty: **Before the first episode**</span>
</div>

!!! overview "Overview"
    **Questions**

    - How do I sign in?
    - Where are the dashboards and the projects?
    - What are a project, a data collection, a link and a dashboard?

    **Objectives**

    - Sign in on the workshop server.
    - Name the four parts of a Depictio project.

Everything happens in the browser: there is nothing to install.

## :material-login: Sign in

1. Open the **workshop server** address the instructor gave you.
2. Sign in with your **personal account**.
3. The first sign-in opens *Choose your own password*. Set a new password: **Dashboards** opens. Until you do, Dashboards sends you back to this page.

!!! callout "Short tours"
    Depictio offers short tours the first time you open some pages, such as *First time on this dashboard?*. Click **Got it**: [episode 1](view.md#guide) shows the Guide it leads to, which stays in the left sidebar. If a **Welcome** card appears bottom right, click **I'll explore on my own**.

!!! warning "No account, or the server does not answer?"
    Open the [workshop Codespace](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/workshop/devcontainer.json&quickstart=1). It runs Depictio in a GitHub cloud workspace, with the nf-core/ampliseq run already ingested. Episodes 1, 2 and 3 work there.

## :material-map-outline: Find your way

| In the sidebar | What it holds |
|---|---|
| :material-view-dashboard:{ .ws-ic .ws-ic-dash } **Dashboards** | The dashboards you can open: your own, and those shared with you |
| :material-jira:{ .ws-ic .ws-ic-project } **Projects** | The projects you can open, their data and who can see them |

## :material-book-alphabet: Four words

A **project** holds **data collections**; **links** connect them; a **dashboard** shows them, through its **components**.

![The ampliseq project: the metadata linked to the other data collections, and the dashboard whose components read them](../../images/tutorials/workshop/diagrams/four-words_light.png#only-light){ .ws-diagram }
![The ampliseq project: the metadata linked to the other data collections, and the dashboard whose components read them](../../images/tutorials/workshop/diagrams/four-words_dark.png#only-dark){ .ws-diagram }

| Word | Meaning | In nf-core/ampliseq |
|---|---|---|
| :material-jira:{ .ws-ic .ws-ic-project } **Project** | Where the data and its dashboards live, with who can open them. Built from one or more pipeline runs, or from files you add | Today's run, read with the ampliseq 2.18.0 template |
| :material-table:{ .ws-ic .ws-ic-dc } **Data collection** | One kind of data in the project, read from one file or several. Its type says what it holds: a table, a MultiQC report, images, a phylogenetic tree, genome tracks… | 23 of them. Most are tables: `metadata`, `taxonomy_composition`, `alpha_rarefaction`… `multiqc_data` holds the MultiQC report |
| :material-link-variant:{ .ws-ic .ws-ic-link } **Link** | Says which identifiers match between two data collections, so that a filter on one narrows the other. The identifiers do not need the same column name, nor even a column: a MultiQC report is matched on its sample names | From `metadata` to the others: to the `sample_id` column of the diversity tables, to the sample names of `multiqc_data` |
| :material-view-dashboard:{ .ws-ic .ws-ic-dash } **Dashboard** | A set of **components** that read the project's data collections: figures, tables, cards, MultiQC plots, maps, and the filters that drive the others | The *nf-core/ampliseq* dashboard: seven tabs, from quality to differential abundance |

More words in the [Reference](reference.md); the full picture in [Data model](../../features/data-model.md).

!!! keypoints "Key points"
    - A project holds data collections: tables, MultiQC reports, images, trees…, not only tables.
    - A link matches the identifiers of two data collections, so a filter on one narrows the other.
    - A dashboard is made of components that read the data collections.

<div class="ws-next" markdown>
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md){ .ws-help }
[<span class="ws-k">Next episode</span><span class="ws-t">1. Read a shared dashboard</span>](view.md){ .ws-go .ws-ep1 }
</div>
