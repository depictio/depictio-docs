---
title: "Move a project to another instance"
description: "Issue an invite code on the target instance, send a project to it from the source, and serve it there read-only."
glightbox: true
---

# Move a project to another instance <small>(v1.21.0+)</small>

A project can travel from one Depictio instance to another with its data, dashboards, logos and comments. An administrator of the target creates a code, and the project's owner on the source sends the project with it.

<figure markdown="span"><video autoplay controls muted loop playsinline poster="../../images/guides/migration/send-receive.webp" src="../../images/guides/migration/send-receive.mp4"></video></figure>

## Before you start

- Depictio **v1.21.0** or later on both instances.
- On the target: `DEPICTIO_MIGRATION_INBOUND_ENABLED=true` and `DEPICTIO_MIGRATION_UI_ENABLED=true`. The Helm chart sets both.
- On the source: `DEPICTIO_MIGRATION_UI_ENABLED=true`, and `DEPICTIO_MIGRATION_DESTINATION_DOMAINS` listing where owners may send. The chart sets `["*"]`, any public https host; the code default `[]` turns sending off.
- Behind an ingress, raise the target's body size limit (`nginx.ingress.kubernetes.io/proxy-body-size`) and its read and send timeouts for large bundles.
- You need to be an administrator on the target and the project's owner (or an administrator) on the source.

## 1. Create a code on the target

On the target, click **New project**, then **Import a project**, and pick **From another instance**. Administrators can also go to **Admin** > **Migrations** and click **Receive a project**.

Under **Options**, set:

- **Code expires after**: **1 day**, **30 days** (the default) or **1 year**.
- **Imported project is read-only**: on by default.
- **Note (optional)**: who the code is for.

Click **Create code**. The dialog shows the **Instance URL** and the **Code** once, with copy buttons. Send both to the project's owner.

[![The Receive dialog after Create code, Instance URL and Code with copy buttons](../images/guides/migration/receive_project_dialog_light.webp#only-light)](../images/guides/migration/receive_project_dialog_light.webp){target=_blank}
[![The Receive dialog after Create code, Instance URL and Code with copy buttons](../images/guides/migration/receive_project_dialog_dark.webp#only-dark)](../images/guides/migration/receive_project_dialog_dark.webp){target=_blank}

## 2. Send the project from the source

On the source, open the project, click **Project settings** and pick **Send**. Click **Send to another instance**.

In the **Destination** step, paste the **Destination URL** and the **Invite code**, and add a message if you like.

[![The Send dialog, Destination step, with Destination URL and Invite code](../images/guides/migration/send_destination_light.webp#only-light)](../images/guides/migration/send_destination_light.webp){target=_blank}
[![The Send dialog, Destination step, with Destination URL and Invite code](../images/guides/migration/send_destination_dark.webp#only-dark)](../images/guides/migration/send_destination_dark.webp){target=_blank}

The **Check** step asks the target what will happen, before anything is built:

- **Imported right away**, or **Waits for an administrator**;
- **Read-only there**, or **Editable there**;
- **Creates the project there**, or **Updates the copy it already has**;
- how much data travels, and any warnings.

[![The Check step listing Imported right away, Read-only there, Creates the project there](../images/guides/migration/send_checked_light.webp#only-light)](../images/guides/migration/send_checked_light.webp){target=_blank}
[![The Check step listing Imported right away, Read-only there, Creates the project there](../images/guides/migration/send_checked_dark.webp#only-dark)](../images/guides/migration/send_checked_dark.webp){target=_blank}

Click **Send**. The dialog follows the push until the target imports it. Past pushes are listed under **Send**, and in **Admin** > **Migrations**.

## 3. Find the project on the target

With an invite code, the import starts at once. The Projects page shows "A project was received", and a toast says so too when realtime events are on (`DEPICTIO_EVENTS_ENABLED=true`).

A push through a pairing key instead waits for review: the banner reads **A project sent to this instance needs a decision**. Click a request to open its sheet, then **Approve** or **Reject**.

[![The Projects page banner telling an admin a project was received](../images/guides/migration/received_projects_light.webp#only-light)](../images/guides/migration/received_projects_light.webp){target=_blank}
[![The Projects page banner telling an admin a project was received](../images/guides/migration/received_projects_dark.webp#only-dark)](../images/guides/migration/received_projects_dark.webp){target=_blank}

[![The migration request sheet with Revalidate, Reject and Approve](../images/guides/migration/request_sheet_light.webp#only-light)](../images/guides/migration/request_sheet_light.webp){target=_blank}
[![The migration request sheet with Revalidate, Reject and Approve](../images/guides/migration/request_sheet_dark.webp#only-dark)](../images/guides/migration/request_sheet_dark.webp){target=_blank}

## 4. Lock or unlock editing

A locked project shows a **Read-only** badge. Nobody can change its dashboards or data, owners included.

[![The imported project's header with the Read-only badge](../images/guides/migration/read_only_badge_light.webp#only-light)](../images/guides/migration/read_only_badge_light.webp){target=_blank}
[![The imported project's header with the Read-only badge](../images/guides/migration/read_only_badge_dark.webp#only-dark)](../images/guides/migration/read_only_badge_dark.webp){target=_blank}

An administrator changes this on the project's **Permissions** page, in the **Editing** row, with **Lock editing** / **Unlock editing**. Visibility is set apart, on the same page: a published copy is usually public and locked.

## 5. Send an update

Send the project again with the same code. The target adds an `import` version instead of overwriting history. Comments written on the target are kept.

## Good to know

- A project can only be updated with the code that first brought it. A new code for a project already there is refused.
- When the code expires, updates stop. To resume, a target admin unlocks and deletes the project, issues a new code, and the source sends again.
- The code is shown once and stored only as a hash. Revoking it in **Admin** > **Migrations** stops it.
- Version history does not travel: the target starts from an `import` version.
- Without a network path, use a ZIP file: on the source, **Project settings** > **Export** > **Export as ZIP**; on the target, **Import a project** > **From a ZIP file**.
- To try it on one machine, start two `depictio local up` instances, each with its own `DEPICTIO_LOCAL_HOME` and `--port`. A local destination is plain http, so put its host in both `DEPICTIO_MIGRATION_DESTINATION_DOMAINS` and `DEPICTIO_MIGRATION_UI_TARGET_HOST_ALLOWLIST` on the source. The Depictio repository scripts this in `dev/migration_lan_test/`.

## See also

- [Publishing and migration reference](../usage/administration/publishing.md)
- [Project migration (CLI and ZIP)](../usage/administration/migrate.md)
- [Kubernetes ingress](../installation/kubernetes.md#ingress)
- [Realtime events](../usage/guides/realtime-events.md)
