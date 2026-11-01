---
title: Genome browser
description: An embedded JBrowse 2 genome browser fed by a genomic_tracks collection, filtered by the dashboard and filtering it back.
---

# :material-dna: Genome browser <small>(v1.20.0+)</small>

<figure markdown="span">
  <video autoplay controls muted loop playsinline poster="../../images/guides/genome-browser/table_to_browser.webp" src="../../images/guides/genome-browser/table_to_browser.mp4"></video>
  <figcaption>A row picked in a table: its record card and the genome browser follow (nf-core/riboseq dashboard template).</figcaption>
</figure>

A pipeline run publishes coverage, peaks, variants and alignments as files. The `jbrowse`
component shows them in an embedded [JBrowse 2](https://jbrowse.org) linear genome view, inside
the dashboard and linked to it:

- **The dashboard drives the browser.** Filter a sample, pick a table row or lasso points in a
  scatter, and the browser shows the matching tracks and moves to the locus of the picked row.
- **The browser drives the dashboard.** Click a feature (or change which tracks are open) and
  the rest of the dashboard filters on that track's sample.

The tracks are listed in a `genomic_tracks` data collection, one row per file. Nothing else has
to run: the browser is part of the web app and the track bytes come through the API, in
`depictio local up`, Docker Compose and Kubernetes alike.

!!! note "Replaces the JBrowse iframe"
    Before v1.20.0, depictio showed JBrowse in an iframe to a separate JBrowse server
    (port 3000) fed by a session watcher (port 9010), with a `jbrowse2` data collection type.
    Both services and that type are gone. See the [changelog](../changelog/README.md) for the
    migration.

---

## The data: a `genomic_tracks` collection

A `genomic_tracks` collection is a table of track files: one row per track. It is ingested like
a table collection, so it can be shown in a table, filtered and linked, and the files it names
are either uploaded or read where they are.

```yaml
- data_collection_tag: tracks
  config:
    type: genomic_tracks
    metatype: Metadata
    scan: {mode: single, scan_parameters: {filename: tracks.tsv}}
    dc_specific_properties:
      format: TSV
      polars_kwargs: {separator: "\t"}
      uri_column: uri
      track_id_column: track_id
      sample_column: sample
      format_column: format
      name_column: name
      category_column: category
      order_column: order
      assembly: hg38
```

| Key | Default | Meaning |
|-----|---------|---------|
| `uri_column` | `uri` | A path relative to the data location, an `s3://` or an `https://` URI |
| `track_id_column` | | A stable track id (else a hash of the URI) |
| `sample_column` | | The column tracks are filtered and selected on |
| `format_column` / `default_format` | `format` | The track format, else inferred from the file extension |
| `index_column` | `index_uri` | The index file; `.tbi`, `.csi`, `.bai`, `.crai`, `.fai` and `.gzi` next to the file are found otherwise |
| `name_column`, `color_column`, `category_column` | | Track label, colour, and the folder of the track selector |
| `order_column` | | The order the browser opens the tracks in |
| `assembly` | `hg38` | A built-in assembly (or one of its aliases), or a custom assembly |
| `tracks_base_path` | the manifest's folder | The local folder relative rows are uploaded from |
| `remote_base_uri` | | An `s3://` or `https://` folder that relative rows are read under, in place |
| `direct_access` | `false` | Let the browser fetch `https://` tracks itself (the host must send CORS headers) |
| `display_defaults` | `{}` | JBrowse track configuration merged into every track of a format |
| `presets` | `{}` | Named configuration fragments a component can pick with `preset` |

**Formats:** `bigwig`, `bedgraph` (tabix), `bed` and `bed.gz`, `bigbed`, `narrowpeak`,
`broadpeak`, `vcf`, `bam`, `cram`, `gff3`, `gtf`, `hic` and `fasta`. Tabix formats need a
`.tbi` or `.csi` index, BAM and CRAM a `.bai` or `.crai`. Small plain BED and narrowPeak files
are read whole.

### Internal and external tracks

A track is either **internal**, a file of the run uploaded into depictio's storage at
ingestion, or **external**, read where it already is. The `uri` of each row, and two keys of the
collection, decide which:

| Track | `uri` in the manifest | Collection keys | Who reads it |
|-------|-----------------------|-----------------|--------------|
| Internal | a relative path | none | the API, from depictio's storage |
| External, read in place | a relative path, or an absolute `s3://` or `https://` URI | `remote_base_uri` for relative paths | the API, from an allow-listed host or bucket |
| External, fetched by the browser | an `https://` URI | `direct_access: true` | the browser |

Two more kinds of external tracks are set on the component rather than in the manifest:
[UCSC tracks](#tracks-and-their-configuration) (`ucsc_tracks`) and raw JBrowse tracks
(`config_overrides.extra_tracks`, [below](#raw-jbrowse-tracks)).

#### Internal tracks

The manifest names each file relative to the manifest's own folder (or to `tracks_base_path`):

```text
track_id    sample  format  uri                          name
S1.signal   S1      bigwig  bigwig/S1.bigWig             S1 signal
S1.peaks    S1      bed     peaks/S1.peaks.bed.gz        S1 peaks
S1.reads    S1      bam     bam/S1.markdup.sorted.bam    S1 reads
```

When the collection is ingested (`depictio run`, `depictio data sync`), the manifest becomes a
Delta table and each file is uploaded with its index (here `S1.peaks.bed.gz.tbi` and
`S1.markdup.sorted.bam.bai`, found next to the file) under the collection's
`genomic_tracks/<dc_id>/` folder of depictio's storage. The files are removed with the
collection or the project. Use internal tracks when the run's results live on a disk the server
cannot reach.

#### External tracks read in place

With `remote_base_uri`, nothing is copied: the relative rows are read under that folder, through
the API, each time the browser asks for a range of a file. A row may also carry an absolute
`s3://` or `https://` URI, which is read in place without `remote_base_uri`.

```yaml
dc_specific_properties:
  uri_column: uri
  remote_base_uri: s3://my-results/chipseq/run-42/   # or https://data.example.org/run-42/
```

The server reads only from hosts and buckets it allows, set by the administrator:

```bash
DEPICTIO_JBROWSE_REMOTE_HTTPS_HOSTS=data.example.org
DEPICTIO_JBROWSE_REMOTE_S3_BUCKETS=my-results
# A private bucket, or one outside AWS:
DEPICTIO_JBROWSE_REMOTE_S3_ENDPOINT_URL=https://s3.example.org
DEPICTIO_JBROWSE_REMOTE_S3_REGION=eu-west-1
DEPICTIO_JBROWSE_REMOTE_S3_ACCESS_KEY=...
DEPICTIO_JBROWSE_REMOTE_S3_SECRET_KEY=...
```

Without credentials, remote buckets are read anonymously. A listed bucket is readable by anyone
who can open a collection pointing at it, so list only buckets whose content may be shown.
`http://` URIs are refused. Since the files stay where they are, a file replaced at the same
path shows its new content (see [Versions](#versions)).

The nf-core dashboard templates turn the results folder of a run into `remote_base_uri`:
`depictio run --var TRACKS_URI=s3://<bucket>/<run>/results/` reads the run's tracks in place,
and without the variable the files found in the local results folder are uploaded.

#### External tracks fetched by the browser

With `direct_access: true`, the browser fetches the collection's `https://` tracks itself
instead of going through the API. The host must answer cross-origin range requests (CORS with
`Range` allowed and `Content-Range` exposed), and the instance's Content Security Policy must
allow it: by default it lets the browser connect only to depictio itself and to UCSC's download
server. Read in place through the API is the safer choice; use direct access for a public host
that is close to the readers.

#### Raw JBrowse tracks

`config_overrides.extra_tracks` adds JBrowse track configurations as they are, next to the
collection's tracks. The browser fetches their files itself, under the same CORS and Content
Security Policy conditions as direct access:

```yaml
- component_type: jbrowse
  data_collection_tag: tracks
  config_overrides:
    extra_tracks:
      - type: FeatureTrack
        trackId: regions_of_interest
        name: Regions of interest
        adapter:
          type: BedTabixAdapter
          bedGzLocation: {uri: "https://hgdownload.soe.ucsc.edu/<path>/regions.bed.gz"}
          index: {location: {uri: "https://hgdownload.soe.ucsc.edu/<path>/regions.bed.gz.tbi"}}
```

### Assemblies

Eleven assemblies are built in, each with UCSC's 2bit sequence, chromosome sizes, chromosome
aliases and a gene track: `hg38`, `hg19`, `hs1` (T2T-CHM13v2.0), `mm10`, `mm39`, `wuhCor1`
(SARS-CoV-2), `sacCer3`, `dm6`, `ce11`, `danRer11` and `TAIR10`. Aliases such as `GRCh38`,
`GRCh37` or `GRCm39` resolve to them. Chromosome names are compared without the `chr` prefix,
so a collection that writes `1` and an assembly that writes `chr1` agree.

Any other genome is a custom assembly:

```yaml
assembly:
  name: MN908947.3
  display_name: SARS-CoV-2 Wuhan-Hu-1
  aliases: [wuhCor1, NC_045512.2]
  twobit_uri: https://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/bigZips/wuhCor1.2bit
  # or fasta_uri + fai_uri (+ gzi_uri for a bgzipped FASTA)
  chrom_sizes_uri: https://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/bigZips/wuhCor1.chrom.sizes
```

Typing a gene name in the locus box searches it on a built-in assembly. A custom assembly has
no gene search: type a locus instead.

---

## The `jbrowse` component

```yaml
- component_type: jbrowse
  workflow_tag: rnaseq
  data_collection_tag: tracks
  title: Genome browser
  track_mode: filtered        # or `all`: every track loaded, filters pick what opens
  max_tracks: 16              # tracks opened under a filter
  initial_tracks: 6           # tracks opened when nothing is filtered
  selection_enabled: true     # emit a filter back to the dashboard
  selection_mode: feature_click   # or visible_tracks
  locus_from:                 # move to the filtered rows of another collection
    data_collection_tag: variants
    chrom_column: CHROM
    start_column: POS
    sort_by: QUAL             # the call the browser opens on first
```

The main keys, all optional:

| Key | What it does |
|-----|--------------|
| `location` | The locus the browser opens on, or a gene name |
| `track_mode`, `max_tracks`, `initial_tracks` | Which tracks open: the filtered ones (or all), and how many |
| `initial_categories`, `default_tracks` | Open on these track categories, or always show these tracks |
| `locus_from` | Follow the filtered rows of another collection (see [below](#the-dashboard-drives-the-browser)) |
| `selection_enabled`, `selection_column`, `selection_mode` | Filter the dashboard from the browser (see [below](#the-browser-drives-the-dashboard)) |
| `color_by` | Colour and group the tracks by a manifest column, with the dashboard's category colours |
| `color_scale` | Colour the tracks along a sequential ramp of a manifest column (a time point, ordered by its rank) |
| `variant_color_by`, `variant_label_by` | Colour variants by a category (an effect, a caller), name them by part of an INFO field |
| `ucsc_tracks` | UCSC Genome Browser tracks opened next to the collection's own |
| `show_annotation` | The assembly's gene track |
| `show_junctions`, `read_pairs_display` | Sashimi arcs on RNA alignments; DNA alignments as pileup, arcs or cloud |
| `display` | Default display settings (scale, autoscale, colour scheme, feature mode, ...) |
| `views` | Extra views: `breakpoint` (needs `locus_from.mate`) and `circular` |
| `preset` | A configuration preset: built in (`sv-calls`, `signal`, `compact`, `peaks`) or the collection's own |
| `config_overrides` | Raw JBrowse configuration, merged last |
| `fetch_size_limit_mb`, `force_load` | The per-track download limit, and whether to lift it by default |
| `follow_window`, `auto_height` | Follow the window of other genome tiles; size the tile to its open tracks |
| `placement` | `grid` (default) or `floating`, a panel that stays on screen from tab to tab |

The component builder has a *Genome browser* type with the same settings, and a live summary
of the tracks the current filters would show.

---

## Linked to the dashboard

### The dashboard drives the browser

Dashboard filters reach the tracks collection through the project's
[links](cross-dc-filtering.md), like they reach an image gallery: filter a sample, a condition
or a cluster, and only the matching tracks open. The view is not rebuilt, so the locus stays
where it is.

With `locus_from`, the browser also moves. When the filters narrow that collection to a few
rows (a picked table row, a volcano point, a gene), the browser frames them. With no filter, it
opens on the first row in `sort_by` order: the most supported fusion, the highest quality
variant, the most significant peak. A table that drives the browser can set
`row_selection_mode: single`, so a click replaces the picked row and the browser frames one
feature, as in the clip at the top of this page.

When `locus_from` is set, the browser's toolbar also walks its regions: next and previous
region, a region picker that can be sorted and searched, and a density strip that shows where
the regions are along the genome. `rank_track: N` on `locus_from` adds a track of the N best
calls, numbered, under the gene annotation.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/ranked_rows.webp" src="../../images/guides/genome-browser/ranked_rows.mp4"></video>
  <figcaption><strong>Ranked calls.</strong> A ranked variant picked, zoomed on and clicked, then the genotypes of each family member and the reads (nf-core/raredisease dashboard template).</figcaption>
</figure>

### The browser drives the dashboard

With `selection_enabled`, a click on a feature emits a filter on `selection_column` (by default
the collection's `sample_column`), and the rest of the dashboard filters on that sample. With
`selection_mode: visible_tracks`, the set of open tracks is the selection instead. The browser
does not filter itself on its own selection, so the other tracks stay open.

A click on a feature opens depictio's own panel with the feature's fields. Hover works both
ways: a feature hovered in the browser highlights the matching points and table rows, and a
point or row hovered elsewhere draws its region as a band in the browser.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/browser_to_dashboard.webp" src="../../images/guides/genome-browser/browser_to_dashboard.mp4"></video>
  <figcaption><strong>Browser to dashboard.</strong> A variant clicked in the browser: the navigator above keeps the calls of its sample (nf-core/viralrecon dashboard template).</figcaption>
</figure>

### A navigator above the browser

A GenomeSpy [`genome_view`](components.md#advanced-visualizations) tile on the same tab is the
navigator: it draws a table (peaks, calls, regions) along the whole chromosome, and a brushed
region moves the browser there. The browser does not filter on the brushed region, so every
track stays open.

A navigator with `open_on_view_window: true` opens on the whole chromosome the browser shows,
with the browser's window drawn as a band. `interaction_mode: select` makes a drag brush a
region rather than pan the axis.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/chipseq_peaks.webp" src="../../images/guides/genome-browser/chipseq_peaks.mp4"></video>
  <figcaption><strong>Peaks to browser.</strong> The peak calls of every sample on the chromosome; zoom, brush a peak, read it in the browser (nf-core/chipseq dashboard template).</figcaption>
</figure>

<div class="grid" markdown>

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/atacseq_peaks.webp" src="../../images/guides/genome-browser/atacseq_peaks.mp4"></video>
  <figcaption>Broad ATAC calls coloured by condition (nf-core/atacseq dashboard template).</figcaption>
</figure>

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/cutandrun_peaks.webp" src="../../images/guides/genome-browser/cutandrun_peaks.mp4"></video>
  <figcaption>SEACR regions as bars, brushed into the browser (nf-core/cutandrun dashboard template).</figcaption>
</figure>

</div>

With `color_scale`, the tracks and the navigator lanes share one sequential ramp, so a time
course reads down the browser from the earliest library to the latest.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/genomespy_jbrowse.webp" src="../../images/guides/genome-browser/genomespy_jbrowse.mp4"></video>
  <figcaption><strong>A time course.</strong> Transcribed genes brushed on the lanes: the browser opens on them, every library in time order, each track on its own scale (nf-core/nascent dashboard template).</figcaption>
</figure>

### Open in genome browser

The genomic tiles of the other tabs (Manhattan, coverage, copy number, sashimi, navigator)
carry an *Open in genome browser* action. It opens the tab holding the browser on the last
point clicked, else on the region of the active region filter, else on the visible window.

---

## Tracks and their configuration

**Tracks menu.** The *Tracks* menu of the tile lists every track the view carries, grouped by
the manifest's categories, with a search, *Show all*, *Hide all* and *Back to filters*. Manual
choices hold until the filters change.

**Force load.** JBrowse stops a track at a download limit and shows a *Force load* button in
it. `fetch_size_limit_mb` sets the limit, and the *Force load* toggle of the toolbar lifts it
for every open track.

**UCSC tracks.** `ucsc_tracks` names tracks of the UCSC Genome Browser catalogue (ClinVar,
ENCODE cCREs, ARTIC primers, ...), opened next to the collection's own. Tracks backed by a
bigWig, bigBed or tabix VCF file are supported; tracks that live in UCSC's database have no file
and are reported as missing. The builder searches the catalogue by name.

<div class="grid" markdown>

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/ucsc_builder.webp" src="../../images/guides/genome-browser/ucsc_builder.mp4"></video>
  <figcaption>UCSC tracks picked in the builder.</figcaption>
</figure>

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/ucsc_and_tracks.webp" src="../../images/guides/genome-browser/ucsc_and_tracks.mp4"></video>
  <figcaption>UCSC tracks, a track's own menu, force load on the whole genome (nf-core/viralrecon dashboard template).</figcaption>
</figure>

</div>

**Display settings.** The toolbar menu groups the display settings by kind of track (view,
alignments, coverage, features, variants). `display:` sets the dashboard's defaults; each
reader's own choices are kept in their browser, and *Reset to dashboard defaults* drops them.

```yaml
display:
  autoscale: localsd   # local | global | globalsd | localsd
  summary: avg         # min | max | avg | whiskers
  color_scheme: strand # alignments: normal | mappingQuality | strand | ...
  feature_mode: compact
```

**Reads and junctions.** `show_junctions: true` draws splice junctions as arcs over the
coverage of RNA alignments; `read_pairs_display: arcs` opens DNA alignments as read arcs, which
suits a structural variant tab.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/sashimi_junctions.webp" src="../../images/guides/genome-browser/sashimi_junctions.mp4"></video>
  <figcaption><strong>Splice junctions.</strong> Cards, landscape, sashimi lanes, a locus picked and zoomed with the reads following, then the table (nf-core/rnafusion dashboard template).</figcaption>
</figure>

**Breakpoint and circular views.** `views: [breakpoint, circular]` adds two buttons to the
toolbar. The breakpoint view shows the two sides of a call (`locus_from.mate` names the second
side) joined by split reads and discordant pairs; the circular view draws the structural
variants of the tracks as chords.

<figure markdown="span">
  <video controls muted loop playsinline preload="none" poster="../../images/guides/genome-browser/fusion_chord.webp" src="../../images/guides/genome-browser/fusion_chord.mp4"></video>
  <figcaption><strong>Fusion breakpoints.</strong> Three chord links in a row: the record and both breakpoints follow each call (nf-core/rnafusion dashboard template).</figcaption>
</figure>

---

## Versions

A [version](versioning.md) preview or a dataset pin reads the tracks manifest at its pinned
commit, like any table, and so does the `locus_from` collection. The track files the manifest
names are not versioned: a file replaced under the same path shows its new content.

---

## Security and configuration

- The browser never receives a storage URL or credentials. Tracks are served through signed
  proxy URLs, and the proxy re-checks read access on the collection's project.
- Clients send track ids, never URLs: the proxy looks the file up in the collection's manifest.
- Remote files are read only from allow-listed `https://` hosts and S3 buckets; `http://` is
  refused and redirects are not followed.

| Variable | Default | Meaning |
|----------|---------|---------|
| `DEPICTIO_JBROWSE_ENABLED` | `true` | Turn the genome browser on or off |
| `DEPICTIO_JBROWSE_REMOTE_HTTPS_HOSTS` | `nf-core-awsmegatests.s3-eu-west-1.amazonaws.com` | Hosts tracks can be read from in place |
| `DEPICTIO_JBROWSE_REMOTE_S3_BUCKETS` | `nf-core-awsmegatests` | S3 buckets tracks can be read from in place |
| `DEPICTIO_JBROWSE_REMOTE_S3_ENDPOINT_URL`, `_REGION` | AWS, `eu-west-1` | The remote S3 endpoint |
| `DEPICTIO_JBROWSE_REMOTE_S3_ACCESS_KEY`, `_SECRET_KEY` | unset (anonymous) | Credentials for a private remote bucket |
| `DEPICTIO_JBROWSE_PRESET_ACCESS` | `proxy` | `direct` lets the browser read UCSC's assembly files itself |
| `DEPICTIO_JBROWSE_UCSC_TRACKS_ENABLED` | `true` | Allow `ucsc_tracks` |
| `DEPICTIO_JBROWSE_MAX_RANGE_MB`, `_MAX_FULL_READ_MB` | `64`, `256` | Caps on one ranged read and on a whole-file read |
| `DEPICTIO_JBROWSE_URL_TTL_S` | `21600` | Lifetime of a signed track URL (6 hours) |

See [Security](security.md) and the [environment reference](../installation/env-reference.md).

---

## Templates with a genome browser

| Dashboard template | Tab |
|--------------------|-----|
| [nf-core/atacseq](../pipeline-templates/nf-core/atacseq.md) 1.2.2 | Locus |
| [nf-core/chipseq](../pipeline-templates/nf-core/chipseq.md) 1.2.0 | Locus |
| [nf-core/cutandrun](../pipeline-templates/nf-core/cutandrun.md) 3.1 | Locus |
| nf-core/drop 1.0.0 | Locus |
| [nf-core/nanoseq](../pipeline-templates/nf-core/nanoseq.md) 3.0.0 | Locus |
| nf-core/nascent 2.3.0 | Genome signal |
| [nf-core/oncoanalyser](../pipeline-templates/nf-core/oncoanalyser.md) 3.0.0 | Small variants, Structural variants |
| nf-core/raredisease 3.1.2 | Locus |
| [nf-core/riboseq](../pipeline-templates/nf-core/riboseq.md) 2.0.0 | Locus |
| [nf-core/rnafusion](../pipeline-templates/nf-core/rnafusion.md) 4.1.3 | Breakpoints, Splice Junctions |
| [nf-core/rnaseq](../pipeline-templates/nf-core/rnaseq.md) 3.26.0 | Gene Explorer |
| [nf-core/rnasplice](../pipeline-templates/nf-core/rnasplice.md) 1.0.4 | Splicing Events |
| nf-core/rnavar 1.3.0 | Genome |
| [nf-core/sarek](../pipeline-templates/nf-core/sarek.md) 3.10.0, 3.11.0 | Locus |
| [nf-core/variantbenchmarking](../pipeline-templates/nf-core/variantbenchmarking.md) 1.4.0 | Germline, Structural & CNV |
| [nf-core/viralrecon](../pipeline-templates/nf-core/viralrecon.md) 3.0.0 | Variants |

The nf-core/methylseq dashboard template has no browser (its Bismark bedGraphs are not indexed),
nor does nf-core/hic (a `.hic` contact map needs a Hi-C display, not linear tracks).

---

## Limits

- JBrowse's web workers are off: track data is parsed on the page's main thread, which is fine
  for tens of open tracks.
- A view carries at most 500 tracks; only `max_tracks` of them open at once.
- Large unindexed BED and bedGraph files are refused: compress them with `bgzip` and index them
  with `tabix`.
- The track files are not versioned, only the manifest that names them.
