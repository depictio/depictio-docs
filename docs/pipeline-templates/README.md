---
title: Templates
icon: material/layers-outline
---

# Depictio Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run
```

---

## Available templates

<div style="display:flex;gap:20px;flex-wrap:wrap;margin:8px 0 24px 0;">

  <a href="nf-core/ampliseq/" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;border:1px solid var(--md-default-fg-color--lightest, #ddd);border-radius:16px;width:300px;overflow:hidden;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,0.12)'" onmouseout="this.style.boxShadow='none'">
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);display:flex;align-items:center;justify-content:center;padding:24px 16px;min-height:90px;">
      <img src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq" style="height:52px;max-width:240px;object-fit:contain;">
    </div>
    <div style="padding:16px 20px;flex:1;display:flex;flex-direction:column;gap:10px;">
      <div style="font-size:0.82em;color:#666;">16S · ITS · CO1 · 18S amplicon sequencing (Illumina, PacBio, IonTorrent)</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <span style="background:#e8f4f8;color:#1565C0;padding:2px 9px;border-radius:8px;font-size:0.78em;font-weight:600;">v2.14.0</span>
        <span style="background:#e8f4f8;color:#1565C0;padding:2px 9px;border-radius:8px;font-size:0.78em;font-weight:600;">v2.16.0</span>
      </div>
      <div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;">
        <span style="background:#2196F3;color:#fff;padding:3px 12px;border-radius:10px;font-size:0.8em;font-weight:600;">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:3px;"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>Reviewed
        </span>
        <span style="font-size:0.82em;color:#2196F3;font-weight:500;">View template →</span>
      </div>
    </div>
  </a>

  <a href="nf-core/viralrecon/" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;border:1px solid var(--md-default-fg-color--lightest, #ddd);border-radius:16px;width:300px;overflow:hidden;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 4px 16px rgba(0,0,0,0.12)'" onmouseout="this.style.boxShadow='none'">
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);display:flex;align-items:center;justify-content:center;padding:24px 16px;min-height:90px;">
      <img src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_light.png" alt="nf-core/viralrecon" style="height:52px;max-width:240px;object-fit:contain;">
    </div>
    <div style="padding:16px 20px;flex:1;display:flex;flex-direction:column;gap:10px;">
      <div style="font-size:0.82em;color:#666;">Viral assembly and variant calling — SARS-CoV-2 and other genomes via nf-core reference config</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <span style="background:#e8f4f8;color:#1565C0;padding:2px 9px;border-radius:8px;font-size:0.78em;font-weight:600;">v3.0.0</span>
      </div>
      <div style="margin-top:auto;display:flex;align-items:center;justify-content:space-between;">
        <span style="background:#2196F3;color:#fff;padding:3px 12px;border-radius:10px;font-size:0.8em;font-weight:600;">
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:3px;"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>Reviewed
        </span>
        <span style="font-size:0.82em;color:#2196F3;font-weight:500;">View template →</span>
      </div>
    </div>
  </a>

</div>

---

## Status levels

Each template carries a status reflecting its review level.

:material-shield-check:{ style="color:#4CAF50" } **Certified** — Validated by the **pipeline lead developer**. Highest trust.

:material-check-circle-outline:{ style="color:#2196F3" } **Reviewed** — Tested, CI passes, reviewed by Depictio team or community.

:material-flask-outline:{ style="color:#FF9800" } **Experimental** — Shared as-is. Feedback and PRs welcome.

---

## How templates work

A template bundles:

- :material-cog: **Project configuration** — workflows, data collections, and cross-DC links with `{VAR_NAME}` placeholders
- :material-chef-hat: **Recipes** — Python transforms that convert raw pipeline outputs into dashboard-ready tables
- :material-view-dashboard: **Dashboard YAML** — imported automatically on first run, with template variable substitution
- :material-link: **Cross-DC links** — enable interactive filtering across data collections

See [Template System Reference](../usage/projects/templates.md) for the YAML format and resolution mechanics, and [Recipes](../usage/projects/recipes.md) for how data transformations work.

---

## Contributing a template

Want to add a template for another pipeline? See the [Contributing Templates](../developer/contributing-templates.md) guide for the directory layout, recipe requirements, and review process.
