---
title: "Depictio Templates"
icon: material/layers-outline
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../images/logo/templates_catalog_logo.png" alt="Depictio Templates">
  <h1 class="catalog-hero__title" id="depictio-templates">Depictio Templates</h1>
</div>

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project, dashboards included, with a single command.

```bash
depictio ingest /data/my_ampliseq_run \
  --template nf-core/ampliseq/latest
```

---

## :material-view-grid-outline: Available templates

<div class="tpl-catalog" data-tpl-catalog>

<div class="tpl-catalog-bar">
  <div class="tpl-catalog-search">
    <i class="mdi mdi-magnify"></i>
    <input type="search" placeholder="Search pipelines, assays, keywords" aria-label="Search templates" data-tpl-search>
  </div>
  <div class="tpl-catalog-chips" role="group" aria-label="Filter by status">
    <button type="button" class="tpl-chip is-active" data-tpl-status="all">All</button>
    <button type="button" class="tpl-chip" data-tpl-status="certified"><i class="mdi mdi-shield-check"></i> Certified</button>
    <button type="button" class="tpl-chip" data-tpl-status="reviewed"><i class="mdi mdi-check-circle-outline"></i> Reviewed</button>
    <button type="button" class="tpl-chip" data-tpl-status="experimental"><i class="mdi mdi-flask-outline"></i> Experimental</button>
    <button type="button" class="tpl-chip" data-tpl-status="draft"><i class="mdi mdi-pencil-outline"></i> Draft</button>
  </div>
  <div class="tpl-catalog-views" role="group" aria-label="View">
    <button type="button" class="tpl-viewbtn is-active" data-tpl-view="grid" title="Grid view" aria-label="Grid view"><i class="mdi mdi-view-grid-outline"></i></button>
    <button type="button" class="tpl-viewbtn" data-tpl-view="table" title="Table view" aria-label="Table view"><i class="mdi mdi-table"></i></button>
  </div>
</div>

<div class="template-cards" data-tpl-grid>

  <a class="template-card" href="nf-core/ampliseq/" data-tpl-name="nf-core/ampliseq" data-tpl-status="reviewed" data-tpl-version="2.18.0" data-tpl-keywords="16S ITS CO1 18S amplicon metabarcoding microbiome dada2 qiime2 taxonomy diversity illumina pacbio iontorrent">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_dark.png" alt="nf-core/ampliseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/ampliseq/master/docs/images/nf-core-ampliseq_logo_light.png" alt="nf-core/ampliseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">16S · ITS · CO1 · 18S amplicon sequencing across Illumina, PacBio, and IonTorrent.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.18.0</span>
        <span class="template-status-reviewed"><i class="mdi mdi-check-circle-outline" style="vertical-align:-1px;"></i> Reviewed</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/viralrecon/" data-tpl-name="nf-core/viralrecon" data-tpl-status="reviewed" data-tpl-version="3.0.0" data-tpl-keywords="viral virus sars-cov-2 covid assembly variant calling consensus lineage pangolin nextclade coverage">
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

  <a class="template-card" href="nf-core/variantbenchmarking/" data-tpl-name="nf-core/variantbenchmarking" data-tpl-status="experimental" data-tpl-version="1.4.0" data-tpl-keywords="benchmark variant caller truth set precision recall f1 germline somatic indel structural variant sv giab">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/variantbenchmarking/master/docs/images/nf-core-variantbenchmarking_logo_dark.png" alt="nf-core/variantbenchmarking">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/variantbenchmarking/master/docs/images/nf-core-variantbenchmarking_logo_light.png" alt="nf-core/variantbenchmarking">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Benchmark variant callers against truth sets: precision, recall and F1 for germline small variants, somatic indels and structural variants.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.4.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/differentialabundance/" data-tpl-name="nf-core/differentialabundance" data-tpl-status="experimental" data-tpl-version="2.0.0" data-tpl-keywords="differential expression deseq2 rnaseq contrast volcano ma plot gene annotation variance stabilised">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/differentialabundance/master/docs/images/nf-core-differentialabundance_logo_dark.png" alt="nf-core/differentialabundance">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/differentialabundance/master/docs/images/nf-core-differentialabundance_logo_light.png" alt="nf-core/differentialabundance">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">DESeq2 differential expression: per-contrast statistics, gene annotation and the variance-stabilised sample space.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/funcscan/" data-tpl-name="nf-core/funcscan" data-tpl-status="experimental" data-tpl-version="4.0.0" data-tpl-keywords="amr antimicrobial resistance peptides amp bgc biosynthetic gene cluster cazyme screening contigs assembly hamronization">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/funcscan/master/docs/images/nf-core-funcscan_logo_dark.png" alt="nf-core/funcscan">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/funcscan/master/docs/images/nf-core-funcscan_logo_light.png" alt="nf-core/funcscan">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Functional screening of contigs: AMR genes, antimicrobial peptides, biosynthetic gene clusters and CAZymes.</p>
      <div class="template-card-meta">
        <span class="template-version">v4.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/airrflow/" data-tpl-name="nf-core/airrflow" data-tpl-status="experimental" data-tpl-version="5.1.2" data-tpl-keywords="airr bcr tcr repertoire immune receptor clonal lineage immcantation presto changeo vdj">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_dark.png" alt="nf-core/airrflow">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_light.png" alt="nf-core/airrflow">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">B and T cell repertoire analysis: sequence processing, repertoire composition and clonal analysis.</p>
      <div class="template-card-meta">
        <span class="template-version">v5.1.2</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/rnafusion/" data-tpl-name="nf-core/rnafusion" data-tpl-status="experimental" data-tpl-version="4.1.3" data-tpl-keywords="fusion gene fusion rnaseq arriba starfusion fusioncatcher fusioninspector sashimi splicing cancer">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnafusion/master/docs/images/nf-core-rnafusion_logo_dark.png" alt="nf-core/rnafusion">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnafusion/master/docs/images/nf-core-rnafusion_logo_light.png" alt="nf-core/rnafusion">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Gene-fusion detection: caller consensus, per-caller evidence, in-silico validation and splice-junction analysis.</p>
      <div class="template-card-meta">
        <span class="template-version">v4.1.3</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/rnaseq/" data-tpl-name="nf-core/rnaseq" data-tpl-status="experimental" data-tpl-version="3.26.0" data-tpl-keywords="rnaseq bulk expression salmon star quantification tpm counts transcriptome gene">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnaseq/master/docs/images/nf-core-rnaseq_logo_dark.png" alt="nf-core/rnaseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnaseq/master/docs/images/nf-core-rnaseq_logo_light.png" alt="nf-core/rnaseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Bulk RNA-seq quantification: MultiQC funnel, Salmon expression overview and a per-gene explorer.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.26.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/taxprofiler/" data-tpl-name="nf-core/taxprofiler" data-tpl-status="experimental" data-tpl-version="2.0.1" data-tpl-keywords="metagenomics taxonomy taxonomic profiling kraken2 bracken metaphlan centrifuge diamond krona taxpasta shotgun">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/taxprofiler/master/docs/images/nf-core-taxprofiler_logo_dark.png" alt="nf-core/taxprofiler">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/taxprofiler/master/docs/images/nf-core-taxprofiler_logo_light.png" alt="nf-core/taxprofiler">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Metagenomic taxonomic profiling across many classifiers, with concordance and confidence views.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/chipseq/" data-tpl-name="nf-core/chipseq" data-tpl-status="experimental" data-tpl-version="2.1.0" data-tpl-keywords="chipseq chip chromatin immunoprecipitation peaks macs3 transcription factor histone narrowpeak broadpeak consensus homer deeptools">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/chipseq/master/docs/images/nf-core-chipseq_logo_dark.png" alt="nf-core/chipseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/chipseq/master/docs/images/nf-core-chipseq_logo_light.png" alt="nf-core/chipseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Transcription-factor and histone ChIP-seq: MACS3 peaks, HOMER annotation and one consensus set per antibody.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/atacseq/" data-tpl-name="nf-core/atacseq" data-tpl-status="experimental" data-tpl-version="2.1.2" data-tpl-keywords="atacseq chromatin accessibility ataqv macs2 peaks nucleosome tss enrichment consensus homer">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/atacseq/master/docs/images/nf-core-atacseq_logo_dark.png" alt="nf-core/atacseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/atacseq/master/docs/images/nf-core-atacseq_logo_light.png" alt="nf-core/atacseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Chromatin accessibility: ataqv library quality, MACS2 broad peaks and the consensus set across libraries.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.2</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/cutandrun/" data-tpl-name="nf-core/cutandrun" data-tpl-status="experimental" data-tpl-version="3.1" data-tpl-keywords="cutandrun cut&run cut&tag chromatin profiling seacr macs2 peaks consensus target histone">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/cutandrun/master/docs/images/nf-core-cutandrun_logo_dark.png" alt="nf-core/cutandrun">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/cutandrun/master/docs/images/nf-core-cutandrun_logo_light.png" alt="nf-core/cutandrun">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">CUT&amp;RUN / CUT&amp;Tag chromatin profiling: SEACR and MACS2 side by side, their agreement and the consensus set per target.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/eager/" data-tpl-name="nf-core/eager" data-tpl-status="experimental" data-tpl-version="2.4.5" data-tpl-keywords="eager ancient dna adna damage deamination mapdamage damageprofiler contamination endogenous authentication">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/eager/dev/docs/images/nf-core-eager_logo_dark.png" alt="nf-core/eager">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/eager/dev/docs/images/nf-core-eager_logo_light.png" alt="nf-core/eager">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Ancient DNA: read preprocessing, mapping, damage patterns and contamination estimates to judge authenticity per library and sample.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.4.5</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/hic/" data-tpl-name="nf-core/hic" data-tpl-status="experimental" data-tpl-version="2.1.0" data-tpl-keywords="hic hi-c chromatin conformation contact map pairs compartments tad cooler">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_dark.png" alt="nf-core/hic">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_light.png" alt="nf-core/hic">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Hi-C: valid pair statistics, contact maps and compartment and TAD calls, from library QC to 3D genome structure.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/mag/" data-tpl-name="nf-core/mag" data-tpl-status="experimental" data-tpl-version="5.5.0" data-tpl-keywords="mag metagenome assembly binning bins checkm busco gtdb taxonomy quast">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mag/master/docs/images/nf-core-mag_logo_dark.png" alt="nf-core/mag">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mag/master/docs/images/nf-core-mag_logo_light.png" alt="nf-core/mag">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Metagenome-assembled genomes: assembly, binning, completeness and contamination, and taxonomy of the recovered bins.</p>
      <div class="template-card-meta">
        <span class="template-version">v5.5.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/methylseq/" data-tpl-name="nf-core/methylseq" data-tpl-status="experimental" data-tpl-version="2.3.0" data-tpl-keywords="methylseq methylation bisulfite bismark cpg mbias em-seq epigenetics">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/methylseq/master/docs/images/nf-core-methylseq_logo_dark.png" alt="nf-core/methylseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/methylseq/master/docs/images/nf-core-methylseq_logo_light.png" alt="nf-core/methylseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">DNA methylation: bisulfite conversion QC, M-bias, CpG coverage and methylation levels compared across samples and groups.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.3.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/nanoseq/" data-tpl-name="nf-core/nanoseq" data-tpl-status="experimental" data-tpl-version="3.0.0" data-tpl-keywords="nanoseq nanopore ont long read pycoqc nanoplot alignment quantification">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/nanoseq/master/docs/images/nf-core-nanoseq_logo_dark.png" alt="nf-core/nanoseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/nanoseq/master/docs/images/nf-core-nanoseq_logo_light.png" alt="nf-core/nanoseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Oxford Nanopore long reads: read length and quality, alignment, and transcript quantification per sample.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/sarek/" data-tpl-name="nf-core/sarek" data-tpl-status="experimental" data-tpl-version="3.11.0" data-tpl-keywords="sarek variant calling germline somatic snv indel vcf vep snpeff wgs wes">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_dark.png" alt="nf-core/sarek">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_light.png" alt="nf-core/sarek">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Germline and somatic variant calling: alignment QC, variant counts per caller, annotated variants and their genome positions.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.11.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/scrnaseq/" data-tpl-name="nf-core/scrnaseq" data-tpl-status="experimental" data-tpl-version="4.2.0" data-tpl-keywords="scrnaseq single cell rna scrna cellranger starsolo alevin knee umap barcode">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/scrnaseq/master/docs/images/nf-core-scrnaseq_logo_dark.png" alt="nf-core/scrnaseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/scrnaseq/master/docs/images/nf-core-scrnaseq_logo_light.png" alt="nf-core/scrnaseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Single-cell RNA-seq: barcode ranks, cells called, genes per cell and embeddings of the filtered cells per sample.</p>
      <div class="template-card-meta">
        <span class="template-version">v4.2.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/riboseq/" data-tpl-name="nf-core/riboseq" data-tpl-status="experimental" data-tpl-version="2.0.0" data-tpl-keywords="riboseq ribosome profiling ribo-seq periodicity p-site orf translation efficiency">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/riboseq/master/docs/images/nf-core-riboseq_logo_dark.png" alt="nf-core/riboseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/riboseq/master/docs/images/nf-core-riboseq_logo_light.png" alt="nf-core/riboseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Ribosome profiling: footprint lengths, P-site periodicity, ORF calls and translational efficiency against matched RNA-seq.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/smrnaseq/" data-tpl-name="nf-core/smrnaseq" data-tpl-status="experimental" data-tpl-version="2.4.1" data-tpl-keywords="smrnaseq small rna mirna microrna mirtrace mirdeep quantification">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/smrnaseq/master/docs/images/nf-core-smrnaseq_logo_dark.png" alt="nf-core/smrnaseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/smrnaseq/master/docs/images/nf-core-smrnaseq_logo_light.png" alt="nf-core/smrnaseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Small RNA-seq: adapter trimming, read length profiles, miRNA quantification and the contaminant fractions per sample.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.4.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/genomeassembler/" data-tpl-name="nf-core/genomeassembler" data-tpl-status="experimental" data-tpl-version="2.0.0" data-tpl-keywords="genomeassembler genome assembly de novo contig n50 busco quast merqury hifi ont">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/genomeassembler/master/docs/images/nf-core-genomeassembler_logo_dark.png" alt="nf-core/genomeassembler">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/genomeassembler/master/docs/images/nf-core-genomeassembler_logo_light.png" alt="nf-core/genomeassembler">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">De novo genome assembly: contiguity, completeness and assembly QC across assemblers and polishing steps.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/mhcquant/" data-tpl-name="nf-core/mhcquant" data-tpl-status="experimental" data-tpl-version="3.2.0" data-tpl-keywords="mhcquant immunopeptidomics mhc hla peptides mass spectrometry binding prediction">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mhcquant/master/docs/images/nf-core-mhcquant_logo_dark.png" alt="nf-core/mhcquant">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mhcquant/master/docs/images/nf-core-mhcquant_logo_light.png" alt="nf-core/mhcquant">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Immunopeptidomics: identified MHC peptides, length and anchor-motif signatures, replicate reproducibility and source proteins across runs.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.2.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/demultiplex/" data-tpl-name="nf-core/demultiplex" data-tpl-status="experimental" data-tpl-version="1.8.0" data-tpl-keywords="demultiplex demultiplexing bcl bclconvert bases2fastq index barcode lane undetermined">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/demultiplex/master/docs/images/nf-core-demultiplex_logo_dark.png" alt="nf-core/demultiplex">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/demultiplex/master/docs/images/nf-core-demultiplex_logo_light.png" alt="nf-core/demultiplex">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Run demultiplexing: reads per lane and sample, index balance, undetermined barcodes and per-sample quality.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.8.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/rnasplice/" data-tpl-name="nf-core/rnasplice" data-tpl-status="experimental" data-tpl-version="1.0.4" data-tpl-keywords="rnasplice splicing alternative splicing rmats suppa dexseq transcript usage">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnasplice/master/docs/images/nf-core-rnasplice_logo_dark.png" alt="nf-core/rnasplice">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnasplice/master/docs/images/nf-core-rnasplice_logo_light.png" alt="nf-core/rnasplice">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Alternative splicing: differential splicing events and transcript usage between conditions, with the supporting expression.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.0.4</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>


  <a class="template-card" href="nf-core/proteinfamilies/" data-tpl-name="nf-core/proteinfamilies" data-tpl-status="experimental" data-tpl-version="2.5.0" data-tpl-keywords="proteinfamilies protein families clustering mmseqs hmmer profile hmm logo alignment famsa structure">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/proteinfamilies/master/docs/images/nf-core-proteinfamilies_logo_dark.png" alt="nf-core/proteinfamilies">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/proteinfamilies/master/docs/images/nf-core-proteinfamilies_logo_light.png" alt="nf-core/proteinfamilies">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Protein families: how the input clustered, the families built or extended, and each family's alignment, conservation, structure and profile HMM.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.5.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/proteinannotator/" data-tpl-name="nf-core/proteinannotator" data-tpl-status="experimental" data-tpl-version="1.1.0" data-tpl-keywords="proteinannotator protein annotation domains interproscan hmmer pfam s4pred secondary structure esmfold">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/proteinannotator/master/docs/images/nf-core-proteinannotator_logo_dark.png" alt="nf-core/proteinannotator">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/proteinannotator/master/docs/images/nf-core-proteinannotator_logo_light.png" alt="nf-core/proteinannotator">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Protein annotation: domains from HMM libraries and InterProScan, predicted secondary structure, and structures folded on demand.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.1.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/proteinfold/" data-tpl-name="nf-core/proteinfold" data-tpl-status="experimental" data-tpl-version="2.1.0" data-tpl-keywords="proteinfold structure prediction alphafold colabfold esmfold plddt pae ramachandran protein">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/proteinfold/master/docs/images/nf-core-proteinfold_logo_dark.png" alt="nf-core/proteinfold">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/proteinfold/master/docs/images/nf-core-proteinfold_logo_light.png" alt="nf-core/proteinfold">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Structure prediction: model confidence per engine, pLDDT along the chain, the predicted aligned error and where the engines agree.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/oncoanalyser/" data-tpl-name="nf-core/oncoanalyser" data-tpl-status="experimental" data-tpl-version="3.0.0" data-tpl-keywords="oncoanalyser cancer tumor somatic wigits purple linx sage cuppa lilac copy number structural variants drivers">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/oncoanalyser/master/docs/images/nf-core-oncoanalyser_logo_dark.png" alt="nf-core/oncoanalyser">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/oncoanalyser/master/docs/images/nf-core-oncoanalyser_logo_light.png" alt="nf-core/oncoanalyser">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Cancer genomics: QC, purity and ploidy, copy number, structural variants, drivers, protein changes on the structure and immune context.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/crisprseq/" data-tpl-name="nf-core/crisprseq" data-tpl-status="experimental" data-tpl-version="2.3.0" data-tpl-keywords="crisprseq crispr gene editing guides indels cut site amplicon substitutions">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/crisprseq/master/docs/images/nf-core-crisprseq_logo_dark.png" alt="nf-core/crisprseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/crisprseq/master/docs/images/nf-core-crisprseq_logo_light.png" alt="nf-core/crisprseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Gene editing: read accounting, edit outcomes per library and per guide, and the indels and substitutions around the cut site.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.3.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/isoseq/" data-tpl-name="nf-core/isoseq" data-tpl-status="experimental" data-tpl-version="3.0.1" data-tpl-keywords="isoseq iso-seq pacbio long read isoforms transcripts ccs lima tama">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/isoseq/master/docs/images/nf-core-isoseq_logo_dark.png" alt="nf-core/isoseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/isoseq/master/docs/images/nf-core-isoseq_logo_light.png" alt="nf-core/isoseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Iso-Seq: CCS and primer QC, the full-length read funnel, isoform categories and structures per gene.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.0.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/pairgenomealign/" data-tpl-name="nf-core/pairgenomealign" data-tpl-status="experimental" data-tpl-version="3.0.4" data-tpl-keywords="pairgenomealign genome alignment last synteny divergence assemblies">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/pairgenomealign/master/docs/images/nf-core-pairgenomealign_logo_dark.png" alt="nf-core/pairgenomealign">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/pairgenomealign/master/docs/images/nf-core-pairgenomealign_logo_light.png" alt="nf-core/pairgenomealign">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Pairwise genome alignment: coverage and identity of each query on the target, divergence, assembly contiguity and synteny.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.0.4</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/drop/" data-tpl-name="nf-core/drop" data-tpl-status="experimental" data-tpl-version="1.0.0" data-tpl-keywords="drop rna outlier aberrant expression splicing mono-allelic rare disease diagnosis">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/drop/master/docs/images/nf-core-drop_logo_dark.png" alt="nf-core/drop">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/drop/master/docs/images/nf-core-drop_logo_light.png" alt="nf-core/drop">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">RNA outlier detection: aberrant expression, splicing and mono-allelic expression in rare disease cohorts.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/epitopeprediction/" data-tpl-name="nf-core/epitopeprediction" data-tpl-status="experimental" data-tpl-version="3.2.0" data-tpl-keywords="epitope mhc binding prediction neoantigen peptide hla immunology">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/epitopeprediction/master/docs/images/nf-core-epitopeprediction_logo_dark.png" alt="nf-core/epitopeprediction">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/epitopeprediction/master/docs/images/nf-core-epitopeprediction_logo_light.png" alt="nf-core/epitopeprediction">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">MHC binding prediction for variant, protein and peptide inputs.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.2.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/genomeqc/" data-tpl-name="nf-core/genomeqc" data-tpl-status="experimental" data-tpl-version="1.0.1" data-tpl-keywords="genome assembly annotation qc busco quast orthology comparison">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/genomeqc/master/docs/images/nf-core-genomeqc_logo_dark.png" alt="nf-core/genomeqc">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/genomeqc/master/docs/images/nf-core-genomeqc_logo_light.png" alt="nf-core/genomeqc">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Genome assembly and annotation QC across genomes: BUSCO, assembly statistics and orthology.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.0.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/hlatyping/" data-tpl-name="nf-core/hlatyping" data-tpl-status="experimental" data-tpl-version="2.2.0" data-tpl-keywords="hla typing optitype mhc class I immunogenetics">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/hlatyping/master/docs/images/nf-core-hlatyping_logo_dark.png" alt="nf-core/hlatyping">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/hlatyping/master/docs/images/nf-core-hlatyping_logo_light.png" alt="nf-core/hlatyping">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">HLA class I typing with OptiType from DNA or RNA reads.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.2.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/mcmicro/" data-tpl-name="nf-core/mcmicro" data-tpl-status="experimental" data-tpl-version="2.0.0" data-tpl-keywords="mcmicro multiplexed imaging tissue cycif codex cell segmentation marker spatial">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_dark.png" alt="nf-core/mcmicro">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/mcmicro/master/docs/images/nf-core-mcmicro_logo_light.png" alt="nf-core/mcmicro">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Multiplexed tissue imaging: segmented cells, marker intensities and morphology.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/nascent/" data-tpl-name="nf-core/nascent" data-tpl-status="experimental" data-tpl-version="2.3.0" data-tpl-keywords="nascent transcription gro-seq pro-seq time course bigwig enhancer genome browser">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/nascent/master/docs/images/nf-core-nascent_logo_dark.png" alt="nf-core/nascent">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/nascent/master/docs/images/nf-core-nascent_logo_light.png" alt="nf-core/nascent">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Nascent transcription time courses (GRO-seq, PRO-seq): signal along the genome and differential transcription.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.3.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/quantms/" data-tpl-name="nf-core/quantms" data-tpl-status="experimental" data-tpl-version="1.1.1" data-tpl-keywords="quantms proteomics mass spectrometry dia label-free quantification peptide protein">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/quantms/master/docs/images/nf-core-quantms_logo_dark.png" alt="nf-core/quantms">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/quantms/master/docs/images/nf-core-quantms_logo_light.png" alt="nf-core/quantms">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Label-free DIA proteomics quantification: identifications, protein abundances and QC.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.1.1</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/raredisease/" data-tpl-name="nf-core/raredisease" data-tpl-status="experimental" data-tpl-version="3.1.2" data-tpl-keywords="raredisease rare disease family trio variant ranking inheritance snv sv genmod">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/raredisease/master/docs/images/nf-core-raredisease_logo_dark.png" alt="nf-core/raredisease">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/raredisease/master/docs/images/nf-core-raredisease_logo_light.png" alt="nf-core/raredisease">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Rare disease family analysis: ranked variants and inheritance models.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.1.2</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/rnavar/" data-tpl-name="nf-core/rnavar" data-tpl-status="experimental" data-tpl-version="1.3.0" data-tpl-keywords="rnavar rna-seq variant calling germline gatk snpeff vcf">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/rnavar/master/docs/images/nf-core-rnavar_logo_dark.png" alt="nf-core/rnavar">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/rnavar/master/docs/images/nf-core-rnavar_logo_light.png" alt="nf-core/rnavar">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">RNA-seq germline variant calling: variants, annotation and alignment QC.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.3.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/stableexpression/" data-tpl-name="nf-core/stableexpression" data-tpl-status="experimental" data-tpl-version="1.1.0" data-tpl-keywords="stable expression reference genes housekeeping normalisation public datasets geo">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/stableexpression/master/docs/images/nf-core-stableexpression_logo_dark.png" alt="nf-core/stableexpression">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/stableexpression/master/docs/images/nf-core-stableexpression_logo_light.png" alt="nf-core/stableexpression">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Most stable reference genes across public expression datasets.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.1.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/viralmetagenome/" data-tpl-name="nf-core/viralmetagenome" data-tpl-status="experimental" data-tpl-version="1.2.0" data-tpl-keywords="viral metagenome virus assembly consensus genome reconstruction qc">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/viralmetagenome/master/docs/images/nf-core-viralmetagenome_logo_dark.png" alt="nf-core/viralmetagenome">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/viralmetagenome/master/docs/images/nf-core-viralmetagenome_logo_light.png" alt="nf-core/viralmetagenome">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Viral genome reconstruction from metagenomic reads: assemblies, consensus genomes and QC.</p>
      <div class="template-card-meta">
        <span class="template-version">v1.2.0</span>
        <span class="template-status-experimental"><i class="mdi mdi-flask-outline" style="vertical-align:-1px;"></i> Experimental</span>
      </div>
    </div>
  </a>

</div>

<div class="tpl-catalog-table" data-tpl-table hidden></div>

<p class="tpl-catalog-empty" data-tpl-empty hidden><i class="mdi mdi-magnify-close"></i> No template matches that search.</p>

</div>

---

## :material-shield-check-outline: Status levels

<div class="status-cards">

  <div class="status-card status-draft">
    <div class="status-card-header">
      <i class="mdi mdi-pencil-outline status-icon"></i>
      <span class="status-title">Draft</span>
    </div>
    <p class="status-desc">Generated and not yet reviewed. Expect it to need fixes before it is usable.</p>
  </div>

  <div class="status-card status-experimental">
    <div class="status-card-header">
      <i class="mdi mdi-flask-outline status-icon"></i>
      <span class="status-title">Experimental</span>
    </div>
    <p class="status-desc">Shared as-is. Feedback and PRs welcome.</p>
  </div>

  <div class="status-card status-reviewed">
    <div class="status-card-header">
      <i class="mdi mdi-check-circle-outline status-icon"></i>
      <span class="status-title">Reviewed</span>
    </div>
    <p class="status-desc">Tested, CI passes, reviewed by the Depictio team or community.</p>
  </div>

  <div class="status-card status-certified">
    <div class="status-card-header">
      <i class="mdi mdi-shield-check status-icon"></i>
      <span class="status-title">Certified</span>
    </div>
    <p class="status-desc">Validated by the <strong>pipeline lead developer</strong>. Highest trust level.</p>
  </div>

</div>

---

## :material-cog-outline: How templates work

A template bundles:

- :material-cog: **[Project configuration](../usage/projects/templates.md#template-yaml-structure)**: workflows, data collections and cross-DC links, with [`{VAR_NAME}` placeholders](../usage/projects/templates.md#template-variables)
- :material-chef-hat: **[Recipes](../usage/projects/recipes.md)**: Python transforms that turn raw pipeline outputs into dashboard-ready tables
- :material-view-dashboard: **[Dashboard YAML](../features/yaml-sync.md)**: imported on the first run, with the template variables substituted
- :material-link: **[Cross-DC links](../usage/projects/templates.md#cross-dc-links)**: interactive filtering across data collections
- :material-seed: **[Recipe seeds](../usage/projects/templates.md#recipe-seeds)**: each recipe's output committed as a `.tsv`, so the bundled project can be explored, and re-ingested, without the pipeline run behind it <small>(v1.6.0+)</small>

---

## :material-tag-multiple-outline: Pipeline version and template version { #pipeline-version-and-template-version }

A template carries two version numbers. They move independently.

<div class="grid cards" markdown>

-   :material-pipe:{ .lg .middle } **Pipeline version**

    ---

    The pipeline release whose outputs the template reads. It is the last part of the
    template id: `nf-core/rnaseq/3.26.0`. A new pipeline release gets a template of its own.

    *Choose it* with `--template`, or with the **Pipeline version** picker on a template's page.

-   :material-layers-outline:{ .lg .middle } **Template version**

    ---

    The revision of the template itself: its data collections, recipes and dashboards, for
    one pipeline release. It moves when the template improves, for example `2.0.0` to `2.1.0`.

    *Find it* beside the picker on a template's page, in the ingest log, and in the project
    and dashboard settings.

</div>

When the template version moves, what you need to do depends on which number changed:

<div class="tpl-bumps" markdown>

<div class="tpl-bump is-major" markdown>
<span class="tpl-bump-tag">Major</span> <code><b>2</b>.1.0 → <b>3</b>.0.0</code>

**The data collections changed.** A collection, a column or a template variable was added,
removed or renamed.

:material-database-refresh: Ingest the run again.
</div>

<div class="tpl-bump is-minor" markdown>
<span class="tpl-bump-tag">Minor</span> <code>2.<b>0</b>.0 → 2.<b>1</b>.0</code>

**The dashboards changed.** Figures, tabs or recipes moved; every collection keeps its columns.

:material-view-dashboard-edit-outline: Import the dashboards again.
</div>

<div class="tpl-bump is-patch" markdown>
<span class="tpl-bump-tag">Patch</span> <code>2.1.<b>0</b> → 2.1.<b>1</b></code>

**Only text changed.** Titles, captions and descriptions.

:material-check: Nothing to do; import again to get the new wording.
</div>

</div>

Depictio records the template version a project was ingested with, and the one each dashboard
was imported from. The viewer warns when a newer one is available.

---

## :material-source-pull: Contributing a template

Want to add a template for another pipeline? The contributing guide covers the directory layout, recipe requirements, and review process.

<div class="catalog-cta-wrap" markdown>
[Read the contributing guide :material-arrow-right:](../developer/contributing-templates.md){ .catalog-cta }
</div>
