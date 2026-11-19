# Unauthenticated Mode

!!! warning "Renamed to Public Mode"

    This page describes the legacy "Unauthenticated Mode" which has been renamed to **Public Mode**. The env var `DEPICTIO_AUTH_UNAUTHENTICATED_MODE` still works as a backward-compatible alias. See [Authentication Modes](authentication-modes.md) for the full overview of all four modes.

## Overview

### What is Unauthenticated Mode?

Each visitor lands on the **Dashboards** page with a temporary guest account, created without a form. The sidebar reads **Public mode**. A guest sees the public dashboards and can use their filters and figures. The account expires after `DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS`.

Earlier versions first landed a visitor as a shared anonymous user, with a modal to switch to a temporary account. That step is gone: every visitor gets a temporary account at once.

Example unauthenticated mode URL is available on documentation landing page: [https://depictio.github.io/depictio-docs/latest/](https://depictio.github.io/depictio-docs/latest/).

## Screenshots

[![The Dashboards page as a guest: the public demo dashboards, Public mode in the sidebar and the TU avatar](../../images/guides/public-mode/guest_dashboards_light.webp#only-light){ width="800" }](../../images/guides/public-mode/guest_dashboards_light.webp){target=_blank}
[![The Dashboards page as a guest: the public demo dashboards, Public mode in the sidebar and the TU avatar](../../images/guides/public-mode/guest_dashboards_dark.webp#only-dark){ width="800" }](../../images/guides/public-mode/guest_dashboards_dark.webp){target=_blank}

**Account settings** shows the guest's temporary account: a `temp_user_…@depictio.temp` email and the **User** role.

[![Account settings of a guest: a temp_user email at depictio.temp, role User, no groups](../../images/guides/public-mode/guest_account_light.webp#only-light){ width="800" }](../../images/guides/public-mode/guest_account_light.webp){target=_blank}
[![Account settings of a guest: a temp_user email at depictio.temp, role User, no groups](../../images/guides/public-mode/guest_account_dark.webp#only-dark){ width="800" }](../../images/guides/public-mode/guest_account_dark.webp){target=_blank}

`/auth/login` opens the sign-in form with **Continue as guest**, to sign in with an account or keep the guest session.

[![The sign-in form in public mode, with Continue as guest under Sign in](../../images/guides/public-mode/guest_sign_in_light.webp#only-light){ width="405" }](../../images/guides/public-mode/guest_sign_in_light.webp){target=_blank}
[![The sign-in form in public mode, with Continue as guest under Sign in](../../images/guides/public-mode/guest_sign_in_dark.webp#only-dark){ width="405" }](../../images/guides/public-mode/guest_sign_in_dark.webp){target=_blank}

## Configuration

### Environment Variables

Enable unauthenticated mode by setting these environment variables:

```bash
# Enable public mode (DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true still works)
DEPICTIO_AUTH_PUBLIC_MODE=true

# Configure anonymous user settings
DEPICTIO_AUTH_ANONYMOUS_USER_EMAIL=anonymous@depict.io
DEPICTIO_AUTH_TEMPORARY_USER_EXPIRY_HOURS=24
```

### Helm Deployment

For Kubernetes deployments, use the provided values files:

```bash
# Deploy with unauthenticated mode
helm upgrade --install your-release ./helm-charts/depictio \
  -f ./helm-charts/depictio/values.yaml \
  -f ./helm-charts/depictio/values-unauth.yaml \
  -n your-namespace
```

## Limitations

- **Session-Based**: Data and dashboards expire after configured time
- **No Persistence**: User data is not permanently stored
- **No User Management**: No user accounts, groups, or permissions
- **Temporary Storage**: All content is ephemeral

## Use Cases

### Scientific Outreach and Demonstrations

- Public sharing of dashboards
- Public demos and presentations

### Educational Use

- Training sessions
- Workshops and tutorials
- Proof-of-concept deployments

## Security Considerations

- **Public Access**: Anyone can access the deployment
- **Data Sensitivity**: Only use with non-sensitive, public data (e.g., public & published datasets ; data powering the visualizations could be extracted from the dashboard by scrapping the page)
- **Resource Limits**: Configure appropriate resource constraints
- **Network Security**: Use proper network isolation and ingress controls
