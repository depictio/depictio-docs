# Authentication Modes

Depictio supports four authentication modes, each designed for a different deployment scenario. Only one mode is active at a time.

## Quick comparison

- **[Auth](#auth-mode)** · default

  ______________________________________________________________________

  For teams. Everyone signs in to an account of their own, with a role on each project.

  Nothing to set with Helm. With Compose, `DEPICTIO_AUTH_SINGLE_USER_MODE=false`.

- **[Single-user](#single-user-mode)**

  ______________________________________________________________________

  For your own instance. No sign-in page: every visitor is signed in as the admin.

  `DEPICTIO_AUTH_SINGLE_USER_MODE=true`

- **[Public](#public-mode)**

  ______________________________________________________________________

  For a showcase. Every visitor gets a guest account of their own; SSO can turn it into a real one.

  `DEPICTIO_AUTH_PUBLIC_MODE=true`

- **[Demo](#demo-mode)**

  ______________________________________________________________________

  Public mode as a read-only demo: the same guests, never asked to sign in.

  `DEPICTIO_AUTH_PUBLIC_MODE=true` and `DEPICTIO_AUTH_DEMO_MODE=true`

Side by side

|                                                                                                                | [Auth](#auth-mode)               | [Single-user](#single-user-mode) | [Public](#public-mode)             | [Demo](#demo-mode)              |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------- | ---------------------------------- | ------------------------------- |
| **A visitor gets**                                                                                             | The sign-in page                 | The admin's session              | A guest account, 24 h              | A guest account, 24 h           |
| **Register**                                                                                                   | unless [disabled](#registration) |                                  |                                    |                                 |
| **[SSO](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md)**                           |                                  | Not used                         | a guest [signs in](#guest-sign-in) | At `/auth/login` only           |
| **Create projects**                                                                                            |                                  |                                  | Admins only                        | Admins only                     |
| **Duplicate a dashboard**                                                                                      |                                  |                                  | the copy expires with the guest    | the copy expires with the guest |
| **[Guided tours](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#guided-tours)**          | Builder chapters                 | Builder chapters                 | Guest chapter                      | Guest chapter                   |
| **[Landing card](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/#landing-hint)** |                                  |                                  |                                    | What's new line only            |

## Auth mode default

For teams and organizations: every visitor signs in, to an account of their own, and sees what their roles allow.

**Turn it on:** it is the mode whenever the other three are off. That is the Helm chart's default. The root `docker-compose.yaml` starts in single-user mode instead, so with Compose set `DEPICTIO_AUTH_SINGLE_USER_MODE=false` in `.env`. [Single sign-on](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md) is optional, here with Google:

```
DEPICTIO_AUTH_OIDC_PROVIDERS='[{"id": "google", "label": "Sign in with Google", "discovery_url": "https://accounts.google.com/.well-known/openid-configuration"}]'
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID=your-client-id
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET=your-secret
```

```
oidc:
  providers:
    - id: google
      label: "Sign in with Google"
      discovery_url: "https://accounts.google.com/.well-known/openid-configuration"
secrets:
  oidcClients:
    google: {clientId: "<client-id>", clientSecret: "<client-secret>"}
```

SSO behind multiple workers

Since **v1.5.2** the OAuth CSRF state is shared through MongoDB, so sign-in works with any number of workers or replicas. On earlier versions the state was per-process and the callback only succeeded when it happened to reach the process that issued it. See [Security](https://depictio.github.io/depictio-docs/latest/features/security/#oauth-callback-security).

**Behavior:**

- Users register or are created by admins, unless [registration is disabled](#registration)
- A first SSO sign-in creates the account, under the same rule
- JWT-based authentication (RS256)
- Admin and regular users; owner, editor and viewer on each project and dashboard

## Single-user mode

For an instance only you use: there is no sign-in page, and every visitor is signed in as the admin.

**Turn it on:** with the root `docker-compose.yaml` it is already on. Otherwise:

```
DEPICTIO_AUTH_SINGLE_USER_MODE=true
```

```
backend:
  env:
    DEPICTIO_AUTH_SINGLE_USER_MODE: "true"
```

**Behavior:**

- The session is the bootstrap admin's (`DEPICTIO_BOOTSTRAP_ADMIN_EMAIL`): whoever reaches the URL can do anything, so keep the instance on your machine or a private network
- Projects, dashboards and every admin page are available at once
- The sidebar shows *Single user mode*
- Provisioning and magic links are refused (403)
- Set together with public mode, single-user mode wins

## Public mode

For a public showcase: there is no sign-in page, and every visitor gets a guest account of their own.

**Turn it on:**

```
DEPICTIO_AUTH_PUBLIC_MODE=true
# Optional: how long a guest account lives (default 24 hours, plus minutes)
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_MINUTES=0
```

```
backend:
  env:
    DEPICTIO_AUTH_PUBLIC_MODE: "true"
    DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS: "24"
```

`DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true` is still read as an alias. To ask visitors for a shared code first, add an [access code](#public-access-code).

**Behavior:**

- On the first page load, the viewer creates a guest account, `temp_user_<id>@depictio.temp`, and signs the visitor in with it: no modal, no shared anonymous user. The account and what it made are removed when it expires
- A guest reads the public dashboards and can duplicate one into a copy of their own, which expires with the account
- Creating a project, importing a dashboard or registering is refused (403) for anyone but an admin; admins and project editors can import (v1.21.0+)
- With an OpenID Connect provider enabled, a guest can [sign in](#guest-sign-in) to a persistent account
- A welcome card and a three-step [tour](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#guided-tours) of the dashboards list (v1.22.0+); on a dashboard, the [landing card](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/#landing-hint) points to its Guide (v1.17.4+)
- The sidebar shows a *Public Mode* badge
- Admins can create CLI tokens in **Profile** > **CLI agents** to refresh dashboards and ingest data without switching public mode off (v1.21.0+)

### Signing in as a guest (v1.17.3+)

When Google or another identity provider is configured, a guest finds **Sign in** where they would need it: the avatar menu, the sidebar's mode line (*Public mode · Sign in*), the profile page, the tour's welcome card and, when [viewers may comment](https://depictio.github.io/depictio-docs/latest/features/comments-annotations/#viewers-can-comment), the comments buttons, which open a *Sign in to comment* prompt. `/auth/login` shows the sign-in form with **Continue as guest**, and a sign-in returns to the page it started from. A public instance with password sign-in only behaves as before.

A public showcase where signed-in readers comment combines `DEPICTIO_AUTH_PUBLIC_MODE`, an identity provider and `DEPICTIO_COMMENTS_VIEWERS_CAN_COMMENT`. Keep [registration](#registration) open, or a first-time reader's account is never created.

## Demo mode

Public mode run as a read-only demo: the same guest accounts, without a prompt to sign in.

**Turn it on:** set both. Demo mode alone does not open the instance: without public mode, visitors meet the sign-in page.

```
DEPICTIO_AUTH_PUBLIC_MODE=true
DEPICTIO_AUTH_DEMO_MODE=true
```

```
backend:
  env:
    DEPICTIO_AUTH_PUBLIC_MODE: "true"
    DEPICTIO_AUTH_DEMO_MODE: "true"
```

**Behavior:**

- Everything in public mode: guest accounts, the access code, the same guest tour
- Guests are never offered **Sign in**, even with an identity provider; an admin signs in at `/auth/login`
- No landing card introducing a dashboard, the tour does that job; it still appears with a What's new line when a dashboard changed since the last visit
- Monitoring is off even for an admin, and profile pictures cannot be changed
- The sidebar shows a *Demo Mode* badge

## Pipeline provisioning and magic links (v1.1.3+)

A pipeline often finishes before its owner has an account. Provisioning closes that gap: `depictio ingest <results dir> --user alice@example.org` creates-or-gets the account, runs as them, and prints a passwordless link to the dashboard it just imported.

Set the shared secret on the instance:

```
DEPICTIO_AUTH_PROVISIONING_API_KEY=<a long random string>
```

**The provisioning endpoints are disabled while this is unset**, so an instance that never sets it cannot have accounts created this way. The CLI must present the same value, through `--provisioning-key` or the identically-named variable.

| Variable                                  | Default                                                                                                     | Description                                                                                          |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `DEPICTIO_AUTH_PROVISIONING_API_KEY`      | unset                                                                                                       | Shared secret for `POST /depictio/api/v1/auth/provision_user`. Unset disables provisioning entirely. |
| `DEPICTIO_AUTH_MAGIC_LINK_EXPIRY_MINUTES` | see [reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#authentication) | How long a magic link stays redeemable.                                                              |

Treat the key like a password

Anyone holding it can create accounts on the instance. Keep it separate from `DEPICTIO_AUTH_INTERNAL_API_KEY` (alias `DEPICTIO_AUTH_INTERNAL_API_KEY_ENV`), whose scope is deliberately different. Pass it through a secret store rather than a shell history, and rotate it if a CI log ever captures it.

A magic link is single-use and expires; redeeming it exchanges the ticket for a normal session. Sending it to the user is the pipeline's job; Depictio only emits it on stdout.

## Restricting access

Three switches, all opt-in, all independent of the four modes above.

### Self-service registration

Set it on an instance where accounts are provisioned by an admin rather than claimed by whoever finds the URL:

```
DEPICTIO_AUTH_REGISTRATION_DISABLED=true
```

**Behavior:**

- `POST /auth/register` returns 403, and the Register view and the link to it are hidden
- [OpenID Connect sign-in](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md) becomes a login-only door: a known email signs in, an unknown one is refused instead of being provisioned an account
- Existing accounts, roles and permissions are untouched
- An administrator can still create accounts with [Add user](https://depictio.github.io/depictio-docs/latest/usage/guides/web_ui/#add-a-user) (v1.19.0+)

### Password sign-in (v1.8.2+)

Closes email and password sign-in so [single sign-on](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md) is the only way in, for an instance whose accounts all come from one identity provider:

```
DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED=true
```

**Behavior:**

- `POST /auth/login` refuses before reading any credential, so a valid password is not a way around the setting, and the sign-in card hides the form rather than showing one that always fails
- Ignored unless at least one OpenID Connect provider is enabled and configured, so forgetting the variables gives you the password form back instead of a locked instance
- Since v1.19.0 it also closes `POST /auth/register` (403), and the refusal says to use single sign-on
- `DEPICTIO_BOOTSTRAP_ADMIN_PASSWORD` is no longer required: SSO matches the admin by email, so pointing `DEPICTIO_BOOTSTRAP_ADMIN_EMAIL` at your own address at the identity provider is what makes you the admin, with no seeded local account

### Public-mode access code (v1.8.2+)

Public mode hands a temporary session to anyone who loads the page. A code makes the instance link-shareable without being world-open:

```
DEPICTIO_AUTH_PUBLIC_MODE=true
DEPICTIO_AUTH_PUBLIC_ACCESS_CODE=your-shared-code
```

**Behavior:**

- A visitor enters the code before a temporary user is minted, and still gets their own throwaway account: it is a shared secret, not a login
- Checked in `/auth/public/create_temporary_user` after the rate limiter, so it is no more brute-forceable than any other credential there
- Ignored outside public and demo mode

On Kubernetes, the first two go under `backend.env` in your values file, and the access code under `secrets.publicAccessCode`, which keeps it in the Secret.

## Choosing a Mode

- **Just you**, on a laptop or a workstation: single-user mode, the default of the Docker Compose quick start.
- **A team** with accounts and roles: auth mode, the Helm chart's default.
- **A public gallery** of dashboards anyone can open: public mode.
- **A product demo** or a guided tutorial: demo mode.

## Related

- [Configuration Guide](https://depictio.github.io/depictio-docs/latest/installation/configuration/index.md): full environment variable reference
- [Environment Reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/index.md): all 160+ variables
