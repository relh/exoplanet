# CHEOPS archive metadata

**Neither candidate has a returned visit in the bounded coordinate search.** Anonymous queries of the official CHEOPS Archive Browser used 120-arcsec cones around TIC 80387959 and TIC 402358350, with all proprietary statuses, latest versions and no date restrictions. Both submissions returned HTTP 200 and completed results tables explicitly showing zero entries. No light curves, science images or spectra were opened.

| Target | Cone center, degrees | Returned visits | Implication |
|---|---|---:|---|
| TIC 80387959 | 165.31057513947022, −48.613881428659525 | 0 | No timing or source-attribution experiment identified through this query |
| TIC 402358350 | 295.15092862046833, +15.640411694115707 | 0 | No independent ephemeris-recovery observation identified through this query |

The centers are the retained Gaia DR3 positions; the interface labels its inputs J2000, while these source coordinates refer to Gaia epoch 2016. No proper-motion correction was applied. The stated result is strictly for these entered cones. This is a target-position search, not a detector-footprint census: observations centered outside 120 arcsec, unindexed products and future observations are not excluded. An archive nonmatch says nothing about whether a planet exists.

The separately frozen [positive control](control-plan.json) used WASP-189, a documented [CHEOPS science target](https://www.esa.int/Science_Exploration/Space_Science/Cheops/First_results_from_Cheops_ESA_s_exoplanet_observer_reveals_extreme_alien_world). The archive resolved its coordinates to 225.686950, −3.03139 degrees. Clearing the name and submitting the same coordinate-only 120-arcsec query returned **eight public visits**. This verifies that the anonymous workflow can return observations; it does not prove archive completeness. The [control metadata](control-summary.json) retains all eight rows.

## Method and verification

The [frozen plan](plan.json) predates both submissions. The official [archive help](https://cheops.unige.ch/archive_browser/index.php/tutorial/) specifies degree units for RA, Dec and radius, describes the proprietary-status filter and latest-version selection, and documents anonymous queries. [Summary](summary.json) preserves exact request fields, request times, response dates and displayed counts; [provenance](provenance.json) records saved payloads and rendered result HTML with SHA-256 hashes. Raw browser captures remain in ignored `data/cheops-metadata-20261013/`.

The initially supplied help URL omitted `/archive_browser/` and returned 404; the corrected linked URL returned 200. Web-tool access also failed, while the local HTTP/browser route succeeded. A browser wait for different empty-result wording timed out; the same live session subsequently completed and explicitly showed zero entries. These access failures were not converted into nonmatches. The first verifier matched an example file key in a hidden help template; the retained [initial verification](verification-initial.json) records that failure. The corrected verifier limits observation-link checks to the actual results table.

Run `python3 results/cheops-metadata-20261013/verify.py` to check the frozen plan, identities, entered coordinates, radius conversion, timestamps, unrestricted filters, response status, displayed counts and raw hashes. These checks establish provenance and query behavior, not archive completeness or astrophysical classification.
