# nf-core/viralrecon

<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
  <img src="https://raw.githubusercontent.com/nf-core/viralrecon/master/docs/images/nf-core-viralrecon_logo_light.png" alt="nf-core/viralrecon" style="height:56px;" onerror="this.src='../../images/pipeline-templates/nf-core/viralrecon/nf-core-viralrecon_logo.png'">
  <div style="flex:1;">
    <strong style="font-size:1.1em;">SARS-CoV-2 / viral genome surveillance — variant calling, lineage assignment, and coverage analysis</strong><br>
    <span style="color:#666;font-size:0.9em;">nf-core pipeline · <a href="https://nf-co.re/viralrecon" target="_blank">nf-co.re/viralrecon</a></span>
  </div>
  <div style="background:#2196F3;color:#fff;padding:4px 12px;border-radius:12px;font-size:0.85em;font-weight:600;white-space:nowrap;"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:4px;"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>Reviewed</div>
</div>

The viralrecon template covers the main outputs of a standard
nf-core/viralrecon run for SARS-CoV-2 / viral genome surveillance:

- :material-chart-bar: **MultiQC quality control** — FastQC, Cutadapt, samtools/picard alignment metrics
- :material-dna: **Variant calling** — iVar variants with gene, effect, and allele-frequency annotations
- :material-virus: **Lineage assignment** — Pangolin lineages with conflict and QC scores
- :material-medical-bag: **Clade assignment** — Nextclade clades with substitution counts
- :material-chart-line: **Coverage analysis** — Mosdepth amplicon coverage, genome coverage, and amplicon heatmap
- :material-chart-scatter-plot: **Cross-sample landscape** — variant landscape and lineage analysis dashboards

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

| Data Collection | Type | Recipe | Key columns | Description |
|-----------------|------|--------|-------------|-------------|
| `multiqc_data` | MultiQC | — | (MultiQC native fields) | Native MultiQC parquet — FastQC, Cutadapt, alignment metrics |
| `summary_metrics` | Table | `summary_metrics.py` | `sample`, `num_reads_mapped`, `pct_genome_covered_10x`, `num_variants_total`, `lineage` | Per-sample alignment, coverage, and variant counts |
| `variants_long` | Table | `variants_long.py` | `sample`, `CHROM`, `POS`, `REF`, `ALT`, `FILTER`, `DP`, `AF` | Per-variant calls with gene, effect, allele frequency |
| `pangolin_lineages` | Table | `pangolin_lineages.py` | `sample`, `lineage`, `conflict`, `scorpio_call`, `qc_status` | Per-sample Pangolin lineage with conflict / QC scores |
| `nextclade_results` | Table | `nextclade_results.py` | `sample`, `clade`, `Nextclade_pango`, `totalSubstitutions`, `totalDeletions` | Per-sample Nextclade clade with substitution counts |
| `mosdepth_amplicon_coverage` | Table | — | `sample`, `amplicon`, `coverage` | Per-amplicon Mosdepth coverage |
| `mosdepth_genome_coverage` | Table | — | `sample`, `chrom`, `start`, `end`, `coverage` | Genome-window Mosdepth coverage |
| `mosdepth_amplicon_heatmap` | Table | — | `sample`, `amplicon`, `coverage` | Mosdepth amplicon coverage heatmap |

All DCs use `metatype: "Aggregated"`. The three Mosdepth DCs are native
table scans (no recipe); the others are Polars recipes that fan per-sample
files via `glob_pattern`.

Cross-DC links are wired so a `sample` selection in any tab filters every
linked DC across the dashboard. See [Cross-DC links](#cross-dc-links) below.

---

## Dashboard tabs

The viralrecon template ships a four-tab dashboard. Each tab targets a
different analytical question; filters propagate across tabs via cross-DC
links on the `summary_metrics.sample` column.

=== "Main — MultiQC overview"

    Pipeline-level quality control powered by MultiQC.

    ![MultiQC overview](../../images/pipeline-templates/nf-core/viralrecon/tab_1_light.png)

    **Filters:** Sample ID, Lineage.

    **Components:** 11 MultiQC plots covering raw read counts, trimming
    statistics, alignment rate, duplication rate, samtools/picard metrics,
    and variant counts.

=== "Coverage & Depth"

    Per-sample and per-amplicon coverage view.

    ![Coverage & Depth](../../images/pipeline-templates/nf-core/viralrecon/tab_2_light.png)

    **Filters:** Sample ID.

    **Components:**

    - 4 summary cards: *Total Samples*, *Amplicons Tracked*, *Amplicon Coverage*, *Genome Coverage*
    - *Genome Coverage per Sample* (line chart)
    - *Amplicon Coverage Heatmap*
    - *Amplicon Coverage Data* table
    - *Genome Coverage Data* table

=== "Lineage Analysis"

    Pangolin lineage and Nextclade clade assignment.

    ![Lineage Analysis](../../images/pipeline-templates/nf-core/viralrecon/tab_3_light.png)

    **Filters:** Sample ID, Lineage, Clade, QC Status.

    **Components:**

    - 4 summary cards: *Total Samples*, *Unique Lineages*, *Unique Clades*, *Avg Genome Coverage (10x)*
    - 6 figures: *Pangolin Lineage Distribution*, *Nextclade QC Status Overview*, *Nextclade Clade Distribution*, *Coverage vs Total Variants by Lineage*, *Genome Coverage per Sample (>= 10x Depth)*, *Nextclade - Substitutions vs Deletions by Clade*
    - 3 tables: *Pangolin Lineage Assignments*, *Nextclade Clade Assignments*, *Summary Metrics*

=== "Variant Landscape"

    Variant calls and functional effects.

    ![Variant Landscape](../../images/pipeline-templates/nf-core/viralrecon/tab_4_light.png)

    **Filters:** Sample ID, Gene, Variant Effect, Functional Class, Allele Frequency (range), Read Depth (range).

    **Components:**

    - 4 summary cards: *Total Variants*, *Unique Genes*, *Mean Allele Freq*, *Unique AA Changes*
    - 5 figures: *Variant Landscape - Allele Frequency vs Genome Position*, *Variant Count by Gene and Functional Class*, *Variant Effect Distribution*, *Variant Functional Class Distribution*, *Variant Count per Sample*
    - 1 table: *Variants Long Table*

!!! note "Screenshots will be added in a follow-up doc update"
    Image paths target `docs/images/pipeline-templates/nf-core/viralrecon/`.
    Captures need to be generated against a representative dataset.

---

## Recipes

The viralrecon template ships four Polars recipes under
`depictio/recipes/nf-core/viralrecon/`. Three use `glob_pattern` to fan
per-sample files into a single delta table; one reads a single MultiQC-
generated CSV.

=== "summary_metrics"

    `depictio/recipes/nf-core/viralrecon/summary_metrics.py`

    **Source:** `multiqc/summary_variants_metrics_mqc.csv` (single file
    produced by viralrecon's MultiQC step).

    **Output schema:**

    | Column | Type |
    |--------|------|
    | `sample` | `Utf8` |
    | `num_reads_mapped` | `Float64` |
    | `pct_reads_mapped` | `Float64` |
    | `coverage_median` | `Float64` |
    | `pct_genome_covered_1x`, `_10x` | `Float64` |
    | `num_variants_snp`, `_indel`, `_total` | `Float64` |
    | `lineage` | `Utf8` |

=== "variants_long"

    `depictio/recipes/nf-core/viralrecon/variants_long.py`

    **Source:** `variants/ivar/variants_long_table.csv` (single ivar
    long-format variant table covering all samples).

    **Output schema:**

    | Column | Type | Notes |
    |--------|------|-------|
    | `sample` | `Utf8` | Sample identifier |
    | `CHROM` | `Utf8` | Reference contig |
    | `POS` | `Int64` | 1-based position |
    | `REF`, `ALT` | `Utf8` | Alleles |
    | `FILTER` | `Utf8` | ivar filter status |
    | `DP` | `Int64` | Total depth |
    | `REF_DP`, `ALT_DP` | `Int64` | Per-allele depth |
    | `AF` | `Float64` | Allele frequency |
    | gene / effect / function annotations | | |

=== "pangolin_lineages"

    `depictio/recipes/nf-core/viralrecon/pangolin_lineages.py`

    **Source (glob):**
    `variants/ivar/consensus/bcftools/pangolin/*.pangolin.csv`
    — one file per sample.

    **Output schema:**

    | Column | Type |
    |--------|------|
    | `sample` | `Utf8` |
    | `lineage` | `Utf8` |
    | `conflict`, `ambiguity_score` | `Float64` |
    | `scorpio_call` | `Utf8` |
    | `scorpio_support` | `Float64` |
    | `pangolin_version` | `Utf8` |
    | `qc_status` | `Utf8` |

=== "nextclade_results"

    `depictio/recipes/nf-core/viralrecon/nextclade_results.py`

    **Source (glob):**
    `variants/ivar/consensus/bcftools/nextclade/*.csv`
    — one file per sample, **semicolon-separated** (recipe sets
    `read_kwargs={"separator": ";"}`).

    **Output schema:**

    | Column | Type |
    |--------|------|
    | `sample` | `Utf8` |
    | `clade` | `Utf8` |
    | `Nextclade_pango` | `Utf8` |
    | `totalSubstitutions`, `totalDeletions`, `totalInsertions` | `Int64` |
    | `totalFrameShifts`, `totalMissing`, `totalNonACGTNs` | `Int64` |
    | QC fields (`qc.overallStatus`, etc.) | `Utf8` |

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
