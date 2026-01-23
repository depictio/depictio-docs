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

### Input Validation

All user input is validated:

- **Pydantic models** for API request validation
- **Sanitization** of user-provided text
- **Type checking** at API boundaries
- **Size limits** on uploads and queries

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
| MinIO Credentials | Separate credentials per environment |

### Environment Configuration

```bash
# Example secure configuration
JWT_PRIVATE_KEY_PATH=/secrets/jwt_private.pem
JWT_PUBLIC_KEY_PATH=/secrets/jwt_public.pem
MONGODB_URI=mongodb://user:pass@mongo:27017/depictio?authSource=admin
MINIO_ACCESS_KEY=<generated-access-key>
MINIO_SECRET_KEY=<generated-secret-key>
```

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
