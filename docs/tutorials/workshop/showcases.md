---
title: "4. Showcases"
description: "Hands-on 4: open the public showcases server, find the dashboard of your own nf-core pipeline, and try a filter. There is a dashboard for each of the 42 nf-core pipeline templates."
glightbox: true
---

# 4. Showcases

<div class="ws-strip" markdown>
[**0** Setup](get-started.md){ .ws-ep0 } [**1** Read](view.md){ .ws-ep1 } [**2** Edit](edit-your-copy.md){ .ws-ep2 } [**3** From a run](from-nf-core-run.md){ .ws-ep3 } [**4** Showcases](showcases.md){ .ws-ep6 .ws-here } [**+** From files](from-a-file.md){ .ws-ep4 }
</div>

<div class="ws-meta ws-ep6" markdown>
<span class="ws-chip" markdown="span">:material-account-eye-outline: **Reader**</span> <span class="ws-chip" markdown="span">:material-view-gallery-outline: **42 pipeline templates**</span> <span class="ws-chip" markdown="span">:material-timer-outline: **Tour, then 5 min**</span> <span class="ws-chip" markdown="span">:material-flag-outline: **After episode 3**</span>
</div>

!!! overview "Overview"
    **Questions**

    - Is there a dashboard for the pipeline I use?

    **Objectives**

    - Find the showcase dashboard of your nf-core pipeline.
    - Read it as you read ampliseq in episode 1.

In episode 3 you built the dashboard of one pipeline, nf-core/ampliseq, from its template. Depictio has a template for **42 nf-core pipelines**, and the **showcases** server shows what each one gives you: a dashboard per pipeline template, built on a test run. The instructor gives a short tour first, then you look for your own pipeline.

## :material-view-gallery-outline: Hands-on 4 · Find your pipeline { #showcases }

**Your task, 5 minutes:** find the dashboard of a pipeline you use, and pick the one figure you would show your team. Then post the pipeline and the figure in the Zoom chat.

1. Open the showcases in a new tab: [showcases.depictio.embl.org/dashboards](https://showcases.depictio.embl.org/dashboards){target=_blank}. It is the **Dashboards** page you know, in the **Thumbnails** view: one card per pipeline.
2. In the search box, type the name of your pipeline, for example `rnaseq`, `sarek` or `chipseq`. No pipeline of your own, or not in the list? Take `rnaseq`.
3. Open its dashboard and go through the **tabs**, left to right: they follow the steps of the pipeline, from the quality of the run to its results.
4. Open the **MultiQC** tab: it is the report of the pipeline, read the same way as in episode 1.
5. Try one **filter**, as in episode 1, and watch the cards and the figures follow.
6. Pick the one figure you would show your team, and post it in the Zoom chat, for example *rnaseq: the General Stats table of the MultiQC tab*.

![The Dashboards page of the showcases server in the Thumbnails view: one card per nf-core pipeline, with a preview of its dashboard](../../images/tutorials/workshop/showcases_thumbs.jpg){ .ws-shot }

!!! question "Check your understanding"
    The dashboards of two different pipelines have the same kinds of components, the same search and the same filters. Why?

    ??? solution "Answer"
        Each dashboard is built from the **template** of a pipeline version: the template lists the data collections, the links between them and the components. Every template uses the same Depictio components, so the interface works the same way for every pipeline.

!!! challenge "Challenge: two MultiQC tabs"
    Open the dashboards of two pipelines. In each, open the **MultiQC** tab. What is the same, and what is different?

    ??? solution "Solution"
        The tab is the same Depictio component, with the same search (**Ctrl+K**) and the same filters. What differs is the content: each pipeline's MultiQC report holds the modules of the tools it ran, so the sections and plots are not the same.

!!! keypoints "Key points"
    - The showcases server has a dashboard for each of the 42 nf-core pipeline templates.
    - A dashboard comes from a template: the same components, filled with the data of one pipeline.
    - You read a showcase as you read ampliseq: search, filters, tabs.

??? note "Bonus · Where the templates come from"
    A template is a file that describes the project of one pipeline version: its data collections, its links and its dashboard. Episode 3 uses the template of nf-core/ampliseq 2.18.0. The showcases use the same mechanism for the other pipelines.

    - The template of ampliseq: [Pipeline templates](../../pipeline-templates/nf-core/ampliseq.md).
    - The outputs of 136 tools that Depictio knows, for pipelines with no template: the [Tools catalog](../../catalog/index.md).
    - To contribute a template: [Contributing a template](../../developer/contributing-templates.md).

<div class="ws-next" markdown>
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md#episode-4){ .ws-help }
[<span class="ws-k">Optional</span><span class="ws-t">Create a project from files</span>](from-a-file.md){ .ws-go .ws-ep4 }
</div>
