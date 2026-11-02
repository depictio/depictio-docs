---
title: Genome assembly QC
hide:
  - navigation
---

<div class="template-banner">
  <a class="template-banner-logo" href="https://nf-co.re/genomeqc" target="_blank" title="nf-core/genomeqc on nf-co.re">
    <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/genomeqc/master/docs/images/nf-core-genomeqc_logo_dark.png" alt="nf-core/genomeqc">
    <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/genomeqc/master/docs/images/nf-core-genomeqc_logo_light.png" alt="nf-core/genomeqc">
  </a>
  <div class="template-banner-body">
    <h1 class="template-title">Genome assembly QC</h1>
    <p class="template-subtitle">Several genome assemblies and their annotations compared: contiguity, foreign and adaptor sequence, BUSCO completeness, a karyotype of conserved genes and telomeric repeats, repeat content, gene models, and the orthogroups the genomes share.</p>
    <p class="template-links">
      <a href="https://nf-co.re/genomeqc" target="_blank"><i class="mdi mdi-open-in-new"></i> nf-co.re</a>
      <a href="https://github.com/nf-core/genomeqc" target="_blank"><i class="mdi mdi-github"></i> GitHub</a>
    </p>
  </div>
  <span class="template-status-experimental template-banner-badge" data-tooltip="Experimental: shared as-is. Feedback and PRs welcome."><i class="mdi mdi-flask-outline"></i> Experimental</span>
</div>

<div class="tpl-version-pick" data-latest="1.0.1">
  <span class="tpl-version-icon"><i class="mdi mdi-source-branch"></i></span>
  <span class="tpl-version-label">Pipeline version</span>
  <select id="tpl-version" class="tpl-version-select" aria-label="Pipeline version">
    <option value="1.0.1" selected>1.0.1</option>
  </select>
  <span class="tpl-version-badge">latest</span>
</div>

The genomeqc template follows an nf-core/genomeqc run from the assemblies as they
are to the genes the genomes share:

- :material-compass-outline: **Overview**: the run in four key figures, live findings and four figures, each linked to the tab that explains it
- :material-chart-box-outline: **Data & QC**: the MultiQC report, how contiguous each assembly is, and whether it carries foreign or adaptor sequence
- :material-dna: **Genomes**: BUSCO completeness, a karyotype of conserved genes and telomeric repeats, repeat content, gene models, and the orthogroups the genomes share

The persistent `Sample filters` (the group and the genome) sit in the left panel
and narrow every tab through the genome hub, one row per assembly.

!!! info "The design table is optional"
    The samplesheet is not published and has no design column, so the design is a
    table you pass (`METADATA_FILE`: the assembly name in a `sample` column, every
    other column a factor such as a family). Without it the group filters and the
    group split fall away and the scatters draw in one colour.

---

## :material-rocket-launch-outline: Quick start

=== "Point at a finished run"

    ```bash
    depictio ingest /path/to/genomeqc_results \
      --template nf-core/genomeqc/latest \
      --var METADATA_FILE=/path/to/genome_design.tsv
    ```

    The results directory is the only required value.

    | Variable | Default | Role |
    |---|---|---|
    | `METADATA_FILE` | unset | design table, one row per assembly; without it the group filter, colours and splits fall away |
    | `GROUP_COL` | first factor column of the design table | column the dashboard groups and filters genomes by |
    | `GROUP_COL_DISPLAY` | title-cased `GROUP_COL` | reader-facing label of `GROUP_COL` in filters and cards |

=== "From the pipeline itself (v1.10.0+)"

    ```bash
    depictio config nextflow --install     # once per machine
    nextflow run nf-core/genomeqc -r 1.0.1 -profile docker --outdir results
    ```

    No `depictio ingest`, and no template named: the pipeline ingests its own
    output directory when it finishes and resolves this template from its own
    manifest. See [Nextflow trigger](../../depictio-cli/nextflow-trigger.md). The
    trigger passes no `--var`, so the run has no design table.

---

## :material-book-open-variant: Reference

The template reads the summary tables of each step: QUAST, BUSCO (assembly and
proteins), tidk, AGAT, the pipeline's gene overlap counts, OrthoFinder's
statistics, FCS-GX, FCS-adaptor, Tiara, RepeatMasker, and the native MultiQC
report, which holds QUAST only. It never reads the masked FASTAs, the RepeatMasker
`.out` tables or the tens of thousands of per-orthogroup files OrthoFinder writes.
QUAST and MultiQC label an assembly after its FASTA, every other tool after the
assembly name, and the hub joins the two.

Every tool collection but QUAST is optional, and a tool that did not run drops
what depends on it:

| Run | What goes |
|---|---|
| No annotation in the samplesheet | the Annotation and Orthology tabs, with the Annotate and Compare steps |
| `--skip_tidk` | the Karyotype tab (sequence lengths come from tidk) |
| No FCS-GX database | the Contamination tab and the Screen step |
| No `--te repeatmasker` | the Repeats tab and the Mask step |
| `--skip_busco` | the Completeness and Karyotype tabs |

!!! info "Self-adapting layout"
    The dashboard adapts to whatever the run actually produced: components bound
    to pruned or unparsed data collections are hidden, tabs left with no real
    visualizations are dropped entirely, and the remaining components are
    re-packed so there are no empty rows.

<div class="tpl-version-block" data-version="1.0.1" markdown>

--8<-- "pipeline-templates/nf-core/_generated/genomeqc-latest.md"

</div>

---

## :material-view-dashboard-outline: Dashboard tabs

One dashboard: the **Overview**, then eight child tabs in two groups, read as a
funnel from the assemblies to the genes the genomes share. Each tab below
carries the **same icon and colour the dashboard gives it**, so the page and the
app read alike.

| Group | Tabs |
|---|---|
| Data & QC | MultiQC, Assembly, Contamination |
| Genomes | Completeness, Karyotype, Repeats, Annotation, Orthology |

Each child tab opens with a short intro and a strip of four cards, then at most
three open sections; tables follow, collapsed. The *Sample sheet* (the genome
hub) is pinned, collapsed, to the bottom of every child tab.

=== ":material-compass-outline: Overview"

    *Genome assembly and annotation quality, from contiguity to the orthogroups the genomes share.*

    [![Overview dashboard](../../images/pipeline-templates/nf-core/genomeqc/overview_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/overview_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Overview dashboard](../../images/pipeline-templates/nf-core/genomeqc/overview_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/overview_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    *The run* lists the genome count, the BUSCO lineage, the annotation validator,
    the OrthoFinder version and the repeat annotation, and *Pipeline* walks six
    steps (measure, screen, mask, complete, annotate, compare), each linked to its
    parameters and its tab. Four key figures: the genomes, the N50, the complete
    BUSCOs and the N bases per 100 kb. The findings are live rows plus four
    figures: contiguity, the BUSCO classes, the gene models and each genome's genes
    by orthogroup.

=== "![MultiQC](../../images/logos/multiqc_light.svg#only-light){ width=18 }![MultiQC](../../images/logos/multiqc_dark.svg#only-dark){ width=18 } MultiQC"

    **Data & QC** · *What does the MultiQC report say about the assemblies?*

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/genomeqc/multiqc_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/multiqc_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![MultiQC dashboard](../../images/pipeline-templates/nf-core/genomeqc/multiqc_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/multiqc_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    MultiQC panels only: QUAST's assembly statistics, the sequences in QUAST's
    length bins and the general statistics. A `Report scope` filter narrows the
    panels to report rows, and the pinned genome filters reach them through the
    FASTA label.

=== ":material-puzzle-outline:{ .mc-blue } Assembly"

    **Data & QC** · *How contiguous is each assembly?*

    [![Assembly dashboard](../../images/pipeline-templates/nf-core/genomeqc/assembly_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/assembly_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Assembly dashboard](../../images/pipeline-templates/nf-core/genomeqc/assembly_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/assembly_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The N50, the L50, the assembly length and the GC content. Then the sequences
    against the N50 of every assembly on log axes, sized by length and coloured by
    group, with the record of the picked genome beside it, and the share of each
    assembly kept above QUAST's minimum lengths. Filters: N50 and sequence count.

=== ":material-shield-search:{ .mc-red } Contamination"

    **Data & QC** · *Does any assembly carry foreign or adaptor sequence?*

    [![Contamination dashboard](../../images/pipeline-templates/nf-core/genomeqc/contamination_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/contamination_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Contamination dashboard](../../images/pipeline-templates/nf-core/genomeqc/contamination_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/contamination_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The highest foreign share FCS-GX reports, the bases it flags, the adaptor bases
    and the sequences Tiara classified. Then the foreign share per genome beside
    Tiara's classes per genome, both stacked bars whose axis starts near the
    smallest bottom share (a `//` marks the cut; the Zoom switch shows the whole
    bar). The FCS-GX, FCS-adaptor and Tiara tables are collapsed.

=== ":material-check-decagram-outline:{ .mc-teal } Completeness"

    **Genomes** · *How much of the conserved gene set does each genome hold?*

    [![Completeness dashboard](../../images/pipeline-templates/nf-core/genomeqc/completeness_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/completeness_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Completeness dashboard](../../images/pipeline-templates/nf-core/genomeqc/completeness_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/completeness_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The complete BUSCOs in the assembly (a threshold at 95%) and in the proteins,
    the duplicated ones and the four classes summed. Then one stacked bar per
    BUSCO run, each assembly beside its proteins, and the assembly score against
    the protein score per genome. Filter: complete BUSCOs.

=== ":material-format-align-left:{ .mc-grape } Karyotype"

    **Genomes** · *Where do the conserved genes and telomeric repeats sit?*

    [![Karyotype dashboard](../../images/pipeline-templates/nf-core/genomeqc/karyotype_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/karyotype_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Karyotype dashboard](../../images/pipeline-templates/nf-core/genomeqc/karyotype_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/karyotype_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The sequences holding a BUSCO, the BUSCOs placed, the BUSCOs per Mb and the
    10 kb windows holding the tidk repeat. Then two ideograms, one karyotype per
    genome each, the 24 longest sequences drawn to their length: the first shaded
    by complete BUSCOs per Mb, the second by copies of the searched repeat per
    10 kb window. A genome picker sits above the chart, and a click on a bar opens
    it zoomed. genomeqc publishes no gene positions, so a whole sequence is
    shaded, not single genes.

=== ":material-repeat:{ .mc-pink } Repeats"

    **Genomes** · *How much of each genome is repeats, and of which kinds?*

    [![Repeats dashboard](../../images/pipeline-templates/nf-core/genomeqc/repeats_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/repeats_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Repeats dashboard](../../images/pipeline-templates/nf-core/genomeqc/repeats_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/repeats_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The masked share, the interspersed share, the simple repeats and the elements
    found. Then the share of each assembly that every repeat class takes; the rank
    switch opens the families. The masking summary and every class and family line
    are collapsed. Filter: repeat class.

=== ":material-file-tree-outline:{ .mc-indigo } Annotation"

    **Genomes** · *How many genes does each annotation hold, and how are they built?*

    [![Annotation dashboard](../../images/pipeline-templates/nf-core/genomeqc/annotation_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/annotation_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Annotation dashboard](../../images/pipeline-templates/nf-core/genomeqc/annotation_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/annotation_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The protein-coding genes, the exons per mRNA, the single-exon genes and the
    overlapping genes. Then every transcript type of every annotation by genes and
    exons per transcript, and the genes per type beside each annotation's genes
    split by overlap (none, another gene, nested on the opposite or the same
    strand). The gene models per type and every AGAT statistic are collapsed.

=== ":material-family-tree:{ .mc-cyan } Orthology"

    **Genomes** · *Which orthogroups do the genomes share?*

    [![Orthology dashboard](../../images/pipeline-templates/nf-core/genomeqc/orthology_light.webp#only-light){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/orthology_light.webp){ .tpl-shot target="_blank" rel="noopener" }

    [![Orthology dashboard](../../images/pipeline-templates/nf-core/genomeqc/orthology_dark.webp#only-dark){ loading=lazy }](../../images/pipeline-templates/nf-core/genomeqc/orthology_dark.webp){ .tpl-shot target="_blank" rel="noopener" }

    The orthogroups by copy class, the core every genome shares, the share of genes
    placed for the genome with the fewest, and the orthogroups of one genome. Then
    each genome's genes in shared, genome-specific or no orthogroups, an UpSet of
    the genomes each orthogroup reaches, and the one-to-one orthologues of every
    pair of genomes. Filter: copy class.

A pick on a genome reaches every per-genome collection through the project links.

---

## :material-play-circle-outline: Running the pipeline

Depictio reads the **output** of nf-core/genomeqc, it does not run the pipeline.
Run the pipeline first:

```bash
nextflow run nf-core/genomeqc -r 1.0.1 \
  --input samplesheet.csv \
  --te repeatmasker \
  --outdir results \
  -profile docker
```

A tool that did not run leaves its tab out (see the table above): the
Contamination tab needs the FCS-GX database (`--gxdb` and `--gxdb_manifest`) and
the Repeats tab needs `--te repeatmasker`. Then point Depictio at the results:

```bash
depictio ingest results/ \
  --template nf-core/genomeqc/latest \
  --var METADATA_FILE=genome_design.tsv
```

See [nf-co.re/genomeqc/usage](https://nf-co.re/genomeqc/1.0.1/docs/usage) for full pipeline documentation.

---

## :material-folder-open-outline: Required data structure

Point `depictio ingest` at the directory holding the pipeline output. Depictio
scans recursively and matches on file name.

```text
<DATA_ROOT>/
├── input/genome_metadata.tsv                   # --var METADATA_FILE (optional design table)
├── pipeline_info/
├── multiqc/multiqc_data/multiqc.parquet        # QUAST only
├── quast/<a>/<a>.quast/transposed_report.tsv   # required
├── busco/{genome,protein}/<a>/stats/*-busco.batch_summary.txt
├── busco/<mode>/<a>/ideogram/*.csv
├── tidk/<a>/search/<kind>/<a>.tsv
├── agat/<a>/stats/<a>.stats.txt
├── gene_overlaps/<a>.counts.tsv
├── orthofinder/                                # summary tables only
├── ortho_seq_count/species_ortho_seq_count.tsv
├── fcsgx/fcs_table.tsv
├── decontamination/{fcs-gx,fcs-adaptor,tiara}/
└── repeatmasker/<a>/<a>.tbl
```

---

## :material-flask-outline: Validation runs

The repository ships
[`download_test_data.sh`](https://github.com/depictio/depictio/blob/main/depictio/projects/nf-core/genomeqc/1.0.1/download_test_data.sh),
which fetches the subset of nf-core's AWS megatest run that the template needs
(files over 50 MB are skipped) and copies the vendored design table into `input/`:

```bash
bash depictio/projects/nf-core/genomeqc/1.0.1/download_test_data.sh \
  /tmp/genomeqc_test
depictio ingest /tmp/genomeqc_test \
  --template nf-core/genomeqc/latest \
  --var METADATA_FILE=/tmp/genomeqc_test/input/genome_metadata.tsv
```

The run is
`s3://nf-core-awsmegatests/genomeqc/results-bce44e5b558e21b38d4dd2b6521302246b4dae6d/`,
the 1.0.1 `test_full` run: three Hymenoptera RefSeq assemblies with their
annotations, the `hymenoptera_odb10` BUSCO lineage, FCS-GX on its test-only
database and RepeatMasker with RepeatModeler. The FCS-GX database is a smoke
test, so its contamination shares are not a real screen.

---

## :material-link-variant: Additional resources

- [nf-co.re/genomeqc](https://nf-co.re/genomeqc): official pipeline documentation
- [nf-co.re/genomeqc/results](https://nf-co.re/genomeqc/results): AWS test results
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
    <span class="tpl-credit-note">Keep it working as nf-core/genomeqc releases.</span>
    <a class="tpl-person" href="https://github.com/weber8thomas" target="_blank" rel="noopener">
      <img src="https://github.com/weber8thomas.png?size=80" alt="" loading="lazy"> weber8thomas
    </a>
  </div>
</div>

Reviewing a template on your own data, or taking over a role here, is a
contribution in itself: the [contributing guide](../../developer/contributing-templates.md)
says what each one involves.
