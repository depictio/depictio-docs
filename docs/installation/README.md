---
title: "Installation"
icon: material/package
description: "Get started with Depictio by choosing the installation method that best suits your needs."
---

# Installation

## :material-rocket-launch: Quickstart

No git clone, no configuration file.

```bash title="Terminal" linenums="1"
curl -LO https://raw.githubusercontent.com/depictio/depictio/main/docker-compose.yaml # (1)!
docker compose up -d # (2)!
```

1.  :material-download: Downloads the single compose file — nothing else needed locally.
2.  :material-play-circle: Starts **all six services** in the background: MongoDB, Redis, MinIO, backend API, frontend, and Celery worker.

!!! success "Open Depictio"

    | | Service | URL | Notes |
    |-|---------|-----|-------|
    | :material-view-dashboard: | **Depictio** | [localhost:5080](http://localhost:5080) | Single-user mode — no login required |
    | :material-api: | **API docs** | [localhost:8058/docs](http://localhost:8058/docs) | Interactive OpenAPI interface |
    | :simple-minio: | **MinIO console** | [localhost:9001](http://localhost:9001) | `minio` / `minio123` |

<div class="grid cards" markdown>

-   :material-pencil: **Customise credentials**

    ---

    Copy `.env.example` to `.env` to change the MinIO password or switch to multi-user mode.

    [:octicons-arrow-right-24: Advanced configuration](docker/#advanced-configuration)

-   :material-account-group: **Multi-user or public mode?**

    ---

    Set `DEPICTIO_AUTH_SINGLE_USER_MODE=false` in `.env` to enable accounts and login.

    [:octicons-arrow-right-24: Authentication modes](../usage/guides/authentication-modes.md)

</div>

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

-   :material-cloud-braces:{ .lg .middle } **Try in GitHub Codespaces**

    ---

    Launch a temporary cloud workspace with Depictio pre-configured — no local setup required.

    [:octicons-arrow-right-24: Open in Codespaces](https://codespaces.new/depictio/depictio)

</div>
