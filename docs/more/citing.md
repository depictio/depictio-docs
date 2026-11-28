---
title: "Citing Depictio"
icon: material/format-quote-close
description: "How to cite Depictio in a publication: the software, its version, and a ready-to-use BibTeX entry."
---

# Citing Depictio

If Depictio helped your work, please cite it. Always give the **version** you used (`depictio --version` prints it), so others can reproduce your dashboards.

## Software citation

> Weber, T. *Depictio* (version X.Y.Z). European Molecular Biology Laboratory (EMBL). <https://github.com/depictio/depictio>

```bibtex
@software{depictio,
  author  = {Weber, Thomas},
  title   = {Depictio},
  version = {X.Y.Z},
  url     = {https://github.com/depictio/depictio},
  license = {MIT},
  note    = {European Molecular Biology Laboratory (EMBL)}
}
```

The repository's **Cite this repository** button (GitHub, right sidebar) gives the same reference in APA and BibTeX, from its [`CITATION.cff`](https://github.com/depictio/depictio/blob/main/CITATION.cff).

## Cite the pipelines too

A dashboard built from a [pipeline template](../pipeline-templates/README.md) shows the results of that pipeline: cite it as well, following its own guidelines (for nf-core, the pipeline's DOI and the [nf-core paper](https://doi.org/10.1038/s41587-020-0439-x)).
