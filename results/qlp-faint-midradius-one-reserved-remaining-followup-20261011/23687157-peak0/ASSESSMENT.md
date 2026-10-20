# TIC 23687157: initial review

Shallow central depression with an uneven floor and two large observing gaps.

Discovery plot visually reviewed. Refined period 1.855186767 days, depth 0.00232757, duration 0.072000 days, training sectors [91], supported events 7. Original flags retained: ['crowding_or_missing_crowding'].

Reserved sector 38: timing_prediction_inconclusive; timing spread 2.284192 days. This neither confirms nor excludes the signal. Source checks and catalog checks remain pending; no credible new planet or novelty claim.


## Initial source images

The raw sector91 stack and all11 individual usable event maps were visually reviewed. Ten maps (events0,1,2,3,7,8,9,10,11,12) show a compact relative positive feature near pixel(2,6), away from the target near(5.2,5.4). TIC23687134 (T=16.0166) lies close to that feature, with several faint neighbors nearby. Event14 is dominated by a large negative field-wide offset (roughly-330 to-380), including mixed-sign structure relative to the local background. It is retained and prevents treating the simple aggregate as a clean eclipse image.

The whole stack is negative; even its maximum formal pixel SNR is-1.04. The moment lies3.42pixels from the target and0.262pixels from23687134, but this is not an absolute positive dimming detection or a calibrated host probability. The repeated feature in the other10 individual events favors neighboring-source contamination. Unique host and physical cause remain unresolved.

Original gates retain11 events with21–31 quality-zero inside samples and62–125 baseline samples. Event3 excludes three quality128 inside samples. Events6/13 each have31 inside samples fully flagged18432/2048 and are excluded.11 raw windows are not11 independent detections; QLP supports7 events. Raw FITS SHA256:228ddc58f35312593c31e1b791f08da96f56d45651513bc6f00444f6b6275c77. The TIC cone returned297 entries. Exact processed SPOC pixel URL404 does not exclude all other possible products.

These images reuse QLP photons; the reserved-sector timing result remains inconclusive. An exact-TIC web search returned no results, which supplies no novelty evidence.


## Catalog context and disposition

The27 TIC entries within3pixels of the difference moment have27 Gaia DR2-to-DR3 mappings and27 returned source rows. There is one classifier and one eclipsing-binary row: TIC23687134 maps uniquely to Gaia DR3 6234066831682693632, classified ECL with score0.76397645. Its catalog frequency0.010373496194980457/day gives period96.399515days, which does not match the1.855187-day TESS fit. This is a known-variable neighbor at the recurring image feature, not a verified period/epoch match or proof that the cataloged eclipse causes the TESS signal. All mappings, raw CSV/JSON equality and identity/period arithmetic were audited.

Initial source inspection is complete. Neighbor contamination is favored, but exact source and physical explanation remain unresolved, particularly given the Gaia-period mismatch and extreme final event. A planet around the target is not supported by these source images. No credible new planet is claimed.
