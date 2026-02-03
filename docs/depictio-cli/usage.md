# Depictio CLI Usage

<!-- prettier-ignore -->
!!! note "Note about the CLI"
    The depictio-cli is a command line interface that allows you to interact with the Depictio backend. It is used to register projects information including workflow files metadata. The depictio-cli is currently in development and is not yet ready for production use.

## 📚 Table of Contents

- [Installation](#installation)
- [Quick Reference](#quick-reference)
- [Global Options](#global-options)
- [🚀 Commands](#-commands)
  - [🏃 Run Command](#run-command)
  - [📋 Config Commands](#config-commands)
  - [📊 Data Commands](#data-commands)
  - [💾 Backup Commands](#backup-commands)
  - [📈 Dashboard Commands](#dashboard-commands)
- [🛠️ Common Use Cases](#common-use-cases)
- [🔧 Error Handling](#error-handling)

## Installation

See the [installation guide](../installation/cli.md) for instructions on how to install the depictio-cli.

## Quick Reference

| Command                                | Description                             | Access Level   |
| -------------------------------------- | --------------------------------------- | -------------- |
| `version`                              | Show CLI version                        | All users      |
| `run`                                  | Execute complete workflow               | All users      |
| `config show-cli-config`               | Display CLI configuration               | All users      |
| `config check-s3-storage`              | Validate S3 storage setup               | All users      |
| `config check-server-accessibility`    | Test server connection                  | All users      |
| `config validate-project-config`       | Validate project configuration          | All users      |
| `config sync-project-config-to-server` | Sync project config to server           | All users      |
| `data scan`                            | Scan project files                      | All users      |
| `data process`                         | Process data collections                | All users      |
| `data join`                            | Execute pre-computed table joins        | All users      |
| `data link list`                       | List DC links for a project             | All users      |
| `data link create`                     | Create a DC link for cross-DC filtering | All users      |
| `data link resolve`                    | Test link resolution                    | All users      |
| `data link delete`                     | Delete a DC link                        | All users      |
| `dashboard validate`                   | Validate dashboard YAML file locally    | All users      |
| `dashboard import`                     | Import dashboard YAML to server         | All users      |
| `dashboard export`                     | Export dashboard to YAML file           | All users      |
| `backup backup`                        | Create system backup                    | **Admin only** |
| `backup restore`                       | Restore from backup                     | **Admin only** |
| `backup list-backups`                  | List available backups                  | **Admin only** |

## Global Options

| Option            | Short | Type      | Default  | Description               |
| ----------------- | ----- | --------- | -------- | ------------------------- |
| `--verbose`       | `-v`  | `boolean` | `false`  | Enable verbose logging    |
| `--verbose-level` | `-vl` | `string`  | `"INFO"` | Set verbose logging level |

## 🚀 Commands

### 🏃 Run Command

<script src="https://asciinema.org/a/R5V6UXLetWzfp7AB39SxoGfhd.js" id="asciicast-R5V6UXLetWzfp7AB39SxoGfhd" async="true"></script>
<p style="text-align: center; margin-top: 0.5rem; font-style: italic; color: #666;">🎬 <strong>🖥️ `depictio-cli run` command example</strong></p>

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

??? info "📋 Basic Configuration"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
    | `--project-config-path` | `string` | `""` | Pipeline configuration file path |
    | `--workflow-name` | `string` | `null` | Specific workflow to process |
    | `--data-collection-tag` | `string` | `null` | Data collection tag to process |

??? info "⚙️ Flow Control Options"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--skip-server-check` | `boolean` | `false` | Skip server accessibility check |
    | `--skip-s3-check` | `boolean` | `false` | Skip S3 storage validation |
    | `--skip-sync` | `boolean` | `false` | Skip config sync to server |
    | `--skip-scan` | `boolean` | `false` | Skip data scanning step |
    | `--skip-process` | `boolean` | `false` | Skip data processing step |

??? info "🔄 Sync & Scan Options"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--update-config` | `boolean` | `false` | Update project configuration on server |
    | `--rescan-folders` | `boolean` | `false` | Reprocess all runs for data collection |
    | `--sync-files` | `boolean` | `false` | Update files for data collection |
    | `--overwrite` | `boolean` | `false` | Overwrite workflow if it already exists |

??? info "🖥️ Output & Control"

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--rich-tables` | `boolean` | `false` | Show detailed execution summary |
    | `--continue-on-error` | `boolean` | `false` | Continue execution on step failure |
    | `--dry-run` | `boolean` | `false` | Show execution plan without running |

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
!!! info "Command Group: `depictio-cli config`"
    All commands in this section are part of the `config` command family. Use them to manage Depictio configurations and validate connections.

Manage Depictio configurations and validate connections.

#### `config show-cli-config`

Display the current CLI configuration.

```bash
depictio-cli config show-cli-config [OPTIONS]
```

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
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

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
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

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
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

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |
| `--project-name`    | `string` | `""`                   | Specific project name       |

```bash
depictio-cli config show-depictio-project-metadata-on-server --project-name my-project
```

---

#### `config validate-project-config`

Validate project configuration file.

```bash
depictio-cli config validate-project-config [OPTIONS]
```

| Parameter               | Type     | Default                | Description                      |
| ----------------------- | -------- | ---------------------- | -------------------------------- |
| `--CLI-config-path`     | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path      |
| `--project-config-path` | `string` | `""`                   | Pipeline configuration file path |

```bash
depictio-cli config validate-project-config --project-config-path ./config.yaml
```

---

#### `config sync-project-config-to-server`

Sync project configuration to server.

```bash
depictio-cli config sync-project-config-to-server [OPTIONS]
```

| Parameter               | Type      | Default                | Description                           |
| ----------------------- | --------- | ---------------------- | ------------------------------------- |
| `--CLI-config-path`     | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path           |
| `--project-config-path` | `string`  | `""`                   | Pipeline configuration file path      |
| `--update`              | `boolean` | `false`                | Update existing project configuration |

```bash
depictio-cli config sync-project-config-to-server --project-config-path ./config.yaml --update
```

### 📊 Data Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio-cli data`"
    All commands in this section are part of the `data` command family. Use them to manage data scanning and processing operations.

Manage data scanning and processing operations.

#### `data scan`

Scan project files for data collections.

```bash
depictio-cli data scan [OPTIONS]
```

| Parameter               | Type      | Default                | Description                            |
| ----------------------- | --------- | ---------------------- | -------------------------------------- |
| `--CLI-config-path`     | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path            |
| `--project-config-path` | `string`  | `""`                   | Pipeline configuration file path       |
| `--workflow-name`       | `string`  | `null`                 | Specific workflow to scan              |
| `--data-collection-tag` | `string`  | `null`                 | Data collection tag to scan            |
| `--rescan-folders`      | `boolean` | `false`                | Reprocess all runs for data collection |
| `--sync-files`          | `boolean` | `false`                | Update files for data collection       |

```bash
depictio-cli data scan --project-config-path ./config.yaml --workflow-name my-workflow
```

---

#### `data process`

Process data collections for workflow execution.

```bash
depictio-cli data process [OPTIONS]
```

| Parameter               | Type      | Default                | Description                      |
| ----------------------- | --------- | ---------------------- | -------------------------------- |
| `--CLI-config-path`     | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path      |
| `--project-config-path` | `string`  | `""`                   | Pipeline configuration file path |
| `--overwrite`           | `boolean` | `false`                | Overwrite existing workflow      |

```bash
depictio-cli data process --project-config-path ./config.yaml --overwrite
```

---

#### `data join`

Execute pre-computed table joins defined in project configuration.

<!-- prettier-ignore -->
!!! note "Links vs Joins"
    For interactive cross-DC filtering, use **links** (configured in YAML, resolved at runtime). Use **joins** only when you need a pre-computed combined dataset stored as a Delta table. See [Cross-DC Filtering](../features/cross-dc-filtering.md).

```bash
depictio-cli data join [OPTIONS]
```

| Parameter               | Type      | Default                | Description                                     |
| ----------------------- | --------- | ---------------------- | ----------------------------------------------- |
| `--CLI-config-path`     | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path                     |
| `--project-config-path` | `string`  | `""`                   | Pipeline configuration file path                |
| `--join-name`           | `string`  | `null`                 | Specific join to process (all if not specified) |
| `--preview`             | `boolean` | `false`                | Preview join results without persisting         |
| `--overwrite`           | `boolean` | `false`                | Overwrite existing joined tables                |

```bash
# Preview all joins
depictio-cli data join --project-config-path ./config.yaml --preview

# Execute a specific join
depictio-cli data join --project-config-path ./config.yaml --join-name my_join
```
<!-- 
---

#### `data link`

Manage DC links for cross-DC interactive filtering. Links enable runtime filtering between data collections without pre-computing joined tables.

<!-- prettier-ignore -->
!!! tip "Links vs Joins"
    **Links** are the preferred method for cross-DC filtering. They resolve at runtime and support any DC type (tables, MultiQC, etc.). **Joins** create pre-computed Delta tables and only work between table DCs.

<!-- ##### `data link list`

List all DC links for a project.

```bash
depictio-cli data link list [OPTIONS]
```

| Parameter               | Type     | Default                | Description                      |
| ----------------------- | -------- | ---------------------- | -------------------------------- |
| `--CLI-config-path`     | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path      |
| `--project-config-path` | `string` | `""`                   | Pipeline configuration file path |
| `--target-dc`           | `string` | `null`                 | Filter links by target DC ID     |
| `--source-dc`           | `string` | `null`                 | Filter links by source DC ID     |

```bash
# List all links in a project
depictio-cli data link list --project-config-path ./config.yaml

# List links targeting a specific DC
depictio-cli data link list --project-config-path ./config.yaml --target-dc multiqc_dc_id
```

---

##### `data link create`

Create a new DC link for cross-DC filtering.

```bash
depictio-cli data link create [OPTIONS]
```

| Parameter               | Type     | Default                | Description                         |
| ----------------------- | -------- | ---------------------- | ----------------------------------- |
| `--CLI-config-path`     | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path         |
| `--project-config-path` | `string` | `""`                   | Pipeline configuration file path    |
| `--source-dc`           | `string` | **required**           | Source data collection ID           |
| `--source-column`       | `string` | **required**           | Column in source DC to link from    |
| `--target-dc`           | `string` | **required**           | Target data collection ID           |
| `--target-type`         | `string` | `table`                | Target DC type (`table`, `multiqc`) |
| `--resolver`            | `string` | `direct`               | Resolver type (see below)           |
| `--description`         | `string` | `null`                 | Optional description for the link   |

**Resolver Types:**

| Resolver         | Use Case                | Description                                   |
| ---------------- | ----------------------- | --------------------------------------------- |
| `direct`         | Same value in both DCs  | 1:1 mapping (e.g., `sample_id` = `sample_id`) |
| `sample_mapping` | MultiQC sample variants | Canonical ID → MultiQC sample name variants   |
| `pattern`        | Template substitution   | e.g., `{sample}.bam` → `S1.bam`               |
| `regex`          | Pattern matching        | Match target values using regex               |
| `wildcard`       | Glob-style matching     | e.g., `S1*` matches `S1_R1.bam`               |

```bash
# Create a direct link between two table DCs
depictio-cli data link create \
    --project-config-path ./config.yaml \
    --source-dc metadata_table \
    --source-column sample_id \
    --target-dc variants_table \
    --target-type table \
    --resolver direct

# Create a sample_mapping link to a MultiQC DC
depictio-cli data link create \
    --project-config-path ./config.yaml \
    --source-dc metadata_table \
    --source-column sample_id \
    --target-dc multiqc_general_stats \
    --target-type multiqc \
    --resolver sample_mapping
```

---

##### `data link resolve`

Test link resolution by resolving filter values from source to target DC.

```bash
depictio-cli data link resolve [OPTIONS]
```

| Parameter               | Type     | Default                | Description                       |
| ----------------------- | -------- | ---------------------- | --------------------------------- |
| `--CLI-config-path`     | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path       |
| `--project-config-path` | `string` | `""`                   | Pipeline configuration file path  |
| `--source-dc`           | `string` | **required**           | Source data collection ID         |
| `--source-column`       | `string` | **required**           | Column in source DC to filter on  |
| `--target-dc`           | `string` | **required**           | Target data collection ID         |
| `--filter`              | `string` | **required**           | Comma-separated values to resolve |

```bash
# Resolve sample IDs to MultiQC sample names
depictio-cli data link resolve \
    --project-config-path ./config.yaml \
    --source-dc metadata_table \
    --source-column sample_id \
    --target-dc multiqc_general_stats \
    --filter "S1,S2,S3"
```

**Example output:**

```
Resolving link:
  Source DC: metadata_table
  Source Column: sample_id
  Target DC: multiqc_general_stats
  Filter Values: ['S1', 'S2', 'S3']

Resolution successful!
  Link ID: 507f1f77bcf86cd799439011
  Resolver Used: sample_mapping
  Target Type: multiqc
  Match Count: 6

Resolved Values (6):
    - S1_R1
    - S1_R2
    - S2_R1
    - S2_R2
    - S3_R1
    - S3_R2
```

---

##### `data link delete`

Delete a DC link.

```bash
depictio-cli data link delete [OPTIONS]
```

| Parameter               | Type      | Default                | Description                      |
| ----------------------- | --------- | ---------------------- | -------------------------------- |
| `--CLI-config-path`     | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path      |
| `--project-config-path` | `string`  | `""`                   | Pipeline configuration file path |
| `--link-id`             | `string`  | **required**           | ID of the link to delete         |
| `--force` / `-f`        | `boolean` | `false`                | Skip confirmation prompt         |

```bash
# Delete a link with confirmation
depictio-cli data link delete --project-config-path ./config.yaml --link-id abc123

# Delete without confirmation
depictio-cli data link delete --project-config-path ./config.yaml --link-id abc123 --force
``` --> -->

### 💾 Backup Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio-cli backup`"
    All commands in this section are part of the `backup` command family. Use them to backup and restore system data and configurations.

Backup and restore system data and configurations.

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    Backup and restore commands require administrator privileges. Only users with admin access can perform backup and restore operations. Ensure your CLI configuration includes admin credentials.

#### `backup backup`

Create a backup of database and S3 storage data.

```bash
depictio-cli backup backup [OPTIONS]
```

| Parameter           | Type      | Default                | Description                        |
| ------------------- | --------- | ---------------------- | ---------------------------------- |
| `--CLI-config-path` | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path        |
| `--backup-name`     | `string`  | `timestamp`            | Name for the backup                |
| `--include-s3`      | `boolean` | `true`                 | Include S3 storage data in backup  |
| `--include-db`      | `boolean` | `true`                 | Include database data in backup    |
| `--output-path`     | `string`  | `./backups`            | Path where backup files are stored |

```bash
depictio-cli backup backup --backup-name production-backup --output-path ./backups
```

---

#### `backup restore`

Restore data from a previously created backup.

```bash
depictio-cli backup restore [OPTIONS]
```

| Parameter           | Type      | Default                | Description                        |
| ------------------- | --------- | ---------------------- | ---------------------------------- |
| `--CLI-config-path` | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path        |
| `--backup-path`     | `string`  | **required**           | Path to backup file or directory   |
| `--restore-s3`      | `boolean` | `true`                 | Restore S3 storage data            |
| `--restore-db`      | `boolean` | `true`                 | Restore database data              |
| `--force`           | `boolean` | `false`                | Force restore without confirmation |

```bash
depictio-cli backup restore --backup-path ./backups/production-backup --force
```

---

#### `backup list-backups`

List all available backups.

```bash
depictio-cli backup list-backups [OPTIONS]
```

| Parameter       | Type     | Default     | Description              |
| --------------- | -------- | ----------- | ------------------------ |
| `--backup-path` | `string` | `./backups` | Path to backup directory |

```bash
depictio-cli backup list-backups --backup-path ./backups
```

### 📈 Dashboard Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio-cli dashboard`"
    All commands in this section are part of the `dashboard` command family. Use them to manage dashboard YAML files - validate, import to server, and export from server.

Manage dashboard YAML files for the [Dashboard YAML Management](../features/yaml-sync.md) feature.

| Command    | Description                  | Server Required          |
| ---------- | ---------------------------- | ------------------------ |
| `validate` | Validate YAML schema locally | No                       |
| `import`   | Import YAML to server        | Yes (unless `--dry-run`) |
| `export`   | Export dashboard to YAML     | Yes                      |

#### `dashboard validate`

Validate a single dashboard YAML file against the DashboardDataLite schema locally.

```bash
depictio-cli dashboard validate <yaml_file> [OPTIONS]
```

| Parameter          | Type      | Default      | Description                                        |
| ------------------ | --------- | ------------ | -------------------------------------------------- |
| `yaml_file`        | `path`    | **required** | Path to YAML dashboard file                        |
| `--verbose` / `-v` | `boolean` | `false`      | Show detailed validation output including warnings |

```bash
# Basic validation
depictio-cli dashboard validate my_dashboard.yaml

# With verbose output
depictio-cli dashboard validate my_dashboard.yaml --verbose
```

**Example Output (Success):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
<span style="color: #2e7d32;">✓ Validation passed</span>
  Errors: 0
  Warnings: 0
</pre>
</div>

**Example Output (Failure):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>

<span style="color: #c62828;">✗ Validation failed</span>
  Errors: 2

┌──────────────────────────────────────────────────────────────────┐
│                       Validation Errors                          │
├─────────────────────┬────────────────┬───────────────────────────┤
│ <span style="color: #0097a7;">Component</span>           │ <span style="color: #c2185b;">Field</span>          │ <span style="color: #c62828;">Message</span>                   │
├─────────────────────┼────────────────┼───────────────────────────┤
│ <span style="color: #0097a7;">-</span>                   │ <span style="color: #c2185b;">component_type</span> │ <span style="color: #c62828;">Invalid value 'graphs'</span>    │
│ <span style="color: #0097a7;">-</span>                   │ <span style="color: #c2185b;">workflow_tag</span>   │ <span style="color: #c62828;">Field required</span>            │
└─────────────────────┴────────────────┴───────────────────────────┘
</pre>
</div>

---

#### `dashboard import`

Import a dashboard YAML file to the server. The project is determined from the YAML `project_tag` field or the `--project` option.

```bash
depictio-cli dashboard import <yaml_file> [OPTIONS]
```

| Parameter          | Type      | Default      | Description                                           |
| ------------------ | --------- | ------------ | ----------------------------------------------------- |
| `yaml_file`        | `path`    | **required** | Path to YAML dashboard file                           |
| `--config` / `-c`  | `string`  | `null`       | Path to CLI config file (required unless `--dry-run`) |
| `--project` / `-p` | `string`  | `null`       | Project ID (overrides `project_tag` in YAML)          |
| `--overwrite`      | `boolean` | `false`      | Update existing dashboard with same title             |
| `--dry-run`        | `boolean` | `false`      | Validate only, don't import                           |
| `--api`            | `string`  | from config  | API base URL                                          |

```bash
# Validate locally without server (no config needed)
depictio-cli dashboard import dashboard.yaml --dry-run

# Import to server
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml

# Update existing dashboard with same title
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --overwrite

# Override project from YAML
depictio-cli dashboard import dashboard.yaml --config ~/.depictio/admin_config.yaml --project 646b0f3c1e4a2d7f8e5b8c9a
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);"><span style="color: #0097a7;">Validating:</span> <span style="color: #c2185b;">dashboard.yaml</span>
<span style="color: #2e7d32;">✓ Validation passed</span>
  Title: Iris Dashboard Demo
  Components: 7
  Project: Iris_Dataset_Project (from YAML project_tag)

<span style="color: #0097a7;">Loading CLI configuration...</span>
<span style="color: #2e7d32;">✓ Configuration loaded</span>
  API URL: http://localhost:8058

<span style="color: #0097a7;">Importing dashboard (project: Iris_Dataset_Project)...</span>
<span style="color: #2e7d32;">✓ Dashboard imported successfully!</span>
  Dashboard ID: 6824cb3b89d2b72169309737
  Title: Iris Dashboard Demo
  Project ID: 650a1b2c3d4e5f6a7b8c9d0e

<span style="color: #0097a7;">View at:</span> http://localhost:8058/dashboard/6824cb3b89d2b72169309737
</pre>
</div>

---

#### `dashboard export`

Export a dashboard from the server to a YAML file.

```bash
depictio-cli dashboard export <dashboard_id> [OPTIONS]
```

| Parameter         | Type     | Default          | Description             |
| ----------------- | -------- | ---------------- | ----------------------- |
| `dashboard_id`    | `string` | **required**     | Dashboard ID to export  |
| `--config` / `-c` | `string` | **required**     | Path to CLI config file |
| `--output` / `-o` | `path`   | `dashboard.yaml` | Output file path        |
| `--api`           | `string` | from config      | API base URL            |

```bash
# Export to default file
depictio-cli dashboard export 6824cb3b89d2b72169309737 --config ~/.depictio/admin_config.yaml

# Export to specific file
depictio-cli dashboard export 6824cb3b89d2b72169309737 --config ~/.depictio/admin_config.yaml -o iris_dashboard.yaml
```

**Example Output:**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);"><span style="color: #0097a7;">Loading CLI configuration...</span>
<span style="color: #0097a7;">Exporting dashboard 6824cb3b89d2b72169309737...</span>
<span style="color: #2e7d32;">✓ Dashboard exported to:</span> <span style="color: #c2185b;">iris_dashboard.yaml</span>
</pre>
</div>

---

For more information about dashboard YAML format and workflows, see [Dashboard YAML Management](../features/yaml-sync.md).

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
!!! warning "Admin Access Required"
    All backup operations require administrator privileges.

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

| Code | Description              | Solution                                         |
| ---- | ------------------------ | ------------------------------------------------ |
| `0`  | Success                  | Command completed successfully                   |
| `1`  | Configuration error      | Check configuration file paths and syntax        |
| `2`  | Server connection failed | Verify server URL and network connectivity       |
| `3`  | S3 storage error         | Validate S3 credentials and bucket configuration |
| `4`  | Data processing failed   | Check data file permissions and formats          |

### Common Issues

=== "Connection Problems"

    **Error:** "Server not accessible"

    **Solutions:**
    ```bash
    # Check server accessibility
    depictio-cli config check-server-accessibility

    # Verify CLI configuration
    depictio-cli config show-cli-config
    ```

=== "Configuration Errors"

    **Error:** "Project config validation failed"

    **Solutions:**
    ```bash
    # Validate configuration with verbose output
    depictio-cli config validate-project-config --project-config-path ./config.yaml --verbose

    # Check configuration examples
    # See: minimal_config.md and full_reference_config.md
    ```

=== "Permission Issues"

    **Error:** "Admin access required"

    **Solutions:**
    - Ensure you're logged in with admin credentials
    - Check CLI configuration includes admin access tokens
    - Contact system administrator for proper permissions

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
