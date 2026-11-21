---
title: "Depictio from the command line"
icon: material/console
description: "The Depictio command line: set it up, create a project from your own tables, add a new season and compare, write a dashboard as a file; an nf-core run with its template as an optional episode."
glightbox: true
---

# :material-console: Depictio from the command line <small>(v1.23+)</small>

<p class="ws-lead">The second <a href="../courses/">hands-on course</a>. In <a href="../workshop/">Depictio in the browser</a> everything happens in the browser. Here the same things happen from your own computer, with the Depictio command line: a results folder on your laptop becomes a project on the server, and a dashboard becomes a file you can edit.</p>

[![The CLI reads the folder on your laptop, writes the tables to the server's storage and records the project; the browser shows the dashboard](../../images/tutorials/workshop-cli/diagrams/cli-flow_light.png#only-light){ .ws-diagram }](../../images/tutorials/workshop-cli/diagrams/cli-flow_light.png){target=_blank}
[![The CLI reads the folder on your laptop, writes the tables to the server's storage and records the project; the browser shows the dashboard](../../images/tutorials/workshop-cli/diagrams/cli-flow_dark.png#only-dark){ .ws-diagram }](../../images/tutorials/workshop-cli/diagrams/cli-flow_dark.png){target=_blank}

<div class="ws-meta" markdown>
<span class="ws-chip" markdown="span">:material-console: **Some terminal practice**</span> <span class="ws-chip" markdown="span">:material-laptop: **macOS or Linux**</span> <span class="ws-chip" markdown="span">:material-language-python: **Python 3.11 or later**</span>
</div>

## Episodes

<div class="grid cards ws-episodes" markdown>

-   <span class="ws-num">0</span> **[Setup](setup.md)**

    ---

    <span class="ws-role">Before the session</span>

    How do I install the CLI and connect it to the server?

-   <span class="ws-num">1</span> **[Your first project from the command line](first-project.md)**

    ---

    <span class="ws-role">Palmer Penguins · one table, one season</span>

    How do I turn a table on my laptop into a project and a dashboard?

-   <span class="ws-num">2</span> **[A second table, then a new season](own-tables.md)**

    ---

    <span class="ws-role">Palmer Penguins · two tables, two seasons</span>

    How do I add a table, link it, and bring the next batch?

-   <span class="ws-num">3</span> **[A dashboard as code](dashboard-as-code.md)**

    ---

    <span class="ws-role">A YAML file</span>

    How do I write, check and share a dashboard as a file?

-   <span class="ws-num">4</span> **[An nf-core run, with its template](nf-core-run.md)**

    ---

    <span class="ws-role">Optional · nf-core/ampliseq</span>

    How does a pipeline Depictio knows skip the project file?

</div>

## Two datasets

<div class="grid cards ws-data" markdown>

-   :material-penguin: **Palmer Penguins**

    ---

    The census and measurements of the browser course, split into one folder per field season.

    Episodes 1, 2, 3 · [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/), CC0

-   ![nf-core](../../images/pipeline-templates/nf-core/ampliseq/nf-core.png){ .ws-logo .off-glb } **nf-core/ampliseq 2.18.0**

    ---

    The megatest run of the browser course, as a folder you download: 12 samples from soil, sediment and water.

    Episode 4 · [nf-core/ampliseq](https://nf-co.re/ampliseq/2.18.0)

</div>

## Requirements

<div class="grid cards" markdown>

-   :material-laptop: **Technical**

    ---

    - A laptop with **macOS or Linux**. On Windows, [WSL2](https://learn.microsoft.com/windows/wsl/install) with Ubuntu.
    - **Python 3.11 to 3.13**: `python3 --version`. Python 3.14 does not work yet. No administrator rights needed: everything goes in a folder of your own.
    - About **1.5 GB** of free disk space.
    - A network that reaches the workshop server **and** its storage: [Setup](setup.md) checks both. Try it before the day.
    - The workshop server address and a personal account, given by the instructor.

-   :material-school-outline: **Skills**

    ---

    - Running commands in a terminal: `cd`, `ls`, `unzip`, pasting a command and reading what it prints.
    - Editing a text file and keeping its indentation: YAML counts spaces.
    - The words of the browser course: project, data collection, link, run, dashboard. The [Reference](../workshop/reference.md) lists them; the course itself helps but is not required.
    - No programming.

</div>

<div class="ws-next ws-links" markdown>
[<span class="ws-k">Instructors</span><span class="ws-t">Instructor notes</span>](facilitators.md){ .ws-help .ws-inst }
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md){ .ws-help }
[<span class="ws-k">Start here</span><span class="ws-t">0. Setup</span>](setup.md){ .ws-go .ws-ep0 }
</div>
