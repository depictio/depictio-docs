---
title: From Google OAuth to OIDC
description: Move an existing Google OAuth sign-in to OpenID Connect, with the variable-by-variable mapping.
icon: material/swap-horizontal
---

# :material-swap-horizontal: From Google OAuth to OIDC

<a id="from-google-oauth-to-oidc"></a>

Existing accounts are matched by email, so nobody loses their projects, dashboards or group
memberships when you switch.

Google is now a plain OIDC provider: the dedicated Google sign-in code is gone. The old
variables **keep working for one release** and are mapped onto a provider with the id
`google`, the label *Sign in with Google* and the Google discovery URL. The API logs a
deprecation warning at startup while they are set, and an explicit `google` entry in
`DEPICTIO_AUTH_OIDC_PROVIDERS` wins over them.

| Old variable | New setting |
|--------------|-------------|
| `DEPICTIO_AUTH_GOOGLE_OAUTH_ENABLED` | declare the provider (`enabled`) |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_ID` | `DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID` |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_CLIENT_SECRET` | `DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET` |
| `DEPICTIO_AUTH_GOOGLE_OAUTH_REDIRECT_URI` | `redirect_uri` (or drop it, see below) |

The redirect URI registered in Google can stay as it was: the old value is the viewer URL
`https://<host>/auth/google/callback`, and that viewer path now forwards the browser, with
its query string, to the API callback `/depictio/api/v1/auth/oidc/google/callback`. To move
to the new default, add `https://<api-host>/depictio/api/v1/auth/oidc/google/callback` to
the authorized redirect URIs in the Google Cloud Console, remove the `redirect_uri`
override, and delete the old URI once nothing uses it.

Move to the [Google recipe](providers.md#recipe-google) before the legacy variables are removed. Google
accounts keep working unchanged: they are matched by email.
