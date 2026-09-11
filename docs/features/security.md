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
| **Session Management** | Configurable token lifetime and refresh |
| **Secure Storage** | Tokens stored in HTTP-only cookies |
| **Token Refresh** | Automatic refresh before expiration |

### Authentication Flow

```text
┌─────────┐     ┌─────────────┐     ┌─────────────┐
│  User   │────▶│  Login API  │────▶│  JWT Token  │
│         │     │             │     │  (signed)   │
└─────────┘     └─────────────┘     └──────┬──────┘
                                           │
                     ┌─────────────────────▼──────┐
                     │  Subsequent API Requests   │
                     │  (Token in Authorization)  │
                     └────────────────────────────┘
```

### Registration Hardening

The `/register` endpoint strips the `is_admin` field from any incoming payload, so self-promotion to admin at registration is not possible. Admin privileges are granted exclusively via the `/auth/turn_sysadmin` endpoint, which enforces two guards: at least one admin must remain in the system at all times (last-admin guard), and a user cannot demote themselves (no-self-demote guard).

### Session Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh token lifetime |
| `JWT_ALGORITHM` | RS256 | JWT signing algorithm |

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

```text
┌─────────────────────────────────────────┐
│               System Level              │
│  (Admin: user management, settings)     │
├─────────────────────────────────────────┤
│              Project Level              │
│  (Owner, Editor, Viewer per project)    │
├─────────────────────────────────────────┤
│             Dashboard Level             │
│  (Inherited from project permissions)   │
└─────────────────────────────────────────┘
```

### Project Permissions

| Permission | Admin | Editor | Viewer |
|------------|-------|--------|--------|
| View dashboards | Yes | Yes | Yes |
| Create dashboards | Yes | Yes | No |
| Edit dashboards | Yes | Yes | No |
| Delete dashboards | Yes | No | No |
| Manage project settings | Yes | No | No |
| Manage project members | Yes | No | No |

### Group-Based Access

Users can be organized into groups for easier permission management:

- **Groups** inherit project permissions
- **Individual users** can have additional permissions
- **Permission inheritance** follows the most permissive grant

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

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   User Code     │────▶│  compile_       │────▶│  Restricted     │
│   (Python)      │     │  restricted()   │     │  Bytecode       │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                        ┌────────────────────────────────▼────────┐
                        │          Safe Execution Context         │
                        │  • Approved libraries (plotly, pandas)  │
                        │  • Custom guards (_getitem_, _getattr_) │
                        │  • Read-only DataFrame copy             │
                        └─────────────────────────────────────────┘
```

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

---

## Remote Data Sources { #remote-data-sources }

The `url`, `s3_prefix` and `manifest` scan modes make the server fetch
user-supplied URLs, which is a textbook server-side request forgery surface.
Every such fetch, whether creating a data collection from a URL, ingesting a
manifest, or a refresh task on the Celery worker, goes through one gateway
module; nothing in server context reads a user-supplied URL directly. See
[Remote data and manifests](../usage/projects/remote-data.md) for the feature
itself.

### What the gateway enforces

| Check | Behaviour |
|-------|-----------|
| **Scheme allowlist** | `https://` and `s3://`. Plain `http://` only with `DEPICTIO_REMOTE_ALLOW_HTTP=true` |
| **Address check** | The host is resolved and private, loopback, link-local and reserved ranges are rejected, including the cloud metadata endpoint |
| **Redirects** | Every `Location` is re-validated against the same policy before it is followed; hops are capped by `DEPICTIO_REMOTE_MAX_REDIRECTS` |
| **Bounded download** | Streamed, with a size cap (`DEPICTIO_REMOTE_MAX_DOWNLOAD_BYTES`) and a per-operation timeout (`DEPICTIO_REMOTE_TIMEOUT_S`); a download that exceeds the cap is aborted and the partial file removed |
| **Host lists** | `DEPICTIO_REMOTE_URL_DENYLIST` always rejects. `DEPICTIO_REMOTE_URL_ALLOWLIST` is exclusive while set, and a listed host bypasses the private-range check |
| **Sanitised errors** | Transport and HTTP errors are logged with their cause and surfaced to the client without internal details |

The policy is read from the environment on every call, so the API and the
worker always agree. The CLI, which fetches the user's own loopback and intranet
hosts, reads directly but keeps the redirect and size caps.

!!! warning "Residual risk: DNS rebinding"
    The address is checked when the host is resolved, and a hostile resolver
    could answer differently between that check and the connection. The
    gateway does not pin the resolved address. Hardened deployments should run
    **allowlist-only**: set `DEPICTIO_REMOTE_URL_ALLOWLIST` to the hosts you
    trust, which turns the address check into a host check.

### Per-project storage credentials

A project owner can attach S3-compatible credentials so remote and manifest
collections can read a private bucket.

- Credentials live in their own collection, never on the project document, so
  they cannot leak through project responses or exports. Template bundles never
  include them.
- The secret is **encrypted at rest** with a symmetric key stored next to the
  JWT key pair, in `DEPICTIO_AUTH_KEYS_DIR`. The API encrypts on write and the
  Celery worker decrypts inside refresh tasks, so backend and worker must mount
  the same keys volume; a worker with a keys directory of its own would mint a
  second key and find every stored secret unreadable.
- The secret is **write-only** in the API: responses only carry `has_secret`,
  and an update that omits the secret keeps the stored one.
- The endpoint URL passes the same host gating as remote data URLs. The
  instance's own object storage is always allowed; a private-network endpoint
  needs to be allowlisted.
- These are read credentials only. Delta tables are still written with the
  instance's own storage configuration, and refresh workers re-read the
  credentials from the database rather than receiving them through the task
  broker.

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

### JBrowse Iframe Sandbox

The JBrowse iframe uses a restricted `sandbox` attribute that omits `allow-same-origin`. Previously, combining `allow-same-origin` with `allow-scripts` would have allowed iframe content to access the parent page's `localStorage` and read authentication tokens; removing `allow-same-origin` closes this vector.

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

### Secret Management

| Secret | Recommendation |
|--------|----------------|
| JWT Keys | Generate unique keys per environment |
| Database Credentials | Use strong passwords, rotate regularly |
| API Keys | Use environment variables, not config files |
| MinIO Credentials | Separate credentials per environment; root password is a `SecretStr` with a ≥16-character validator and no default — the server refuses to start if the value is absent or matches a known-default string |
| Project storage secrets | Encrypted at rest with `secrets_key.bin` in `DEPICTIO_AUTH_KEYS_DIR`; back the keys volume up with the JWT key pair and mount it on the worker too, see [Per-project storage credentials](#per-project-storage-credentials) |

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
