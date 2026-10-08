---
title: "Installation"
icon: material/package
description: "Get started with Depictio by choosing the installation method that best suits your needs."
---

# Installation

## :material-rocket-launch: Quickstart

No git clone, no configuration file.

```bash title="1 — Download"
curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml
```

```bash title="2 — Start"
docker compose up -d
```

!!! success "Open Depictio"

    | | Service | URL | Notes |
    |-|---------|-----|-------|
    | :material-view-dashboard: | **Depictio** | [localhost:5080](http://localhost:5080) | Single-user mode — no login required |
    | :material-api: | **API docs** | [localhost:8058/docs](http://localhost:8058/docs) | Interactive OpenAPI interface |

<div class="grid cards" markdown>

-   :material-pencil: **Customise credentials**

    ---

    Copy `.env.example` to `.env` to change the S3 password or switch to multi-user mode.

    [:octicons-arrow-right-24: Advanced configuration](docker/#advanced-configuration)

-   :material-account-group: **Multi-user or public mode?**

    ---

    Set `DEPICTIO_AUTH_SINGLE_USER_MODE=false` in `.env` to enable accounts and login.

    [:octicons-arrow-right-24: Authentication modes](../usage/guides/authentication-modes.md)

</div>

---

## Server Deployment

Three ways to run the same Depictio server, which differ in how its services run.

<div class="grid cards" markdown>

-   :simple-kubernetes:{ .lg .middle } **Kubernetes** · Helm chart

    ---

    Deploy Depictio on a Kubernetes cluster with the official Helm chart.

    Ideal for production environments and scalable deployments.

    [:octicons-arrow-right-24: Installation guide](kubernetes/)

-   :simple-docker:{ .lg .middle } **Docker Compose** · containers

    ---

    The recommended way to run Depictio. One compose file starts every service in containers, object storage included. Upgrading from before v1.12.0? Copy the former MinIO store's data first: [Upgrading to v1.12.0](upgrade/v1.12.0-seaweedfs.md).

    Ideal for development, testing, and small-scale deployments.

    [:octicons-arrow-right-24: Installation guide](docker/)

-   :simple-python:{ .lg .middle } **Python package** · pip / uv, no containers

    ---

    Install `depictio[local]` with uv or pip: `depictio local up` then runs every service as a local process on your machine.

    Ideal for reviewing a template on your own results, on a laptop.

    [:octicons-arrow-right-24: Installation guide](local/)

</div>

## CLI & Configuration

<div class="grid cards" markdown>

-   :material-console-line:{ .lg .middle } **Depictio CLI**

    ---

    Command-line tool for data ingestion, project management, and interacting with the Depictio API.

    [:octicons-arrow-right-24: CLI guide](cli/)

-   :material-cog-outline:{ .lg .middle } **Configuration**

    ---

    Configure authentication, S3 storage, backups, and advanced features via environment variables.

    [:octicons-arrow-right-24: Configuration guide](configuration/)

-   :material-cloud-braces:{ .lg .middle } **Try in GitHub Codespaces**

    ---

    Launch a temporary cloud workspace with Depictio pre-configured — no local setup required. Boots in single-user mode with the Iris reference project pre-seeded and the viewer opened automatically.

    [:octicons-arrow-right-24: Open in Codespaces](https://codespaces.new/depictio/depictio)

</div>
