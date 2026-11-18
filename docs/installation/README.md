---
title: "Installation"
icon: material/package
description: "Get started with Depictio by choosing the installation method that best suits your needs."
---

# Installation

Run a Depictio server, then install the CLI to load your data into it.

## :material-rocket-launch: Quickstart

No git clone, no configuration file.

```bash title="1. Download"
curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml
```

```bash title="2. Start"
docker compose up -d
```

!!! success "Open Depictio"

    | | Service | URL | Notes |
    |-|---------|-----|-------|
    | :material-view-dashboard: | **Depictio** | [localhost:5080](http://localhost:5080) | Single-user mode, no login required |
    | :material-api: | **API docs** | [localhost:8058/docs](http://localhost:8058/docs) | Interactive OpenAPI interface |

<div class="grid cards" markdown>

-   :material-pencil:{ .lg .middle .dp-blue } **Customise credentials**

    ---

    Copy `.env.example` to `.env` to change the S3 password.

    [:octicons-arrow-right-24: Advanced configuration](docker.md#advanced-configuration)

-   :material-cloud-braces:{ .lg .middle .dp-purple } **Try in GitHub Codespaces**

    ---

    The Python package in a cloud workspace, with two example projects.

    [:octicons-arrow-right-24: Open in Codespaces](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/try/devcontainer.json&quickstart=1)

</div>

## :material-server: Run the server

The same server, three ways to run its services.

<div class="grid cards" markdown>

-   :simple-docker:{ .lg .middle .dp-teal } **Docker Compose**

    ---

    Recommended. One compose file starts every service, storage included.

    [:octicons-arrow-right-24: Docker Compose](docker.md)

-   :simple-kubernetes:{ .lg .middle .dp-blue } **Kubernetes**

    ---

    The official Helm chart, for production and scalable deployments.

    [:octicons-arrow-right-24: Kubernetes](kubernetes.md)

-   :simple-python:{ .lg .middle .dp-yellow } **Python package**

    ---

    `depictio local up` runs every service as a process, no containers.

    [:octicons-arrow-right-24: Python package](local.md)

</div>

## :material-cog-outline: Configure and connect

<div class="grid cards" markdown>

-   :material-console-line:{ .lg .middle .dp-teal } **CLI**

    ---

    Install the `depictio` command and point it at your server.

    [:octicons-arrow-right-24: CLI installation](cli.md)

-   :material-cog:{ .lg .middle .dp-blue } **Configuration**

    ---

    What to set for a first deployment, then each setting by topic.

    [:octicons-arrow-right-24: Configuration](configuration.md)

-   :material-format-list-bulleted:{ .lg .middle .dp-violet } **Environment reference**

    ---

    Every environment variable Depictio reads, with its default.

    [:octicons-arrow-right-24: Environment reference](env-reference.md)

-   :material-account-group:{ .lg .middle .dp-purple } **Authentication modes**

    ---

    Turn on accounts and login, or open dashboards to the public.

    [:octicons-arrow-right-24: Authentication modes](../usage/guides/authentication-modes.md)

-   :material-shield-key-outline:{ .lg .middle .dp-green } **Single sign-on**

    ---

    Sign in through any OpenID Connect provider, and mirror its groups.

    [:octicons-arrow-right-24: OpenID Connect](sso/index.md)

-   :material-swap-horizontal:{ .lg .middle .dp-orange } **Upgrade to v1.12.0**

    ---

    Coming from before v1.12.0? Copy the MinIO store to SeaweedFS.

    [:octicons-arrow-right-24: MinIO to SeaweedFS](upgrade/v1.12.0-seaweedfs.md)

</div>

First time? Run the quickstart, then install the [CLI](cli.md) to load your data.
