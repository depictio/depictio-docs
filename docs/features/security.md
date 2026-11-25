---
title: "Security Features"
icon: material/shield-check
description: "Comprehensive security features including authentication, authorization, and code execution restrictions."
---

# Security Features

Depictio implements comprehensive security measures to protect your data and ensure safe operation in production environments.

---

## Authentication

### JWT-Based Authentication

Depictio uses JSON Web Tokens (JWT) for secure authentication:

| Feature | Description |
|---------|-------------|
| **Token Security** | Public/private key encryption (RS256) |
| **Algorithm Pinning** | Algorithm pinned server-side (RS256/RS512); `alg=none` and algorithm-confusion attacks are rejected before any MongoDB access |
| **Claim Validation** | Signature and `exp` claim are both verified on every request; expired tokens are rejected immediately |
| **Session Management** | Access token 1 hour, refresh token 7 days; a CLI token lasts 1 year |
| **Storage** | The browser keeps the pair in local storage; the server keeps every live token in MongoDB, so deleting one revokes it |
| **Token Refresh** | Automatic refresh before expiration; since v1.23.0 every refresh also issues a new refresh token, and a retired one presented again revokes the session |

### Authentication Flow

[![Three ways in: a password, single sign-on or a CLI token. The API signs an access and a refresh token with its private key and keeps them in MongoDB; every request carries the access token, whose signature, expiry and presence in MongoDB are checked before the user's role](../images/security/sign-in_light.png#only-light)](../images/security/sign-in_light.png){target=_blank}
[![Three ways in: a password, single sign-on or a CLI token. The API signs an access and a refresh token with its private key and keeps them in MongoDB; every request carries the access token, whose signature, expiry and presence in MongoDB are checked before the user's role](../images/security/sign-in_dark.png#only-dark)](../images/security/sign-in_dark.png){target=_blank}

### Registration Hardening

The `/register` endpoint strips the `is_admin` field from any incoming payload, so self-promotion to admin at registration is not possible. Admin privileges are granted exclusively via the `/auth/turn_sysadmin` endpoint, which enforces two guards: at least one admin must remain in the system at all times (last-admin guard), and a user cannot demote themselves (no-self-demote guard).

### Session Configuration

Token lifetimes are fixed. The signing algorithm is `DEPICTIO_AUTH_KEYS_ALGORITHM`, `RS256`
by default: see the [environment reference](../installation/env-reference.md).

### Session hardening <small>(v1.23.0+)</small> { #session-hardening }

A refresh token is single-use: every refresh issues a new one, and the session keeps its
original expiry. A retired token presented again revokes the whole session, unless it
arrives within 30 seconds of its replacement, so two tabs refreshing at once both stay
signed in. `POST /auth/logout` deletes the session server-side, and the viewer calls it
when signing out.

- An empty password never signs in, and passwordless accounts (anonymous,
  pipeline-provisioned) get an unusable hash instead of a hash of the empty string.
- A leftover anonymous admin from single-user mode is demoted at startup in multi-user
  mode.
- `must_change_password` is enforced on the server: until the password is changed, only
  `/auth/me`, `/auth/me/optional`, `/auth/edit_password` and logout answer; every other
  route, `/auth/refresh` included, answers 403. The viewer sends a flagged user to the
  password form.
- No API response returns the stored password hash: `/auth/me`, registration and every
  other endpoint that returns a user carry the profile fields only.
- WebSockets authenticate with a first message `{"type": "auth", "token": ...}` instead
  of `?token=` in the URL, which appears in server and proxy logs. The query token is
  still accepted for one release, with a deprecation warning.

### Public access code <small>(v1.23.0+)</small> { #public-access-code }

A public instance behind an access code is only as safe as the code is hard to guess.

- Only wrong codes count towards the guessing limit: 10 a minute per address, 100 a
  minute for the whole instance. Guest sessions are capped at 60 a minute per address,
  so a room behind one NAT can sign in at once.
- A code shorter than 12 characters is reported at startup, never the code itself.
- A request without a token no longer gets the anonymous identity unless it carries the
  code.

---

## Role-Based Access Control (RBAC)

Depictio implements a hierarchical permission system for fine-grained access control.

### User Roles

| Role | Description | Typical Use |
|------|-------------|-------------|
| **Admin** | Full system access | System administrators |
| **User** | Standard access | Project members |
| **Viewer** | Read-only access | Collaborators, stakeholders |

### Permission Levels

Permissions are applied at multiple levels:

[![An admin passes every check. Anyone else gets a project role, the highest of their own and their groups' roles, with a viewer floor on a public project; a dashboard takes the project role unless its own owners or editors name them. No role answers 404](../images/security/access_light.png#only-light)](../images/security/access_light.png){target=_blank}
[![An admin passes every check. Anyone else gets a project role, the highest of their own and their groups' roles, with a viewer floor on a public project; a dashboard takes the project role unless its own owners or editors name them. No role answers 404](../images/security/access_dark.png#only-dark)](../images/security/access_dark.png){target=_blank}

### Project Permissions

| Permission | Admin | Editor | Viewer |
|------------|-------|--------|--------|
| View dashboards | Yes | Yes | Yes |
| Create dashboards | Yes | Yes | No |
| Edit dashboards | Yes | Yes | No |
| Delete dashboards | Yes | No | No |
| Manage project settings | Yes | No | No |
| Manage project members | Yes | No | No |

### Group-Based Access <small>(v1.18.0+)</small> { #group-based-access }

A project can be shared with [groups](../usage/administration/groups.md) as owner, editor
or viewer, beside its individual users. A user's role is the **highest** of their own role
and their groups' roles, so a direct viewer whose group owns the project is an owner.

Since v1.18.0 every access check (projects, dashboards, workflows, files, tables, MultiQC,
advanced visualizations, events, runs, the catalog and the screenshot service) goes
through one module, `depictio/api/v1/permissions.py`, where these hand-rolled checks had
drifted apart:

- an anonymous visitor matches public projects only;
- editors now pass every viewer-level read;
- renaming a data collection or editing its properties needs **editor**, and deleting one
  needs **owner**, where a direct viewer could write and an editor could not;
- `PUT /projects/update` checks the stored project and no longer writes `permissions`:
  sharing goes through the Permissions page or `POST /projects/update_project_permissions`.

A refusal is the same 404 as a missing resource. `GET /groups/list` returns names only,
never membership.

Since v1.23.0 the seven `POST /advanced_viz/compute_*` routes check data collection
access like `POST /advanced_viz/data`, instead of letting any user compute over another
project's table, and the legacy `DELETE /datacollections/delete/{workflow_id}/{dc_id}`
needs owner rights, where it checked viewer rights.

---

## Code Execution Security (Code Mode)

When using Code Mode for custom visualizations, Depictio implements strict security measures.

### RestrictedPython Security

Depictio uses [RestrictedPython](https://restrictedpython.readthedocs.io/) (Zope Foundation) for secure code execution:

| Feature | Description |
|---------|-------------|
| **Battle-Tested** | Used in production by Zope/Plone for 20+ years |
| **Compile-Time Restrictions** | Unsafe operations blocked during compilation |
| **Safe Execution Environment** | Pre-approved globals and built-ins only |
| **No System Access** | File system, network, and OS operations blocked |

### Security Architecture

[![A code figure is checked (steps, then fig, and no reassigned df), compiled with compile_restricted, then run on the Celery worker with a copy of df, px, go, pd, pl, np and safe builtins. While it runs, the attribute guard and an audit hook refuse file readers and writers, other submodules, eval and SQL, writing files, processes, sockets, libraries and new imports](../images/security/code-figure_light.png#only-light)](../images/security/code-figure_light.png){target=_blank}
[![A code figure is checked (steps, then fig, and no reassigned df), compiled with compile_restricted, then run on the Celery worker with a copy of df, px, go, pd, pl, np and safe builtins. While it runs, the attribute guard and an audit hook refuse file readers and writers, other submodules, eval and SQL, writing files, processes, sockets, libraries and new imports](../images/security/code-figure_dark.png#only-dark)](../images/security/code-figure_dark.png){target=_blank}

### Allowed Operations

```python
# Available libraries in Code Mode
import plotly.express as px      # Visualization library
import plotly.graph_objects as go # Advanced plotting
import pandas as pd              # Data manipulation
df                               # Your dataset (read-only copy)

# Safe built-in functions
len(), range(), str(), int(), float(), sum(), min(), max()
list(), dict(), tuple(), set(), sorted(), reversed()
```

### Blocked Operations

RestrictedPython prevents these operations at compile-time:

| Category | Blocked Operations |
|----------|-------------------|
| **File Operations** | `open()`, file I/O, filesystem access |
| **Network Access** | `requests`, `urllib`, socket operations |
| **System Calls** | `os.*`, `sys.*`, `subprocess`, shell commands |
| **Dangerous Built-ins** | `exec()`, `eval()`, `__import__()`, `compile()` |
| **Attribute Access** | Private attributes (underscore methods) on unsafe objects |

### Locking figure code <small>(v1.21.0+)</small> { #figure-code-lock }

A code figure runs Python on a server worker. On an instance open to people you do not know, such as a workshop, set `DEPICTIO_VIEWER_CODE_FIGURES_LOCKED=true`. The server then refuses new figure code from anyone but an administrator, and the figure builder shows "Writing figure code is turned off on this server." Code already on a dashboard or shipped with a template or the catalogue keeps rendering, and saving, moving or duplicating dashboards still works. UI mode stays available for new figures.

### Code sent with a render <small>(v1.23.0+)</small> { #code-sent-with-a-render }

- Running code sent with a figure preview needs **editor** rights on the project.
  Viewers and anonymous visitors render the code stored on the component.
- A code error shows its traceback to editors only; anyone else gets the generic
  failure message, with no paths.
- `/figure/analyze_code` needs a signed-in user and caps its input at 100 kB.
- Calls that mutate shared plotly or polars state from user code are blocked.
- User code runs under an address-space cap, `DEPICTIO_CODE_MODE_MAX_MEMORY_MB`
  (1024 MB by default), applied in Celery prefork children where one task runs per
  process. See the [environment reference](../installation/env-reference.md).

### Past versions in a render <small>(v1.15.0+)</small> { #past-versions-in-a-render }

A render request can draw a component as a past [dashboard version](versioning.md)
defined it. The request names that version with `definition_version`, and the server
reads the component from its own record of the version. A request cannot send a
component definition, so the code of a code-mode figure always comes from a saved
dashboard.

- A request that carries `component_overrides` is refused with 400.
- A version that no longer exists, or belongs to another dashboard, is refused with 400.
- A component that read another data collection in that version is refused with 409.

---

## Data Protection

### Encryption

| Data State | Protection |
|------------|------------|
| **In Transit** | TLS 1.2+ for all HTTP communication |
| **At Rest** | MongoDB encryption, MinIO server-side encryption |
| **Tokens** | RS256 asymmetric encryption |

### Data Isolation

- **Project boundaries**: Data strictly isolated between projects
- **User isolation**: Users can only access authorized projects
- **Delta Lake**: Versioned data with access controls
- **File-delete IDOR fix**: File-deletion permission is checked against `current_user.is_admin` (the requesting user's flag), not the file-owner's flag. This closes an IDOR where a non-admin could delete files owned by an admin account.

### Input Validation

All user input is validated:

- **Pydantic models** for API request validation
- **Sanitization** of user-provided text
- **Type checking** at API boundaries
- **Size limits** on uploads and queries

### Images and logos <small>(v1.23.0+)</small> { #images-and-logos }

`/files/serve/image` and `/dashboards/logo/{id}` serve anonymous callers only for public
projects and dashboards; anyone else needs access to the project. An `<img>` tag cannot
send an Authorization header, so the viewer exchanges image and logo paths for
short-lived signed URLs (HMAC, 1 hour) through `POST /files/serve/image/sign` and
`POST /dashboards/logo/sign`. Signatures are never stored: every render mints a fresh
one, and a saved dashboard keeps the stable unsigned URL.

### Migration and backup hardening <small>(v1.23.0+)</small> { #migration-backup-hardening }

- Project export stays admin-only outside public mode. In public mode only owners and
  editors may export, and the bundle carries no other user's email.
- A ZIP import refuses S3 keys outside the project's prefixes and dashboard ids already
  in use. The JSON import body is capped at 50 MB.
- An unverified requester email no longer takes ownership of an imported project.
- Backup files and their checksum sidecars are written owner-only (0600).

### Offline copies for visitors <small>(v1.25.0+)</small> { #public-offline-download }

A project owner may let visitors of a **public** project download each dashboard as one
offline HTML file. It is off unless the instance sets both
`DEPICTIO_STATIC_EXPORT_ENABLED` and `DEPICTIO_STATIC_EXPORT_PUBLIC_DOWNLOAD_ENABLED`, and
the owner turns it on in Project › Permissions.

- **Visitors never build anything.** The server keeps a copy built under the owner's
  rules, at the dashboard's default view. The download route reads that file and starts
  no job, so a stranger cannot make the server compute.
- **The owner sees what leaves first.** Before turning the option on, the owner reviews,
  per dashboard, the data collections the file carries, their columns and row counts, and
  which tables ship whole, then confirms. Once downloaded, no access control follows the
  file.
- **A public copy names no one and runs no author code.** It carries no email address,
  no Python runtime, and figures written in code mode ship as pictures without their
  source.
- **It follows the project.** A copy is rebuilt after a save or an ingestion. Making the
  project private, turning the option off, or deleting the dashboard or project deletes
  the copies. An imported project arrives with the option off.
- **Downloads are rate-limited per address** (10 a minute by default). When the limiter
  cannot count (Redis unreachable), downloads are refused with a 503 rather than let
  through. Owner-started exports have their own per-user limit and a cap on the export
  queue.

---

## Remote Data Sources <small>(v1.16.0+)</small> { #remote-data-sources }

The `url`, `s3_prefix` and `manifest` scan modes, and creating a project from
a run folder, make the server read locations a user supplies, which is a
textbook server-side request forgery surface. Every `https://` fetch, whether
creating a data collection from a URL, ingesting a manifest, a refresh task
on the Celery worker, or fetching a brand logo for a notebook export, goes
through one gateway module; every `s3://` read is
decided by one [access module](#s3-locations); a folder on the server's disk is
read only on a [`depictio local`](#folders-on-the-servers-disk) server, or by a
**Run ingestion** inside the folders an administrator allowed. Nothing in
server context reads a user-supplied location directly. See
[Remote data and manifests](../usage/projects/remote-data.md) for the feature
itself.

### What the gateway enforces

| Check | Behaviour |
|-------|-----------|
| **Scheme allowlist** | `https://` and `s3://`. Plain `http://` only with `DEPICTIO_REMOTE_ALLOW_HTTP=true` |
| **Address check** | The host is resolved and private, loopback, link-local, reserved, multicast and unspecified addresses are rejected, including the cloud metadata endpoint |
| **Redirects** | Every `Location` is re-validated against the same policy before it is followed; hops are capped by `DEPICTIO_REMOTE_MAX_REDIRECTS` |
| **Bounded download** | Streamed, with a size cap (`DEPICTIO_REMOTE_MAX_DOWNLOAD_BYTES`) and a per-operation timeout (`DEPICTIO_REMOTE_TIMEOUT_S`); a download that exceeds the cap is aborted and the partial file removed |
| **Host lists** | Exact host names, compared without case. `DEPICTIO_REMOTE_URL_DENYLIST` always rejects. `DEPICTIO_REMOTE_URL_ALLOWLIST` is exclusive while set, and a listed host bypasses the private-range check. An `s3://` location skips both: the [S3 rules](#s3-locations) apply instead |
| **Sanitised errors** | Transport and HTTP errors are logged with their cause and surfaced to the client without internal details |

The policy is read from the environment on every call, so the API and the
worker apply the same one as long as both are given the same
`DEPICTIO_REMOTE_*` settings. The CLI, which fetches the user's own loopback and
intranet hosts, reads directly but keeps the redirect and size caps.

!!! note "DNS rebinding: the address is pinned (v1.23.0+)"
    A fetch or a push target connects to the exact IP address the check validated, so a
    resolver that answers differently between the check and the connect is refused at
    connect, with the same error as the check. Requests carried by an environment proxy
    keep the plain client and the pre-check, because the proxy resolves the name.
    Before v1.23.0 the resolved address was not pinned; hardened deployments ran
    **allowlist-only** (`DEPICTIO_REMOTE_URL_ALLOWLIST`), which turns the address check
    into a host check.

### S3 locations { #s3-locations }

Which bucket the server reads, and with which credentials, is decided from the
configuration before any request goes out, so a bucket name typed by a user
never becomes an existence or region oracle.

- The bucket that holds the instance's own data is refused as a source: it
  holds every project's data.
- The instance's own S3 keys are never used for a user-supplied location.
- A bucket is read without credentials when listed in
  `DEPICTIO_REMOTE_PUBLIC_S3_BUCKETS`, or with project storage settings that
  hold no key, and with the server's ambient credentials only when listed in
  `DEPICTIO_REMOTE_CREDENTIALED_S3_BUCKETS`. Anyone on the instance can read
  what the second list names. Both lists are empty by default.
- Any other bucket needs the project's storage settings, and is read with them
  alone. Settings typed in while creating a project from a run folder are the
  only credentials that request uses.
- Errors name the bucket and the prefix, never an endpoint of the instance, a
  key or a request id.

The full order is under
[Reading S3 buckets](../usage/projects/remote-data.md#reading-s3-buckets). The
CLI reads from the user's own machine and skips the instance-bucket refusal and
the credentialed list.

### Folders on the server's disk { #folders-on-the-servers-disk }

A server reads a local path stored on a project in two cases only:
[**Run ingestion**](dashboards.md#run-ingestion) <small>(v1.15.0+)</small>,
which reads inside `DEPICTIO_INGESTION_ALLOWED_DATA_ROOTS` alone, see
[Starting an ingestion from the browser](../installation/docker.md#browser-trigger),
and a `depictio local` server, which is the user's own computer. Otherwise,
data ingested from a local folder is refreshed by the CLI that ingested it. On
a `depictio local` server:

- Local folders are off unless `DEPICTIO_LOCAL_DATA_ROOTS` is set, and only in
  single-user mode (`DEPICTIO_AUTH_SINGLE_USER_MODE`). `depictio local up` sets
  both, with the home folder and the folders given with `--data-root-allow`. A
  server with roots but not in single-user mode logs a warning and keeps them
  off.
- Every local read (listing, inspecting, creating, refreshing) needs a request
  addressed to a loopback host (`localhost` or a loopback address), which also
  defends against DNS rebinding, from an administrator.
- Paths are resolved to their real path and confined to the roots. Hidden
  folders and the folders Depictio keeps for itself (`~/.depictio`, the local
  home, the keys and CLI configuration folders, the backups) are refused even
  below a root.
- A run folder over 100,000 files is refused. For a project made from a run
  folder, every template variable given as a path and every location a data
  collection scans must be inside it; one pointing elsewhere is refused.

Since v1.23.0 the same rule is enforced when the server opens a stored local path, a
file record included: in server context a local path is read only below the bundled
projects, inside the server's own `depictio_*` upload folders of the temporary
directory (not the rest of it, where other processes leave files), or where the
local-data policy allows. Anything else is refused, so a registered path pointing at
the server's own keys hands back nothing. The CLI is not confined. Registering files
with `POST /files/upsert_batch` needs edit rights on every data collection it writes
to.

Since **v1.18.0** a phylogeny tree's stored location follows the same rules. An `s3://`
Newick goes through the [S3 location](#s3-locations) checks (never the instance bucket
with the instance's keys), a local one is read only below the bundled projects or a
`depictio local` folder, and an error no longer names the paths it tried.

### Per-project storage credentials

A project owner or an administrator can attach S3-compatible credentials so
remote and manifest collections can read a private bucket.

- Credentials live in their own collection, never on the project document, so
  they cannot leak through project responses or exports. Template bundles never
  include them. An instance [backup](../usage/administration/backup.md#what-is-covered)
  does, with the secret still encrypted: keep backup files as safe as the keys
  volume.
- The secret is **encrypted at rest** with a symmetric key stored next to the
  JWT key pair, in `DEPICTIO_AUTH_KEYS_DIR`. The API encrypts on write and the
  Celery worker decrypts inside refresh tasks, so backend and worker must mount
  the same keys volume; a worker with a keys directory of its own would mint a
  second key and find every stored secret unreadable.
- The secret is **write-only** in the API: responses only carry `has_secret`.
  An update that omits the secret keeps the stored one only while the access
  key, the endpoint and the bucket are unchanged, so a stored secret is never
  sent to another endpoint.
- Only project owners and administrators read or change the settings.
- The endpoint URL passes the same host gating as remote data URLs. The
  instance's own object storage is always allowed. Any other endpoint on a
  private network needs to be allowlisted, while an allowlist is set every
  endpoint must be on it, and `http://` needs `DEPICTIO_REMOTE_ALLOW_HTTP`.
  An empty endpoint, possible through the API only, means Amazon S3 and is
  not gated.
- The stored endpoint is checked again at every read, so tightening the host
  lists also stops settings saved before: their reads answer 409 until an
  owner updates them. A secret the instance cannot decrypt answers 500.
- These are read credentials only. Delta tables are still written with the
  instance's own storage configuration, and refresh workers re-read the
  credentials from the database rather than receiving them through the task
  broker.

### External structure services <small>(v1.19.0+)</small> { #structure-resolver }

The [protein tiles](proteins.md#structure-resolver) can fetch a model the run did not
publish. The resolver is **off by default** (`DEPICTIO_STRUCTURE_RESOLVER_ENABLED`), because
once on, exactly the accession, the gene and taxon, or the protein sequence leaves the
server, to EBI's AlphaFold DB, UniProt or Meta's ESM Atlas. For an unpublished sequence that
is a disclosure.

- Only the three configured hosts are contacted, redirects included and each re-checked.
- A model is capped in size (`MAX_BYTES`), each call and each request in time, and a body
  with no `ATOM` record is refused.
- Anonymous visitors of a public instance get a 403, so only signed-in users trigger calls.
- Models are cached in the instance bucket; failures are not.
- The tile names the service it called, with the endpoint under *Technical details*, and
  credits the model.

---

## Content Security Policy { #content-security-policy }

Deployed instances send a Content-Security-Policy header. The development server sends
none, so a policy violation only ever shows up on a deployment.

Most of the policy is `'self'`. Three allowances are not obvious, and are the ones to carry
across if you replace the policy at a reverse proxy or ingress:

| Directive | Allowance | Needed for |
|-----------|-----------|------------|
| `script-src` | `'unsafe-eval' 'wasm-unsafe-eval'` | Plotly's WebGL renderer and the in-browser Python runtime |
| `connect-src` | `ws: wss:` | The real-time events WebSocket |
| `connect-src` | the basemap origins below | Map tiles |

### Basemap origins { #basemap-origins }

Maps load their style, glyphs, sprite and vector tiles over `fetch`, so `connect-src`
governs them; allowing images is not enough. A map missing these renders blank.

```text
https://basemaps.cartocdn.com
https://*.basemaps.cartocdn.com
https://tile.openstreetmap.org
```

The apex domain is listed separately because a `*.` wildcard does not match it.

!!! warning "The policy lives in two files"
    The API middleware (`depictio/api/main.py`) and the viewer's nginx template
    (`docker-images/nginx.conf.template`) each send their own copy, and the two must agree.

---

## Audit Logging

Depictio logs security-relevant events for compliance and troubleshooting.

### Logged Events

| Event Type | Details Logged |
|------------|----------------|
| **Authentication** | Login attempts, token refresh, logout |
| **Authorization** | Permission checks, access denials |
| **Data Access** | Dashboard views, data queries |
| **Modifications** | Dashboard edits, project changes |
| **Admin Actions** | User management, system configuration |

### Log Configuration

Configure logging via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `LOG_FORMAT` | `json` | Log format (json/text) |
| `AUDIT_LOG_ENABLED` | `true` | Enable audit logging |

---

## Security Best Practices

### Genome browser track access <small>(v1.20.0+)</small> { #genome-browser-track-access }

The [genome browser](genome-browser/index.md) runs inside the viewer, not in an iframe, and the
browser never talks to S3 or to a track host itself. Every track byte goes through the
API's Range-capable track proxy:

- **Signed, expiring URLs.** The API hands the browser signed proxy URLs, valid for
  `DEPICTIO_JBROWSE_URL_TTL_S` seconds (6 hours by default). The proxy re-checks that the
  caller can read the data collection's project.
- **Ids, not URLs.** A request names a track of the collection's manifest, never a
  location, so a viewer cannot make the server fetch an address of their choosing.
- **Remote tracks need an allow-list.** A track read in place is refused unless its
  `https://` host is in `DEPICTIO_JBROWSE_REMOTE_HTTPS_HOSTS` or its `s3://` bucket is in
  `DEPICTIO_JBROWSE_REMOTE_S3_BUCKETS` (comma-separated lists). A listed S3 bucket is read
  with the server's credentials, so anyone who can open a collection pointing at it can
  read it: list only buckets that hold nothing private. In depictio's own data bucket, only
  the collection's `genomic_tracks/<dc_id>/` folder is served; a remote folder pointing
  elsewhere in it is refused.
- **Remote S3 credentials.** Without `DEPICTIO_JBROWSE_REMOTE_S3_ACCESS_KEY` and
  `DEPICTIO_JBROWSE_REMOTE_S3_SECRET_KEY`, remote buckets are read anonymously.
- **Direct access is opt-in.** A collection with `direct_access: true` has the browser
  fetch its `https://` tracks itself, which bypasses the proxy and needs the host to allow
  it with CORS.

The full variable list is in the [environment reference](../installation/env-reference.md#genome-browser).

### OpenID Connect sign-in { #oidc-sign-in }

[OpenID Connect single sign-on](../installation/sso/index.md) uses the authorization code flow
with PKCE (`S256`). A callback is accepted only if it answers a login this instance
started, and only once: the `state` is stored server-side in MongoDB and consumed
atomically. The `nonce` binds the `id_token` to the login, and the token is verified
against the provider's JWKS (signature, issuer, audience, expiry, with 60 seconds of
clock-skew leeway). The email is trusted only when the provider asserts it is verified.
The redirect URI comes from the configuration, never from the request, and redirects stay
on this site. The browser is handed a single-use ticket in the URL fragment, so no token
travels in a query string. Accounts created by single sign-on get a random password hash
instead of an invalid placeholder.

### OAuth Callback Security

The OAuth callback validates that the redirect URL is same-origin before calling `window.location.assign`. This closes an open-redirect vulnerability where a crafted authorization response could send the user (and any attached tokens) to an attacker-controlled domain.

Since **v1.5.2** the CSRF `state` is stored in MongoDB (`oauth_states`), used once and expired by a TTL index. It was previously held in per-process memory, so sign-in only worked when the callback happened to reach the worker that issued the state.

!!! warning "`DEPICTIO_DEV_MODE` no longer skips state validation"
    The flag used to bypass this check entirely, leaving the callback without CSRF
    protection on any deployment that set it. It now only affects hot-reload and
    verbose logging.

### Deployment Recommendations

1. **Use HTTPS**: Always deploy behind TLS termination
2. **Secure MongoDB**: Enable authentication, use TLS
3. **Secure MinIO**: Enable access keys, use TLS
4. **Network Isolation**: Use private networks for internal services
5. **Regular Updates**: Keep dependencies updated

### Single-user mode stays local <small>(v1.23.0+)</small> { #single-user-stays-local }

A single-user server signs in whoever reaches it as the admin, so the quick-start
compose files publish the viewer (which also proxies the API) on `127.0.0.1` by default.
Set `DEPICTIO_BIND_ADDRESS=0.0.0.0` only for a multi-user deployment reachable from
other machines. A single-user server logs an error the first time it answers a request
addressed to a non-local host (once per host, never blocking).

### Secret Management

| Secret | Recommendation |
|--------|----------------|
| JWT Keys | Generate unique keys per environment |
| Database Credentials | Use strong passwords, rotate regularly |
| API Keys | Use environment variables, not config files |
| MinIO Credentials | Separate credentials per environment; root password is a `SecretStr` with a ≥16-character validator and no default — the server refuses to start if the value is absent or matches a known-default string |
| Project storage secrets | Encrypted at rest with `secrets_key.bin` in `DEPICTIO_AUTH_KEYS_DIR`; back the keys volume up with the JWT key pair and mount it on the worker too, see [Per-project storage credentials](#per-project-storage-credentials) |

### Secrets in logs and responses <small>(v1.23.0+)</small> { #secrets-in-logs }

- Backup logs mask the S3 keys.
- The admin CLI no longer logs its configuration and token at debug level.
- `GET /auth/list_tokens` returns metadata only (id, name, lifetime, expiry), never
  the token values.

### Environment Configuration

```bash
# Example secure configuration
JWT_PRIVATE_KEY_PATH=/secrets/jwt_private.pem
JWT_PUBLIC_KEY_PATH=/secrets/jwt_public.pem
MONGODB_URI=mongodb://user:pass@mongo:27017/depictio?authSource=admin
MINIO_ACCESS_KEY=<generated-access-key>
MINIO_SECRET_KEY=<generated-secret-key>

# CORS — list allowed origins explicitly (comma-separated); wildcard with credentials is rejected
DEPICTIO_FASTAPI_CORS_ALLOWED_ORIGINS=https://your-domain.example.com

# Bootstrap admin (replaces initial_users.yaml)
DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD=<strong-password>
```

**CORS**: `allow_origins=["*"]` has been removed. Origins are configured via `DEPICTIO_FASTAPI_CORS_ALLOWED_ORIGINS` (comma-separated list). A wildcard combined with `allow_credentials=True` is explicitly rejected by the framework and will raise a startup error.

**Admin bootstrap**: `initial_users.yaml` is replaced by env-driven bootstrap via `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD`. This avoids shipping a default credentials file and ensures the admin password is injected as a secret at deploy time.

### Kubernetes Security

When deploying on Kubernetes:

- Use **Secrets** for sensitive configuration
- Enable **Network Policies** to restrict pod communication
- Use **ServiceAccounts** with minimal permissions
- Enable **Pod Security Standards**

---

## Security Reporting

If you discover a security vulnerability, please report it responsibly:

1. **Email**: Contact the maintainers privately
2. **GitHub**: Use GitHub Security Advisories (private disclosure)
3. **Details**: Include steps to reproduce and potential impact

**Do not disclose vulnerabilities publicly until a fix is available.**

### What to Report

- Code execution restriction bypasses
- Authentication/authorization bypasses
- Data access vulnerabilities
- Injection vulnerabilities (SQL, NoSQL, command)
- Cross-site scripting (XSS) issues

---

*Security is a shared responsibility. While Depictio provides robust security features, proper configuration and operational practices are essential for maintaining a secure environment.*
