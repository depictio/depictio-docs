---
title: Proteins
icon: material/molecule
description: Structures, alignments and per-residue facts on a dashboard: the eight protein tiles, the tables they read, how they stay linked by residue and where the 3D model comes from.
---

# :material-molecule: Proteins <small>(v1.19.0+)</small>

Structure prediction, protein annotation and protein family pipelines publish a 3D model, the
alignment behind it and per-residue facts (confidence, secondary structure, domains,
variants). Eight [advanced visualizations](advanced-visualizations.md#proteins) draw them, and
they stay linked: pick a residue in any of them and every tile moves to it, point at a residue
and every tile marks it. Each tile has its own entry, with its settings and a YAML example, on
the [Advanced visualizations](advanced-visualizations.md#proteins) page. This page covers what
they share.

| Kind | Shows |
|------|-------|
| [`molecule_3d`](advanced-visualizations.md#molecule-3d) | The 3D model, coloured by confidence, chain, value or structure, with variants as spheres |
| [`msa`](advanced-visualizations.md#msa) | A multiple sequence alignment with consensus and conservation |
| [`sequence_track`](advanced-visualizations.md#sequence-track) | The sequence on a ruler, with a value lane, secondary structure, domains and variants |
| [`hmm_logo`](advanced-visualizations.md#hmm-logo) | The logo of a profile HMM, and where the hits of a search land on it |
| [`domain_architecture`](advanced-visualizations.md#domain-architecture) | The domains of many proteins, one row each, or grouped by architecture |
| [`secondary_structure`](advanced-visualizations.md#secondary-structure) | Helices, strands and coil with the probabilities behind them, sources compared |
| [`pae_matrix`](advanced-visualizations.md#pae-matrix) | The predicted aligned error of a model, as AlphaFold DB draws it |
| [`ramachandran`](advanced-visualizations.md#ramachandran) | The backbone torsions of the model, a quality check computed in the browser |

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

| Input | Shape |
|-------|-------|
| Structure files | `indexed_file` collection, `format: pdb` or `mmcif`, one file per entity, the sample id equal to the `entity` value. Predictors write pLDDT in the B-factor column |
| Residue table | `entity`, `position`, optionally `chain`, `residue`, `value`, `category` |
| Variants | `entity`, `position`, `ref_aa`, `alt_aa`, a consequence and a label |
| Domains | `entity`, `start`, `end`, `label`, optionally `source` |
| Alignment | `msa_id` (the `entity` it aligns), `seq_id`, `rank` (0 is the query), `aligned_sequence` |
| PAE files | `indexed_file` collection, `format: pae`: proteinfold TSV, AlphaFold DB or ColabFold JSON |

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
