---
title: "Depictio Templates"
icon: material/layers-outline
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../images/logo/templates_catalog_logo.png" alt="Depictio Templates">
  <h1 class="catalog-hero__title" id="depictio-templates">Depictio <span class="accent-t" role="img" aria-label="T"><svg class="accent-t-svg" viewBox="145 40.05 330.65 407.46" aria-hidden="true"><g transform="rotate(180, 310.325, 243.78)"> <g transform="translate(0.000000,569.000000) scale(0.100000,-0.100000)" fill="#9870FF" stroke="none"> <path d="M2925 5268 c-14 -13 -71 -113 -127 -223 -56 -110 -135 -265 -176 -345 -41 -80 -88 -172 -104 -205 -15 -33 -33 -68 -38 -78 -6 -9 -42 -79 -82 -155 -39 -75 -92 -177 -118 -227 -75 -143 -152 -290 -222 -425 -36 -69 -94 -179 -130 -245 -36 -66 -98 -183 -138 -260 -40 -77 -83 -158 -95 -180 -151 -268 -245 -446 -245 -461 0 -39 37 -83 77 -90 234 -43 308 -61 311 -76 2 -8 -11 -40 -29 -69 -18 -30 -57 -97 -87 -149 -86 -146 -76 -197 41 -219 34 -7 105 -21 157 -32 53 -10 105 -19 116 -19 11 0 28 -6 38 -13 17 -12 17 -15 0 -50 -10 -20 -21 -37 -26 -37 -4 0 -8 -5 -8 -11 0 -6 -31 -65 -70 -130 -95 -160 -94 -199 5 -226 148 -41 402 -79 680 -103 72 -6 166 -15 210 -19 121 -13 647 -4 835 14 224 21 246 24 315 36 33 6 94 17 135 24 97 16 215 41 315 67 44 12 109 27 145 35 93 20 133 42 143 78 9 32 64 -94 -934 2139 -143 319 -269 590 -280 602 -11 12 -75 140 -140 285 -79 173 -132 275 -154 301 -19 21 -35 43 -35 48 0 22 -182 416 -198 428 -24 18 -58 15 -87 -10z m85 -170 c15 -35 55 -125 89 -201 38 -85 60 -146 56 -157 -3 -10 -29 -58 -57 -107 -28 -48 -65 -117 -83 -153 -17 -36 -58 -114 -89 -175 -32 -60 -90 -171 -128 -245 -80 -154 -122 -233 -235 -445 -44 -82 -113 -213 -153 -290 -40 -77 -89 -169 -108 -205 -119 -222 -165 -307 -197 -365 -12 -22 -62 -111 -110 -198 l-88 -158 -61 6 c-33 4 -113 17 -176 29 -88 16 -116 25 -118 38 -2 9 26 67 61 130 35 62 88 158 117 213 68 129 204 385 241 453 73 132 90 165 154 287 38 72 111 213 163 315 124 244 247 480 287 555 55 101 187 360 290 564 68 137 100 190 107 183 6 -6 23 -39 38 -74z m259 -515 c24 -54 73 -162 108 -241 45 -97 63 -149 59 -165 -5 -19 -141 -272 -195 -361 -22 -36 -58 -102 -111 -201 -42 -79 -60 -111 -170 -310 -43 -77 -149 -268 -236 -425 -189 -343 -186 -337 -199 -358 -6 -9 -30 -53 -55 -97 -25 -44 -54 -96 -65 -116 -194 -347 -251 -439 -272 -439 -22 0 -151 25 -301 57 -40 9 -75 20 -78 25 -6 9 -5 11 137 258 53 91 113 197 134 235 21 39 57 104 80 145 79 140 98 175 182 334 47 88 99 184 115 215 17 31 64 121 106 201 41 80 96 183 122 230 26 47 103 191 170 320 67 129 144 276 170 325 26 50 91 174 145 278 53 103 100 187 104 187 4 0 27 -44 50 -97z m262 -511 c9 -20 207 -462 439 -982 232 -520 476 -1066 541 -1214 66 -147 131 -291 145 -319 25 -48 25 -51 8 -64 -10 -7 -24 -13 -31 -13 -7 0 -41 -9 -75 -19 -55 -17 -188 -49 -338 -81 -25 -5 -94 -17 -155 -25 -60 -8 -130 -18 -155 -21 -25 -4 -61 -8 -80 -9 -19 -2 -88 -8 -152 -14 -209 -20 -615 -23 -863 -7 -343 22 -787 87 -822 120 -9 8 -5 22 17 61 16 28 43 77 61 110 17 33 43 78 58 100 42 65 51 78 69 109 49 81 92 155 167 286 45 80 117 206 160 280 43 74 88 153 100 175 81 144 125 226 125 229 0 4 37 70 138 246 59 103 73 128 103 185 17 33 91 168 164 300 73 132 147 267 165 300 18 33 47 85 66 116 19 31 34 59 34 62 0 16 73 127 83 127 7 0 19 -17 28 -38z"/> </g> </g></svg></span>emplates</h1>
</div>

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

Want to add a template for another pipeline? The contributing guide covers the directory layout, recipe requirements, and review process.

<div class="catalog-cta-wrap" markdown>
[Read the contributing guide :material-arrow-right:](../developer/contributing-templates.md){ .catalog-cta }
</div>
