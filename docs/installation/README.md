---
title: "Installation"
icon: material/package
description: "Get started with Depictio by choosing the installation method that best suits your needs."
---

# Installation

## Depictio (server)

<div class="installation-grid">
  <div class="installation-card">
    <img src="../assets/docker-compose.webp" alt="Docker Compose" class="card-logo" width="100px">
    <h3>Docker Compose</h3>
    <p>For development, testing, and small-scale deployments.</p>
    <a href="docker/" class="md-button md-button--primary">Guide</a>
  </div>

  <div class="installation-card">
    <img src="../assets/kubernetes.png" alt="Kubernetes" class="card-logo" width="100px">
    <h3>Kubernetes</h3>
    <p>For production environments and scalable deployments.</p>
    <a href="kubernetes/" class="md-button md-button--primary">Guide</a>
  </div>
</div>

## Depictio-CLI

<div class="cli-container">
  <div class="installation-card">
    <img src="../assets/depictio-cli.png" alt="Depictio CLI" class="card-logo">
    <h3>Depictio-CLI</h3>
    <p>For data ingestion and management.</p>
    <a href="cli/" class="md-button md-button--primary">Guide</a>
  </div>
</div>

## Configuration

<div class="cli-container">
  <div class="installation-card">
    <img src="../assets/depictio-configuration.png" alt="Depictio Configuration" class="card-logo">
    <h3>Environment Variables</h3>
    <p>Configure authentication, backups, and advanced features.</p>
    <a href="configuration/" class="md-button md-button--primary">Guide</a>
  </div>
</div>

<style>
/* Installation Cards Grid */
.installation-grid {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.installation-card {
  flex: 0 1 300px;
  padding: 1.25rem;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,0.1);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: center;
  background-color: white;
}

.card-logo {
  height: 60px;
  margin-bottom: 1rem;
}

.installation-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.installation-card p {
  color: var(--md-default-fg-color--light);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

/* CLI Container */
.cli-container {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0;
}

.cli-container .installation-card {
  max-width: 300px;
}

@media (max-width: 650px) {
  .installation-grid {
    flex-direction: column;
    align-items: center;
  }

  .installation-card {
    width: 100%;
    max-width: 300px;
  }
}
</style>
