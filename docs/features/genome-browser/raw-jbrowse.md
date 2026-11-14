---
title: "Genome browser: Raw JBrowse configuration"
icon: material/code-json
description: Any JBrowse setting or track, merged last.
glightbox: true
---

# Raw JBrowse configuration

`config_overrides` passes JBrowse configuration as it is: per-format displays, per-track settings, extra tracks. An extra track is fetched by the browser itself, so its host must send CORS headers and be allowed by the instance's Content Security Policy.

```yaml
# on the jbrowse component
config_overrides:
  formats:
    bam: {displays: [{type: LinearAlignmentsDisplay, height: 80}]}
  extra_tracks:
    - type: FeatureTrack
      trackId: regions
      name: Regions of interest
      adapter:
        type: BedTabixAdapter
        bedGzLocation: {uri: "https://data.example.org/regions.bed.gz"}
        index: {location: {uri: "https://data.example.org/regions.bed.gz.tbi"}}
```

[:material-arrow-left: All examples](index.md#examples)
