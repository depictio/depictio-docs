---
glightbox: true
---

# :material-database-arrow-right:{ style="color: #009688" } Project Migration

Depictio supports **non-destructive project migration** between instances — move a project (MongoDB metadata + S3 data files + dashboards) from one Depictio deployment to another without touching any other project on the target.

## Overview

Migration works as a scoped upsert: every document is written via `ReplaceOne(..., upsert=True)`, so:

- Re-running migration is idempotent — no duplicates are created.
- Only the migrated project's documents are affected — all other projects on the target remain untouched.
- Owner IDs that do not exist on the target are remapped to the importing admin user.

## How It Works

The CLI and the browser differ in how the files travel, and **Send** goes straight from one instance to the other. All three end in the same scoped upsert on the target: projects (with their workflows and data collections), then files, Delta tables and runs, then dashboards.

<figure markdown="span">
  [![Three ways to move a project: the CLI sends a ZIP without the data and copies the files bucket to bucket, the browser exports a ZIP with the data, and Send goes instance to instance with an invite code issued on the target](../../images/guides/migration/migration-paths_light.png#only-light)](../../images/guides/migration/migration-paths_light.png){target=_blank}
  [![Three ways to move a project: the CLI sends a ZIP without the data and copies the files bucket to bucket, the browser exports a ZIP with the data, and Send goes instance to instance with an invite code issued on the target](../../images/guides/migration/migration-paths_dark.png#only-dark)](../../images/guides/migration/migration-paths_dark.png){target=_blank}
</figure>

The CLI calls `POST /migrate/export-project` on the source and `/migrate/import-project` on the target. The browser's import goes through `POST /migrate/import-project-zip`, which restores `s3_data/` before the upsert. See [Send to another instance](#send-to-another-instance) for the third path.

### ZIP Archive Contents

| File / Folder | Always present | Description |
|---|:---:|---|
| `bundle.json` | ✅ | MongoDB documents — project (with embedded workflows + data_collections), files, deltatables, runs, dashboards |
| `migrate_metadata.json` | ✅ | Export timestamp, project name, mode, Depictio version, document counts |
| `s3_metadata.json` | ✅ | S3 paths discovered, file/byte counts, errors |
| `s3_data/` | UI only (mode `all`/`files`) | S3 objects bundled at their original paths for cross-instance UI import |

> **Note:** Workflows and data collections are not stored in separate MongoDB collections — they are embedded inside the project document and are exported/imported as part of `projects` in `bundle.json`.

## Migration Modes

| Mode        | MongoDB docs | S3 files | Typical use case                              |
| ----------- | :----------: | :------: | --------------------------------------------- |
| `all`       | ✅           | ✅       | First-time full migration                     |
| `metadata`  | ✅           | ❌       | Both instances share the same S3 bucket       |
| `dashboard` | dashboards only | ❌    | Project exists on remote, updating layouts    |
| `files`     | ❌           | ✅       | MongoDB already migrated, syncing data files  |

## CLI Usage

See [CLI Reference — migrate](../../depictio-cli/usage.md#migrate-commands) for the full option reference.

```bash
# Recommended: dry-run first
depictio migrate \
  --project "My Project" \
  --server ~/.depictio/CLI_local.yaml \
  --to-server ~/.depictio/CLI_remote.yaml \
  --dry-run

# Full migration
depictio migrate \
  --project "My Project" \
  --server ~/.depictio/CLI_local.yaml \
  --to-server ~/.depictio/CLI_remote.yaml

# From the server `depictio local up` runs, to a shared instance
depictio migrate \
  --project "My Project" \
  --server local \
  --to-server ~/.depictio/CLI_remote.yaml
```

`--server` names the source and `--to-server` the target, each as `local` or a
CLI configuration file. Without `--server`, the source is the
[default server](../../depictio-cli/usage.md#choosing-a-server); without
`--to-server`, the target is `~/.depictio/CLI_remote.yaml`, with no fallback to
the local server. `DEPICTIO_CLI_TOKEN` and `DEPICTIO_CLI_API_BASE_URL` apply to
the source only. The former `--CLI-config-path` and `--target-config` still work.

Each config file points to a different Depictio instance and carries its own API URL, token, and S3 credentials.

## Web UI

Export and import are also in the viewer, with no CLI.

### Export a Project

1. Open the project and click **Project settings**.
2. Open **Export**.
3. Click **Export as ZIP**. `depictio_export_<project_id>.zip` downloads: the same bundle the CLI produces, with the data inside.

The project's menu on the **Projects** page also has **Export as ZIP**.

[![Project settings, Export section, with the Export as ZIP button](../../images/guides/project-creation/export_zip_light.webp#only-light){ width="688" }](../../images/guides/project-creation/export_zip_light.webp){target=_blank}
[![Project settings, Export section, with the Export as ZIP button](../../images/guides/project-creation/export_zip_dark.webp#only-dark){ width="688" }](../../images/guides/project-creation/export_zip_dark.webp){target=_blank}

### Import a Project

1. On **Projects**, click **New project**, then **Import a project** under **Or start from**.
2. Open **From a ZIP file**. It is the only tab unless you are an admin on an instance with the migration UI on.
3. Choose the `.zip` file. Tick **Replace the project if it already exists** to overwrite a project with the same id.
4. Click **Import project**. The project, its data and its dashboards are created, owned by your account.

[![The Import a project dialog, From another instance tab](../../images/guides/project-creation/import_from_instance_light.webp#only-light){ width="440" }](../../images/guides/project-creation/import_from_instance_light.webp){target=_blank}
[![The Import a project dialog, From another instance tab](../../images/guides/project-creation/import_from_instance_dark.webp#only-dark){ width="440" }](../../images/guides/project-creation/import_from_instance_dark.webp){target=_blank}

[![The Import a project dialog, From a ZIP file tab](../../images/guides/project-creation/import_from_zip_light.webp#only-light){ width="440" }](../../images/guides/project-creation/import_from_zip_light.webp){target=_blank}
[![The Import a project dialog, From a ZIP file tab](../../images/guides/project-creation/import_from_zip_dark.webp#only-dark){ width="440" }](../../images/guides/project-creation/import_from_zip_dark.webp){target=_blank}

<!-- prettier-ignore -->
!!! note "Owner remapping"
    When importing via the UI, all project and dashboard owners in the bundle are automatically remapped to the importing user. This differs from the CLI, which only remaps owners that do not already exist on the target instance.

## Send to another instance <small>(v1.21.0+)</small> { #send-to-another-instance }

A project can also go straight from one instance to another, with no file to carry. The receiving instance issues a code, and the project's owner sends with it.

1. **On the receiving instance**, an admin opens **New project** > **Import a project** > **From another instance**, or **Admin** > **Migrations** > **Receive a project**.
2. Under **Options**, set **Code expires after** (1 day, 30 days or 1 year), **Imported project is read-only** and an optional **Note**.
3. **Create code** shows the **Instance URL** and the **Code** once. Pass both to the project's owner.
4. **On the sending instance**, the owner opens **Project settings** > **Send** > **Send to another instance**.
5. Under **Destination**, paste the URL and the invite code. **Check** shows what will travel and whether it is imported right away. Then **Send**.
6. On the receiving instance, the project appears with a **Read-only** badge when it was locked. An admin locks and unlocks it on its **Permissions** page.

A project is updated only with the code that first brought it: send again with the same code to publish a new version. Admins see a banner on **Projects** when a project was received or needs a decision, and a live toast when `DEPICTIO_EVENTS_ENABLED` is on.

[![Receive a project: the Instance URL and Code shown once, with copy buttons](../../images/guides/migration/receive_project_dialog_light.webp#only-light){ width="440" }](../../images/guides/migration/receive_project_dialog_light.webp){target=_blank}
[![Receive a project: the Instance URL and Code shown once, with copy buttons](../../images/guides/migration/receive_project_dialog_dark.webp#only-dark){ width="440" }](../../images/guides/migration/receive_project_dialog_dark.webp){target=_blank}

[![Send to another instance, Destination step: Destination URL and Invite code](../../images/guides/migration/send_destination_light.webp#only-light){ width="460" }](../../images/guides/migration/send_destination_light.webp){target=_blank}
[![Send to another instance, Destination step: Destination URL and Invite code](../../images/guides/migration/send_destination_dark.webp#only-dark){ width="460" }](../../images/guides/migration/send_destination_dark.webp){target=_blank}

[![Send to another instance, Check step: what travels, imported right away, read-only there](../../images/guides/migration/send_checked_light.webp#only-light){ width="429" }](../../images/guides/migration/send_checked_light.webp){target=_blank}
[![Send to another instance, Check step: what travels, imported right away, read-only there](../../images/guides/migration/send_checked_dark.webp#only-dark){ width="429" }](../../images/guides/migration/send_checked_dark.webp){target=_blank}

[![The Projects page banner telling an admin a project was received](../../images/guides/migration/received_projects_light.webp#only-light)](../../images/guides/migration/received_projects_light.webp){target=_blank}
[![The Projects page banner telling an admin a project was received](../../images/guides/migration/received_projects_dark.webp#only-dark)](../../images/guides/migration/received_projects_dark.webp){target=_blank}

[![A received project with its Read-only badge](../../images/guides/migration/read_only_badge_light.webp#only-light)](../../images/guides/migration/read_only_badge_light.webp){target=_blank}
[![A received project with its Read-only badge](../../images/guides/migration/read_only_badge_dark.webp#only-dark)](../../images/guides/migration/read_only_badge_dark.webp){target=_blank}

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../../images/guides/migration/send-receive.webp" src="../../../images/guides/migration/send-receive.mp4"></video></figure>

The controls need `DEPICTIO_MIGRATION_UI_ENABLED` on both sides. The receiving side also needs `DEPICTIO_MIGRATION_INBOUND_ENABLED`, and the sending side `DEPICTIO_MIGRATION_DESTINATION_DOMAINS` (`"*"` allows any host, the Helm chart default is `["*"]`). See [Publishing to another instance](publishing.md) for the full reference.

## S3 Data Scope

When `mode=all` or `mode=files`, the migrate feature copies S3 objects for all supported data collection types:

| Data Collection Type | S3 location source                                        |
| -------------------- | --------------------------------------------------------- |
| Delta Lake / Table   | `deltatables.delta_table_location`                        |
| GeoJSON              | `data_collections.config.dc_specific_properties.s3_location` |
| Image                | `data_collections.config.dc_specific_properties.s3_base_folder` |
| MultiQC              | `multiqc_reports.s3_location`                             |
| Genomic tracks       | The `genomic_tracks/<dc_id>/` folder of the data bucket (files uploaded at ingestion; tracks read in place are not copied) |

S3 objects are streamed directly from source to target (no full buffering in RAM).

## Permissions

Both the CLI and UI require **administrator** privileges:

- **CLI**: both source and target configs must authenticate as admins.
- **UI export**: the user must be admin (or project owner).
- **UI import**: the user must be admin; all document owners are remapped to the importing user.
