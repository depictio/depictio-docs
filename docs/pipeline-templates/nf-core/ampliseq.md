# <span style="color: #45B8AC;">:material-dna:</span> nf-core/ampliseq

<div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;">
  <img src="../../images/pipeline-templates/nf-core/ampliseq/ampliseq_icon.png" alt="ampliseq" style="height:48px;">
  <div>
    <strong>16S/ITS amplicon sequencing — microbial community analysis</strong><br>
    <span style="color:#666;font-size:0.9em;">nf-core pipeline · <a href="https://nf-co.re/ampliseq" target="_blank">nf-co.re/ampliseq</a></span>
  </div>
  <span style="margin-left:auto;background:#45B8AC;color:#fff;padding:3px 10px;border-radius:12px;font-size:0.8em;font-weight:600;">:material-check-decagram: Official</span>
</div>

nf-core/ampliseq analyses amplicon sequencing data (16S rRNA by default) via [QIIME2](https://qiime2.org/). The template covers MultiQC quality control, taxonomy composition, diversity metrics, and differential abundance.

---

## Quick start

=== "Base (no metadata)"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.16.0 \
      --data-root /path/to/ampliseq_results \
      --var SAMPLESHEET_FILE=samplesheet.csv
    ```

    Produces: MultiQC + taxonomy composition dashboards (no diversity/ANCOM-BC).

=== "Extended (with metadata)"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.16.0 \
      --data-root /path/to/ampliseq_results \
      --var SAMPLESHEET_FILE=samplesheet.csv \
      --var METADATA_FILE=Metadata.tsv \
      --var GROUP_COL=habitat
    ```

    Produces: Full dashboard with diversity, facetted charts, sampling map, heatmap annotations, ANCOM-BC differential abundance.

---

## Template variables

| Variable | Required | Auto-detected | Description |
|----------|----------|---------------|-------------|
| `DATA_ROOT` | :material-check: | — | Pipeline output root directory (set via `--data-root`) |
| `SAMPLESHEET_FILE` | :material-check: | — | Path to ampliseq samplesheet CSV |
| `METADATA_FILE` | — | — | Path to sample metadata TSV. Enables extended dashboard. |
| `GROUP_COL` | — | :material-check: | Metadata column for grouping/facetting. Auto-detected as first annotation column. |
| `GROUP_COL_DISPLAY` | — | :material-check: | Title-cased version of GROUP_COL (e.g., "Habitat") |
| `ANNOTATION_COLS` | — | :material-check: | Comma-separated list of all annotation columns from metadata |

---

## Data collections

| Data Collection | Type | Source | Recipe | Base | Extended |
|-----------------|------|--------|--------|:----:|:--------:|
| `multiqc_data` | MultiQC | `multiqc/multiqc_data/multiqc.parquet` | — | :material-check: | :material-check: |
| `samplesheet` | Table | `{SAMPLESHEET_FILE}` | — | :material-check: | :material-check: |
| `metadata` | Table | `{METADATA_FILE}` | — | :material-close: | :material-check: |
| `alpha_diversity` | Table | `qiime2/diversity/.../metadata.tsv` | `alpha_diversity.py` | :material-close: | :material-check: |
| `alpha_rarefaction` | Table | `qiime2/alpha-rarefaction/faith_pd.csv` | `alpha_rarefaction.py` | :material-close: | :material-check: |
| `taxonomy_composition` | Table | `qiime2/barplot/level-2.csv` | `taxonomy_composition.py` | :material-check: | :material-check: |
| `taxonomy_rel_abundance` | Table | `qiime2/rel_abundance_tables/rel-table-2.tsv` + metadata DC | `taxonomy_rel_abundance.py` | :material-check: | :material-check: |
| `taxonomy_heatmap` | Table | rel_abundance DC + metadata DC | `taxonomy_heatmap.py` | :material-check: | :material-check: |
| `ancombc_results` | Table | 5 ANCOM-BC CSV slices | `ancombc.py` | :material-close: | :material-check: |

**Base** = no `METADATA_FILE` provided. Conditionals remove metadata, alpha metrics, and ANCOM-BC.
**Extended** = `METADATA_FILE` provided. All DCs active, facetted charts by `GROUP_COL`.

---

## Dashboard variants

=== "Base (MultiQC + Taxonomy)"

    - **MultiQC tab**: General stats, Cutadapt, FastQC plots with sample filter
    - **Community Analysis tab**: 4 metric cards + sunburst, mean rel abundance by Phylum (± std), stacked bar per sample, heatmap, data table

=== "Extended (Full Analysis)"

    - **MultiQC tab**: Same + GROUP_COL filter, DatePicker, sample filter
    - **Community Analysis tab**: All base components + alpha diversity bar chart, rarefaction curves, facetted charts by GROUP_COL, sampling locations map, heatmap with habitat/city annotations
    - **Diff. Abundance tab**: ANCOM-BC volcano plot, top differential taxa, summary cards

---

## Cross-DC links (7)

| Source | Column | Target | Target Field | Description |
|--------|--------|--------|-------------|-------------|
| `samplesheet` | `sampleID` | `multiqc_data` | `sample_name` | Filter MultiQC by samples |
| `metadata` | `ID` | `alpha_diversity` | `sample` | Filter diversity by metadata |
| `metadata` | `ID` | `alpha_rarefaction` | `sample` | Filter rarefaction by metadata |
| `metadata` | `ID` | `taxonomy_composition` | `sample` | Filter taxonomy by metadata |
| `metadata` | `ID` | `taxonomy_rel_abundance` | `sample` | Filter rel abundance by metadata |
| `samplesheet` | `sampleID` | `taxonomy_heatmap` | `sample` | Filter heatmap (base) |
| `metadata` | `ID` | `taxonomy_heatmap` | `sample` | Filter heatmap (extended) |

Metadata links are auto-pruned when `METADATA_FILE` is absent.

---

## Required data structure

```text
<DATA_ROOT>/
├── samplesheet.csv                                # --var SAMPLESHEET_FILE
├── Metadata.tsv                                   # --var METADATA_FILE (optional)
├── multiqc/
│   └── multiqc_data/
│       └── multiqc.parquet
└── qiime2/
    ├── alpha-rarefaction/                          # ⚠ Requires metadata
    │   └── faith_pd.csv
    ├── ancombc/differentials/                      # ⚠ Requires metadata + --ancombc
    │   └── Category-<GROUP_COL>-level-2/
    │       ├── lfc_slice.csv
    │       ├── p_val_slice.csv
    │       ├── q_val_slice.csv
    │       ├── se_slice.csv
    │       └── w_slice.csv
    ├── barplot/
    │   └── level-2.csv
    ├── diversity/alpha_diversity/                  # ⚠ Requires metadata
    │   └── faith_pd_vector/
    │       └── metadata.tsv
    └── rel_abundance_tables/
        └── rel-table-2.tsv
```

---

## Recipes (6)

| Recipe | Input | Output | Key transformation |
|--------|-------|--------|--------------------|
| `alpha_diversity.py` | `faith_pd_vector/metadata.tsv` | `sample`, `faith_pd` + metadata cols | Filter comment rows, rename `id` → `sample` |
| `alpha_rarefaction.py` | `faith_pd.csv` | `sample`, `depth`, `iter`, `faith_pd` | Wide → long unpivot, regex depth/iter extraction |
| `taxonomy_composition.py` | `barplot/level-2.csv` | `sample`, `taxonomy`, `count` + metadata cols | Detect taxonomy by `;` in column names |
| `taxonomy_rel_abundance.py` | `rel-table-2.tsv` + metadata DC | `sample`, `taxonomy`, `rel_abundance`, `Kingdom`, `Phylum` + metadata cols | Wide → long, taxonomy split, metadata join |
| `taxonomy_heatmap.py` | rel_abundance DC + metadata DC | `Phylum`, `Kingdom`, sample columns + `_col_annotations_json` | Pivot to wide matrix, embed metadata annotations |
| `ancombc.py` | 5 ANCOM-BC slice CSVs | `id`, `contrast`, `lfc`, `q_val`, `significant`, ... | Melt 5 slices, join, compute `-log10(q)` |

---

## Version differences

| Aspect | 2.14.0 | 2.16.0 |
|--------|--------|--------|
| Metadata sample column | `sample` | `ID` |
| Recipe override | `taxonomy_rel_abundance.py` (v2.14-specific) | shared recipe |
| Template variables | `DATA_ROOT` only | `DATA_ROOT` + `SAMPLESHEET_FILE` + optional metadata vars |
| Conditionals | none | metadata-based DC removal |

---

## Additional resources

- [nf-co.re/ampliseq](https://nf-co.re/ampliseq) — official pipeline documentation
- [nf-co.re/ampliseq/2.16.0/results](https://nf-co.re/ampliseq/2.16.0/results) — AWS test results
- [Templates reference](../../usage/projects/templates.md) — full template YAML spec
- [Recipes](../../usage/projects/recipes.md) — how to read, test, and write recipes
