---
title: SSO provider recipes
description: Step-by-step OpenID Connect setup for Keycloak, Google, Authentik and any other compliant identity provider.
icon: material/puzzle-outline
---

# :material-puzzle-outline: Provider recipes

Ready-to-adapt settings for common identity providers. The keys are described in the
[configuration reference](configuration.md#provider-keys).

All values are placeholders: replace `idp.example.org`, the realm and client
credentials with your own. In every recipe the redirect URI to register is
`https://depictio.example.org/depictio/api/v1/auth/oidc/<id>/callback`, with the `<id>` of
that recipe.

---

## :material-key-chain-variant: Keycloak { #recipe-keycloak }

1. In the realm, create a client: **Client type** OpenID Connect, **Client ID** `depictio`,
   **Client authentication** on, **Standard flow** on (direct access grants and implicit
   flow off).
2. **Valid redirect URIs**:
   `https://depictio.example.org/depictio/api/v1/auth/oidc/keycloak/callback`.
3. In the client's **Advanced** settings, set **Proof Key for Code Exchange Code Challenge
   Method** to `S256`.
4. Copy the secret from the **Credentials** tab.
5. For groups, add a **Group Membership** mapper to the client's dedicated scope with
   **Token Claim Name** `groups`, **Full group path** off (to get `lab` rather than
   `/lab`), and **Add to ID token** on. To use realm roles instead, read the built-in
   dotted claim `realm_access.roles`.

```bash
DEPICTIO_AUTH_OIDC_PROVIDERS='[
  {
    "id": "keycloak",
    "label": "Sign in with your institution",
    "issuer": "https://idp.example.org/realms/example",
    "claims": {
      "groups": "groups",
      "display_name": "name",
      "login": "preferred_username"
    }
  }
]'
DEPICTIO_AUTH_OIDC_KEYCLOAK_CLIENT_ID=depictio
DEPICTIO_AUTH_OIDC_KEYCLOAK_CLIENT_SECRET=change-me
```

For realm roles, use `"groups": "realm_access.roles"`. Keycloak also lists its built-in
roles (such as `offline_access`) in that claim, and they would become groups.

---

## :material-google: Google { #recipe-google }

1. In the [Google Cloud Console](https://console.cloud.google.com/), under **APIs &
   Services** > **Credentials**, create an **OAuth client ID** of type **Web application**.
2. **Authorized redirect URIs**:
   `https://depictio.example.org/depictio/api/v1/auth/oidc/google/callback`.
3. Configure the consent screen. Choose **Internal** to restrict sign-in to your Google
   Workspace organization.

```bash
DEPICTIO_AUTH_OIDC_PROVIDERS='[
  {
    "id": "google",
    "label": "Sign in with Google",
    "discovery_url": "https://accounts.google.com/.well-known/openid-configuration",
    "claims": { "display_name": "name" },
    "authorize_params": { "hd": "example.org", "prompt": "select_account" }
  }
]'
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_ID=1234567890-example.apps.googleusercontent.com
DEPICTIO_AUTH_OIDC_GOOGLE_CLIENT_SECRET=change-me
```

- `hd` in `authorize_params` only **hints** the Workspace domain to the account chooser; it
  is not enforced on its own. To restrict sign-in for real, use an **Internal** consent
  screen, or close registration so that only pre-provisioned accounts can sign in.
- Google sends **no groups claim**, so there is no group sync. Leave `claims.groups` unset.
- Google sends `email_verified`, so `assume_email_verified` is not needed.

---

## :material-tools: Authentik and other providers { #recipe-generic }

Any compliant provider works the same way. In **Authentik**, create an **OAuth2/OpenID
Provider** with client type *Confidential*, the redirect URI
`https://depictio.example.org/depictio/api/v1/auth/oidc/authentik/callback` (strict
matching), and the scopes `openid email profile`. Attach it to an application; the issuer
is `https://idp.example.org/application/o/<application-slug>/`. For groups, add a scope
mapping that returns a `groups` claim.

```bash
DEPICTIO_AUTH_OIDC_PROVIDERS='[
  {
    "id": "authentik",
    "label": "Sign in with Authentik",
    "issuer": "https://idp.example.org/application/o/depictio/",
    "claims": { "groups": "groups", "display_name": "name", "login": "preferred_username" }
  }
]'
DEPICTIO_AUTH_OIDC_AUTHENTIK_CLIENT_ID=change-me
DEPICTIO_AUTH_OIDC_AUTHENTIK_CLIENT_SECRET=change-me
```

For another provider: open its **discovery document**
(`/.well-known/openid-configuration`), use its `issuer` value verbatim, and add to `scopes`
any extra scope it needs to release groups.
