---
title: "Authentication Modes"
description: "Depictio supports four authentication modes to fit different deployment scenarios."
---

# :material-shield-account:{ style="color: #009688" } Authentication Modes

Depictio supports four authentication modes, each designed for a different deployment scenario. Only one mode is active at a time.

## Quick comparison

<div class="grid cards" markdown>

-   :material-shield-account-outline:{ .lg .middle .dp-blue } **[Auth](#auth-mode)** · default

    ---

    For teams. Everyone signs in to an account of their own, with a role on each project.

    Nothing to set with Helm. With Compose, `DEPICTIO_AUTH_SINGLE_USER_MODE=false`.

-   :material-laptop:{ .lg .middle .dp-orange } **[Single-user](#single-user-mode)**

    ---

    For your own instance. No sign-in page: every visitor is signed in as the admin.

    `DEPICTIO_AUTH_SINGLE_USER_MODE=true`

-   :material-earth:{ .lg .middle .dp-teal } **[Public](#public-mode)**

    ---

    For a showcase. Every visitor gets a guest account of their own; SSO can turn it into a real one.

    `DEPICTIO_AUTH_PUBLIC_MODE=true`

-   :material-compass-outline:{ .lg .middle .dp-violet } **[Demo](#demo-mode)**

    ---

    Public mode as a read-only demo: the same guests, never asked to sign in.

    `DEPICTIO_AUTH_PUBLIC_MODE=true` and `DEPICTIO_AUTH_DEMO_MODE=true`

</div>

[![What a visitor gets in each mode: the sign-in page in Auth mode, the admin's session in Single-user mode, a temporary guest account of their own in Public and Demo mode, behind an optional access code](../../images/guides/authentication-modes/auth-modes_light.png#only-light)](../../images/guides/authentication-modes/auth-modes_light.png){target=_blank}
[![What a visitor gets in each mode: the sign-in page in Auth mode, the admin's session in Single-user mode, a temporary guest account of their own in Public and Demo mode, behind an optional access code](../../images/guides/authentication-modes/auth-modes_dark.png#only-dark)](../../images/guides/authentication-modes/auth-modes_dark.png){target=_blank}

??? abstract "Side by side"

    | | [:material-shield-account-outline: Auth](#auth-mode) | [:material-laptop: Single-user](#single-user-mode) | [:material-earth: Public](#public-mode) | [:material-compass-outline: Demo](#demo-mode) |
    |---|---|---|---|---|
    | **A visitor gets** | The sign-in page | The admin's session | A guest account, 24 h | A guest account, 24 h |
    | **Register** | :material-check: unless [disabled](#registration) | :material-close: | :material-close: | :material-close: |
    | **[SSO](../../installation/sso/index.md)** | :material-check: | Not used | :material-check: a guest [signs in](#guest-sign-in) | At `/auth/login` only |
    | **Create projects** | :material-check: | :material-check: | Admins only | Admins only |
    | **Duplicate a dashboard** | :material-check: | :material-check: | :material-check: the copy expires with the guest | :material-check: the copy expires with the guest |
    | **Guided tour** | Builder tour | Builder tour | Explorer tour | Explorer tour |

## :material-shield-account-outline: Auth mode <small>default</small> { #auth-mode }

For teams and organizations: every visitor signs in, to an account of their own, and sees
what their roles allow.

**Turn it on:** it is the mode whenever the other three are off. That is the Helm chart's
default. The root `docker-compose.yaml` starts in single-user mode instead, so with Compose set
`DEPICTIO_AUTH_SINGLE_USER_MODE=false` in `.env`.
[Single sign-on](../../installation/sso/index.md) is optional, here with Google:

=== "Environment"

    ```bash
    DEPICTIO_AUTH_OIDC_PROVIDERS='[{"id": "google", "label": "Sign in with Google", "discovery_url": "https://accounts.google.com/.well-known/openid-configuration"}]'
    DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID=your-client-id
    DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET=your-secret
    ```

=== "Helm values"

    ```yaml
    oidc:
      providers:
        - id: google
          label: "Sign in with Google"
          discovery_url: "https://accounts.google.com/.well-known/openid-configuration"
    secrets:
      oidcClients:
        google: {clientId: "<client-id>", clientSecret: "<client-secret>"}
    ```

!!! tip "SSO behind multiple workers"
    Since **v1.5.2** the OAuth CSRF state is shared through MongoDB, so sign-in
    works with any number of workers or replicas. On earlier versions the state
    was per-process and the callback only succeeded when it happened to reach the
    process that issued it. See [Security](../../features/security.md#oauth-callback-security).

**Behavior:**

- Users register or are created by admins, unless [registration is disabled](#registration)
- A first SSO sign-in creates the account, under the same rule
- JWT-based authentication (RS256)
- Admin and regular users; owner, editor and viewer on each project and dashboard

## :material-laptop: Single-user mode { #single-user-mode }

For an instance only you use: there is no sign-in page, and every visitor is signed in as
the admin.

**Turn it on:** with the root `docker-compose.yaml` it is already on. Otherwise:

=== "Environment"

    ```bash
    DEPICTIO_AUTH_SINGLE_USER_MODE=true
    ```

=== "Helm values"

    ```yaml
    backend:
      env:
        DEPICTIO_AUTH_SINGLE_USER_MODE: "true"
    ```

**Behavior:**

- The session is the bootstrap admin's (`DEPICTIO_BOOTSTRAP_ADMIN_EMAIL`): whoever reaches
  the URL can do anything, so keep the instance on your machine or a private network
- Projects, dashboards and every admin page are available at once
- The sidebar shows *Single user mode*
- Provisioning and magic links are refused (403)
- Set together with public mode, single-user mode wins

## :material-earth: Public mode { #public-mode }

For a public showcase: there is no sign-in page, and every visitor gets a guest account of
their own.

**Turn it on:**

=== "Environment"

    ```bash
    DEPICTIO_AUTH_PUBLIC_MODE=true
    # Optional: how long a guest account lives (default 24 hours, plus minutes)
    DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24
    DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_MINUTES=0
    ```

=== "Helm values"

    ```yaml
    backend:
      env:
        DEPICTIO_AUTH_PUBLIC_MODE: "true"
        DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS: "24"
    ```

`DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true` is still read as an alias. To ask visitors for a
shared code first, add an [access code](#public-access-code).

**Behavior:**

- On the first page load, the viewer creates a guest account, `temp_user_<id>@depictio.temp`,
  and signs the visitor in with it: no modal, no shared anonymous user. The account and what
  it made are removed when it expires
- A guest reads the public dashboards and can duplicate one into a copy of their own, which
  expires with the account
- Creating a project, importing a dashboard or registering is refused (403) for anyone but
  an admin; admins and project editors can import <small>(v1.21.0+)</small>
- With an OpenID Connect provider enabled, a guest can [sign in](#guest-sign-in) to a
  persistent account
- A short tour of the dashboards list ends by picking a dashboard, where a
  [landing hint](dashboard-guide.md#landing-hint) points to its Guide <small>(v1.17.4+)</small>
- The sidebar shows a *Public Mode* badge
- Admins can create CLI tokens in **Profile** > **CLI agents** to refresh dashboards and ingest data without switching public mode off <small>(v1.21.0+)</small>

### Signing in as a guest <small>(v1.17.3+)</small> { #guest-sign-in }

When Google or another identity provider is configured, a guest finds **Sign in** where
they would need it: the avatar menu, the sidebar's mode line (*Public mode · Sign in*),
the profile page, the tour's welcome step and, when
[viewers may comment](../../features/comments-annotations.md#viewers-can-comment), the
comments buttons, which open a *Sign in to comment* prompt. `/auth/login` shows the
sign-in form with **Continue as guest**, and a sign-in returns to the page it started
from. A public instance with password sign-in only behaves as before.

A public showcase where signed-in readers comment combines `DEPICTIO_AUTH_PUBLIC_MODE`,
an identity provider and `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT`. Keep
[registration](#registration) open, or a first-time reader's account is never created.

## :material-compass-outline: Demo mode { #demo-mode }

Public mode run as a read-only demo: the same guest accounts, without a prompt to sign in.

**Turn it on:** set both. Demo mode alone does not open the instance: without public mode,
visitors meet the sign-in page.

=== "Environment"

    ```bash
    DEPICTIO_AUTH_PUBLIC_MODE=true
    DEPICTIO_AUTH_DEMO_MODE=true
    ```

=== "Helm values"

    ```yaml
    backend:
      env:
        DEPICTIO_AUTH_PUBLIC_MODE: "true"
        DEPICTIO_AUTH_DEMO_MODE: "true"
    ```

**Behavior:**

- Everything in public mode: guest accounts, the access code, the same explorer tour
- Guests are never offered **Sign in**, even with an identity provider; an admin signs in at
  `/auth/login`
- No landing hint on dashboards, the tour does that job
- Monitoring is off even for an admin, and profile pictures cannot be changed
- The sidebar shows a *Demo Mode* badge

## Pipeline provisioning and magic links (v1.1.3+)

A pipeline often finishes before its owner has an account. Provisioning closes
that gap: `depictio ingest <results dir> --user alice@example.org` creates-or-gets the
account, runs as them, and prints a passwordless link to the dashboard it just
imported.

Set the shared secret on the instance:

```bash
DEPICTIO_AUTH_PROVISIONING_API_KEY=<a long random string>
```

**The provisioning endpoints are disabled while this is unset**, so an instance
that never sets it cannot have accounts created this way. The CLI must present
the same value, through `--provisioning-key` or the identically-named variable.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPICTIO_AUTH_PROVISIONING_API_KEY` | unset | Shared secret for `POST /depictio/api/v1/auth/provision_user`. Unset disables provisioning entirely. |
| `DEPICTIO_AUTH_MAGIC_LINK_EXPIRY_MINUTES` | see [reference](../../installation/env-reference.md#authentication) | How long a magic link stays redeemable. |

!!! warning "Treat the key like a password"
    Anyone holding it can create accounts on the instance. Keep it separate
    from `DEPICTIO_AUTH_INTERNAL_API_KEY` (alias `DEPICTIO_AUTH_INTERNAL_API_KEY_ENV`), whose scope is deliberately
    different. Pass it through a secret store rather than a shell history, and
    rotate it if a CI log ever captures it.

A magic link is single-use and expires; redeeming it exchanges the ticket for a
normal session. Sending it to the user is the pipeline's job; Depictio only
emits it on stdout.

## Restricting access

Three switches, all opt-in, all independent of the four modes above.

### Self-service registration { #registration }

Set it on an instance where accounts are provisioned by an admin rather than claimed by whoever finds the URL:

```bash
DEPICTIO_AUTH_REGISTRATION_DISABLED=true
```

**Behavior:**

- `POST /auth/register` returns 403, and the Register view and the link to it are hidden
- [OpenID Connect sign-in](../../installation/sso/index.md) becomes a login-only door: a known email signs in, an unknown one is refused instead of being provisioned an account
- Existing accounts, roles and permissions are untouched
- An administrator can still create accounts with [Add user](web_ui.md#add-a-user) (v1.19.0+)

### Password sign-in <small>(v1.8.2+)</small> { #password-login }

Closes email and password sign-in so [single sign-on](../../installation/sso/index.md) is the only way in, for an instance whose accounts all come from one identity provider:

```bash
DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED=true
```

**Behavior:**

- `POST /auth/login` refuses before reading any credential, so a valid password is not a way around the setting, and the sign-in card hides the form rather than showing one that always fails
- Ignored unless at least one OpenID Connect provider is enabled and configured, so forgetting the variables gives you the password form back instead of a locked instance
- Since v1.19.0 it also closes `POST /auth/register` (403), and the refusal says to use single sign-on
- `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD` is no longer required: SSO matches the admin by email, so pointing `DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` at your own address at the identity provider is what makes you the admin, with no seeded local account

### Public-mode access code <small>(v1.8.2+)</small> { #public-access-code }

Public mode hands a temporary session to anyone who loads the page. A code makes the instance link-shareable without being world-open:

```bash
DEPICTIO_AUTH_PUBLIC_MODE=true
DEPICTIO_AUTH_PUBLIC_ACCESS_CODE=your-shared-code
```

**Behavior:**

- A visitor enters the code before a temporary user is minted, and still gets their own throwaway account: it is a shared secret, not a login
- Checked in `/auth/public/create_temporary_user` after the rate limiter, so it is no more brute-forceable than any other credential there
- Ignored outside public and demo mode

On Kubernetes, the first two go under `backend.env` in your values file, and the access
code under `secrets.publicAccessCode`, which keeps it in the Secret.

## Choosing a Mode

```
Personal analytics tool?          → Single-User Mode
Team/org with user accounts?      → Auth Mode (Helm default)
Public dashboard gallery?         → Public Mode
Product demo or guided tutorial?  → Demo Mode
```

## Related

- [Configuration Guide](../../installation/configuration.md): full environment variable reference
- [Environment Reference](../../installation/env-reference.md): all 160+ variables
