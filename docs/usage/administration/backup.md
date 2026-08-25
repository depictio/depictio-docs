---
title: Backup & Restore
description: Back up and restore Depictio MongoDB data using the CLI.
---

# :material-database-export: Backup & Restore

The `depictio backup` commands let administrators snapshot the MongoDB database and restore it from a previous backup. All backup operations require admin credentials.

!!! warning "Admin only"
    All `backup` sub-commands require the authenticated user to be an administrator.

---

## Commands

### `backup create`

Create a server-side snapshot of the MongoDB database. Short-lived tokens and temporary users are excluded automatically.

```bash
depictio backup create

# Also back up S3 Delta Lake files
depictio backup create --include-s3-data --s3-backup-prefix my-backup
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
depictio backup list
```

---

### `backup validate`

Check that a backup file is well-formed and passes Pydantic model validation before attempting a restore.

```bash
depictio backup validate 20260315_143000
```

---

### `backup restore`

!!! danger "Destructive operation"
    Restore **replaces existing data** in the selected collections. Use `--dry-run` first to preview what would change.

Restore all or selected collections from a backup snapshot.

```bash
# Preview first
depictio backup restore 20260315_143000 --dry-run

# Restore everything (prompts for confirmation)
depictio backup restore 20260315_143000

# Restore specific collections only
depictio backup restore 20260315_143000 --collections projects,dashboards

# Skip confirmation prompt (automation / CI)
depictio backup restore 20260315_143000 --force
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
depictio backup create

# 2. Validate the backup
depictio backup validate 20260315_143000

# 3. Dry-run a restore to see what would change
depictio backup restore 20260315_143000 --dry-run

# 4. Restore if needed
depictio backup restore 20260315_143000
```

---

## What is covered

A backup snapshots the MongoDB collections that hold your work: projects,
dashboards, workflows, data collections, users and permissions. Short-lived
tokens and temporary users are excluded automatically.

Four collections are **deliberately not backed up**, because they are
operational rather than authored data:

| Collection | Why it is excluded |
|------------|--------------------|
| `task_events` | Celery task history, expired by a TTL index |
| `app_logs` | Application logs, a capped collection |
| `telemetry` | Anonymous aggregate counters |
| `ingestion_runs` | Ingestion audit and lineage records |

!!! note "`ingestion_runs` has no TTL"
    Unlike the other three it is not self-expiring, so the ingestion history it
    holds is genuinely not recoverable from a backup. Restoring a snapshot leaves
    whatever is already in that collection untouched.

Backups record the Depictio version that produced them, so a snapshot describes
itself.

## Restoring across versions

!!! warning "Supported from v1.0.0 onwards"
    Restoring a backup taken by **v1.0.0 or later** into a newer Depictio is
    supported and covered by tests. Backups produced before v1.0.0 are out of
    scope — the data models changed too much for deserialization to be reliable.

Two checks guard this, so a model change cannot silently break older backups:
frozen backup fixtures are validated against the current Pydantic models on every
pull request, and a scheduled job restores a backup produced by the previous
released image using an image built from current code, comparing document counts.

This matters because restore is destructive: it deletes the target collections
before inserting. A backup that failed to deserialize cleanly could otherwise
drop data on an upgraded deployment. Run `backup validate` before any restore you
have not just created yourself.
