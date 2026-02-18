---
title: "Home"
icon: material/home
description: "Depictio is a modern, interactive platform that enables dashboards creation from bioinformatics workflows outputs."
hide:
  - navigation
  - toc
  - path
---


#


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

    <p class="hero-description">
      A modern open-source platform that transforms bioinformatics workflow outputs into interactive dashboards.<br>
      <span class="hero-subtext">Build, share, and explore data visualizations with or without writing code.</span>
    </p>

  </div>

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

</section>

<!-- Workflow Integration Section -->
<section class="workflow-section">
  <div class="workflow-content">
    <h2 class="workflow-title">Workflow Ecosystem</h2>
    <p class="workflow-description">
      Connect with standardized bioinformatics workflows from various platforms.
    </p>
    <div class="workflow-logos">
      <div class="workflow-card">
        <a href="https://nf-co.re/" target="_blank" rel="noopener">
          <img src="https://raw.githubusercontent.com/nf-core/logos/refs/heads/master/nf-core-logos/nf-core-logo.png" alt="nf-core logo" class="workflow-logo nf-core-logo nf-core-light">
          <img src="https://raw.githubusercontent.com/nf-core/logos/refs/heads/master/nf-core-logos/nf-core-logo-darkbg.png" alt="nf-core logo" class="workflow-logo nf-core-logo nf-core-dark">
        </a>
      </div>
      <div class="workflow-card">
        <a href="https://workflowhub.eu/" target="_blank" rel="noopener">
          <img src="https://about.workflowhub.eu/assets/img/workflowhub-square.svg" alt="WorkflowHub logo" class="workflow-logo">
        </a>
      </div>
      <div class="workflow-card">
        <a href="https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html#catalog" target="_blank" rel="noopener" class="snakemake-catalog-link">
          <img src="https://avatars.githubusercontent.com/u/33450111?v=4" alt="Snakemake logo" class="workflow-logo">
          <span class="workflow-label">Snakemake Workflow Catalog</span>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Dashboard Components Section -->
<section class="components-section">
  <div class="components-content">
    <h2 class="components-title">Dashboard Components</h2>
    <p class="components-description">
      Build powerful dashboards with a rich library of interactive components.
    </p>
    <div class="components-grid">
      <div class="component-card">
        <div class="component-icon" style="background: var(--depictio-purple);">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.45,15.18L22,7.31V19L22,21H2V3H4V15.54L9.5,6L16,9.78L20.24,2.45L21.97,3.45L16.74,12.5L10.23,8.75L4.31,19H6.57L10.96,11.44L17.45,15.18Z"/>
          </svg>
        </div>
        <h4>Figure</h4>
        <p>Scatter, bar, box, histogram, line plots and more with Plotly</p>
      </div>
      <div class="component-card">
        <div class="component-icon" style="background: var(--depictio-blue);">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M5,4H19A2,2 0 0,1 21,6V18A2,2 0 0,1 19,20H5A2,2 0 0,1 3,18V6A2,2 0 0,1 5,4M5,8V12H11V8H5M13,8V12H19V8H13M5,14V18H11V14H5M13,14V18H19V14H13Z"/>
          </svg>
        </div>
        <h4>Table</h4>
        <p>Interactive AG Grid tables with filtering, sorting, and export</p>
      </div>
      <div class="component-card">
        <div class="component-icon" style="background: var(--depictio-teal);">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M5,3A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3H5M7,7H17V9H7V7M7,11H14V13H7V11M7,15H17V17H7V15Z"/>
          </svg>
        </div>
        <h4>Card</h4>
        <p>Metric cards with aggregations (count, sum, mean, min, max)</p>
      </div>
      <div class="component-card">
        <div class="component-icon" style="background: var(--depictio-green);">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7,5H21V7H7V5M7,13V11H21V13H7M4,4.5A1.5,1.5 0 0,1 5.5,6A1.5,1.5 0 0,1 4,7.5A1.5,1.5 0 0,1 2.5,6A1.5,1.5 0 0,1 4,4.5M4,10.5A1.5,1.5 0 0,1 5.5,12A1.5,1.5 0 0,1 4,13.5A1.5,1.5 0 0,1 2.5,12A1.5,1.5 0 0,1 4,10.5M7,19V17H21V19H7M4,16.5A1.5,1.5 0 0,1 5.5,18A1.5,1.5 0 0,1 4,19.5A1.5,1.5 0 0,1 2.5,18A1.5,1.5 0 0,1 4,16.5Z"/>
          </svg>
        </div>
        <h4>Interactive</h4>
        <p>Filters with sliders, dropdowns, and date pickers</p>
      </div>
      <div class="component-card">
        <div class="component-icon multiqc-logo-icon">
          <img src="https://raw.githubusercontent.com/MultiQC/logo/main/logos/multiqc_icon_color.svg" alt="MultiQC">
        </div>
        <h4>MultiQC</h4>
        <p>Quality control reports embedded in dashboards</p>
      </div>
      <div class="component-card">
        <div class="component-icon" style="background: var(--depictio-pink);">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M22,16V4A2,2 0 0,0 20,2H8A2,2 0 0,0 6,4V16A2,2 0 0,0 8,18H20A2,2 0 0,0 22,16M11,12L13.03,14.71L16,11L20,16H8M2,6V20A2,2 0 0,0 4,22H18V20H4V6"/>
          </svg>
        </div>
        <h4>Image</h4>
        <p>Image galleries with S3/MinIO storage integration</p>
      </div>
    </div>
  </div>
</section>

<!-- Live Demo Section -->

<section class="live-demo-section">
  <div class="live-demo-info">
    <!-- Unified Demo Card with Badge and Expandable Info -->
    <div class="demo-note-card">
      <div class="demo-note-header" onclick="toggleDemoNote()">
        <div class="demo-badge-integrated">
          <span class="live-indicator"></span>
          <div class="demo-badge-content">
            <strong>Live interactive demo - Try it!</strong>
            <a href="https://demo.depictio.embl.org/" target="_blank" rel="noopener" class="demo-direct-link">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
              </svg>
            </a>
          </div>
        </div>
        <div class="demo-note-toggle">
          <svg class="demo-toggle-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"/>
          </svg>
        </div>
      </div>
      <div class="demo-note-content" id="demo-note-content">
        <p>The demo is running an <strong>"unauthenticated mode"</strong> to allow anyone to try it out without needing an account. However, you can create a temporary account to create your own projects and upload datasets.</p>
        <p><strong>Note:</strong> Accounts and related data will be reset after 1 hour to keep the demo environment clean.</p>

        <div class="demo-alternatives">
          <h4>Get started with Depictio</h4>
          <div class="demo-alt-buttons">
            <a href="https://demo.depictio.embl.org/" class="demo-alt-btn demo-btn" target="_blank" rel="noopener">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
              </svg>
              Try Demo Directly
            </a>
            <a href="https://codespaces.new/depictio/depictio" class="demo-alt-btn" target="_blank" rel="noopener">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              Open in Codespaces
            </a>
            <a href="installation/docker/" class="demo-alt-btn install-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
              Install Locally
            </a>
          </div>
        </div>
      </div>
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


<!-- Technology Stack Section -->
<section class="tech-section">
  <div class="container text-center">
    <h2>Powered by Modern Technologies</h2>
    <div class="tech-badges">
      <a href="https://dash.plotly.com/" target="_blank" rel="noopener" class="tech-badge plotly">
        <img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" alt="Plotly">
        <span>Dash</span>
      </a>
      <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener" class="tech-badge fastapi">
        <img src="https://fastapi.tiangolo.com/img/icon-white.svg" alt="FastAPI">
        <span>FastAPI</span>
      </a>
      <a href="https://www.mongodb.com/" target="_blank" rel="noopener" class="tech-badge mongodb">
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" alt="MongoDB">
        <span>MongoDB</span>
      </a>
      <a href="https://min.io/" target="_blank" rel="noopener" class="tech-badge minio">
        <img src="https://cdn.prod.website-files.com/681c8426519d8db8f867c1e8/682dcb06620717ccd769b572_MINIO_Bird.png" alt="MinIO">
        <span>MinIO</span>
      </a>
      <a href="https://pola.rs/" target="_blank" rel="noopener" class="tech-badge polars">
        <img src="https://raw.githubusercontent.com/pola-rs/polars-static/master/logos/polars-logo-dark.svg" alt="Polars">
        <span>Polars</span>
      </a>
    </div>
  </div>
</section>

<section class="overview-section">
  <h2>Project Overview</h2>
  <div class="overview-content">
    <div class="challenge-box">
      <div class="challenge-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"/>
        </svg>
      </div>
      <div class="challenge-content">
        <h3>The Challenge</h3>
        <p>Bioinformatics researchers face significant challenges managing and analyzing large-scale datasets from production workflows. Despite numerous available tools, there's a notable absence of platforms designed for seamless integration with production workflows.</p>
      </div>
    </div>

    <div class="solution-box">
      <div class="solution-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"/>
        </svg>
      </div>
      <div class="solution-content">
        <h3>Our Solution</h3>
        <p>Depictio addresses this gap with a generic, centralized platform that integrates workflow output data to build interactive dashboards. It provides scalable, flexible, and open-source solutions for researchers handling large datasets from any execution engine (Nextflow, Snakemake, Galaxy, R, etc.).</p>
      </div>
    </div>
  </div>
</section>

<!-- Goals Section -->
<section class="goals-section">
  <h2>Why Depictio?</h2>
  <div class="goals-grid">
    <div class="goal-card">
      <div class="goal-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,12.5A1.5,1.5 0 0,1 10.5,11A1.5,1.5 0 0,1 12,9.5A1.5,1.5 0 0,1 13.5,11A1.5,1.5 0 0,1 12,12.5M12,7.2C9.9,7.2 8.2,8.9 8.2,11C8.2,14 12,17.5 12,17.5C12,17.5 15.8,14 15.8,11C15.8,8.9 14.1,7.2 12,7.2Z"/>
        </svg>
      </div>
      <h3>No Code Required</h3>
      <p>Create interactive dashboards without writing code. Drag and drop components, configure visualizations through the UI.</p>
    </div>
    <div class="goal-card">
      <div class="goal-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/>
        </svg>
      </div>
      <h3>Workflow Integration</h3>
      <p>Connect directly to Nextflow, Snakemake, Galaxy outputs. Automatically ingest results from production pipelines.</p>
    </div>
    <div class="goal-card">
      <div class="goal-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
        </svg>
      </div>
      <h3>Shareable & Reproducible</h3>
      <p>Export dashboards as YAML for version control. Share with collaborators, deploy across environments.</p>
    </div>
    <div class="goal-card">
      <div class="goal-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.5,12C18,12 20,14 20,16.5C20,17.38 19.75,18.21 19.31,18.9L22.39,22L21,23.39L17.88,20.32C17.19,20.75 16.37,21 15.5,21C13,21 11,19 11,16.5C11,14 13,12 15.5,12M15.5,14A2.5,2.5 0 0,0 13,16.5A2.5,2.5 0 0,0 15.5,19A2.5,2.5 0 0,0 18,16.5A2.5,2.5 0 0,0 15.5,14M5,3H19C20.1,3 21,3.89 21,5V13.03C20.5,12.23 19.81,11.54 19,11V5H5V19H9.5C9.81,19.75 10.26,20.42 10.81,21H5C3.9,21 3,20.1 3,19V5A2,2 0 0,1 5,3M7,7H17V9H7V7M7,11H12.03C11.23,11.5 10.54,12.19 10,13H7V11M7,15H9.17C9.06,15.5 9,16 9,16.5V17H7V15Z"/>
        </svg>
      </div>
      <h3>Real-time Exploration</h3>
      <p>Filter and interact with data in real-time. Cross-filter between components for deep data exploration.</p>
    </div>
  </div>
</section>

<section class="key-features-section">
  <h2>Key Features</h2>
  <div class="features-container">
    <div class="feature-box data-ingestion">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
        </svg>
      </div>
      <h3>Data Ingestion</h3>
      <ul>
        <li><strong>Client-side processing:</strong> Depictio-CLI scans and processes data locally, pushing results to S3</li>
        <li><strong>Multiple formats:</strong> Support for Parquet, CSV, JSON, TSV using Polars and Delta Lake</li>
        <li><strong>Automatic aggregation:</strong> Combine files across workflow runs into unified datasets</li>
        <li><strong>MultiQC integration:</strong> Seamless QC report visualization with dedicated components</li>
      </ul>
    </div>

    <div class="feature-box frontend">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"/>
        </svg>
      </div>
      <h3>Frontend & Visualization</h3>
      <ul>
        <li><strong>Drag-and-drop dashboards:</strong> Build layouts visually without coding</li>
        <li><strong>Cross-component filtering:</strong> Interactive filters affect all linked visualizations</li>
        <li><strong>Code Mode:</strong> Write custom Python/Plotly code for advanced visualizations</li>
        <li><strong>Project organization:</strong> Group dashboards by projects with user permissions</li>
      </ul>
    </div>

    <div class="feature-box system">
      <div class="feature-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M4,6H20V16H4M20,18A2,2 0 0,0 22,16V6C22,4.89 21.1,4 20,4H4C2.89,4 2,4.89 2,6V16A2,2 0 0,0 4,18H0V20H24V18H20Z"/>
        </svg>
      </div>
      <h3>System & Infrastructure</h3>
      <ul>
        <li><strong>Cloud-ready:</strong> Built for Kubernetes and Docker-Compose environments</li>
        <li><strong>YAML Dashboard Sync:</strong> Import and export dashboards as human-readable YAML files for version control and Infrastructure-as-Code workflows</li>
        <li><strong>S3/MinIO Storage:</strong> Scalable object storage for data files and images</li>
        <li><strong>Delta Lake:</strong> ACID transactions and versioned data tables</li>
        <li><strong>Open-source:</strong> Community-driven development with transparent deployment</li>
      </ul>
    </div>
  </div>
</section>

<section class="getting-started-section">
  <h2>Getting Started</h2>
  <p class="getting-started-intro">Ready to get started with Depictio?</p>

  <div class="installation-grid">
    <a href="installation/docker/" class="installation-card docker">
      <div class="card-icon">
        <img src="assets/docker.svg" alt="Docker" width="24" height="24">
      </div>
      <div class="card-content">
        <h3>Docker Compose</h3>
        <p>Quickest way to get started</p>
        <span class="card-badge recommended">Recommended</span>
      </div>
      <div class="card-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>
        </svg>
      </div>
    </a>

    <a href="installation/kubernetes/" class="installation-card kubernetes">
      <div class="card-icon">
        <img src="assets/kubernetes.svg" alt="Kubernetes" width="24" height="24">
      </div>
      <div class="card-content">
        <h3>Kubernetes</h3>
        <p>For production environments</p>
        <span class="card-badge production">Production</span>
      </div>
      <div class="card-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>
        </svg>
      </div>
    </a>

    <a href="installation/cli/" class="installation-card cli">
      <div class="card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M20,19V7H4V19H20M20,3A2,2 0 0,1 22,5V19A2,2 0 0,1 20,21H4A2,2 0 0,1 2,19V5C2,3.89 2.9,3 4,3H20M13,17V15H18V17H13M9.58,13L5.57,9H8.4L11.7,12.3C12.09,12.69 12.09,13.33 11.7,13.72L8.42,17H5.59L9.58,13Z"/>
        </svg>
      </div>
      <div class="card-content">
        <h3>CLI Tools</h3>
        <p>For data ingestion and management</p>
        <span class="card-badge tools">Tools</span>
      </div>
      <div class="card-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>
        </svg>
      </div>
    </a>
  </div>
</section>

<!-- Funding Section -->
<section class="funding-section">
  <h2>Funding</h2>

  <!-- Statement about academic and public funding in a single sentence -->
  <p class="funding-intro">Depictio is developed with the support of academic and public funding, enabling us to provide a free and open-source platform for the bioinformatics community.</p>

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
</section>

<!-- Academic Partners Section -->
<section class="partners-section">
  <h2>Academic Partners</h2>
  <div class="partners-container">
    <div class="partner-card">
      <img src="./assets/scilifelab_logo.png" alt="SciLifeLab Logo">
      <h3>SciLifeLab Data Centre</h3>
      <p>SciLifeLab Data Centre provides data-driven life science research infrastructure and expertise to accelerate open science in Sweden and beyond.</p>
      <a href="https://www.scilifelab.se/data/" class="md-button" target="_blank">Learn More</a>
    </div>
  </div>
</section>

<style>
  /* CSS Variables for Theme Compatibility */
  :root {
    --depictio-purple: #9966cc;
    --depictio-violet: #7a5dc7;
    --depictio-blue: #6495ed;
    --depictio-teal: #45b8ac;
    --depictio-green: #8bc34a;
    --depictio-yellow: #f9cb40;
    --depictio-orange: #f68b33;
    --depictio-pink: #e6779f;
    --depictio-red: #e53935;
  }

  /* Dark theme support */
  [data-md-color-scheme="slate"] {
    --md-primary-fg-color: var(--depictio-blue);
    --md-accent-fg-color: var(--depictio-purple);
  }

  /* Light theme logo visibility */
  [data-md-color-scheme="default"] .logo-light {
    display: none;
  }

  [data-md-color-scheme="default"] .logo-dark {
    display: block;
  }

  /* Dark theme logo visibility */
  [data-md-color-scheme="slate"] .logo-dark {
    display: none;
  }

  [data-md-color-scheme="slate"] .logo-light {
    display: block;
  }

  /* nf-core logo theme support */
  [data-md-color-scheme="default"] .nf-core-dark {
    display: none;
  }

  [data-md-color-scheme="default"] .nf-core-light {
    display: block;
  }

  [data-md-color-scheme="slate"] .nf-core-light {
    display: none;
  }

  [data-md-color-scheme="slate"] .nf-core-dark {
    display: block;
  }

.md-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.md-button svg {
  vertical-align: middle;
  margin-top: -1px; /* Fine-tune vertical position */
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
  border: 1px solid var(--md-default-fg-color--lightest);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  background-color: var(--md-default-bg-color);
}

[data-md-color-scheme="slate"] .funding-card {
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
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
  border: 1px solid var(--md-default-fg-color--lightest);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  display: flex;
  flex-direction: column;
  background-color: var(--md-default-bg-color);
}

[data-md-color-scheme="slate"] .partner-card {
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
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
  .hero-section {
    text-align: center;
  }

  .hero-section img {
    margin-bottom: 1.5rem;
    display: block;
    margin-left: auto;
    margin-right: auto;
  }

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
    text-decoration: none;
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

  .hero-subtext {
    font-size: 1rem;
    color: var(--md-default-fg-color--light);
    display: block;
    margin-top: 0.5rem;
  }

  /* Dashboard Components Section */
  .components-section {
    background: #ffffff;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 0 -2rem;
  }

  [data-md-color-scheme="slate"] .components-section {
    background: transparent;
  }

  .components-content {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
  }

  .components-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--md-default-fg-color);
    margin: 0 0 1rem 0;
    line-height: 1.2;
  }

  .components-description {
    font-size: 1.2rem;
    color: var(--md-default-fg-color--light);
    margin-bottom: 2.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .components-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    max-width: 900px;
    margin: 0 auto;
  }

  .component-card {
    background: var(--md-default-bg-color);
    border-radius: 12px;
    padding: 1.5rem 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--md-default-fg-color--lightest);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-align: center;
  }

  [data-md-color-scheme="slate"] .component-card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .component-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .component-icon {
    width: 48px;
    height: 48px;
    margin: 0 auto 1rem auto;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .component-icon svg {
    width: 24px;
    height: 24px;
  }

  .component-icon.multiqc-logo-icon {
    background: transparent;
  }

  .component-icon.multiqc-logo-icon img {
    width: 48px;
    height: 48px;
    object-fit: contain;
  }

  .component-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
  }

  .component-card p {
    margin: 0;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light);
    line-height: 1.5;
  }

  @media (max-width: 900px) {
    .components-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 768px) {
    .components-section {
      padding: 1rem 1rem 2rem 1rem;
      margin: 0 -1rem;
    }
  }

  @media (max-width: 500px) {
    .components-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Goals Section */
  .goals-section {
    background: #f8fafc;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 0 -2rem;
  }

  [data-md-color-scheme="slate"] .goals-section {
    background: rgba(255, 255, 255, 0.03);
  }

  .goals-section h2 {
    text-align: center;
    margin-top: 0;
  }

  .goals-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    max-width: 1200px;
    margin: 2rem auto 0 auto;
  }

  .goal-card {
    background: var(--md-default-bg-color);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--md-default-fg-color--lightest);
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  [data-md-color-scheme="slate"] .goal-card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .goal-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  .goal-icon {
    width: 56px;
    height: 56px;
    margin: 0 auto 1rem auto;
    background: linear-gradient(135deg, var(--depictio-purple) 0%, var(--depictio-blue) 100%);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .goal-icon svg {
    width: 28px;
    height: 28px;
  }

  .goal-card h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
  }

  .goal-card p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--md-default-fg-color--light);
    line-height: 1.6;
  }

  @media (max-width: 1024px) {
    .goals-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 768px) {
    .goals-section {
      padding: 1rem 1rem 2rem 1rem;
      margin: 0 -1rem;
    }
  }

  @media (max-width: 480px) {
    .goals-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Workflow Section */
  .workflow-section {
    background: #f8fafc;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 0 -2rem;
    border-radius: 0;
  }

  .workflow-content {
    max-width: 1000px;
    margin: 0 auto;
    text-align: center;
  }

  .workflow-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--md-default-fg-color);
    margin: 0 0 1rem 0;
    line-height: 1.2;
  }

  .workflow-description {
    font-size: 1.2rem;
    color: var(--md-default-fg-color--light);
    margin-bottom: 3rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .workflow-logos {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: nowrap;
    gap: 40px;
    width: 100%;
    overflow-x: auto;
  }

  .workflow-card {
    background: var(--md-default-bg-color);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--md-default-fg-color--lightest);
    transition: all 0.3s ease;
    min-width: 220px;
    height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  [data-md-color-scheme="slate"] .workflow-card {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
  }

  .workflow-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  }

  .workflow-card a {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: inherit;
  }

  .workflow-label {
    margin-top: 1rem;
    font-weight: 600;
    font-size: 1rem;
    color: var(--md-default-fg-color);
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

  /* Header Styles */
  h2 {
    font-size: 2.25rem;
    font-weight: 900;
    color: var(--md-default-fg-color);
    margin: 3rem 0 1.5rem 0;
    line-height: 1.2;
    letter-spacing: -0.025em;
    font-stretch: ultra-condensed;
    font-variation-settings: "wght" 650;
    transform: scaleX(0.95);
  }

  h3 {
    font-size: 1.75rem;
    font-weight: 900;
    color: var(--md-default-fg-color);
    margin: 2.5rem 0 1rem 0;
    line-height: 1.3;
    letter-spacing: -0.02em;
    font-stretch: condensed;
  }

  h4 {
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--md-default-fg-color--light);
    margin: 2rem 0 0.75rem 0;
    line-height: 1.4;
    font-stretch: condensed;
  }

  /* Dark theme header adjustments */
  [data-md-color-scheme="slate"] h2,
  [data-md-color-scheme="slate"] h3 {
    color: var(--md-default-fg-color);
  }

  [data-md-color-scheme="slate"] h4 {
    color: var(--md-default-fg-color--light);
  }

  /* Technology Stack Section */
  .tech-section {
    margin: 2rem 0;
  }

  .tech-section h2 {
    margin-bottom: 1.5rem;
    color: var(--md-default-fg-color);
  }

  .tech-badges {
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
    overflow-x: auto;
  }

  .tech-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 700;
    color: #2d3748;
    text-decoration: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .tech-badge img {
    width: 20px;
    height: 20px;
    object-fit: contain;
  }

  .tech-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  /* Individual technology colors */
  .tech-badge.plotly {
    background: linear-gradient(135deg, #5a6bc4 0%, #495ab3 100%);
    color: white;
  }

  .tech-badge.fastapi {
    background: linear-gradient(135deg, #4db6ac 0%, #409a94 100%);
    color: white;
  }

  .tech-badge.mongodb {
    background: linear-gradient(135deg, #66bb6a 0%, #5aa05e 100%);
    color: white;
  }

  .tech-badge.minio {
    background: linear-gradient(135deg, #ff8a80 0%, #e57373 100%);
    color: white;
  }

  .tech-badge.polars {
    background: linear-gradient(135deg, #00a2e8 0%, #0080c7 100%);
    color: white;
  }

  /* Project Overview Section */
  .overview-section {
    margin: 3rem 0;
  }

  .overview-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
  }

  .challenge-box,
  .solution-box {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.5rem;
    border-radius: 12px;
    background: var(--md-default-bg-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--md-default-fg-color--lightest);
  }

  [data-md-color-scheme="slate"] .challenge-box,
  [data-md-color-scheme="slate"] .solution-box {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .challenge-box {
    border-left: 4px solid #F68B33;
  }

  .solution-box {
    border-left: 4px solid #8BC34A;
  }

  .challenge-icon,
  .solution-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 0.25rem;
  }

  .challenge-icon {
    background: #F68B33;
    color: white;
  }

  .solution-icon {
    background: #8BC34A;
    color: white;
  }

  .challenge-icon svg,
  .solution-icon svg {
    width: 20px;
    height: 20px;
  }

  .challenge-content h3,
  .solution-content h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
  }

  .challenge-content p,
  .solution-content p {
    margin: 0;
    line-height: 1.6;
    color: var(--md-default-fg-color--light);
  }

  @media (max-width: 768px) {
    .overview-content {
      grid-template-columns: 1fr;
    }
  }

  /* Key Features Section */
  .key-features-section {
    margin: 3rem 0;
  }

  .features-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .feature-box {
    background: var(--md-default-bg-color);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--md-default-fg-color--lightest);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
  }

  [data-md-color-scheme="slate"] .feature-box {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .feature-box:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .feature-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--feature-color);
  }

  .feature-box.data-ingestion {
    --feature-color: #9966CC;
  }

  .feature-box.frontend {
    --feature-color: #6495ED;
  }

  .feature-box.system {
    --feature-color: #45B8AC;
  }

  .feature-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 1rem;
    background: var(--feature-color);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    flex-shrink: 0;
    position: relative;
  }

  .feature-icon svg {
    width: 24px;
    height: 24px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    fill: currentColor;
  }

  .feature-box h3 {
    margin: 0 0 1rem 0;
    color: var(--md-default-fg-color);
    font-size: 1.25rem;
    font-weight: 600;
  }

  .feature-box ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .feature-box li {
    margin-bottom: 0.75rem;
    color: var(--md-default-fg-color--light);
    line-height: 1.5;
    position: relative;
    padding-left: 1.5rem;
  }

  .feature-box li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0.6rem;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--feature-color);
  }

  .feature-box li:last-child {
    margin-bottom: 0;
  }

  .feature-box strong {
    color: var(--md-default-fg-color);
  }

  @media (max-width: 768px) {
    .features-container {
      grid-template-columns: 1fr;
    }

    .feature-box {
      padding: 1.5rem;
    }
  }

  /* Getting Started Section */
  .getting-started-section {
    margin: 3rem 0;
  }

  .getting-started-intro {
    text-align: center;
    font-size: 1.1rem;
    color: var(--md-default-fg-color--light);
    margin-bottom: 2rem;
  }

  .installation-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .installation-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--md-default-bg-color);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--md-default-fg-color--lightest);
    text-decoration: none;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  [data-md-color-scheme="slate"] .installation-card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .installation-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--card-color);
  }

  .installation-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .installation-card.docker {
    --card-color: #9966CC;
  }

  .installation-card.kubernetes {
    --card-color: #6495ED;
  }

  .installation-card.cli {
    --card-color: #45B8AC;
  }

  .card-icon {
    width: 48px;
    height: 48px;
    background: var(--card-color);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    flex-shrink: 0;
  }

  .card-icon svg {
    width: 24px;
    height: 24px;
  }

  .card-icon img {
    width: 24px;
    height: 24px;
    filter: brightness(0) invert(1);
  }

  .card-content {
    flex: 1;
  }

  .card-content h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--md-default-fg-color);
  }

  .card-content p {
    margin: 0 0 0.75rem 0;
    color: var(--md-default-fg-color--light);
    font-size: 0.9rem;
  }

  .card-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .card-badge.recommended {
    background: rgba(153, 102, 204, 0.1);
    color: #9966CC;
  }

  .card-badge.production {
    background: rgba(100, 149, 237, 0.1);
    color: #6495ED;
  }

  .card-badge.tools {
    background: rgba(69, 184, 172, 0.1);
    color: #45B8AC;
  }

  .card-arrow {
    width: 24px;
    height: 24px;
    color: var(--card-color);
    flex-shrink: 0;
    opacity: 0.7;
    transition: opacity 0.3s ease, transform 0.3s ease;
  }

  .installation-card:hover .card-arrow {
    opacity: 1;
    transform: translateX(4px);
  }

  .card-arrow svg {
    width: 100%;
    height: 100%;
  }

  @media (max-width: 768px) {
    .installation-grid {
      grid-template-columns: 1fr;
    }
  }

  /* Section Background Alternation */
  .workflow-section,
  .tech-section,
  .key-features-section,
  .funding-section {
    background: #f8fafc;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 0 -2rem;
    border-radius: 0;
  }

  .overview-section,
  .getting-started-section,
  .partners-section {
    background: #ffffff;
    padding: 1.5rem 2rem 4rem 2rem;
    margin: 0 -2rem 0 -2rem;
    margin-bottom: 0 !important;
  }

  /* Dark theme section backgrounds */
  [data-md-color-scheme="slate"] .workflow-section,
  [data-md-color-scheme="slate"] .tech-section,
  [data-md-color-scheme="slate"] .key-features-section,
  [data-md-color-scheme="slate"] .funding-section {
    background: rgba(255, 255, 255, 0.03);
  }

  [data-md-color-scheme="slate"] .overview-section,
  [data-md-color-scheme="slate"] .getting-started-section,
  [data-md-color-scheme="slate"] .partners-section {
    background: transparent;
  }

  .workflow-section h2,
  .tech-section h2,
  .key-features-section h2,
  .overview-section h2,
  .getting-started-section h2,
  .funding-section h2,
  .partners-section h2 {
    margin-top: 0;
  }

  @media (max-width: 768px) {
    .workflow-section,
    .tech-section,
    .key-features-section,
    .getting-started-section,
    .overview-section,
    .funding-section,
    .partners-section {
      padding: 1rem 1rem 2rem 1rem;
      margin: 0 -1rem;
    }
  }

  /* Demo Unavailable Message Styles */
  .demo-unavailable-message {
    background: #f8fafc;
    padding: 1.5rem 2rem 3rem 2rem;
    margin: 0 -2rem;
    border-radius: 0;
    text-align: center;
  }

  [data-md-color-scheme="slate"] .demo-unavailable-message {
    background: rgba(255, 255, 255, 0.03);
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
    color: var(--depictio-purple);
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

  @media (max-width: 768px) {
    .demo-unavailable-message {
      padding: 1rem 1rem 2rem 1rem;
      margin: 0 -1rem;
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
</style>

<script>
function toggleDemoNote() {
  const content = document.getElementById('demo-note-content');
  const toggle = document.querySelector('.demo-note-toggle');

  content.classList.toggle('expanded');
  toggle.classList.toggle('expanded');
}

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
          <a href="https://codespaces.new/depictio/depictio" class="md-button" target="_blank" rel="noopener">Open in Codespaces</a>
          <a href="usage/get_started/" class="md-button">View Documentation</a>
        </div>
      </div>
    `;

    // Insert the fallback message after the workflow section
    const workflowSection = document.querySelector('.workflow-section');
    if (workflowSection) {
      workflowSection.insertAdjacentElement('afterend', fallbackMessage);
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
