# CLI Installation

This guide will walk you through installing and configuring the Depictio CLI tool, which is used for data ingestion and management.

## Overview

The Depictio CLI is a command-line tool that allows you to:

- Scan and process data files
- Upload data to the Depictio platform
- Manage projects and workflows
- Configure data collections

## Prerequisites

Before installing the CLI, ensure you have:

- Python 3.11 or higher
- pip, or [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Access to a running Depictio instance

!!! tip "No instance to connect to?"
    `depictio local up` starts one on your machine, without Docker, and the CLI uses it by default when no other server is configured. See [Python package installation](local.md).

## Installation Methods

### Install via pip

The CLI is the [`depictio`](https://pypi.org/project/depictio/) package on PyPI. Install it with plain pip or with your preferred package manager like `uv`:

```bash
pip install depictio
```

| Install | Gives |
| ------- | ----- |
| `pip install depictio` | The CLI: the `depictio` command |
| `pip install "depictio[multiqc]"` | The CLI, plus MultiQC report parsing, which the nf-core templates use |
| `pip install "depictio[local]"` | The CLI, plus the server that [`depictio local up`](local.md) runs on your machine |

If you prefer using `uv`, `uv tool install` puts the `depictio` command on your `PATH`, in an environment of its own:

```bash
uv tool install "depictio[multiqc]"
```

!!! info "`depictio-cli` is the former name"
    Up to v1.11, the CLI was the `depictio-cli` package and command. Both are kept
    as aliases: `pip install depictio-cli` installs `depictio` at the same
    version, and either package gives both the `depictio` and the `depictio-cli`
    commands, so existing scripts and Nextflow hooks keep working.

    - Do not run `pip uninstall depictio-cli` on its own: it removes files that
      `depictio` needs. `pip install --force-reinstall --no-deps depictio`
      repairs it.
    - With `depictio-cli` and `depictio` installed as two separate `uv tool`s,
      the next install fails with *Executable already exists*, since both now
      provide the same commands. Pass `--force`, or run
      `uv tool uninstall depictio-cli` first.

### Install from Source

You can also install the CLI directly from the source code:

```bash
git clone https://github.com/depictio/depictio.git
cd depictio
python -m venv depictio-env
source depictio-env/bin/activate
pip install -e ".[multiqc]"
```

This will install the CLI in development mode, allowing you to modify the code if needed.

### Run it from a container <small>(v1.10.0+)</small> { #container-image }

The CLI is also published to GHCR, built alongside the other Depictio images and
tagged with the same versions. Use it on a CI runner or a head node that has
Docker but where you cannot install a Python environment:

```bash
docker run --rm \
  -v /path/to/results:/path/to/results \
  -v "$HOME/.depictio:$HOME/.depictio:ro" \
  --network host \
  ghcr.io/depictio/depictio-cli:1.12.0 \
  ingest /path/to/results \
  --server "$HOME/.depictio/CLI.yaml" \
  --template nf-core/ampliseq/2.16.0
```

Mount each host path at the same path inside the container, because the paths you
pass are recorded in the project as given. The container has its own home, so
name your config with `--server`, and it runs as UID 1000, so that file
must be readable by that user. `-e DEPICTIO_CLI_TOKEN` overrides the token in the
file; it does not replace the file. The image carries the MultiQC extra and the
bundled templates. Its entrypoint is `depictio-cli`, the former name of
`depictio`, so the arguments start with the command, here `ingest`.

## Verifying the Installation

After installation, verify that the CLI is working correctly:

```bash
depictio --version
depictio --help
```

`depictio --help` lists the commands, grouped by purpose. `depictio` with no command prints a quick start instead.

## Configuration

Before using the CLI, you need to configure it to connect to your Depictio instance.

You need to have access to the Depictio web interface in order to generate a configuration file:

1. Log in to the Depictio web interface
2. Navigate to your user profile
3. Click on "Generate CLI Config"
4. Copy the generated YAML configuration into your clipboard using the "Copy to clipboard" icon button
5. Place the configuration file in the following location:
    - `~/.depictio/CLI.yaml` (recommended, default location)

### Which server a command uses <small>(v1.12.0+)</small>

Every command takes `--server`: `local` for the server `depictio local up` runs, or the path to a CLI configuration file. Without it, a command uses, in this order:

1. the file that `$DEPICTIO_CLI_CONFIG_PATH` names;
2. else `~/.depictio/CLI.yaml`, when that file exists;
3. else the local server.

So a configuration saved as `~/.depictio/CLI.yaml` needs no option, and a machine without one reaches its local server. The rule depends on files and variables only, never on whether a local server is running. When `DEPICTIO_CLI_TOKEN` or `DEPICTIO_CLI_API_BASE_URL` is set, there is no fallback to the local server. `--server` replaces the former `--CLI-config-path`, which still works. See [Which server a command uses](../depictio-cli/usage.md#choosing-a-server) for the details.

## Troubleshooting

### Common Issues

#### Connection Errors

If you see connection errors:

1. Check the `Server:` line the command prints first: it names the server and the configuration file it came from
2. Verify that your Depictio instance is running
3. Check that the API URL in your configuration is correct
4. Ensure your token is valid and has not expired

#### Authentication Issues

If you see authentication errors:

1. Check that your token is correct
2. Verify that your user account has the necessary permissions
3. Generate a new token if needed

#### S3 Storage Issues

If you have issues with S3 storage:

1. Verify that the S3 storage is running
2. Check that your S3 credentials are correct
3. Ensure the bucket is reachable with those credentials. From v1.6.0 the server creates it at startup if it is missing, so a bucket that is still absent points at the credentials or the endpoint rather than at provisioning

`depictio config check` runs both checks, the server and its storage, against the server the command reaches.

## Next Steps

Now that you have installed and configured the CLI, you can:

- [Learn how to use the CLI](../depictio-cli/usage.md)
- [Understand the YAML configuration](../usage/projects/reference.md)
- [Get started with Depictio](../usage/get_started.md)
