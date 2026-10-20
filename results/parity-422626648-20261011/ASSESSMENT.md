# TIC422626648: alternating depths strengthen the binary interpretation

**Status: binary-suspect target-region signal; deprioritize as a new planet lead.**
The fixed fitted period is4.095345849 days. Even and odd dips have different
depths in both tested QLP detrending windows:

| Window | Even depth | Odd depth | Difference / formal error |
|---|---:|---:|---:|
| 1.5 days | 0.9268% | 0.5418% | 3.64 |
| 2.5 days | 0.9241% | 0.5415% | 3.62 |

Each family has only two usable measured QLP events. Their centers correspond
to original-clock even events0,4 and odd events3,5. The event labels inside the
saved family measurements use their respective2P clocks and must not be confused
with original-clock numbering. Not all six raw-image events survive this QLP
measurement path. The reported totals contain34 in-window measurements per family.

The descriptive event-scatter ratios are5.78 and5.83, but two events per family
cannot calibrate a reliable significance against time-correlated systematics.
Formal errors likewise omit correlated noise. These are post-inspection checks
of the same sector, not independent validation or formal classification odds.

All six previously reconstructed raw-image target amplitudes show the same
alternation: even-event mean19.53 versus odd-event mean10.43 in template units,
with three events each. `raw-amplitude-parity.json` records the inputs, source hash
and descriptive calculation. These amplitudes are not fractional depths; the
comparison uses fixed registration and a fitted background plane. It is another
reduction of the same observations, not an independent observing epoch.

An eclipsing system with alternating eclipses and an orbital period near
**8.19069 days** is therefore a plausible hypothesis. This is not a measured
spectroscopic orbit. The previously documented Gaia RV variability strengthens
the concern but is not phase-linked to these dips. No companion mass or confirmed
binary classification is claimed. A twice-period interpretation needs further
shape/timing modeling and independent data.

`verify.py` reconstructs all four QLP parity measurements, checks raw/input hashes
and recomputes errors. The phase plots were inspected. The unchanged measurement
routines passed the existing test suite:49 tests in23.77s. Raw-image evidence and its
182 independently reconstructed fits are in the preceding PRF event report.
