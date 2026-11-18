# Configuration reference

Every setting of [OpenID Connect single sign-on](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md): the variables, the keys of a provider entry, which claims feed the account, and the callback to register at the IdP.

______________________________________________________________________

## Environment variables

| Variable                                | Default   | Description                                                                                                                                                |
| --------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEPICTIO_AUTH_OIDC_PROVIDERS`          | *(empty)* | JSON list of provider objects, see [provider keys](#provider-keys)                                                                                         |
| `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_ID`     | -         | Client id of provider `<ID>`. Overrides `client_id` in the list                                                                                            |
| `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_SECRET` | -         | Client secret of provider `<ID>`. Overrides `client_secret` in the list                                                                                    |
| `DEPICTIO_AUTH_REGISTRATION_DISABLED`   | `false`   | SSO becomes login-only: see [Closed registration](https://depictio.github.io/depictio-docs/latest/installation/sso/groups-and-access/#registration-closed) |
| `DEPICTIO_AUTH_PASSWORD_LOGIN_DISABLED` | `false`   | SSO becomes the only way in: see [SSO-only mode](https://depictio.github.io/depictio-docs/latest/installation/sso/groups-and-access/#sso-only)             |
| `DEPICTIO_VIEWER_PUBLIC_URL`            | -         | Public URL of the viewer, where the ticket hand-off and error redirects land                                                                               |

The deprecated `DEPICTIO_AUTH_GOOGLE_OAUTH_*` variables are described in [From Google OAuth to OIDC](https://depictio.github.io/depictio-docs/latest/installation/sso/migration/#from-google-oauth-to-oidc). The full variable list is in the [Environment Reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#authentication).

______________________________________________________________________

## Provider keys

Each object of `DEPICTIO_AUTH_OIDC_PROVIDERS` accepts these keys. Unknown keys are rejected.

| Key                          | Default                                                      | Description                                                                                                                                                                                 |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                         | *(required)*                                                 | Stable identifier, used in URLs and in the credential variable names. Lower case, `[a-z0-9][a-z0-9_-]{0,31}`                                                                                |
| `label`                      | `Sign in with <id>`                                          | Text of the sign-in button                                                                                                                                                                  |
| `enabled`                    | `true`                                                       | Set `false` to hide a provider without deleting it                                                                                                                                          |
| `issuer`                     | -                                                            | Expected issuer, for example `https://idp.example.org/realms/example`. Discovery defaults to `<issuer>/.well-known/openid-configuration`, and the document's `issuer` must equal this value |
| `discovery_url`              | -                                                            | Explicit discovery document URL, overriding the default derived from `issuer`                                                                                                               |
| `client_id`                  | -                                                            | Client id. Prefer `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_ID`                                                                                                                                       |
| `client_secret`              | -                                                            | Client secret. Prefer `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_SECRET`                                                                                                                               |
| `scopes`                     | `["openid", "email", "profile"]`                             | A list or a space-separated string. `openid` is always added                                                                                                                                |
| `redirect_uri`               | `<API external URL>/depictio/api/v1/auth/oidc/<id>/callback` | Callback registered at the IdP. Never read from the request                                                                                                                                 |
| `claims`                     | see [Claim mapping](#claim-mapping)                          | Which claims feed the account                                                                                                                                                               |
| `sso_provider`               | the `id`                                                     | Value stored on the user as `sso_provider`                                                                                                                                                  |
| `assume_email_verified`      | `false`                                                      | Trust the email even without `email_verified: true`. See [Email and accounts](https://depictio.github.io/depictio-docs/latest/installation/sso/#email-and-accounts)                         |
| `token_endpoint_auth_method` | `client_secret_basic`                                        | How the client authenticates at the token endpoint: `client_secret_basic`, `client_secret_post`, or `none` for a public client protected by PKCE alone                                      |
| `authorize_params`           | `{}`                                                         | Extra parameters added to the authorization request, for example `{"prompt": "select_account", "hd": "example.org"}`                                                                        |
| `fetch_userinfo`             | `true`                                                       | Also call the userinfo endpoint and merge its claims **under** the `id_token` claims, only when its `sub` matches                                                                           |

At least one of `issuer` or `discovery_url` is required, plus a client id and, unless `token_endpoint_auth_method` is `none`, a client secret.

______________________________________________________________________

## Claim mapping

`claims` maps Depictio's fields to the **names of claims** the IdP sends:

| Key            | Default   | Feeds                                                                                                      |
| -------------- | --------- | ---------------------------------------------------------------------------------------------------------- |
| `email`        | `email`   | The account email (the matching key)                                                                       |
| `groups`       | *(unset)* | SSO-managed [groups](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/index.md) |
| `display_name` | *(unset)* | The display name, for example `name`                                                                       |
| `login`        | *(unset)* | The login, for example `preferred_username`                                                                |
| `title`        | *(unset)* | The title shown in Account settings                                                                        |
| `picture`      | `picture` | The profile picture (an `https://` URL), unless the user uploaded one                                      |

- A claim value can be a string or a list of strings: IdPs disagree on whether a single group is `"lab"` or `["lab"]`, and Depictio accepts both.
- Names are matched exactly first, then ignoring case.
- A **dotted name** is read as a path into nested objects when no top-level claim carries the whole name: `realm_access.roles` reads `{"realm_access": {"roles": [...]}}`.
- A mapping left unset skips that part of the sync.

______________________________________________________________________

## Redirect URI

The default callback is `<API external URL>/depictio/api/v1/auth/oidc/<id>/callback`, built from the API's external URL setting. Register exactly that value at the IdP: a mismatch is refused by the IdP before the user ever reaches Depictio. Behind a proxy, or on a public host other than the one Depictio knows, set `redirect_uri` explicitly. Most providers only allow `https` redirect URIs outside `localhost`, so the API must be served over TLS.

______________________________________________________________________

## On Kubernetes

With the Helm chart, the provider list goes under `oidc.providers` (rendered into `DEPICTIO_AUTH_OIDC_PROVIDERS`) and the credentials under `secrets.oidcClients.<id>` (rendered into the chart's Secret as `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_ID` and `DEPICTIO_AUTH_OIDC_<ID>_CLIENT_SECRET`):

```
oidc:
  providers:
    - id: keycloak
      label: Sign in with your institution
      issuer: https://idp.example.org/realms/example
      claims:
        groups: groups
secrets:
  oidcClients:
    keycloak:
      clientId: depictio
      clientSecret: change-me
```

Keep `secrets.oidcClients` in your environment's secrets values rather than in the repository. The backend ConfigMap also exports `DEPICTIO_VIEWER_PUBLIC_URL`, which the hand-off back to the viewer needs.
