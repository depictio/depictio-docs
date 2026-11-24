# Administration

Running a Depictio deployment: moving and protecting its data, watching its work, and shaping it for your users.

- **Project migration**

  ______________________________________________________________________

  Move a project, its data and dashboards, to another instance.

  [Project migration](https://depictio.github.io/depictio-docs/latest/usage/administration/migrate/index.md)

- **Backup and restore**

  ______________________________________________________________________

  Snapshot and restore the database, from the admin panel or the CLI.

  [Backup and restore](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md)

- **Monitoring**

  ______________________________________________________________________

  Celery tasks, ingestion runs, watchers, logs and worker health.

  [Log and Task](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/index.md)

- **Branding**

  ______________________________________________________________________

  The deployment's own logo, name, colours, typography and figure palette.

  [Branding](https://depictio.github.io/depictio-docs/latest/usage/administration/branding/index.md)

- **Groups**

  ______________________________________________________________________

  Share projects with a whole lab, run by its group admins.

  [Groups](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/index.md)

- **Activity page**

  ______________________________________________________________________

  Tasks and ingestion runs of your projects, without admin rights.

  [Activity](#activity)

## Admin tables (v1.21.0+)

**Projects**, **Dashboards** and **Users** in the admin panel are tables with search, sort, a column chooser and row actions. Select several rows to delete them in one go, and switch to the compact **Rows** mode to see more on screen.

## Activity page (v1.21.0+)

`/activity` lists the tasks, ingestion runs and agents of the projects you belong to, without admin rights. Owners and editors see the full detail. Viewers see a redacted version. Logs stay admin-only, in [Monitoring](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/index.md).
