# Project Migration

Depictio supports **non-destructive project migration** between instances — move a project (MongoDB metadata + S3 data files) from one Depictio deployment to another without touching any other project on the target.

## Overview

Migration works as a scoped upsert: every document is written via `ReplaceOne(..., upsert=True)`, so:

- Re-running migration is idempotent — no duplicates are created.
- Only the migrated project's documents are affected — all other projects on the target remain untouched.
- Owner IDs that do not exist on the target are remapped to the importing admin user.

## How It Works

```
Source instance                        Target instance
─────────────────                      ─────────────────
depictio-cli                           API: /migrate/import-project
    │                                       │
    ├─ api_export_project()                 ├─ Upsert: projects
    │     └─ POST /migrate/export-project   ├─ Upsert: workflows
    │           → ZIP bundle               ├─ Upsert: data_collections
    │             ├─ bundle.json           ├─ Upsert: files / deltatables / runs
    │             └─ migrate_metadata.json └─ Upsert: dashboards
    │
    └─ (optionally) copy S3 files
          source MinIO → target MinIO
```

The export endpoint returns a **ZIP archive** containing:

- `bundle.json` — all MongoDB documents for the project (projects, workflows, data_collections, files, deltatables, runs, dashboards)
- `migrate_metadata.json` — export timestamp, project name, mode, document counts

## Migration Modes

| Mode        | MongoDB docs | S3 files | Typical use case                              |
| ----------- | :----------: | :------: | --------------------------------------------- |
| `all`       | ✅           | ✅       | First-time full migration                     |
| `metadata`  | ✅           | ❌       | Both instances share the same S3 bucket       |
| `dashboard` | dashboards only | ❌    | Project exists on remote, updating layouts    |
| `files`     | ❌           | ✅       | MongoDB already migrated, syncing data files  |

## CLI Usage

See [CLI Reference — migrate run](../../depictio-cli/usage.md#migrate-commands) for the full option reference.

```bash
# Recommended: dry-run first
depictio-cli migrate run \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml \
  --dry-run

# Full migration
depictio-cli migrate run \
  --project "My Project" \
  --CLI-config-path ~/.depictio/CLI_local.yaml \
  --target-config ~/.depictio/CLI_remote.yaml
```

Each config file points to a different Depictio instance and carries its own API URL, token, and S3 credentials.

## Web UI

Migration is also available directly from the Projects page — no CLI required.

### Export a Project

1. Open **Projects** (`/projects`).
2. Expand the project you want to export.
3. Open the **Project Management** accordion section.
4. Click **Export Project** (violet button).
5. A `.zip` file downloads automatically — this is the same bundle the CLI produces.

### Import a Project

1. Click **Create New Project**.
2. Switch to the **Import** tab.
3. Drag-and-drop (or browse for) the `.zip` bundle.
4. A preview shows the project name, export mode, and document counts.
5. Click **Import Project** — the project is created and owned by your account.

<!-- prettier-ignore -->
!!! note "Owner remapping"
    When importing via the UI, all project and dashboard owners in the bundle are automatically remapped to the importing user. This differs from the CLI, which only remaps owners that do not already exist on the target instance.

## S3 Data Scope

When `mode=all` or `mode=files`, the migrate feature copies S3 objects for all supported data collection types:

| Data Collection Type | S3 location source                                        |
| -------------------- | --------------------------------------------------------- |
| Delta Lake / Table   | `deltatables.delta_table_location`                        |
| GeoJSON              | `data_collections.config.dc_specific_properties.s3_location` |
| Image                | `data_collections.config.dc_specific_properties.s3_base_folder` |
| MultiQC              | `multiqc_reports.s3_location`                             |
| JBrowse2             | S3 URIs in `jbrowse_collection.tracks[].uri`              |

S3 objects are streamed directly from source to target (no full buffering in RAM).

## Permissions

Both the CLI and UI require **administrator** privileges:

- **CLI**: both source and target configs must authenticate as admins.
- **UI export**: the user must be admin (or project owner).
- **UI import**: the user must be admin; all document owners are remapped to the importing user.
