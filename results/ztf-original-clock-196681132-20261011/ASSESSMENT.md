# TIC196681132: promising independent-photometry agreement, still unresolved

Unmodified ZTF photometry shows dimming at the original frozen TESS clock. The fitted depth is2.106% across all658 quality-screened points, consistent in scale with the roughly1.974% TESS depth. The signal appears in both chronological subsets and all three filters. This is promising agreement in independent photometry; it is not a fresh blind validation or a planet classification.

This check was prompted by the preceding injection controls, after the later ZTF observations had already been opened. No period, epoch or duration was adjusted here: P=0.7244717005days, BTJD epoch3776.471636, duration0.032day come from the preexisting TESS fit. The earlier strongest free-phase ZTF peak had a different epoch and failed its reserved test; that negative result is preserved. The present result does not retroactively replace that selected peak.

| Subset | Depth | Formal error | Formal SNR | Residual-scaled SNR | Inside points |
| --- | ---: | ---: | ---: | ---: | ---: |
| All | 2.106% | 0.214% | 9.86 | 4.31 | 26 |
| Early, HMJD<60000 | 1.998% | 0.271% | 7.37 | 3.10 | 16 |
| Later, already inspected | 2.239% | 0.347% | 6.45 | 3.05 | 10 |

The26 inside points span24 frozen-clock event numbers. Separate g/r/i fits give depths2.293%,2.004% and2.036%; the i result has only three inside points. The fit includes an independent baseline per object ID. Adding object-by-year-bin intercepts gives1.908% depth. Leaving out each nominal in-window event in turn yields1.858–2.216%, so a single event does not drive the positive depth. All measurements use the already archived quality filter and discovery-median normalization; no additional outlier clipping occurs.

No shifted-phase control among41 shifts from0.1 to0.9cycle exceeds the original-clock formal SNR. These overlapping controls are not exchangeable and the current analysis follows data inspection; zero exceedances is not a calibrated false-alarm probability. Residual chi-square3427.60 for654degrees of freedom shows substantial extra scatter. Dividing the formal SNR by the square root of reduced chi-square gives the descriptive residual-scaled values above, not rigorous correlated-noise significance.

The three fold panels were inspected. Under the alternative TDB-based HMJD interpretation, the all-data depth becomes2.210% (25inside points), early depth2.153%, and later depth remains2.239%. Thus the roughly69-second time-scale difference tested here does not erase the feature. This does not establish the true archive time scale or eliminate the large original ephemeris-propagation uncertainty.

verify.py independently reconstructs72 fits via weighted within-group centering, verifies input hashes, checks a deterministic synthetic2% dip with unequal group offsets, and records the alternative time-scale calculations. The preserved source data and fixed clock are unchanged. Repository test results are recorded separately after completion.

Remaining concerns: the check is post-inspection, the measurements are sparse, formal errors understate scatter, and the cloud/catalog count differences remain unresolved. ZTF position associations and TESS image-response fits favor the target region, but neither excludes an unresolved eclipsing binary. Gaia RUWE is elevated and velocity diagnostics are incomplete. Retain TIC196681132 as a higher-priority unresolved transit-like signal, not a securely attributed new planet candidate. Further binary diagnostics and genuinely new observations remain needed.
