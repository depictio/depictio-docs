# <span style="color: #45B8AC;">:material-folder-multiple:</span> YAML Project configuration breakdown

<!-- markdownlint-disable MD046 -->
!!! tip "Configuration Validation"
    **Always validate your YAML configuration before using:**
    ```bash
    # Validate configuration syntax and structure
    depictio-cli config validate-project-config \
      --project-config-path ./my_project.yaml --verbose
    ```

    **For YAML syntax highlighting in VS Code:** Install the YAML extension and save files with `.yaml` or `.yml` extension.

!!! warning "Configuration Template Warning"
    **Do not copy-paste entire configurations blindly.** This reference shows all available options with their defaults and descriptions. Only specify values that differ from defaults or are required for your specific use case.
<!-- markdownlint-enable MD046 -->

This guide provides comprehensive YAML configuration examples for Depictio projects, from simple setups to complex bioinformatics workflows. For a complete reference of all options, see the [Configuration Reference](reference.md).

## <span style="color: #45B8AC;">:material-rocket-launch:</span> Quick Start Examples

Choose your starting point based on your project complexity:

=== "**Basic** Project (Minimal)"

    Perfect for direct file upload and analysis:

    ```yaml
    name: "My Analysis Project"
    project_type: "basic"
    
    # Files will be uploaded through the web interface
    # No additional configuration needed!
    ```

=== "**Basic** Project (CLI)"

    For CLI-based basic projects with direct files:

    ```yaml
    name: "CSV Analysis Project"  
    project_type: "basic"
    is_public: false
    
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

=== "Advanced Project (Minimal)"

    For workflow-generated data with pattern matching:

    ```yaml
    name: "RNA-seq Analysis"
    project_type: "advanced"
    
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

## <span style="color: #45B8AC;">:material-file-document:</span> Configuration Schema

### Project-Level Configuration

All projects share these top-level configuration options:

```yaml linenums="1"
# === REQUIRED FIELDS ===

# Project identification
name: string                              # Required: Human-readable project name
                                          # Must be non-empty string
                                          # Example: "Multi-omics Cancer Study"


# Advanced projects only: Workflow definitions  
workflows: [Workflow]                     # Default: [] (empty for basic projects)
                                          # Array of workflow configurations
                                          # See "Workflow Configuration" section

# === REQUIRED FIELDS WITH DEFAULT VALUES ===

# Project type determines the configuration structure
project_type: "basic" | "advanced"        # Default: "basic"
                                          # Options:
                                          # - basic: Direct file upload/processing
                                          # - advanced: Workflow-integrated projects

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
```

### Project Types Deep Dive

#### Basic Projects

Designed to be minimal and easy to set up, WebUI compatible, and suitable for small-scale analyses.

**Use cases:**

- Direct CSV/Excel file analysis
- Ad-hoc data exploration  
- Small-scale studies (< 100 files)
- Quick prototyping and visualization

**Configuration:**

- Minimal setup required
- Data uploaded via web interface or defined in `data_collections`
- No workflow integration needed (default workflow is created under the hood for system compatibility)

#### Advanced Projects  

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

## <span style="color: #45B8AC;">:material-cog:</span> Workflow Configuration (Advanced)

Advanced projects use workflows to describe data organization patterns. Each workflow corresponds to a computational pipeline that generates structured data.

```yaml linenums="1"
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
                                          # Examples: 
                                          #   - "/absolute/path/to/data"
                                          #   - "{DATA_ROOT}/project1"
                                          #   - "{HOME}/workflows/results"
      
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

    catalog:                              # Optional: Workflow registry information
      name: string | null                 # Options: "nf-core", "smk-wf-catalog", "workflowhub"
      url: string | null                  # Catalog URL
                                          # Example: "https://nf-co.re/rnaseq"
    
    repository_url: string | null         # Optional: Source code repository
                                          # Example: "https://github.com/user/workflow"
    
    workflow_tag: string | null           # Optional: Auto-generated workflow identifier
                                          # Format: "engine/name" or "catalog/name"
                                          # Usually auto-populated, rarely set manually
    
    config:                               # Optional: Workflow-specific configuration
      version: string | null              # Workflow configuration version
      workflow_parameters: object | null # Workflow-specific parameters
```

### Workflow Data Location Patterns

#### Flat Structure

```yaml
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

```yaml
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

```yaml
# Environment setup
# export DATA_ROOT="/mnt/storage/projects"  
# export PROJECT_NAME="cancer_study"
# export BACKUP_LOCATION="/backup/data"

data_location:
  locations:
    - "{DATA_ROOT}/{PROJECT_NAME}/results"     # Expands to: /mnt/storage/projects/cancer_study/results
    - "{BACKUP_LOCATION}/{PROJECT_NAME}"       # Expands to: /backup/data/cancer_study
```

**Common Environment Variables:**

- `DATA_ROOT`, `DATA_LOCATION` - Primary data storage
- `PROJECT_ROOT` - Project base directory  
- `HOME`, `USER` - User-specific paths
- `SCRATCH_DIR`, `TEMP_DIR` - Temporary storage locations

## <span style="color: #45B8AC;">:material-database:</span> Data Collections Configuration

Data collections define how to discover, process, and structure your data files. They are the core building blocks that connect file system data to Depictio <span style="color: #F68B33;">:material-view-dashboard:</span> dashboards.

```yaml
data_collections:
  - # === REQUIRED FIELDS ===
    
    data_collection_tag: string    # Required: Unique identifier within project
                                  # Must be unique across all data collections
                                  # Used for referencing in joins and dashboards
                                  # Example: "gene_counts", "quality_metrics"
    
    config:                     # Required: Data collection configuration
      type: string                # Required: Data collection type
                                  # Options (only table for now):
                                  #  - "table": Tabular data (CSV, TSV, Excel, Parquet, Feather)
      
      metatype: string | null    # Required for table type
                                  # Required: Data collection metatype
                                  # Options:
                                  # - "metadata": Single annotation/metadata file per project
                                  # - "aggregate": Multiple files combined into unified dataset
      
      scan:                     # Required: File discovery configuration
        mode: string              # Required: Scanning strategy
                                  # Options:
                                  # - "single": Single file per project/run
                                  # - "recursive": Pattern-based file discovery

        scan_parameters:        # Required: Mode-specific parameters
          # For mode: "single"
          filename: string      # Required: Relative or absolute file path
                               # Example: "metadata/sample_info.csv"
          
          # For mode: "recursive"  
          regex_config:         # Required: Pattern matching configuration
            pattern: string    # Required: Regex pattern for file discovery
                              # Example: "stats/.*_stats\\.tsv"
            wildcards: [...]   # Optional: Named capture groups for metadata extraction
          max_depth: int | null # Optional: Maximum directory depth to search
          ignore: [string] | null  # Optional: Patterns to exclude from search
      
      dc_specific_properties:   # Required: Type-specific configuration
        # See "Table Configuration" section for details
    
    # === OPTIONAL FIELDS ===
    
    description: string | null  # Optional: Human-readable description
                               # Example: "Per-sample quality control metrics"
```

### Specific Data Collection Types

!!! note "Data Collection Types"
    Data collections can be of different types, each with its own configuration requirements. Currently, only the "table" type is supported, which handles structured tabular data. Future versions may introduce additional types for other data formats (e.g., Omics data, Images, GeoJSON).  

#### **Table** Data Collection Configuration

Table data collections handle structured tabular data (CSV, TSV, Excel, Parquet, Feather):

```yaml
dc_specific_properties:
  # === REQUIRED FIELDS ===
  
  format: string               # Required: File format
                              # Values: "csv", "tsv", "xlsx", "xls", "parquet", "feather"
                              # Case-insensitive, normalized to lowercase
  
  polars_kwargs: object       # Required: Polars DataFrame configuration
                             # Polars-specific parameters for data reading
                             # See "Polars Configuration" section
  
  # === OPTIONAL FIELDS ===
  
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

### Polars Configuration Options

Polars is Depictio's high-performance data processing engine. Configure data reading with these options:

```yaml
polars_kwargs:
  # === COMMON OPTIONS ===
  
  # CSV/TSV specific
  separator: string           # Column separator character
                             # Default: "," for CSV, "\t" for TSV
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
  column_types: object      # Explicit column type mapping
                           # Forces specific data types
                           # Example:
                           #   sample_id: "String"
                           #   count: "Int64"  
                           #   p_value: "Float64"
                           #   significant: "Boolean"
  
  column_names: [string]    # Override column names
                           # Useful when has_header: false
                           # Example: ["sample", "gene", "expression"]
  
  # Missing data handling
  null_values: [string]     # Values to treat as null/missing
                           # Default: ["", "NULL", "null", "None"]
                           # Example: ["NA", "N/A", "", "null", "-"]
  
  # Performance options
  n_rows: int               # Limit number of rows to read
                           # Useful for testing configurations
                           # Example: 1000 (read only first 1000 rows)
  
  # Encoding
  encoding: string          # File encoding  
                           # Default: "utf8"
                           # Example: "utf8", "latin1", "ascii"
  
  # Excel specific (for .xlsx, .xls files)
  sheet_name: string        # Excel sheet name to read
                           # Default: first sheet
                           # Example: "Results", "Sheet1"
  
  sheet_id: int            # Excel sheet index (0-based)
                          # Alternative to sheet_name
                          # Example: 0 (first sheet), 1 (second sheet)
```

### File Scanning Patterns

#### Single File Mode

Best for metadata files or summary statistics generated once per project:

```yaml
scan:
  mode: "single"
  scan_parameters:
    filename: "multiqc_data/multiqc_general_stats.txt"
    
# Finds exactly one file:
# project_root/multiqc_data/multiqc_general_stats.txt
```

#### Recursive Mode

Uses regex patterns to discover files across directory structures:

```yaml  
scan:
  mode: "recursive"
  scan_parameters:
    regex_config:
      pattern: "star_salmon/.*/quant.sf"
      # Wildcards for metadata extraction (optional)
      wildcards:
        - name: "sample_id"
          wildcard_regex: "star_salmon/([^/]+)/quant.sf"
    max_depth: 5        # Optional: limit search depth

# Matches files like:
# run_001/star_salmon/sample_A/quant.sf
# run_001/star_salmon/sample_B/quant.sf  
# run_002/star_salmon/sample_C/quant.sf
```

### Data Collection Joins

When you use a production-oriented workflow, it can be tricky to modify workflow structure itself and rely instead of post-processing steps to reformat data into a unified structure. Depictio supports joining multiple data collections to create unified datasets.

!!! note "Note about join configuration"
    A join need to be defined once and does not need to be repeated for each data collection. For instance, if DC1 & DC2 are joined, the join configuration needs to be defined in either DC1 or DC2, not both.

This can be achieved by defining join configurations:

```yaml
# In one data collection configuration
join:
  on_columns: [string]        # Required: Column names for joining
                             # Must exist in both datasets
                             # Example: ["sample_id"], ["sample_id", "timepoint"]
  
  how: string                # Required: Join type
                            # "inner": Keep only rows with matches in both datasets
                            # "outer": Keep all rows, fill missing with null
                            # "left": Keep all rows from left dataset  
                            # "right": Keep all rows from right dataset
  
  with_dc: [string]         # Required: Target data collections to join with
                           # References to other data_collection_tag values
                           # Example: ["metadata", "quality_stats"]

# Example: Join expression data with sample metadata
data_collections:
  - data_collection_tag: "sample_metadata"
    # ... metadata configuration ...
    
  - data_collection_tag: "gene_expression"
    # ... expression configuration ...
    join:
      on_columns: ["sample_id"]
      how: "inner"  
      with_dc: ["sample_metadata"]
```

!!! warnning "Join Limitations"
    Joins are currently limited to simple column-based joins. Future versions may support more complex joins and transformations.

## <span style="color: #45B8AC;">:material-library:</span> Configuration Patterns Library

### Pattern 1: Multi-sample RNA-seq Study

```yaml
name: "RNA-seq Expression Analysis"
project_type: "advanced"
is_public: false

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
        join:
          on_columns: ["sample_id"]
          how: "inner"
          with_dc: ["qc_summary"]
```

### Pattern 2: Multi-sample Strand-seq (single-cell) Study

```yaml
name: "Strand-Seq data analysis"
project_type: "advanced"
data_management_platform_project_url: "https://labid.embl.org/core/projects/default/5baa8f07-bd00-46e7-b3cb-ec79d01f6f3c"

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
        join:
          on_columns: ["sample", "cell"]
          how: "inner"
          with_dc: ["mosaicatcher_stats"]
      
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
        join:
          on_columns: ["sample", "cell"]
          how: "inner"
          with_dc: ["ashleys_labels", "mosaicatcher_stats"]
      
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
        join:
          on_columns: ["sample"]
          how: "inner"
          with_dc: ["ashleys_labels", "mosaicatcher_stats", "sv_calls"]
```

## 🔍 Validation

### CLI Validation Commands

```bash
# Validate configuration file syntax and structure
depictio-cli config validate-project-config \
  --project-config-path ./my_project.yaml \
  --verbose

# Check server connectivity and permissions
depictio-cli config check-server-accessibility

# Dry-run mode: validate without processing data
depictio-cli run --project-config-path ./my_project.yaml \
  --dry-run --verbose

# Test file discovery patterns
depictio-cli data scan --project-config-path ./my_project.yaml \
  --verbose --verbose-level DEBUG
```
<!-- 
### Common Configuration Errors

#### Environment Variables Not Resolved

**Error:**

```log
ValueError: Environment variable 'DATA_ROOT' is not set for path '{DATA_ROOT}/study1'
```

**Solution:**

```bash
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

```log
ValueError: Invalid regex pattern: "*.tsv"
```

**Solution:**

```yaml
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

```bash
# Check if paths exist
ls -la "{DATA_ROOT}/study1"

# Test regex pattern manually
find /data/study1 -type f -name "*.tsv" | grep -E "stats/.*\.tsv"

# Use verbose logging to see search process
depictio-cli --verbose --verbose-level DEBUG data scan --project-config-path config.yaml
  
```

#### Join Configuration Errors

**Error:**

```log
ValueError: Column 'sample_id' not found in dataset 'expression_data'
```

**Solution:**

```yaml
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

```yaml
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
    - "backup/.*"   # Skip backup directories
    - ".*\\.tmp"    # Skip temporary files

# 3. Use efficient file formats
format: "parquet"  # Much faster than CSV for large data

# 4. Optimize regex patterns
pattern: "^stats/sample_.*\\.tsv$"  # Anchored patterns are faster
# Instead of: "stats/.*sample.*tsv"  # Unanchored, slower
```

## 🔄 Migration & Compatibility

### Configuration Version Migration

```yaml
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
|------------------|-------------|-----------|
| `parent_runs_location` | `data_location.locations` | Move array to nested structure |
| `engine: "string"` | `engine: {name: "string"}` | Convert to object format |
| `mode: "aggregate"` | `metatype: "aggregate"` | Rename field |

### Backward Compatibility

Current Depictio versions support legacy configurations with warnings. Update configurations using:

```bash
# Generate updated configuration
depictio-cli config migrate --input legacy_config.yaml --output new_config.yaml

# Validate migrated configuration
depictio-cli config validate-project-config --project-config-path new_config.yaml
``` -->

## 📖 Additional Resources

- **[Projects Guide](guide.md)** - Comprehensive project management guide
- **[Configuration Reference](reference.md)** - Complete YAML reference documentation
- **[CLI Reference](../../depictio-cli/usage.md)** - Complete CLI command documentation  
- **[Dashboard Creation](../guides/dashboard_creation.md)** - Building interactive dashboards
- **[API Documentation](../../api/reference.md)** - Programmatic project management
- **[Pydantic Models](https://github.com/depictio/depictio/tree/main/depictio/models/models)** - Schema definitions and validation

---

*This reference covers all configuration options available in Depictio. Start with the Quick Start examples and gradually add complexity as needed for your specific use case.*
