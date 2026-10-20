# TIC196681132 recovers a previously reported eclipsing binary

TIC196681132 is EPIC212601505, listed in the eclipsing-binary table of
[Crossfield et al. (2018), arXiv:1806.03127](https://arxiv.org/pdf/1806.03127).
The downloaded preprint labels this **Table 4**, spanning multiple pages.
This removes the source from our priority list for new planet candidates.
It does not constitute a new measurement of companion mass or an orbital solution.

The EPIC and TIC records share both **2MASS13303399-1033194** and
**UCAC4 398-055708**. Their unpropagated catalog positions differ by only
0.174 arcsec. The identification is therefore supported by exact cross-identifiers,
not merely a match to the rounded VSX position.

| Measurement | Published K2 row | Our TESS fit |
|---|---:|---:|
| Period (days) | 0.724453 | 0.7244717005 |
| Duration (days) | 0.035719 | 0.032 |
| Depth / squared radius ratio | 0.020973 | 0.0197392 |

The period difference is 1.616 seconds; these are similar measurements, not
identical ephemerides. No cycle-count or dynamical inference is made. The paper
lists epoch2458179.96618 BJD_TDB and Kp14.486. Our independently retrieved ZTF
roughly2.1% dimming supports recovery of the known variable, not planet novelty.

VSX identifies EPIC212601505 (OID625667) as **EA:**, where the colon marks
an uncertain classification, with period0.72436144 days. That differs from
our TESS fit by9.527 seconds. The published EB listing is stronger provenance
for prior reporting than our earlier exact-TIC nonmatches in planet catalogs.
Those narrower nonmatches never ruled out a known K2 variable.

The same successful60-arcsec VSX queries return no rows for TIC241928959 or
TIC422626648. Neither result establishes novelty or excludes a binary. Their
sparse ZTF checks remain inconclusive; TIC422626648 retains the Gaia RV concern.

## Evidence and verification

`plan.json`, `results.json`, `paper-source.json`, and
`epic-source-corrected.json` retain queries, URLs, raw paths and SHA-256 hashes.
`verify.py` checks all five raw hashes, the two exact cross-identifiers and
published period row; `verification.json` records successful calculations.
The cached paper text was extracted with `pdftotext -layout`; its table heading
and row were inspected. No scientific search algorithm changed in this review.

The initial EPIC query incorrectly used column `EPIC` and returned HTTP400;
`epic-source.json` preserves it. The corrected query uses catalog column `ID`.
An earlier USQ paper download returned HTTP403 and the direct AAVSO detail page
could not be opened; the successful primary arXiv PDF and CDS catalog responses
provide the evidence used here.

Earlier assessments remain as a historical record. Their promising/new-signal
interpretations for TIC196681132 are superseded by this identity check.
Future triage should include VSX and K2 identifiers before extensive follow-up.
