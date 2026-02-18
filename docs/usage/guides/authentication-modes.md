---
title: "Authentication Modes"
icon: material/shield-account
description: "Depictio supports four authentication modes to fit different deployment scenarios."
---

# Authentication Modes

Depictio supports four authentication modes, each designed for a different deployment scenario. Only one mode is active at a time.

## Quick Comparison

| | **Auth** (default) | **Single-User** | **Public** | **Demo** |
|---|---|---|---|---|
| **Use case** | Multi-user, enterprise | Personal instance | Public-facing showcase | Guided product tour |
| **Login required** | Yes | No | No (browse); Yes (create) | No (browse); Yes (create) |
| **Anonymous access** | None | Full admin | Read-only | Read-only + guided tour |
| **Dashboard creation** | Registered users | Immediate | After sign-in | After sign-in |
| **User management** | Full RBAC | Disabled | Disabled | Disabled |
| **Temporary users (24h)** | No | No | Yes | Yes |
| **Google OAuth** | Optional | Optional | Optional | Optional |
| **Guided tour** | No | No | No | Yes |

## Auth Mode (Default)

Standard multi-user authentication with full access control.

**When to use:** Teams and organizations that need user accounts, roles, and project-level permissions.

```bash
# Default - no special env vars needed
# Optionally enable Google OAuth:
DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED=true
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID=your-client-id
DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET=your-secret
```

**Behavior:**

- Users register or are created by admins
- JWT-based authentication (RS256)
- Role-based access: admin and regular users
- Project and dashboard-level permissions (owner, editor, viewer)

## Single-User Mode

Zero-friction mode for personal or self-hosted instances.

**When to use:** You are the only user and want immediate full access without login.

```bash
DEPICTIO_AUTH_SINGLE_USER_MODE=true
```

**Behavior:**

- An anonymous user is created with **admin privileges**
- No login screen — full access immediately
- Dashboard creation, project management, and all features available
- Sidebar shows a "Single User Mode" badge
- User management UI is hidden (unnecessary with one user)

## Public Mode

Read-only anonymous access with optional sign-in for full features.

**When to use:** Sharing dashboards publicly — visitors can browse without an account, but must sign in to create or edit content.

```bash
DEPICTIO_AUTH_PUBLIC_MODE=true

# Backward-compatible alias:
# DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true
```

**Behavior:**

- Anonymous user has **read-only** access to public dashboards
- A "Sign In" button in the sidebar opens an auth modal with:
    - **Temporary user** — 24-hour session, auto-cleaned after expiry
    - **Google OAuth** — persistent account (if enabled)
- After sign-in, users can create dashboards, duplicate existing ones, and manage projects
- Sidebar shows a "Public Mode" badge

**Configuration:**

```bash
# Temporary user session duration (default: 24h)
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24
```

## Demo Mode

Extends Public Mode with a guided interactive tour for first-time visitors.

**When to use:** Product demos, onboarding, trade shows — guide users through Depictio's features step by step. Can also be repurposed as a self-service tutorial environment.

```bash
DEPICTIO_AUTH_PUBLIC_MODE=true
DEPICTIO_AUTH_DEMO_MODE=true
```

**Behavior:**

- All Public Mode features, plus:
- A 5-step interactive tour appears for new visitors:
    1. **Welcome** — explains the demo environment and 24h session limit
    2. **Explore Dashboards** — browse example dashboards
    3. **Sign In** — create a temporary account or use Google OAuth
    4. **Duplicate to Edit** — copy an existing dashboard to customize it
    5. **Explore Projects** — register a project and upload data
- Tour state is persisted in the browser (won't re-show after completion)
- Sidebar shows a "Demo Mode" badge

## Choosing a Mode

```
Personal analytics tool?          → Single-User Mode
Team/org with user accounts?      → Auth Mode (default)
Public dashboard gallery?         → Public Mode
Product demo or guided tutorial?  → Demo Mode
```

## Related

- [Configuration Guide](../../installation/configuration.md) — Full environment variable reference
- [Environment Reference](../../installation/env-reference.md) — All 160+ variables
