---
title: "Home"
icon: material/home
description: "Depictio is a modern, interactive platform that enables dashboards creation from bioinformatics workflows outputs."
hide:
  - navigation
  - toc
  - path
---

<!-- markdownlint-disable MD025 -->

#

<!-- markdownlint-enable MD025 -->

<style>
  .md-typeset h1 {
    /* display: none; */
    font-size: 0.01rem;
    padding: 0;
    margin: 0;
  }
</style>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container text-center">
    <img src="./images/logo/logo_hd.svg" alt="Depictio logo" width="350" class="logo-dark">
    <img src="./images/logo/logo_hd_white.svg" alt="Depictio logo" width="350" class="logo-light">
    <div class="hero-demo">
      <img src="./images/Demo.gif" alt="Depictio Demo" class="demo-image">
    </div>
    <p class="hero-description">
      A modern platform that allows to create dashboards from bioinformatics workflows outputs.
    </p>

  </div>
</section>

<!-- Workflow Integration Section -->
<section class="workflow-section">
  <div class="container text-center">
    <p class="section-heading">
      Generate dashboards using results from standardised workflows available in:
    </p>
    <a href="https://nf-co.re/" target="_blank" rel="noopener">
      <img src="https://www.scilifelab.se/wp-content/uploads/2021/09/nf-core-logo.png" alt="nf-core logo" class="workflow-logo nf-core-logo">
    </a>
    <a href="https://workflowhub.eu/" target="_blank" rel="noopener">
      <img src="https://about.workflowhub.eu/assets/img/workflowhub-square.svg" alt="WorkflowHub logo" class="workflow-logo">
    </a>
    <a href="https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#catalog" target="_blank" rel="noopener" class="snakemake-catalog-link">
      <img src="https://avatars.githubusercontent.com/u/33450111?v=4" alt="Snakemake logo" class="workflow-logo">
      <strong>Snakemake workflow catalog</strong>
    </a>
  </div>
</section>

<!-- Features Section -->
<section class="features-section">
  <div class="container">
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">
          <span class="twemoji">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"/></svg>
          </span>
        </div>
        <h3>Interactive Dashboards</h3>
        <p>Create customizable dashboards with real-time data interaction</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">
          <span class="twemoji">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.35,10.04C18.67,6.59 15.64,4 12,4C9.11,4 6.6,5.64 5.35,8.04C2.34,8.36 0,10.91 0,14A6,6 0 0,0 6,20H19A5,5 0 0,0 24,15C24,12.36 21.95,10.22 19.35,10.04Z"/></svg>
          </span>
        </div>
        <h3>Cloud-Ready</h3>
        <p>Designed for cloud environments with Kubernetes support</p>
      </div>
    </div>

  </div>
</section>

<!-- CTA Section -->
<section class="cta-section">
  <div class="container text-center">
    <div class="cta-buttons">
      <a href="installation/" class="md-button md-button--primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M8,5.14V19.14L19,12.14L8,5.14Z" />
        </svg>
        Get Started
      </a>
      <a href="https://gitpod.io/#https://github.com/depictio/depictio" class="md-button md-button--gitpod">
        <img src="images/gitpod-logo-mark.svg" width="12" height="12" alt="Gitpod">
        Try on Gitpod
      </a>
      <a href="features/" class="md-button md-button--secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z" />
        </svg>
        Learn More
      </a>
    </div>
  </div>
</section>

<style>
.md-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.md-button svg {
  vertical-align: middle;
  margin-top: -1px; /* Fine-tune vertical position */
}

.md-button--gitpod {
  background-color:rgb(252, 249, 244) !important;
  border-color: #ff8a00 !important;
  color: #ff8a00 !important;
}

.md-button--gitpod:hover {
  background-color: #e67e00 !important;
  border-color: #e67e00 !important;
}

.md-button--primary {
  background-color: #9966CC !important;
  border-color: #9966CC !important;
  color: white !important;
}

.md-button--primary:hover {
  background-color: #9966CC !important;
  border-color: #9966CC !important;
}
.md-button--secondary {
  background-color: #8BC34A !important;
  border-color: #8BC34A !important;
  color: white !important;
}

.md-button--secondary:hover {
  background-color: #8BC34A !important;
  border-color: #8BC34A !important;
}
</style>

## Project Overview

In the field of bioinformatics, researchers often face significant challenges when working with frequently executed production workflows, especially in managing and analyzing large-scale datasets. Despite the availability of numerous bioinformatics tools, there is a notable absence of platforms specifically designed for seamless integration with production workflows, which include standardized data ingestion, QC monitoring, and results exploration.

Depictio addresses this gap, offering a generic and centralized platform that allows to integrate workflows output data in order to build interactive dashboards, facilitating downstream analysis and QC metrics monitoring into a cohesive system. Depictio provides a scalable, flexible, and open-source solution tailored to meet needs of researchers handling large datasets generated by production workflows, agnostically of their execution engine (nextflow, snakemake, galaxy, R …).

## Key Features

### Data Ingestion

- **Manual or Automated:** Data ingestion can be triggered manually or through a watcher system
- **Client-side scan & processing:** Depictio-CLI (using [typer](https://typer.tiangolo.com/) python package) allows to scan and process data locally, pushing to the S3 bucket the resulting data format ready to be used by the dashboard
- **Data Types:** Support for tabular data formats (Parquet, CSV, JSON, TSV, compressed/uncompressed) using [Polars](https://pola-rs.github.io/polars-book/) and [Delta Lake](https://delta.io/) format

### Frontend

- **Customizable Dashboards:** Design and customise dashboards easily
- **Interactivity:** Explore data dynamically with instant updates in response to selections and inputs applied to the dashboards components
- **Project-based Organization:** Organize dashboards according projects, allowing easier management and sharing

### System

- **Scalable and Cloud-Oriented:** Built for cloud environments with Kubernetes and Docker-Compose support
- **Open-Source and Shareable:** Community-driven development model with transparent deployment

## Getting Started

Ready to get started with Depictio? Check out our installation guides:

- [Docker Compose Installation](installation/docker/) - Quickest way to get started
- [Kubernetes Installation](installation/kubernetes/) - For production environments
- [CLI Installation](installation/cli/) - For data ingestion and management

## Funding

<div class="funding-grid">
  <div class="funding-card">
    <img src="./assets/EN_fundedbyEU_VERTICAL_RGB_POS.png" alt="EU Logo">
    <h3>Marie Skłodowska-Curie Grant</h3>
    <p>This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 945405</p>
    <a href="https://marie-sklodowska-curie-actions.ec.europa.eu/" class="md-button" target="_blank">Learn More</a>
  </div>

  <div class="funding-card">
    <img src="./assets/AriseLogo300dpi.png" alt="ARISE Logo">
    <h3>ARISE Programme</h3>
    <p>ARISE is a postdoctoral research programme for technology developers, hosted at EMBL.</p>
    <a href="https://www.embl.org/about/info/arise/" class="md-button" target="_blank">Learn More</a>
  </div>

  <div class="funding-card">
    <img src="./assets/EMBL_logo_colour_DIGITAL.png" alt="EMBL Logo">
    <h3>EMBL</h3>
    <p>The European Molecular Biology Laboratory is Europe's flagship laboratory for the life sciences.</p>
    <a href="https://www.embl.org/" class="md-button" target="_blank">Learn More</a>
  </div>
</div>

## Academic Partners

<div class="partners-container">
  <div class="partner-card">
    <img src="./assets/scilifelab_logo.png" alt="SciLifeLab Logo">
    <h3>SciLifeLab Data Centre</h3>
    <p>SciLifeLab Data Centre provides data-driven life science research infrastructure and expertise to accelerate open science in Sweden and beyond.</p>
    <a href="https://www.scilifelab.se/data/" class="md-button" target="_blank">Learn More</a>
  </div>
</div>

<style>
/* Funding Grid */
.funding-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  margin: 2rem 0;
}

.funding-card {
  flex: 1 1 250px;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  background-color: white;
}

.funding-card img {
  height: 100px;
  object-fit: contain;
  margin-bottom: 10px;
  margin-left: auto;
  margin-right: auto;
}

.funding-card h3 {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.funding-card p {
  flex: 1;
  font-size: 0.9rem;
  color: var(--md-default-fg-color--light);
}

.funding-card a {
  margin-top: 1rem;
  align-self: center;
}

/* Partners Section */
.partners-container {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.partner-card {
  max-width: 500px;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  background-color: white;
}

.partner-card img {
  height: 60px;
  object-fit: contain;
  margin-bottom: 10px;
  margin-left: auto;
  margin-right: auto;
}

.partner-card h3 {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.partner-card p {
  flex: 1;
  color: var(--md-default-fg-color--light);
}

.partner-card a {
  margin-top: 1rem;
  align-self: center;
}

@media (max-width: 768px) {
  .funding-grid {
    flex-direction: column;
  }

  .funding-card {
    max-width: 100%;
  }
}
</style>

<style>
  /* Base Styles */
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 1rem;
  }

  section {
    margin: 3rem 0;
  }

  /* Hero Section */
  .hero-section img {
    margin-bottom: 1.5rem;
  }

  .hero-demo {
    margin: 2rem 0;
  }

  .demo-image {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  .hero-description {
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }

  /* Workflow Section */
  .workflow-section {
    margin: 2.5rem 0;
  }

  .section-heading {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  .workflow-section a {
    display: inline-block;
    margin: 0 15px;
    vertical-align: middle;
  }

  .workflow-logo {
    height: 50px;
    width: 150px;
    object-fit: contain;
  }

  .nf-core-logo {
    height: 60px;
    width: 250px;
    max-width: 120px;
  }

  .snakemake-catalog-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    vertical-align: middle;
  }

  .snakemake-catalog-link .workflow-logo {
    height: 65px;
    width: 65px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .snakemake-catalog-link strong {
    font-size: 1.1rem;
    color: var(--md-default-fg-color);
    white-space: nowrap;
    line-height: 35px;
    display: flex;
    align-items: center;
  }

  /* Features Section */
  .features-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .feature-card {
    flex: 1 1 250px;
    padding: 1.5rem;
    border-radius: 8px;
    background-color: var(--md-primary-fg-color--light);
    color: var(--md-primary-bg-color);
    text-align: center;
  }

  .feature-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
  }

  /* CTA Section */
  .cta-buttons {
    margin: 2rem 0;
  }

  .cta-buttons a {
    margin: 0 0.5rem;
  }

  /* Overview and Key Features Sections */
  .container h2 {
    margin-top: 2rem;
    margin-bottom: 1rem;
  }

  .feature-category {
    margin-bottom: 1.5rem;
  }

  .feature-category h3 {
    margin-bottom: 0.5rem;
  }

  /* Roadmap Section */
  .roadmap-items {
    padding-left: 1rem;
    margin-bottom: 2rem;
  }

  .roadmap-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 0.75rem;
  }

  .roadmap-item input[type="checkbox"] {
    margin-right: 0.5rem;
    margin-top: 0.25rem;
  }

  .task-list-item-checkbox {
    position: relative;
    top: 0.1em;
  }

  /* Getting Started Section */
  .installation-links {
    margin-top: 1rem;
  }

  .installation-links li {
    margin-bottom: 0.5rem;
  }

  /* Responsive Adjustments */
  @media (max-width: 768px) {
    .features-grid {
      flex-direction: column;
    }

    .feature-card {
      max-width: 100%;
    }
  }

  .text-center {
    text-align: center;
  }
</style>
