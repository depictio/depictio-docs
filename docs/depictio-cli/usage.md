# Depictio CLI Usage

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! note "Note about the CLI"
    The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register projects information including workflow files metadata. The depictio-cli is currently in development and is not yet ready for production use.
<!-- markdownlint-enable MD046 -->

## 📚 Table of Contents

- [Installation](#installation)
- [Quick Reference](#quick-reference)
- [Global Options](#global-options)
- [🚀 Commands](#-commands)
  - [📋 Config Commands](#-config-commands)
  - [📊 Data Commands](#-data-commands)
  - [💾 Backup Commands](#-backup-commands)
  - [🏃 Run Command](#-run-command)
- [🛠️ Common Use Cases](#️-common-use-cases)
- [🔧 Error Handling](#-error-handling)

## Installation

See the [installation guide](../installation/cli.md) for instructions on how to install the depictio-cli.

## Quick Reference

| Command | Description | Access Level |
|---------|-------------|--------------|
| `version` | Show CLI version | All users |
| `run` | Execute complete workflow | All users |
| `config show-cli-config` | Display CLI configuration | All users |
| `config check-s3-storage` | Validate S3 storage setup | All users |
| `config check-server-accessibility` | Test server connection | All users |
| `config validate-project-config` | Validate project configuration | All users |
| `config sync-project-config-to-server` | Sync project config to server | All users |
| `data scan` | Scan project files | All users |
| `data process` | Process data collections | All users |
| `backup backup` | Create system backup | **Admin only** |
| `backup restore` | Restore from backup | **Admin only** |
| `backup list-backups` | List available backups | **Admin only** |

## Global Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--verbose` | `-v` | `boolean` | `false` | Enable verbose logging |
| `--verbose-level` | `-vl` | `string` | `"INFO"` | Set verbose logging level |

## 🚀 Commands

### 🏃 Run Command

Execute the complete Depictio workflow: validate → sync → scan → process

```bash
depictio-cli run [OPTIONS]
```

**Quick Start:**

```bash
depictio-cli run --project-config-path ./config.yaml
```

**Pipeline Steps:**

  1. ✅ Check server accessibility
  2. ✅ Check S3 storage configuration
  3. ✅ Validate project configuration
  4. ✅ Sync project configuration to server
  5. ✅ Scan data files
  6. ✅ Process data collections

<!-- markdownlint-disable MD046 -->
??? info "📋 Basic Configuration"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
    | `--project-config-path` | `string` | `""` | Pipeline configuration file path |
    | `--workflow-name` | `string` | `null` | Specific workflow to process |
    | `--data-collection-tag` | `string` | `null` | Data collection tag to process |
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? info "⚙️ Flow Control Options"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--skip-server-check` | `boolean` | `false` | Skip server accessibility check |
    | `--skip-s3-check` | `boolean` | `false` | Skip S3 storage validation |
    | `--skip-sync` | `boolean` | `false` | Skip config sync to server |
    | `--skip-scan` | `boolean` | `false` | Skip data scanning step |
    | `--skip-process` | `boolean` | `false` | Skip data processing step |
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? info "🔄 Sync & Scan Options"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--update-config` | `boolean` | `false` | Update project configuration on server |
    | `--rescan-folders` | `boolean` | `false` | Reprocess all runs for data collection |
    | `--sync-files` | `boolean` | `false` | Update files for data collection |
    | `--overwrite` | `boolean` | `false` | Overwrite workflow if it already exists |
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
??? info "🖥️ Output & Control"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--rich-tables` | `boolean` | `false` | Show detailed execution summary |
    | `--continue-on-error` | `boolean` | `false` | Continue execution on step failure |
    | `--dry-run` | `boolean` | `false` | Show execution plan without running |
<!-- markdownlint-enable MD046 -->

**Examples:**

=== "Basic Usage"

```bash
# Complete workflow execution
depictio-cli run --project-config-path ./config.yaml
```

=== "Development"

```bash
# With detailed output and error handling
depictio-cli run \
  --project-config-path ./config.yaml \
  --continue-on-error \
  --rich-tables
```

=== "Dry Run"

```bash
# Preview execution without running
depictio-cli run \
  --project-config-path ./config.yaml \
  --dry-run
```

=== "Skip Steps"

```bash
# Skip server checks for faster execution
depictio-cli run \
  --project-config-path ./config.yaml \
  --skip-server-check \
  --skip-s3-check
```

### 📋 Config Commands

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! info "Command Group: `depictio-cli config`"
    All commands in this section are part of the `config` command family. Use them to manage Depictio configurations and validate connections.
<!-- markdownlint-enable MD046 -->

Manage Depictio configurations and validate connections.

#### `config show-cli-config`

Display the current CLI configuration.

```bash
depictio-cli config show-cli-config [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |

```bash
depictio-cli config show-cli-config
```

---

#### `config check-s3-storage`

Validate S3 storage configuration.

```bash
depictio-cli config check-s3-storage [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |

```bash
depictio-cli config check-s3-storage
```

---

#### `config check-server-accessibility`

Test connection to Depictio server.

```bash
depictio-cli config check-server-accessibility [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |

```bash
depictio-cli config check-server-accessibility
```

---

#### `config show-depictio-project-metadata-on-server`

Display metadata for registered projects.

```bash
depictio-cli config show-depictio-project-metadata-on-server [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-name` | `string` | `""` | Specific project name |

```bash
depictio-cli config show-depictio-project-metadata-on-server --project-name my-project
```

---

#### `config validate-project-config`

Validate project configuration file.

```bash
depictio-cli config validate-project-config [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-config-path` | `string` | `""` | Pipeline configuration file path |

```bash
depictio-cli config validate-project-config --project-config-path ./config.yaml
```

---

#### `config sync-project-config-to-server`

Sync project configuration to server.

```bash
depictio-cli config sync-project-config-to-server [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-config-path` | `string` | `""` | Pipeline configuration file path |
| `--update` | `boolean` | `false` | Update existing project configuration |

```bash
depictio-cli config sync-project-config-to-server --project-config-path ./config.yaml --update
```

### 📊 Data Commands

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! info "Command Group: `depictio-cli data`"
    All commands in this section are part of the `data` command family. Use them to manage data scanning and processing operations.
<!-- markdownlint-enable MD046 -->

Manage data scanning and processing operations.

#### `data scan`

Scan project files for data collections.

```bash
depictio-cli data scan [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-config-path` | `string` | `""` | Pipeline configuration file path |
| `--workflow-name` | `string` | `null` | Specific workflow to scan |
| `--data-collection-tag` | `string` | `null` | Data collection tag to scan |
| `--rescan-folders` | `boolean` | `false` | Reprocess all runs for data collection |
| `--sync-files` | `boolean` | `false` | Update files for data collection |

```bash
depictio-cli data scan --project-config-path ./config.yaml --workflow-name my-workflow
```

---

#### `data process`

Process data collections for workflow execution.

```bash
depictio-cli data process [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-config-path` | `string` | `""` | Pipeline configuration file path |
| `--overwrite` | `boolean` | `false` | Overwrite existing workflow |

```bash
depictio-cli data process --project-config-path ./config.yaml --overwrite
```

### 💾 Backup Commands

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! info "Command Group: `depictio-cli backup`"
    All commands in this section are part of the `backup` command family. Use them to backup and restore system data and configurations.
<!-- markdownlint-enable MD046 -->

Backup and restore system data and configurations.

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! warning "Admin Access Required"
    Backup and restore commands require administrator privileges. Only users with admin access can perform backup and restore operations. Ensure your CLI configuration includes admin credentials.
<!-- markdownlint-enable MD046 -->

#### `backup backup`

Create a backup of database and S3 storage data.

```bash
depictio-cli backup backup [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--backup-name` | `string` | `timestamp` | Name for the backup |
| `--include-s3` | `boolean` | `true` | Include S3 storage data in backup |
| `--include-db` | `boolean` | `true` | Include database data in backup |
| `--output-path` | `string` | `./backups` | Path where backup files are stored |

```bash
depictio-cli backup backup --backup-name production-backup --output-path ./backups
```

---

#### `backup restore`

Restore data from a previously created backup.

```bash
depictio-cli backup restore [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--backup-path` | `string` | **required** | Path to backup file or directory |
| `--restore-s3` | `boolean` | `true` | Restore S3 storage data |
| `--restore-db` | `boolean` | `true` | Restore database data |
| `--force` | `boolean` | `false` | Force restore without confirmation |

```bash
depictio-cli backup restore --backup-path ./backups/production-backup --force
```

---

#### `backup list-backups`

List all available backups.

```bash
depictio-cli backup list-backups [OPTIONS]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--backup-path` | `string` | `./backups` | Path to backup directory |

```bash
depictio-cli backup list-backups --backup-path ./backups
```

## 🛠️ Common Use Cases

### 🚀 Quick Start

=== "Complete Setup"

```bash
# 1. Validate your project configuration
depictio-cli config validate-project-config --project-config-path ./config.yaml

# 2. Run the complete workflow
depictio-cli run --project-config-path ./config.yaml
```

=== "Step by Step"

```bash
# 1. Check system status
depictio-cli config check-server-accessibility
depictio-cli config check-s3-storage

# 2. Validate and sync configuration
depictio-cli config validate-project-config --project-config-path ./config.yaml
depictio-cli config sync-project-config-to-server --project-config-path ./config.yaml

# 3. Scan and process data
depictio-cli data scan --project-config-path ./config.yaml
depictio-cli data process --project-config-path ./config.yaml
```

### 🔧 Development Workflow

=== "Testing Changes"

```bash
# Preview changes without execution
depictio-cli run --project-config-path ./config.yaml --dry-run

# Test with specific workflow
depictio-cli run --project-config-path ./config.yaml --workflow-name test-workflow
```

=== "Debugging"

```bash
# Enable verbose logging
depictio-cli run --project-config-path ./config.yaml --verbose --continue-on-error

# Skip problematic steps
depictio-cli run --project-config-path ./config.yaml --skip-server-check --skip-s3-check
```

### 💾 Backup Operations

<!-- prettier-ignore -->
<!-- markdownlint-disable MD046 -->
!!! warning "Admin Access Required"
    All backup operations require administrator privileges.
<!-- markdownlint-enable MD046 -->

=== "Create Backup"

```bash
# Create timestamped backup
depictio-cli backup backup --backup-name "backup-$(date +%Y%m%d-%H%M%S)"

# Custom backup location
depictio-cli backup backup --backup-name production-backup --output-path /secure/backups
```

=== "Restore Backup"

```bash
# List available backups
depictio-cli backup list-backups --backup-path /secure/backups

# Restore specific backup
depictio-cli backup restore --backup-path /secure/backups/production-backup --force
```

### 📊 Data Management

=== "Rescan Data"

```bash
# Rescan all folders
depictio-cli data scan --project-config-path ./config.yaml --rescan-folders

# Sync file updates
depictio-cli data scan --project-config-path ./config.yaml --sync-files
```

=== "Process Updates"

```bash
# Overwrite existing workflow
depictio-cli data process --project-config-path ./config.yaml --overwrite

# Update and reprocess
depictio-cli run --project-config-path ./config.yaml --update-config --overwrite
```

## 🔧 Error Handling

### Exit Codes

| Code | Description | Solution |
|------|-------------|----------|
| `0` | Success | Command completed successfully |
| `1` | Configuration error | Check configuration file paths and syntax |
| `2` | Server connection failed | Verify server URL and network connectivity |
| `3` | S3 storage error | Validate S3 credentials and bucket configuration |
| `4` | Data processing failed | Check data file permissions and formats |

### Common Issues

<!-- markdownlint-disable MD046 -->
=== "Connection Problems"

    **Error:** "Server not accessible"

    **Solutions:**
    ```bash
    # Check server accessibility
    depictio-cli config check-server-accessibility

    # Verify CLI configuration
    depictio-cli config show-cli-config
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
=== "Configuration Errors"

    **Error:** "Project config validation failed"

    **Solutions:**
    ```bash
    # Validate configuration with verbose output
    depictio-cli config validate-project-config --project-config-path ./config.yaml --verbose

    # Check configuration examples
    # See: minimal_config.md and full_reference_config.md
    ```
<!-- markdownlint-enable MD046 -->

<!-- markdownlint-disable MD046 -->
=== "Permission Issues"

    **Error:** "Admin access required"

    **Solutions:**
    - Ensure you're logged in with admin credentials
    - Check CLI configuration includes admin access tokens
    - Contact system administrator for proper permissions
<!-- markdownlint-enable MD046 -->

### Troubleshooting Steps

**1. Check Prerequisites:**

- Depictio server is running and accessible
- CLI configuration file exists (`~/.depictio/CLI.yaml`)
- Project configuration file is valid YAML
- Proper permissions for file access

**2. Enable Verbose Logging:**

   ```bash
   depictio-cli [command] --verbose --verbose-level DEBUG
   ```

**3. Test Components Individually:**

```bash
depictio-cli config check-server-accessibility
depictio-cli config check-s3-storage
depictio-cli config validate-project-config --project-config-path ./config.yaml
```

**4. Use Dry Run Mode:**

```bash
depictio-cli run --project-config-path ./config.yaml --dry-run
```

## 📖 Configuration References

- [Minimal YAML Configuration](minimal_config.md)
- [Full Reference Configuration](full_reference_config.md)
