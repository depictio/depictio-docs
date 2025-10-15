# <span style="color: #45B8AC;">:material-folder-multiple:</span> YAML Configuration Reference

<!-- markdownlint-disable MD046 -->

!!! warning "Full Configuration Template Warning"
    **Do not copy-paste this entire configuration blindly.** This reference shows all available options with their defaults and descriptions. Only specify values that differ from defaults or are required for your specific use case.

<!-- markdownlint-enable MD046 -->

This is a complete reference of all configuration options available in Depictio YAML files. For getting started and examples, see the [YAML Examples Guide](yaml-examples.md).

```yaml
# =============================================================================
# DEPICTIO PROJECT CONFIGURATION REFERENCE
# =============================================================================

# Required: Project identification
name:
  "My Project Name" # Required: Human-readable project name
  # Must be non-empty string
  # Example: "Multi-omics Cancer Study"

# Required: Project type determines configuration structure
project_type:
  "basic" # Required: Options are "basic" or "advanced" (default: "basic")
  # basic: Direct file upload/processing
  # advanced: Workflow-integrated projects

# Optional: Project visibility settings
is_public:
  false # Optional: Project visibility (default: false)
  # true: Visible to all users (read-only)
  # false: Restricted to project members

# Optional: CLI integration path
yaml_config_path:
  null # Optional: Path to this YAML file (default: null)
  # Auto-populated by CLI, rarely set manually

# Optional: External project management integration
data_management_platform_project_url:
  null # Optional: URL to external project system (default: null)
  # Must start with http:// or https://
  # Example: "https://labid.embl.org/projects/123"

# =============================================================================
# WORKFLOWS (Required for Advanced Projects)
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
      "nextflow/rnaseq_pipeline" # Optional: Auto-generated workflow identifier
      # Format: "engine/name" or "catalog/name"

    # Optional: Workflow registry information
    catalog:
      name:
        "nf-core" # Optional: Catalog name
        # Options: "nf-core", "smk-wf-catalog", "workflowhub"
      url:
        "https://nf-co.re/rnaseq" # Optional: Catalog URL
        # Example: "https://nf-co.re/rnaseq"

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

      runs_regex:
        "batch_[A-C]" # Required for "sequencing-runs" structure
        # Optional for "flat" structure
        # Regex pattern to identify individual runs
        # Example: "run_\\d+", "sample_.*", "batch[A-Z]"

    # Required: Data collections for this workflow
    data_collections:
      - # Required: Unique identifier for this data collection
        data_collection_tag:
          "gene_expression" # Required: Unique within project
          # Used for referencing in joins and dashboards
          # Example: "gene_counts", "quality_metrics"

        # Optional: Human-readable description
        description:
          "Per-sample gene expression quantification" # Optional: Description of the data collection
          # Used in UI tooltips and documentation

        # Required: Data collection configuration
        config:
          # Required: Type of data collection
          type:
            "table" # Required: Data collection type
            # Options (only table for now):
            #   "table" - Tabular data (CSV, TSV, Excel, Parquet, Feather)

          # Required: Data aggregation strategy
          metatype:
            "aggregate" # Required: Data collection metatype
            # Options:
            #   "metadata" - Single annotation/metadata file per project
            #   "aggregate" - Multiple files combined into unified dataset

          # Required: File discovery configuration
          scan:
            # Required: File scanning strategy
            mode:
              "recursive" # Required: Scanning strategy
              # Options:
              #   "single" - Single file per project/run
              #   "recursive" - Pattern-based file discovery

            # Required: Mode-specific scan parameters
            scan_parameters:
              # For mode: "recursive" - specify search pattern
              regex_config: # Required for recursive mode: Pattern matching configuration
                pattern:
                  "salmon/.*/quant.sf" # Required: Regex pattern for file discovery
                  # Example: "stats/.*_stats\\.tsv"
                wildcards: # Optional: Named capture groups for metadata extraction
                  - name: "sample_id" # Wildcard name for metadata extraction
                    wildcard_regex: "salmon/([^/]+)/quant.sf" # Regex with capture group

              # For mode: "single" - specify exact file (alternative to regex_config)
              # filename: "metadata/sample_info.csv"  # Required for single mode: File path
              # Can be absolute or relative path

          # Required: Type-specific configuration
          dc_specific_properties:
            # Required: File format specification
            format:
              "tsv" # Required: File format
              # Values: "csv", "tsv", "xlsx", "xls", "parquet", "feather"
              # Case-insensitive, normalized to lowercase

            # Required: Data reading configuration using Polars
            polars_kwargs:
              # Common options
              separator:
                "\t" # Required for CSV/TSV: Column separator character
                # Default: "," for CSV, "\t" for TSV
                # Example: ",", "\t", "|", ";"
              has_header:
                true # Required: First row contains column names
                # true: First row is headers, false: First row is data
              skip_rows:
                0 # Optional: Number of rows to skip at file beginning (default: 0)
                # Useful for files with metadata headers

              # Advanced options
              column_types: # Optional: Explicit column type mapping
                Name: "String" # Forces specific data types
                Length: "Int64" # Example types: "String", "Int64", "Float64", "Boolean"
                EffectiveLength: "Float64"
                TPM: "Float64"
                NumReads: "Float64"
              column_names:
                null # Optional: Override column names when has_header: false
                # Example: ["sample", "gene", "expression"]
              null_values:
                ["", "NULL", "null", "None"] # Optional: Values to treat as null/missing
                # Default: ["", "NULL", "null", "None"]
              n_rows:
                null # Optional: Limit number of rows to read
                # Useful for testing configurations
              encoding:
                "utf8" # Optional: File encoding (default: "utf8")
                # Example: "utf8", "latin1", "ascii"

              # Excel-specific options (for .xlsx, .xls files)
              sheet_name:
                null # Optional: Excel sheet name to read
                # Example: "Results", "Sheet1"
              sheet_id:
                null # Optional: Excel sheet index (0-based)
                # Example: 0 (first sheet), 1 (second sheet)

            # Optional: Column filtering for performance
            keep_columns: # Optional: Column filtering
              - "Name" # If specified, only these columns are retained
              - "TPM" # Improves performance for large datasets
              - "NumReads" # Example: ["sample_id", "expression", "p_value"]

            # Optional: Column documentation
            columns_description: # Optional: Column documentation
              Name: "Gene/transcript identifier" # Human-readable column descriptions
              TPM: "Transcripts per million" # Used in dashboard tooltips and documentation
              NumReads: "Estimated read count" # Example format: column_name: "Description"

        # Optional: Data joining configuration
        join: # Optional: Join this collection with others
          on_columns:
            ["sample_id"] # Required: Column names for joining
            # Must exist in both datasets
            # Example: ["sample_id"], ["sample_id", "timepoint"]
          how:
            "inner" # Required: Join type
            # Options: "inner", "outer", "left", "right"
          with_dc:
            ["qc_summary"] # Required: Target data collections to join with
            # References to other data_collection_tag values

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
            #   - Automatically detects multiqc_data/multiqc.parquet in each run
            #   - No scan configuration needed (auto-detected)
            #   - No metatype specification required
            #   - No dc_specific_properties needed
            #   - Requires MultiQC 1.29+ to generate parquet format

        # Optional: Join with other data collections
        join: # Optional: Join MultiQC data with other collections
          on_columns:
            ["sample"] # Required: Column for joining (typically "sample")
            # MultiQC sample names must match values in other datasets
          how:
            "inner" # Required: Join type
          with_dc:
            ["sample_metadata"] # Required: Target data collections
            # Can join with metadata, QC metrics, or other tables
```

## See Also

- **[YAML Examples](yaml-examples.md)** - Complete configuration examples and patterns
- **[Project Guide](guide.md)** - Comprehensive project management guide
- **[CLI Reference](../../depictio-cli/usage.md)** - Command-line interface documentation

