---
title: "Projects"
description: "Create, fill and manage Depictio projects: from a few uploaded tables to the runs of a pipeline."
glightbox: true
---

# <span style="color: #45B8AC;">:material-folder-multiple:</span> Projects in Depictio

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../../images/guides/project-creation/create-project-from-folder.webp" src="../../../images/guides/project-creation/create-project-from-folder.mp4"></video></figure>

A project holds your data collections, the dashboards built on them, and who may use them. This page goes through each task; the [overview](index.md) shows how they fit together.

## Create a project <small>(v1.21.0+)</small> { #create-a-project }

[![The Projects page with the New project button in the header](../../images/guides/project-creation/projects_page_light.webp#only-light)](../../images/guides/project-creation/projects_page_light.webp){target=_blank}
[![The Projects page with the New project button in the header](../../images/guides/project-creation/projects_page_dark.webp#only-dark)](../../images/guides/project-creation/projects_page_dark.webp){target=_blank}

A project starts from its data: Depictio works out whether it holds plain tables or the run of a pipeline. There is no Basic or Advanced choice.

### 1. Name the project

[![Screen 1 of New project: Project name, Description, Make this project public, Add data / Create without data, Or start from Import a project](../../images/guides/project-creation/new_project_dialog_light.webp#only-light){ width="569" }](../../images/guides/project-creation/new_project_dialog_light.webp){target=_blank}
[![Screen 1 of New project: Project name, Description, Make this project public, Add data / Create without data, Or start from Import a project](../../images/guides/project-creation/new_project_dialog_dark.webp#only-dark){ width="569" }](../../images/guides/project-creation/new_project_dialog_dark.webp){target=_blank}

**Projects**, **New project**: a **Project name**, an optional **Description** and **Make this project public**. Then:

- **Add data**: files, a folder, a pipeline run.
- **Create without data**: an empty project, filled later with [Add data](#add-data).
- **Import a project**: one exported from Depictio, see [Project migration](../administration/migrate.md#web-ui). **See an example** opens a finished project, when the server holds one.

In public or demo mode, only admins can create projects.

### 2. Your data

[![The Your data step with its Upload and Read in place sides](../../images/guides/project-creation/your_data_step_light.webp#only-light)](../../images/guides/project-creation/your_data_step_light.webp){target=_blank}
[![The Your data step with its Upload and Read in place sides](../../images/guides/project-creation/your_data_step_dark.webp#only-dark)](../../images/guides/project-creation/your_data_step_dark.webp){target=_blank}

**Add data** opens a stepper, **Your data**, **What Depictio found**, **Create**; **Use the whole window** gives it the full screen. The two sides can be combined:

=== "Upload"

    Drop files or whole folders, up to 50 MB each. Tables (CSV, TSV, Parquet, Feather), MultiQC reports, phylogenetic trees, GeoJSON maps and images are recognised.

=== "Read in place"

    [![Read in place, One file URL tab: the URL, the name, the format and a preview of the table](../../images/guides/project-creation/read_in_place_url_light.webp#only-light)](../../images/guides/project-creation/read_in_place_url_light.webp){target=_blank}
    [![Read in place, One file URL tab: the URL, the name, the format and a preview of the table](../../images/guides/project-creation/read_in_place_url_dark.webp#only-dark)](../../images/guides/project-creation/read_in_place_url_dark.webp){target=_blank}

    Nothing is uploaded. **Folder or bucket** takes an `s3://` location, or a folder on the server's disk (**Browse**, where the server allows it, as under `depictio local`). **One file URL** takes a single `https://` or `s3://` CSV, TSV, Parquet or Feather file, gzipped or not. See [Remote data](remote-data.md#from-a-run-folder) for buckets and their keys.

### 3. Pick how Depictio reads it { #read-levels }

[![The read levels: Flat tables, Custom workflows and Pipeline template, with the detected pipeline](../../images/guides/project-creation/read_levels_light.webp#only-light)](../../images/guides/project-creation/read_levels_light.webp){target=_blank}
[![The read levels: Flat tables, Custom workflows and Pipeline template, with the detected pipeline](../../images/guides/project-creation/read_levels_dark.webp#only-dark)](../../images/guides/project-creation/read_levels_dark.webp){target=_blank}

**How should Depictio read this folder?** offers three levels. The best fit is preselected; one that does not fit says why.

| Level | Makes | Same in YAML |
|-------|-------|--------------|
| :material-table: **Flat tables** | One collection per table file, no workflow, no dashboards | Top-level `data_collections` |
| :material-sitemap: **Custom workflows** | Collections you define in the [Project Builder](#project-builder), grouped by workflow | `workflows` |
| :material-package-variant: **Pipeline template** | A recognised pipeline read with its [template](templates.md), dashboards included | `depictio ingest DIR --template ID` |

A recognised pipeline shows **Pipeline:** *name version* **· Detected**, with **Change**. Otherwise **I know the pipeline** opens the picker. `project_type` (`basic`, `advanced`) is still read from YAML but changes nothing.

### 4. Check, then create

[![What Depictio found step for a pipeline run: Pipeline, Source, Contents and the collections found](../../images/guides/project-creation/what_depictio_found_light.webp#only-light)](../../images/guides/project-creation/what_depictio_found_light.webp){target=_blank}
[![What Depictio found step for a pipeline run: Pipeline, Source, Contents and the collections found](../../images/guides/project-creation/what_depictio_found_dark.webp#only-dark)](../../images/guides/project-creation/what_depictio_found_dark.webp){target=_blank}

**What Depictio found** lists the pipeline, the runs, the source and the contents before anything is written. For flat tables, tick the tables and click **Create project with N tables**. For a pipeline, **Next**, then **Create Project** starts the ingestion.

[![A project page header with the Pipeline, Runs, Data collections and Source facts](../../images/guides/project-creation/project_header_found_light.webp#only-light)](../../images/guides/project-creation/project_header_found_light.webp){target=_blank}
[![A project page header with the Pipeline, Runs, Data collections and Source facts](../../images/guides/project-creation/project_header_found_dark.webp#only-dark)](../../images/guides/project-creation/project_header_found_dark.webp){target=_blank}

The project header then says what it holds: **Pipeline**, **Runs**, **Data collections** and their **Source**.

### With the CLI { #create-with-the-cli }

A YAML file describes the project and `depictio ingest` creates it.

=== "Tables only"

    ```yaml
    name: "My Project"
    workflows:              # ingest scans the collections of a workflow
      - name: "tables"
        engine: { name: "python" }
        data_location: { structure: "flat", locations: ["/path/to"] }
        data_collections:
          - data_collection_tag: "my_data"
            config:
              type: "Table"
              metatype: "Metadata"
              scan:
                mode: "single"
                scan_parameters:
                  filename: "/path/to/data.csv"
              dc_specific_properties:
                format: "CSV"
    ```

    ```bash
    depictio ingest --project-config-path tables_project.yaml
    ```

=== "Runs of a pipeline"

    Collections sit under a workflow, read from each run folder that `runs_regex` matches under `data_location.locations`:

    ```yaml
    name: "RNA-seq Expression Study"
    workflows:
      - name: "rnaseq_pipeline"
        engine: { name: "nextflow", version: "24.10.3" }
        data_location:
          structure: "sequencing-runs"
          locations: ["{DATA_LOCATION}/rnaseq-results"]
          runs_regex: ".*"
        data_collections:
          - data_collection_tag: "sample_stats"
            config:
              type: "Table"
              metatype: "Aggregate"
              scan:
                mode: "recursive"
                scan_parameters:
                  regex_config: { pattern: "stats/.*_stats.tsv" }
              dc_specific_properties:
                format: "TSV"
                polars_kwargs: { separator: "\t" }
    ```

    Annotated versions, links and every scan mode: [YAML examples](yaml-examples.md) and the [reference](reference.md).

=== "From a template"

    ```bash
    depictio ingest /data/my_ampliseq_run --template nf-core/ampliseq/2.16.0
    ```

    One command resolves the template's variables, creates the project, runs its recipes and imports its dashboards. Without `--template`, the template is detected from the folder, and a folder none fits gets one [composed from the catalog](composed-dashboards.md). The folder can be an `s3://` prefix, see [Remote data](remote-data.md). Full reference: [Templates](templates.md).

`--dry-run` previews without contacting the server, and `--skip STEP` leaves steps out (see [Skipping steps](../../depictio-cli/usage.md#skipping-steps)). Running the same command again with `--update-config` refreshes the project and keeps its dashboards ([Refreshing a project](../../depictio-cli/usage.md#refreshing-a-project)).

## Add data to a project { #add-data }

[![Add data on a pipeline project: a second run folder, its What Depictio found facts and the Add run button](../../images/guides/project-creation/add_data_run_light.webp#only-light)](../../images/guides/project-creation/add_data_run_light.webp){target=_blank}
[![Add data on a pipeline project: a second run folder, its What Depictio found facts and the Add run button](../../images/guides/project-creation/add_data_run_dark.webp#only-dark)](../../images/guides/project-creation/add_data_run_dark.webp){target=_blank}

**Add data** on the project page has the same **Upload** and **Read in place** sides. Another run of the project's pipeline is added as a run; any other folder offers its tables as new collections. The button says which: **Add run**, **Add N tables** or **Add run and N tables**. From the CLI, `depictio ingest --attach-run`.

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../../images/guides/project-creation/add-run.webp" src="../../../images/guides/project-creation/add-run.mp4"></video></figure>

[![Add data refusing a run: the Samples row warning that its samples are already in the project](../../images/guides/project-creation/duplicate_samples_light.webp#only-light)](../../images/guides/project-creation/duplicate_samples_light.webp){target=_blank}
[![Add data refusing a run: the Samples row warning that its samples are already in the project](../../images/guides/project-creation/duplicate_samples_dark.webp#only-dark)](../../images/guides/project-creation/duplicate_samples_dark.webp){target=_blank}

- A run whose MultiQC reports name samples already in the project is held back: the **Samples** row lists them. Rename them, or read the run as its own project. When not every report could be read, the check is partial: the row shows **Needs a look** and names the reports it skipped <small>(v1.22.0+)</small>. The **Checks** of a new project made from several runs do the same.
- Only a project made from a pipeline template takes another run, and only when its collections walk a folder. A project read from an `s3://` run folder cannot.
- Each run is listed on the project's [Runs](../../features/runs.md) page.

### Edit a table { #edit-a-table }

[![An uploaded table unlocked (Editable), with Save changes, Discard and Past versions](../../images/guides/metadata-panel/table_edit_mode_light.webp#only-light)](../../images/guides/metadata-panel/table_edit_mode_light.webp){target=_blank}
[![An uploaded table unlocked (Editable), with Save changes, Discard and Past versions](../../images/guides/metadata-panel/table_edit_mode_dark.webp#only-dark)](../../images/guides/metadata-panel/table_edit_mode_dark.webp){target=_blank}

A table you uploaded or added, typically a sample sheet, can be edited like a spreadsheet. Tables from a pipeline run or a template stay read-only, since the next ingestion would overwrite them.

1. Turn the lock switch from **Read-only** to **Editable**.
2. Click a cell to change it, or drop a file to preview **Add columns**, **Fill missing** or **Replace**.
3. Each save is a new version. **Past versions**, then **Restore v3** for instance, writes an old one back as a new version.

A table whose columns look like a latitude and longitude shows **Map coordinates…**, see [Map-capable tables](#example-map-capable-table-dcs). See also the [Metadata panel](../../features/metadata-panel.md).

### Manage a data collection { #managing-data-collections-from-the-viewer-v0120 }

[![Manage Data Collection, Modify data: the Replace existing data switch and the file drop zone](../../images/guides/project-creation/manage_dc_modify_light.webp#only-light){ width="620" }](../../images/guides/project-creation/manage_dc_modify_light.webp){target=_blank}
[![Manage Data Collection, Modify data: the Replace existing data switch and the file drop zone](../../images/guides/project-creation/manage_dc_modify_dark.webp#only-dark){ width="620" }](../../images/guides/project-creation/manage_dc_modify_dark.webp){target=_blank}

The :material-database-cog-outline: icon of a collection (**Manage data (append / replace / clear)**) opens **Manage Data Collection**, for editors and owners.

| Tab | Does | Button |
|-----|------|--------|
| **Modify data** | Adds dropped files: one table file up to 5 MB, or MultiQC folders (50 MB a file, 500 MB in all) | **Append folders** |
| **Modify data**, **Replace existing data** on | Wipes the collection and ingests the dropped files | **Replace all data** |
| **Clear contents** | Deletes the data, keeps the collection and its links; type its name to confirm | **Clear data collection** |

[![Manage Data Collection, Clear contents: the warning and the collection name to type to confirm](../../images/guides/project-creation/manage_dc_clear_light.webp#only-light){ width="620" }](../../images/guides/project-creation/manage_dc_clear_light.webp){target=_blank}
[![Manage Data Collection, Clear contents: the warning and the collection name to type to confirm](../../images/guides/project-creation/manage_dc_clear_dark.webp#only-dark){ width="620" }](../../images/guides/project-creation/manage_dc_clear_dark.webp){target=_blank}

MultiQC reports must agree (same modules, plot keys and MultiQC version, no sample twice) or they are refused. A later CLI refresh keeps what was added here. Collections read from a manifest, a URL or a bucket are re-read with **Project settings**, [**Data refresh**](remote-data.md#refreshing-the-data).

### Join two tables { #join-two-tables }

<span class="ver-badge">v1.23.0+</span>

<figure markdown="span"><video preload="none" data-autoplay controls muted loop playsinline poster="../../../images/guides/project-creation/join-create.webp" src="../../../images/guides/project-creation/join-create.mp4"></video></figure>

[![Create table join: two tables joined on sample, with the preview counting the rows without a match](../../images/guides/project-creation/join_create_modal_light.webp#only-light){ width="620" }](../../images/guides/project-creation/join_create_modal_light.webp){target=_blank}
[![Create table join: two tables joined on sample, with the preview counting the rows without a match](../../images/guides/project-creation/join_create_modal_dark.webp#only-dark){ width="620" }](../../images/guides/project-creation/join_create_modal_dark.webp){target=_blank}

Two tables that share a column become one new table, read by any component. On the project page: **Cross-DC links**, **Add join** (owners and editors, project not read-only).

1. **Name** the join: letters, digits, `_` and `-`. The new table is called `joined_<name>`.
2. Pick the **Left table** and the **Right table**: preselected from the project's link, or else its two oldest tables.
3. Pick the **Join column(s)** they share and a **Join type**: **Left**, **Inner**, **Outer** or **Right**.
4. Check the preview (row and column counts, rows without a match, warnings), then **Create join**.

[![Cross-DC links: the map with the joined table, and the Joins list with the join's tables, columns, type and row count](../../images/guides/project-creation/join_list_light.webp#only-light)](../../images/guides/project-creation/join_list_light.webp){target=_blank}
[![Cross-DC links: the map with the joined table, and the Joins list with the join's tables, columns, type and row count](../../images/guides/project-creation/join_list_dark.webp#only-dark)](../../images/guides/project-creation/join_list_dark.webp){target=_blank}

The two tables stay as they are; the joined table carries a `joined` badge and is rebuilt whenever one of them changes. It cannot be appended to, replaced or cleared itself: change its sources instead. The join is listed under **Joins** in the same section, where it can be deleted.

What a join is, and how it differs from a link: [Joining and linking](../../features/data-model.md#join-from-the-web-ui).

## Project Builder <small>(v1.21.0+)</small> { #project-builder }

For a folder no shipped template fits, the Project Builder lets you define the collections yourself. It writes the same YAML as the CLI.

=== "In the app"

    [![Project Builder, Source & project step: the data root and the project fields](../../images/guides/project-creation/builder_source_light.webp#only-light)](../../images/guides/project-creation/builder_source_light.webp){target=_blank}
    [![Project Builder, Source & project step: the data root and the project fields](../../images/guides/project-creation/builder_source_dark.webp#only-dark)](../../images/guides/project-creation/builder_source_dark.webp){target=_blank}

    Pick **Custom workflows** for a folder, then **Open the Project Builder** (or go to `/projects/build`). Three steps: **Source & project**, **Data collections**, **Review & create**. Start from scratch, from a folder or from a shipped template; a GitHub URL fills the workflow's metadata from its RO-Crate or Nextflow manifest.

    [![Project Builder, Data collections step: a workflow tree, one collection with its path wildcard and the matching files](../../images/guides/project-creation/builder_collections_light.webp#only-light)](../../images/guides/project-creation/builder_collections_light.webp){target=_blank}
    [![Project Builder, Data collections step: a workflow tree, one collection with its path wildcard and the matching files](../../images/guides/project-creation/builder_collections_dark.webp#only-dark)](../../images/guides/project-creation/builder_collections_dark.webp){target=_blank}

    Every collection kind, path wildcards, run detection by regular expression and links between collections.

    [![Project Builder, Review & create step: the links, the generated YAML and the Create button](../../images/guides/project-creation/builder_review_light.webp#only-light)](../../images/guides/project-creation/builder_review_light.webp){target=_blank}
    [![Project Builder, Review & create step: the links, the generated YAML and the Create button](../../images/guides/project-creation/builder_review_dark.webp#only-dark)](../../images/guides/project-creation/builder_review_dark.webp){target=_blank}

=== "Without a server"

    On a machine with no Depictio server, such as an HPC login node, the builder reads only the folder you give it:

    ```bash
    uv tool install 'depictio[builder]'
    depictio project-builder ./results            # --out DIR, --port 8129
    ```

    It opens `http://127.0.0.1:8129/projects/build` and writes a template bundle to `<dir>/.depictio/template`. Run it against any server:

    ```bash
    depictio ingest ./results --template ./results/.depictio/template
    ```

## Data collection types { #type-specific-data-collection-configuration }

Most collections are tables. A few types carry extra configuration at the collection level, so every figure built on them inherits it.

| Type | Holds | Read by |
|------|-------|---------|
| :material-map-marker-multiple: [Map-capable table](#example-map-capable-table-dcs) | A table with coordinates | Map figures |
| :material-family-tree: [`phylogeny`](#example-phylogeny-dcs-and-their-metadata-table) | A Newick or Nexus tree, with a metadata table | [Phylogenetic](../../features/advanced-visualizations.md#phylogenetic) |
| :material-dna: [`indexed_file`](#example-indexed-file-dcs) | One indexed genomic file per sample, no table | [Genome view](../../features/advanced-visualizations.md#genome-view) |
| :material-chart-timeline: [`genomic_tracks`](#example-genomic-tracks-dcs) | A table of track files, one row each | [Genome browser](../../features/genome-browser/index.md) |
| :material-molecule: [Protein structures](#example-protein-structure-dcs) | One structure or PAE file per protein | [Protein tiles](../../features/proteins.md#the-data) |

### :material-map-marker-multiple: Map-capable tables { #example-map-capable-table-dcs }

A table whose columns look like a latitude and longitude shows **Map coordinates…**: confirm or change the columns. Every Map figure on it then inherits them. In YAML, set `lat_column` and `lon_column` (both, and different) in the collection's `dc_specific_properties`, `crs` defaulting to `EPSG:4326` (see the [reference](reference.md)); at upload, `POST /create_from_upload` takes `latColumn` and `lonColumn`. A figure's own `lat_column` and `lon_column` still win.

### :material-family-tree: Phylogeny and its metadata table { #example-phylogeny-dcs-and-their-metadata-table }

Ingestion copies the tree file as is to S3, never converted. Its tip annotations come from a separate table keyed by taxon name; leave the three `metadata_*` keys out and the tree renders unannotated.

??? example "YAML"

    ```yaml
    - data_collection_tag: "bacterial_tree"
      config:
        type: "phylogeny"
        metatype: "Aggregate"
        scan:
          mode: "single"
          scan_parameters:
            filename: "{DATA_ROOT}/trees/bacterial_tree.nwk"
        dc_specific_properties:
          format: "newick"          # or "nexus"
          ladderize: true
          metadata_dc_tag: "bacterial_metadata"
          metadata_taxon_column: "taxon"
          # tip_label_strategy: "first_token" when leaf names carry a suffix
    ```

A component points at the tree with `tree_wf_id` and `tree_dc_id`. More in [YAML examples](yaml-examples.md).

### :material-dna: Indexed files { #example-indexed-file-dcs }

For a genomic file too large to become a table: a per-sample VCF, a BAM, a bigWig, a GFF3, or any bgzip and tabix-indexed file. Ingestion builds no table: it copies each file and its index to S3, and a genome track reads only the region in view. Prefer a table when the data is small enough to filter as rows.

??? example "YAML"

    ```yaml
    - data_collection_tag: "variant_files"
      optional: true
      config:
        type: "indexed_file"
        metatype: "Metadata"
        scan:
          mode: "recursive"
          scan_parameters:
            regex_config:
              pattern: ".*\\.ann\\.vcf\\.gz$"
        dc_specific_properties:
          format: "vcf"            # vcf, bam, bigwig, bigbed, gff3, fasta or tabix
          assembly: "{GENOME}"
          sample_regex: "(?P<sample>[^/]+?)\\.ann\\.vcf\\.gz$"
          max_file_size_mb: 64
    ```

| Key | Default | Meaning |
|-----|---------|---------|
| `format` | required | `vcf`, `bam`, `bigwig`, `bigbed`, `gff3`, `fasta`, `tabix` (aliases `bw`, `bb`, `gff`) |
| `index_suffix` | per format | `.tbi`, `.bai` or `.fai`; none for bigWig and bigBed. An empty string declares a self-indexed file |
| `sample_regex` | file name | A regex with a named `sample` group |
| `sample_col` | `sample` | The sample column of the project's tables, so the dashboard's sample filter applies |
| `assembly` | none | Genome assembly; left out, the component decides |
| `max_file_size_mb` | `512` | Per-file cap |

One primary file per sample: a file without its index, or a second file for a sample already taken, is skipped with a warning. `optional: true` keeps a run fetched without its indexes from failing.

#### Storage the browser can read <small>(v1.13.0+)</small> { #indexed-file-storage }

The browser reads the files from the object store with presigned URLs, valid 15 minutes. They are signed for `DEPICTIO_S3_PUBLIC_URL`, or else `DEPICTIO_S3_EXTERNAL_PROTOCOL`, `_HOST` and `_PORT`: an in-cluster name such as `http://s3:9000` fails in the browser. The store must answer the viewer's origin with CORS and serve range requests: the bundled SeaweedFS allows every origin (narrow it with `-s3.allowedOrigins=`); on AWS, allow `GET` and `HEAD` with `Range`, and expose `Content-Range`, `Content-Length`, `Accept-Ranges` and `ETag`. Without this, a genome view shows no file tracks.

### :material-chart-timeline: Genomic tracks { #example-genomic-tracks-dcs }

A table of track files, one row per bigWig, narrowPeak, BAM, VCF or other file, its location in `uri_column`. It is ingested like a table, so it filters, links and joins like one, and the [genome browser](../../features/genome-browser/index.md) shows the rows left after filtering. A relative `uri` is uploaded at ingestion; an `s3://` or `https://` one is read in place, from hosts on the server's [allow-list](../../features/security.md#genome-browser-track-access).

??? example "YAML, from the nf-core/chipseq template"

    ```yaml
    - data_collection_tag: "tracks"
      config:
        type: "genomic_tracks"
        metatype: "Metadata"
        source: "transformed"
        transform:
          recipe: "nf-core/chipseq/tracks.py"
        dc_specific_properties:
          format: "TSV"
          uri_column: "uri"
          track_id_column: "track_id"
          sample_column: "sample_id"
          format_column: "format"
          assembly: "hg19"
    ```

A project writing its own table uses `scan` instead of `transform`, and `remote_base_uri` to read relative paths under a remote prefix. Every key (`index_column`, `name_column`, `color_column`, `direct_access`, the assembly presets) is in the [reference](reference.md). A link with `target_type: genomic_tracks` lets a table selection pick the tracks, see [Cross-DC filtering](../../features/cross-dc-filtering.md#supported-target-types).

### :material-molecule: Protein structures <small>(v1.19.0+)</small> { #example-protein-structure-dcs }

Structures and PAE matrices are `indexed_file` collections with no index, one file per protein, fetched whole by a [protein tile](../../features/proteins.md#the-data). `format` is `pdb` (`.pdb`, `.ent`), `mmcif` (`.cif`, `.mmcif`) or `pae` (`.pae.tsv`, `.pae.json`). The sample id the scan derives must equal the `entity` of the residue tables.

??? example "YAML"

    ```yaml
    - data_collection_tag: "structures"
      config:
        type: "indexed_file"
        metatype: "Metadata"
        scan:
          mode: "recursive"
          scan_parameters:
            regex_config:
              pattern: ".*/top_ranked_structures/[^/]+\\.pdb$"
        dc_specific_properties:
          format: "pdb"
          sample_regex: "top_ranked_structures/(?P<sample>[^/]+?)\\.pdb$"
    ```

## :material-lock: Project permissions { #project-permissions }

| Role | Can |
|------|-----|
| **Owner** | Everything: edit, delete, manage permissions, delete a collection |
| **Editor** | Change data, write a collection, create and edit dashboards |
| **Viewer** | Read the project and its dashboards |

A role goes to a person or to a [group](../administration/groups.md) <small>(v1.18.0+)</small>, from the project's **Permissions** page; a person's role is the highest of their own and their groups'. Sharing goes through **Permissions** only.

**Make this project public**, or `is_public: true`, lets every user read it; only owners and editors can change it.

### Everyone with access <small>(v1.19.0+)</small> { #everyone-with-access }

**Everyone with access** sums direct and group grants: one row per person, highest role first. Typing a group's name previews its members before **Add group**. Emails show only to those who may change the sharing: owners, system admins and the admins of an owning group.

## :material-trash-can: Project deletion { #project-deletion }

Deleting a project, in the web UI or with `DELETE /depictio/api/v1/projects/{id}`, deletes its workflows, data collections, dashboards and its S3 objects. There is no trash: export it first with **Export as a ZIP file** ([Project migration](../administration/migrate.md)) if you may need it back.

## Troubleshooting

=== "YAML fails validation"

    ```bash
    depictio -v config check --project-config-path ./config.yaml
    ```

=== "Files not found"

    Preview what each collection matches, without contacting the server, then scan alone:

    ```bash
    depictio ingest --project-config-path ./config.yaml --dry-run
    depictio data scan --project-config-path ./config.yaml
    ```

    Check the paths, the regex patterns and the variables they use.

=== "More detail"

    `-v` logs at INFO, `-vv` at DEBUG: `depictio -vv ingest --project-config-path ./config.yaml`.

## See also

- [YAML examples](yaml-examples.md) and the [full reference](reference.md)
- [Templates](templates.md), [Recipes](recipes.md) and [Remote data and manifests](remote-data.md)
- [CLI usage](../../depictio-cli/usage.md) and [Cross-DC filtering](../../features/cross-dc-filtering.md)
- [Runs](../../features/runs.md), [What's new](../../features/whats-new.md) and the [Metadata panel](../../features/metadata-panel.md)
- [Creating dashboards](../guides/dashboard_creation.md)
