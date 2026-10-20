# TIC 310128088: retrospective diagnostic

Native refinement gives period 14.645747172 days, with only two
supported training events. Both reserved-sector checks are timing-inconclusive,
not confirmations or rejections. Files were not cached at freezing; this is
nevertheless a retrospective application of a later diagnostic policy.

Discovery plot visually reviewed: Large excursions near the ends of observing segments dominate the deep folded feature.
Original flags remain binding. No source-attribution check has been completed.
This signal is retained as unresolved diagnostic evidence, not a credible new
planet candidate. Secondary scans are exploratory and not calibrated significance.

## Pixel and quality review

Sector 11 contains both native events. Each has five in-event processed-pixel
cadences, all quality 12288 (4096 + 8192); each local baseline also has zero
quality-zero cadences. Thus the unchanged image gate yields zero usable events.
The TESS quality definitions identify these as automatic stray-light and planet
search exclusion flags:
https://lightkurve.github.io/lightkurve/_modules/lightkurve/utils.html .
This product's flags need not match QLP's flags.

The raw 11x11 TESScut permits two image windows under its quality flags, but
the visually reviewed difference is broad across the valid stamp rather than
a compact source. The formal peak SNR49 and moment offset4.88pixels are not
host evidence. Several rows have no finite image data; plotted zero differences
there are the routine's empty-weight output, not measured zero flux changes.
Both background-plane checks fail with zero available background pixels after
catalog-source masking; no background-corrected localization is obtained.

Combined evidence makes this an artifact-suspect diagnostic, not a credible
planet candidate. Exact physical cause and host remain undetermined. Reserved
timing remains inconclusive, not a planet rejection. No image-quality gate was
relaxed. Raw images and processed pixels share the same observing epoch.

Evidence: ../../spoc-pixels-310128088-s11-20261011/coverage.json and
../../tesscut-310128088-s11-20261011/analysis.json, difference.png,
background.json. The initial copied-path failure is retained separately.
