---
title: "Depictio from the command line"
icon: material/console
description: "Day 2 of the workshop: set up the command line, build a project from your own tables, bring an nf-core run from the terminal, then collaborate on a dashboard and export it. Going further holds the rest."
glightbox: true
---

# :material-console: Depictio from the command line <small>(v1.24+)</small>

<p class="ws-lead">The second <a href="../courses/">hands-on course</a>. In <a href="../workshop/">Depictio in the browser</a> everything happens in the browser. Here you start from your own tables in the browser, bring an nf-core run in from your terminal with the Depictio command line, then collaborate on the dashboard and export it. Day 2 is on 16 December.</p>

![The CLI runs where the files are (a laptop, a server or cluster, the end of a Nextflow run, a scheduled job), reads the folder, writes the tables to the server's storage and records the project; the browser shows the dashboard](../../images/tutorials/workshop-cli/diagrams/cli-flow_light.png#only-light){ .ws-diagram }
![The CLI runs where the files are (a laptop, a server or cluster, the end of a Nextflow run, a scheduled job), reads the folder, writes the tables to the server's storage and records the project; the browser shows the dashboard](../../images/tutorials/workshop-cli/diagrams/cli-flow_dark.png#only-dark){ .ws-diagram }

<div class="ws-meta" markdown>
<span class="ws-chip" markdown="span">:material-console: **Some terminal practice**</span> <span class="ws-chip" markdown="span">:material-laptop: **macOS or Linux**</span> <span class="ws-chip" markdown="span">:material-language-python: **Python 3.11 or later**</span>
</div>

## Episodes

<div class="grid cards ws-episodes" markdown>

-   <span class="ws-num">0</span> **[Setup](setup.md)**

    ---

    <span class="ws-role">Before the session</span>

    How do I install the CLI and connect it to the server?

-   <span class="ws-num">1</span> **[Your own tables, no template](project-builder.md)**

    ---

    <span class="ws-role">Palmer Penguins · in the browser</span>

    How do I turn my own tables into a project, when no template exists?

-   <span class="ws-num">2</span> **[An nf-core run from the terminal](nf-core-run.md)**

    ---

    <span class="ws-role">nf-core run · the command line</span>

    How does a pipeline Depictio knows skip the project file?

-   <span class="ws-num">3</span> **[Collaborate and export](collaborate-and-export.md)**

    ---

    <span class="ws-role">Your copy of nf-core/ampliseq · in the browser</span>

    How do I label, comment, go back to a version, and hand the dashboard over as a file?

-   <span class="ws-num">+</span> **[Going further](going-further.md)**

    ---

    <span class="ws-role">Optional · A project file by hand, a new season, a dashboard as code</span>

    What else can the command line do?

</div>

## Timetable { #timetable }

16 December, 10:00 to 12:00, in the browser and in the terminal. Each episode ends with a hands-on; the times include it.

| Time | Block | Min | Hands-on |
|---|---|---|---|
| 10:00 | Welcome | 5 | |
| 10:05 | [1 · Your own tables, no template](project-builder.md) | 20 | 10 min |
| 10:25 | The command line: [your CLI.yaml](setup.md) | 10 | |
| 10:35 | [2 · An nf-core run from the terminal](nf-core-run.md) | 25 | 15 min |
| 11:00 | Break | 10 | |
| 11:10 | [3 · Collaborate and export](collaborate-and-export.md) | 25 | 15 min |
| 11:35 | Wrap-up | 10 | |
| 11:45 | Your questions | 15 | |

Install the command line before the day: [Setup](setup.md).

## Two datasets

<div class="grid cards ws-data" markdown>

-   :material-penguin: **Palmer Penguins**

    ---

    The census and measurements of the browser course, split into one folder per field season.

    Episode 1 and Going further · [palmerpenguins](https://allisonhorst.github.io/palmerpenguins/), CC0

-   ![nf-core](../../images/pipeline-templates/nf-core/ampliseq/nf-core.png){ .ws-logo .off-glb } **nf-core/ampliseq 2.18.0**

    ---

    Your copy of the dashboard of the browser course: 12 samples from soil, sediment and water.

    Episode 3 · [nf-core/ampliseq](https://nf-co.re/ampliseq/2.18.0)

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
