# Installation

Run a Depictio server, then install the CLI to load your data into it.

## Quickstart

No git clone, no configuration file.

1. Download

```
curl -LO https://raw.githubusercontent.com/depictio/depictio/stable/docker-compose.yaml
```

2. Start

```
docker compose up -d
```

Open Depictio

|     | Service      | URL                                               | Notes                               |
| --- | ------------ | ------------------------------------------------- | ----------------------------------- |
|     | **Depictio** | [localhost:5080](http://localhost:5080)           | Single-user mode, no login required |
|     | **API docs** | [localhost:8058/docs](http://localhost:8058/docs) | Interactive OpenAPI interface       |

- **Customise credentials**

  ______________________________________________________________________

  Copy `.env.example` to `.env` to change the S3 password.

  [Advanced configuration](https://depictio.github.io/depictio-docs/latest/installation/docker/#advanced-configuration)

- **Try in GitHub Codespaces**

  ______________________________________________________________________

  The Python package in a cloud workspace, with two example projects.

  [Open in Codespaces](https://codespaces.new/depictio/depictio?devcontainer_path=.devcontainer/try/devcontainer.json&quickstart=1)

## Run the server

The same server, three ways to run its services.

- **Docker Compose**

  ______________________________________________________________________

  Recommended. One compose file starts every service, storage included.

  [Docker Compose](https://depictio.github.io/depictio-docs/latest/installation/docker/index.md)

- **Kubernetes**

  ______________________________________________________________________

  The official Helm chart, for production and scalable deployments.

  [Kubernetes](https://depictio.github.io/depictio-docs/latest/installation/kubernetes/index.md)

- **Python package**

  ______________________________________________________________________

  `depictio local up` runs every service as a process, no containers.

  [Python package](https://depictio.github.io/depictio-docs/latest/installation/local/index.md)

## Configure and connect

- **CLI**

  ______________________________________________________________________

  Install the `depictio` command and point it at your server.

  [CLI installation](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md)

- **Configuration**

  ______________________________________________________________________

  What to set for a first deployment, then each setting by topic.

  [Configuration](https://depictio.github.io/depictio-docs/latest/installation/configuration/index.md)

- **Environment reference**

  ______________________________________________________________________

  Every environment variable Depictio reads, with its default.

  [Environment reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/index.md)

- **Authentication modes**

  ______________________________________________________________________

  Turn on accounts and login, or open dashboards to the public.

  [Authentication modes](https://depictio.github.io/depictio-docs/latest/usage/guides/authentication-modes/index.md)

- **Single sign-on**

  ______________________________________________________________________

  Sign in through any OpenID Connect provider, and mirror its groups.

  [OpenID Connect](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md)

- **Upgrade to v1.12.0**

  ______________________________________________________________________

  Coming from before v1.12.0? Copy the MinIO store to SeaweedFS.

  [MinIO to SeaweedFS](https://depictio.github.io/depictio-docs/latest/installation/upgrade/v1.12.0-seaweedfs/index.md)

First time? Run the quickstart, then install the [CLI](https://depictio.github.io/depictio-docs/latest/installation/cli/index.md) to load your data.
