---
title: Administration
icon: material/shield-account
description: Migration, backups, monitoring, usage statistics, branding, groups, admin tables and the Activity page.
glightbox: true
---

# :material-shield-account: Administration

Running a Depictio deployment: moving and protecting its data, watching its work, and shaping it for your users.

<div class="grid cards" markdown>

-   :material-database-arrow-right:{ .lg .middle .dp-teal } **Project migration**

    ---

    Move a project, its data and dashboards, to another instance.

    [:octicons-arrow-right-24: Project migration](migrate.md)

-   :material-database-export:{ .lg .middle .dp-blue } **Backup and restore**

    ---

    Snapshot and restore the database, from the admin panel or the CLI.

    [:octicons-arrow-right-24: Backup and restore](backup.md)

-   :material-chart-timeline-variant:{ .lg .middle .dp-orange } **Monitoring**

    ---

    Celery tasks, ingestion runs, watchers, logs and worker health.

    [:octicons-arrow-right-24: Log and Task](monitoring.md)

-   :material-chart-bar:{ .lg .middle .dp-teal } **Usage statistics**

    ---

    Who uses the instance and what they open, kept in your own database.

    [:octicons-arrow-right-24: Usage](usage-stats.md)

-   :material-palette-outline:{ .lg .middle .dp-purple } **Branding**

    ---

    The deployment's own logo, name, colours, typography and figure palette.

    [:octicons-arrow-right-24: Branding](branding.md)

-   :material-account-group-outline:{ .lg .middle .dp-violet } **Groups**

    ---

    Share projects with a whole lab, run by its group admins.

    [:octicons-arrow-right-24: Groups](groups.md)

-   :material-format-list-checks:{ .lg .middle .dp-green } **Activity page**

    ---

    Tasks and ingestion runs of your projects, without admin rights.

    [:octicons-arrow-right-24: Activity](#activity)

</div>

## Admin tables <small>(v1.21.0+)</small> { #admin-tables }

**Projects**, **Dashboards** and **Users** in the admin panel are tables with search, sort, a column chooser and row actions. Select several rows to delete them in one go, and switch to the compact **Rows** mode to see more on screen.

[![The admin Projects table, its column chooser open](../../images/guides/admin/admin_projects_columns_light.webp#only-light)](../../images/guides/admin/admin_projects_columns_light.webp){target=_blank}
[![The admin Projects table, its column chooser open](../../images/guides/admin/admin_projects_columns_dark.webp#only-dark)](../../images/guides/admin/admin_projects_columns_dark.webp){target=_blank}

## Activity page <small>(v1.21.0+)</small> { #activity }

`/activity` lists the tasks, ingestion runs and agents of the projects you belong to, without admin rights. Owners and editors see the full detail. Viewers see a redacted version. Logs stay admin-only, in [Monitoring](monitoring.md).

[![The /activity page, listing the tasks and ingestion runs of your projects](../../images/guides/admin/activity_page_light.webp#only-light)](../../images/guides/admin/activity_page_light.webp){target=_blank}
[![The /activity page, listing the tasks and ingestion runs of your projects](../../images/guides/admin/activity_page_dark.webp#only-dark)](../../images/guides/admin/activity_page_dark.webp){target=_blank}
