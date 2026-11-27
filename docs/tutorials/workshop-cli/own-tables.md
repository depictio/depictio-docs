---
glightbox: true
title: "A new season"
description: "Add a second table and its link to your Depictio project file, refresh the project, then add the next field season as a new run and compare what it changed."
---

# A new season

<div class="ws-strip" markdown>
[**0** Setup](setup.md){ .ws-ep0 } [**1** Your tables](project-builder.md){ .ws-ep1 } [**2** nf-core run](nf-core-run.md){ .ws-ep2 } [**3** Collaborate](collaborate-and-export.md){ .ws-ep3 } [**+** Going further](going-further.md){ .ws-ep4 .ws-here }
</div>

!!! note "Going further"
    Optional: not part of the timed workshop. It is one of the lessons of [Going further](going-further.md).

<div class="ws-meta ws-ep2" markdown>
<span class="ws-chip" markdown="span">:material-console: **Creator, from the terminal**</span> <span class="ws-chip" markdown="span">:material-penguin: **Palmer Penguins, two tables, two seasons**</span>
</div>

!!! overview "Overview"
    **Questions**

    - How do I add a table to a project, and link it to the first one?
    - The next season arrives: how do I add it, and see what it changed?

    **Objectives**

    - Extend the project file: a second table, a link, any season.
    - Refresh the project with `--update-config`.
    - Add the 2008 season as a new run, and compare.

You continue with the project of the lesson A project file by hand, in the same folder, `~/depictio-workshop/penguins-workshop`. `penguins.yaml` is `penguins-1.yaml` with three additions.

![penguins.yaml names the season folder with {SEASON_DIR}, two data collections and the link on individual_id; season_2007 refreshed with --update-config, then season_2008 attached with --attach-run, gives one project with two runs, and Compare on season_2008](../../images/tutorials/workshop-cli/diagrams/project-file_light.png#only-light){ .ws-diagram }
![penguins.yaml names the season folder with {SEASON_DIR}, two data collections and the link on individual_id; season_2007 refreshed with --update-config, then season_2008 attached with --attach-run, gives one project with two runs, and Compare on season_2008](../../images/tutorials/workshop-cli/diagrams/project-file_dark.png#only-dark){ .ws-diagram }

## :material-file-compare: What changes in the file

Compare the two files:

```bash
diff -u penguins-1.yaml penguins.yaml
```

```diff
--- penguins-1.yaml
+++ penguins.yaml
@@ -6,7 +6,7 @@
     data_location:
       structure: "flat"                   # flat: each folder under locations is one run
       locations:                          # relative to the folder you run depictio in
-        - "seasons/season_2007"           #   one folder, so one run: season_2007
+        - "{SEASON_DIR}"                  #   the folder named by SEASON_DIR on the command line
     data_collections:                     # the tables, one entry each
       - data_collection_tag: "physical_features"  # the table's name in Depictio
         config:
@@ -19,3 +19,21 @@
                 pattern: "physical_features.csv"  # the file that makes the table
           dc_specific_properties:
             format: "CSV"                 # how to read the file
+      - data_collection_tag: "demographic_data"   # a second table: who each bird is
+        config:
+          type: "Table"
+          metatype: "Aggregate"
+          scan:
+            mode: "recursive"
+            scan_parameters:
+              regex_config:
+                pattern: "demographic_data.csv"
+          dc_specific_properties:
+            format: "CSV"
+links:                                    # tables that filter each other
+  - source_dc_tag: "demographic_data"     # a filter on this table...
+    source_column: "individual_id"
+    target_dc_tag: "physical_features"    # ...narrows this one,
+    target_type: "table"
+    link_config:
+      target_field: "individual_id"       # matching individual_id
```

Lines starting with `-` are in `penguins-1.yaml` only, lines starting with `+` in `penguins.yaml` only; the others are the same in both. Three additions:

| Addition | Why |
|---|---|
| `{SEASON_DIR}` | One file for every season: the folder is no longer written in the file, the command line gives it, as `SEASON_DIR=seasons/season_2008` |
| `demographic_data` | Who each bird is: species, island, sex |
| `links` | The two tables share `individual_id`: a filter on a column only `demographic_data` has, such as `sex`, can narrow `physical_features` |

## :material-database-refresh: Refresh the project

```console
$ SEASON_DIR=seasons/season_2007 depictio ingest --project-config-path penguins.yaml \
    --project yourname-penguins --update-config
…
• The project keeps 1 run location(s): those of this configuration
✓ Project updated on server
✓ Data collection 'physical_features' processed successfully.
✓ Data collection 'demographic_data' processed successfully.
✓ Ingestion completed successfully! (7/7 steps)
```

`SEASON_DIR=…` goes on the **same line**, before `depictio`: it fills `{SEASON_DIR}` for this command only.

`--update-config` is how you change a project that exists, with no `--overwrite` and nothing to delete first: the project follows the file (two tables, one link now), every run is read again, and your dashboard stays as it is. Without it, the CLI refuses, as in challenge 1.2.

!!! challenge "Challenge 2.1: what did the refresh change?"
    Open your project in the browser. How many data collections, links and runs does it have now?

    ??? solution "Solution"
        Two data collections, `physical_features` and `demographic_data`, and one link. Still one run, `season_2007`: the folder is the same, written as `{SEASON_DIR}`.

## :material-update: A new season: 2008

```console
$ SEASON_DIR=seasons/season_2008 depictio ingest --project-config-path penguins.yaml \
    --project yourname-penguins --attach-run
…
✓ Workflow 'field_survey': +1 run location(s) -> seasons/season_2008
✓ Ingestion completed successfully! (8/8 steps)
```

`--attach-run` adds the folder to the **existing** project as one more run.

1. In the browser, open your project's **Runs** tab (1): two runs, `season_2007` and `season_2008`.
2. Expand **season_2008** (2): its two new files, and under **Produced** what the ingestion wrote to each table: +114 rows.
3. Click **Compare** (3).

    ![The Runs tab (1), season_2008 unfolded (2) with its new files and the rows it added, and Compare (3)](../../images/tutorials/workshop-cli/ep2_runs.webp){ .ws-shot }

4. Open **Changes** (the badge icon in the dashboard header). **Show on the dashboard → Split** (5) draws each figure three times: all the birds, the new season, the ones seen before.

    ![The Changes panel: physical_features 109 → 223 rows (4); Split (5) draws the scatter for All, New: season_2008 and Seen before, and the card reads 223, 114 and 109](../../images/tutorials/workshop-cli/ep2_compare.webp){ .ws-shot }

!!! challenge "Challenge 2.2: what did 2008 bring?"
    In the **Changes** panel, which table changed, and how many rows did it have before and after? Switch **Show on the dashboard** to **Split**: what do the cards show?

    ??? solution "Solution"
        The panel lists one collection: `physical_features`, from 109 to 223 rows. In **Split**, each figure is drawn three times: **All**, **New: season_2008** and **Seen before**. **Birds measured** reads 223, 114 and 109; the mean body mass reads 4,197, 4,267 and 4,125 g.

!!! callout "Why Compare stays grey on season_2007"
    Compare shows what an ingestion changed. The first run created the project: there was nothing before it to compare with. Each `--attach-run` records an ingestion for its run, so **Compare** works from the second run on.

!!! further "Going further"
    `depictio watch` runs `ingest` again whenever a folder changes: useful when new results land on a shared drive. See `depictio watch --help`.

!!! keypoints "Key points"
    - A project file grows with your data: add a table, add a link, and refresh with `--update-config`.
    - `{SEASON_DIR}` lets one file serve every season; set it on the command line.
    - `--attach-run` adds a folder as a new run; **Runs → Compare** shows what it changed.

<div class="ws-next" markdown>
[<span class="ws-k">Stuck?</span><span class="ws-t">Troubleshooting</span>](troubleshooting.md#new-season){ .ws-help }
[<span class="ws-k">Next episode</span><span class="ws-t">A dashboard as code</span>](dashboard-as-code.md){ .ws-go .ws-ep3 }
</div>
