# Unauthenticated Mode

!!! warning "Renamed to Public Mode"

    This page describes the legacy "Unauthenticated Mode" which has been renamed to **Public Mode**. The env var `DEPICTIO_AUTH_UNAUTHENTICATED_MODE` still works as a backward-compatible alias. See [Authentication Modes](authentication-modes.md) for the full overview of all four modes.

## Overview

### What is Unauthenticated Mode?

In unauthenticated mode, user lands as a temporary anonymous user with limited access. This anonymous user can only access the existing **public dashboards** and play with the interactive features in a stateless manner (no database persistence), but cannot create or modify dashboards. This mode is ideal for quick demonstrations or public sharing of dashboards without requiring user authentication.

If the user wants to create its own dashboard, modify existing ones using the same dataset, or create its own basic project and upload a dataset, they can switch to a temporary authenticated user mode. The temporary user will have a limited session duration (24h by default), after which dashboards will be cleared.

Example unauthenticated mode URL is available on documentation landing page: [https://depictio.github.io/depictio-docs/latest/](https://depictio.github.io/depictio-docs/latest/).

## Screenshots

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/unauth_mode/landing_page.png" target="_blank">
        <img src="../../../images/guides/unauth_mode/landing_page.png" width="600">
    </a>
    <!-- Caption -->
    <p style="text-align: center;"><b>Unauthenticated mode landing page - Anonymous</b><br><i>User is logged as anonymous and needs to login to access more features (create/duplicate dashboards, create project, upload dataset)</i></p>
</div>

<!-- 1 line space -->

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/unauth_mode/modal.png" target="_blank">
        <img src="../../../images/guides/unauth_mode/modal.png" width="600">
    </a>
    <!-- Caption -->
    <p style="text-align: center;"><b>Account status switch modal</b><br><i>Once the user wants to access more features, they can switch to a temporary authenticated user mode. The user and the related session information (dashboards, projects, etc.) will be stored temporarily (24h by default).</i></p>
</div>
<!-- 1 line space -->
<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/unauth_mode/landing_page_tmp_user.png" target="_blank">
        <img src="../../../images/guides/unauth_mode/landing_page_tmp_user.png" width="600">
    </a>
    <!-- Caption -->
    <p style="text-align: center;"><b>Unauthenticated mode landing page - Temporary user</b><br><i>User is now logged in as a temporary user and can access more features (create/duplicate dashboards, create project, upload dataset) for a limited time (24h by default).</i></p>
</div>

## Configuration

### Environment Variables

Enable unauthenticated mode by setting these environment variables:

```bash
# Enable unauthenticated access
DEPICTIO_AUTH_UNAUTHENTICATED_MODE=true

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
