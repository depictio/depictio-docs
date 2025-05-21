# Minimal Reference Configuration

<!-- markdownlint-disable MD046 -->
!!! danger "Warning"
  This is not recommended to copy and paste the configuration as is. The configuration is meant to be a example and should be modified to fit your specific use case.
<!-- markdownlint-enable MD046 -->

This is a minimal reference configuration example file for the Depictio CLI. It includes the minimum required options and their descriptions. You can use this as a template to create your own configuration file.

```yaml
name: "Example project"
# Workflows section
workflows:
  - name: "example_workflow"
    engine:
      name: "python"
    config:
      parent_runs_location:
        - "/home/user/data/example_workflow"
      runs_regex: ".*"
    # Data collections section
    data_collections:
      - data_collection_tag: "example_data_collection"
        config:
          type: "Table"
          metatype: "Aggregate"
          scan:
            mode: recursive
            scan_parameters:
              regex_config:
                pattern: "*.stats.tsv"
          dc_specific_properties:
            format: "TSV"
            polars_kwargs:
              separator: "\t"
```
