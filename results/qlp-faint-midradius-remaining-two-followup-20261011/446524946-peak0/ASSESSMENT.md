# TIC 446524946: likely cataloged-binary contamination

Training sectors [36, 37]. Native refinement: period 1.114581039 days, duration 0.133056 days, depth 107859 ± 394 ppm (formal selected-fit error), 28 supported events. Original flags: crowding_or_missing_crowding.

Visually inspected discovery plot: Very deep, broad rounded eclipse, about 15 percent at the bottom of the seed-period folded plot. This raises a strong eclipsing-system or contamination concern; source and host unresolved. The displayed plot uses the discovery seed; the native refinement above differs slightly.

Sector 9: recovered_at_frozen_ephemeris_requires_further_vetting, timing spread 0.0371 days. Fixed-ephemeris depth 95992 ± 709 ppm, 15 supported events. Sector 10: recovered_at_frozen_ephemeris_requires_further_vetting, timing spread 0.0361 days. Fixed-ephemeris depth 98482 ± 636 ppm, 15 supported events.

Inconclusive timing neither confirms nor reliably rejects recurrence. The source and catalog checks below supersede the initial pending status; full quality and host validation is incomplete. No secure host, novelty, or credible planet claim.

Training-only off-phase scan selects phase 0.573529, depth 512 ± 574 ppm, formal SNR 0.89, 0 supported events. This maximum over phase and duration has uncalibrated significance; it does not establish a secondary eclipse.

The two reserved sectors were not previously cached according to the frozen manifest. Their recurrence supports a persistent eclipsing signal, without establishing planetary origin or its host. The shallow off-phase maximum does not rule out a binary at this period or a period alias.

## Source check

Raw sector-36 and sector-37 difference images include 22 and 21 events. Both plots were visually inspected: each shows a compact positive feature displaced from the target toward TIC 446692470 and unresolved neighbors. Diagnostic target offsets are 2.205 and 2.238 pixels; TIC 446692470 is closest to the moments at 0.114 and 0.232 pixels. Fainter sources, including TIC 863677640, remain unresolved. These images support contamination, without calibrated PRF confidence or a unique-source proof. The raw images share photons with QLP and use temporal subtraction without a full background model.

Both exact processed TESS-SPOC pixel requests returned HTTP 404; errors and URLs are preserved, not interpreted as nondetections. Source provenance verification passed in `verify_pixels.py` / `source_review.json`.

The Gaia query covers 12 selected TIC sources. It returns 14 DR2-to-DR3 neighborhood mappings and 12 unique DR3 sources; two distant cross-links are preserved as ambiguous mappings, not assumed physical associations. The closest bright neighbor TIC 446692470 has a direct mapping to DR3 5357965212082497280, classified ECL and listed with eclipsing-binary period 2.229088455 days. Half that period is 1.114544228 days, differing from the QLP period by -3.18 seconds. This spatial and approximate half-period agreement strongly favors contamination by a cataloged eclipsing binary. A joint epoch/model match and calibrated attribution remain undone. Independent-sector recurrence establishes a persistent signal, not a planet on the target. Catalog request/results/provenance are in `../../gaia-446524946-neighbors-20261011/`.
