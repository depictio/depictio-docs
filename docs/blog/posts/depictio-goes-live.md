---
date: 2025-08-07
authors:
  - thomas-weber
categories:
  - Announcements
  - Launch
  - Demo
tags:
  - dashboard
  - visualization
  - demo
  - bioinformatics
  - launch

---


# <span class="depictio-icon"></span> Depictio goes live !

 **Depictio is now live with a public demo!**

<!-- more -->

<div style="padding: 64.29% 0 0 0; position: relative">
  <iframe
    src="https://player.vimeo.com/video/1109036952?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479&amp;autoplay=1&amp;loop=1"
    frameborder="0"
    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
    title="depictio-main-1754915546775"
  ></iframe>
</div>
<script src="https://player.vimeo.com/api/player.js"></script>

A longer demo is also available in [Dashboard Creation Guide](../../usage/guides/dashboard_creation.md#video-example).

## 🎯 What is Depictio?

Depictio is an open-source, modern, web-based platform that aims to help life-science researchers and bioinformaticians to analyse complex data generated out of high-throughput experiments into interactive, shareable dashboards without requiring programming skills.

## ❓ Why Depictio and how does it differ from other tools (e.g., Shiny, Dash, Streamlit, Gradio, etc.)?

In **bioinformatics**, **core facilities** and research groups generating large datasets are relying on highly standardised workflows (e.g., **[nf-core](https://nf-co.re/) pipelines**) that produce structured outputs. These datasets require interactive exploration and visualization tools, helpful for quality control issues identification, as well as deriving actionable insights.

While there are multiple popular dashboarding solutions amongts bioinformaticians like Shiny, Dash, Streamlit, Gradio, they require programming skills and time to design tailored systems. This includes multiple steps, from the data ingestion to the data visualisation, as well as hosting and maintaining platforms in a production environment.

Depictio aims to fill this gap by providing a **comprehensive platform** composed of a cloud-compatible microservices architecture and a companion CLI tool (depictio-cli) living close to the data. The system provides a **no-code dashboard creation experience** that allows researchers to focus on data analysis.

## 🤨 Wait, but where is the life science focus in this ?

While the current version of Depictio is a general-purpose dashboarding tool (open-source alternative to **Plotly Studio**), the next phase (Q3-Q4 2025) is to have a strong focus towards **life sciences** domain-specific features.

On the frontend, this means bringing in **specialized components** (like **JBrowse2** for genome visualization) and bioinformatics heavily used **visualizations** (like **volcano plots**, **heatmaps**, etc.) that are tailored for life science data.

On the backend and data ingestion side, our plan is to focus on developing seamless integration of **[MultiQC](https://seqera.io/multiqc/)** reports (gold standard in bioinformatics QC reporting) and to develop workflows templates for popular bioinformatics pipelines (like nf-core) to make it easy to aggregate, visualize and analyze aggregated results.

In the end, the idea would be to provide a comprehensive platform that allows life science researchers to easily create interactive dashboards using **community-driven templates** for established workflows.

In the spirit of MultiQC's automated data discovery for gold-standard bioinformatics QC tools (cutadapt, fastqc, ...) using `multiqc .` in a terminal, you would be able to run `depictio --template nf-core/rnaseq .` to automatically ingest workflow relevant data and fill a dashboard with pre-configured components for visualizing the results of a RNA-seq analysis conducted with nf-core/rnaseq pipeline.

## 👥 Who is it for?

**Current users:**

- Researchers and data scientists seeking **code-free** dashboard creation
- Anyone working with datasets who wants **interactive exploration tools**

**Future target audience:**

- Life science researchers analyzing **high-throughput experimental data**
- Bioinformaticians working with **standardised pipeline outputs** and **multi-omics datasets**

## 🎨 Main current features

- **No-code dashboard creation**: Build interactive dashboards without writing code
- **Real-time interactivity**: Play with your data using sliders, dropdowns, as well as box selection on scatter plots
- **Multi-data sources support**: Combine multiple data sources (so-called **Data Collections** in Depictio) in a single dashboard using SQL-like joining system
- **Authenticated or Unauthenticated Access**: Use the system with JWT-based authentication and Google Oauth or in unauthenticated mode (like the demo)
- **Docker-compose & Kubernetes ready**: Easy deployment options for production use
- **Companion CLI (depictio-cli)**: Command-line interface for managing projects, scan data, and upload datasets

## 🛠️ **[Modern Architecture](../../features/architecture.md)**

Depictio is built on a state-of-the-art microservices architecture combining modern technologies for optimal performance, scalability, and developer experience. The system provides a comprehensive platform for interactive data visualization and analysis.

<div class="grid cards" markdown>

- :material-react:{ .react } __Frontend Technologies__

    ---

    Plotly Dash (React-based) interactive interface with Mantine UI components

- :material-server:{ .fastapi } __Asynchronous Backend__

    ---

    High-performance async FastAPI backend with Python for real-time updates

- :material-database:{ .mongodb } __Metadata Storage__

    ---

    MongoDB for project metadata, configurations, and user management

- :material-database-outline:{ .deltalake } __Data Storage__

    ---

    Delta Lake for optimized data storage and time-travel capabilities

- :material-folder-network:{ .minio } __Object Storage__

    ---

    MinIO S3-compatible storage for scalable file management

- :material-lightning-bolt:{ .polars } __Data Processing__

    ---

    Polars engine for high-performance data manipulation and Delta Lake storage

- :material-shield-check:{ .jwt } __Authentication__

    ---

    JWT-based authentication with Google OAuth integration

- :material-tools:{ .docker } __DevOps & Deployment__

    ---

    Docker and Kubernetes support for cloud-native infrastructure

</div>

<style>
/* Technology-specific colors for grid cards */
.grid.cards .react {
  color: #61dafb;
}

.grid.cards .fastapi {
  color: #4db6ac;
}

.grid.cards .mongodb {
  color: #66bb6a;
}

.grid.cards .deltalake {
  color: #ff6b35;
}

.grid.cards .minio {
  color: #ff8a80;
}

.grid.cards .polars {
  color: #00a2e8;
}

.grid.cards .jwt {
  color: #000000;
}

[data-md-color-scheme="slate"] .grid.cards .jwt {
  color: #ffffff;
}

.grid.cards .docker {
  color: #2496ed;
}
</style>

### Architecture Overview

The system is designed with a clear separation of concerns:

- **🎨 Frontend Layer**: React-based dashboard interface with Plotly visualizations and Mantine UI components
- **⚙️ API Layer**: FastAPI backend handling authentication, data operations, and real-time updates  
- **💾 Data Layer**: MongoDB for metadata, Delta Lake for analytics data, MinIO for object storage
- **🚀 Processing Engine**: Polars for high-performance data manipulation and analysis
- **🔧 CLI Tool**: `depictio-cli` for project management, data scanning, and automated workflows

## 👥 Who is behind Depictio?

Depictio is an open-source and academic project initiated by Thomas Weber, Research Fellow at the [European Molecular Biology Laboratory (EMBL)](https://www.embl.org/) during his ARISE fellowship (Marie Skłodowska-Curie Actions ; grant agreement No 945405). The project is primarily supported by the [EMBL Data Science Centre](https://www.embl.org/about/info/data-science-centre/) with additional contributions from the [SciLifeLab Data Centre](https://www.scilifelab.se/contact/data-center/).

## 🔬 Who is currently using Depictio?

Depictio is currently being used by EMBL researchers and data scientists across different life science fields. Some specific use cases include:

- **Strand-seq biobank ([Korbel group](https://www.embl.org/groups/korbel/), EMBL Heidelberg)**: Single-cell DNA sequencing to study Structural Variants (SVs) in human genomes. Pipeline used: [mosaicatcher-pipeline](https://github.com/friendsofstrandseq/mosaicatcher-pipeline)
- **Marine microbiome interactome study ([Vincent group](https://www.embl.org/groups/vincent/), [TREC](https://www.embl.org/about/info/trec/expedition/), EMBL Heidelberg)**: Marine microbiome analysis using single-cell amplicon sequencing. Pipeline used: [nf-core/ampliseq](https://github.com/nf-core/ampliseq)

## 🚀 How to Try It Out

Access the live demo at [demo.depictio.embl.org](https://demo.depictio.embl.org) or start using it below directly and explore the features. You can also create your own project and upload datasets to start dashboarding. Don't forget to check out the [guides](../../usage/README.md) for step-by-step instructions on how to use the system.

!!! note
    The demo is running a "unauthenticated mode" to allow anyone to try it out without needing an account. However, you can create a temporary account to create your own projects and upload datasets. Accounts and related data will be reset after 1 hour to keep the demo environment clean.

<!-- Live Demo Section -->

<section class="live-demo-section">
  <div class="live-demo-info">
    <div class="demo-badge">
      <span class="live-indicator"></span>
      <strong>Live interactive demo - Try it!</strong>
    </div>
  </div>

  <div class="hero-iframe-demo" id="iframe-container">
    <div class="demo-header" id="demo-header" style="display: none;">
      <div class="demo-header-content">
        <div class="demo-header-left">
          <span class="live-indicator"></span>
          <span class="demo-title">Live Demo</span>
        </div>
        <button class="close-btn" onclick="toggleFullscreen()" title="Exit Fullscreen">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>
    </div>
    <button class="fullscreen-btn" onclick="toggleFullscreen()" title="Toggle Fullscreen">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
        <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
      </svg>
    </button>
    <iframe id="demo-iframe" src="https://demo.depictio.embl.org/" width="100%" height="1080" frameborder="0" allowfullscreen style="zoom: 0.56;">
      <p>Your browser does not support iframes. <a href="https://demo.depictio.embl.org/">Click here to view the Depictio dashboard</a></p>
    </iframe>
  </div>
</section>

<style>

  .hero-demo {
    margin: 2rem 0;
  }

  .demo-image {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  .live-demo-info {
    color: var(--md-default-fg-color);
    padding: 0.5rem 0;
    margin: 1rem 0 0.5rem 0;
    text-align: center;
  }

  .demo-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .demo-badge {
    display: inline-flex;
    align-items: center;
    gap: 16px;
    padding: 16px 28px 16px 32px;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.4) 100%);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 50px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transition: all 0.3s ease;
  }

  [data-md-color-scheme="slate"] .demo-badge {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .demo-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9);
  }

  .live-indicator {
    width: 10px;
    height: 10px;
    background: #4ade80;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.7);
    }
    70% {
      box-shadow: 0 0 0 10px rgba(74, 222, 128, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
    }
  }

  .demo-description {
    margin: 0 0 0.3rem 0;
    font-size: 0.9rem;
    font-weight: 500;
  }

  .demo-note {
    margin: 0;
    font-size: 0.65rem;
    opacity: 0.8;
    font-style: italic;
  }

  .try-it-banner {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.25);
    padding: 6px 12px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
  }

  .try-it-banner:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(2px);
  }

  .try-it-text {
    font-weight: 600;
    font-size: 0.8rem;
    color: white;
  }

  .try-it-arrow {
    width: 14px;
    height: 14px;
    color: white;
    transition: transform 0.3s ease;
  }

  .try-it-banner:hover .try-it-arrow {
    transform: translateY(2px);
  }

  .live-demo-section {
    margin: 2rem 0;
    padding: 0 2rem;
  }

  .hero-iframe-demo {
    margin: 1rem auto 2rem auto;
    position: relative;
    max-width: 1200px;
  }

  .hero-iframe-demo iframe {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  .demo-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 8px 8px 0 0;
    position: relative;
    z-index: 11;
    width: 100%;
    box-sizing: border-box;
  }

  .demo-header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: none;
    width: 100%;
  }

  .demo-header-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .demo-title {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-weight: 500;
    font-size: 1rem;
    letter-spacing: 0.5px;
  }

  .close-btn {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  .fullscreen-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 10;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .fullscreen-btn:hover {
    background: rgba(0, 0, 0, 0.9);
  }

  .hero-iframe-demo.fullscreen {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 9999 !important;
    margin: 0 !important;
    padding: 0 !important;
    background: black !important;
    border-radius: 0 !important;
    overflow: hidden !important;
    max-width: none !important;
    box-sizing: border-box !important;
  }

  .hero-iframe-demo.fullscreen::before {
    display: none !important;
  }

  .hero-iframe-demo.fullscreen .demo-header {
    display: block !important;
    position: relative !important;
    width: 100% !important;
    height: 60px !important;
    border-radius: 0 !important;
    box-sizing: border-box !important;
  }

  .hero-iframe-demo.fullscreen iframe {
    width: 100vw !important;
    height: calc(100vh - 60px) !important;
    border-radius: 0 !important;
    zoom: 1 !important;
    position: relative !important;
    left: 0 !important;
    top: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
  }

  .hero-iframe-demo.fullscreen .fullscreen-btn {
    display: none;
  }

  .hero-description {
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }

  /* Demo Unavailable Message Styles */
  .demo-unavailable-message {
    background: #f8fafc;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 2rem 0;
    border-radius: 12px;
    text-align: center;
    border: 1px solid var(--md-default-fg-color--lightest);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  [data-md-color-scheme="slate"] .demo-unavailable-message {
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .demo-unavailable-content {
    max-width: 600px;
    margin: 0 auto;
  }

  .demo-unavailable-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem auto;
    background: #f68b33;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .demo-unavailable-icon svg {
    width: 40px;
    height: 40px;
  }

  .demo-unavailable-content h3 {
    margin: 0 0 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
  }

  .demo-unavailable-content p {
    margin: 0 0 2rem 0;
    color: var(--md-default-fg-color--light);
    line-height: 1.6;
  }

  .demo-unavailable-content a {
    color: var(--md-primary-fg-color);
    text-decoration: none;
  }

  .demo-unavailable-content a:hover {
    text-decoration: underline;
  }

  .demo-alternative-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .demo-alternative-actions .md-button img {
    vertical-align: middle;
    margin-right: 8px;
    margin-top: -2px;
  }

  .md-button--gitpod {
    background-color: rgb(252, 249, 244) !important;
    border-color: #ff8a00 !important;
    color: #ff8a00 !important;
  }

  .md-button--gitpod:hover {
    background-color: #e67e00 !important;
    border-color: #e67e00 !important;
    color: white !important;
  }

  @media (max-width: 768px) {
    .demo-unavailable-message {
      padding: 1rem;
      margin: 1rem 0;
    }

    .demo-alternative-actions {
      flex-direction: column;
      align-items: center;
    }

    .demo-alternative-actions .md-button {
      width: 100%;
      max-width: 280px;
    }
  }

  /* Technology Stack Badges */
  .tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
    margin-top: 1rem;
  }

  .tech-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    text-decoration: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    white-space: nowrap;
  }

  .tech-badge img {
    width: 16px;
    height: 16px;
    object-fit: contain;
  }

  .tech-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  /* Individual technology colors */
  .tech-badge.plotly {
    background: linear-gradient(135deg, #5a6bc4 0%, #495ab3 100%);
  }

  .tech-badge.mantine {
    background: linear-gradient(135deg, #339af0 0%, #228be6 100%);
  }

  .tech-badge.react {
    background: linear-gradient(135deg, #61dafb 0%, #21b1c7 100%);
  }

  .tech-badge.fastapi {
    background: linear-gradient(135deg, #4db6ac 0%, #409a94 100%);
  }

  .tech-badge.python {
    background: linear-gradient(135deg, #3776ab 0%, #2d5d8f 100%);
  }

  .tech-badge.mongodb {
    background: linear-gradient(135deg, #66bb6a 0%, #5aa05e 100%);
  }

  .tech-badge.deltalake {
    background: linear-gradient(135deg, #ff6b35 0%, #e55527 100%);
  }

  .tech-badge.minio {
    background: linear-gradient(135deg, #ff8a80 0%, #e57373 100%);
  }

  .tech-badge.polars {
    background: linear-gradient(135deg, #00a2e8 0%, #0080c7 100%);
  }

  .tech-badge.jwt {
    background: linear-gradient(135deg, #000000 0%, #333333 100%);
  }

  .tech-badge.oauth {
    background: linear-gradient(135deg, #ea4335 0%, #d23f31 100%);
  }

  .tech-badge.docker {
    background: linear-gradient(135deg, #2496ed 0%, #1d7dd8 100%);
  }

  .tech-badge.kubernetes {
    background: linear-gradient(135deg, #326ce5 0%, #2558d1 100%);
  }

  /* Grid cards styling enhancement */
  .grid.cards > .card {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  [data-md-color-scheme="slate"] .grid.cards > .card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .grid.cards > .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  [data-md-color-scheme="slate"] .grid.cards > .card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }

  @media (max-width: 768px) {
    .tech-stack {
      justify-content: flex-start;
    }

    .tech-badge {
      font-size: 0.8rem;
      padding: 6px 10px;
    }

    .tech-badge img {
      width: 14px;
      height: 14px;
    }
  }
</style>

<script>
function toggleFullscreen() {
  const container = document.getElementById('iframe-container');
  const button = container.querySelector('.fullscreen-btn');
  const buttonIcon = button.querySelector('svg path');
  const header = document.getElementById('demo-header');

  if (container.classList.contains('fullscreen')) {
    // Exit fullscreen
    container.classList.remove('fullscreen');
    header.style.display = 'none';
    buttonIcon.setAttribute('d', 'M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z');
    button.setAttribute('title', 'Toggle Fullscreen');
    document.body.style.overflow = '';
  } else {
    // Enter fullscreen
    container.classList.add('fullscreen');
    header.style.display = 'block';
    buttonIcon.setAttribute('d', 'M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z');
    button.setAttribute('title', 'Exit Fullscreen');
    document.body.style.overflow = 'hidden';
  }
}

// Function to check if the demo website is reachable
async function checkDemoAvailability() {
  const demoSection = document.querySelector('.live-demo-section');
  const iframe = document.getElementById('demo-iframe');
  const demoUrl = 'https://demo.depictio.embl.org/';
  
  if (!demoSection || !iframe) return;
  
  try {
    // Try to fetch the demo website
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

    const response = await fetch(demoUrl, {
      method: 'HEAD',
      mode: 'no-cors', // Allow cross-origin requests
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    // If we get here, the site is reachable (even with no-cors, network errors will throw)
    console.log('Demo site is reachable');

  } catch (error) {
    console.log('Demo site not reachable:', error.message);

    // Hide the live demo section
    demoSection.style.display = 'none';

    // Create and show fallback message
    const fallbackMessage = document.createElement('div');
    fallbackMessage.className = 'demo-unavailable-message';
    fallbackMessage.innerHTML = `
      <div class="demo-unavailable-content">
        <div class="demo-unavailable-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12,2C6.48,2 2,6.48 2,12C2,17.52 6.48,22 12,22C17.52,22 22,17.52 22,12C22,6.48 17.52,2 12,2ZM13,17H11V15H13V17ZM13,13H11V7H13V13Z"/>
          </svg>
        </div>
        <h3>Live Demo Temporarily Unavailable</h3>
        <p>The interactive demo is currently not accessible. Please try again later or <a href="https://demo.depictio.embl.org/" target="_blank" rel="noopener">visit the demo site directly</a>.</p>
        <div class="demo-alternative-actions">
          <a href="https://gitpod.io/#https://github.com/depictio/depictio/releases/latest" class="md-button md-button--gitpod" target="_blank" rel="noopener">
            <img src="../../images/gitpod-logo-mark.svg" alt="Gitpod" width="16" height="16">
            Open in Gitpod
          </a>
          <a href="../../usage/get_started/" class="md-button">View Documentation</a>
        </div>
      </div>
    `;

    // Insert the fallback message after the note section
    const noteSection = document.querySelector('.admonition');
    if (noteSection) {
      noteSection.insertAdjacentElement('afterend', fallbackMessage);
    } else {
      // Fallback: insert before the "What You Can Do" section
      const nextSection = document.querySelector('h2');
      if (nextSection) {
        nextSection.insertAdjacentElement('beforebegin', fallbackMessage);
      }
    }
  }
}

// Handle ESC key to exit fullscreen
document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const container = document.getElementById('iframe-container');
      if (container && container.classList.contains('fullscreen')) {
        toggleFullscreen();
      }
    }
  });
  
  // Check demo availability when page loads
  checkDemoAvailability();
});
</script>

## 🎮 What You Can Do in the Demo

### 1. **Explore Pre-loaded Demo Datasets ..**

- **Iris** and **Palmer Penguins** datasets for quick visualization (Palmer penguins was turned into a sequencing runs-like dataset to showcase the system)

### 2. **.. or Upload Your Own Data**

- Create your own project and upload datasets in your favorite tabular format (CSV, Parquet, etc.)

### 3. **Create Interactive Dashboards**

- **Figures**: Scatter plots, bar charts, histograms, ...
- **Tables**: Sortable, filterable data tables
- **Metrics Cards**: Key performance indicators
- **Interactive Components**: Sliders, dropdowns, segmented controls, and more

### 4. **Experience Real-time Interactivity**

- Use box selection on scatter plots
- Apply multiple filters simultaneously
- Reset filters with a single click

## 🗺️ What's Next?

Get a look at our [roadmap](../../roadmap/README.md) to see what we're working on next:

- **Support MultiQC Integration** - Seamless quality control workflows
- **JBrowse2 Integration** - Interactive genome browser for genomic data
- **TUI (Terminal User Interface) for project creation** - Create project configuration using UI on the terminal
- **Workflow Templates** - Pre-configured dashboards for popular pipelines like [nf-core](https://nf-co.re/)

## 🤝 Join Our Community and Contribute

Depictio is open-source and community-driven. We welcome contributions, feedback, and ideas to make it better!

- **🐙 GitHub**: [github.com/depictio/depictio](https://github.com/depictio/depictio)
- **💬 Discussions**: Share feedback and ask questions
- **🐛 Issues**: Report bugs or request features
- **⭐ Star us**: Help spread the word!

*Questions? Feedback? We'd love to hear from you! Open an issue on GitHub or reach out directly.*

---

*Thomas Weber*  
*August 2025*
