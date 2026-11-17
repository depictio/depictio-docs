---
title: SSO provider recipes
description: Step-by-step OpenID Connect setup for Keycloak, Google, Microsoft Entra ID, Authentik and any other compliant identity provider.
icon: material/puzzle-outline
---

# :material-puzzle-outline: Provider recipes

Ready-to-adapt settings for common identity providers. The keys are described in the
[configuration reference](configuration.md#provider-keys).

All values are placeholders: replace `idp.example.org`, the realm, tenant and client
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

## :material-microsoft: Microsoft Entra ID { #recipe-entra }

1. In the Entra admin center, under **App registrations**, register a new application
   (single tenant, unless you know you need more).
2. **Redirect URI**, platform **Web**:
   `https://depictio.example.org/depictio/api/v1/auth/oidc/entra/callback`.
3. Under **Certificates & secrets**, create a client secret.
4. Use the **tenant-specific** issuer, `https://login.microsoftonline.com/<tenant-id>/v2.0`.
   The generic `common` or `organizations` endpoints return tokens whose issuer contains
   the signing-in user's own tenant id, which can never match a fixed configured issuer.
5. For groups, under **Token configuration** > **Add groups claim**, choose the group types
   you need, and emit the `groups` claim in the ID token.

```bash
DEPICTIO_AUTH_OIDC_PROVIDERS='[
  {
    "id": "entra",
    "label": "Sign in with Microsoft",
    "issuer": "https://login.microsoftonline.com/<tenant-id>/v2.0",
    "claims": { "groups": "groups", "display_name": "name" }
  }
]'
DEPICTIO_AUTH_OIDC_ENTRA_CLIENT_ID=00000000-0000-0000-0000-000000000000
DEPICTIO_AUTH_OIDC_ENTRA_CLIENT_SECRET=change-me
```

Two Entra specifics:

- **Group claim values are object ids** (GUIDs) by default, not names. Depictio takes group
  names verbatim, so groups would be named after GUIDs. Configure the groups claim to emit
  group names where Entra supports it (groups synchronized from on-premises Active
  Directory), or keep the GUIDs. A user in too many groups (more than 200 in a JWT) gets an
  **overage**: the token carries no `groups` claim, only a pointer to Microsoft Graph, which
  Depictio does not follow. Because an absent claim removes the user from every SSO-managed
  group (see [Group claim semantics](groups-and-access.md#group-claim-semantics)), restrict
  the claim to the groups assigned to the application to avoid it.
- **`email` may be absent**, for accounts without a mailbox, and Entra never sends
  `email_verified`. If your users' sign-in names are their email addresses, you can map the
  email to `preferred_username`:

    ```json
    "claims": { "email": "preferred_username" },
    "assume_email_verified": true
    ```

    !!! warning "Only with a directory you control"
        `assume_email_verified` tells Depictio to trust the address without any proof from
        the IdP, and `preferred_username` is a display-oriented claim. This is safe only for
        a single-tenant app whose directory you administer, where users cannot choose their
        own sign-in name; never with a multi-tenant or external-guest configuration.

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
