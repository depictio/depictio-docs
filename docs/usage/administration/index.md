---
title: Administration
icon: material/shield-account
description: Operational tasks for managing Depictio deployments.
glightbox: true
---

# :material-shield-account: Administration

Operational tasks for managing Depictio deployments.

| Page | Description |
|------|-------------|
| [Project Migration](migrate.md) | Move projects between Depictio instances non-destructively |
| [Backup & Restore](backup.md) | Snapshot and restore the database from the admin panel or the CLI, on a schedule if you want one |
| [Monitoring (Log & Task)](monitoring.md) | Admin panel for Celery tasks, ingestion runs, logs, and worker health |
| [Branding](branding.md) | Give the deployment its own logo, name, colours, typography and figure palette |
| [Groups](groups.md) | Share projects with whole groups, and let group admins and a P.I. run their own group |

## Admin tables <small>(v1.21.0+)</small> { #admin-tables }

**Projects**, **Dashboards** and **Users** in the admin panel are tables with search, sort, a column chooser and row actions. Select several rows to delete them in one go, and switch to the compact **Rows** mode to see more on screen.

[![The admin Projects table, its column chooser open](../../images/guides/admin/admin_projects_columns_light.webp#only-light)](../../images/guides/admin/admin_projects_columns_light.webp){target=_blank}
[![The admin Projects table, its column chooser open](../../images/guides/admin/admin_projects_columns_dark.webp#only-dark)](../../images/guides/admin/admin_projects_columns_dark.webp){target=_blank}

## Activity page <small>(v1.21.0+)</small> { #activity }

`/activity` lists the tasks, ingestion runs and agents of the projects you belong to, without admin rights. Owners and editors see the full detail. Viewers see a redacted version. Logs stay admin-only, in [Monitoring](monitoring.md).

[![The /activity page, listing the tasks and ingestion runs of your projects](../../images/guides/admin/activity_page_light.webp#only-light)](../../images/guides/admin/activity_page_light.webp){target=_blank}
[![The /activity page, listing the tasks and ingestion runs of your projects](../../images/guides/admin/activity_page_dark.webp#only-dark)](../../images/guides/admin/activity_page_dark.webp){target=_blank}
