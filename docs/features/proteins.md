---
title: Proteins
icon: material/molecule
description: "Structures, alignments and per-residue facts on a dashboard: the eight protein tiles, the tables they read, how they stay linked by residue and where the 3D model comes from."
---

# :material-molecule: Proteins <small>(v1.19.0+)</small>

Structure prediction, protein annotation and protein family pipelines publish a 3D model, the
alignment behind it and per-residue facts (confidence, secondary structure, domains,
variants). Eight [advanced visualizations](advanced-visualizations.md#proteins) draw them, and
they stay linked: pick a residue in any of them and every tile moves to it, point at a residue
and every tile marks it. Each tile has its own entry, with its settings and a YAML example, on
the [Advanced visualizations](advanced-visualizations.md#proteins) page. This page covers what
they share.

<div class="viz-bento" markdown>

<div class="viz-grid" markdown>

<div class="viz-tile viz-tile--f" markdown>
[![3D structure](../images/guides/advanced-visualizations/thumbs/molecule_3d_light.webp#only-light){ width=960 height=720 loading=lazy decoding=async }](../images/guides/advanced-visualizations/molecule_3d_light.webp){ .glightbox data-type="image" data-title="3D structure" data-gallery="proteins-light" data-desc-position="bottom" }
[![3D structure](../images/guides/advanced-visualizations/thumbs/molecule_3d_dark.webp#only-dark){ width=960 height=720 loading=lazy decoding=async }](../images/guides/advanced-visualizations/molecule_3d_dark.webp){ .glightbox data-type="image" data-title="3D structure" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[3D structure](advanced-visualizations.md#molecule-3d){ .viz-tile__name title="Jump to 3D structure" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--w" markdown>
[![Sequence track](../images/guides/advanced-visualizations/thumbs/sequence_track_light.webp#only-light){ width=960 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/sequence_track_light.webp){ .glightbox data-type="image" data-title="Sequence track" data-gallery="proteins-light" data-desc-position="bottom" }
[![Sequence track](../images/guides/advanced-visualizations/thumbs/sequence_track_dark.webp#only-dark){ width=960 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/sequence_track_dark.webp){ .glightbox data-type="image" data-title="Sequence track" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Sequence track](advanced-visualizations.md#sequence-track){ .viz-tile__name title="Jump to Sequence track" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![Alignment](../images/guides/advanced-visualizations/thumbs/msa_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/msa_light.webp){ .glightbox data-type="image" data-title="Alignment" data-gallery="proteins-light" data-desc-position="bottom" }
[![Alignment](../images/guides/advanced-visualizations/thumbs/msa_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/msa_dark.webp){ .glightbox data-type="image" data-title="Alignment" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Alignment](advanced-visualizations.md#msa){ .viz-tile__name title="Jump to Alignment" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![HMM logo](../images/guides/advanced-visualizations/thumbs/hmm_logo_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/hmm_logo_light.webp){ .glightbox data-type="image" data-title="HMM logo" data-gallery="proteins-light" data-desc-position="bottom" }
[![HMM logo](../images/guides/advanced-visualizations/thumbs/hmm_logo_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/hmm_logo_dark.webp){ .glightbox data-type="image" data-title="HMM logo" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[HMM logo](advanced-visualizations.md#hmm-logo){ .viz-tile__name title="Jump to HMM logo" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![Domain architecture](../images/guides/advanced-visualizations/thumbs/domain_architecture_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/domain_architecture_light.webp){ .glightbox data-type="image" data-title="Domain architecture" data-gallery="proteins-light" data-desc-position="bottom" }
[![Domain architecture](../images/guides/advanced-visualizations/thumbs/domain_architecture_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/domain_architecture_dark.webp){ .glightbox data-type="image" data-title="Domain architecture" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Domain architecture](advanced-visualizations.md#domain-architecture){ .viz-tile__name title="Jump to Domain architecture" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![Secondary structure](../images/guides/advanced-visualizations/thumbs/secondary_structure_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/secondary_structure_light.webp){ .glightbox data-type="image" data-title="Secondary structure" data-gallery="proteins-light" data-desc-position="bottom" }
[![Secondary structure](../images/guides/advanced-visualizations/thumbs/secondary_structure_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/secondary_structure_dark.webp){ .glightbox data-type="image" data-title="Secondary structure" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Secondary structure](advanced-visualizations.md#secondary-structure){ .viz-tile__name title="Jump to Secondary structure" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![Predicted aligned error](../images/guides/advanced-visualizations/thumbs/pae_matrix_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/pae_matrix_light.webp){ .glightbox data-type="image" data-title="Predicted aligned error" data-gallery="proteins-light" data-desc-position="bottom" }
[![Predicted aligned error](../images/guides/advanced-visualizations/thumbs/pae_matrix_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/pae_matrix_dark.webp){ .glightbox data-type="image" data-title="Predicted aligned error" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Predicted aligned error](advanced-visualizations.md#pae-matrix){ .viz-tile__name title="Jump to Predicted aligned error" } <span class="ver-badge">v1.19.0+</span></span>
</div>

<div class="viz-tile viz-tile--s" markdown>
[![Ramachandran](../images/guides/advanced-visualizations/thumbs/ramachandran_light.webp#only-light){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/ramachandran_light.webp){ .glightbox data-type="image" data-title="Ramachandran" data-gallery="proteins-light" data-desc-position="bottom" }
[![Ramachandran](../images/guides/advanced-visualizations/thumbs/ramachandran_dark.webp#only-dark){ width=480 height=360 loading=lazy decoding=async }](../images/guides/advanced-visualizations/ramachandran_dark.webp){ .glightbox data-type="image" data-title="Ramachandran" data-gallery="proteins-dark" data-desc-position="bottom" }
<span class="viz-tile__cap">[Ramachandran](advanced-visualizations.md#ramachandran){ .viz-tile__name title="Jump to Ramachandran" } <span class="ver-badge">v1.19.0+</span></span>
</div>

</div>

The nf-core [proteinfamilies](../pipeline-templates/nf-core/proteinfamilies.md),
[proteinannotator](../pipeline-templates/nf-core/proteinannotator.md) and
[proteinfold](../pipeline-templates/nf-core/proteinfold.md) templates are built on them, and
[sarek](../pipeline-templates/nf-core/sarek.md) and
[oncoanalyser](../pipeline-templates/nf-core/oncoanalyser.md) draw coding variants on a
predicted structure.

---

## The data { #the-data }

Every protein tile reads tables joined on two column names: `entity` (which protein) and
`position` (the 1-based residue number in the structure's numbering). A tile shows one entity
at a time: the one the filters name, else the reader's pick, else the first.

| Input | Shape | Read by |
|-------|-------|---------|
| :material-molecule: **Structure files** | `indexed_file` collection, `format: pdb` or `mmcif`, one file per entity, the sample id equal to the `entity` value. Predictors write pLDDT in the B-factor column | [3D structure](advanced-visualizations.md#molecule-3d), [Ramachandran](advanced-visualizations.md#ramachandran) |
| :material-table: **Residue table** | `entity`, `position`, optionally `chain`, `residue`, `value`, `category` | [3D structure](advanced-visualizations.md#molecule-3d), [Sequence track](advanced-visualizations.md#sequence-track), [Secondary structure](advanced-visualizations.md#secondary-structure), [Predicted aligned error](advanced-visualizations.md#pae-matrix), [Ramachandran](advanced-visualizations.md#ramachandran) |
| :material-map-marker-alert-outline: **Variants** | `entity`, `position`, `ref_aa`, `alt_aa`, a consequence and a label | [3D structure](advanced-visualizations.md#molecule-3d), [Sequence track](advanced-visualizations.md#sequence-track) |
| :material-view-sequential-outline: **Domains** | `entity`, `start`, `end`, `label`, optionally `source` | [Sequence track](advanced-visualizations.md#sequence-track), [Domain architecture](advanced-visualizations.md#domain-architecture) |
| :material-text-box-outline: **Alignment** | `msa_id` (the `entity` it aligns), `seq_id`, `rank` (0 is the query), `aligned_sequence` | [Alignment](advanced-visualizations.md#msa) |
| :material-grid: **PAE files** | `indexed_file` collection, `format: pae`: proteinfold TSV, AlphaFold DB or ColabFold JSON | [Predicted aligned error](advanced-visualizations.md#pae-matrix) |

The helpers in `depictio/recipes/lib/` (`protein_structure`, `msa`, `hmm`,
`secondary_structure`, `pae`) build these tables. See [Recipes](../usage/projects/recipes.md).

---

## Linked by residue { #residue-selection }

![Protein tiles linked by residue: one range is shown by every tile, a pick leaves the browser as a filter on the tables, a hover stays in it](../images/guides/protein-tiles/schema_residue_linking_light.png#only-light){ loading=lazy }
![Protein tiles linked by residue: one range is shown by every tile, a pick leaves the browser as a filter on the tables, a hover stays in it](../images/guides/protein-tiles/schema_residue_linking_dark.png#only-dark){ loading=lazy }

- **A pick is a filter.** A click or brush emits a `residue_selection`: the entity, a
  `position` range and, on a complex, the chain. Every table with those columns narrows, and
  every protein tile shows the range. The last gesture wins.
- **A hover is not.** Pointing at a residue marks it in every protein tile, in the browser only.
- <span class="ver-badge">v1.19.1+</span> **Zoom can follow.** Turn on the sync icon of a
  tile, or a section's button, and the other residue tiles and the 3D model follow its zoom.
- A [lollipop](advanced-visualizations.md#lollipop) joins with `selection_enabled: true`, a [profile](advanced-visualizations.md#profile) with
  `residue_axis: true`. Cards and figures that do not draw the position column ignore the range.

## Where the structure comes from { #structure-resolver }

![The 3D model comes from a file of the run, or from the resolver: bucket cache, AlphaFold DB, UniProt, ESMFold](../images/guides/protein-tiles/schema_structure_resolver_light.png#only-light){ loading=lazy }
![The 3D model comes from a file of the run, or from the resolver: bucket cache, AlphaFold DB, UniProt, ESMFold](../images/guides/protein-tiles/schema_structure_resolver_dark.png#only-dark){ loading=lazy }

`structure_source: file` reads the run's own files and makes no outbound call.
`structure_source: resolve` asks the server for a model by UniProt accession, by gene and
taxon, or by sequence. The resolver is off until `DEPICTIO_STRUCTURE_RESOLVER_ENABLED=true`,
and tries, first hit wins:

1. its cache in the instance bucket;
2. AlphaFold DB, by accession;
3. UniProt, gene and taxon to an accession, then AlphaFold DB;
4. ESMFold, for a sequence of at most 400 residues.

The tile credits the service it used. A `pae_matrix` has no resolver path. See
[External structure services](security.md#structure-resolver) for what leaves the server and
the [environment reference](../installation/env-reference.md#structure-resolver) for the settings.

## Numbering mismatch { #numbering-mismatch }

A variant table and a model do not always number residues alike (a construct, an isoform, an
off-by-one). A variant whose `ref_aa` disagrees with the model is listed under a *numbering
mismatch* badge instead of being drawn on the wrong residue; one past the end of the model is
counted under *outside the model*.
