# <span style="color: #45B8AC;">:material-dna:</span> nf-core/ampliseq

<div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;">
  <img src="../../images/pipeline-templates/nf-core/ampliseq/ampliseq_icon.png" alt="ampliseq" style="height:48px;">
  <div>
    <strong>16S/ITS amplicon sequencing — microbial community analysis</strong><br>
    <span style="color:#666;font-size:0.9em;">nf-core pipeline · <a href="https://nf-co.re/ampliseq" target="_blank">nf-co.re/ampliseq</a></span>
  </div>
  <span style="margin-left:auto;background:#45B8AC;color:#fff;padding:3px 10px;border-radius:12px;font-size:0.8em;font-weight:600;">:material-check-decagram: Official</span>
</div>

nf-core/ampliseq analyses amplicon sequencing data, by default 16S rRNA, via [QIIME2](https://qiime2.org/). Depictio's ampliseq template covers the core diversity, taxonomy, and differential abundance outputs produced by a standard pipeline run.

---

## Quick start

=== "2.16.0"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.16.0 \
      --data-root /path/to/ampliseq_results
    ```

=== "2.14.0"

    ```bash
    depictio run \
      --template nf-core/ampliseq/2.14.0 \
      --data-root /path/to/ampliseq_results
    ```

---

## Dashboards

Three dashboards are imported automatically. Each opens as a tab in the Depictio viewer.

=== "2.16.0"

    === "MultiQC"

        **nf-core/ampliseq** — Quality control overview powered by MultiQC.

        ![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png)

    === "Community Analysis"

        **Community Analysis** — Alpha diversity (Faith PD), rarefaction curves, and taxonomic composition across samples.

        ![Community Analysis dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_light.png)

    === "Differential Abundance"

        **Diff. Abundance** — ANCOM-BC differential abundance results: volcano plots, log-fold change heatmaps, and significance tables.

        ![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_light.png)

=== "2.14.0"

    === "MultiQC"

        **nf-core/ampliseq** — Quality control overview powered by MultiQC.

        ![MultiQC dashboard](../../images/pipeline-templates/nf-core/ampliseq/multiqc_light.png)

    === "Community Analysis"

        **Community Analysis** — Alpha diversity (Faith PD), rarefaction curves, and taxonomic composition across samples.

        ![Community Analysis dashboard](../../images/pipeline-templates/nf-core/ampliseq/community_light.png)

    === "Differential Abundance"

        **Diff. Abundance** — ANCOM-BC differential abundance results: volcano plots, log-fold change heatmaps, and significance tables.

        ![Differential Abundance dashboard](../../images/pipeline-templates/nf-core/ampliseq/differential_light.png)

---

## Required data structure

=== "2.16.0"

    ```text
    <DATA_ROOT>/
    ├── input/
    │   └── Metadata_full.tsv          # Sample metadata (columns: ID, name, habitat, …)
    ├── multiqc/                       # MultiQC HTML + data directory
    │   └── multiqc_data/
    │       └── multiqc.parquet
    └── qiime2/
        ├── alpha-rarefaction/
        │   └── faith_pd.csv           # Rarefaction curves (wide CSV)
        ├── ancombc/differentials/Category-habitat-level-2/
        │   ├── lfc_slice.csv
        │   ├── p_val_slice.csv
        │   ├── q_val_slice.csv
        │   ├── se_slice.csv
        │   └── w_slice.csv
        ├── barplot/
        │   └── level-2.csv            # Taxonomy barplot (wide CSV)
        ├── diversity/alpha_diversity/faith_pd_vector/
        │   └── metadata.tsv           # Faith PD per sample
        └── rel_abundance_tables/
            └── rel-table-2.tsv        # Relative abundance (wide TSV)
    ```

=== "2.14.0"

    Same structure as 2.16.0. The only difference is in `input/Metadata_full.tsv`:
    the sample identifier column is named `sample` (v2.14) instead of `ID` (v2.16).

    ```text
    <DATA_ROOT>/
    ├── input/
    │   └── Metadata_full.tsv          # column: "sample" (not "ID")
    ├── multiqc/
    │   └── multiqc_data/
    │       └── multiqc.parquet
    └── qiime2/
        └── (same as 2.16.0)
    ```

---

## Recipes — before & after

Five recipes transform raw QIIME2 outputs into dashboard-ready tables.

### Alpha diversity (`alpha_diversity.py`)

=== "Raw file — `faith_pd_vector/metadata.tsv`"

    ```text
    #q2:types	categorical	numeric
    id	habitat	faith_pd
    S001	marine	4.2134
    S002	freshwater	6.8821
    S003	marine	3.9012
    ```

    The file has a QIIME2 comment header row (`#q2:types`) and uses `id` instead of `sample`.

=== "After recipe"

    ```
    $ depictio recipe run nf-core/ampliseq/alpha_diversity.py \
        --data-dir /data/ampliseq_results --head 3

    shape: (3, 3)
    ┌──────────┬────────────┬──────────┐
    │ sample   ┆ habitat    ┆ faith_pd │
    │ ---      ┆ ---        ┆ ---      │
    │ str      ┆ str        ┆ f64      │
    ╞══════════╪════════════╪══════════╡
    │ S001     ┆ marine     ┆ 4.2134   │
    │ S002     ┆ freshwater ┆ 6.8821   │
    │ S003     ┆ marine     ┆ 3.9012   │
    └──────────┴────────────┴──────────┘
    ```

    Comment row dropped, `id` → `sample`, `faith_pd` cast to Float64.

### Alpha rarefaction (`alpha_rarefaction.py`)

=== "Raw file — `alpha-rarefaction/faith_pd.csv`"

    ```text
    ,depth-500_iter-1,depth-500_iter-2,depth-1000_iter-1,depth-1000_iter-2
    S001,2.14,2.31,3.88,3.94
    S002,3.02,2.98,5.11,5.24
    ```

    Wide format: one column per `depth_iter` combination.

=== "After recipe"

    ```
    shape: (8, 4)
    ┌────────┬───────┬──────┬──────────┐
    │ sample ┆ depth ┆ iter ┆ faith_pd │
    │ ---    ┆ ---   ┆ ---  ┆ ---      │
    │ str    ┆ i64   ┆ i64  ┆ f64      │
    ╞════════╪═══════╪══════╪══════════╡
    │ S001   ┆ 500   ┆ 1    ┆ 2.14     │
    │ S001   ┆ 500   ┆ 2    ┆ 2.31     │
    │ S001   ┆ 1000  ┆ 1    ┆ 3.88     │
    │ S002   ┆ 500   ┆ 1    ┆ 3.02     │
    └────────┴───────┴──────┴──────────┘
    ```

    Wide → long unpivot; depth and iter extracted from column names via regex.

### Relative abundance (`taxonomy_rel_abundance.py`)

=== "Raw files"

    **`rel-table-2.tsv`** — wide TSV, samples as columns:
    ```text
    # Constructed from biom file
    #OTU ID	S001	S002	S003
    k__Bacteria;p__Proteobacteria	0.42	0.31	0.55
    k__Bacteria;p__Firmicutes	0.18	0.29	0.12
    ```

    **`metadata DC`** — loaded from the `metadata` data collection (cross-DC join):
    ```text
    ID	habitat
    S001	marine
    S002	freshwater
    ```

=== "After recipe"

    ```
    shape: (6, 6)
    ┌────────┬──────────────────────────────┬───────────────┬────────────┬────────────────┬──────────────────┐
    │ sample ┆ taxonomy                     ┆ rel_abundance ┆ habitat    ┆ Kingdom        ┆ Phylum           │
    │ ---    ┆ ---                          ┆ ---           ┆ ---        ┆ ---            ┆ ---              │
    │ str    ┆ str                          ┆ f64           ┆ str        ┆ str            ┆ str              │
    ╞════════╪══════════════════════════════╪═══════════════╪════════════╪════════════════╪══════════════════╡
    │ S001   ┆ k__Bacteria;p__Proteobacte…  ┆ 0.42          ┆ marine     ┆ k__Bacteria    ┆ p__Proteobacte…  │
    │ S002   ┆ k__Bacteria;p__Proteobacte…  ┆ 0.31          ┆ freshwater ┆ k__Bacteria    ┆ p__Proteobacte…  │
    └────────┴──────────────────────────────┴───────────────┴────────────┴────────────────┴──────────────────┘
    ```

    Wide → long; taxonomy split into Kingdom/Phylum; metadata joined via cross-DC reference.

---

## Data collections overview

=== "2.16.0"

    | Tag | Type | Source | Recipe |
    |-----|------|--------|--------|
    | `metadata` | Table | `input/Metadata_full.tsv` | — |
    | `multiqc` | MultiQC | `multiqc/` | — |
    | `alpha_diversity` | Table (transformed) | `faith_pd_vector/metadata.tsv` | `alpha_diversity.py` |
    | `alpha_rarefaction` | Table (transformed) | `alpha-rarefaction/faith_pd.csv` | `alpha_rarefaction.py` |
    | `taxonomy_composition` | Table (transformed) | `barplot/level-2.csv` | `taxonomy_composition.py` |
    | `taxonomy_rel_abundance` | Table (transformed) | `rel-table-2.tsv` + metadata DC | `taxonomy_rel_abundance.py` |
    | `ancombc` | Table (transformed) | 5 ANCOM-BC CSVs | `ancombc.py` |

    5 cross-DC links connect `metadata` → all transformed tables for interactive filtering.

=== "2.14.0"

    Identical data collections. The version override for `taxonomy_rel_abundance.py` handles the `sample` column name difference in v2.14 metadata.

---

## Version differences

| Aspect | 2.14.0 | 2.16.0 |
|--------|--------|--------|
| Metadata sample column | `sample` | `ID` |
| Recipe override | `taxonomy_rel_abundance.py` (v2.14-specific) | shared recipe |
| Dashboard seeds | identical structure | identical structure |

---

## Additional resources

- [nf-co.re/ampliseq](https://nf-co.re/ampliseq) — official pipeline documentation
- [nf-co.re/ampliseq/2.16.0/results](https://nf-co.re/ampliseq/2.16.0/results) — AWS test results (reference outputs)
- [Templates reference](../../usage/projects/templates.md) — full template YAML spec
- [Recipes](../../usage/projects/recipes.md) — how to read, test, and write recipes
- [Contributing Templates](../../developer/contributing-templates.md) — add a new template
