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
  - [🍳 Recipe Commands](#recipe-commands)
  - [📋 Config Commands](#config-commands)
  - [📊 Data Commands](#data-commands)
  - [📈 Dashboard Commands](#dashboard-commands)
  - [💾 Backup Commands](#backup-commands)
  - [🔄 Migrate Commands](#migrate-commands)
- [🛠️ Common Use Cases](#common-use-cases)
<!-- - [🔧 Error Handling](#error-handling) -->

## Installation

See the [installation guide](../installation/cli.md) for instructions on how to install the depictio-cli.

## Quick Reference

| Command                                | Description                             | Access Level   |
| -------------------------------------- | --------------------------------------- | -------------- |
| `version`                              | Show CLI version                        | All users      |
| `run`                                  | Execute complete workflow               | All users      |
| `recipe list`                          | List all bundled recipes                | All users      |
| `recipe info <name>`                   | Show recipe sources and schema          | All users      |
| `recipe run <name>`                    | Execute a recipe locally with validation| All users      |
| `config show-cli-config`               | Display CLI configuration               | All users      |
| `config check-s3-storage`              | Validate S3 storage setup               | All users      |
| `config check-server-accessibility`    | Test server connection                  | All users      |
| `config validate-project-config`       | Validate project configuration          | All users      |
| `config sync-project-config-to-server` | Sync project config to server           | All users      |
| `data scan`                            | Scan project files                      | All users      |
| `data process`                         | Process data collections                | All users      |
| `dashboard validate`                   | Validate dashboard YAML file locally    | All users      |
| `dashboard import`                     | Import dashboard YAML to server         | All users      |
| `dashboard export`                     | Export dashboard to YAML file           | All users      |
| `backup create`                        | Create system backup                    | **Admin only** |
| `backup list`                          | List available backups                  | **Admin only** |
| `backup validate`                      | Validate backup against models          | **Admin only** |
| `backup restore`                       | Restore from backup                     | **Admin only** |
| `backup check-coverage`                | Check validation coverage               | **Admin only** |
| `migrate`                          | Migrate a project to another instance   | **Admin only** |

<!-- | Command                                | Description                             | Access Level   |
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
| `backup create`                        | Create system backup                    | **Admin only** |
| `backup list`                          | List available backups                  | **Admin only** |
| `backup validate`                      | Validate backup against models          | **Admin only** |
| `backup restore`                       | Restore from backup                     | **Admin only** |
| `backup check-coverage`                | Check validation coverage               | **Admin only** | -->

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
    | `--project-config-path` | `string` | `""` | Pipeline configuration file path (mutually exclusive with `--template`) |
    | `--workflow-name` | `string` | `null` | Specific workflow to process |
    | `--data-collection-tag` | `string` | `null` | Data collection tag to process |

??? info "🍳 Template Options"

    Use these flags to run from a pre-packaged template instead of a project YAML. `--template` and `--project-config-path` are mutually exclusive.

    | Parameter | Type | Default | Description |
    |-----------|------|---------|-------------|
    | `--template` | `string` | `null` | Template ID (e.g. `nf-core/ampliseq/2.16.0`) |
    | `--data-root` | `path` | `null` | Root directory substituted for `{DATA_ROOT}` in template. Required when `--template` is set. |
    | `--project-name` | `string` | `null` | Custom project name (auto-generated from template if omitted) |
    | `--dashboard` | `path` | `null` | Override default dashboard(s) to import. Repeatable. |
    | `--skip-dashboard-import` | `flag` | `false` | Skip the automatic dashboard import step (Step 8) |

    See [Templates](templates.md) for full documentation.

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

=== "Template (nf-core/ampliseq)"

```bash
# Set up a complete ampliseq project from raw pipeline output
depictio-cli run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run
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

### 🍳 Recipe Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio-cli recipe`"
    All commands in this section are part of the `recipe` command family. Use them to discover, inspect, and locally test data transformation recipes before running them in a project. For full recipe documentation, see [Recipes](recipes.md).

Discover and execute data transformation recipes locally.

#### `recipe list`

List all bundled recipes.

```bash
depictio-cli recipe list
```

**Output:**

```
Available recipes (5):
  nf-core/ampliseq/alpha_diversity.py
  nf-core/ampliseq/alpha_rarefaction.py
  nf-core/ampliseq/ancombc.py
  nf-core/ampliseq/taxonomy_composition.py
  nf-core/ampliseq/taxonomy_rel_abundance.py
```

---

#### `recipe info <name>`

Show recipe details: description, sources, and expected output schema.

```bash
depictio-cli recipe info <recipe_name>
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `recipe_name` | `string` | **required** | Recipe name (e.g. `nf-core/ampliseq/alpha_diversity.py`) |

```bash
depictio-cli recipe info nf-core/ampliseq/alpha_diversity.py
```

**Output:**

```
Recipe: nf-core/ampliseq/alpha_diversity.py
Description: Transform QIIME2 alpha diversity vector to per-sample Faith PD table.

Sources (1):
  faith_pd: qiime2/diversity/alpha_diversity/faith_pd_vector/metadata.tsv (TSV)

Expected output schema (3 columns):
  sample: Utf8
  habitat: Utf8
  faith_pd: Float64
```

---

#### `recipe run <name>`

Execute a recipe against a local data directory with all 4 validation checkpoints.

```bash
depictio-cli recipe run <recipe_name> [OPTIONS]
```

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `recipe_name` | — | **required** | Recipe name (e.g. `nf-core/ampliseq/alpha_diversity.py`) |
| `--data-dir` | `-d` | **required** | Root directory with workflow output files |
| `--output` | `-o` | `null` | Save result to `.parquet` or `.csv` file |
| `--head` | `-n` | `20` | Number of rows to display |

```bash
# Run with validation output
depictio-cli recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results

# Save output and show first 5 rows
depictio-cli recipe run nf-core/ampliseq/alpha_diversity.py \
  --data-dir /data/ampliseq_results \
  --output alpha_diversity.parquet \
  --head 5
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

Validate a dashboard YAML file. Runs in two passes: schema + domain constraints (always), then server schema validation (when `--config` is provided).

```bash
depictio-cli dashboard validate <yaml_file> [OPTIONS]
```

| Parameter           | Type      | Default      | Description                                                       |
| ------------------- | --------- | ------------ | ----------------------------------------------------------------- |
| `yaml_file`         | `path`    | **required** | Path to YAML dashboard file                                       |
| `--config` / `-c`   | `string`  | `null`       | CLI config file — enables server schema validation (Pass 2)       |
| `--offline`         | `boolean` | `false`      | Skip server schema check even when `--config` is provided         |
| `--verbose` / `-v`  | `boolean` | `false`      | Show detailed validation output                                   |
| `--api`             | `string`  | from config  | API base URL                                                      |

```bash
# Schema + domain only (no server needed)
depictio-cli dashboard validate my_dashboard.yaml

# Full validation including server column check
depictio-cli dashboard validate my_dashboard.yaml --config ~/.depictio/admin_config.yaml

# Force offline even when config is provided
depictio-cli dashboard validate my_dashboard.yaml --config ~/.depictio/admin_config.yaml --offline
```

**Example Output (Success):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
  <span style="color: #2e7d32;">✓ Schema + domain OK</span>
  Pass 2: server schema validation
  <span style="color: #2e7d32;">✓ Server schema OK</span>

<span style="color: #2e7d32;">✓ Validation passed</span>
</pre>
</div>

**Example Output (Failure — per-component error table):**

<div class="terminal-output" style="background-color: var(--md-code-bg-color); padding: 1em; border-radius: 0.25rem; overflow-x: auto; font-size: 0.85em;">
<pre style="margin: 0; color: var(--md-code-fg-color);">Validating: <span style="color: #c2185b;">my_dashboard.yaml</span>
  Pass 1: schema + domain constraints
<span style="color: #c62828;">✗ Schema/domain validation failed</span>
                         Validation Errors
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component     ┃ Field     ┃ Message                                            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ pie-chart     │ -         │ Invalid visu_type 'pie' for mode='ui'.             │
│               │           │ Valid values: scatter, line, bar, box, histogram   │
└───────────────┴───────────┴────────────────────────────────────────────────────┘
</pre>
</div>

---

#### `dashboard import`

Import a dashboard YAML file to the server. The project is determined from the YAML `project_tag` field or the `--project` option.

```bash
depictio-cli dashboard import <yaml_file> [OPTIONS]
```

| Parameter          | Type      | Default      | Description                                                    |
| ------------------ | --------- | ------------ | -------------------------------------------------------------- |
| `yaml_file`        | `path`    | **required** | Path to YAML dashboard file                                    |
| `--config` / `-c`  | `string`  | `null`       | Path to CLI config file (required unless `--dry-run`)          |
| `--project` / `-p` | `string`  | `null`       | Project ID (overrides `project_tag` in YAML)                   |
| `--overwrite`      | `boolean` | `false`      | Update existing dashboard with same title                      |
| `--dry-run`        | `boolean` | `false`      | Validate schema + domain only, don't import (no server needed) |
| `--offline`        | `boolean` | `false`      | Skip server schema check (column names not verified)           |
| `--api`            | `string`  | from config  | API base URL                                                   |

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
  API URL: localhost:8058

<span style="color: #0097a7;">Importing dashboard (project: Iris_Dataset_Project)...</span>
<span style="color: #2e7d32;">✓ Dashboard imported successfully!</span>
  Dashboard ID: 6824cb3b89d2b72169309737
  Title: Iris Dashboard Demo
  Project ID: 650a1b2c3d4e5f6a7b8c9d0e

<span style="color: #0097a7;">View at:</span> localhost:8058/dashboard/6824cb3b89d2b72169309737
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

### 💾 Backup Commands

<!-- prettier-ignore -->
!!! info "Command Group: `depictio-cli backup`"
    All commands in this section are part of the `backup` command family. Use them to backup and restore MongoDB database and S3 data. **Admin access required.**

Backup and restore system data and configurations.

#### `backup create`

Create a backup of the MongoDB database.

```bash
depictio-cli backup create [OPTIONS]
```

| Parameter            | Type      | Default                | Description                          |
| -------------------- | --------- | ---------------------- | ------------------------------------ |
| `--CLI-config-path`  | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path          |
| `--dry-run`          | `boolean` | `false`                | Validate without creating backup     |
| `--include-s3-data`  | `boolean` | `false`                | Include S3 deltatable data in backup |
| `--s3-backup-prefix` | `string`  | `backup`               | Prefix for S3 backup location        |

```bash
depictio-cli backup create --include-s3-data
```

---

#### `backup list`

List available backup files on the server.

```bash
depictio-cli backup list [OPTIONS]
```

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |

```bash
depictio-cli backup list
```

---

#### `backup validate`

Validate a backup file against Pydantic models.

```bash
depictio-cli backup validate <backup_id> [OPTIONS]
```

| Parameter           | Type     | Default                | Description                             |
| ------------------- | -------- | ---------------------- | --------------------------------------- |
| `backup_id`         | `string` | **required**           | Backup ID to validate (YYYYMMDD_HHMMSS) |
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path             |

```bash
depictio-cli backup validate 20240115_143052
```

---

#### `backup restore`

Restore data from a backup file. **Warning: destructive operation.**

```bash
depictio-cli backup restore <backup_id> [OPTIONS]
```

| Parameter           | Type      | Default                | Description                             |
| ------------------- | --------- | ---------------------- | --------------------------------------- |
| `backup_id`         | `string`  | **required**           | Backup ID to restore (YYYYMMDD_HHMMSS)  |
| `--CLI-config-path` | `string`  | `~/.depictio/CLI.yaml` | CLI configuration file path             |
| `--dry-run`         | `boolean` | `false`                | Simulate restore without making changes |
| `--collections`     | `string`  | `null`                 | Comma-separated list of collections     |
| `--force`           | `boolean` | `false`                | Skip confirmation prompt                |

```bash
depictio-cli backup restore 20240115_143052 --dry-run
```

---

#### `backup check-coverage`

Check validation coverage for all MongoDB collections.

```bash
depictio-cli backup check-coverage [OPTIONS]
```

| Parameter           | Type     | Default                | Description                 |
| ------------------- | -------- | ---------------------- | --------------------------- |
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml` | CLI configuration file path |

```bash
depictio-cli backup check-coverage
```

### 🔄 Migrate Commands

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    All migrate operations require administrator privileges on both the source and target instances.

#### `migrate`

Migrate a project from one Depictio instance to another — non-destructive upsert, never wipes existing data on the target.

```bash
depictio-cli migrate --project <name> [OPTIONS]
```

| Parameter           | Type     | Default                     | Description                                        |
| ------------------- | -------- | --------------------------- | -------------------------------------------------- |
| `--project`         | `string` | **required**                | Project name to migrate                            |
| `--CLI-config-path` | `string` | `~/.depictio/CLI.yaml`      | Source instance CLI config (credentials + API URL) |
| `--target-config`   | `string` | `~/.depictio/CLI_remote.yaml` | Target instance CLI config                       |
| `--mode`            | `string` | `all`                       | Migration scope: `all`, `metadata`, `dashboard`, `files` |
| `--dry-run`         | `flag`   | `False`                     | Preview changes without writing anything           |

**Migration modes:**

| Mode        | What is migrated                                  | When to use                                         |
| ----------- | ------------------------------------------------- | --------------------------------------------------- |
| `all`       | MongoDB documents + S3 files                      | First-time full migration                           |
| `metadata`  | MongoDB documents only                            | Both instances share the same S3 storage            |
| `dashboard` | Dashboard documents only                          | Project already exists on remote, updating layouts  |
| `files`     | S3 files only                                     | MongoDB already migrated, syncing data files        |

```bash
# Dry-run first (recommended before any migration)
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --dry-run

# Full migration (MongoDB + S3)
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml

# Metadata-only (shared S3)
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --mode metadata

# Dashboard-only update
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --mode dashboard
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
!!! warning "Admin Access Required"
    All backup operations require administrator privileges.

=== "Create Backup"

```bash
# Create database backup
depictio-cli backup create

# Include S3 deltatable data
depictio-cli backup create --include-s3-data
```

=== "Restore Backup"

```bash
# List available backups
depictio-cli backup list

# Preview restore
depictio-cli backup restore 20240115_143052 --dry-run

# Restore specific backup
depictio-cli backup restore 20240115_143052 --force
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

### 🔄 Project Migration

<!-- prettier-ignore -->
!!! warning "Admin Access Required"
    Migration requires administrator privileges on both source and target instances.

=== "First-time Migration"

```bash
# 1. Dry-run to preview what will be migrated
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --dry-run

# 2. Run full migration (MongoDB docs + S3 files)
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml
```

=== "Shared S3 Storage"

```bash
# When source and target share the same S3, only migrate MongoDB docs
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --mode metadata
```

=== "Dashboard Update"

```bash
# Push updated dashboard layouts to a remote instance
# (project and data already exist on remote)
depictio-cli migrate \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --mode dashboard
```

## 📖 Configuration References

- [Minimal YAML Configuration](minimal_config.md)
- [Full Reference Configuration](full_reference_config.md)

<!--
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
``` -->


<!-- ---

#### `data join`

Execute pre-computed table joins defined in project configuration.

<!-- prettier-ignore -->
<!-- !!! note "Links vs Joins"
    For interactive cross-DC filtering, use **links** (configured in YAML, resolved at runtime). Use **joins** only when you need a pre-computed combined dataset stored as a Delta table. See [Cross-DC Filtering](../features/cross-dc-filtering.md). -->

<!-- ```bash
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
---

#### `data link`

Manage DC links for cross-DC interactive filtering. Links enable runtime filtering between data collections without pre-computing joined tables.

<!-- prettier-ignore -->
<!-- !!! tip "Links vs Joins"
    **Links** are the preferred method for cross-DC filtering. They resolve at runtime and support any DC type (tables, MultiQC, etc.). **Joins** create pre-computed Delta tables and only work between table DCs. -->

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
``` -->
