# Proteins (v1.19.0+)

Structure prediction, protein annotation and protein family pipelines publish a 3D model, the alignment behind it and per-residue facts (confidence, secondary structure, domains, variants). Eight [advanced visualizations](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#proteins) draw them, and they stay linked: pick a residue in any of them and every tile moves to it, point at a residue and every tile marks it. Each tile has its own entry, with its settings and a YAML example, on the [Advanced visualizations](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#proteins) page. This page covers what they share.

[3D structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#molecule-3d "Jump to 3D structure") v1.19.0+

[Sequence track](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#sequence-track "Jump to Sequence track") v1.19.0+

[Alignment](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#msa "Jump to Alignment") v1.19.0+

[HMM logo](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#hmm-logo "Jump to HMM logo") v1.19.0+

[Domain architecture](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#domain-architecture "Jump to Domain architecture") v1.19.0+

[Secondary structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#secondary-structure "Jump to Secondary structure") v1.19.0+

[Predicted aligned error](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#pae-matrix "Jump to Predicted aligned error") v1.19.0+

[Ramachandran](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#ramachandran "Jump to Ramachandran") v1.19.0+

The nf-core [proteinfamilies](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/proteinfamilies/index.md), [proteinannotator](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/proteinannotator/index.md) and [proteinfold](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/proteinfold/index.md) templates are built on them, and [sarek](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/sarek/index.md) and [oncoanalyser](https://depictio.github.io/depictio-docs/latest/pipeline-templates/nf-core/oncoanalyser/index.md) draw coding variants on a predicted structure.

______________________________________________________________________

## The data

Every protein tile reads tables joined on two column names: `entity` (which protein) and `position` (the 1-based residue number in the structure's numbering). A tile shows one entity at a time: the one the filters name, else the reader's pick, else the first.

| Input               | Shape                                                                                                                                                              | Read by                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Structure files** | `indexed_file` collection, `format: pdb` or `mmcif`, one file per entity, the sample id equal to the `entity` value. Predictors write pLDDT in the B-factor column | [3D structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#molecule-3d), [Ramachandran](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#ramachandran)                                                                                                                                                                                                                                                                                                                                                                            |
| **Residue table**   | `entity`, `position`, optionally `chain`, `residue`, `value`, `category`                                                                                           | [3D structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#molecule-3d), [Sequence track](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#sequence-track), [Secondary structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#secondary-structure), [Predicted aligned error](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#pae-matrix), [Ramachandran](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#ramachandran) |
| **Variants**        | `entity`, `position`, `ref_aa`, `alt_aa`, a consequence and a label                                                                                                | [3D structure](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#molecule-3d), [Sequence track](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#sequence-track)                                                                                                                                                                                                                                                                                                                                                                        |
| **Domains**         | `entity`, `start`, `end`, `label`, optionally `source`                                                                                                             | [Sequence track](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#sequence-track), [Domain architecture](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#domain-architecture)                                                                                                                                                                                                                                                                                                                                                         |
| **Alignment**       | `msa_id` (the `entity` it aligns), `seq_id`, `rank` (0 is the query), `aligned_sequence`                                                                           | [Alignment](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#msa)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **PAE files**       | `indexed_file` collection, `format: pae`: proteinfold TSV, AlphaFold DB or ColabFold JSON                                                                          | [Predicted aligned error](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#pae-matrix)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

The helpers in `depictio/recipes/lib/` (`protein_structure`, `msa`, `hmm`, `secondary_structure`, `pae`) build these tables. See [Recipes](https://depictio.github.io/depictio-docs/latest/usage/projects/recipes/index.md).

______________________________________________________________________

## Linked by residue

- **A pick is a filter.** A click or brush emits a `residue_selection`: the entity, a `position` range and, on a complex, the chain. Every table with those columns narrows, and every protein tile shows the range. The last gesture wins.
- **A hover is not.** Pointing at a residue marks it in every protein tile, in the browser only.
- v1.19.1+ **Zoom can follow.** Turn on the sync icon of a tile, or a section's button, and the other residue tiles and the 3D model follow its zoom.
- A [lollipop](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#lollipop) joins with `selection_enabled: true`, a [profile](https://depictio.github.io/depictio-docs/latest/features/advanced-visualizations/#profile) with `residue_axis: true`. Cards and figures that do not draw the position column ignore the range.

## Where the structure comes from

`structure_source: file` reads the run's own files and makes no outbound call. The browser fetches them from S3 through presigned URLs, or through the API with [`DEPICTIO_S3_BROWSER_ACCESS=proxy`](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#s3-browser-access) (v1.22.0+) when browsers cannot reach S3 (the tile otherwise fails with *Failed to fetch*). `structure_source: resolve` asks the server for a model by UniProt accession, by gene and taxon, or by sequence. The resolver is off until `DEPICTIO_STRUCTURE_RESOLVER_ENABLED=true`, and tries, first hit wins:

1. its cache in the instance bucket;
1. AlphaFold DB, by accession;
1. UniProt, gene and taxon to an accession, then AlphaFold DB;
1. ESMFold, for a sequence of at most 400 residues.

The tile credits the service it used. A `pae_matrix` has no resolver path. See [External structure services](https://depictio.github.io/depictio-docs/latest/features/security/#structure-resolver) for what leaves the server and the [environment reference](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#structure-resolver) for the settings.

## Numbering mismatch

A variant table and a model do not always number residues alike (a construct, an isoform, an off-by-one). A variant whose `ref_aa` disagrees with the model is listed under a *numbering mismatch* badge instead of being drawn on the wrong residue; one past the end of the model is counted under *outside the model*.
