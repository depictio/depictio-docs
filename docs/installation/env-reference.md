---
title: "Environment Variables Reference"
icon: material/cog-outline
description: "Every Depictio environment variable, grouped by prefix. Synced with settings_models.py at v1.21.0."
---

# Environment Variables Reference

Every environment variable Depictio reads, grouped by prefix. The settings models in
[`settings_models.py`](https://github.com/depictio/depictio/blob/main/depictio/api/v1/configs/settings_models.py)
are the source of truth; the few variables read elsewhere (start scripts, Compose) are listed with
their section. For what to set first, see the [Configuration guide](configuration.md).

Values are strings in the environment. A list accepts a JSON list, and a comma-separated string where
the description says so. With Docker Compose they go in `.env`; with Helm, in `backend.env`
(secrets under `secrets.*`).

## Sections

| Prefix | Section |
|--------|---------|
| `DEPICTIO_FASTAPI_` | [FastAPI Backend](#fastapi-backend), [Component export](#component-export) |
| `DEPICTIO_VIEWER_` | [React Viewer Frontend](#react-viewer-frontend) |
| `DEPICTIO_MONGODB_` | [MongoDB Database](#mongodb-database) |
| `DEPICTIO_S3_` | [S3 Storage](#s3-storage), [S3 File Cache](#s3-file-cache) |
| `DEPICTIO_REMOTE_`, `DEPICTIO_LOCAL_DATA_` | [Remote Data Sources](#remote-data-sources), [Local data folders](#local-data-folders) |
| `DEPICTIO_AUTH_` | [Authentication](#authentication) |
| `DEPICTIO_BOOTSTRAP_` | [Bootstrap](#bootstrap) |
| `DEPICTIO_CACHE_` | [Redis Cache](#redis-cache) |
| `DEPICTIO_CELERY_` | [Celery Task Queue](#celery-task-queue) |
| `DEPICTIO_EVENTS_` | [Real-time Events](#real-time-events) |
| `DEPICTIO_PERFORMANCE_` | [Performance & Timeouts](#performance-timeouts) |
| `DEPICTIO_BACKUP_` | [Backup & Restore](#backup-restore) |
| `DEPICTIO_MIGRATION_` | [Project Migration](#project-migration) |
| `DEPICTIO_ANALYTICS_`, `DEPICTIO_GOOGLE_ANALYTICS_` | [Internal Analytics](#internal-analytics), [Google Analytics](#google-analytics) |
| `DEPICTIO_LOGGING_`, `DEPICTIO_MONITORING_` | [Logging](#logging), [Monitoring](#monitoring) |
| `DEPICTIO_DASHBOARD_VERSIONS_`, `DEPICTIO_COMMENTS_` | [Dashboard Versions](#dashboard-versions), [Comments](#comments) |
| `DEPICTIO_INGESTION_`, `DEPICTIO_JOBS_` | [Ingestion](#ingestion), [Jobs](#jobs) |
| `DEPICTIO_JBROWSE_`, `DEPICTIO_STRUCTURE_RESOLVER_`, `DEPICTIO_MULTIQC_` | [Genome Browser](#genome-browser), [Structure Resolver](#structure-resolver), [MultiQC Prerender](#multiqc-prerender) |
| `DEPICTIO_TELEMETRY_`, `DEPICTIO_VERSION_CHECK_` | [Telemetry](#telemetry), [Release Check](#release-check) |
| `DEPICTIO_BRANDING_`, `DEPICTIO_FEEDBACK_` | [Branding](#branding), [Feedback](#feedback) |
| `DEPICTIO_` | [Global Settings](#global-settings), [Compose and image variables](#compose-and-image-variables) |

---

## FastAPI Backend

**Config Class:** `FastAPIConfig`
**Environment Prefix:** `DEPICTIO_FASTAPI_`

The API server. Each service section (FastAPI, Viewer, MongoDB, S3) shares the same address fields:
`SERVICE_NAME` and `SERVICE_PORT` are the in-network address other containers use, `EXTERNAL_HOST`,
`EXTERNAL_PORT` and `EXTERNAL_PROTOCOL` build the address browsers and the CLI use, and `PUBLIC_URL`
overrides that address (a reverse proxy or CDN).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_FASTAPI_SERVICE_NAME` | `depictio-backend` | Host name inside the Compose network |
| `DEPICTIO_FASTAPI_SERVICE_PORT` | `8058` | Port inside the network |
| `DEPICTIO_FASTAPI_EXTERNAL_HOST` | `localhost` | Host name for external access |
| `DEPICTIO_FASTAPI_EXTERNAL_PORT` | `8058` | Port for external access |
| `DEPICTIO_FASTAPI_EXTERNAL_PROTOCOL` | `http` | `http` or `https` |
| `DEPICTIO_FASTAPI_PUBLIC_URL` | - | Public URL of the API, overriding the three above |
| `DEPICTIO_FASTAPI_EXTERNAL_SERVICE` | `false` | `true` when the API runs outside the Compose network |
| `DEPICTIO_FASTAPI_HOST` | `0.0.0.0` | Bind address of Gunicorn, read by the image's start script |
| `DEPICTIO_FASTAPI_PORT` | `8058` | Bind port, read by the start script only |
| `DEPICTIO_FASTAPI_WORKERS` | `4` | Gunicorn worker processes |
| `DEPICTIO_FASTAPI_CORS_ALLOWED_ORIGINS` | _(empty)_ | Allowed CORS origins, comma-separated (e.g. `https://app.example.com,https://example.com`). Empty disables credentialed cross-origin requests. Wildcard `*` is rejected when used with credentials. |
| `DEPICTIO_FASTAPI_CORS_ALLOW_CREDENTIALS` | `true` | Whether the CORS layer attaches credentials (cookies / Authorization header). |

### Component export <small>(v1.17.0+)</small> { #component-export }

The API that serves one dashboard component to another website. See [Component export and embedding](../features/component-export.md).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_FASTAPI_EMBED_ENABLED` | `false` | Serve `/depictio/api/v1/export` and show **Export / embed** on the tiles. Off, every export route answers `404` |
| `DEPICTIO_FASTAPI_EMBED_ALLOWED_ORIGINS` | _(empty)_ | Sites allowed to frame an exported page, comma-separated. They become its CSP `frame-ancestors`. Empty: the pages open on their own but cannot be framed. `*` is refused |
| `DEPICTIO_FASTAPI_EMBED_CSP_UNSAFE_INLINE` | `false` | Allow inline scripts in the exported page instead of listing their hashes |

---

## React Viewer Frontend

**Config Class:** `ViewerConfig`
**Environment Prefix:** `DEPICTIO_VIEWER_`

The React app, served by nginx. The API reads these settings and hands them to the browser at boot,
so they are set on the **backend**, not on the viewer container.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_VIEWER_SERVICE_NAME` | `depictio-viewer` | Host name inside the Compose network |
| `DEPICTIO_VIEWER_SERVICE_PORT` | `80` | Port inside the network |
| `DEPICTIO_VIEWER_EXTERNAL_HOST` | `localhost` | Host name for external access |
| `DEPICTIO_VIEWER_EXTERNAL_PORT` | `5080` | Host-side port mapped to the viewer container |
| `DEPICTIO_VIEWER_EXTERNAL_PROTOCOL` | `http` | `http` or `https` |
| `DEPICTIO_VIEWER_PUBLIC_URL` | - | Public URL of the viewer, where magic links and the [OpenID Connect](sso/index.md) hand-off land |
| `DEPICTIO_VIEWER_EXTERNAL_SERVICE` | `false` | `true` when the viewer runs outside the Compose network |
| `DEPICTIO_VIEWER_INSPECTOR_ENABLED` | `false` | Docked component inspector, replacing the per-component popovers for advanced-visualisation controls, notes and metadata. Experimental (v1.4.0+) |
| `DEPICTIO_VIEWER_DASHBOARDS_DEFAULT_VIEW` | `table` | View `/dashboards` opens in for someone who never picked one: `thumbnails` or `table`. A view chosen in the browser, or named by a shared link, wins (v1.11.2+; the default was `thumbnails` until v1.12.0) |
| `DEPICTIO_VIEWER_CODE_FIGURES_LOCKED` | `false` | Refuse new figure code from non-admin users. Existing code figures still render. See [Security](../features/security.md#figure-code-lock) (v1.21.0+) |

---

## MongoDB Database

**Config Class:** `MongoDBConfig`
**Environment Prefix:** `DEPICTIO_MONGODB_`

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MONGODB_SERVICE_NAME` | `mongo` | Host name inside the network |
| `DEPICTIO_MONGODB_SERVICE_PORT` | `27018` | Port inside the network |
| `DEPICTIO_MONGODB_EXTERNAL_HOST` | `localhost` | Host name for external access |
| `DEPICTIO_MONGODB_EXTERNAL_PORT` | `27018` | Port for external access |
| `DEPICTIO_MONGODB_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_MONGODB_PUBLIC_URL` | - | Overrides the external address |
| `DEPICTIO_MONGODB_EXTERNAL_SERVICE` | `false` | `true` for a MongoDB outside the Compose network |
| `DEPICTIO_MONGODB_DB_NAME` | `depictioDB` | Database name |
| `DEPICTIO_MONGODB_WIPE` | `false` | Drop the database on startup. Development only, and it also turns telemetry off |
| `DEPICTIO_MONGODB_USERNAME` | - | Username, for operator-managed replica-set auth |
| `DEPICTIO_MONGODB_PASSWORD` | - | Password, for operator-managed replica-set auth |
| `DEPICTIO_MONGODB_REPLICA_SET` | - | Replica set name, e.g. `rs0` |
| `DEPICTIO_MONGODB_AUTH_SOURCE` | `admin` | Authentication source database |

---

<a id="minios3-storage"></a>

## S3 Storage { #s3-storage }

**Config Class:** `S3DepictioCLIConfig`
**Environment Prefix:** `DEPICTIO_S3_` (legacy `DEPICTIO_MINIO_`)

S3-compatible object storage: the bundled SeaweedFS store (Compose service `s3`),
or any external S3 endpoint (AWS, NetApp, Ceph, MinIO, …) set with
`DEPICTIO_S3_PUBLIC_URL` and `DEPICTIO_S3_EXTERNAL_SERVICE=true`.

!!! info "`DEPICTIO_MINIO_*` became `DEPICTIO_S3_*` in v1.12.0"
    The bundled store is SeaweedFS instead of MinIO since **v1.12.0**, and these
    settings were renamed with it. The former `DEPICTIO_MINIO_<FIELD>` names still
    work: each is read when its `DEPICTIO_S3_<FIELD>` counterpart is unset, the new
    name wins when both are set, and the server logs a deprecation warning naming
    the old variables it found. An install that used the bundled MinIO has to copy
    its data to the new store: see
    [Upgrading to v1.12.0: MinIO → SeaweedFS](upgrade/v1.12.0-seaweedfs.md).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_S3_SERVICE_NAME` | `s3` | Host name of the store inside the Compose network (`minio` before v1.12.0, still an alias of the `s3` service) |
| `DEPICTIO_S3_SERVICE_PORT` | `9000` | - |
| `DEPICTIO_S3_EXTERNAL_HOST` | `localhost` | - |
| `DEPICTIO_S3_EXTERNAL_PORT` | `9000` | - |
| `DEPICTIO_S3_EXTERNAL_PROTOCOL` | `http` | - |
| `DEPICTIO_S3_PUBLIC_URL` | - | Full endpoint URL of an external S3 |
| `DEPICTIO_S3_EXTERNAL_SERVICE` | `false` | `true` when the store is outside the Docker Compose network |
| `DEPICTIO_S3_ROOT_USER` | `minio` | S3 access key |
| `DEPICTIO_S3_ROOT_PASSWORD` | _(empty)_ | S3 secret key. Outside single-user mode the server refuses to start unless it has at least 8 characters and is not a well-known default (`minio123`, `changeme`, ...) |
| `DEPICTIO_S3_BUCKET` | `depictio-bucket` | - |
| `DEPICTIO_S3_VERIFY_TLS` | `true` | Verify TLS certificates when connecting to S3. Set to `false` only for local dev with self-signed certificates. |
| `DEPICTIO_S3_BROWSER_ACCESS` <small>(v1.22.0+)</small> | `presigned` | How browsers read [indexed files](#s3-browser-access) (3D structures, GenomeSpy VCF/BAM/bigWig tracks): `presigned` or `proxy`. The Helm chart sets it, see [`s3.browserAccess`](kubernetes.md#s3-browser-access) |

### Browser access to indexed files <small>(v1.22.0+)</small> { #s3-browser-access }

The 3D structure viewer and GenomeSpy's file-backed tracks read their files from the
browser, by HTTP range request.

- **`presigned`** (default): the API hands out URLs signed for the S3 public endpoint
  (`DEPICTIO_S3_PUBLIC_URL`, or the `EXTERNAL_*` host and port), and the browser reads S3
  directly. S3 must be reachable from the reader's browser, with CORS allowing `Range`.
- **`proxy`**: the API hands out its own URLs,
  `GET|HEAD /depictio/api/v1/files/indexed/{dc_id}/object/{sample}/{name}`, and streams
  each object by byte range. Each URL is signed for one object and one user and lives
  15 minutes; the reader's access is checked again on every request. No CORS or CSP entry
  for S3 is needed.

Use `proxy` when browsers cannot reach S3: an IP-only install where S3 stays on the Compose
network, a Serve app, a store with no public route. The symptom in `presigned` mode is a
structure or track that fails with *Failed to fetch* while tables and figures load.

### Required S3 permissions

At startup the server checks that the configured bucket is usable. Since
**v1.5.2** those checks are scoped to that single bucket: `HeadBucket`, then a
put/delete round trip on a test object.

A credential that can only reach `DEPICTIO_S3_BUCKET` is therefore enough,
which is useful on managed S3 where keys are issued per bucket rather than per
account.

Since **v1.6.0** the server creates the bucket before running those checks, so
**you do not have to provision it first**: pointing a fresh deployment at empty
object storage is enough. A bucket that already exists is left alone: creation
short-circuits and no `CreateBucket` call is made, so a credential issued
against an existing bucket needs no extra permission.

!!! note "Account-wide `ListBuckets` is no longer required"
    Before v1.5.2 the check called `ListBuckets`, an account-level operation.
    Bucket-scoped credentials got `AccessDenied` and the server refused to start,
    even though the bucket itself was perfectly usable.

!!! note "Before v1.6.0, a first boot against empty storage failed"
    The checks ran before the line that creates the bucket, so a deployment with
    nothing provisioned ahead of it died during startup with *"Bucket
    'depictio-bucket' does not exist"*. Genuinely broken storage still refuses to
    start, since the checks now simply follow creation.

---

## Remote Data Sources <small>(v1.16.0+)</small> { #remote-data-sources }

**Config Class:** `RemoteConfig`
**Environment Prefix:** `DEPICTIO_REMOTE_`

Policy for reading user-supplied locations: the gateway that fetches `https://`
URLs (the `url` and `manifest` scan modes, manifest downloads, the endpoint
gating of per-project storage credentials), and which `s3://` buckets the
server may read without the project's storage settings. The section is read
from the environment on every read, so the API and the Celery worker apply the
same policy, and a malformed value fails at the first read instead of silently
falling back to a default. The run-folder browser then offers no S3 location,
and the server log says why. See
[Remote data and manifests](../usage/projects/remote-data.md#reading-s3-buckets)
and [Security](../features/security.md#remote-data-sources).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_REMOTE_ALLOW_HTTP` | `false` | Accept plain `http://` URLs in addition to `https://` and `s3://`. Off by default: the gateway and the models reject `http://` locations. Turn on for local or airgapped deployments that serve data without TLS |
| `DEPICTIO_REMOTE_URL_ALLOWLIST` | _(empty)_ | Comma-separated host names the gateway may fetch from. **Exclusive while set**: any host not listed is rejected, and a listed host skips the private/loopback address rejection, which is how internal deployments opt an intranet host in. Empty accepts every public host |
| `DEPICTIO_REMOTE_URL_DENYLIST` | _(empty)_ | Comma-separated host names the gateway always rejects. Checked before the allowlist, so a host present in both lists is denied |
| `DEPICTIO_REMOTE_PUBLIC_S3_BUCKETS` | _(empty)_ | Comma-separated S3 locations read without credentials, each `bucket` or `bucket/prefix`, on Amazon S3. Unsigned access is opt-in: any other `s3://` location needs the project's storage settings, read unsigned too when they hold no key, or an entry in the next list |
| `DEPICTIO_REMOTE_CREDENTIALED_S3_BUCKETS` | _(empty)_ | Comma-separated S3 locations, same syntax, that the API and the worker read with their own ambient credentials (the AWS default chain: environment, IAM role, web identity). Every user of the instance can read what is listed here. Not used by the CLI |
| `DEPICTIO_REMOTE_MAX_DOWNLOAD_BYTES` | `524288000` (500 MiB) | Size cap in bytes for a single remote download: a data file, a manifest the CLI reads, a MultiQC report. Downloads stream and abort, removing the partial file, once the cap is exceeded. The server reads a manifest up to 50 MiB, or this cap when it is lower |
| `DEPICTIO_REMOTE_TIMEOUT_S` | `30.0` | Timeout in seconds applied to each connect, read and write operation of a remote fetch, not a total download time. Also the connect and read timeouts of the S3 client that reads a user-supplied `s3://` location |
| `DEPICTIO_REMOTE_MAX_REDIRECTS` | `3` | Maximum redirect hops followed for a remote URL. Every `Location` is re-validated against this policy before it is followed |

!!! warning "A listed host bypasses the private-address check"
    Setting `DEPICTIO_REMOTE_URL_ALLOWLIST` both restricts fetches to the listed
    hosts and exempts those hosts from the private-range rejection. List only
    hosts you control.

The backend and the Celery worker must agree on these variables:

| Deployment | Where to set them |
|------------|-------------------|
| Kubernetes | `backend.env` in the Helm values, rendered for both the backend and the Celery worker |
| Docker Compose | `.env`, passed to both the backend and the worker |
| Python package | The shell that runs `depictio local up`, which passes `DEPICTIO_REMOTE_*` on to the server, but not `AWS_*`: see [`depictio local`](local.md) |

### Local data folders <small>(v1.16.0+)</small> { #local-data-folders }

**Config Class:** `LocalDataConfig`
**Environment Prefix:** `DEPICTIO_LOCAL_DATA_`

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_LOCAL_DATA_ROOTS` | _(empty)_ | Comma-separated absolute folders (or `~/...`) the web UI may read run folders from. Empty turns local folders off. Honoured only with `DEPICTIO_AUTH_SINGLE_USER_MODE`; hidden folders and the folders Depictio keeps for itself are never read |

`depictio local up` sets it to your home folder plus each
[`--data-root-allow`](local.md#up-options) folder; there is no need to set it
by hand. See [From a run folder](../usage/projects/remote-data.md#from-a-run-folder).

---

## Authentication

**Config Class:** `AuthConfig`
**Environment Prefix:** `DEPICTIO_AUTH_`

Keys, sign-in modes and OpenID Connect single sign-on. The modes are compared in
[Authentication Modes](../usage/guides/authentication-modes.md).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_AUTH_KEYS_DIR` | `/app/depictio/keys` | Directory for JWT public/private key files (`depictio/keys` in the package outside the images). Also holds `secrets_key.bin`, the key that encrypts per-project storage credentials at rest; the backend and the Celery worker must mount the same directory, or secrets written by one are unreadable by the other |
| `DEPICTIO_AUTH_KEYS_ALGORITHM` | `RS256` | JWT signing algorithm: `RS256`, `RS512`, `ES256` or `SHA256` |
| `DEPICTIO_AUTH_CLI_CONFIG_DIR` | `/app/depictio/.depictio` | Directory for CLI configuration files (admin token, etc.) |
| `DEPICTIO_AUTH_INTERNAL_API_KEY` | _(auto-generated)_ | Internal API key for service-to-service calls. Also accepted as `DEPICTIO_AUTH_INTERNAL_API_KEY_ENV` |
| `DEPICTIO_AUTH_SINGLE_USER_MODE` | `false` | Single-user mode: no login, the anonymous user is an admin, and no secret is enforced at startup. **The root `docker-compose.yaml` sets it to `true` unless you set `false`**; the Helm chart leaves it `false` |
| `DEPICTIO_AUTH_PUBLIC_MODE` | `false` | Public mode: anonymous read-only access with optional sign-in |
| `DEPICTIO_AUTH_UNAUTHENTICATED_MODE` | `false` | Former name of `DEPICTIO_AUTH_PUBLIC_MODE`, still read as an alias |
| `DEPICTIO_AUTH_DEMO_MODE` | `false` | Demo mode: public mode with the guest [tour](../usage/guides/web_ui.md#guided-tours) of the dashboards list, guests never offered sign-in, and no landing card introducing a dashboard |
| `DEPICTIO_AUTH_PUBLIC_ACCESS_CODE` | - | Shared code a visitor enters before public mode hands out a temporary session. Ignored outside public and demo mode. With Helm, set `secrets.publicAccessCode`. See [Public-mode access code](../usage/guides/authentication-modes.md#public-access-code) |
| `DEPICTIO_AUTH_ANONYMOUS_USER_EMAIL` | `anonymous@depict.io` | Default anonymous user email |
| `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS` | `24` | Number of hours until temporary users expire |
| `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_MINUTES` | `0` | Number of minutes until temporary users expire |
| `DEPICTIO_AUTH_OIDC_PROVIDERS` | _(empty)_ | JSON list of OpenID Connect providers (Keycloak, Google, Authentik, ...). Keys: `id`, `label`, `enabled`, `issuer`, `discovery_url`, `client_id`, `client_secret`, `scopes`, `redirect_uri`, `claims`, `sso_provider`, `assume_email_verified`, `token_endpoint_auth_method`, `authorize_params`, `fetch_userinfo`. See [Single sign-on (OpenID Connect)](sso/configuration.md#provider-keys) |
| `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_ID` | - | Client id of the provider whose `id` is `<ID>` (upper case, `-` as `_`). Overrides `client_id` in `DEPICTIO_AUTH_OIDC_PROVIDERS` |
| `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_SECRET` | - | Client secret of that provider. Overrides `client_secret`; use it from a secret store |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED` | `false` | **Deprecated**, still works for one release: mapped to an OIDC provider with id `google`. See [From Google OAuth to OIDC](sso/migration.md#from-google-oauth-to-oidc) |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID` | - | **Deprecated**: use `DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID` |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET` | - | **Deprecated**: use `DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET` |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_REDIRECT_URI` | - | **Deprecated**: the `redirect_uri` of the `google` provider |
| `DEPICTIO_AUTH_REGISTRATION_DISABLED` | `false` | Block self-service registration: `/register` returns 403 and the Register UI is hidden, so only pre-provisioned accounts can log in. Independent of public/single-user mode |
| `DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED` | `false` | Close email and password sign-in so SSO is the only way in. Ignored unless at least one OIDC provider is enabled and configured. See [Password sign-in](../usage/guides/authentication-modes.md#password-login) |
| `DEPICTIO_AUTH_PROVISIONING_API_KEY` | - | Shared secret for pipeline-side user provisioning (`POST /auth/provision_user`). Scoped to provisioning only, kept separate from the internal API key. Also accepted as `DEPICTIO_AUTH_PROVISIONING_API_KEY_ENV`. **The provisioning endpoints are disabled while this is unset.** See [Pipeline provisioning](../usage/guides/authentication-modes.md#pipeline-provisioning-and-magic-links-v113) |
| `DEPICTIO_AUTH_MAGIC_LINK_EXPIRY_MINUTES` | `15` | Lifetime of a single-use magic-link login ticket |

!!! warning "`DEPICTIO_AUTH_SAML_*` was removed"
    SAML sign-in is gone. A server that still finds `DEPICTIO_AUTH_SAML_*` variables ignores them
    and logs an error naming the OpenID Connect key that replaces each one. See
    [Single sign-on (OpenID Connect)](sso/index.md).

---

## Bootstrap

**Config Class:** `AuthBootstrapConfig`
**Environment Prefix:** `DEPICTIO_BOOTSTRAP_`

First-boot admin seeding. Idempotent: the admin is created only when MongoDB holds none, so a
password changed in the UI survives restarts and Helm wipe jobs. Single-user mode seeds its own
local admin and needs neither. With Helm, set `secrets.bootstrapAdminEmail` and
`secrets.bootstrapAdminPassword`.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` | _(empty)_ | Email of the first admin. When MongoDB holds no admin and this or the password is unset, the server stops at startup |
| `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD` | _(empty)_ | Password of the first admin: at least 8 characters, and not a well-known default such as `admin` or `password`. Not needed with `DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED`, where the email alone names the SSO account that owns the instance |
| `DEPICTIO_BOOTSTRAP_SEED_TEST_USER` | `false` | Seed a non-admin test user for CI/Cypress fixtures. Leave `false` in production. |
| `DEPICTIO_BOOTSTRAP_TEST_USER_EMAIL` | `test_user@example.com` | Email for the CI test user (only when `seed_test_user=true`). |
| `DEPICTIO_BOOTSTRAP_TEST_USER_PASSWORD` | `test_pwd` | Password for the CI test user (only when `seed_test_user=true`). |

---

## Redis Cache

**Config Class:** `CacheConfig`
**Environment Prefix:** `DEPICTIO_CACHE_`

Redis cache configuration settings.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CACHE_REDIS_HOST` | `redis` | Redis server hostname |
| `DEPICTIO_CACHE_REDIS_PORT` | `6379` | Redis server port |
| `DEPICTIO_CACHE_REDIS_PASSWORD` | - | Redis password |
| `DEPICTIO_CACHE_REDIS_DB` | `0` | Redis database number |
| `DEPICTIO_CACHE_REDIS_SSL` | `false` | Use SSL for Redis connection |
| `DEPICTIO_CACHE_ENABLE_REDIS_CACHE` | `true` | Enable Redis caching for DataFrames |
| `DEPICTIO_CACHE_DEFAULT_TTL` | `3600` | Default cache TTL in seconds (1 hour) |
| `DEPICTIO_CACHE_DATAFRAME_TTL` | `1800` | DataFrame cache TTL in seconds (30 minutes) |
| `DEPICTIO_CACHE_MAX_DATAFRAME_SIZE_MB` | `100` | Maximum DataFrame size to cache (MB) |
| `DEPICTIO_CACHE_REDIS_MAX_MEMORY_MB` | `1024` | **Not enforced.** Declared but never applied to the Redis server; see the note below. |
| `DEPICTIO_CACHE_CACHE_KEY_PREFIX` | `depictio:df:` | Prefix for cache keys |

!!! warning "Cap Redis on the server, not through Depictio"
    `DEPICTIO_CACHE_REDIS_MAX_MEMORY_MB` is read into settings and then never applied:
    Depictio issues no `CONFIG SET`, so setting it leaves Redis **uncapped**. A cache that
    grows until the container's memory limit kills it takes the Celery broker down with it
    when both share one Redis, which fails every figure offload until it recovers.

    Set the limit on Redis itself instead, and give it an eviction policy:

    ```bash
    redis-server --maxmemory 1500mb --maxmemory-policy volatile-lru
    ```

    `volatile-lru` rather than `allkeys-lru` because the policy is server-wide: cache
    entries are written with a TTL and broker keys are not, so only the cache is evicted.

---

## Celery Task Queue

**Config Class:** `CeleryConfig`
**Environment Prefix:** `DEPICTIO_CELERY_`

The Celery worker renders figure previews, large dashboard renders, screenshots and, with the
[ingestion worker](docker.md#ingestion-worker), offloaded ingestion. It always runs: the dashboard
editor needs it.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CELERY_BROKER_HOST` | `redis` | Redis broker hostname |
| `DEPICTIO_CELERY_BROKER_PORT` | `6379` | Redis broker port |
| `DEPICTIO_CELERY_BROKER_PASSWORD` | - | Redis broker password |
| `DEPICTIO_CELERY_BROKER_DB` | `1` | Redis database for Celery broker |
| `DEPICTIO_CELERY_RESULT_BACKEND_HOST` | `redis` | Redis result backend hostname |
| `DEPICTIO_CELERY_RESULT_BACKEND_PORT` | `6379` | Redis result backend port |
| `DEPICTIO_CELERY_RESULT_BACKEND_PASSWORD` | - | Redis result backend password |
| `DEPICTIO_CELERY_RESULT_BACKEND_DB` | `2` | Redis database for Celery results |
| `DEPICTIO_CELERY_RESULT_EXPIRES` | `3600` | Task result lifetime in seconds. Celery keeps at least 86400 whatever the value |
| `DEPICTIO_CELERY_INGESTION_QUEUE` | `ingestion` | Queue of the offloaded ingestion tasks, read by the [ingestion worker](docker.md#ingestion-worker) (v1.15.0+) |
| `DEPICTIO_CELERY_OFFLOAD_PREVIEW` | `true` | Offload component-design preview endpoints (`/figure/preview`, etc.) to Celery |
| `DEPICTIO_CELERY_OFFLOAD_RENDERING` | `false` | Force-offload *all* dashboard render endpoints (`/dashboards/render_*`) to Celery. Off by default: renders offload adaptively by size instead |
| `DEPICTIO_CELERY_OFFLOAD_SIZE_THRESHOLD_BYTES` | `52428800` (50 MB) | Source Delta-table size at/above which a render is offloaded even when `OFFLOAD_RENDERING` is off. `0` disables size-based offload |
| `DEPICTIO_CELERY_OFFLOAD_TIMEOUT_SECONDS` | `30.0` | Per-request Celery offload timeout in seconds before HTTP 504 |

### Worker processes { #celery-worker-processes }

The worker image's start script reads these, so set them on the **worker** container
(`celery.env` with Helm). Each container is sized on its own.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CELERY_WORKERS` | `4` | Worker processes (`--concurrency`). Each one holds its own DataFrames, so size it to the host's memory. The Helm chart sets `2` |
| `DEPICTIO_CELERY_MAX_TASKS_PER_CHILD` | `50` | Tasks a process runs before it is replaced, which returns its memory |
| `DEPICTIO_CELERY_PREFETCH` | `1` | Tasks a process reserves ahead |
| `DEPICTIO_CELERY_QUEUES` | `celery` | Queues the worker reads. The ingestion worker sets `ingestion` |
| `DEPICTIO_CELERY_NODENAME` | `celery@%h` | Node name, so health checks reach one worker |
| `DEPICTIO_INGESTION_WORKER_CONCURRENCY` | `2` | Compose only: `DEPICTIO_CELERY_WORKERS` of the ingestion worker |

`DEPICTIO_CELERY_WORKER_CONCURRENCY`, `_WORKER_POOL`, `_WORKER_PREFETCH_MULTIPLIER`,
`_WORKER_MAX_TASKS_PER_CHILD`, `_TASK_SOFT_TIME_LIMIT`, `_TASK_TIME_LIMIT`, `_DEFAULT_QUEUE`,
`_WORKER_SEND_TASK_EVENTS` and `_TASK_SEND_SENT_EVENT` are declared in the settings but never applied:
the pool is Celery's default `prefork`, each task sets its own time limits, and a task with no route
goes to the `celery` queue. `DEPICTIO_CELERY_ENABLED`, a Dash-era switch, only prints a log line.

---

## Real-time Events

**Config Class:** `EventsConfig`
**Environment Prefix:** `DEPICTIO_EVENTS_`

Real-time dashboard events (WebSocket live refresh). Disabled by default: set
`DEPICTIO_EVENTS_ENABLED=true` to turn the system on. Uses Redis pub/sub to fan events out to
connected viewers, so a reachable Redis instance is required when enabled. See
[Real-time Events](../usage/guides/realtime-events.md) for the full setup.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_EVENTS_ENABLED` | `false` | Master switch for the real-time event system |
| `DEPICTIO_EVENTS_REDIS_HOST` | `redis` | Redis hostname for pub/sub |
| `DEPICTIO_EVENTS_REDIS_PORT` | `6379` | Redis port |
| `DEPICTIO_EVENTS_REDIS_PASSWORD` | - | Redis password (optional) |
| `DEPICTIO_EVENTS_REDIS_DB` | `3` | Redis database number (cache=0, celery=1,2) |
| `DEPICTIO_EVENTS_MONGODB_CHANGE_STREAMS_ENABLED` | `true` | Enable MongoDB change streams for data collections (requires a replica set) |
| `DEPICTIO_EVENTS_WS_HEARTBEAT_INTERVAL` | `30` | WebSocket heartbeat/ping interval in seconds |
| `DEPICTIO_EVENTS_WS_CONNECTION_TIMEOUT` | `60` | WebSocket connection timeout in seconds |
| `DEPICTIO_EVENTS_DEBOUNCE_MS` | `1000` | Debounce interval in milliseconds for rapid updates |

!!! note "Dev-only trigger endpoint"
    [`DEPICTIO_ENABLE_DEV_ENDPOINTS`](#global-settings) gates the admin-only
    `/events/test-trigger/{dc_id}` route used to broadcast a test event by hand. Normal refresh
    does not need it: ingestion drives it.

---

## Performance & Timeouts

**Config Class:** `PerformanceConfig`
**Environment Prefix:** `DEPICTIO_PERFORMANCE_`

Dashboard thumbnails, service readiness and render caps. Times are in milliseconds unless the name
ends in a unit or says otherwise.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_PERFORMANCE_BROWSER_NAVIGATION_TIMEOUT` | `60000` | Headless browser navigation timeout |
| `DEPICTIO_PERFORMANCE_BROWSER_PAGE_LOAD_TIMEOUT` | `90000` | Headless browser page load timeout |
| `DEPICTIO_PERFORMANCE_SCREENSHOTS_ENABLED` | `true` | Generate dashboard thumbnails with Playwright. `depictio local up` sets it to `false` unless `--screenshots` is passed |
| `DEPICTIO_PERFORMANCE_SCREENSHOTS_DIR` | package's `api/static/screenshots` | Where thumbnails are written and served from. At startup, thumbnails of dashboards absent from the database are deleted from it |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_NAVIGATION_TIMEOUT` | `60000` | Time to open the dashboard before a capture |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_CONTENT_WAIT` | `30000` | Time to wait for the components to render |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_STABILIZATION_WAIT` | `10000` | Time to let the layout settle |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_CAPTURE_TIMEOUT` | `120000` | Whole capture timeout |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_VIEWPORT_WIDTH` | `1440` | Width of the page a dashboard thumbnail is captured from, in CSS pixels (v1.11.2+) |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_VIEWPORT_HEIGHT` | `900` | Height of that page, in CSS pixels (v1.11.2+) |
| `DEPICTIO_PERFORMANCE_SCREENSHOT_SCALE` | `2.0` | Pixel density of the capture, from `1.0` to `3.0`. Each capture also writes an `@2x` file for the hover preview (v1.11.2+) |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_RETRIES` | `5` | Attempts to reach a service before the screenshot job gives up |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_DELAY` | `3` | Seconds between those attempts |
| `DEPICTIO_PERFORMANCE_SERVICE_READINESS_TIMEOUT` | `10` | Seconds per attempt |

### Render caps

Bound how many rows a single figure, table or advanced-viz render materialises, so large
data collections stay responsive. See [Performance & Scaling](../features/performance.md)
for what each cap does to the rendered result.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_PERFORMANCE_FIGURE_MAX_POINTS` | `10000` | Target marker count for point plots (scatter family). Above it the figure is downsampled before serialising to Plotly. A per-component `max_points` overrides this |
| `DEPICTIO_PERFORMANCE_FIGURE_MAX_LOAD_ROWS` | `500000` | Row ceiling loaded from Delta for a point-plot / code-mode figure. Bypassed when the client requests a full load |
| `DEPICTIO_PERFORMANCE_TABLE_SORT_MAX_ROWS` | `1000000` | Post-filter row count above which a table is served in natural scan order instead of sorted; the response reports `sort_disabled` so the grid drops the sort affordance. `0` disables the gate |
| `DEPICTIO_PERFORMANCE_ADVANCED_VIZ_NO_SAMPLE_MAX_ROWS` | `2000000` | Row ceiling for the advanced-viz kinds that must not be sampled. Past it the request falls back to a uniform sample and the chart is marked estimated. `0` disables the ceiling |
| `DEPICTIO_PERFORMANCE_ADVANCED_VIZ_TAIL_P_THRESHOLD` | `0.05` | Significance cutoff below which a volcano/Manhattan row is kept whole rather than sampled. Fallback only, since a renderer's own threshold wins |
| `DEPICTIO_PERFORMANCE_ADVANCED_VIZ_TAIL_EFFECT_THRESHOLD` | `1.0` | Same, for kinds whose tail is a signed effect size (MA's log2 fold change) |
| `DEPICTIO_PERFORMANCE_BOX_SAMPLE_ROWS_PER_GROUP` | `0` | Rows sampled per box-plot group before computing quartiles; `0` computes them exactly. Trades a sort for an extra scan, so see the tuning notes |
| `DEPICTIO_PERFORMANCE_BOX_SAMPLE_MAX_GROUPS` | `64` | Group-count ceiling above which box quartiles are always computed exactly (grouped quantiles get cheaper as cardinality rises) |

---

## Backup & Restore

**Config Class:** `BackupConfig`
**Environment Prefix:** `DEPICTIO_BACKUP_`

MongoDB backups, their schedule and retention, and the copy of S3 data. See
[Backup & Restore](../usage/administration/backup.md).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_BACKUP_BASE_DIR` | `/app/depictio` | Folder the two backup directories below are relative to (the `depictio` package folder outside the images) |
| `DEPICTIO_BACKUP_BACKUP_DIR` | `backups` | MongoDB backup directory, under `BASE_DIR` |
| `DEPICTIO_BACKUP_AUTO_BACKUP_ENABLED` | `false` | Run scheduled MongoDB backups |
| `DEPICTIO_BACKUP_AUTO_BACKUP_INTERVAL_HOURS` | `24` | Hours between scheduled backups, at least 1 |
| `DEPICTIO_BACKUP_AUTO_BACKUP_TIME_OF_DAY` | - | `HH:MM` in UTC that anchors the schedule, e.g. `03:00`. Unset: due whenever an interval has passed |
| `DEPICTIO_BACKUP_BACKUP_FILE_RETENTION_DAYS` | `30` | Days every backup is kept. `0` keeps them forever |
| `DEPICTIO_BACKUP_BACKUP_RETENTION_WEEKLY_WEEKS` | `0` | Then one backup per ISO week, for this many weeks. `0` turns the tier off |
| `DEPICTIO_BACKUP_BACKUP_RETENTION_MONTHLY_MONTHS` | `0` | Then one backup per month, for this many months. `0` turns the tier off |
| `DEPICTIO_BACKUP_S3_BACKUP_STRATEGY` | `s3_to_s3` | How S3 data is backed up: `s3_to_s3`, `local` or `both` |
| `DEPICTIO_BACKUP_S3_LOCAL_BACKUP_DIR` | `backups/s3_data_backups` | Local copy of S3 data, under `BASE_DIR` |
| `DEPICTIO_BACKUP_BACKUP_S3_ENABLED` | `false` | Enable separate backup S3 bucket |
| `DEPICTIO_BACKUP_BACKUP_S3_BUCKET` | `depictio-backups` | Backup S3 bucket name |
| `DEPICTIO_BACKUP_BACKUP_S3_ENDPOINT_URL` | - | Backup S3 endpoint URL |
| `DEPICTIO_BACKUP_BACKUP_S3_ACCESS_KEY` | - | Backup S3 access key |
| `DEPICTIO_BACKUP_BACKUP_S3_SECRET_KEY` | - | Backup S3 secret key |
| `DEPICTIO_BACKUP_BACKUP_S3_REGION` | `us-east-1` | Backup S3 region |
| `DEPICTIO_BACKUP_COMPRESS_LOCAL_BACKUPS` | `true` | Compress local S3 data backups |
| `DEPICTIO_BACKUP_MIGRATION_ALLOWED_S3_ENDPOINTS` | _(empty)_ | Comma-separated allowlist of external S3 endpoints permitted for project migration. Empty = only the deployment's own S3 store is allowed (SSRF guard). |

---

## Project Migration <small>(v1.21.0+)</small> { #project-migration }

**Config Class:** `MigrationConfig`
**Environment Prefix:** `DEPICTIO_MIGRATION_`

Pushing a project from one instance to another, with an admin's approval on the receiving side. Both
directions are off until configured. Lists are JSON. With Helm, `TARGETS` and `INBOUND_SOURCES` hold
pairing keys and do not belong in `backend.env`: pass them through a Secret. See
[Send to another instance](../usage/administration/migrate.md#send-to-another-instance).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MIGRATION_UI_ENABLED` | `false` | Show the migration controls (Migrate, **Admin → Migrations**, push targets, the editing lock). Off only hides them; the API follows the settings below. The Helm chart sets `true` |
| `DEPICTIO_MIGRATION_INSTANCE_LABEL` | - | How this instance names itself in bundles |
| `DEPICTIO_MIGRATION_TARGETS` | `[]` | Sending side: instances this one may push to, `[{"name", "url", "pairing_key"}]`. Keys are at least 32 characters. Listed targets may use `http://` and private addresses |
| `DEPICTIO_MIGRATION_ALLOW_UI_TARGETS` | `false` | Let admins add push targets in the UI. Those go through the SSRF guard |
| `DEPICTIO_MIGRATION_UI_TARGET_HOST_ALLOWLIST` | `[]` | Hosts a UI-added target may reach over `http://` or on a private address |
| `DEPICTIO_MIGRATION_DESTINATION_DOMAINS` | `[]` | Sending side: domain suffixes a project owner may publish to with a URL and an invite code. `["*"]` allows any public `https://` host, the Helm default |
| `DEPICTIO_MIGRATION_INBOUND_ENABLED` | `false` | Receiving side: accept pushes from `INBOUND_SOURCES` and from holders of a valid invite code. Off, the inbound routes answer 404. The Helm chart sets `true` |
| `DEPICTIO_MIGRATION_INBOUND_SOURCES` | `[]` | Instances allowed to push here: `[{"name", "pairing_key", "allowed_source_buckets", "max_pending", "max_per_day", "max_bundle_bytes"}]` |
| `DEPICTIO_MIGRATION_LOCK_IMPORTED_DEFAULT` | `true` | Approval publishes the project read-only unless the admin unticks it |
| `DEPICTIO_MIGRATION_INVITE_TTL_DAYS` | `30` | Default lifetime of an invite code |
| `DEPICTIO_MIGRATION_INVITE_MAX_TTL_DAYS` | `365` | Longest lifetime an admin may give one |
| `DEPICTIO_MIGRATION_PENDING_TTL_DAYS` | `14` | Days a received push waits for a decision |
| `DEPICTIO_MIGRATION_INTERRUPTED_AFTER_MINUTES` | `60` | At startup, a push or import idle for longer is marked failed |
| `DEPICTIO_MIGRATION_MAX_BUNDLE_BYTES` | `10737418240` (10 GiB) | Largest bundle accepted |
| `DEPICTIO_MIGRATION_STAGING_PREFIX` | `_migration_staging` | Bucket prefix a received bundle is staged under. One path segment |
| `DEPICTIO_MIGRATION_SPOOL_DIR` | - | Local folder a bundle is built in. Unset: the system temporary folder |
| `DEPICTIO_MIGRATION_HTTP_TIMEOUT_S` | `60.0` | Timeout of a call to the other instance |
| `DEPICTIO_MIGRATION_UPLOAD_TIMEOUT_S` | `1800.0` | How long the sender waits for the answer after sending a bundle |

---

## Internal Analytics

**Config Class:** `AnalyticsConfig`
**Environment Prefix:** `DEPICTIO_ANALYTICS_`

Per-user session tracking, stored in your own MongoDB and served by the admin analytics API. Off by
default, with no page in the UI yet. Separate from [Telemetry](#telemetry).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_ANALYTICS_ENABLED` | `false` | Record sessions and serve the analytics endpoints |
| `DEPICTIO_ANALYTICS_SESSION_TIMEOUT_MINUTES` | `30` | Session timeout in minutes |
| `DEPICTIO_ANALYTICS_CLEANUP_DAYS` | `90` | Days analytics records are kept |
| `DEPICTIO_ANALYTICS_TRACK_ANONYMOUS_USERS` | `true` | Track anonymous sessions too |
| `DEPICTIO_ANALYTICS_CLEANUP_ENABLED` | `true` | Delete records older than `CLEANUP_DAYS` |

---

## Google Analytics

**Config Class:** `GoogleAnalyticsConfig`
**Environment Prefix:** `DEPICTIO_GOOGLE_ANALYTICS_`

Configuration for Google Analytics tracking.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_GOOGLE_ANALYTICS_ENABLED` | `false` | Enable Google Analytics tracking |
| `DEPICTIO_GOOGLE_ANALYTICS_TRACKING_ID` | - | Google Analytics tracking ID (GA4 measurement ID) |

---

## Logging

**Config Class:** `LoggingConfig`
**Environment Prefix:** `DEPICTIO_LOGGING_`

Logging verbosity and output configuration.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_LOGGING_VERBOSITY_LEVEL` | `ERROR` | - |

---

## Genome Browser

**Config Class:** `JBrowseConfig`
**Environment Prefix:** `DEPICTIO_JBROWSE_`

Settings of the embedded [genome browser](../features/genome-browser/index.md) (v1.20.0+). It
runs inside the viewer and reads every track through the API, so there is no separate
server to deploy. Tracks stored in Depictio's own bucket are always served; tracks read in
place from a remote host or bucket must be allow-listed here, see
[Security](../features/security.md#genome-browser-track-access).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_JBROWSE_ENABLED` | `true` | Enable the genome browser component |
| `DEPICTIO_JBROWSE_REMOTE_HTTPS_HOSTS` | `nf-core-awsmegatests.s3-eu-west-1.amazonaws.com` | Comma-separated hostnames the track proxy may read `https://` tracks from (exact match) |
| `DEPICTIO_JBROWSE_REMOTE_S3_BUCKETS` | `nf-core-awsmegatests` | Comma-separated S3 buckets the track proxy may read `s3://` tracks from, with the server's credentials |
| `DEPICTIO_JBROWSE_REMOTE_S3_ENDPOINT_URL` | - | Endpoint for remote `s3://` tracks (default: AWS) |
| `DEPICTIO_JBROWSE_REMOTE_S3_REGION` | `eu-west-1` | Region for remote `s3://` tracks |
| `DEPICTIO_JBROWSE_REMOTE_S3_ACCESS_KEY` | - | Access key for remote `s3://` buckets (anonymous if unset) |
| `DEPICTIO_JBROWSE_REMOTE_S3_SECRET_KEY` | - | Secret key for remote `s3://` buckets |
| `DEPICTIO_JBROWSE_PRESET_ACCESS` | `proxy` | How the browser reads the built-in assemblies' UCSC files: `proxy` (through the API) or `direct` (from hgdownload.soe.ucsc.edu) |
| `DEPICTIO_JBROWSE_UCSC_TRACKS_ENABLED` | `true` | Resolve components' `ucsc_tracks` through the UCSC REST API |
| `DEPICTIO_JBROWSE_UCSC_API_URL` | `https://api.genome.ucsc.edu` | UCSC REST API the UCSC track catalogue is read from |
| `DEPICTIO_JBROWSE_UCSC_CATALOG_TTL_S` | `86400` | How long a genome's UCSC track catalogue is cached in the API process (at least 60) |
| `DEPICTIO_JBROWSE_REMOTE_TIMEOUT_S` | `30.0` | Remote read timeout, in seconds |
| `DEPICTIO_JBROWSE_MAX_RANGE_MB` | `64` | Largest byte range served in one request |
| `DEPICTIO_JBROWSE_MAX_FULL_READ_MB` | `256` | Largest file served whole when the browser sends no Range header (plain BED, GFF and VCF are read whole; index larger files) |
| `DEPICTIO_JBROWSE_URL_TTL_S` | `21600` | Lifetime of the signed track URLs handed to the browser, in seconds (at least 60) |

---

## S3 File Cache

**Config Class:** `S3CacheConfig`
**Environment Prefix:** `DEPICTIO_S3_`

Local copies of S3 files (MultiQC reports and others), so they are downloaded once.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_S3_CACHE_DIR` | `~/.depictio/s3_cache` | Local directory for the S3 file cache, kept across restarts |

---

<!-- ## Dashboard YAML Sync (DEPRECATED — JSON-based API has replaced it, hidden from user-facing nav)

**Config Class:** `DashboardYAMLConfig`
**Environment Prefix:** `DEPICTIO_DASHBOARD_YAML_`

YAML-based dashboard management. Marked DEPRECATED in
`DashboardYAMLConfig`: the system is being phased out in favour of the
JSON-based API. `enabled` now defaults to `false`, and
`auto_export_on_save` / `auto_import_on_change` / `watch_local_dir` are
likewise off by default and tagged DEPRECATED in code. Defaults here
mirror the code so future-you finds correct values if the section is
ever re-surfaced.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_DASHBOARD_YAML_ENABLED` | `false` | Enable YAML-based dashboard management (DEPRECATED) |
| `DEPICTIO_DASHBOARD_YAML_LOCAL_DIR` | `<repo>/dashboards/local` | Directory for instance-specific dashboard YAML files (auto-synced) |
| `DEPICTIO_DASHBOARD_YAML_TEMPLATES_DIR` | `<repo>/dashboards/templates` | Directory for template dashboard YAML files (version control) |
| `DEPICTIO_DASHBOARD_YAML_BASE_DIR` | - | DEPRECATED: Use local_dir instead. Base directory for dashboard YAML files |
| `DEPICTIO_DASHBOARD_YAML_ORGANIZE_BY_PROJECT` | `true` | Organize YAML files in subdirectories by project name |
| `DEPICTIO_DASHBOARD_YAML_USE_DASHBOARD_TITLE` | `true` | Use dashboard title in filename (vs just ID) |
| `DEPICTIO_DASHBOARD_YAML_INCLUDE_EXPORT_METADATA` | `true` | Include export timestamp and version in YAML files |
| `DEPICTIO_DASHBOARD_YAML_COMPACT_MODE` | `true` | Use compact YAML format with references (75-80% smaller files) |
| `DEPICTIO_DASHBOARD_YAML_MVP_MODE` | `true` | Use MVP minimal YAML format (60-80 lines, human-readable IDs, no layout) |
| `DEPICTIO_DASHBOARD_YAML_REGENERATE_STATS` | `true` | Regenerate column statistics on import instead of storing in YAML |
| `DEPICTIO_DASHBOARD_YAML_AUTO_LAYOUT` | `false` | Auto-generate component layout on import if missing |
| `DEPICTIO_DASHBOARD_YAML_AUTO_EXPORT_ON_SAVE` | `false` | Auto-export to YAML on save (DEPRECATED) |
| `DEPICTIO_DASHBOARD_YAML_AUTO_IMPORT_ON_CHANGE` | `false` | Auto-import from YAML on file change (DEPRECATED) |
| `DEPICTIO_DASHBOARD_YAML_WATCHER_DEBOUNCE_SECONDS` | `2.0` | Seconds to wait after file change before syncing |
| `DEPICTIO_DASHBOARD_YAML_WATCH_LOCAL_DIR` | `false` | Watch and auto-sync local dashboards directory (DEPRECATED) |
| `DEPICTIO_DASHBOARD_YAML_WATCH_TEMPLATES_DIR` | `false` | Watch and auto-sync templates directory (useful for template development) |
| `DEPICTIO_DASHBOARD_YAML_ENABLE_VALIDATION` | `true` | Enable validation gate before syncing YAML to MongoDB |
| `DEPICTIO_DASHBOARD_YAML_BLOCK_ON_VALIDATION_ERRORS` | `true` | Block sync if validation fails (set False to only warn) |
| `DEPICTIO_DASHBOARD_YAML_VALIDATE_COLUMN_NAMES` | `true` | Validate that column names exist in data collection schema |
| `DEPICTIO_DASHBOARD_YAML_VALIDATE_COMPONENT_TYPES` | `true` | Validate chart types, aggregation functions, and filter types |

(`DEPICTIO_DASHBOARD_YAML_WATCHER_AUTO_START` removed — the field no
longer exists on `DashboardYAMLConfig`.)

---
-->

## Monitoring

**Config Class:** `MonitoringConfig`
**Environment Prefix:** `DEPICTIO_MONITORING_`

Feeds the admin Log & Task panel. See [Monitoring](../usage/administration/monitoring.md).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MONITORING_ENABLED` | `true` | Enable the admin monitoring feature |
| `DEPICTIO_MONITORING_RETENTION_DAYS` | `14` | TTL in days for `task_events` records before automatic expiry |
| `DEPICTIO_MONITORING_APP_LOG_MIN_LEVEL` | `WARNING` | Minimum level captured into `app_logs`. One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `DEPICTIO_MONITORING_APP_LOG_CAPPED_MB` | `64` | Size cap in MB of the capped `app_logs` collection |
| `DEPICTIO_MONITORING_LIVE_UPDATES` | `true` | Push live task and ingestion status over the events WebSocket. Only active when `DEPICTIO_EVENTS_ENABLED` is also true |
| `DEPICTIO_MONITORING_INGESTION_STALE_AFTER_HOURS` | `24` | Hours without a write after which a `running` ingestion is swept to `abandoned`. `0` disables the sweep. The bundled compose files and Helm chart do not forward it, so set it on the backend yourself (v1.11.0+) |
| `DEPICTIO_MONITORING_AGENT_TTL_SECONDS` | `300` | How long a [watcher](../usage/administration/monitoring.md#watchers) stays listed after its last heartbeat. At least 60 |

---

## Dashboard Versions

**Config Class:** `DashboardVersionsConfig`
**Environment Prefix:** `DEPICTIO_DASHBOARD_VERSIONS_`

The version history of every dashboard. See [Dashboard and data versions](../features/versioning.md#retention-and-configuration).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_DASHBOARD_VERSIONS_ENABLED` | `true` | Record a version on each dashboard save. Off, nothing new is recorded |
| `DEPICTIO_DASHBOARD_VERSIONS_COALESCE_WINDOW_SECONDS` | `300` | How long consecutive autosaves by the same author fold into one version, counted from its creation |
| `DEPICTIO_DASHBOARD_VERSIONS_MAX_VERSIONS_PER_FAMILY` | `100` | Autosaves kept per dashboard, bookmarked ones aside |
| `DEPICTIO_DASHBOARD_VERSIONS_RETENTION_DAYS` | `90` | Age after which versions that are not bookmarked are dropped |
| `DEPICTIO_DASHBOARD_VERSIONS_KEEP_DAILY_FOR_DAYS` | `30` | Age after which autosaves thin to the last one of each day |
| `DEPICTIO_DASHBOARD_VERSIONS_MAX_SNAPSHOT_BYTES` | `8388608` (8 MiB) | Largest version recorded. A larger one is skipped and logged; the save itself goes through |
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_ENABLED` | `false` | Show readers what changed since their last visit. See [_"What's new"_](../features/whats-new.md) (v1.21.0+) |
| `DEPICTIO_DASHBOARD_VERSIONS_CHANGES_SINCE_MARK_MODE` | `sticky` | Default for readers who have not chosen: `sticky` keeps the marks until the reader marks them as seen, `previous_visit` shows what changed since the visit before this one (v1.21.0+) |

---

## Comments <small>(v1.17.2+)</small> { #comments }

**Config Class:** `CommentsConfig`
**Environment Prefix:** `DEPICTIO_COMMENTS_`

Who may use the comment threads of a dashboard. See [Viewers can comment](../features/comments-annotations.md#viewers-can-comment).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT` | `false` | Let anyone with viewer access to a project read and write its threads. Moderation, annotations and agent proposals stay with editors and owners, and anonymous visitors never comment |

---

## Structure Resolver <small>(v1.19.0+)</small> { #structure-resolver }

**Config Class:** `StructureResolverSettings`
**Environment Prefix:** `DEPICTIO_STRUCTURE_RESOLVER_`

Lets the [protein tiles](../features/proteins.md#structure-resolver) fetch a model the run did not publish, from AlphaFold DB, UniProt and ESMFold. Off by default: once on, an accession, a gene and taxon, or a sequence leaves the server. See [External structure services](../features/security.md#structure-resolver). Compose and Helm forward only `ENABLED`; add the others to the service's environment.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_STRUCTURE_RESOLVER_ENABLED` | `false` | Turn the resolver on. Off, `structure_source: resolve` tiles answer 403 |
| `DEPICTIO_STRUCTURE_RESOLVER_AFDB_BASE_URL` | `https://alphafold.ebi.ac.uk` | AlphaFold DB |
| `DEPICTIO_STRUCTURE_RESOLVER_UNIPROT_BASE_URL` | `https://rest.uniprot.org` | UniProt, to turn a gene and taxon into an accession |
| `DEPICTIO_STRUCTURE_RESOLVER_ESMFOLD_URL` | `https://api.esmatlas.com/foldSequence/v1/pdb/` | ESMFold, which folds a sequence |
| `DEPICTIO_STRUCTURE_RESOLVER_TIMEOUT_S` | `60` | Timeout of one call to a service |
| `DEPICTIO_STRUCTURE_RESOLVER_TOTAL_TIMEOUT_S` | `120` | Time one request may spend across all its calls and retries |
| `DEPICTIO_STRUCTURE_RESOLVER_MAX_BYTES` | `20971520` (20 MiB) | Largest model accepted |
| `DEPICTIO_STRUCTURE_RESOLVER_ESMFOLD_MAX_LENGTH` | `400` | Longest sequence sent to ESMFold |
| `DEPICTIO_STRUCTURE_RESOLVER_CACHE_PREFIX` | `structures/resolved` | Where fetched models are cached in the instance bucket |

---

## Ingestion

**Config Class:** `IngestionConfig`
**Environment Prefix:** `DEPICTIO_INGESTION_`

Server-side limits and opt-ins for ingestion (v1.15.0+). Everything but the step limit is off by default. See [Ingestion worker](docker.md#ingestion-worker).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_INGESTION_STEP_UPDATES_PER_MINUTE` | `60` | Live step updates recorded per ingestion run and minute. `success`, `failed` and `skipped` steps always pass. See [Monitoring](../usage/administration/monitoring.md#ingestion) |
| `DEPICTIO_INGESTION_ASYNC_DELTATABLE_UPSERT` | `false` | Hand the profiling of a written table to the ingestion worker when the CLI asks with `--async-upsert`. Needs `DEPICTIO_JOBS_ENABLED`, without which it stays inline. See [Offloading the table profile](docker.md#async-upsert) |
| `DEPICTIO_INGESTION_BROWSER_TRIGGER` | `false` | Offer [**Run ingestion**](../features/dashboards.md#run-ingestion) on project pages to owners, editors and admins. Needs `DEPICTIO_JOBS_ENABLED` and `DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS`. See [Starting an ingestion from the browser](docker.md#browser-trigger) |
| `DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS` | empty | Directories a browser-started ingestion may read, comma-separated or as a JSON list. Every path a project names, and every file its scan registers, must resolve inside one of them. Empty refuses every ingestion |

---

## Jobs

**Config Class:** `JobsConfig`
**Environment Prefix:** `DEPICTIO_JOBS_`

Records of work the server accepted but finishes in the background, polled through the [`/jobs` API](../api/README.md#jobs) (v1.15.0+). Off by default.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_JOBS_ENABLED` | `false` | Create the `jobs` collection and serve `/jobs`. Required by both offloaded ingestion features |
| `DEPICTIO_JOBS_RETENTION_HOURS` | `24` | How long a successful job is kept |
| `DEPICTIO_JOBS_FAILED_RETENTION_HOURS` | `168` | How long a failed or cancelled job is kept |
| `DEPICTIO_JOBS_MAX_RESULT_BYTES` | `262144` | Largest job result stored. A larger one is dropped and the job marked `result_truncated` |

---

## Telemetry

**Config Class:** `TelemetryConfig`
**Environment Prefix:** `DEPICTIO_TELEMETRY_`

Anonymous installation heartbeat. See [Telemetry](../features/telemetry.md) for
what is sent and how to inspect it.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_TELEMETRY_ENABLED` | `true` | Send anonymous installation telemetry. Also suppressed by `DO_NOT_TRACK`, in CI, under pytest, and when `DEPICTIO_MONGODB_WIPE` is set |
| `DEPICTIO_TELEMETRY_ENDPOINT` | PostHog Cloud EU | Collector ingestion URL, PostHog-compatible capture endpoint |
| `DEPICTIO_TELEMETRY_API_KEY` | Depictio's own project | Collector project token. Public write-only key, carries no read access. Override only to point at your own collector |
| `DEPICTIO_TELEMETRY_INTERVAL_HOURS` | `24` | Hours between heartbeat attempts, 1–168. At most one send per UTC day either way |
| `DEPICTIO_TELEMETRY_DEPLOYMENT_KIND` | auto-detected | Override the detected kind: `helm`, `kubernetes`, `docker-compose`, `docker-compose-dev`, `docker`, `devcontainer`, `local` |
| `DEPICTIO_TELEMETRY_INCLUDE_USAGE_METRICS` | `true` | Include bucketed deployment-size counts. Disable to send only install identity and version |
| `DEPICTIO_TELEMETRY_DEBUG` | `false` | Log the payload instead of sending it, so an operator can audit telemetry before deciding |
| `DEPICTIO_TELEMETRY_STATE_DIR` | `~/.depictio` | Where the CLI stores its anonymous ID |

Five more are stated by the Helm chart from its own `values.yaml` and are unset
outside Helm: `DEPICTIO_TELEMETRY_REPLICAS`, `DEPICTIO_TELEMETRY_CPU_REQUEST`,
`DEPICTIO_TELEMETRY_CPU_LIMIT`, `DEPICTIO_TELEMETRY_MEMORY_REQUEST` and
`DEPICTIO_TELEMETRY_MEMORY_LIMIT`. CPU quantities are parsed to millicores and
memory to MiB before they can reach the payload; neither is ever sent raw.

---

## MultiQC Prerender

**Config Class:** `MultiQCPrerenderConfig`
**Environment Prefix:** `DEPICTIO_MULTIQC_`

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_MULTIQC_PRERENDER_DIR` | `~/.depictio/multiqc_prerender` | Local directory for pre-rendered MultiQC figures |

---

## Global Settings

**Config Class:** `Settings`
**Environment Prefix:** `DEPICTIO_`

Top-level settings, plus the `DEPICTIO_` variables the server reads directly.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_CONTEXT` | `server` | `server` for the API and workers, `client` for the CLI. Server context enforces the secrets |
| `DEPICTIO_DISABLE_EXAMPLE_DASHBOARDS` | `false` | Skip seeding the bundled reference projects (Iris, Penguins, Advanced Visualisations, nf-core/ampliseq, nf-core/viralrecon) and their dashboards on API startup |
| `DEPICTIO_SEED_PROJECTS` | _(empty = all)_ | Comma-separated allowlist of bundled reference projects to seed on startup, e.g. `iris` or `iris,penguins`. Names: `iris`, `penguins`, `ampliseq`, `advanced_viz_showcase`, `viralrecon`. Ignored when `DEPICTIO_DISABLE_EXAMPLE_DASHBOARDS=true` |
| `DEPICTIO_SEED_EXTRA_PROJECTS` | _(empty)_ | Comma-separated optional projects to seed on top of the default set: `catalog_conformance` (a CI test fixture) and `genome_tracks_examples` (the Genome Tracks Showcase, opt-in since v1.22.0 on a fresh database; an instance that already has it keeps it) |
| `DEPICTIO_WALKTHROUGH_DISABLED` | `false` | Turn off the [guided tours](../usage/guides/web_ui.md#guided-tours) (coach cards) and, since v1.22.0, the dashboard [landing card](../usage/guides/dashboard-guide.md#landing-hint) for every user; the header compass stays, disabled. Useful for embedded iframes, screenshot staging and demos with their own narration |
| `DEPICTIO_ENABLE_DEV_ENDPOINTS` | `false` | Expose the destructive test endpoints (`utils/drop_S3_content`, `utils/drop_all_collections`, `events/test-trigger`). Off, they answer 404 even for admins. Development only |
| `DEPICTIO_DEV_MODE` | `false` | Development mode: the API runs under `uvicorn --reload`, the worker restarts on code changes, telemetry, the guided tours and the landing card are off, and the admin CLI config is re-exported at each start. Not a security switch |
| `DEPICTIO_DELTA_CACHE_DIR` | `/app/cache/delta_cache` | Local cache of Delta tables read by the API |

---

## Branding

**Config Class:** `BrandingConfig`
**Environment Prefix:** `DEPICTIO_BRANDING_`

Deployment-level defaults for the [brand theme](../usage/administration/branding.md). Every one of these is the leftmost layer: the `/admin` Branding panel and a dashboard's own override sit on top of them, and neither needs a redeploy. Leave a variable unset and the layer above, or Depictio's own look, applies.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_BRANDING_PRESET` | - | Starting point seeded into the theme: `depictio`, `trec`, `embl` or `ocean`. The flat variables below override it field by field. |
| `DEPICTIO_BRANDING_APP_NAME` | `Depictio` | Browser tab title and login greeting |
| `DEPICTIO_BRANDING_LOGO_URL` | - | Logo for light mode. Absolute (`https://`) or a path this deployment serves |
| `DEPICTIO_BRANDING_LOGO_URL_DARK` | - | Logo for dark mode. Falls back to `DEPICTIO_BRANDING_LOGO_URL` |
| `DEPICTIO_BRANDING_PRIMARY_COLOR` | - | Primary brand colour. Hex, or a Mantine palette name (`blue`, `teal`, `grape`, ...). A hex value is expanded server-side into a 10-shade tuple with your colour on the shade a filled button paints |
| `DEPICTIO_BRANDING_SECONDARY_COLOR` | - | Secondary brand colour |
| `DEPICTIO_BRANDING_TERTIARY_COLOR` | - | Tertiary / accent brand colour |
| `DEPICTIO_BRANDING_TINT_MODE` | `accent` | How far the brand reaches. `accent` re-tints the primary accent only; `full` also gives the secondary and tertiary the app's existing teal and orange accent families. `gray`, `red`, `green` and `yellow` are never remapped |
| `DEPICTIO_BRANDING_SUCCESS_COLOR` | - | Overrides Mantine green. Status colours stay outside the brand reach so pass / warn / fail keep reading as meaning |
| `DEPICTIO_BRANDING_WARNING_COLOR` | - | Overrides Mantine yellow |
| `DEPICTIO_BRANDING_DANGER_COLOR` | - | Overrides Mantine red |
| `DEPICTIO_BRANDING_FONT_FAMILY` | - | Body font stack. Must be installed or served by this deployment; none is fetched for you |
| `DEPICTIO_BRANDING_HEADINGS_FONT_FAMILY` | - | Headings font stack |
| `DEPICTIO_BRANDING_DEFAULT_RADIUS` | - | Corner radius as a Mantine token, `xs` to `xl` |
| `DEPICTIO_BRANDING_COLORWAY` | _(derived)_ | Categorical figure palette, comma-separated hex. Derived from the brand palette when unset |
| `DEPICTIO_BRANDING_SEQUENTIAL` | _(derived)_ | Continuous figure scale, comma-separated hex. Derived from the brand palette when unset |
| `DEPICTIO_BRANDING_PLOT_TEMPLATE` | - | Plotly template for figures whose component picks none. Unset means follow the UI colour scheme, using Depictio's brand-aware `mantine_light` / `mantine_dark` |
| `DEPICTIO_BRANDING_THEME` | - | Escape hatch: a whole brand theme as JSON, for fields with no flat variable of their own (the per-scheme chrome surfaces). Merged **under** the flat variables above |

!!! example "Full commented block"
    The depictio repository ships the whole set with inline commentary in [`.env.example`](https://github.com/depictio/depictio/blob/main/.env.example), and a Kubernetes equivalent in [`helm-charts/depictio/examples/values-branding.yaml`](https://github.com/depictio/depictio/blob/main/helm-charts/depictio/examples/values-branding.yaml).

!!! tip "Chrome surfaces need the JSON variable"
    `app_bg`, `section_bg`, `nav_bg` and `heading` are set per colour scheme, so they have no flat variable. Pass them through `DEPICTIO_BRANDING_THEME`:

    ```bash
    DEPICTIO_BRANDING_THEME={"surfaces_light":{"app_bg":"#f8faf9","nav_bg":"#ffffff","heading":"#00514b"}}
    ```

---

## Release Check <small>(v1.17.0+)</small> { #release-check }

**Config Class:** `VersionCheckConfig`
**Environment Prefix:** `DEPICTIO_VERSION_CHECK_`

Tells administrators when a newer Depictio release is published. The API asks the GitHub Releases API with an unauthenticated `GET` that sends nothing about the instance. See [Release check](../usage/guides/web_ui.md#release-check).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_VERSION_CHECK_ENABLED` | _(unset)_ | Unset: the check is on and administrators can turn it off in **Administration → Settings**. `true` or `false` decides instead and locks that switch |
| `DEPICTIO_VERSION_CHECK_INTERVAL_HOURS` | `6` | Hours between checks, `1` to `168`, once for the whole instance |
| `DEPICTIO_VERSION_CHECK_REPOSITORY` | `depictio/depictio` | GitHub repository whose releases are compared with the running version |
| `DEPICTIO_VERSION_CHECK_TIMEOUT_SECONDS` | `10` | Timeout of the GitHub request |

---

## Feedback

**Config Class:** `FeedbackConfig`
**Environment Prefix:** `DEPICTIO_FEEDBACK_`

An opt-in link on every dashboard that carries the reader's context to wherever you point it: an issue form, a helpdesk, a `mailto:`. It renders only when enabled **and** a URL is set (v1.11.0+).

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_FEEDBACK_ENABLED` | `false` | Show the link: an icon at the end of the dashboard header, and a **Feedback** section in the dashboard's Settings |
| `DEPICTIO_FEEDBACK_URL` | - | Link target. `{dashboard}`, `{dashboard_id}`, `{tab}` (the tab label the reader sees) and `{url}` are filled in and URL-encoded in the browser; no other placeholder is |
| `DEPICTIO_FEEDBACK_LABEL` | `Feedback` | Icon tooltip and settings label |

```bash
DEPICTIO_FEEDBACK_ENABLED=true
DEPICTIO_FEEDBACK_URL='https://github.com/<org>/<repo>/issues/new?template=dashboard_feedback.yml&dashboard={dashboard}&tab={tab}&page={url}'
DEPICTIO_FEEDBACK_LABEL='Send feedback'
```

---

## Compose and image variables { #compose-and-image-variables }

Read by `docker-compose.yaml` or a container, not by the settings models.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_VERSION` | the release the compose file pins | Image tag of the backend, viewer and worker. `next` follows `main` |
| `DEPICTIO_CSP_S3_ORIGIN` | `DEPICTIO_S3_PUBLIC_URL` | Viewer container: S3 origin added to the CSP `connect-src`, for genome tracks read straight from the bucket |
| `DATA_DIR` | `data` | `docker-compose.dev.yaml` only: host folder holding the MongoDB, Redis and SeaweedFS data |

`DEPICTIO_CELERY_WORKERS` and the other worker variables are in [Worker processes](#celery-worker-processes),
`DEPICTIO_FASTAPI_HOST` / `_PORT` / `_WORKERS` in [FastAPI Backend](#fastapi-backend).

### Declared but not read

These names exist in `settings_models.py` and change nothing. Most are left over from the Dash
frontend; setting one has no effect.

- `DEPICTIO_VIEWER_HOST`, `_WORKERS`, `_DEBUG`, `_AUTO_GENERATE_FIGURES`
- `DEPICTIO_FASTAPI_SSL`, `DEPICTIO_FASTAPI_LOGGING_LEVEL` (the log level is `DEPICTIO_LOGGING_VERBOSITY_LEVEL`)
- `DEPICTIO_CACHE_FALLBACK_TO_MEMORY`, `DEPICTIO_CACHE_CACHE_VERSION`
- `DEPICTIO_PERFORMANCE_HTTP_CLIENT_TIMEOUT`, `_API_REQUEST_TIMEOUT`, `_BROWSER_ELEMENT_TIMEOUT`, `_SCREENSHOT_API_TIMEOUT`, `_DNS_CACHE_TTL`, `_CONNECTION_POOL_SIZE`, `_MAX_KEEPALIVE_CONNECTIONS`, `_DISABLE_LOADING_SPINNERS`, `_DISABLE_ANIMATIONS`, `_DISABLE_THEME_ANIMATIONS`
- every `DEPICTIO_PROFILING_*`
- the Celery worker fields listed under [Worker processes](#celery-worker-processes)

---

## See Also

- [Quick Start with Docker](docker.md)
- [Configuration Guide](configuration.md)
- [Kubernetes Installation](kubernetes.md)
