# <span style="color: #45B8AC;">:material-folder-multiple:</span> YAML Configuration Reference


!!! warning "Full Configuration Template Warning"
    **Do not copy-paste this entire configuration blindly.** This reference shows all available options with their defaults and descriptions. Only specify values that differ from defaults or are required for your specific use case.


This is a complete reference of all configuration options available in Depictio YAML files, as of v1.21.0. For getting started and examples, see the [YAML Examples Guide](yaml-examples.md). For a folder no template recognises, `depictio project-builder <dir>` (v1.21.0+) defines the collections in the browser and writes an ad-hoc template next to the data, which `depictio ingest <dir> --template <bundle>` runs.

```yaml
# =============================================================================
# DEPICTIO PROJECT CONFIGURATION REFERENCE
# =============================================================================

# Required: Project identification
name:
  "My Project Name" # Required: Human-readable project name
  # Must be non-empty string
  # Example: "Multi-omics Cancer Study"

description: null # Optional: plain text shown with the project (HTML is removed)

# Optional, ignored since v1.21.0: kept so older files still validate
project_type:
  "basic" # Options are "basic" or "advanced" (default: "basic")
  # No longer decides what a project can do

# Optional: Project visibility settings
is_public:
  false # Optional: Project visibility (default: false)
  # true: Visible to all users (read-only)
  # false: Restricted to project members

# Optional: CLI integration path
yaml_config_path:
  null # Optional: Path to this YAML file (default: null)
  # Set by the CLI to the file's absolute path; never set by hand

# Optional: External project management integration
data_management_platform_project_url:
  null # Optional: URL to external project system (default: null)
  # Must start with http:// or https://
  # Example: "https://labid.embl.org/projects/123"

layout:
  null # Optional: "runs", "pipeline" or "tables" (default: null = detected)
  # Overrides the layout the viewer detects; no backend effect

realtime: # Optional: real-time updates (default: null)
  enabled: true # Default: true
  debounce_ms: 1000 # Default: 1000
  watch_data_collections: null # DC tags to watch (default: null = all)

# Accepted, but `depictio ingest` only scans the collections of `workflows`:
# declare data collections under a workflow (see below).
data_collections: [] # Optional (default: [])

# Set by Depictio, never written by hand: permissions (the CLI user becomes
# owner), registration_time, last_modified, hash, triggered_by (what ran the
# last ingestion, default "manual"), template_origin, provenance,
# published_lock, pending_owner_email.

# =============================================================================
# LINKS (Cross-DC Interactive Filtering)
# =============================================================================

links:  # Optional: Define relationships for cross-DC filtering
  - source_dc_tag: "sample_metadata"   # Required (or source_dc_id): DC holding the filter
    source_column: "sample_id"         # Required: Column to filter on
    target_dc_tag: "multiqc_fastqc"    # Required (or target_dc_id): DC to update when filtered
    target_type: "multiqc"             # Required: "table", "multiqc", "image" or "genomic_tracks"
    # source_dc_id / target_dc_id take a DC id (the `id` pinned on a DC),
    # never a tag: a tag written there matches nothing
    link_config:                       # Optional (default: resolver "direct")
      resolver: "sample_mapping"       # Default "direct"
      target_field: "sample_name"      # Optional: Field to match in target DC
      # mappings: {S1: [S1_R1, S1_R2]} # Optional: explicit variants (sample_mapping)
      # pattern: "{sample}.bam"        # Optional: must contain {sample} (pattern)
      # columns: {chrom: chromosome, pos: position}  # Required by "region"
      # case_sensitive: true           # Default: true
      # Resolvers:
      #   "direct" - Same value in both DCs
      #   "sample_mapping" - Canonical ID → MultiQC sample variants
      #   "pattern" - Template substitution (e.g., "{sample}.bam")
      #   "regex" - Target values matched by a regex
      #   "wildcard" - Glob matching (e.g., "S1*")
      #   "region" - Genomic region renamed onto the target's chrom/pos columns
    description: null                  # Optional
    enabled: true                      # Default: true; disabled links are ignored

# =============================================================================
# JOINS (tables combined at ingestion)
# =============================================================================

joins: # Optional: run by `depictio ingest` on the client, stored as a new Table DC
  - name: "expression_with_metadata" # Required: letters, digits, _ and - (1-100 chars)
    left_dc: "gene_expression"       # Required: DC tag, or "workflow.tag" across workflows
    right_dc: "sample_metadata"      # Required: must differ from left_dc
    on_columns: ["sample_id"]        # Required: at least one, no duplicates
    how: "inner"                     # Default "inner"; "left", "right", "outer"
    workflow_name: null              # Optional: workflow unscoped tags are looked up in
    persist: true                    # Default: true (write the result as a Delta table)
    description: null                # Optional
    granularity:                     # Optional: aggregate the finer table first
      aggregate_to: "sample_id"      # Required: aggregation key column
      numeric_default: "mean"        # Default "mean"; also sum, min, max, first, last, count, median
      categorical_default: "first"   # Default "first"
      column_overrides:              # Optional
        - column: "reads"
          function: "sum"

# =============================================================================
# WORKFLOWS (for projects with workflows)
# =============================================================================

workflows:
  - # Required: Workflow identification
    name:
      "rnaseq_pipeline" # Required: Unique workflow identifier
      # Example: "rnaseq_pipeline", "variant_calling"

    # Required: Execution engine information
    engine:
      name:
        "nextflow" # Required: Engine name
        # Examples: "nextflow", "snakemake", "python", "galaxy", "cwl", "shell", "r"
      version:
        "24.10.3" # Optional: Engine version for reproducibility
        # Example: "24.10.3", "7.32.0"

    # Optional: Workflow metadata
    version:
      "3.18.0" # Optional: Workflow version
      # Example: "1.0.0", "v2.3.1"
    description: "nf-core RNA-seq pipeline for expression quantification" # Optional: Workflow description
    repository_url:
      "https://github.com/nf-core/rnaseq" # Optional: Source code repository
      # Example: "https://github.com/user/workflow"
    workflow_tag:
      "nextflow/rnaseq_pipeline" # Optional: workflow identifier (CLI --workflow-name)
      # Default from a YAML file: the workflow `name`

    # Optional: Workflow registry information
    catalog:
      name:
        "nf-core" # Required in a catalog: "nf-core", "smk-wf-catalog" or "workflowhub"
      url:
        "https://nf-co.re/rnaseq" # Required in a catalog: http(s):// or git:// URL

    # Optional: run settings and provenance
    config:
      version: null # Optional
      workflow_parameters: null # Optional: free mapping of pipeline parameters
      # Filled by ingestion when the run tells: engine_name, pipeline_version,
      # nextflow_version, tools_executed

    # Required: Data location configuration
    data_location:
      structure:
        "sequencing-runs" # Required: Directory organization pattern
        # Options:
        #   "flat" - All files in single directory level
        #   "sequencing-runs" - Hierarchical run-based structure

      locations: # Required: Root directories to search
        - "{DATA_ROOT}/rnaseq_studies/cohort_2024" # Supports environment variable expansion: {VAR_NAME}
        - "/backup/rnaseq_data" # Examples: "/absolute/path/to/data", "{DATA_ROOT}/project1"
        # The CLI checks that each local location exists (a directory, or a
        # local manifest file). A location may also be an s3:// or https://
        # URL, for remote scan modes (http:// only with DEPICTIO_REMOTE_ALLOW_HTTP)

      runs_regex:
        "batch_[A-C]" # Required for "sequencing-runs" structure
        # Optional for "flat" structure
        # Regex pattern to identify individual runs
        # Example: "run_\\d+", "sample_.*", "batch[A-Z]"

      # attached_locations: written by `depictio ingest --attach-run`, not by hand

    # runs, registration_time: written by ingestion, not by hand

    # Required: Data collections for this workflow
    data_collections:
      - # Required: Unique identifier for this data collection
        data_collection_tag:
          "gene_expression" # Required: Unique within project
          # Used for referencing in links and dashboards
          # Example: "gene_counts", "quality_metrics"

        # Optional: Human-readable description
        description:
          "Per-sample gene expression quantification" # Optional: Description of the data collection
          # Used in UI tooltips and documentation

        optional: false # Default: false. In a template, the DC is dropped when
        # its source is absent instead of failing the run

        # Required: Data collection configuration
        config:
          # Required: Type of data collection
          type:
            "table" # Required: Data collection type
            # Options:
            # Case-insensitive, stored lowercase. Options:
            #   "table" - Tabular data (CSV, TSV, Excel, Parquet, Feather)
            #   "MultiQC" - MultiQC quality control reports
            #   "Image" - A table with a column of image paths; see "IMAGE" below
            #   "geojson" - GeoJSON boundary files for choropleth maps
            #   "phylogeny" - Newick / Nexus trees for the phylogenetic viz
            #   "indexed_file" - Indexed genomic files (VCF, BAM, bigWig,
            #     bigBed, GFF3, FASTA, bgzip + tabix), range-read by the
            #     browser; see the "INDEXED FILE" block below
            #   "genomic_tracks" - Manifest of genome-browser tracks, one row
            #     per track file; see the "GENOMIC TRACKS" block below
            #   "jbrowse2" - legacy, superseded by "genomic_tracks"

          source:
            "native" # Optional (default "native"): where the data comes from
            # "native" - scanned files (needs scan)
            # "transformed" - computed by a recipe (needs transform, no scan)
            # "joined", "aggregated" - derived, no scan

          transform: # Required when source is "transformed"; see Recipes
            # recipe: "nf-core/ampliseq/taxonomy_rel_abundance.py"  # Required: a .py recipe
            # source_overrides:                 # Optional: repoint a recipe source
            #   rel_table: {path: "custom/rel-table.tsv"}  # path or glob_pattern, exactly one
            # params: {marker_panel: "{MARKER_PANEL}"}      # Optional: passed to transform()
            # scope: null   # Optional (v1.21.0+): "run" (once per run), "aggregate"
            #               # (over every run) or "pipeline"; null = the recipe's default
            # materialized, run_params: written by Depictio, not by hand

          # Optional: a free label, not checked
          metatype:
            "aggregate" # Optional (default: null)
            # Conventions:
            #   "metadata" - Single annotation/metadata file per project
            #   "aggregate" - Multiple files combined into unified dataset
            # A join with a "Metadata" side gets no depictio_run_id column

          # Required for native DCs except MultiQC: File discovery configuration
          scan:
            # Required: File scanning strategy
            mode:
              "recursive" # Required: Scanning strategy
              # Options:
              #   "single" - Single file per project/run
              #   "recursive" - Pattern-based file discovery
              #   "url" - One remote file at an s3:// or https:// URL
              #   "s3_prefix" - Every object under an s3:// prefix matching a glob
              #   "manifest" - The files a Data Manifest lists for this collection
              # mode and scan_parameters must agree: a parameter block that
              # belongs to another mode is rejected with a message naming both.
              # The three remote modes are detailed under "Remote scan modes" below.

            # Required: Mode-specific scan parameters
            scan_parameters:
              # For mode: "recursive" - specify search pattern
              regex_config: # Required for recursive mode: Pattern matching configuration
                pattern:
                  "salmon/{sample_id}/quant.sf" # Required: Regex pattern for file discovery
                  # Example: "stats/.*_stats\\.tsv"
                wildcards: # Optional: what each {name} placeholder of the pattern stands for
                  - name: "sample_id" # The placeholder, and since v1.16.0 a column of the table holding what it matched
                    wildcard_regex: "[^/]+" # Regex the placeholder is replaced by
              max_depth: null # Optional: directory levels searched below each run (0 = run directory only)
              ignore: null # Optional: glob patterns skipped, e.g. ["work", "*.tmp"]

              # For mode: "single" - specify exact file (alternative to regex_config)
              # filename: "metadata/sample_info.csv"  # Required for single mode: File path
              # Can be absolute or relative path
              # scope: null   # Optional (v1.21.0+): "project" reads one file for every
              #               # run; null (default) or "run" binds each run its own file
              # run_files is written by the CLI on --attach-run, not by hand

              # For mode: "url" - one remote file, fetched by the server
              # url: "https://data.example.org/run42/metadata.tsv"  # Required: absolute s3:// or https:// URL

              # For mode: "s3_prefix" - list a bucket prefix (the remote counterpart of recursive)
              # prefix: "s3://my-bucket/run42/"          # Required: s3:// prefix, bucket included
              # pattern: "*.samples.csv"                 # Optional: glob on the key relative to the prefix, or on the file name (default "*")
              # pattern_syntax: "glob"                   # Optional: "glob" (default) or "regex"
              # id_regex: "^([^/]+?)\\.samples\\.csv$"   # Optional: one capture group, searched in the key relative to the prefix; the capture becomes depictio_manifest_id
              # max_files: 10000                         # Optional: ceiling on matching objects (default 10000, max 100000)

              # For mode: "manifest" - consume the entries of a Data Manifest
              # manifest_url: "https://data.example.org/run42/manifest.json"  # Required: https:// manifest URL (a local path in CLI context)
              # manifest_type: "samples"                 # Required: manifest `type` this collection consumes (its tag, by convention)
              # id_field: "id"                           # Optional: manifest column holding the entity id
              # url_field: "url"                         # Optional: manifest column holding the file URL
              # type_field: "type"                       # Optional: manifest column holding the type
              # run_field: "run"                         # Optional: manifest column holding the run grouping

          # Required: Type-specific configuration
          dc_specific_properties:
            # Required: File format specification
            format:
              "tsv" # Required: File format
              # Values: "csv", "tsv", "xlsx", "xls", "parquet", "feather"
              # Case-insensitive, normalized to lowercase

            # Optional (default: {}): keyword arguments passed as they are to
            # polars: scan_csv (csv, tsv), scan_parquet, scan_ipc (feather) or
            # read_excel (xls, xlsx). A key the reader does not take fails at ingestion.
            polars_kwargs:
              # Common options (scan_csv)
              separator:
                "\t" # Optional: Column separator character
                # Unset: tab for a .tsv/.tab file (or format tsv), else ","
                # Example: ",", "\t", "|", ";"
              has_header:
                true # Optional (default: true): First row contains column names
              skip_rows:
                0 # Optional: Number of rows to skip at file beginning (default: 0)
                # Useful for files with metadata headers

              # Advanced options
              schema_overrides: # Optional: Explicit column type mapping
                Name: "String" # Forces specific data types
                Length: "Int64" # Example types: "String", "Int64", "Float64", "Boolean"
                EffectiveLength: "Float64"
                TPM: "Float64"
                NumReads: "Float64"
              new_columns:
                null # Optional: Rename the columns, e.g. when has_header: false
                # Example: ["sample", "gene", "expression"]
              null_values:
                ["", "NA"] # Optional: Values to treat as null/missing (default: none)
              n_rows:
                null # Optional: Limit number of rows to read
                # Useful for testing configurations
              encoding:
                "utf8" # Optional: "utf8" (default) or "utf8-lossy"

              # Excel-specific options (read_excel, for .xlsx, .xls files)
              # sheet_name: "Results"   # Optional: sheet to read (default: the first)
              # sheet_id: 1             # Optional: 1-based sheet index, instead of sheet_name

            # Optional (default: all columns): Column filtering for performance
            keep_columns: # Optional: Column filtering
              - "Name" # If specified, only these columns are retained
              - "TPM" # Improves performance for large datasets
              - "NumReads" # Example: ["sample_id", "expression", "p_value"]

            # Optional: Column documentation
            columns_description: # Optional: Column documentation
              Name: "Gene/transcript identifier" # Human-readable column descriptions
              TPM: "Transcripts per million" # Used in dashboard tooltips and documentation
              NumReads: "Estimated read count" # Example format: column_name: "Description"

            # Optional, for Map components: both or neither
            # lat_column: "latitude"   # Column holding the latitude
            # lon_column: "longitude"  # Column holding the longitude; must differ
            # crs: "EPSG:4326"         # Default: "EPSG:4326"

          # Legacy: config.join {on_columns, how, with_dc} is still accepted but
          # no longer joins anything (its on_columns only order the Delta table).
          # Declare joins at project level, under "joins" above.

      # --- MultiQC DATA COLLECTION (v0.5.0+) ---
      - data_collection_tag:
          "multiqc_data" # Required: Unique identifier for MultiQC data

        description:
          "MultiQC quality control report data" # Optional: Description

        config:
          # Required: Type specification for MultiQC
          type:
            "MultiQC" # Required: Identifies this as a MultiQC data collection
            # NOTE: MultiQC type has special handling:
            #   - scan is optional. Without it, ingestion looks for
            #     <location>/*/multiqc_data/multiqc.parquet (also under */multiqc/
            #     and */*/); the templates declare a recursive scan instead
            #   - metatype and dc_specific_properties are optional: samples,
            #     modules and plots are filled at ingestion
            #   - Requires MultiQC 1.29+ to generate parquet format

          # scan:                       # Optional, as the templates do
          #   mode: "recursive"
          #   scan_parameters:
          #     regex_config:
          #       pattern: "multiqc/multiqc_data/multiqc.parquet"

        # NOTE: For MultiQC, use project-level "links" instead of joins
        # Links enable interactive filtering with sample_mapping resolver
        # Example link configuration (at project level):
        #   links:
        #     - source_dc_tag: "sample_metadata"
        #       source_column: "sample_id"
        #       target_dc_tag: "multiqc_data"
        #       target_type: "multiqc"
        #       link_config:
        #         resolver: "sample_mapping"

      # --- IMAGE DATA COLLECTION ---
      - data_collection_tag: "cell_images" # Required

        config:
          type: "image" # A table whose image_column holds image paths
          metatype: "Metadata"
          scan:
            mode: single
            scan_parameters:
              filename: "path/to/images.csv" # The table, not the images

          dc_specific_properties:
            format: "csv" # Required: csv, tsv, parquet, feather, xls, xlsx or mixed
            image_column: "image_path" # Required: column of image paths
            s3_base_folder:
              "s3://my-bucket/project/images/" # Optional: paths in image_column
              # are relative to it; must start with s3://
            local_images_path:
              null # Optional: local folder `depictio ingest` uploads to
              # s3_base_folder (which the CLI then requires)
            thumbnail_size: 150 # Optional: pixels, 50 to 1000 (default 150)
            supported_formats: [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tiff"] # Default
            # polars_kwargs, keep_columns, columns_description: as for a Table DC

      # --- GeoJSON DATA COLLECTION ---
      - data_collection_tag:
          "europe_geojson" # Required: Unique identifier for GeoJSON data

        description:
          "GeoJSON boundaries for European regions" # Optional: Description

        config:
          # Required: Type specification for GeoJSON
          type:
            "geojson" # Required: Identifies this as a GeoJSON data collection
            # NOTE: GeoJSON type stores FeatureCollection files in S3
            #   - Used as boundary source for choropleth_map components
            #   - Referenced by geojson_dc_tag in dashboard YAML
            #   - Requires a single .geojson file

          metatype:
            "GeoJSON" # Optional: free label

          # Required: File discovery configuration
          scan:
            mode: single
            scan_parameters:
              filename: "path/to/boundaries.geojson"

          # Required: GeoJSON-specific configuration
          dc_specific_properties:
            feature_id_key:
              "properties.NAME" # Optional (default "id"): GeoJSON property path to match locations_column
              # Maps to Plotly's featureidkey parameter
              # Common values: "id", "properties.NAME", "properties.ISO_A3"

      # --- PHYLOGENY DATA COLLECTION ---
      - data_collection_tag:
          "bacterial_tree" # Required: Unique identifier for the tree

        description: "Bacterial phylogeny, Newick file" # Optional

        config:
          type:
            "phylogeny" # Required: Identifies this as a tree data collection
            # NOTE: file-backed, nothing is parsed or converted
            #   - Ingestion copies the file as is to S3; served as raw Newick via
            #     /advanced_viz/phylogeny/{dc_id}/newick
            #   - Referenced by tree_dc_id in an advanced_viz component
            #     of kind "phylogenetic"

          metatype: "Aggregate" # Optional: free label

          scan:
            mode: single
            scan_parameters:
              filename: "path/to/tree.nwk"

          dc_specific_properties:
            format: "newick" # Optional: "newick" (default) or "nexus"

            ladderize:
              true # Optional: ladderise the tree by default (default true)
              # Viewers can toggle this in the viz controls

            # Tip annotations live in a SEPARATE Table DC, keyed by taxon
            # name, the same pattern Microreact uses. All three keys are
            # optional; without them the tree renders unannotated.
            metadata_dc_tag:
              "bacterial_metadata" # Optional: tag of the metadata Table DC
            metadata_taxon_column:
              "taxon" # Optional: column joining to tip labels (default "taxon")
            tip_label_strategy:
              "taxon" # Optional: "taxon" (leaf name IS the taxon id, default)
              #                   or "first_token" (take the first
              #                   underscore-separated token of the leaf name)

      # --- GENOMIC TRACKS DATA COLLECTION ---
      - data_collection_tag:
          "tracks" # Required: Unique identifier for the track manifest

        description: "Genome-browser tracks, one row per file" # Optional

        config:
          type:
            "genomic_tracks" # Required: Identifies this as a track manifest
            # NOTE: the manifest is ingested like a Table DC (a Delta table)
            #   - Each row names one track file in uri_column
            #   - Rendered by the "jbrowse" component; filterable and
            #     linkable like any table (target_type: "genomic_tracks")

          metatype: "Metadata" # Optional: free label

          scan:
            mode: single
            scan_parameters:
              filename: "path/to/tracks.tsv" # The manifest, not the track files

          dc_specific_properties:
            format: "tsv" # Required: manifest format (csv, tsv, parquet, feather, xls, xlsx)
            polars_kwargs:
              separator: "\t" # As for a Table DC

            # Manifest columns
            uri_column: "uri" # Column holding the track location (default "uri")
            track_id_column: "track_id" # Unique track id (default: the row's uri)
            sample_column: "sample" # Entity the track belongs to; used for cross-filtering
            format_column: "format" # Track format column (default "format")
            default_format: "bigwig" # Used when no column and no file extension tells
            # Track formats: bigwig, bedgraph, bed, bigbed, narrowpeak,
            # broadpeak, vcf, bam, cram, gff3, gtf, fasta
            index_column: "index_uri" # Index location (default "index_uri"; inferred otherwise)
            order_column: "order" # Tracks open in ascending order of this column
            name_column: "name" # Track label
            color_column: "color" # Track colour
            category_column: "category" # Folders in the track selector

            # Reference genome: a preset name or a custom assembly
            assembly:
              "hg38" # Default "hg38". Presets: hg38, hg19, hs1, mm10, mm39,
              # sacCer3, dm6, ce11, danRer11, TAIR10, wuhCor1.
              # A custom assembly is a mapping with `name` and either
              # `fasta_uri` + `fai_uri` (+ `gzi_uri` when bgzipped) or `twobit_uri`;
              # optional: display_name, aliases, chrom_sizes_uri, refname_aliases_uri

            # Where the track files are. A track uri is one of:
            #   - a relative path: uploaded to Depictio's S3 at ingestion
            #   - s3://bucket/key or https://host/path: read in place
            tracks_base_path:
              null # Optional: local folder relative uris resolve against
              # (default: the manifest's folder)
            remote_base_uri:
              null # Optional: s3:// or https:// prefix relative uris are read
              # in place under, instead of being uploaded
            direct_access:
              false # Optional: let the browser fetch https:// tracks itself
              # (the host must send CORS and Range headers)

            # Display
            display_defaults: {} # Optional: per-format JBrowse track config, keyed by track format
            presets: {} # Optional: named JBrowse config fragments a component can pick

            keep_columns: null # Optional: as for a Table DC
            columns_description: null # Optional: as for a Table DC

      # --- INDEXED FILE DATA COLLECTION ---
      - data_collection_tag: "variant_files" # Required

        config:
          type: "indexed_file" # Files read whole or by range from S3; no table
          metatype: "Aggregate" # Optional: free label
          scan:
            mode: recursive
            scan_parameters:
              regex_config:
                pattern: "variants/.*\\.vcf\\.gz"

          dc_specific_properties:
            format:
              "vcf" # Required: vcf, bam, bigwig, bigbed, gff3, fasta, tabix,
              # pdb, mmcif or pae (aliases: bw, bb, gff, cif, ent)
            index_suffix:
              null # Optional: index sidecar suffix, starting with "."
              # (default: the format's, e.g. .tbi; "" for no index)
            sample_regex:
              null # Optional: regex on the file path naming the sample
              # (named group "sample"; default: the file name without suffixes)
            sample_col: "sample" # Default "sample": the sample column name elsewhere in the project
            assembly: null # Optional: genome assembly, e.g. "hg38"
            max_file_size_mb: 512 # Default 512 (1 to 51200): larger files are skipped
```

A `genomic_tracks` collection is shown by the [genome browser](../../features/genome-browser/index.md);
the [guide](guide.md#example-genomic-tracks-dcs) has a worked example.

## Remote scan modes <small>(v1.16.0+)</small> { #remote-scan-modes }

Three scan modes fetch data from where it already is instead of walking a local
directory. Whoever ingests, the CLI or the server, reads the files there; the
server goes through a gateway that validates every URL and decides which
buckets it may read (see [Security](../../features/security.md#remote-data-sources)).
The files are materialised to Delta Lake exactly like scanned local files.
[Remote data and manifests](remote-data.md) explains when to use which.

`mode` and `scan_parameters` are cross-checked: declaring `mode: url` with a
`filename` block, for instance, is rejected with a message naming the mode the
parameters belong to and the parameters the declared mode expects. The
[scan bounds](yaml-examples.md#scan-bounds) `max_depth` and `ignore` belong to
`recursive`: a remote mode that declares them is rejected the same way.

### `url`: one remote file

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | yes | | Absolute `s3://` or `https://` URL of the file. `http://` is accepted only with `DEPICTIO_REMOTE_ALLOW_HTTP=true`, set on the server and, for a CLI ingestion, in the CLI's environment too. Validation here is syntactic; reachability and address checks happen at fetch time. |

```yaml
scan:
  mode: url
  scan_parameters:
    url: "https://data.example.org/run42/metadata.tsv"
```

### `s3_prefix`: every object under a prefix

The remote counterpart of `recursive`: list the objects under an `s3://` prefix
and keep the keys matching a glob. It is S3-only by construction, since plain
HTTPS exposes no listing operation.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prefix` | yes | | `s3://` prefix, bucket included, e.g. `s3://my-bucket/run42/` |
| `pattern` | no | `"*"` | Glob matched against the key *relative to* the prefix and against the file name, so `*.csv` rather than the full path. Its `*` also crosses `/`, so `*.csv` reaches the keys of sub-prefixes too |
| `pattern_syntax` | no | `"glob"` | How `pattern` is read: `glob` (fnmatch) or `regex`. A regex is matched from the start of the file name, and of the relative key when it contains a `/`, as in a `recursive` scan. A [run folder on S3](remote-data.md#a-run-folder-on-s3) turns each `recursive` collection into an `s3_prefix` scan that keeps the template's regex, with `regex` here |
| `id_regex` | no | `null` | Regex with exactly one capture group, searched in the key relative to the prefix, then in the file name. The capture is stored as the file's entity id and read back as the `depictio_manifest_id` column, which gives a prefix scan the same cross-DC join key as a manifest. An object it does not match is kept without an id, and the scan warns how many there are |
| `max_files` | no | `10000` | Ceiling on the number of matching objects (at most `100000`), a backstop against pointing a collection at a bucket root. The listing also stops after 10 × `max_files` keys. Either limit is reported as a warning |

```yaml
scan:
  mode: s3_prefix
  scan_parameters:
    prefix: "s3://my-bucket/run42/"
    pattern: "*.samples.csv"
    id_regex: "^([^/]+?)\\.samples\\.csv$"
```

### `manifest`: the entries of a Data Manifest

The collection consumes every manifest entry whose `type` equals
`manifest_type`. The manifest contract (`id`, `type`, `url`, optional `run`) is
described on [Remote data and manifests](remote-data.md#the-data-manifest-contract).

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `manifest_url` | yes | | `https://` URL of the manifest (JSON or CSV). In CLI context a local path is accepted too. An `s3://` URL passes validation but is not read yet |
| `manifest_type` | yes | | Which manifest `type` this collection consumes. By convention, the collection's own tag |
| `id_field` | no | `"id"` | Manifest column holding the entity id |
| `url_field` | no | `"url"` | Manifest column holding the file URL |
| `type_field` | no | `"type"` | Manifest column holding the type |
| `run_field` | no | `"run"` | Manifest column holding the run grouping. Files of a manifest without that column get `remote` as their run |

The `*_field` overrides remap a manifest with non-canonical column names onto
the contract without rewriting it. In a template, every `manifest` collection
reads the same manifest, so they must all name the same columns: **From
Manifest** refuses a template whose collections disagree.

```yaml
scan:
  mode: manifest
  scan_parameters:
    manifest_url: "{MANIFEST_URL}"
    manifest_type: "samples"
```

## See Also

- **[YAML Examples](yaml-examples.md)** - Complete configuration examples and patterns
- **[Project Guide](guide.md)** - Comprehensive project management guide
- **[Remote data and manifests](remote-data.md)** - Choosing between a URL, a prefix and a manifest
- **[Templates](templates.md)** and **[Recipes](recipes.md)** - The `template:` block, `optional` and `transform`
- **[Cross-DC Filtering](../../features/cross-dc-filtering.md)** - How links resolve
- **[CLI Reference](../../depictio-cli/usage.md)** - Command-line interface documentation
