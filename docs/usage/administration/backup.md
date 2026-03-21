---
title: Backup & Restore
description: Back up and restore Depictio MongoDB data using the CLI.
---

# :material-database-export: Backup & Restore

The `depictio-cli backup` commands let administrators snapshot the MongoDB database and restore it from a previous backup. All backup operations require admin credentials.

!!! warning "Admin only"
    All `backup` sub-commands require the authenticated user to be an administrator.

---

## Commands

### `backup create`

Create a server-side snapshot of the MongoDB database. Short-lived tokens and temporary users are excluded automatically.

```bash
depictio-cli backup create

# Also back up S3 Delta Lake files
depictio-cli backup create --include-s3-data --s3-backup-prefix my-backup
```

| Flag | Default | Description |
|------|---------|-------------|
| `--include-s3-data` | `false` | Also back up S3 Delta Lake files |
| `--s3-backup-prefix` | `"backup"` | Prefix for the S3 backup folder |
| `--dry-run` | `false` | Validate the backup process without writing anything |

On success, prints a backup ID (format `YYYYMMDD_HHMMSS`) and document counts per collection.

---

### `backup list`

List all available backups stored on the server.

```bash
depictio-cli backup list
```

---

### `backup validate`

Check that a backup file is well-formed and passes Pydantic model validation before attempting a restore.

```bash
depictio-cli backup validate 20260315_143000
```

---

### `backup restore`

!!! danger "Destructive operation"
    Restore **replaces existing data** in the selected collections. Use `--dry-run` first to preview what would change.

Restore all or selected collections from a backup snapshot.

```bash
# Preview first
depictio-cli backup restore 20260315_143000 --dry-run

# Restore everything (prompts for confirmation)
depictio-cli backup restore 20260315_143000

# Restore specific collections only
depictio-cli backup restore 20260315_143000 --collections projects,dashboards

# Skip confirmation prompt (automation / CI)
depictio-cli backup restore 20260315_143000 --force
```

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | `false` | Simulate restore without writing any changes |
| `--collections` | all | Comma-separated list of collections to restore |
| `--force` | `false` | Skip the confirmation prompt |

---

## Typical workflow

```bash
# 1. Create a backup before a major operation
depictio-cli backup create

# 2. Validate the backup
depictio-cli backup validate 20260315_143000

# 3. Dry-run a restore to see what would change
depictio-cli backup restore 20260315_143000 --dry-run

# 4. Restore if needed
depictio-cli backup restore 20260315_143000
```
