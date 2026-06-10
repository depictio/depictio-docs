# nf-core/viralrecon

<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
  <div style="flex-shrink:0;">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_dark.png" alt="nf-core/viralrecon" style="height:56px;">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_light.png" alt="nf-core/viralrecon" style="height:56px;">
  </div>
  <div style="flex:1;">
    <strong style="font-size:1.1em;">Assembly and intrahost/low-frequency variant calling for viral samples — SARS-CoV-2 + other viral genomes via the nf-core reference-genomes config.</strong><br>
    <span style="font-size:0.9em;">nf-core pipeline · <a href="https://nf-co.re/viralrecon" target="_blank">nf-co.re/viralrecon</a></span>
  </div>
  <span class="template-status-reviewed" style="white-space:nowrap;flex-shrink:0;"><i class="mdi mdi-check-circle-outline" style="vertical-align:-1px;"></i> Reviewed</span>
</div>

The viralrecon template covers the main outputs of a standard
nf-core/viralrecon run. The pipeline itself supports any viral genome
configured in nf-core's reference-genomes config; the bundled depictio
template was validated against SARS-CoV-2 / ARTIC amplicon data but the
recipe / dashboard structure carries over to other viruses with the
same iVar variant-calling + Pangolin / Nextclade lineage layout.

- :material-chart-bar: **MultiQC quality control** — fastp, FastQC, samtools, picard, mosdepth, iVar, bcftools, Pangolin, Nextclade, QUAST alignment metrics
- :material-dna: **Variant calling** — iVar variants with gene, effect, and allele-frequency annotations; Oncoplot and UpSet views
- :material-virus: **Lineage assignment** — Pangolin lineages with conflict and QC scores; Sankey funnel (QC status → lineage → clade)
- :material-medical-bag: **Clade assignment** — Nextclade clades with substitution counts
- :material-chart-line: **Coverage analysis** — Mosdepth amplicon coverage, genome coverage track, and amplicon heatmap
- :material-chart-scatter-plot: **Cross-sample landscape** — variant feature matrix for PCA / UMAP embedding; sample × gene oncoplot

---

## Quick start

```bash
depictio run \
  --template nf-core/viralrecon/3.0.0 \
  --data-root /path/to/viralrecon_results
```

Unlike the ampliseq template, viralrecon needs no extra template variables —
just point `--data-root` at the pipeline's output directory. The template
expects nf-core/viralrecon's standard layout:

```
viralrecon_results/
├── multiqc/
│   ├── multiqc_data/
│   │   └── multiqc.parquet
│   └── summary_variants_metrics_mqc.csv
└── variants/
    └── ivar/
        ├── consensus/
        │   └── bcftools/
        │       ├── pangolin/*.pangolin.csv
        │       └── nextclade/*.csv
        ├── variants_long_table.csv
        └── *.mosdepth.{coverage,heatmap}.tsv
```

!!! warning "`--variant_caller ivar` is required"
    The viralrecon template's recipes hardcode paths under `variants/ivar/`
    (see `variants_long.py`, `pangolin_lineages.py`, `nextclade_results.py`).
    Running nf-core/viralrecon with the alternative `--variant_caller bcftools`
    produces a different output layout that the template won't match.

!!! tip "Aggregated data collections"
    All eight viralrecon DCs use `metatype: "Aggregated"`. They are built
    by recipes that fan multiple per-sample files into a single delta
    table via `glob_pattern`. See [Recipes](../../usage/projects/recipes.md#glob_pattern-per-sample-inputs)
    for the underlying mechanism.

---

## Template variables

| Variable | Required | Auto | Description |
|----------|:--------:|:----:|-------------|
| `DATA_ROOT` | :material-check: | — | Pipeline output root (set via `--data-root`) |

The viralrecon template's recipes use `glob_pattern` to discover
per-sample files relative to `DATA_ROOT`, so no samplesheet path needs to
be passed.

---

## Test data

A small test fixture is available for local development without re-running
the full pipeline. The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh)
which fetches a real viralrecon run from nf-core's AWS megatest bucket:

```bash
bash depictio/projects/nf-core/viralrecon/3.0.0/download_test_data.sh \
  --target /tmp/viralrecon_test
```

This pulls a published run from
`s3://nf-core-awsmegatests/viralrecon/results-395079f1d24dce731ac22e03d7a5e71f110103fc/`
and validates that all expected file patterns are present.

Once the download finishes, run depictio against it:

```bash
depictio run \
  --template nf-core/viralrecon/3.0.0 \
  --data-root /tmp/viralrecon_test/run_1
```

!!! warning "`--variant_caller ivar` is required"
    The viralrecon template's recipes hardcode paths under `variants/ivar/`.
    Running nf-core/viralrecon with `--variant_caller bcftools` produces a
    different output layout that the template won't match.

!!! note "Alternative: run nf-core/viralrecon locally"
    The script can also re-run nf-core/viralrecon end-to-end if you'd
    rather regenerate the fixture from scratch:

    ```bash
    nextflow run nf-core/viralrecon -r 3.0.0 \
      -profile test_illumina,docker \
      --variant_caller ivar \
      --outdir /tmp/viralrecon_test/run_1
    ```

---

## Data collections

**Core data collections** (14 DCs total):

| Data Collection | Recipe | Key columns | Description |
|-----------------|--------|-------------|-------------|
| `multiqc_data` | — | (MultiQC native fields) | Native MultiQC parquet — fastp, FastQC, samtools/picard metrics |
| `summary_metrics` | `summary_metrics.py` | `sample`, `num_reads_mapped`, `pct_genome_covered_10x`, `num_variants_total`, `lineage` | Per-sample alignment, coverage, and variant counts |
| `variants_long` | `variants_long.py` | `sample`, `CHROM`, `POS`, `REF`, `ALT`, `FILTER`, `DP`, `AF` | Per-variant calls with gene, effect, allele frequency |
| `pangolin_lineages` | `pangolin_lineages.py` | `sample`, `lineage`, `conflict`, `scorpio_call`, `qc_status` | Per-sample Pangolin lineage with conflict / QC scores |
| `nextclade_results` | `nextclade_results.py` | `sample`, `clade`, `Nextclade_pango`, `totalSubstitutions`, `totalDeletions` | Per-sample Nextclade clade with substitution counts |
| `mosdepth_amplicon_coverage` | — | `sample`, `amplicon`, `coverage` | Per-amplicon Mosdepth coverage |
| `mosdepth_genome_coverage` | — | `sample`, `chrom`, `start`, `end`, `coverage` | Genome-window Mosdepth coverage |
| `mosdepth_amplicon_heatmap` | — | `sample`, `amplicon`, `coverage` | Mosdepth amplicon coverage heatmap |

All DCs use `metatype: "Aggregated"`. The three Mosdepth DCs are native
table scans (no recipe); the others are Polars recipes that fan per-sample
files via `glob_pattern`.

**Advanced-viz canonical DCs** — reformatted to the role-based schema consumed by advanced viz renderers:

| Data Collection | Drives | Recipe |
|-----------------|--------|--------|
| `oncoplot_canonical` | Oncoplot (sample × gene × mutation type) | `nf-core/viralrecon/oncoplot_canonical.py` |
| `complex_heatmap_canonical` | Hierarchical heatmap (samples × amplicons) | `mosdepth/complex_heatmap_canonical.py` |
| `coverage_track_canonical` | Genome coverage track (chromosome / position / value) | `mosdepth/coverage_track_canonical.py` |
| `sankey_canonical` | Sankey funnel (qc_status → lineage → clade) | `nf-core/viralrecon/sankey_canonical.py` |
| `upset_canonical` | UpSet (mutation × lineage binary membership) | `nf-core/viralrecon/upset_canonical.py` |
| `variant_feature_matrix_canonical` | Sample × mutation binary matrix (PCA / UMAP embedding) | `nf-core/viralrecon/variant_feature_matrix_canonical.py` |

Cross-DC links are wired so a `sample` selection in any tab filters every
linked DC across the dashboard. See [Cross-DC links](#cross-dc-links) below.

---

## Dashboard tabs

The viralrecon template ships a five-tab dashboard (MultiQC parent +
four child tabs). Each tab targets a different analytical question;
filters propagate across tabs via cross-DC links on the
`summary_metrics.sample` column.

=== "Main — MultiQC overview"

    Pipeline-level quality control powered by MultiQC.

    [![MultiQC overview](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png)](../../images/pipeline-templates/nf-core/viralrecon/multiqc_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Lineage.

    **Components:** 11 MultiQC plots covering raw read counts, trimming
    statistics, alignment rate, duplication rate, samtools/picard metrics,
    and variant counts.

=== "Coverage & Depth"

    Per-sample and per-amplicon coverage view.

    [![Coverage & Depth](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png)](../../images/pipeline-templates/nf-core/viralrecon/coverage_depth_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID.

    **Components:**

    - 4 summary cards: *Total Samples*, *Amplicons Tracked*, *Amplicon Coverage*, *Genome Coverage*
    - *Genome Coverage per Sample* (line chart)
    - *Amplicon Coverage Heatmap*
    - *Amplicon Coverage Data* table
    - *Genome Coverage Data* table

=== "Lineage & Clustering"

    Pangolin lineage and Nextclade clade assignment, plus a Sankey
    funnel from QC status → lineage → clade.

    [![Lineage & Clustering](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png)](../../images/pipeline-templates/nf-core/viralrecon/lineage_clustering_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Lineage, Clade, QC Status.

    **Components:**

    - 4 summary cards: *Total Samples*, *Unique Lineages*, *Unique Clades*, *Avg Genome Coverage (10x)*
    - 6 figures: *Pangolin Lineage Distribution*, *Nextclade QC Status Overview*, *Nextclade Clade Distribution*, *Coverage vs Total Variants by Lineage*, *Genome Coverage per Sample (>= 10x Depth)*, *Nextclade — Substitutions vs Deletions by Clade*
    - Sankey funnel: qc_status → lineage → clade (canonical sankey)
    - 3 tables: *Pangolin Lineage Assignments*, *Nextclade Clade Assignments*, *Summary Metrics*

=== "Variants"

    Variant calls and functional effects, with manhattan-style genome
    landscape and oncoplot of high-impact mutations.

    [![Variants](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png)](../../images/pipeline-templates/nf-core/viralrecon/variants_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Gene, Variant Effect, Functional Class, Allele Frequency (range), Read Depth (range).

    **Components:**

    - 4 summary cards: *Total Variants*, *Unique Genes*, *Mean Allele Freq*, *Unique AA Changes*
    - Manhattan plot: chr × pos × score (canonical manhattan)
    - Lollipop: per-gene variants (canonical lollipop)
    - Oncoplot: sample × gene × mutation_type (canonical oncoplot)
    - 5 figures: *Allele Frequency vs Genome Position*, *Variant Count by Gene and Functional Class*, *Variant Effect Distribution*, *Variant Functional Class Distribution*, *Variant Count per Sample*
    - 1 table: *Variants Long Table*

=== "Sample QC"

    Per-sample QC scorecard combining alignment, coverage, variant counts
    and lineage / clade assignment in one place.

    [![Sample QC](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png)](../../images/pipeline-templates/nf-core/viralrecon/sample_qc_light.png){target="_blank" rel="noopener"}

    **Filters:** Sample ID, Lineage, QC Status.

    **Components:**

    - Summary cards: total samples, samples passing QC, mean coverage,
      mean variants per sample
    - Sample × metric heatmap (canonical complex heatmap)
    - Summary metrics table

---

## Recipes

The viralrecon template ships ten Polars recipes. Four produce the core
typed data collections; six produce canonical schemas for the advanced-viz
renderers.

**nf-core/viralrecon recipes** (under `nf-core/viralrecon/`):

| Recipe | Input | Key transformation |
|--------|-------|--------------------|
| `summary_metrics.py` | `multiqc/summary_variants_metrics_mqc.csv` | Single file; passes through alignment, coverage, and variant count columns |
| `variants_long.py` | `variants/ivar/variants_long_table.csv` | Single iVar long-format table; renames/coerces types |
| `pangolin_lineages.py` | `variants/ivar/consensus/bcftools/pangolin/*.pangolin.csv` (glob) | Fan per-sample → unified table |
| `nextclade_results.py` | `variants/ivar/consensus/bcftools/nextclade/*.csv` (glob, semicolon-sep) | Fan per-sample → unified table |
| `oncoplot_canonical.py` | variants_long DC | Pivot to `(sample_id, gene, mutation_type, mutation_label)` |
| `sankey_canonical.py` | summary_metrics + pangolin_lineages + nextclade_results DCs | Join, produce `(sample, qc_status, lineage, clade, value)` |
| `upset_canonical.py` | variants_long DC | Binary mutation × lineage presence matrix |
| `variant_feature_matrix_canonical.py` | variants_long DC | Binary sample × mutation matrix for PCA/UMAP |

**mosdepth recipes** (under `mosdepth/`, shared across pipelines):

| Recipe | Input | Key transformation |
|--------|-------|--------------------|
| `complex_heatmap_canonical.py` | mosdepth_amplicon_heatmap DC | Amplicon × sample coverage matrix |
| `coverage_track_canonical.py` | mosdepth_genome_coverage DC | Rename `chrom` → `chromosome`, `start` → `position` |


---

## Cross-DC links

The viralrecon template wires seven cross-DC links from
`summary_metrics.sample` to every other data collection — selecting a
sample propagates the filter across:

- `multiqc_data` (resolver: `sample_mapping`)
- `variants_long`
- `pangolin_lineages`
- `nextclade_results`
- `mosdepth_amplicon_coverage`
- `mosdepth_genome_coverage`
- `mosdepth_amplicon_heatmap`

This star-topology means `summary_metrics` is the canonical "sample
roster" for the dashboard — adding a new DC just requires another link
from `summary_metrics.sample` to wire it into the existing filter graph.
