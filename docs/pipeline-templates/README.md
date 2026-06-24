---
title: Templates
icon: material/layers-outline
---

# Depictio Templates

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio-cli run \
  --template nf-core/ampliseq/2.16.0 \
  --data-root /data/my_ampliseq_run
```

---

## Available templates

<div class="template-cards">

  <a class="template-card" href="nf-core/ampliseq/">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_dark.png" alt="nf-core/ampliseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">16S · ITS · CO1 · 18S amplicon sequencing across Illumina, PacBio, and IonTorrent.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.16.0</span>
        <span class="template-status-reviewed"><i class="mdi mdi-check-circle-outline" style="vertical-align:-1px;"></i> Reviewed</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/viralrecon/">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_dark.png" alt="nf-core/viralrecon">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_light.png" alt="nf-core/viralrecon">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Viral assembly and variant calling — SARS-CoV-2 and other genomes via the nf-core reference config.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.0.0</span>
        <span class="template-status-reviewed"><i class="mdi mdi-check-circle-outline" style="vertical-align:-1px;"></i> Reviewed</span>
      </div>
    </div>
  </a>

</div>

---

## Status levels

<div class="status-cards">

  <div class="status-card status-certified">
    <div class="status-card-header">
      <i class="mdi mdi-shield-check status-icon"></i>
      <span class="status-title">Certified</span>
    </div>
    <p class="status-desc">Validated by the <strong>pipeline lead developer</strong>. Highest trust level.</p>
  </div>

  <div class="status-card status-reviewed">
    <div class="status-card-header">
      <i class="mdi mdi-check-circle-outline status-icon"></i>
      <span class="status-title">Reviewed</span>
    </div>
    <p class="status-desc">Tested, CI passes, reviewed by the Depictio team or community.</p>
  </div>

  <div class="status-card status-experimental">
    <div class="status-card-header">
      <i class="mdi mdi-flask-outline status-icon"></i>
      <span class="status-title">Experimental</span>
    </div>
    <p class="status-desc">Shared as-is. Feedback and PRs welcome.</p>
  </div>

</div>

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
