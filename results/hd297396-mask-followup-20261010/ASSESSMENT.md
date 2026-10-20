# HD297396: spectral mask and RV coherence sensitivity

One exposure,2012-12-27T06:34:44.521, used maskG2; the other107 useK5.
It differs by approximately49m/s between RV reductions after their median
pre-upgrade offset is removed. Its SNR is67.8, so a simple low-SNR cut would not
address the discrepancy. Metadata and the full row are preserved.

Mask-dependent zero points are a legitimate instrument concern: see
[HARPS mask documentation](https://support.eso.org/en-US/kb/articles/harps-how-to-get-the-pipeline-generated-files-ccf-s1d-e2ds-bis-int-guide)
and [Gaia RV standards analysis](https://academic.oup.com/mnras/article/517/2/1849/6711702).
This motivates a sensitivity test, not declaring the exposure erroneous.

The new optional ingestion mode bins separately by night, mask and pre/post-fiber
configuration. A distinct fitted offset absorbs the singletonG2 point; this is
mathematically similar to removing its constraint on orbital parameters. It is
post-hoc, not an independently calibrated correction. Original results remain.

With original fixed RV periods and separate mask offsets, the13-night original
late-sample component improvement for4.2689d is+2.23(SERVAL) and-3.01(DRS), versus
+10.80/-15.98 originally. Adding the knownTOI3.0178746d sinusoid gives-0.61/-6.30.
The new three-block comparisons are more consistent, but they overlap the already
opened data and do not provide fresh validation. Fixed2m/s white jitter persists.

The previously excluded14post-upgrade nights can test the predicted temporal
shape if only a constant instrumental offset is fitted in that test set. This
post-hoc conditional test yields-10.86(SERVAL) and+5.35(DRS) without the knownTOI
term, and-3.07/+13.38 with it. Periods, phases, amplitudes and trend stay trained
on the original earlier data. The reductions still disagree; no likelihood-ratio
significance or planet validation follows.

A mask audit finds three mixed-mask targets in the32-star cohort: GJ9255,
HD297396 andHD85512. Their mask-aware re-screen is archived separately in
../rv-mask-rescreen-20261010; it produces no new promoted candidate. Repeated use
of previously opened validation nights is labeled retrospective.
