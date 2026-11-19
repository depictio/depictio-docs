---
title: Minimal project YAML
description: The smallest project file depictio ingest accepts.
---

# Minimal project YAML

For a pipeline with no [template](../usage/projects/templates.md): one workflow, one table collected from every run.

```yaml
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

```bash
depictio ingest --project-config-path project.yaml --dry-run
depictio ingest --project-config-path project.yaml
```

Every field: [Full reference](../usage/projects/reference.md). Worked examples: [YAML project configuration](../usage/projects/yaml-examples.md).
