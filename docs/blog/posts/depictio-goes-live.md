---
date: 2025-01-08
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

## 🎯 What is Depictio?

Depictio is an open-source modern, web-based platform that aims to help life-science researchers and bioinformaticians to analyse complex data generated out of high-throughput experiments into interactive, shareable dashboards without requiring programming skills.

## ❓ Why Depictio and how does it differ from other tools (e.g., Shiny, Dash, Streamlit, Gradio, etc.)?

In **bioinformatics**, **core facilities** and groups generating large datasets are frequently running highly standardised workflows (e.g., **[nf-core](https://nf-co.re/) pipelines**) that produce structured outputs. These datasets require interactive exploration and visualization to identify quality control issues and derive insights.

While there are multiple dashboarding solutions popular like Shiny, Dash, Streamlit, Gradio and others, they require programming skills and time to design tailored systems. This includes multiple steps, from the data ingestion to the data visualisation, as well as hosting and maintaining the platform in a production environment.

Depictio aims to fill this gap by providing a **comprehensive platform** composed of a cloud-compatible microservices architecture and a companion CLI tool (depictio-cli) living close to the data. The system provides a **no-code dashboard creation experience** that allows researchers to focus on data analysis.

## 🤨 Wait, but where is the 🧬 life science focus in this ?

While the current version of Depictio is a general-purpose dashboarding tool (open-source alternative to **Plotly Studio**), the next phase is to evolve it into a **domain-specific life science platform**.

On the frontend, this means bringing in **specialized components** (like **JBrowse2** for genome visualization) and bioinformatics heavily used **visualizations** (like **volcano plots**, **heatmaps**, etc.) that are tailored for life science data.

On the backend and data ingestion side, our plan is to focus on developing seamless integration of **[MultiQC](https://seqera.io/multiqc/)** reports (gold standard in bioinformatics QC reporting) and to develop workflows templates for popular bioinformatics pipelines (like nf-core) to make it easy to aggregate, visualize and analyze aggregated results.

In the end, the idea would be to provide a comprehensive platform that allows life science researchers to easily create interactive dashboards using **community-driven templates** for established workflows.

Similarly to run `multiqc .` in a terminal, to automatically scan bioinformatics QC data (cutadapt, fastqc, ...), you would be able to run `depictio --template nf-core/rnaseq` to automatically ingest workflow relevant data and fill a dashboard with pre-configured components for visualizing the results.

## 👥 Who is it for?

**Current users:**

- Researchers and data scientists seeking **code-free** dashboard creation
- Anyone working with datasets who wants **interactive exploration tools**

**Future target audience:**

- Life science researchers analyzing **high-throughput experimental data**
- Bioinformaticians working with **standardised pipeline outputs** and **multi-omics datasets**

## 🎨 Main current features

- **No-code dashboard creation**: Build interactive dashboards without writing code
- **Real-time interactivity**: Play with data using sliders, dropdowns, as well as box selection on scatter plots
- **Multi-table support**: Combine multiple data sources (so-called **Data Collections** in Depictio) in a single dashboard using SQL-like joining system
- **Authenticated or Unauthenticated Access**: Use the system with JWT-based authentication and Google Oauth or in unauthenticated mode (like the demo)
- **Docker-compose & Kubernetes ready**: Easy deployment options for production use
- **Companion CLI (depictio-cli)**: Command-line interface for managing projects, scan data, and upload datasets

## 🛠️ **[Modern Architecture](../../features/architecture.md)**

As mentioned earlier, even Depictio is actually based on **Plotly Dash**, the system is built on a state-of-the-art microservices architecture combining Plotly Dash, FastAPI, mongoDB and an optional on-premise MinIO bucket manager. A large part of the backend is responsible for managing data ingestion, processing and storage, while the frontend is responsible for rendering interactive dashboards. Data procesing is mainly done using the [Polars](https://www.pola.rs/) data engine, which is a high-performance DataFrame library, designed for fast data manipulation and analysis.

- **Frontend**: React with Dash and Mantine components
- **Backend**: FastAPI with async processing
- **Data Engine**: Polars for high-performance processing
- **Storage**: Delta Lake format stored on S3-compatible object storage
- **Deployment**: Docker & Kubernetes ready

## 🚀 How to Try It Out

Access the live demo at [demo.depictio.embl.org](https://demo.depictio.embl.org) or start using it below directly and explore the features. You can also create your own project and upload datasets to start dashboarding. Don't forget to check out the [guides](../../usage/README.md) for step-by-step instructions on how to use the system.

!!! note
    The demo is running a "unauthenticated mode" to allow anyone to try it out without needing an account. However, you can create a temporary account to create your own projects and upload datasets. Accounts and related data will be reset after 24 hours to keep the demo environment clean.

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
*January 2025*
