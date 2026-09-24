---
title: "Depictio Templates"
icon: material/layers-outline
---

<div class="catalog-hero">
  <img class="catalog-hero__logo" style="width: 104px;" src="../images/logo/templates_catalog_logo.png" alt="Depictio Templates">
  <h1 class="catalog-hero__title" id="depictio-templates">Depictio Templates</h1>
</div>

Templates are pre-packaged project configurations that set up a complete bioinformatics analysis project — dashboards included — with a single command.

```bash
depictio-cli run \
  --template nf-core/ampliseq/latest \
  --data-root /data/my_ampliseq_run
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

  <a class="template-card" href="nf-core/airrflow/" data-tpl-name="nf-core/airrflow" data-tpl-status="experimental" data-tpl-version="5.1.0" data-tpl-keywords="airr bcr tcr repertoire immune receptor clonal lineage immcantation presto changeo vdj">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_dark.png" alt="nf-core/airrflow">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/airrflow/master/docs/images/nf-core-airrflow_logo_light.png" alt="nf-core/airrflow">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">B and T cell repertoire analysis: sequence processing, repertoire composition and clonal analysis.</p>
      <div class="template-card-meta">
        <span class="template-version">v5.1.0</span>
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

  <a class="template-card" href="nf-core/chipseq/" data-tpl-name="nf-core/chipseq" data-tpl-status="draft" data-tpl-version="2.1.0" data-tpl-keywords="chipseq chip chromatin immunoprecipitation peaks macs3 transcription factor histone narrowpeak broadpeak consensus homer deeptools">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/chipseq/master/docs/images/nf-core-chipseq_logo_dark.png" alt="nf-core/chipseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/chipseq/master/docs/images/nf-core-chipseq_logo_light.png" alt="nf-core/chipseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Transcription-factor and histone ChIP-seq: MACS3 peaks, HOMER annotation and one consensus set per antibody.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.0</span>
        <span class="template-status-draft"><i class="mdi mdi-pencil-outline" style="vertical-align:-1px;"></i> Draft</span>
      </div>
    </div>
  </a>

  <a class="template-card" href="nf-core/atacseq/" data-tpl-name="nf-core/atacseq" data-tpl-status="draft" data-tpl-version="2.1.2" data-tpl-keywords="atacseq chromatin accessibility ataqv macs2 peaks nucleosome tss enrichment consensus homer">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/atacseq/master/docs/images/nf-core-atacseq_logo_dark.png" alt="nf-core/atacseq">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/atacseq/master/docs/images/nf-core-atacseq_logo_light.png" alt="nf-core/atacseq">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Chromatin accessibility: ataqv library quality, MACS2 broad peaks and the consensus set across libraries.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.1.2</span>
        <span class="template-status-draft"><i class="mdi mdi-pencil-outline" style="vertical-align:-1px;"></i> Draft</span>
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

  <a class="template-card" href="nf-core/hic/" data-tpl-name="nf-core/hic" data-tpl-status="experimental" data-tpl-version="2.0.0" data-tpl-keywords="hic hi-c chromatin conformation contact map pairs compartments tad cooler">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_dark.png" alt="nf-core/hic">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/hic/master/docs/images/nf-core-hic_logo_light.png" alt="nf-core/hic">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Hi-C: valid pair statistics, contact maps and compartment and TAD calls, from library QC to 3D genome structure.</p>
      <div class="template-card-meta">
        <span class="template-version">v2.0.0</span>
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

  <a class="template-card" href="nf-core/sarek/" data-tpl-name="nf-core/sarek" data-tpl-status="experimental" data-tpl-version="3.10.0" data-tpl-keywords="sarek variant calling germline somatic snv indel vcf vep snpeff wgs wes">
    <div class="template-card-logo">
      <img class="nf-core-dark" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_dark.png" alt="nf-core/sarek">
      <img class="nf-core-light" src="https://raw.githubusercontent.com/nf-core/sarek/master/docs/images/nf-core-sarek_logo_light.png" alt="nf-core/sarek">
    </div>
    <div class="template-card-body">
      <p class="template-card-desc">Germline and somatic variant calling: alignment QC, variant counts per caller, annotated variants and their genome positions.</p>
      <div class="template-card-meta">
        <span class="template-version">v3.10.0</span>
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

## :material-source-pull: Contributing a template

Want to add a template for another pipeline? The contributing guide covers the directory layout, recipe requirements, and review process.

<div class="catalog-cta-wrap" markdown>
[Read the contributing guide :material-arrow-right:](../developer/contributing-templates.md){ .catalog-cta }
</div>
