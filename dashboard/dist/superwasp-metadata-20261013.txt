# SuperWASP archive availability

**Neither candidate has a useful independent transit test in this bounded archive screen.** The first target has only seven cataloged measurements during 37.47 minutes. The second has no returned source within 120 arcseconds. No epoch flux was opened, and neither result changes the candidate classification.

| Cone | Returned sources | Relevant coverage | Assessment |
|---|---:|---|---|
| TIC 80387959 | 12 | Nearest source: 7 points; HJD UTC 2453922.203634–2453922.229653 | Too short to establish recurrence or an event baseline; catalog scatter 0.1692 mag |
| TIC 402358350 | 0 | Official search resolved the input coordinate and explicitly reported no data in this region | Bounded archive nonmatch; not evidence against a planet |
| Documented control | 9 | Exact example 1SWASP J063954.26+353125.7: 4,965 points over 1,327.624132 days | Verifies the same public search route returns long series |

The 80387959 nearest entry, **1SWASP J110114.50-483649.2**, lies 0.831 arcseconds from the retained Gaia J2016 coordinate. This positional association does not establish an isolated photometric source. Its catalog WASP magnitude is 11.28537; median TAMMAG2 is 11.23959 mag. All twelve returned entries have only six or seven points in the same approximately 37.47-minute interval, so none supplies a long neighbor series. Separate source IDs do not demonstrate resolved, independent apertures. No PSF, aperture response, saturation or signal sensitivity was calibrated here. A 0.1692-mag catalog scatter is not an estimate of achievable transit precision after arbitrary detrending, but these seven points cannot provide repeated-event evidence at the 4.19-day clock. Downloading their flux is not justified by this objective.

## Method and access limitations

The [frozen plan](plan.json) specifies metadata-only 120-arcsecond cones at retained Gaia J2016 positions, all sources regardless of brightness, and a documented positive control. Positions are not propagated to the WASP epoch; the cone is much wider than the known proper-motion displacement. [Queries](queries.json) preserve the exact selected columns. The initial TAP schema query successfully identified `superwasptimeseries`, but all three spatial queries returned HTTP 403 Cloudflare blocks. These errors are retained and are **not** nonmatches.

The planned fallback used the [official search form](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblSearch/nph-tblSearchInit?app=ExoTbls&config=superwasptimeseries) with the same coordinates/radius and no added column constraints. The 803 and control tables show all 12 and 9 results respectively; their complete rendered metadata are retained. The 402 query returned HTTP 200 XML explicitly stating that the input resolves to the requested location but no data were found in that region. The browser automatically dismissed that alert, prompting two redundant identical submissions before inspecting the saved network body. The retained 402 form captures are not result tables; `ui-402358350-network.json` is its authoritative result. No authentication, CAPTCHA bypass or security-filter evasion was attempted.

The [official documentation](https://exoplanetarchive.ipac.caltech.edu/docs/SuperWASPUsage.html) supplies the positive-control identifier. Its successful recovery verifies query functionality and metadata parsing, not completeness of the survey or sensitivity around either candidate. The search page describes this archive as the 2004–2008 public release. These results do not cover all WASP observations ever collected or establish physical absence. The metadata use HJD UTC, not the TESS BJD TDB clock. No timing conversion, event test or dip fit is claimed. A separate old-epoch timing assessment retains the backward extrapolation limitations.

## Reproducibility

[summary.json](summary.json) retains every returned row and spherical separations. [manifest.json](manifest.json) records HTTP requests, errors, timestamps and SHA-256 values for saved documentation and TAP responses. [browser-manifest.json](browser-manifest.json) records UI metadata captures, source URLs, request timestamps and hashes. Raw files remain in ignored `data/superwasp-metadata-20261013/`. `summarize.py` parses saved metadata only; it performs no downloads. `verify.py` checks frozen hashes, source counts, cone geometry, relevant metadata and error/nonmatch distinction. Passing these checks does not validate a planet.

The [independent review](../old-epoch-timing-20261013/REVIEW-superwasp.md) reproduces the metadata and provenance checks. It does not establish photometric sensitivity or a planetary/nonplanetary classification.
