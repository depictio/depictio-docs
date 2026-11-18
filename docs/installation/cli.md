---
title: Install and configure the CLI
description: Install the depictio command and point it at a server.
---

# Install and configure the CLI

The `depictio` command ingests pipeline results and manages projects, dashboards and backups on a Depictio server. It needs Python 3.11 or later. No server yet? [`depictio local up`](local.md) starts one on your machine.

## Install { #install-via-pip }

=== "pip"

    ```bash
    pip install "depictio[multiqc]"
    ```

=== "uv"

    ```bash
    uv tool install "depictio[multiqc]"
    ```

=== "From source"

    ```bash
    git clone https://github.com/depictio/depictio.git && cd depictio
    pip install -e ".[multiqc]"
    ```

| Extra | Adds |
| --- | --- |
| none | The `depictio` command |
| `multiqc` | MultiQC report parsing, used by the nf-core templates |
| `watch` | File events for [`depictio watch`](../depictio-cli/usage.md#watch-command); without it, it polls |
| `builder` | The [Project Builder](../depictio-cli/usage.md#project-builder) |
| `local` | The server [`depictio local up`](local.md) runs |

Check it with `depictio --version`. `depictio` alone prints a quick start, `depictio --help` the commands.

!!! info "`depictio-cli`, the former name"
    Up to v1.11 the CLI was the `depictio-cli` package. Both packages now install both commands, `depictio` and `depictio-cli`, so old scripts and Nextflow hooks keep working. Never `pip uninstall depictio-cli` alone: it removes files `depictio` needs (`pip install --force-reinstall --no-deps depictio` repairs it). With both as `uv tool`s, reinstall with `--force` or `uv tool uninstall depictio-cli` first.

## Configure

The CLI reaches a server through a configuration file, `~/.depictio/CLI.yaml`:

1. In the web UI, open **Account settings** → **CLI agents** → **Add configuration** ([screenshots](../usage/get_started.md#create-a-cli-configuration)).
2. Download or copy the file to `~/.depictio/CLI.yaml`. It holds a token that signs in as you: keep it private.
3. Check it:

    ```bash
    depictio config check
    ```

The file holds `api_base_url`, `user` with its `token`, `s3_storage`, and optionally `instance_label` (the name shown in monitoring) and `remote_storage_options` (credentials to read `s3://` sources). Other files are named with `--server FILE`; `--server local` reaches the local server. See [Which server a command uses](../depictio-cli/usage.md#choosing-a-server).

## Run it from a container { #container-image }

```bash
docker run --rm --network host \
  -v /path/to/results:/path/to/results \
  -v "$HOME/.depictio:$HOME/.depictio:ro" \
  ghcr.io/depictio/depictio-cli:<version> \
  ingest /path/to/results --server "$HOME/.depictio/CLI.yaml"
```

For a CI runner or head node with Docker but no Python. The image carries the MultiQC extra; its entrypoint is `depictio-cli`. Mount each path at the same path inside, since paths are recorded as given. The container runs as UID 1000 with its own home, so name the file with `--server` and make it readable. `-e DEPICTIO_CLI_TOKEN` overrides its token.

## Troubleshooting

Every command first prints a `Server:` line naming the server and the file it read. `depictio config check` tests the server and its S3 storage.

| Symptom | Check |
| --- | --- |
| Connection error | The server runs, and `api_base_url` is right |
| Authentication error | The token is valid; generate a new configuration if needed |
| S3 error | The storage runs and its credentials are right. The server creates a missing bucket at startup |

Next: [Common tasks](../depictio-cli/tasks.md).
