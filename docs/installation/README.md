---
title: "Installation"
icon: material/package
description: "Get started with Depictio by choosing the installation method that best suits your needs."
---

# Installation

## Quickstart

No configuration file needed — MinIO is bundled by default:

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
docker compose up -d
```

| Service | URL |
|---------|-----|
| Depictio | <http://localhost:5080> |
| API docs | <http://localhost:8058/docs> |
| MinIO console | <http://localhost:9001> (minio / minio123) |

---

## Server Deployment

<div class="grid cards" markdown>

-   :fontawesome-brands-docker:{ .lg .middle } **Docker Compose**

    ---

    The recommended way to run Depictio. MinIO is bundled — one command starts everything.

    Ideal for development, testing, and small-scale deployments.

    [:octicons-arrow-right-24: Installation guide](docker/)

-   :simple-kubernetes:{ .lg .middle } **Kubernetes**

    ---

    Deploy Depictio on a Kubernetes cluster using the official Helm chart.

    Ideal for production environments and scalable deployments.

    [:octicons-arrow-right-24: Installation guide](kubernetes/)

</div>

## CLI & Configuration

<div class="grid cards" markdown>

-   :material-console-line:{ .lg .middle } **Depictio CLI**

    ---

    Command-line tool for data ingestion, project management, and interacting with the Depictio API.

    [:octicons-arrow-right-24: CLI guide](cli/)

-   :material-cog-outline:{ .lg .middle } **Configuration**

    ---

    Configure authentication, S3/MinIO, backups, and advanced features via environment variables.

    [:octicons-arrow-right-24: Configuration guide](configuration/)

-   :simple-gitpod:{ .lg .middle } **Try in Gitpod**

    ---

    Launch a temporary workspace with Depictio pre-installed — no local setup required.

    [:octicons-arrow-right-24: Open in Gitpod](https://gitpod.io/#https://github.com/depictio/depictio/releases/latest)

</div>
