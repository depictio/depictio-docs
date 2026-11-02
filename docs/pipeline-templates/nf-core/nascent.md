---
title: Nascent transcription
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/nascent" target="_blank" title="nf-core/nascent on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/nascent/master/docs/images/nf-core-nascent_logo_dark.png" alt="nf-core/nascent">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/nascent/master/docs/images/nf-core-nascent_logo_light.png" alt="nf-core/nascent">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Nascent transcription</h1>
    <p class="template-subtitle">Nascent RNA over a time course, from run-on reads to responding genes: library quality, the response class of each gene, how each time point moves from the baseline, and the strand-specific signal along the genome.</p>
    <p class="template-links">
      <a href="https://nf-co.re/nascent" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/nascent" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="2.3.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="2.3.0" selected>2.3.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The nascent template follows an nf-core/nascent run from run-on libraries
(GRO-seq, PRO-seq) to the genes and genomic windows that respond over a time course:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-shield-check-outline: **Library QC**: reads in genes, genes detected and strand balance of each library, in time order
- :material-chart-timeline-variant: **Gene dynamics**: induced and repressed genes, by the phase of their peak, with the genes that move most
- :material-chart-scatter-plot-hexbin: **Sample similarity**: how far each time point has moved from the baseline
- :material-dna: **Genome signal**: the strand-specific signal along the genome, linked to a genome browser
- :material-chart-bell-curve: **Signal dynamics**: the 250 kb windows that gain or lose signal over time


<div class="tpl-showcase">
  <div class="tpl-showcase-bar">
    <span class="tpl-showcase-live"></span>
    <span class="tpl-showcase-label">Live showcase</span>
    <span class="tpl-showcase-meta">nf-core/nascent, nf-core test data</span>

    <a class="tpl-showcase-open" href="https://showcases.depictio.embl.org/dashboard/6ae7935f9e97ca1af10fb77e" target="_blank" rel="noopener"><i class="mdi mdi-open-in-new"></i> Open</a>
  </div>
  <iframe class="tpl-showcase-frame" src="https://showcases.depictio.embl.org/dashboard/6ae7935f9e97ca1af10fb77e" loading="lazy" title="nf-core/nascent showcase dashboard" allowfullscreen></iframe>
</div>

The persistent sample filters (group, library, time point) sit in the left panel
and narrow every tab; a pick reaches the per-library collections by `sample` and
the per-gene and per-window calls by the time point of their peak.

!!! info "Without replicates, a call is a rule"
    A gene or window is called induced or repressed when its peak change against
    the baseline is at least twofold and at least two time points move that way.
    Time courses are rarely replicated, so this is a fold-change rule on
    consecutive time points, not a statistical test: read a gene's trajectory
    before trusting its class.


---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/nascent_results \
      --template nf-core/nascent/latest \
      --var METADATA_FILE=/path/to/design.tsv
    ```

    The results directory is the only required value. nascent publishes neither a
    sample sheet nor a design table; the optional design gives each library its
    hours. Without it, a library id ending in a duration (`<name>_30min`,
    `<name>_2h`) still gets its time point, and a library with neither drops out of
    the time-course panels while its QC stays on Library QC.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | unset (reference: `{DATA_ROOT}/input/design.tsv`) | design table: the library id in `sample`, the hours in `TIME_COL`, a `time_point` label and any factor |
    | `TIME_COL` | `time_h` | design column holding each library's hours |
    | `GROUP_COL` | first factor column of the design | column the dashboard groups and filters libraries by |
    | `TRACKS_URI` | unset | `s3://` or `https://` folder holding the run's results: the browser reads the bigWigs in place instead of uploading them from `DATA_ROOT` |
    | `GENOME` | `hg38` | UCSC assembly of the genome tracks' axis and gene lane |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/nascent -r 2.3.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so put a design table at `results/input/design.tsv`
    before the run if the library ids do not carry their duration.


---

## :material-book-open-variant: Reference

The template reads the featureCounts gene matrix, the strand coverage written
as bedGraph and bigWig, and the run parameters. The strand bedGraphs (4 to 10
million intervals each on a human genome) are never ingested whole: two recipes
stream them into 250 kb windows and per-library totals. The bigWigs are range-read
by the browser for the region in view. The BAMs, the `dreg.bedGraph`, the QC
reports and the transcript identification outputs are not read, and the template
has no MultiQC tab.

On the time axis, `log2(1 + hours)` keeps the first hour from taking a few pixels.
The baseline is the earliest time point, and the later ones are split into
`Early`, `Mid` and `Late` by rank. An expressed gene has at least 10 reads in at
least half of the libraries. A library keeps one colour on every tab, a ramp along
the time course (the later, the darker).

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows. A run without the strand coverage drops
    Genome signal and Signal dynamics.

<div class="tpl-version-block" data-version="2.3.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/nascent-latest.md"

</div>


---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then five child tabs in two groups, read from the
quality of each library to where along the genome transcription changes. Each tab
below carries the **same icon and colour the dashboard gives it**, so the page and
the app read alike.

| Group | Tabs |
|---|---|
| Data & QC | Library QC |
| Time course | Gene dynamics, Sample similarity, Genome signal, Signal dynamics |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* is pinned,
collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Nascent transcription over a time course, from run-on reads to responding genes.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/nascent/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/nascent/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Hero, *About* and run cards and a five-step pipeline flow. Four key figures: the
    libraries, the reads in genes, the responsive genes and the strand skew (pass, warn
    and fail against 10 and 15 points). Four findings, each with a highlight, the third
    naming the chromosome whose share of the signal moves most against its baseline.

=== ":material-shield-check-outline:{ .mc-blue } Library QC"

    **Data & QC** · *Does each library have the depth and balance to be read?*

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/nascent/library_qc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/library_qc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Library QC dashboard](../../images/pipeline-templates/nf-core/nascent/library_qc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/library_qc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    Reads in genes and genes detected per library in time order, against their median
    (a bar under half the typical depth is shallow; a click narrows the other tiles).
    The plus-strand share per library against the even split, with the balanced band
    (40 to 60%) shaded, and the hotspot, off-chromosome and mitochondrial shares. The
    gene-count and strand tables are collapsed.

=== ":material-chart-timeline-variant:{ .mc-grape } Gene dynamics"

    **Time course** · *Which genes change transcription over the time course, and when?*

    [![Gene dynamics dashboard](../../images/pipeline-templates/nf-core/nascent/gene_dynamics_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/gene_dynamics_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Gene dynamics dashboard](../../images/pipeline-templates/nf-core/nascent/gene_dynamics_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/gene_dynamics_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The median trajectory of each response class with its quartile band, the ten genes
    that move most, and the forty most dynamic genes as a heatmap in time order. A
    response class is a direction with the phase of the peak (`Induced early` to
    `Repressed late`). The call per gene and the value per time point are collapsed.

=== ":material-chart-scatter-plot-hexbin:{ .mc-pink } Sample similarity"

    **Time course** · *How far has each time point moved from the baseline?*

    [![Sample similarity dashboard](../../images/pipeline-templates/nf-core/nascent/sample_similarity_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/sample_similarity_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Sample similarity dashboard](../../images/pipeline-templates/nf-core/nascent/sample_similarity_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/sample_similarity_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The library correlation matrix, a PCA of the libraries coloured by phase, and the
    correlation of each time point with the baseline and with the previous one. A course
    moves along the first components in time order: a library off that line is a
    candidate outlier rather than biology.

=== ":material-dna:{ .mc-teal } Genome signal"

    **Time course** · *Where along the genome is nascent transcription read?*

    [![Genome signal dashboard](../../images/pipeline-templates/nf-core/nascent/genome_signal_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/genome_signal_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Genome signal dashboard](../../images/pipeline-templates/nf-core/nascent/genome_signal_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/genome_signal_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The binned signal, one thin lane per library, linked to a genome browser with the
    plus and minus bigWigs: brush a region or type one and the browser zooms to it. The
    cards follow the region in view, and the lanes and tracks are coloured along the time
    course. Below, each chromosome's share of the signal against its baseline share, per
    time point. The lanes are on log2 of the signal, so the ribosomal DNA hotspot does
    not tower over everything.

=== ":material-chart-bell-curve:{ .mc-orange } Signal dynamics"

    **Time course** · *Which genomic windows gain or lose nascent signal over time?*

    [![Signal dynamics dashboard](../../images/pipeline-templates/nf-core/nascent/signal_dynamics_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/signal_dynamics_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Signal dynamics dashboard](../../images/pipeline-templates/nf-core/nascent/signal_dynamics_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/nascent/signal_dynamics_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The gene rule applied to the comparable 250 kb windows, so a change outside
    annotated genes shows too: the windows that change (rising or falling), by phase of the peak, the forty
    windows that change most as a heatmap, and the median course of each trend. The
    window table is collapsed.

The gene and window trajectories (and so the median curves and the heatmaps) follow
the calls in scope, not the picked time points, so each keeps its whole course. The
baseline never peaks: picking only the baseline library leaves no gene or window in
scope.


---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/nascent, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/nascent -r 2.3.0 \
  --input samplesheet.csv \
  --outdir results \
  -profile docker
```

Then point Depictio at the results, with the design table that gives the hours:

```bash
depictio ingest results/ \
  --template nf-core/nascent/latest \
  --var METADATA_FILE=design.tsv
```

See [nf-co.re/nascent/usage](https://nf-co.re/nascent/2.3.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/
│   └── design.tsv                              # --var METADATA_FILE (optional, not published)
├── pipeline_info/
│   ├── params_*.json
│   └── *software*versions*.yml
├── quantification/gene/<group>.featureCounts.txt
└── coverage_graphs/
    ├── <sample>.{plus,minus}.bedGraph          # streamed into 250 kb windows
    └── <sample>.{plus,minus}.bigWig            # range-read by the genome browser
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/nascent/2.3.0/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs and
copies the vendored sample sheet and design table into `input/`:

```bash
bash depictio/projects/nf-core/nascent/2.3.0/download_test_data.sh \
  /tmp/nascent_test
depictio ingest /tmp/nascent_test \
  --template nf-core/nascent/latest \
  --var METADATA_FILE=/tmp/nascent_test/input/design.tsv
```

The run is
`s3://nf-core-awsmegatests/nascent/results-7d4fe61975015f652c271886e661764b05cfd3bf/`,
the 2.3.0 `test_full` profile: one GRO-seq time course of 11 single-end libraries,
0 h to 72 h. The download is about 5.2 GB, 4.8 GB of it the strand bedGraphs. That
run did not finish its transcript identification and wrote no MultiQC report, which
is why the template has no Transcripts or MultiQC tab.

---

## :material-link-variant: Additional resources

- [nf-co.re/nascent](https://nf-co.re/nascent): official pipeline documentation
- [nf-co.re/nascent/results](https://nf-co.re/nascent/results): AWS test results
- [Template System Reference](../../usage/projects/templates.md): YAML format, variables, conditionals
- [Recipes](../../usage/projects/recipes.md): how to read, test, and write recipes

---

## :material-account-group-outline: Authorship

<div class="tpl-credits">
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-code-braces"></i> Developers</span>
    <span class="tpl-credit-note">Wrote the template, its recipes and its dashboards.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-eye-check-outline"></i> Reviewers</span>
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it from Reviewed.</span>
    <span class="tpl-person"><i class="mdi mdi-account-plus-outline"></i> Open</span>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/nascent releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
