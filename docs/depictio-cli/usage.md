# Depictio CLI Usage

!!! note
The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register projects information including workflow files metadata. The depictio-cli is currently in development and is not yet ready for production use.

## Installation

See the [installation guide](../installation/cli.md) for instructions on how to install the depictio-cli.

## YAML Project Configuration

<!-- markdownlint-disable MD059 -->

Minimal reference configuration example can be found [here](minimal_config.md). Full reference configuration example can be found [here](full_reference_config.md).

## Command Line Interface

The depictio-cli provides a set of commands organized into different groups. Each command has specific options and parameters. You can always use the `--help` flag with any command to see its usage information.

```bash
depictio-cli --help
```

### Global Options

These options can be used with any command:

- `--verbose`, `-v`: Enable verbose logging
- `--verbose-level`, `-vl`: Set verbose logging level (default: "INFO")

### Config Commands

The `config` command group provides functionality for managing Depictio configurations.

#### show-cli-config

Shows the current Depictio CLI configuration.

```bash
depictio-cli config show-cli-config [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")

**Example:**

```bash
depictio-cli config show-cli-config
```

#### check-s3-storage

Checks the S3 storage configuration provided in the CLI configuration file.

```bash
depictio-cli config check-s3-storage [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")

**Example:**

```bash
depictio-cli config check-s3-storage
```

#### check-server-accessibility

Checks if the Depictio server is accessible.

```bash
depictio-cli config check-server-accessibility [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")

**Example:**

```bash
depictio-cli config check-server-accessibility
```

#### show-depictio-project-metadata-on-server

Shows Depictio metadata for registered Depictio projects.

```bash
depictio-cli config show-depictio-project-metadata-on-server [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")
- `--project-name`: Name of the project (default: "")

**Example:**

```bash
depictio-cli config show-depictio-project-metadata-on-server --project-name my-project
```

#### validate-project-config

Validates the Depictio Project configuration.

```bash
depictio-cli config validate-project-config [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")
- `--project-config-path`: Path to the pipeline configuration file (default: "")

**Example:**

```bash
depictio-cli config validate-project-config --project-config-path ./my-project-config.yaml
```

#### sync-project-config-to-server

Syncs the Depictio project configuration to the server.

```bash
depictio-cli config sync-project-config-to-server [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the configuration file (default: "~/.depictio/CLI.yaml")
- `--project-config-path`: Path to the pipeline configuration file (default: "")
- `--update`: Update the project configuration on the server (default: False)

**Example:**

```bash
depictio-cli config sync-project-config-to-server --project-config-path ./my-project-config.yaml --update
```

### Data Commands

The `data` command group provides functionality for managing data in Depictio.

#### scan

Scans files for a project.

```bash
depictio-cli data scan [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the CLI configuration file (default: "~/.depictio/CLI.yaml")
- `--project-config-path`: Path to the pipeline configuration file (default: "")
- `--workflow-name`: Name of the workflow to be scanned (optional)
- `--data-collection-tag`: Data collection tag to be scanned (optional)
- `--rescan-folders`: Reprocess all runs for the data collection (default: False)
- `--sync-files`: Update files for the data collection (default: False)

**Example:**

```bash
depictio-cli data scan --project-config-path ./my-project-config.yaml --workflow-name my-workflow
```

#### process

Processes data collections for a specific tag.

```bash
depictio-cli data process [OPTIONS]
```

**Options:**

- `--CLI-config-path`: Path to the CLI configuration file (default: "~/.depictio/CLI.yaml")
- `--project-config-path`: Path to the pipeline configuration file (default: "")
- `--overwrite`: Overwrite the workflow if it already exists (default: False)
<!-- - `--workflow-name`: Name of the workflow to be processed (optional)
- `--data-collection-tag`: Data collection tag to be processed (optional) -->

**Example:**

```bash
depictio-cli data process --project-config-path ./my-project-config.yaml --workflow-name my-workflow --data-collection-tag my-tag
```

## Common Workflows

### Prerequisites

- Ensure you have the Depictio server running and accessible.
- Ensure you have the CLI configuration file set up (default location: `~/.depictio/CLI.yaml`).
- Ensure you have a valid project configuration file (YAML format) ready for use.
- Ensure you have the necessary permissions to access the server and perform operations.

### Setting Up a New Project

1\. Create a project configuration file
2\. Validate the project configuration

```bash
depictio-cli config validate-project-config --project-config-path ./my-project-config.yaml
```

3\. Sync the project configuration to the server

```bash
depictio-cli config sync-project-config-to-server --project-config-path ./my-project-config.yaml
```

4\. Scan files for the project

```bash
depictio-cli data scan --project-config-path ./my-project-config.yaml
```

5\. Process the data

```bash
depictio-cli data process --project-config-path ./my-project-config.yaml
```

### Checking System Status

1\. Check the CLI configuration

```bash
depictio-cli config show-cli-config
```

2\. Check S3 storage configuration

```bash
depictio-cli config check-s3-storage
```

3\. Check server accessibility

```bash
depictio-cli config check-server-accessibility
```
