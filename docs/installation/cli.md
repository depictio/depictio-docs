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
- pip (Python package manager)
- Access to a running Depictio instance

## Installation Methods

!!! note "Note about the installation"
Pypi is not available yet, so you can only install the CLI from source.

### Install from Source

You can also install the CLI directly from the source code:

```bash
git clone https://github.com/depictio/depictio.git
cd depictio/cli
python -m venv depictio-cli-env
source depictio-cli-env/bin/activate
pip install -e .
```

This will install the CLI in development mode, allowing you to modify the code if needed.

## Verifying the Installation

After installation, verify that the CLI is working correctly:

```bash
depictio-cli --help
```

This should display the help message with available commands and options.

## Configuration

Before using the CLI, you need to configure it to connect to your Depictio instance.

You need to have access to the Depictio web interface in order to generate a configuration file:

1. Log in to the Depictio web interface
2. Navigate to your user profile
3. Click on "Generate CLI Config"
4. Copy the generated YAML configuration into your clipboard using the "Copy to clipboard" icon button
5. Place the configuration file in the following location:
   - `~/.depictio/config.yaml` (recommended)

## Troubleshooting

### Common Issues

#### Connection Errors

If you see connection errors:

1. Verify that your Depictio instance is running
2. Check that the API URL in your configuration is correct
3. Ensure your token is valid and has not expired

#### Authentication Issues

If you see authentication errors:

1. Check that your token is correct
2. Verify that your user account has the necessary permissions
3. Generate a new token if needed

#### S3 Storage Issues

If you have issues with S3 storage:

1. Verify that MinIO is running
2. Check that your S3 credentials are correct
3. Ensure the bucket exists and is accessible

## Next Steps

Now that you have installed and configured the CLI, you can:

- [Learn how to use the CLI](../depictio-cli/usage.md)
- [Understand the YAML configuration](../depictio-cli/full_reference_config.md)
- [Get started with Depictio](../usage/get_started.md)
