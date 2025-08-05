---
title: "Timeline Test"
description: "Testing the timeline plugin syntax"
---

# Timeline Plugin Test

## Basic Timeline Test

::timeline::

[
    {
        "title": "Launch",
        "content": "First implementation.",
        "icon": "./nf-core-logo-square.png",
        "sub_title": "2022-Q1"
    },
    {
        "title": "One",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "icon": "☀️",
        "key": "cyan",
        "sub_title": "2022-Q2"
    },
    {
        "title": "Two",
        "content": "Lorem ipsum dolor sit amet.",
        "icon": "📊",
        "sub_title": "2022-Q3"
    },
    {
        "title": "Three",
        "content": "Lorem ipsum dolor sit amet.",
        "key": "pink",
        "icon": "✨",
        "sub_title": "2022-Q4"
    }
]

::/timeline::

## Depictio Roadmap Timeline

::timeline center alternate::

[
    {
        "title": "Visualization Studio",
        "content": "Interactive dashboards with modern web components and real-time data binding",
        "icon": ":fontawesome-solid-chart-line:",
        "key": "green",
        "sub_title": "Phase 1: Foundation ✅"
    },
    {
        "title": "Data Ingestion", 
        "content": "Support for multiple tabular formats: Parquet, CSV, JSON, TSV with automated processing",
        "icon": ":fontawesome-solid-database:",
        "key": "green",
        "sub_title": "Phase 1: Foundation ✅"
    },
    {
        "title": "MultiQC Integration",
        "content": "Seamless integration with bioinformatics quality control reports", 
        "icon": ":fontawesome-solid-flask:",
        "key": "orange",
        "sub_title": "Phase 2: Specialization 🚧"
    },
    {
        "title": "Configuration Assistant",
        "content": "CLI-based project setup wizard with intelligent recommendations",
        "icon": ":fontawesome-solid-terminal:", 
        "key": "orange",
        "sub_title": "Phase 2: Specialization 🚧"
    },
    {
        "title": "Workflow Templates",
        "content": "Pre-configured dashboards for popular bioinformatics workflows and pipelines",
        "icon": ":fontawesome-solid-sitemap:",
        "key": "blue", 
        "sub_title": "Phase 3: Ecosystem 📋"
    }
]

::/timeline::


::gantt::

- title: Definition Phase
  activities:
  - title: Creative Brief
    start: 2022-03-03
    lasts: 1 day
  - title: Graphic Design Research
    start: 2022-03-02
    end: 2022-03-10
    lasts: 2 weeks
  - title: Brainstorming / Mood Boarding
    start: 2022-03-11
    end: 2022-03-20

- title: Creation Phase
  activities:
  - title: Sketching
    start: 2022-03-21
    end: 2022-04-01
  - title: Design Building
    start: 2022-04-02
    end: 2022-04-20
  - title: Refining
    start: 2022-04-21
    end: 2022-04-30

- title: Feedback Phase
  activities:
  - title: Presenting
    start: 2022-04-22
    end: 2022-05-01
  - title: Revisions
    start: 2022-05-02
    end: 2022-05-10

- title: Delivery Phase
  activities:
  - title: Final delivery
    start: 2022-05-11
    end: 2022-05-12

::/gantt::


::cards::

- title: Zeus
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/001-zeus.png

- title: Athena
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/003-athena.png

- title: Poseidon
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/007-poseidon.png

- title: Artemis
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/021-artemis.png

- title: Ares
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/006-ares.png

- title: Nike
  content: Lorem ipsum dolor sit amet.
  image: ./img/icons/027-nike.png

::/cards::