# YAML Project configuration breakdown

Configuration Validation

**Always validate your YAML configuration before using:**

```
# Validate configuration syntax and structure
depictio -v config check --project-config-path ./my_project.yaml
```

**For YAML syntax highlighting in VS Code:** Install the YAML extension and save files with `.yaml` or `.yml` extension.

Configuration Template Warning

**Do not copy-paste entire configurations blindly.** This reference shows all available options with their defaults and descriptions. Only specify values that differ from defaults or are required for your specific use case.

This guide provides comprehensive YAML configuration examples for Depictio projects, from simple setups to complex bioinformatics workflows. For a complete reference of all options, see the [Configuration Reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md).

## Quick Start Examples

Choose your starting point based on your project complexity. `project_type` is optional and ignored since v1.21.0, so the examples omit it.

Perfect for direct file upload and analysis:

```
name: "My Analysis Project"

# Files will be uploaded through the web interface
# No additional configuration needed!
```

For CLI-based projects with direct files. `depictio ingest` scans the collections of a workflow, so even one table sits under a `flat` workflow:

```
name: "CSV Analysis Project"
is_public: false

workflows:
  - name: "tables"
    engine:
      name: "python"
    data_location:
      structure: "flat"
      locations:
        - "/path/to"
    data_collections:
      - data_collection_tag: "main_data"
        description: "Primary dataset for analysis"
        config:
          type: "table"
          metatype: "metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "/path/to/data.csv"
          dc_specific_properties:
            format: "csv"
            polars_kwargs:
              separator: ","
              has_header: true
```

For workflow-generated data with pattern matching:

```
name: "RNA-seq Analysis"

workflows:
  - name: "rnaseq_pipeline"
    engine:
      name: "nextflow"
      version: "24.10.3"
    data_location:
      structure: "sequencing-runs"
      locations:
        - "{DATA_LOCATION}/results"
      runs_regex: "run_.*"
    data_collections:
      - data_collection_tag: "gene_counts"
        config:
          type: "table"
          metatype: "aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: "counts/.*\\.tsv"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              separator: "\t"
              has_header: true
```

## Configuration Schema

### Project-Level Configuration

All projects share these top-level configuration options:

```
# === REQUIRED FIELDS ===

# Project identification
name: string                              # Required: Human-readable project name
                                          # Must be non-empty string
                                          # Example: "Multi-omics Cancer Study"


# Workflow definitions: every data collection the CLI ingests sits in one
workflows: [Workflow]                     # Default: [] (empty for UI-only projects)
                                          # Array of workflow configurations
                                          # See "Workflow Configuration" section

# === REQUIRED FIELDS WITH DEFAULT VALUES ===

# Legacy field, optional and ignored since v1.21.0
project_type: "basic" | "advanced"        # Default: "basic"
                                          # Still accepted, but no longer decides
                                          # what a project can do

# Project visibility
is_public: boolean                        # Default: false
                                          # true: Visible to all users (read-only)
                                          # false: Restricted to project members

# CLI integration (typically auto-managed)
yaml_config_path: string | null          # Default: null
                                          # Path to this YAML configuration file
                                          # Auto-populated by CLI, rarely set manually

# === OPTIONAL FIELDS ===

# External project management integration
data_management_platform_project_url: string | null    # Default: null
                                                        # URL to external project system
                                                        # Must start with http:// or https://
                                                        # Example: "https://labid.embl.org/projects/123"

description: string | null                # Default: null. Plain text (HTML is removed)

links: [DCLink]                           # Default: []. See "Cross-DC Links"
joins: [JoinDefinition]                   # Default: []. See "Data Collection Joins"

layout: "runs" | "pipeline" | "tables" | null  # Default: null (detected by the viewer)

realtime:                                 # Default: null
  enabled: boolean                        # Default: true
  debounce_ms: int                        # Default: 1000
  watch_data_collections: [string] | null # Default: null (all)
```

### Project Shapes

Since v1.21.0 there is no project type to choose. `project_type` is still accepted in YAML and kept in the model, so older files validate, but it is optional and ignored. A project has workflows or it does not.

#### Tables only

Designed to be minimal and easy to set up, WebUI compatible, and suitable for small-scale analyses.

**Use cases:**

- Direct CSV/Excel file analysis
- Ad-hoc data exploration
- Small-scale studies (< 100 files)
- Quick prototyping and visualization

**Configuration:**

- Minimal setup required
- Data uploaded via the web interface, which creates a workflow under the hood
- From the CLI, tables are declared under a `flat` workflow (see **Tables only (CLI)** above): `depictio ingest` does not scan a top-level `data_collections`

#### With workflows

Designed for complex data processing pipelines, automated workflows, and large-scale analyses.

**Use cases:**

- Bioinformatics pipeline outputs
- Multi-sample studies oriented
- Automated data ingestion and updates
- Core facility workflows

**Configuration:**

- Requires `workflows` and `data_collections` definitions (1 workflow contains >= 1 data collection(s))
- CLI-driven data processing
- Regex-based file discovery
- Multi-run aggregation capabilities

## Workflow Configuration

Projects with workflows use workflows to describe data organization patterns. Each workflow corresponds to a computational pipeline that generates structured data.

```
workflows:
  - # === REQUIRED FIELDS ===

    name: string                          # Required: Workflow identifier
                                          # Must be non-empty
                                          # Example: "rnaseq_pipeline", "variant_calling"

    engine:                               # Required: Execution engine information
      name: string                        # Required: Engine name
                                          # Examples: "nextflow", "snakemake", "python",
                                          #          "galaxy", "cwl", "shell", "r"
                                          # Note: currently not validated against a list

      version: string | null              # Optional: Engine version for reproducibility
                                          # Example: "24.10.3", "7.32.0"
                                          # Note: version is currently saved only for the sake of documentation, no functional impact on the system, will be implemented in the future

    data_location:                        # Required: Where to find workflow outputs
      structure: string                   # Required: Directory organization pattern
                                          # Options:
                                          # - "flat": All files in single directory level
                                          # - "sequencing-runs": Hierarchical run-based structure

      locations: [string]                 # Required: Root directories to search
                                          # Supports environment variable expansion: {VAR_NAME}
                                          # The CLI checks each local one exists
                                          # Examples:
                                          #   - "/absolute/path/to/data"
                                          #   - "{DATA_ROOT}/project1"
                                          #   - "{HOME}/workflows/results"
                                          #   - "s3://my-bucket/run42/" (remote modes)

      runs_regex: string | null           # Required if structure="sequencing-runs"
                                          # Optional if structure="flat"
                                          # Regex pattern to identify individual runs
                                          # Example: "run_\\d+", "sample_.*", "batch[A-Z]"

    data_collections: [DataCollection]    # Required: Data collection definitions
                                          # Array of data collections for this workflow
                                          # See "Data Collections Configuration"

    # === OPTIONAL FIELDS ===

    version: string | null                # Optional: Workflow version
                                          # Example: "1.0.0", "v2.3.1"
                                          # Note: version is currently saved only for the sake of documentation, no functional impact on the system, will be implemented in the future

    description: string | null            # Optional: Workflow description

    catalog:                              # Optional: Workflow registry information
      name: string                        # Required in a catalog: "nf-core", "smk-wf-catalog", "workflowhub"
      url: string                         # Required in a catalog: http(s):// or git:// URL
                                          # Example: "https://nf-co.re/rnaseq"

    repository_url: string | null         # Optional: Source code repository
                                          # Example: "https://github.com/user/workflow"

    workflow_tag: string | null           # Optional: Workflow identifier, used by --workflow-name
                                          # Default from a YAML file: the workflow name

    config:                               # Optional: Workflow-specific configuration
      version: string | null              # Workflow configuration version
      workflow_parameters: object | null # Workflow-specific parameters
      # engine_name, pipeline_version, nextflow_version, tools_executed:
      # filled by ingestion from the run's provenance
```

### Workflow Data Location Patterns

#### Flat Structure

```
data_location:
  structure: "flat"
  locations:
    - "/data/project1/results"
    - "{BACKUP_LOCATION}/project1"  # Environment variable expansion
  # runs_regex not needed for flat structure

# Directory layout:
# /data/project1/results/
# ├── sample1_stats.csv
# ├── sample2_stats.csv
# ├── sample1_counts.tsv
# └── sample2_counts.tsv
```

#### Sequencing-Runs Structure

```
data_location:
  structure: "sequencing-runs"
  locations:
    - "{DATA_ROOT}/rnaseq_study"
  runs_regex: "run_\\d+"  # Required: matches run_001, run_002, etc.

# Directory layout:
# ${DATA_ROOT}/rnaseq_study/
# ├── run_001/
# │   ├── sample_A/
# │   │   ├── stats.tsv
# │   │   └── counts.tsv
# │   └── sample_B/
# │       ├── stats.tsv
# │       └── counts.tsv
# └── run_002/
#     ├── sample_C/
#     │   ├── stats.tsv
#     │   └── counts.tsv
#     └── sample_D/
#         ├── stats.tsv
#         └── counts.tsv
```

### Environment Variable Expansion

Depictio supports environment variable expansion in file paths:

```
# Environment setup
# export DATA_ROOT="/mnt/storage/projects"
# export PROJECT_NAME="cancer_study"
# export BACKUP_LOCATION="/backup/data"

data_location:
  structure: "flat"
  locations:
    - "{DATA_ROOT}/{PROJECT_NAME}/results"     # Expands to: /mnt/storage/projects/cancer_study/results
    - "{BACKUP_LOCATION}/{PROJECT_NAME}"       # Expands to: /backup/data/cancer_study
```

**Common Environment Variables:**

- `DATA_ROOT`, `DATA_LOCATION` - Primary data storage
- `PROJECT_ROOT` - Project base directory
- `HOME`, `USER` - User-specific paths
- `SCRATCH_DIR`, `TEMP_DIR` - Temporary storage locations

## Data Collections Configuration

Data collections define how to discover, process, and structure your data files. They are the core building blocks that connect file system data to Depictio dashboards.

```
data_collections:
  - # === REQUIRED FIELDS ===

    data_collection_tag: string    # Required: Unique identifier within project
                                  # Must be unique across all data collections
                                  # Used for referencing in links and dashboards
                                  # Example: "gene_counts", "quality_metrics"

    config:                     # Required: Data collection configuration
      type: string                # Required: Data collection type (case-insensitive)
                                  # Options:
                                  #  - "table": Tabular data (CSV, TSV, Excel, Parquet, Feather)
                                  #  - "MultiQC": MultiQC quality control reports
                                  #  - "Image": A table with a column of image paths
                                  #  - "geojson": GeoJSON boundary files for choropleth maps
                                  #  - "phylogeny": Newick / Nexus trees
                                  #  - "indexed_file": VCF, BAM, bigWig, ... read by range
                                  #  - "genomic_tracks": Manifest of genome-browser tracks

      source: string              # Optional: "native" (default), "transformed",
                                  # "joined" or "aggregated"; only "native" needs scan

      metatype: string | null    # Optional: free label, not checked
                                  # Conventions:
                                  # - "metadata": Single annotation/metadata file per project
                                  # - "aggregate": Multiple files combined into unified dataset

      scan:                     # Required for native DCs, except MultiQC
        mode: string              # Required: Scanning strategy
                                  # Options:
                                  # - "single": Single file per project/run
                                  # - "recursive": Pattern-based file discovery
                                  # - "url": One remote file (s3:// or https://)
                                  # - "s3_prefix": Objects under an s3:// prefix matching a glob
                                  # - "manifest": Files listed in a Data Manifest

        scan_parameters:        # Required: Mode-specific parameters
          # For mode: "single"
          filename: string      # Required: Relative or absolute file path
                               # Example: "metadata/sample_info.csv"

          # For mode: "recursive"
          regex_config:         # Required: Pattern matching configuration
            pattern: string    # Required: Regex pattern for file discovery
                              # Example: "stats/.*_stats\\.tsv"
            wildcards: [...]   # Optional: {name} placeholders of the pattern, each a column (v1.16.0+)
          max_depth: int | null # Optional: directory levels searched below each run
                                # directory; 0 = files directly in it (v1.15.0+)
          ignore: [string] | null  # Optional: glob patterns to skip, matched against
                                   # the name or the run-relative path (v1.15.0+)

          # For mode: "url"
          url: string           # Required: Absolute s3:// or https:// URL

          # For mode: "s3_prefix"
          prefix: string        # Required: s3:// prefix, bucket included
          pattern: string       # Optional: Glob on the key relative to the prefix (default "*")
          pattern_syntax: string  # Optional: "glob" (default) or "regex"
          id_regex: string | null  # Optional: One capture group; the capture becomes depictio_manifest_id
          max_files: int        # Optional: Listing ceiling (default 10000)

          # For mode: "manifest"
          manifest_url: string  # Required: Manifest URL (a local path in CLI context)
          manifest_type: string # Required: Manifest `type` this collection consumes
          id_field: string      # Optional: Column overrides for non-canonical manifests
          url_field: string     # (defaults: "id", "url", "type", "run")
          type_field: string
          run_field: string | null

      dc_specific_properties:   # Required for table, image, indexed_file and
                                # genomic_tracks; defaulted for the other types
        # See "Table Configuration" section for details

      transform:                # Required when source is "transformed"
        recipe: string          # See the template pattern below and Recipes

    # === OPTIONAL FIELDS ===

    description: string | null  # Optional: Human-readable description
                               # Example: "Per-sample quality control metrics"

    optional: boolean          # Default: false. In a template, drop the DC
                               # instead of failing when its data is absent
```

### Specific Data Collection Types

Data Collection Types

Data collections can be of different types, each with its own configuration requirements. Supported types: **Table** (structured tabular data), **MultiQC** (quality control reports), **Image** (image galleries), **GeoJSON** (boundary files for choropleth maps), **Phylogeny** (trees), **Indexed file** and **Genomic tracks** (genome browser). The [reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md) lists every type's properties.

#### **Table** Data Collection Configuration

Table data collections handle structured tabular data (CSV, TSV, Excel, Parquet, Feather):

```
dc_specific_properties:
  # === REQUIRED FIELDS ===

  format: string               # Required: File format
                              # Values: "csv", "tsv", "xlsx", "xls", "parquet", "feather"
                              # Case-insensitive, normalized to lowercase

  # === OPTIONAL FIELDS ===

  polars_kwargs: object       # Default: {}. Keyword arguments for the polars reader
                             # See "Polars Configuration" section

  keep_columns: [string] | null    # Optional: Column filtering
                                  # If specified, only these columns are retained
                                  # Improves performance for large datasets
                                  # Example: ["sample_id", "expression", "p_value"]

  columns_description: {string: string} | null  # Optional: Column documentation
                                               # Human-readable column descriptions
                                               # Used in dashboard tooltips and documentation
                                               # Example:
                                               #   sample_id: "Unique sample identifier"
                                               #   expression: "Log2 expression level"
```

#### **MultiQC** Data Collection Configuration (v0.5.0+)

MultiQC data collections provide specialized handling for quality control reports with automatic detection:

```
config:
  # === REQUIRED FIELD ===

  type: "MultiQC"          # Required: Identifies this as a MultiQC data collection

  # === AUTOMATIC HANDLING ===
  # The following are NOT required for MultiQC type:
  # - metatype: Optional free label
  # - scan: Without it, ingestion looks for */multiqc_data/multiqc.parquet
  #   (also */multiqc/multiqc_data/ and */*/multiqc_data/) under each location.
  #   The templates declare a recursive scan on that path instead
  # - dc_specific_properties: Filled at ingestion (samples, modules, plots)

  # === REQUIREMENTS ===
  # - MultiQC 1.29+ must be used to generate parquet format
  # - Each run directory must contain: multiqc_data/multiqc.parquet
```

#### **GeoJSON** Data Collection Configuration

GeoJSON data collections store boundary files (FeatureCollections) used as the geometry source for choropleth map components:

```
config:
  # === REQUIRED FIELDS ===

  type: "geojson"          # Required: Identifies this as a GeoJSON data collection

  metatype: "GeoJSON"      # Optional: free label

  scan:                    # Required: File discovery
    mode: "single"
    scan_parameters:
      filename: "path/to/boundaries.geojson"

  dc_specific_properties:
    feature_id_key: "properties.NAME"  # Optional (default "id"): GeoJSON property path
                                       # to match the locations_column
                                       # in choropleth map components
                                       # Common values: "id", "properties.NAME",
                                       #   "properties.ISO_A3"
```

**GeoJSON-Specific Notes:**

- **Purpose**: Provides region boundaries for `choropleth_map` components
- **Dashboard Reference**: Referenced via `geojson_dc_tag` in dashboard YAML
- **File Format**: Standard GeoJSON FeatureCollection (`.geojson`)
- **Feature ID Key**: Maps to Plotly's `featureidkey` parameter, identifying which GeoJSON property matches the `locations_column` in your tabular data

#### **Phylogeny** Data Collection Configuration

Phylogeny data collections hold a Newick or Nexus tree. Ingestion copies the file as is to S3: nothing is parsed or converted. Tip annotations live in a **separate Table data collection** keyed by taxon name, and the phylogeny DC names it so every phylogenetic component inherits the same join.

```
data_collections:
  - data_collection_tag: "bacterial_tree"
    description: "Bacterial phylogeny (21 taxa), Newick format"
    config:
      # === REQUIRED FIELDS ===

      type: "phylogeny"        # Required: Identifies this as a tree data collection

      metatype: "Aggregate"    # Optional: free label

      scan:                    # Required: File discovery
        mode: "single"
        scan_parameters:
          filename: "{DATA_ROOT}/trees/bacterial_tree.nwk"

      # === OPTIONAL FIELDS ===

      dc_specific_properties:
        format: "newick"                      # "newick" (default) or "nexus"
        ladderize: true                       # Ladderise by default; viewers can toggle
        metadata_dc_tag: "bacterial_metadata" # Table DC supplying tip annotations
        metadata_taxon_column: "taxon"        # Column joining to tip labels
        tip_label_strategy: "taxon"           # "taxon" (default) or "first_token"

  # The metadata table is an ordinary Table DC
  - data_collection_tag: "bacterial_metadata"
    description: "Tip metadata (group / habitat / resistance)"
    config:
      type: "Table"
      metatype: "Aggregate"
      scan:
        mode: "single"
        scan_parameters:
          filename: "{DATA_ROOT}/trees/bacterial_metadata.tsv"
      dc_specific_properties:
        format: "TSV"
        polars_kwargs:
          separator: "\t"
```

**Phylogeny-Specific Notes:**

- **No materialisation**: unlike a Table DC there is no Delta table and no Parquet copy. The backend serves the raw Newick over `/advanced_viz/phylogeny/{dc_id}/newick`
- **Metadata is optional**: leave the three `metadata_*` keys out and the tree still renders, just unannotated
- **Tip labels**: use `tip_label_strategy: "first_token"` when leaf names carry a suffix, so `Escherichia_coli_K12` joins as `Escherichia_coli`
- **Component reference**: an `advanced_viz` component of kind `phylogenetic` points at the tree with `tree_wf_id` / `tree_dc_id`, then colours tips from any column of the metadata DC. See [Phylogenetic](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#phylogenetic)

______________________________________________________________________

**Linking MultiQC with Metadata (Recommended):**

Use **links** for interactive filtering between metadata tables and MultiQC:

```
# At project level - enables cross-DC filtering
links:
  - source_dc_tag: sample_metadata   # Filter from metadata table
    source_column: sample_id          # Filter by sample ID
    target_dc_tag: multiqc_data       # Update MultiQC visualizations
    target_type: multiqc              # Target type
    link_config:
      resolver: sample_mapping        # Maps canonical IDs to MultiQC sample variants
```

**MultiQC-Specific Notes:**

- **Automatic Detection**: No need to specify file paths or patterns
- **Fixed Location**: Without a `scan`, the system looks for `multiqc_data/multiqc.parquet` one or two levels below each location
- **Format Requirement**: Requires MultiQC 1.29+ to generate `.parquet` output
- **No Configuration Overhead**: Just specify `type: "MultiQC"` and you're done
- **Link Column**: Use `sample_mapping` resolver in links to connect with metadata tables

**Example Directory Structure:**

```
project_root/
├── run_001/
│   └── multiqc_data/
│       └── multiqc.parquet    # Auto-detected
├── run_002/
│   └── multiqc_data/
│       └── multiqc.parquet    # Auto-detected
└── run_003/
    └── multiqc_data/
        └── multiqc.parquet    # Auto-detected
```

### Polars Configuration Options

Polars is Depictio's high-performance data processing engine. Configure data reading with these options:

```
polars_kwargs:
  # === COMMON OPTIONS ===

  # Passed as is to polars: scan_csv (csv, tsv), scan_parquet,
  # scan_ipc (feather) or read_excel (xls, xlsx). Use that reader's
  # argument names: an unknown key fails at ingestion.

  # CSV/TSV specific
  separator: string           # Column separator character
                             # Default: tab for a .tsv/.tab file (or format
                             # tsv), else ","
                             # Example: ",", "\t", "|", ";"

  has_header: boolean        # First row contains column names
                            # Default: true
                            # Set false if first row is data

  skip_rows: int            # Number of rows to skip at file beginning
                           # Default: 0
                           # Useful for files with metadata headers
                           # Example: 3 (skip first 3 lines)

  # === ADVANCED OPTIONS ===

  # Data types
  schema_overrides: object  # Explicit column type mapping
                           # Forces specific data types
                           # Example:
                           #   sample_id: "String"
                           #   count: "Int64"
                           #   p_value: "Float64"
                           #   significant: "Boolean"

  new_columns: [string]     # Rename the columns
                           # Useful when has_header: false
                           # Example: ["sample", "gene", "expression"]

  # Missing data handling
  null_values: [string]     # Values to treat as null/missing
                           # Default: none
                           # Example: ["NA", "N/A", "", "null", "-"]

  # Performance options
  n_rows: int               # Limit number of rows to read
                           # Useful for testing configurations
                           # Example: 1000 (read only first 1000 rows)

  # Encoding
  encoding: string          # File encoding
                           # Default: "utf8"; the other value is "utf8-lossy"

  # Excel specific (read_excel, for .xlsx, .xls files)
  sheet_name: string        # Excel sheet name to read
                           # Default: first sheet
                           # Example: "Results", "Sheet1"

  sheet_id: int            # Excel sheet number, 1-based
                          # Alternative to sheet_name
                          # Example: 1 (first sheet), 2 (second sheet)
```

### File Scanning Patterns

#### Single File Mode

Best for metadata files or summary statistics generated once per project:

```
scan:
  mode: "single"
  scan_parameters:
    filename: "multiqc_data/multiqc_general_stats.txt"

# Finds exactly one file:
# project_root/multiqc_data/multiqc_general_stats.txt
```

With several runs, each run reads its own copy of `filename`. Since **v1.21.0**, `scope: "project"` under `scan_parameters` reads one file for every run instead.

#### Recursive Mode

Uses regex patterns to discover files across directory structures:

```
scan:
  mode: "recursive"
  scan_parameters:
    regex_config:
      pattern: "star_salmon/{sample_id}/quant.sf"
      # Wildcards (optional): each {name} in the pattern stands for its regex
      wildcards:
        - name: "sample_id"
          wildcard_regex: "[^/]+"
    max_depth: 5        # Optional: limit search depth

# Matches files like:
# run_001/star_salmon/sample_A/quant.sf
# run_001/star_salmon/sample_B/quant.sf
# run_002/star_salmon/sample_C/quant.sf
```

A wildcard names a part of the pattern: `{sample_id}` in `pattern` is replaced by its `wildcard_regex` before files are matched. Since **v1.16.0**, each wildcard also becomes a column of the table at ingestion, holding what it matched in each file's path: here `sample_id` is `sample_A` for the rows of `star_salmon/sample_A/quant.sf`. A file that already has a column of that name keeps its own. A [composed dashboard](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/#adding-them) relies on this to keep the sample of files that carry it in their path only.

#### Limiting a recursive scan (v1.15.0+)

Two optional `scan_parameters` keep a recursive scan out of directories it does not need:

- `max_depth`: how many directory levels below each run directory to search. `0` keeps the scan to files directly in the run directory, `1` adds its subdirectories, and so on. In the example above, `star_salmon/sample_A/quant.sf` sits at depth 2.
- `ignore`: glob patterns, such as `work` or `*.tmp`. Each is matched against the file or directory name and against its path from the run directory, so `logs/*` works too. A matching directory is not entered at all.

```
scan:
  mode: "recursive"
  scan_parameters:
    regex_config:
      pattern: "star_salmon/.*/quant.sf"
    max_depth: 2
    ignore:
      - "work"
      - "*.tmp"
```

Earlier releases accepted both keys and ignored them. From v1.15.0 the scan applies them, so a project that set them may register fewer files than before, and the CLI prints a warning naming its collections. `--legacy-scan-depth` on `depictio ingest` or `depictio data scan` ignores them again for one release.

Both keys belong to `recursive` scans. The [remote modes](#remote-modes) reject them, and from v1.16.0 they are not carried over when a `recursive` collection is read from an [`s3://` run folder](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#a-run-folder-on-s3) or pointed at another folder with `--bind`: that scan walks everything below its folder.

#### Remote Modes (v1.16.0+)

Three modes fetch data from where it already is, read by the CLI or the server, and the result is materialised like any scanned file. The full parameter tables are in the [reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/#remote-scan-modes), and [Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md) explains when to use which.

An S3 prefix, with the glob matched against the key relative to the prefix and `id_regex` capturing the cross-DC join key:

```
workflows:
  - name: "run42"
    engine:
      name: "python"
    data_location:
      structure: "flat"
      locations:
        - "s3://my-bucket/run42/"
    data_collections:
      - data_collection_tag: "samples"
        config:
          type: "Table"
          metatype: "Aggregate"
          scan:
            mode: s3_prefix
            scan_parameters:
              prefix: "s3://my-bucket/run42/"
              pattern: "*.samples.csv"
              id_regex: "^([^/]+?)\\.samples\\.csv$"
          dc_specific_properties:
            format: "CSV"

# Lists s3://my-bucket/run42/ and keeps keys ending in .samples.csv:
# sample_A.samples.csv  -> depictio_manifest_id = sample_A
# sample_B.samples.csv  -> depictio_manifest_id = sample_B
```

For a single remote file, `mode: url` with `url: "https://host/path/file.csv"` (or an `s3://bucket/key`) replaces the block above.

A manifest-driven project, where each collection consumes the manifest entries of one `type` and the manifest `id` becomes the join key between them:

```
workflows:
  - name: "manifest"
    engine:
      name: "python"
    data_location:
      structure: "flat"
      locations:
        - "https://data.example.org/run42/manifest.json"
    data_collections:
      - data_collection_tag: "samples"
        config:
          type: "Table"
          metatype: "Metadata"
          scan:
            mode: manifest
            scan_parameters:
              manifest_url: "https://data.example.org/run42/manifest.json"
              manifest_type: "samples"
          dc_specific_properties:
            format: "CSV"
      - data_collection_tag: "measurements"
        optional: true      # in a template, dropped when the manifest has no "measurements" rows
        config:
          type: "Table"
          metatype: "Aggregate"
          scan:
            mode: manifest
            scan_parameters:
              manifest_url: "https://data.example.org/run42/manifest.json"
              manifest_type: "measurements"
          dc_specific_properties:
            format: "CSV"

# manifest.json (or .csv) lists one row per file:
#   id,type,url,run
#   S1,samples,https://data.example.org/run42/S1.samples.csv,run42
#   S1,measurements,https://data.example.org/run42/S1.measurements.csv,run42
```

`optional: true` takes effect when the project comes from a template, through `depictio ingest --template … --manifest` or **From Manifest**. Ingested as is, with `--project-config-path`, a manifest with no `measurements` row stops the run with *Manifest has no entries of type 'measurements'*.

### Cross-DC Links (Interactive Filtering)

Links enable **cross-DC filtering** at runtime: filter one data collection and automatically update related visualizations without pre-computed joins.

```
# Project-level links configuration
links:
  - source_dc_tag: string     # Required (or source_dc_id): DC containing the filter
    source_column: string     # Required: Column to filter on
    target_dc_tag: string     # Required (or target_dc_id): DC to receive filtered values
    target_type: string       # Required: "table", "multiqc", "image" or "genomic_tracks"
    link_config:              # Optional
      resolver: string        # Default "direct"; see the table below
      target_field: string    # Optional: Field to match in target DC
      mappings: object        # Optional: {canonical: [variants]} for sample_mapping
      pattern: string         # Optional: must contain {sample}, for pattern
      columns: object         # Required by region: {chrom: ..., pos: ...}
      case_sensitive: boolean # Default: true
    description: string       # Optional
    enabled: boolean          # Default: true
```

`source_dc_id` and `target_dc_id` take a data collection id, the `id` pinned on a collection: a tag written there matches nothing. Name collections by tag with `source_dc_tag` and `target_dc_tag`.

**Resolvers:**

| Resolver         | Use Case                                                                   |
| ---------------- | -------------------------------------------------------------------------- |
| `direct`         | Same value in both DCs                                                     |
| `sample_mapping` | Canonical ID → MultiQC sample variants                                     |
| `pattern`        | Template substitution (e.g., `{sample}.bam`)                               |
| `regex`          | Target values matched by a regex                                           |
| `wildcard`       | Glob matching (e.g., `S1*` matches `S1_R1.bam`)                            |
| `region`         | A genomic region renamed onto the target's chromosome and position columns |

**Example:**

```
name: "My Project"

links:
  - source_dc_tag: sample_metadata
    source_column: sample_id
    target_dc_tag: multiqc_fastqc
    target_type: multiqc
    link_config:
      resolver: sample_mapping

# workflows: ... the workflow declaring sample_metadata and multiqc_fastqc ...
```

For detailed documentation, see [Cross-DC Filtering](https://depictio.github.io/depictio-docs/latest/features/cross-dc-filtering/index.md).

### Data Collection Joins (Client-Side Pre-computed)

Joins vs Links

**Joins** and **Links** serve different purposes:

- **Joins**: Combine Table DCs into a single pre-computed view during `depictio ingest`. The joined dataset is pushed to the server as one unified Delta table. No dynamic joining happens on the server.
- **Links**: Enable runtime cross-DC filtering in the dashboard UI. Data collections remain separate; filtering happens dynamically.

Joins are processed client-side when running `depictio ingest` and create a merged view that gets uploaded to the server. They only work with **Table-type** data collections.

Joins are declared at project level, next to `links`:

```
# Project-level joins configuration
joins:
  - name: string              # Required: letters, digits, _ and -
    left_dc: string           # Required: DC tag, or "workflow.tag" across workflows
    right_dc: string          # Required: another DC tag
    on_columns: [string]      # Required: columns present in both
    how: string               # Default "inner"; "left", "right", "outer"
    workflow_name: string     # Optional: workflow unscoped tags are looked up in
    persist: boolean          # Default: true (write the result as a Delta table)
    description: string       # Optional
    granularity:              # Optional: aggregate the finer table first
      aggregate_to: string    # Required: the aggregation key column
      numeric_default: string # Default "mean" (sum, min, max, first, last, count, median)
      categorical_default: string  # Default "first"
      column_overrides: [{column: string, function: string}]  # Optional
```

The older per-collection `config.join` block (`on_columns`, `how`, `with_dc`) is still accepted but no longer joins anything.

**Example: Joining sample metadata with expression data**

```
name: "Expression with metadata"

workflows:
  - name: "rnaseq"
    engine:
      name: "nextflow"
    data_location:
      structure: "sequencing-runs"
      locations:
        - "{DATA_ROOT}/rnaseq"
      runs_regex: "run_.*"
    data_collections:
      - data_collection_tag: "sample_metadata"
        config:
          type: "table"
          metatype: "metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "{DATA_ROOT}/rnaseq/samplesheet.csv"
          dc_specific_properties:
            format: "csv"

      - data_collection_tag: "expression"
        config:
          type: "table"
          metatype: "aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: "counts/.*\\.tsv"
          dc_specific_properties:
            format: "tsv"

joins:
  - name: "expression_with_metadata"
    left_dc: "expression"
    right_dc: "sample_metadata"
    on_columns: ["sample_id"]
    how: "left"
```

When you run `depictio ingest`, the CLI will:

1. Load both data collections locally
1. Perform the join operation on the client
1. Push the resulting joined table to the server, as a data collection of its own

**When to use Joins vs Links:**

| Use Case                                     | Recommended                             |
| -------------------------------------------- | --------------------------------------- |
| Need a single combined dataset for analysis  | **Joins**                               |
| Want to filter one DC based on another in UI | **Links**                               |
| Working with MultiQC data                    | **Links** (joins don't support MultiQC) |
| Need to reduce server-side data duplication  | **Joins**                               |
| Want dynamic, runtime filtering              | **Links**                               |

## Configuration Patterns Library

### Pattern 1: Multi-sample RNA-seq Study

```
name: "RNA-seq Expression Analysis"
is_public: false

# Cross-DC Links for interactive filtering
links:
  - source_dc_tag: qc_summary           # Filter from QC data
    source_column: Sample               # Column to filter on
    target_dc_tag: salmon_gene_tpm      # Target expression data
    target_type: table                  # Target type
    link_config:
      resolver: direct                  # Same sample IDs in both DCs

workflows:
  - name: "nextflow-custom-rnaseq"
    engine:
      name: "nextflow"
      version: "24.10.3"
    version: "3.18.0"

    data_location:
      structure: "sequencing-runs"
      locations:
        - "{DATA_ROOT}/rnaseq_studies/cohort_2024"
      runs_regex: "batch_[A-C]"

    data_collections:
      # Quality control metrics
      - data_collection_tag: "qc_summary"
        description: "Aggregated quality control summary across samples"
        config:
          type: "table"
          metatype: "metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "qc_reports/multiqc_general_stats.txt"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              separator: "\t"
              has_header: true
            keep_columns:
              - "Sample"
              - "fastqc-total_sequences"
              - "fastqc-percent_duplicates"
              - "fastqc-percent_gc"
              - "fastqc-avg_sequence_length"
              - "fastqc-percent_fails"
            columns_description:
              "Sample": "Sample identifier"
              "fastqc-total_sequences": "Total number of sequences processed by FastQC"
              "fastqc-percent_duplicates": "Percentage of duplicate sequences"
              "fastqc-percent_gc": "Overall GC content percentage"
              "fastqc-avg_sequence_length": "Average read length"
              "fastqc-percent_fails": "Percentage of FastQC modules that failed"

      # Gene expression quantification
      - data_collection_tag: "salmon_gene_tpm"
        description: "Salmon merged gene-level TPM expression matrix"
        config:
          type: "table"
          metatype: "metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "salmon/salmon.gene_tpm.melted.tsv"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              separator: "\t"
              has_header: true
            columns_description:
              sample_id: "Sample identifier"
              gene_id: "Gene identifier"
              gene_name: "Gene symbol/name"
              condition: "Experimental condition (e.g., treatment, control)"
              replicate: "Biological replicate identifier"
              tpm: "Transcripts per million (TPM) expression value"
        # Note: Use project-level links (above) for interactive filtering
```

### Pattern 2: Multi-sample Strand-seq (single-cell) Study

```
name: "Strand-Seq data analysis"
data_management_platform_project_url: "https://labid.embl.org/core/projects/default/5baa8f07-bd00-46e7-b3cb-ec79d01f6f3c"

# Cross-DC Links for interactive filtering
links:
  - source_dc_tag: mosaicatcher_samples_metadata
    source_column: sample
    target_dc_tag: mosaicatcher_stats
    target_type: table
    link_config:
      resolver: direct
  - source_dc_tag: mosaicatcher_samples_metadata
    source_column: sample
    target_dc_tag: ashleys_labels
    target_type: table
    link_config:
      resolver: direct
  - source_dc_tag: mosaicatcher_samples_metadata
    source_column: sample
    target_dc_tag: sv_calls
    target_type: table
    link_config:
      resolver: direct

workflows:
  - name: "mosaicatcher-pipeline"
    engine:
      name: "snakemake"
    version: "2.3.5"
    catalog:
      name: "smk-wf-catalog"
      url: "https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/friendsofstrandseq/mosaicatcher-pipeline.html"
    repository_url: "https://github.com/friendsofstrandseq/mosaicatcher-pipeline"
    workflow_tag: "snakemake/mosaicatcher-pipeline"

    data_location:
      structure: "sequencing-runs"
      locations:
        - "/Data/mosaicatcher-pipeline-results/"
      runs_regex: ".*"

    data_collections:
      # MosaiCatcher statistics per cell
      - data_collection_tag: "mosaicatcher_stats"
        description: "Statistics file generated by MosaiCatcher"
        config:
          type: "table"
          metatype: "aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: ".*\\.info_raw"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              skip_rows: 13
              separator: "\t"
              has_header: true
            keep_columns:
              - "sample"
              - "cell"
              - "mapped"
              - "dupl"
              - "pass1"
              - "good"
            columns_description:
              sample: "Sample ID"
              cell: "Cell ID"
              mapped: "Total number of reads seen"
              dupl: "Reads filtered out as PCR duplicates"
              pass1: "Coverage compliant cells (binary)"
              good: "Reads used for counting"

      # Ashleys QC labels
      - data_collection_tag: "ashleys_labels"
        description: "Probabilities generated by ashleys-qc model"
        config:
          type: "table"
          metatype: "aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: ".*cell_selection/labels\\.tsv"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              separator: "\t"
              has_header: true
        # Note: Use project-level links (above) for interactive filtering

      # Structural variant calls
      - data_collection_tag: "sv_calls"
        description: "SV calls generated by MosaiCatcher (stringent)"
        config:
          type: "table"
          metatype: "aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: "stringent_filterTRUE\\.tsv"
          dc_specific_properties:
            format: "tsv"
            polars_kwargs:
              separator: "\t"
              has_header: true
            columns_description:
              sample: "Sample identifier"
              cell: "Single cell identifier"
              chrom: "Chromosome name"
              start: "SV start position"
              end: "SV end position"
              sv_call_name: "Structural variant call identifier"
        # Note: Use project-level links (above) for interactive filtering

      # Sample metadata
      - data_collection_tag: "mosaicatcher_samples_metadata"
        description: "Metadata file for MosaiCatcher samples"
        config:
          type: "table"
          metatype: "metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "/Data/mosaicatcher-pipeline-results/metadata/mosaicatcher_samples_metadata_2024.xlsx"
          dc_specific_properties:
            format: "xlsx"
            polars_kwargs:
              has_header: true
            columns_description:
              sample: "Sample identifier"
              patient_id: "Patient identifier"
              tissue_type: "Type of tissue analyzed"
              collection_date: "Date of sample collection"
        # Note: Use project-level links (above) for interactive filtering
```

### Pattern 3: MultiQC Quality Control Integration (v0.5.0+)

```
name: "MultiQC Quality Control Analysis"

# Cross-DC Links for interactive filtering
links:
  - source_dc_tag: sample_metadata      # Filter from metadata table
    source_column: sample               # Column to filter on
    target_dc_tag: multiqc_data         # Target MultiQC visualizations
    target_type: multiqc                # Target type
    link_config:
      resolver: sample_mapping          # Maps canonical IDs to MultiQC sample variants

workflows:
  - name: "qc-pipeline"
    engine:
      name: "python"
    data_location:
      structure: "sequencing-runs"
      runs_regex: "run_.*"
      locations:
        - "{DATA_ROOT}/qc_results"

    data_collections:
      # MultiQC data collection - automatically detected
      - data_collection_tag: "multiqc_data"
        description: "MultiQC quality control report data"
        config:
          type: "MultiQC"
          # NOTE: No scan, metatype, or dc_specific_properties needed
          # MultiQC automatically detects multiqc_data/multiqc.parquet in each run
          # Requires MultiQC 1.29+ to generate parquet format

      # Sample metadata for context
      - data_collection_tag: "sample_metadata"
        description: "Sample metadata table for MultiQC integration"
        config:
          type: "Table"
          metatype: "Metadata"
          scan:
            mode: "single"
            scan_parameters:
              filename: "metadata/sample_info.csv"
          dc_specific_properties:
            format: "CSV"
            polars_kwargs:
              separator: ","
              has_header: true
            columns_description:
              "sample": "Sample identifier matching MultiQC sample names"
              "treatment": "Treatment condition applied to the sample"
              "batch": "Batch identifier for experimental runs"
          # Note: Use project-level links (above) for interactive filtering
          # instead of join configuration

      # Additional per-sample QC metrics
      - data_collection_tag: "sample_qc_metrics"
        description: "Per-sample quality control metrics and statistics"
        config:
          type: "Table"
          metatype: "Aggregate"
          scan:
            mode: "recursive"
            scan_parameters:
              regex_config:
                pattern: "qc_metrics/.*\\.csv"
          dc_specific_properties:
            format: "CSV"
            polars_kwargs:
              separator: ","
              has_header: true
            columns_description:
              "sample": "Sample identifier"
              "total_reads": "Total number of reads"
              "mapped_reads": "Number of successfully mapped reads"
              "mapping_rate": "Percentage of reads mapped to reference"
          # Note: Use project-level links (above) for interactive filtering
```

**Key Points for MultiQC Integration:**

- **Automatic Detection**: MultiQC data is automatically detected from `multiqc_data/multiqc.parquet` in each run
- **Minimal Configuration**: Only requires `type: "MultiQC"` - no scan parameters needed
- **Format Requirement**: Requires MultiQC 1.29+ to generate parquet output format
- **Cross-DC Filtering**: Use project-level **links** with `sample_mapping` resolver to connect metadata tables with MultiQC visualizations
- **Location**: Each run must contain a `multiqc_data/multiqc.parquet` file generated by MultiQC

## 🔍 Validation

### CLI Validation Commands

```
# Validate configuration file syntax and structure
depictio -v config check --project-config-path ./my_project.yaml

# Check server connectivity and S3 storage
depictio config check

# Dry-run mode: validate without processing data
depictio -v ingest --project-config-path ./my_project.yaml --dry-run

# Test file discovery patterns
depictio -vv data scan --project-config-path ./my_project.yaml
```

<!--

### Common Configuration Errors

#### Environment Variables Not Resolved

**Error:**

```
ValueError: Environment variable 'DATA_ROOT' is not set for path '{DATA_ROOT}/study1'
```

**Solution:**

```
# Set required environment variables
export DATA_ROOT="/mnt/storage/projects"
export PROJECT_NAME="my_study"

# Verify variables are set
echo $DATA_ROOT
echo $PROJECT_NAME

# Alternative: use absolute paths
data_location:
  locations:
    - "/mnt/storage/projects/my_study"  # Direct path instead of {DATA_ROOT}/my_study
```

#### Invalid Regex Patterns

**Error:**

```
ValueError: Invalid regex pattern: "*.tsv"
```

**Solution:**

```
# Incorrect: shell glob pattern
pattern: "*.tsv"

# Correct: regex pattern
pattern: ".*\\.tsv"

# More specific: files ending with _stats.tsv
pattern: ".*_stats\\.tsv"

# Directory-specific: stats files in any subdirectory
pattern: "stats/.*\\.tsv"
```

#### File Discovery Issues

**Error:** No files found during scanning

**Debug steps:**

```
# Check if paths exist
ls -la "{DATA_ROOT}/study1"

# Test regex pattern manually
find /data/study1 -type f -name "*.tsv" | grep -E "stats/.*\.tsv"

# Use verbose logging to see search process
depictio-cli --verbose --verbose-level DEBUG data scan --project-config-path config.yaml
```

#### Join Configuration Errors

**Error:**

```
ValueError: Column 'sample_id' not found in dataset 'expression_data'
```

**Solution:**

```
# Check column names match exactly (case-sensitive)
join:
  on_columns: ["sample_id"]  # Must exist in both datasets

# Alternative: inspect data first
keep_columns:
  - "Sample_ID"  # Note: different capitalization
  - "expression"

# Update join to use correct column name
join:
  on_columns: ["Sample_ID"]  # Match actual column name
```

#### Performance Issues

**Symptoms:**

- Slow file scanning
- Memory usage during processing
- Dashboard loading delays

**Optimizations:**

```
# 1. Use column filtering
dc_specific_properties:
  keep_columns:
    - "sample_id"
    - "gene_name"
    - "expression"
    # Don't load unnecessary columns

# 2. Limit file search depth
scan_parameters:
  regex_config:
    pattern: "results/.*\\.tsv"
  max_depth: 3  # Don't search too deep
  ignore:
    - "backup"   # Skip backup directories
    - "*.tmp"    # Skip temporary files

# 3. Use efficient file formats
format: "parquet"  # Much faster than CSV for large data

# 4. Optimize regex patterns
pattern: "^stats/sample_.*\\.tsv$"  # Anchored patterns are faster
# Instead of: "stats/.*sample.*tsv"  # Unanchored, slower
```

## 🔄 Migration & Compatibility

### Configuration Version Migration

```
# Legacy configuration (pre v0.3.0)
workflows:
  - name: "old_pipeline"
    engine: "nextflow"  # String format (deprecated)
    parent_runs_location:  # Old field name
      - "/data/runs"
    runs_regex: ".*"

# Current configuration (v0.3.0+)
workflows:
  - name: "new_pipeline"
    engine:  # Object format (current)
      name: "nextflow"
      version: "24.10.3"
    data_location:  # New field name
      structure: "sequencing-runs"
      locations:
        - "/data/runs"
      runs_regex: ".*"
```

### Deprecated Fields

| Deprecated Field | Replacement | Migration |
| --- | --- | --- |
| `parent_runs_location` | `data_location.locations` | Move array to nested structure |
| `engine: "string"` | `engine: {name: "string"}` | Convert to object format |
| `mode: "aggregate"` | `metatype: "aggregate"` | Rename field |

### Backward Compatibility

Current Depictio versions support legacy configurations with warnings. Update configurations using:

```
# Generate updated configuration
depictio-cli config migrate --input legacy_config.yaml --output new_config.yaml

# Validate migrated configuration
depictio-cli config validate-project-config --project-config-path new_config.yaml
``` -->

### Pattern: Template project with recipe-transformed data collections { #pattern-template-project }

Templates are pre-packaged project configurations for specific bioinformatics pipelines. You don't write the YAML manually: you point the CLI at your data directory and a template ID. This pattern shows what the template YAML looks like internally and how to invoke it.

**1. Minimal `template:` metadata block (top of a template YAML)**

```yaml
template:
  template_id: "nf-core/ampliseq/2.16.0"
  description: "nf-core/ampliseq microbial community analysis template"
  version: "1.0.0"
  variables:
    - name: "DATA_ROOT"
      description: "Root directory containing ampliseq pipeline output data"
      required: true
  dashboards:
    - "dashboards/base.yaml"
```

**2. Recipe-transformed data collection (`source: "transformed"`)**

```
data_collections:
  - data_collection_tag: "taxonomy_rel_abundance"
    description: "Taxonomic relative abundance at Phylum level"
    config:
      type: "Table"
      source: "transformed"          # ← marks this DC as recipe-produced
      transform:
        recipe: "nf-core/ampliseq/taxonomy_rel_abundance.py"
        # Optional: override a source file path (path or glob_pattern)
        # source_overrides:
        #   rel_table:
        #     path: "custom/path/to/rel-table-2.tsv"
        # Optional (v1.21.0+): "run", "aggregate" or "pipeline"
        # scope: "run"
      dc_specific_properties:
        format: "TSV"
        columns_description:
          "sample": "Sample identifier"
          "taxonomy": "Taxonomic classification (Kingdom;Phylum)"
          "rel_abundance": "Relative abundance (0-1)"
```

**3. Cross-DC source via `dc_ref` (in a recipe's SOURCES)**

Some recipes reference another data collection instead of a file. The `dc_ref` field names the source DC's `data_collection_tag`:

```
# In the recipe Python file (e.g. taxonomy_rel_abundance.py):
SOURCES = [
    RecipeSource(
        ref="rel_table",
        path="qiime2/rel_abundance_tables/rel-table-2.tsv",
        format="TSV",
        read_kwargs={"skip_rows": 1},
    ),
    RecipeSource(
        ref="metadata",
        dc_ref="metadata",  # ← loaded from the "metadata" DC
        optional=True,      # absent when no METADATA_FILE was given
    ),
]
```

The `dc_ref` source is resolved automatically during `depictio ingest`: no additional YAML is needed in the project config.

**4. Running the template**

```
# Minimal: the results directory and a template ID
depictio ingest /data/my_ampliseq_run \
  --template nf-core/ampliseq/2.16.0

# Skip auto-import (import dashboards manually later)
depictio ingest /data/my_ampliseq_run \
  --template nf-core/ampliseq/2.16.0 \
  --skip dashboards
```

For full template reference, see [Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md). For recipe documentation, see [Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md).

______________________________________________________________________

## 📖 Additional Resources

- **[Projects Guide](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md)** - Comprehensive project management guide
- **[Configuration Reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md)** - Complete YAML reference documentation
- **[CLI Reference](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md)** - Complete CLI command documentation
- **[Templates](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md)** - Pre-packaged project configurations
- **[Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md)** - URL, S3 prefix and manifest scan modes
- **[Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md)** - Data transformation recipes
- **[Dashboard Creation](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard_creation/index.md)** - Building interactive dashboards
- **[API Documentation](https://depictio.github.io/depictio-docs/latest/api/reference/index.md)** - Programmatic project management
- **[Pydantic Models](https://github.com/depictio/depictio/tree/main/depictio/models/models)** - Schema definitions and validation

______________________________________________________________________

*This reference covers all configuration options available in Depictio. Start with the Quick Start examples and gradually add complexity as needed for your specific use case.*
