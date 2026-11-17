---
title: SSO troubleshooting and security
description: Error codes of a failed OpenID Connect sign-in, their common causes, and the protections the login flow applies.
icon: material/stethoscope
---

# :material-stethoscope: Troubleshooting and security

What to check when an OpenID Connect sign-in fails, and what the flow protects against.

---

## :material-bug-outline: Troubleshooting { #troubleshooting }

A failed sign-in always ends at `/auth?error=<code>` with a short code, to keep details out
of the browser. **The reason is in the API logs** (`docker logs depictio-backend`, or
`kubectl logs` on the backend pod): search for `OIDC`.

| Code | Meaning | Where to look |
|------|---------|---------------|
| `sso_failed` | The login could not be completed: unknown or reused `state`, token exchange refused, invalid `id_token`, no usable email claim, or an unexpected error | The warning `OIDC login with '<id>' failed: …` names the reason |
| `sso_cancelled` | The user denied access or cancelled at the IdP (`access_denied`) | Nothing to fix; the IdP may also deny by policy |
| `sso_unavailable` | The provider is unknown or disabled, or its discovery document could not be fetched | `OIDC provider '<id>' discovery failed: …`, or an unknown provider id in the URL |
| `registration_disabled` | The email has no account and `DEPICTIO_AUTH_REGISTRATION_DISABLED` is on | Create the account first, or reopen registration |
| `email_not_verified` | The IdP did not assert `email_verified: true` | `provider '<id>' did not verify …`: fix the IdP, or set `assume_email_verified` if appropriate |

Common causes:

- **Issuer mismatch.** The `issuer` you configured must equal the `issuer` field of the
  discovery document, and the `iss` of the tokens, character for character (scheme, host,
  path, realm). Open `<issuer>/.well-known/openid-configuration` and copy the value. For
  Entra ID, use the tenant-specific issuer.
- **Redirect URI mismatch.** The IdP rejects the authorization request, before Depictio is
  involved, when the callback differs from the registered one. Compare it with
  `https://<api-host>/depictio/api/v1/auth/oidc/<id>/callback`, mind the scheme (`https`
  behind a TLS-terminating proxy) and set `redirect_uri` if Depictio builds a different
  host than the public one.
- **Clock skew.** `exp` and `iat` are checked with 60 seconds of leeway. A larger drift
  between the API host and the IdP makes the `id_token` look expired or not yet valid:
  synchronize clocks (NTP).
- **No button.** The provider is disabled, or lacks an issuer or client id or secret: the
  startup log has `OIDC provider '<id>' is enabled but lacks …`.
  `GET /depictio/api/v1/auth/oidc/providers` lists what is shown.
- **Groups disappear.** The groups claim is missing from the token; see
  [Group claim semantics](groups-and-access.md#group-claim-semantics).
- **Startup error about SAML.** A line starting `SAML SSO has been removed and these
  variables are IGNORED` lists each `DEPICTIO_AUTH_SAML_*` variable found and the OIDC
  setting that replaces it: see [From SAML to OIDC](migration.md#from-saml-to-oidc).
- **`sso_failed` after a long pause at the IdP.** The `state` lives 10 minutes; start again.

---

## :material-shield-lock-outline: Security { #security }

- A callback is accepted only if it answers a login this instance started, and only once:
  the `state` is consumed atomically, so a replay finds nothing.
- Authorization-code interception is covered by PKCE (`S256`), and ID-token replay by the
  `nonce`. Tokens are verified against the IdP's JWKS, which is re-fetched when the IdP
  rotates keys.
- The redirect URI comes from the configuration, never from the request, and a `next` path
  stays on this site.
- The browser is handed a single-use ticket in the URL fragment, redeemed by the viewer.

See [OpenID Connect sign-in](../../features/security.md#oidc-sign-in) on the Security page.
