---
title: "Configuration"
icon: material/cog
description: "What to set for a first Depictio deployment, then the settings by topic."
---

# Configuration Guide

Depictio reads its configuration from environment variables. This page covers what to set for a
first deployment, then each topic. Every variable, with its default, is in the
[Environment Reference](env-reference.md).

| Deployment | Where the variables go |
|------------|------------------------|
| Docker Compose | `.env` next to `docker-compose.yaml`, started from the repository's [`.env.example`](https://github.com/depictio/depictio/blob/main/.env.example) |
| Helm | `backend.env` in your values file; credentials under `secrets.*`; worker sizing under `celery.env` |
| `depictio local up` | The shell that runs it. See [Python package](local.md) |

## First deployment { #first-deployment }

With no `.env`, the root `docker-compose.yaml` starts in **single-user mode**: no login, and no
secret is checked. That suits one person on one machine. For a server other people reach, set:

```bash
DEPICTIO_AUTH_SINGLE_USER_MODE=false
DEPICTIO_S3_ROOT_USER=depictio
DEPICTIO_S3_ROOT_PASSWORD=change-me     # openssl rand -base64 24
DEPICTIO_BOOTSTRAP_ADMIN_EMAIL=admin@example.org
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=change-me     # openssl rand -base64 24
DEPICTIO_VIEWER_PUBLIC_URL=https://depictio.example.org
DEPICTIO_FASTAPI_PUBLIC_URL=https://depictio.example.org
```

| Variable | Why | Helm |
|----------|-----|------|
| `DEPICTIO_AUTH_SINGLE_USER_MODE=false` | Turns sign-in on, and with it the secret checks | Already `false` |
| `DEPICTIO_S3_ROOT_USER`, `_ROOT_PASSWORD` | Bucket credentials. The server refuses a password under 8 characters or a well-known default such as `minio123` | `secrets.s3RootUser`, `secrets.s3RootPassword`; generated when empty |
| `DEPICTIO_BOOTSTRAP_ADMIN_EMAIL`, `_ADMIN_PASSWORD` | The first admin, created once on an empty database. Without them the first start stops | `secrets.bootstrapAdminEmail`, `secrets.bootstrapAdminPassword` |
| `DEPICTIO_VIEWER_PUBLIC_URL`, `DEPICTIO_FASTAPI_PUBLIC_URL` | The addresses browsers use behind your proxy: magic links and SSO land there | Derived from `global.domain` |

Everything else has a working default. A refused secret is named in the startup error:

```bash
docker compose logs depictio-backend
```

## Storage { #storage-configuration }

Depictio keeps its data in S3-compatible object storage: the bundled SeaweedFS store
(Compose service `s3`, Helm `s3.enabled`), or an external S3 service. The settings are
`DEPICTIO_S3_*`; the `DEPICTIO_MINIO_*` names of releases before v1.12.0 still work. An install
that ran the bundled MinIO copies its data when it upgrades: see
[Upgrading to v1.12.0: MinIO → SeaweedFS](upgrade/v1.12.0-seaweedfs.md). The server creates the
bucket if needed and only needs rights on that bucket: see
[Required S3 permissions](env-reference.md#required-s3-permissions).

### External S3 { #external-s3 }

For AWS, NetApp, Ceph or your own MinIO. With Docker Compose, in `.env`, then start without the
bundled store (`docker compose up -d --scale s3=0`):

```bash
DEPICTIO_S3_PUBLIC_URL=https://s3.example.com
DEPICTIO_S3_EXTERNAL_SERVICE=true
DEPICTIO_S3_BUCKET=your-bucket-name
DEPICTIO_S3_ROOT_USER=your-access-key
DEPICTIO_S3_ROOT_PASSWORD=your-secret-key
```

With Helm, turn the bundled store off; the chart then sets `DEPICTIO_S3_EXTERNAL_SERVICE` itself:

```yaml
s3:
  enabled: false
  env:
    DEPICTIO_S3_PUBLIC_URL: "https://s3.example.com"
    DEPICTIO_S3_BUCKET: "your-bucket-name"
secrets:
  s3RootUser: "your-access-key"
  s3RootPassword: "your-secret-key"
```

## Authentication { #authentication-configuration }

The sign-in mode is one switch, compared in [Authentication Modes](../usage/guides/authentication-modes.md):

```bash
DEPICTIO_AUTH_SINGLE_USER_MODE=true    # one person, no login (the Compose default)
DEPICTIO_AUTH_PUBLIC_MODE=true         # anonymous read-only, sign in to create
DEPICTIO_AUTH_DEMO_MODE=true           # with PUBLIC_MODE: adds the guided tour
```

With none set (and `SINGLE_USER_MODE=false` under Compose), everyone signs in. Restricting
registration or password sign-in, the public-mode access code and pipeline provisioning are on the
same page. Every `DEPICTIO_AUTH_*` variable is in the
[reference](env-reference.md#authentication).

### Single sign-on (OpenID Connect)

Users can sign in through any OpenID Connect identity provider (Keycloak, Google,
Authentik, ...), with their groups mirrored from it. Providers are
declared as a JSON list; credentials go in their own variables:

```bash
DEPICTIO_AUTH_OIDC_PROVIDERS='[
  {
    "id": "google",
    "label": "Sign in with Google",
    "discovery_url": "https://accounts.google.com/.well-known/openid-configuration"
  }
]'
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID=1234567890-example.apps.googleusercontent.com
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET=change-me
```

The redirect URI to register at the provider is
`https://<api-host>/depictio/api/v1/auth/oidc/<id>/callback`. Full reference, provider
recipes and migration from the former `DEPICTIO_AUTH_GOOGLE_OAUTH_*` settings:
[Single sign-on (OpenID Connect)](sso/index.md).

### Keys { #authentication-keys }

On first start the backend writes an RS256 key pair (`private_key.pem`, `public_key.pem`) and
`secrets_key.bin`, which encrypts per-project storage credentials, into `DEPICTIO_AUTH_KEYS_DIR`
(`/app/depictio/keys`). The backend and the Celery worker must share that folder: Compose mounts the
`depictio_keys` volume on both, the Helm chart a volume of its own. To bring your own pair, put the
two files in a folder, mount it read-only on the backend **and** the worker, and point
`DEPICTIO_AUTH_KEYS_DIR` at it:

```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
chmod 600 private_key.pem
```

The internal API key, used between services, is generated too. Set
`DEPICTIO_AUTH_INTERNAL_API_KEY` (e.g. `openssl rand -hex 32`) to choose it.

### CORS

Control which browser origins are allowed to make credentialed cross-origin requests to the FastAPI backend:

```bash
# Comma-separated list of allowed origins (scheme + host + optional port)
DEPICTIO_FASTAPI_CORS_ALLOWED_ORIGINS=https://app.example.com,https://dash.example.com
```

| Value | Behaviour |
|---|---|
| *(empty / unset)* | No credentialed cross-origin requests are permitted |
| `https://app.example.com` | Only the listed origins are allowed |
| `*` | **Rejected when credentials are used**: list explicit origins |

Leave it unset when the browser reaches the API on the viewer's own origin, as with the bundled
nginx.

## Background workers { #background-workers }

The `depictio-celery-worker` container always runs: the dashboard editor's previews, large renders
and thumbnails go through it, over Redis. Size it with `DEPICTIO_CELERY_WORKERS` on the worker
(`celery.env` with Helm; default 4 processes, the chart sets 2). Each process holds its own data, so
memory sets the limit. When renders offload, and how long the API waits, is set on the backend:
see [Celery Task Queue](env-reference.md#celery-task-queue). Offloaded ingestion runs on a second
worker: see [Ingestion worker](docker.md#ingestion-worker).

## Backup and Restore Configuration

MongoDB backups run from the admin panel or on a schedule; S3 data is copied to a second bucket,
a local folder, or both. Day-to-day use is in [Backup & Restore](../usage/administration/backup.md).

```bash
DEPICTIO_BACKUP_AUTO_BACKUP_ENABLED=true
DEPICTIO_BACKUP_AUTO_BACKUP_TIME_OF_DAY=03:00              # UTC
DEPICTIO_BACKUP_BACKUP_FILE_RETENTION_DAYS=30
DEPICTIO_BACKUP_S3_BACKUP_STRATEGY=s3_to_s3                # s3_to_s3, local or both
```

### Backup to Separate S3 Bucket

Keep the copy of S3 data apart from the primary bucket:

```bash
DEPICTIO_BACKUP_BACKUP_S3_ENABLED=true
DEPICTIO_BACKUP_BACKUP_S3_BUCKET=depictio-backups
DEPICTIO_BACKUP_BACKUP_S3_ENDPOINT_URL=https://s3.amazonaws.com
DEPICTIO_BACKUP_BACKUP_S3_ACCESS_KEY=your-backup-s3-access-key
DEPICTIO_BACKUP_BACKUP_S3_SECRET_KEY=your-backup-s3-secret-key
DEPICTIO_BACKUP_BACKUP_S3_REGION=us-east-1
```

Scheduled backups, retention tiers and every `DEPICTIO_BACKUP_*` variable:
[Backup & Restore](env-reference.md#backup-restore).

## Example projects { #example-projects }

At startup the API seeds five reference projects with their dashboards: Iris, Penguins, Advanced
Visualisations, nf-core/ampliseq and nf-core/viralrecon. Every other
[pipeline template](../pipeline-templates/README.md) comes from ingesting a run.

```bash
DEPICTIO_DISABLE_EXAMPLE_DASHBOARDS=true    # seed none of them
DEPICTIO_SEED_PROJECTS=iris,penguins        # or only these
```

## Analytics and telemetry { #analytics }

| What | Default | Set |
|------|---------|-----|
| Anonymous installation [telemetry](../features/telemetry.md), once a day | On | `DEPICTIO_TELEMETRY_ENABLED=false` or `DO_NOT_TRACK=1` to stop it |
| [Internal analytics](env-reference.md#internal-analytics): sessions stored in your MongoDB | Off | `DEPICTIO_ANALYTICS_ENABLED=true` |
| Google Analytics 4 | Off | `DEPICTIO_GOOGLE_ANALYTICS_ENABLED=true` and `DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID=G-...` |

All three are set on the backend. The viewer reads them from the API at boot, so with Helm they
go in `backend.env` only, as in the chart's `examples/values-google-analytics.yaml`.

## Optional features { #optional-features }

Off or bounded by default. Each link goes to the variables.

| Feature | Turn on with |
|---------|--------------|
| Live refresh over WebSocket | [`DEPICTIO_EVENTS_ENABLED`](env-reference.md#real-time-events) |
| What changed since a reader's last visit | [`DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED`](env-reference.md#dashboard-versions) |
| Background ingestion and the `/jobs` API | [`DEPICTIO_JOBS_ENABLED`](env-reference.md#jobs), then [`DEPICTIO_INGESTION_*`](env-reference.md#ingestion) |
| Reading `https://` and `s3://` sources | [`DEPICTIO_REMOTE_*`](env-reference.md#remote-data-sources) |
| Exporting and embedding a component | [`DEPICTIO_FASTAPI_EMBED_ENABLED`](env-reference.md#component-export) |
| Remote genome browser tracks | [`DEPICTIO_JBROWSE_*`](env-reference.md#genome-browser) |
| Protein structures from AlphaFold DB and ESMFold | [`DEPICTIO_STRUCTURE_RESOLVER_ENABLED`](env-reference.md#structure-resolver) |
| Pushing projects to another instance | [`DEPICTIO_MIGRATION_*`](env-reference.md#project-migration) |
| Comments by viewers | [`DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT`](env-reference.md#comments) |
| A feedback link on every dashboard | [`DEPICTIO_FEEDBACK_*`](env-reference.md#feedback) |
| Your logo, colours and fonts | [`DEPICTIO_BRANDING_*`](env-reference.md#branding) |
| The new-release notice for admins | [`DEPICTIO_VERSION_CHECK_*`](env-reference.md#release-check) |

## Version and development { #development }

```bash
DEPICTIO_VERSION=1.21.0       # image tag; unset uses the release the compose file pins, `next` follows main
DEPICTIO_DEV_MODE=true        # API reload, worker restart on code change, no telemetry or walkthrough
```

`DEPICTIO_DEV_MODE` is not a security switch: since v1.5.2 it no longer touches OAuth state
validation. See [Security](../features/security.md#oauth-callback-security). Keep
`DEPICTIO_MONGODB_WIPE` and `DEPICTIO_ENABLE_DEV_ENDPOINTS` off outside development.

## Security checklist { #security }

- Keep `.env` and Helm secrets out of version control; supply them from a secret store.
- Turn single-user mode off on anything others can reach, and put a TLS proxy in front.
- Back up the keys folder with the database: without `secrets_key.bin`, stored project credentials
  cannot be read.
- Keep backups in a bucket apart from the data.
