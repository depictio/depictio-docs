---
title: Immunopeptidomics
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/mhcquant" target="_blank" title="nf-core/mhcquant on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mhcquant/master/docs/images/nf-core-mhcquant_logo_dark.png" alt="nf-core/mhcquant">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mhcquant/master/docs/images/nf-core-mhcquant_logo_light.png" alt="nf-core/mhcquant">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Immunopeptidomics</h1>
    <p class="template-subtitle">Identification yield and FDR behaviour, the MHC length and anchor-motif signature, replicate reproducibility, shared and private peptides with their source proteins, and retention-time and mass checks, next to the pipeline's own MultiQC report.</p>
    <p class="template-links">
      <a href="https://nf-co.re/mhcquant" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/mhcquant" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-draft template-banner-badge" data-tooltip="Draft: generated and not yet reviewed. Expect it to need fixes before it is usable."><i class="mdi mdi-pencil-outline"></i> Draft</span>
</div>

<div class="tpl-version-pick" data-latest="3.2.0">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Template version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Template version">
    <option value="3.2.0" selected>3.2.0</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The mhcquant template follows an nf-core/mhcquant run from the spectra to the
peptides each sample presents:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the sections mhcquant writes into its own MultiQC report, and how consistently the replicate injections of a sample quantify the same peptides
- :material-magnify-scan: **Search**: the spectra, PSMs and peptides of each raw file, how the raw search behaves as the FDR threshold moves, and whether the peptides elute and ionise as predicted
- :material-ruler: **Immunopeptidome**: the length profile and anchor motifs that point to the MHC class, and the peptides the conditions share with the proteins they come from

The persistent `Sample filters` (condition, sample, raw file) sit in the left
panel and apply to every tab, and the collapsed `Sample sheet` and `Reference
tables` sections are pinned to the bottom of every child tab.

!!! info "The samplesheet is not in the output"
    mhcquant does not publish the samplesheet it ran on, and the samplesheet is
    the hub every other collection links to. The template reads the file named by
    `METADATA_FILE`, which defaults to `input/samplesheet.tsv` under the data
    root: copy the sheet you passed to `--input` there, or point the variable at
    it. The CLI's metadata auto-detection picks the first non-id column of the
    sheet as the grouping column, so pass `--var GROUP_COL=Condition` unless
    `Condition` already comes second.

!!! note "No binding predictions"
    mhcquant 3.2.0 no longer runs MHCflurry or any other binding predictor, so
    the template has no binder-rank view. The MHC signature tab reads the class
    and the presenting alleles from peptide lengths and positional motifs instead.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/mhcquant_results \
      --template nf-core/mhcquant/latest \
      --var METADATA_FILE=/path/to/samplesheet.tsv \
      --var GROUP_COL=Condition
    ```

    `METADATA_FILE` can be left out when the sheet already sits at
    `input/samplesheet.tsv` under the data root. A run started without
    `--quantify` has no replicate intensities: add `--var NO_QUANTIFICATION=true`
    and the replicate collections are dropped, with the Reproducibility tab. A
    run without `--annotate_ions` takes `--var NO_ION_ANNOTATION=true`.

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/mhcquant -r 3.2.0 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md).

---

## :material-book-open-variant: Reference

The template reads the samplesheet, the MultiQC report, the per-sample peptide
tables at the output root, the Comet pin files that precede rescoring and the
fragment-ion annotations. Every other collection (sample summary, length
distribution, composition, motif matrix, replicate pairs and detection, source
proteins, condition sharing) is a recipe over the peptide table. 42 of its 58
tiles carry a `use:` catalog reference (`mhcquant/*`, `openms/*`, `multiqc/*`),
so a tile says where its panel comes from.

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="3.2.0" markdown>

--8<-- "pipeline-templates/nf-core/_generated/mhcquant-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then six child tabs in three groups, read as a
funnel from the spectra to the peptides each sample presents. Each tab below
carries the **same icon and colour the dashboard gives it**, so the page and the
app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Reproducibility |
| Search | Identification, Physico-chemical checks |
| Immunopeptidome | MHC signature, Peptides and proteins |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables and record cards follow, collapsed. The design comes
from the samplesheet: one row per raw file with its sample, its condition
(`GROUP_COL`, `Condition` by default) and its search database. The persistent
*Sample filters* (condition, sample, raw file) sit in the left panel and narrow
every tab: the links carry a pick to every sample-level table by `sample_id` and
to the Comet tables by `run_id`. The *Sample sheet* and the *Reference tables*
(the per-sample summary) are pinned, collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Immunopeptidomics, from the spectra to the peptides each sample presents.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/mhcquant/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/mhcquant/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    A short hero links the run parameters. *About this dashboard* says how the two
    filter levels work, *The run* lists the samples and raw files, the enzyme, the
    FDR threshold, the peptide length bounds and the rescoring engine, and
    *Pipeline* walks the six steps from the search to the comparison of conditions,
    each linked to its parameters and its tab. The key figures read collections
    every route writes, so a route never leaves a gap in them. The findings are live
    values: they follow the filters.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · the left panel starts collapsed. *Key figures* has its own
        filter bar (the condition and the sample), and so does *Findings* (the
        condition and the peptide length): each narrows its own section only.

        | Section | What it holds |
        |---|---|
        | Top | Hero, *About this dashboard*, *The run*, *Pipeline* |
        | Key figures | 4 headline cards: samples, PSMs, peptides, identification rate |
        | Findings | Live result rows, then 4 figures: the accepted PSMs against the FDR threshold, the observed against predicted retention time, the length profile and the source proteins |
        | How to read this dashboard | The tabs by group, each with its question |

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *Did the search identify peptides evenly across samples?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mhcquant/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/mhcquant/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only: the sections mhcquant writes into its own report. Open:
    identification counts, the q-value and Comet Xcorr distributions, then
    precursor m/z, retention time and peptide intensity. Compare the counts across
    samples first, then check that a low-yield sample's scores look like the
    others. The total ion chromatograms, the fragment mass error and the Percolator
    feature weights are collapsed, for when the cause is the acquisition or the
    rescoring model.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Report sample`, read from the MultiQC report.

        | Section | What it holds |
        |---|---|
        | Identification yield | 3 MultiQC panels |
        | Peptide properties | 3 MultiQC panels |
        | Acquisition and rescoring (collapsed) | 3 MultiQC panels |

=== ":material-set-merge:{ .mc-cyan } Reproducibility"

    **Data & QC** · *Do the replicate injections of a sample quantify the same peptides?*

    [![Reproducibility dashboard](../../images/pipeline-templates/nf-core/mhcquant/reproducibility_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/reproducibility_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Reproducibility dashboard](../../images/pipeline-templates/nf-core/mhcquant/reproducibility_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/reproducibility_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    OpenMS aligns the replicate injections of each sample and quantifies every
    peptide in each. The replicates per peptide, the peptide detections as a ring by
    replicate, the median log10 intensity and the peptides quantified in both
    replicates of a pair. Then the intensity scatter for every replicate pair and
    the UpSet of the replicate combinations: a pair off the diagonal, or a small
    all-replicate core, points at one injection to check. Replicate labels follow
    the samplesheet `ID` order within a sample. The membership table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Replicate pair` on `mhcquant_replicate_pairs` and a
        `Replicates detected` range on `mhcquant_replicate_detection`.

        | Section | What it holds |
        |---|---|
        | Replicates at a glance | 4 cards |
        | Replicate agreement | 1 advanced visualization |
        | Replicate overlap | 1 advanced visualization |
        | Replicate table (collapsed) | *Replicate membership per peptide* |

    !!! tip "Only with `--quantify`"
        Every tile here binds a replicate collection. A run without `--quantify`
        takes `--var NO_QUANTIFICATION=true`: the tab is dropped, and the replicate
        columns of the per-sample summary stay empty.

=== ":material-magnify-scan:{ .mc-blue } Identification"

    **Search** · *How many spectra became peptides, and at what FDR?*

    [![Identification dashboard](../../images/pipeline-templates/nf-core/mhcquant/identification_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/identification_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Identification dashboard](../../images/pipeline-templates/nf-core/mhcquant/identification_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/identification_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The spectra searched, as a funnel to the target matches and the PSMs accepted
    at 5% and 1% FDR; the identification rate per raw file; the PSMs that passed the
    pipeline's filter; the accepted precursors by modification. Then the accepted
    PSMs against the q-value threshold, one curve per raw file, and the score of the
    accepted peptides by sample. The Comet numbers come from the pin files, before
    MS2Rescore and Percolator, so they describe the raw search, not the final FDR.
    The Comet search table is collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Peptide score` and `PSMs per peptide` ranges on
        `mhcquant_peptides`.

        | Section | What it holds |
        |---|---|
        | Yield at a glance | 4 cards |
        | Search and FDR | 1 advanced visualization + *Score of the accepted peptides* |
        | Search table (collapsed) | *Comet search yield per raw file* |

=== ":material-waves:{ .mc-lime } Physico-chemical checks"

    **Search** · *Do the identified peptides elute and ionise as peptides should?*

    [![Physico-chemical checks dashboard](../../images/pipeline-templates/nf-core/mhcquant/physico_chemical_checks_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/physico_chemical_checks_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Physico-chemical checks dashboard](../../images/pipeline-templates/nf-core/mhcquant/physico_chemical_checks_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/physico_chemical_checks_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The retention-time error per sample, the precursor mass error per raw file, the
    correlation with the MS2PIP-predicted spectrum and the precursors by charge.
    Then the observed against DeepLC-predicted retention time, with the record of a
    picked peptide beside it, and side by side retention time against Kyte-Doolittle
    hydropathy and precursor m/z over the gradient by charge. Outliers on these
    plots are the identifications to question first. The fragment-ion cards and
    table are collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Precursor charge` and a `Retention time (min)` range on
        `mhcquant_peptides`.

        | Section | What it holds |
        |---|---|
        | Accuracy at a glance | 4 cards |
        | Chromatography | 1 advanced visualization + a peptide record card |
        | Hydropathy and charge | 2 advanced visualizations |
        | Fragment ions (collapsed) | 2 cards, *Matched fragment ions per peptide* |

    !!! tip "Only with `--annotate_ions`"
        A run without `--annotate_ions` takes `--var NO_ION_ANNOTATION=true`, and
        the Fragment ions section is dropped.

=== ":material-ruler:{ .mc-violet } MHC signature"

    **Immunopeptidome** · *Which MHC class do the peptide lengths and anchor motifs point to?*

    [![MHC signature dashboard](../../images/pipeline-templates/nf-core/mhcquant/mhc_signature_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/mhc_signature_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MHC signature dashboard](../../images/pipeline-templates/nf-core/mhcquant/mhc_signature_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/mhc_signature_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The 9-mer share per sample, the median peptide length, and the distinct
    sequences ranked by their P2 and C-terminal residues, the two class I anchors.
    Then the length profile with the class I (8 to 12) and class II (13 to 25)
    ranges shaded, the composition per sample by length, switchable to charge and
    modification, and the amino-acid frequency at each position per sample and
    length, where the anchor motifs show. A flat or shifted length profile points at
    co-purified peptides or a length filter set too wide. The length table is
    collapsed.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Peptide length` and `Modification` on `mhcquant_peptides`,
        which also narrow the length profile and the motif heatmap through the
        project links.

        | Section | What it holds |
        |---|---|
        | Signature at a glance | 4 cards |
        | Length signature | 2 advanced visualizations |
        | Anchor motifs | 1 advanced visualization |
        | Length table (collapsed) | *Peptides per length and sample* |

=== ":material-relation-many-to-many:{ .mc-grape } Peptides and proteins"

    **Immunopeptidome** · *Which peptides do conditions share, and which proteins do they come from?*

    [![Peptides and proteins dashboard](../../images/pipeline-templates/nf-core/mhcquant/peptides_and_proteins_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/peptides_and_proteins_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Peptides and proteins dashboard](../../images/pipeline-templates/nf-core/mhcquant/peptides_and_proteins_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/mhcquant/peptides_and_proteins_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The distinct sequences by condition sharing, the peptides per source protein,
    the protein intensity and the source proteins per peptide. Then the UpSet of
    the conditions each sequence was identified in, and the source proteins by the
    peptides they give against their intensity; a click selects the protein.
    Peptides private to one condition are the candidates for condition-specific
    presentation: check their support in the peptide record first. The peptide and
    protein tables are collapsed, each with a record card for the selected row.

    ??? abstract ":material-tune-variant: Filters and components"

        **Filters** · `Condition sharing` on `peptide_condition_sharing` and a
        `Peptides per protein` range on `mhcquant_source_proteins`.

        | Section | What it holds |
        |---|---|
        | Peptides at a glance | 4 cards |
        | Sharing between conditions | 1 advanced visualization |
        | Source proteins | 1 advanced visualization |
        | Peptide detail (collapsed) | *Identified peptides* + a peptide record card |
        | Protein detail (collapsed) | *Source proteins* + a protein record card |

    !!! tip "One condition"
        On a run with a single condition, the sharing split and the UpSet show a
        single set.

Tables and scatters select on their entity column: the sample sheet on
`sample_id`, which the links carry to every collection and to the MultiQC panels,
and the pinned per-sample summary on `sample`; the Comet table on raw files
(`run_id`) and the replicate membership table on peptides; the peptide table and
the three scatters of Physico-chemical checks on `sequence`, which also reaches the
condition-sharing collection; the source-protein scatter and table on `protein`;
the fragment-ion table on `peptide`. A pick narrows every tile that reads the same
collection or one linked from it, and each record card waits beside its table or
scatter for a picked row or point. The length table and the replicate-pair scatter
select nothing.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/mhcquant, it does not run the pipeline.
Run the pipeline first, with quantification and ion annotation if you want the
Reproducibility tab and the fragment checks:

```bash
nextflow run nf-core/mhcquant -r 3.2.0 \
  --input samplesheet.tsv \
  --fasta proteome.fasta \
  --quantify --annotate_ions \
  --outdir results -profile docker
```

Then point Depictio at the results, with the samplesheet you started from:

```bash
depictio ingest results/ --template nf-core/mhcquant/latest \
  --var METADATA_FILE=samplesheet.tsv --var GROUP_COL=Condition
```

See [nf-co.re/mhcquant/usage](https://nf-co.re/mhcquant/3.2.0/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio scans
recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/
│   └── samplesheet.tsv                        # the hub (METADATA_FILE default): ID, Sample, Condition, ReplicateFileName
├── <Sample>_<Condition>.tsv                   # one FDR-filtered peptide table per sample
├── multiqc/multiqc_data/
│   └── multiqc.parquet                        # mhcquant custom-content sections
├── intermediate_results/
│   ├── comet/*_pin.tsv                        # Comet PSMs per raw file, before rescoring
│   └── ion_annotations/*_matching_ions.tsv    # optional, --annotate_ions
└── pipeline_info/
    ├── params_*.json
    └── *software*versions*.yml
```

The replicate intensities are the `intensity_<k>` columns of the peptide tables,
present only with `--quantify`. The mzTab exports, the OpenMS XML intermediates
and the spectral library are not read.

---

## :material-flask-outline: Validation runs

The template was validated against the AWS megatest of the 3.2.0 release
(`results-6ec12c97f7889a3e1f09ab89930723045c6bac68`, `test_full` profile: a
PRIDE immunopeptidomics dataset of two samples with three raw replicates each,
one sample per condition), and the screenshots above come from it. With one
sample per condition, the sharing UpSet on that run is dominated by private
peptides. `megatest.yaml` lists the tables-only subset the template needs, and
the download script also places the vendored samplesheet under `input/`:

```bash
bash depictio/projects/nf-core/mhcquant/3.2.0/download_test_data.sh /tmp/mhcquant_test
depictio ingest /tmp/mhcquant_test --template nf-core/mhcquant/latest \
  --var GROUP_COL=Condition
```

Do not pass `--project` when ingesting: the dashboard is attached to the
project by name, so renaming it breaks a later `depictio dashboard import`.
Re-ingesting accumulates dashboards, so delete the project before repeating a run.

---

## :material-link-variant: Additional resources

- [nf-co.re/mhcquant](https://nf-co.re/mhcquant): official pipeline documentation
- [nf-co.re/mhcquant/3.2.0/results](https://nf-co.re/mhcquant/3.2.0/results): AWS test results
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
    <span class="tpl-credit-note">Nobody has run it on their own data and signed it off yet, which is what keeps it a Draft.</span>
    <span class="tpl-person"><i class="mdi mdi-account-plus-outline"></i> Open</span>
  </div>
  <div class="tpl-credit">
    <span class="tpl-credit-role"><i class="mdi mdi-wrench-outline"></i> Maintainers</span>
    <span class="tpl-credit-note">Keep it working as nf-core/mhcquant releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
