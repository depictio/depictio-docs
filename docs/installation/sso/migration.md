---
title: Migrating to OpenID Connect
description: Move an existing SAML 2.0 or Google OAuth sign-in to OpenID Connect, with the variable-by-variable mapping.
icon: material/swap-horizontal
---

# :material-swap-horizontal: Migration

Existing accounts are matched by email, so nobody loses their projects, dashboards or group
memberships when you switch. SSO-managed groups already created through SAML keep working:
the next OIDC sign-in re-syncs them from `claims.groups`.

---

## :material-transfer: From SAML to OIDC { #from-saml-to-oidc }

SAML support is **removed**. The `DEPICTIO_AUTH_SAML_*` variables are ignored, and the API
logs an **error at startup** listing each one it found with its replacement, so a forgotten
variable does not silently remove your sign-in button.

Most SAML IdPs (Keycloak, Entra ID, Authentik, Okta, ...) offer OIDC as well. In the IdP,
create an OIDC client next to the SAML one (see the [recipes](providers.md)), then map
the settings:

| Old variable | New setting |
|--------------|-------------|
| `DEPICTIO_AUTH_SAML_ENABLED` | the provider entry's `enabled` |
| `DEPICTIO_AUTH_SAML_IDP_ENTITY_ID` | `issuer` |
| `DEPICTIO_AUTH_SAML_IDP_SSO_URL` | `issuer` (discovery finds the endpoints), or `discovery_url` |
| `DEPICTIO_AUTH_SAML_IDP_CERT` | nothing: signing keys come from the IdP's JWKS |
| `DEPICTIO_AUTH_SAML_SP_ENTITY_ID` | `client_id` |
| `DEPICTIO_AUTH_SAML_SP_BASE_URL` | `redirect_uri` (the default is built from the API external URL) |
| `DEPICTIO_AUTH_SAML_NAME_ID_FORMAT` | nothing |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_EMAIL` | `claims.email` |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_USERNAME` | `claims.login` |
| `DEPICTIO_AUTH_SAML_LOGIN_LABEL` | `label` |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_GROUPS` | `claims.groups` |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_TITLE` | `claims.title` |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_DISPLAY_NAME` | `claims.display_name` |
| `DEPICTIO_AUTH_SAML_ATTRIBUTE_LOGIN` | `claims.login` |

Also needed:

- A **client secret** (`DEPICTIO_AUTH_OIDC_<ID>_CLIENT_SECRET`): SAML had none.
- The **redirect URI** registered at the IdP changes from the SAML ACS
  (`…/auth/saml/callback`) to `…/auth/oidc/<id>/callback`. The SAML metadata endpoint no
  longer exists.
- Group values: a SAML attribute and the matching OIDC claim often carry the same names,
  but check once. Names that differ create new groups, and the old ones lose their SSO
  members.
- The `saml` Python extra (`pip install "depictio[server,saml]"`) is gone: the plain
  `server` extra is enough.

For example, a Keycloak SAML setup becomes:

```bash
# before
DEPICTIO_AUTH_SAML_ENABLED=true
DEPICTIO_AUTH_SAML_IDP_ENTITY_ID=https://idp.example.org/realms/example
DEPICTIO_AUTH_SAML_IDP_SSO_URL=https://idp.example.org/realms/example/protocol/saml
DEPICTIO_AUTH_SAML_IDP_CERT=/run/secrets/idp.pem
DEPICTIO_AUTH_SAML_SP_ENTITY_ID=depictio
DEPICTIO_AUTH_SAML_LOGIN_LABEL="Sign in with your institution"
DEPICTIO_AUTH_SAML_ATTRIBUTE_GROUPS=groups

# after
DEPICTIO_AUTH_OIDC_PROVIDERS='[{
  "id": "keycloak",
  "label": "Sign in with your institution",
  "issuer": "https://idp.example.org/realms/example",
  "claims": {"groups": "groups"}
}]'
DEPICTIO_AUTH_OIDC_KEYCLOAK_CLIENT_ID=depictio
DEPICTIO_AUTH_OIDC_KEYCLOAK_CLIENT_SECRET=change-me
```

On Kubernetes, move the SAML values under `auth:` to `oidc.providers` and
`secrets.oidcClients`, as in [On Kubernetes](configuration.md#on-kubernetes).

---

## :material-google: From Google OAuth to OIDC { #from-google-oauth-to-oidc }

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
