---
title: Usage statistics
description: Self-hosted usage statistics in Admin › Activity › Usage, and the API that serves them to reports and agents.
---

# :material-chart-bar:{ style="color: #009688" } Usage statistics

<span class="ver-badge">v1.23.1+</span>

Who uses the instance, how often, from where, and what they open. The data stays in this deployment's MongoDB and is never sent anywhere. Open **Admin › Activity › Usage** (`/admin/usage`), pick **Day**, **Week**, **Month** or **Year** and the number of periods.

The pane shows the headline numbers against the previous period, then **Activity** (active users or visitors, logins, dashboard views), **New vs returning** users, **Content created** (accounts, projects, dashboards, ingestions), a weekday by hour heatmap, and top dashboards, projects, login methods, countries, browsers, devices, languages and referrers.

On by default. `DEPICTIO_USAGE_STATS_ENABLED=false` stops all recording and the routes answer 404. The variables are in the [environment reference](../../installation/env-reference.md#usage-statistics).

!!! info "Replaces the legacy analytics"
    The `DEPICTIO_ANALYTICS_*` variables are ignored, and `/analytics-data/*` is gone. The old `user_sessions` and `user_activities` collections are left in MongoDB: drop them by hand once you no longer need them.

## What is counted

A login records one row per day, user and method (`password`, `oidc:<provider>`, `magic_link`, `temporary`, `single_user`). The viewer sends one beacon per page load, which records the browser and, on a dashboard, the dashboard. `/embed` renders, bots and headless browsers send nothing or are dropped.

| Mode | Headline numbers |
| --- | --- |
| Multi-user | Active users, logins by method, new vs returning, new accounts |
| Public or demo | Visitors, unique addresses, countries, page views. Guest accounts are counted apart, never as users |
| Single-user | Page views, dashboard views, browsers |

??? info "Visitors behind one address (NAT)"
    Three counts are reported side by side: `visitors` (distinct browsers, from a random id kept in the browser, correct behind a NAT), `visitors_fp` (keyed hashes of address and user agent, a cross-check) and `unique_ips` (distinct addresses, as hashes). The *Browsers per address* table lists the addresses that carry many browsers, a way to spot institutes.

## Privacy and retention

- **No IP address or user agent is stored**: an address is kept as a keyed hash under a per-instance key, a user agent as browser, OS and device class. Referrers keep the external domain only.
- **Daily rows expire** after `DEPICTIO_USAGE_STATS_RETENTION_DAYS` (395 days, 13 months, at most 25 months). Closed months and years are kept first as anonymous totals.
- **Readers can opt out**: the **About** page has a *Privacy* notice and a switch, *Exclude this browser from usage statistics*. Browsers sending Do Not Track or Global Privacy Control are never recorded.
- **Deleting an account** deletes its rows.

As the operator, mention the statistics in your instance's privacy policy (the About notice can serve as its basis). The GDPR notes and the CNIL conditions the design follows are in [docs/usage-stats.md](https://github.com/depictio/depictio/blob/v1.23.1/docs/usage-stats.md#gdpr).

### Countries and cities

Optional. Point `DEPICTIO_USAGE_STATS_GEOIP_DB_PATH` at a City `.mmdb` file, [DB-IP Lite](https://db-ip.com/db/lite.php) (CC-BY 4.0, no key) or MaxMind GeoLite2, mounted into the backend (with Helm, set the variable in `backend.env`). Only the country and city are stored. Without the file, the geo panels are hidden.

## API for reports and agents

`GET /depictio/api/v1/analytics/usage` takes an admin token, or the internal API key in `X-Api-Key` (`DEPICTIO_AUTH_INTERNAL_API_KEY`).

```bash
# Last 12 months: KPIs with previous-period values, series, breakdowns
curl -s -H "X-Api-Key: $KEY" "https://depictio.example.org/depictio/api/v1/analytics/usage?granularity=month&periods=12"

# Weekly series as CSV
curl -s -H "X-Api-Key: $KEY" "https://depictio.example.org/depictio/api/v1/analytics/usage?granularity=week&periods=26&format=csv"
```

??? info "Query parameters"
    | Query | Default | |
    | --- | --- | --- |
    | `granularity` | `month` | `day`, `week` (ISO, Monday), `month`, `year` |
    | `periods` | `12` | Number of periods ending with the current one |
    | `start`, `end` | none | Custom range (UTC), aligned on period boundaries. `end` includes its period |
    | `format` | `json` | `csv` returns the time series only |

    The JSON holds `mode`, `totals`, `kpis` (`current` and `previous`), `series`, `breakdowns` and `hours_heatmap`. Field by field: [docs/usage-stats.md](https://github.com/depictio/depictio/blob/v1.23.1/docs/usage-stats.md#api-for-agents-and-reports).
