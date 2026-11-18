# Minimal project YAML

For a pipeline with no [template](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/index.md): one workflow, one table collected from every run.

```
name: "Example project"
workflows:
  - name: "example_workflow"
    engine:
      name: "python"
    data_location:
      structure: "sequencing-runs"   # one subfolder per run; or "flat"
      locations:
        - "/home/user/data/example_workflow"
      runs_regex: ".*"               # which subfolders are runs
    data_collections:
      - data_collection_tag: "example_table"
        config:
          type: "Table"
          metatype: "Aggregate"
          scan:
            mode: recursive
            scan_parameters:
              regex_config:
                pattern: ".*\\.stats\\.tsv"   # a regular expression, not a glob
          dc_specific_properties:
            format: "TSV"
            polars_kwargs:
              separator: "\t"
```

```
depictio ingest --project-config-path project.yaml --dry-run
depictio ingest --project-config-path project.yaml
```

Every field: [Full reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md). Worked examples: [YAML project configuration](https://depictio.github.io/depictio-docs/latest/usage/projects/yaml-examples/index.md).
