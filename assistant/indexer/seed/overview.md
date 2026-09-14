---
url: ""
breadcrumb: "Depictio"
---

# What Depictio is

Depictio is an open-source platform for building interactive, multi-dataset dashboards
from the outputs of bioinformatics workflows — nf-core and other Nextflow pipelines,
Snakemake workflows, or any tabular, image, GeoJSON or phylogeny data you can point it at.
It is aimed at researchers who produce data they want to explore and share interactively,
without writing a web application.

The shape of the work is: describe a project in YAML, ingest its data with the
`depictio-cli`, then build dashboards in the browser from components (figures, tables,
cards, interactive filters, maps, image grids, MultiQC panels). Dashboards can be exported
back to YAML, so they can be version-controlled and re-applied to new runs.

It is released under the MIT License and can be self-hosted with Docker Compose or
Kubernetes. It is developed mainly by Thomas Weber at the EMBL Data Science Centre in
Heidelberg, with support from the SciLifeLab Data Centre.

# Trying Depictio without installing it

There is a public demo instance at demo.depictio.embl.org with example projects loaded. No
account is needed and it resets periodically, so treat anything you build there as
temporary.

A full stack can also be launched in GitHub Codespaces from the depictio/depictio
repository, which needs nothing installed locally.
