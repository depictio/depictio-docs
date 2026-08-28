---
title: Branding
description: Give a deployment its own logo, name, colours, typography and figure palette, and let a single dashboard override any of it.
---

# :material-palette-outline:{ style="color: #9966CC" } Branding <small>(v1.8.0+)</small>

Depictio ships in a neutral Mantine look. A deployment can replace it with its own logo, name, colours, chrome surfaces, typography and figure palette, and a single dashboard can override any of it. All of that is one object, the **brand theme**, so every place you can set it takes the same fields.

## Where it can be set

```text
Mantine defaults  <-  DEPICTIO_BRANDING_*  <-  /admin overrides  <-  dashboard
```

| Layer | Set from | Needs a redeploy |
| --- | --- | --- |
| Deployment defaults | `DEPICTIO_BRANDING_*` environment variables. See [Environment Reference](../../installation/env-reference.md#branding) | Yes |
| Instance overrides | **Administration → Branding** at `/admin`, saved server-side | No |
| Dashboard override | The dashboard's Settings drawer, or `brand_theme:` in its YAML | No |

Each layer states only what differs and inherits the rest. That is what makes a dashboard's *inherit the instance* real rather than a copy: change the instance logo and every dashboard that never uploaded its own follows.

!!! info "Availability"
    The layered engine landed in **v1.8.0** ([#1003](https://github.com/depictio/depictio/pull/1003)). Dashboards carrying the older `logo_url` or `plot_theme` fields fold into `brand_theme` on read and keep working.

**Administration → Branding** puts the whole theme on one page, with a live preview that renders real components under the draft, in either colour scheme:

[![The Branding panel in /admin](../../images/guides/branding/branding-admin-panel_light.webp#only-light)](../../images/guides/branding/branding-admin-panel_light.webp){target=_blank}

[![The Branding panel in /admin](../../images/guides/branding/branding-admin-panel_dark.webp#only-dark)](../../images/guides/branding/branding-admin-panel_dark.webp){target=_blank}

## The fields

The admin form groups them as below, and a dashboard override offers the same set.

| Group | Fields |
| --- | --- |
| Identity | `app_name` (browser tab title and login greeting), `logo_url`, `logo_url_dark`, and `logo_mode`: `inherit` (the default), `custom` or `none` |
| Brand palette | `primary`, `secondary`, `tertiary`, each a hex colour or a Mantine palette name (`blue`, `teal`, `grape`, and so on) |
| Status colours | `success`, `warning`, `danger`, held outside the brand reach so pass, warn and fail keep reading as meaning rather than as decoration |
| Reach | `tint_mode`: `accent` (the default) re-tints the primary accent only, `full` carries all three brand colours into buttons, tabs, badges and section accents. `gray`, `red`, `green` and `yellow` are never remapped in either mode |
| Surfaces | `surfaces_light` and `surfaces_dark`, each holding `app_bg` (page), `section_bg` (cards and panels), `nav_bg` (header and sidebar) and `heading` (title text). Hex only, since these become raw CSS values |
| Typography and shape | `font_family`, `headings_font_family`, `default_radius` (a Mantine token, `xs` to `xl`) |
| Figures | `plots.template` for figures whose component picks none, unset meaning *follow the UI colour scheme*; `plots.colorway` and `plots.sequential` for the categorical and continuous palettes |

!!! warning "Fonts are not fetched for you"
    A named font has to be installed on the viewer's machine or served by the deployment. An unavailable font fails silently, so the admin form renders a live sample of what you typed.

## Derived values

`colorway`, `sequential` and the Mantine shade tuples are derived from the brand palette whenever you leave them unset, so figures follow the brand without a second list to keep in step. The derivation runs server-side, once, and the resolved theme is what `/utils/public-config` serves, so a dashboard's figures and the chrome around them cannot drift apart. State `colorway` or `sequential` yourself and the derivation steps aside for that field alone.

A hex brand colour is expanded into a 10-shade tuple with **your colour on shade 6**, the shade a filled control actually paints in light mode (8 in dark). Generic generators place the input by its lightness instead, which for a dark brand leaves every button a washed-out cousin of it. The colorway walks the brand hues before rotating hue, so a figure's first series are recognisably the brand.

!!! note "`palettes` is output, not input"
    The resolved theme carries a `palettes` object holding the derived tuples, keyed by role. The server fills it in and authors never set it, in the environment, in the admin panel or in YAML.

## Presets, import and export

**Presets** seeds the form from a starting point, namely the stock Depictio look, TREC, EMBL or Ocean, also settable at deploy time with `DEPICTIO_BRANDING_PRESET`. Everything a preset fills in stays editable, and the flat environment variables override it field by field. **Export** writes the current theme as JSON and **Import** reads one back, so a brand can be version-controlled and moved between deployments.

[![The Presets menu](../../images/guides/branding/branding-presets.webp)](../../images/guides/branding/branding-presets.webp){target=_blank}

## A dashboard override

From a dashboard in edit mode: **Settings → Appearance → Branding → Customise**. The same fields appear, with the instance's values shown as placeholders. The override applies to that dashboard's page only, so it can wear its own identity inside a differently branded instance. See [Using the dashboard](../guides/dashboard_usage.md#appearance) for the rest of the Appearance section.

[![A dashboard wearing its own brand](../../images/guides/branding/dashboard-brand-override.webp)](../../images/guides/branding/dashboard-brand-override.webp){target=_blank}

In YAML it is a top-level `brand_theme:` block. The bundled penguins demo carries one as a worked example:

```yaml
brand_theme:
  primary: "#159090"    # Gentoo
  secondary: "#a034f0"  # Chinstrap
  tertiary: "#ff8c00"   # Adelie
  tint_mode: "full"
```

!!! warning "Uploaded logos do not travel"
    Logos uploaded through the UI are stripped on export, since the file lives on the instance that received it. Use `logo_url` with an absolute address for a logo that should survive a move.

## See Also

- [Environment Reference](../../installation/env-reference.md#branding) for every `DEPICTIO_BRANDING_*` variable
- [Using the dashboard](../guides/dashboard_usage.md#appearance) for the per-dashboard Appearance controls
- [Components](../../features/components.md#figure-components) for the per-figure theme and font scale
