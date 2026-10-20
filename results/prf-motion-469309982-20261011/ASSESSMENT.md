# TIC469309982: motion nuisance terms do not establish target-star dimming

Adding two target-PRF spatial derivatives as pointing-related nuisance terms still gives no consistent positive target signal across both discovery epochs. These are posthoc model-sensitivity checks, not proof of an instrumental cause or a validated host assignment.

| Sector | Local radius (pixels) | Signed target amplitude / formal error | Target + motion chi-square / dof |
|---|---:|---:|---:|
|9|2.5|+2.34|159.30 /15|
|9|3.5|+3.48|174.67 /31|
|36|2.5|−6.45|1091.89 /14|
|36|3.5|−2.17|1226.28 /33|

Positive amplitudes denote dimming. The negative sector36 fits are contrary to target-centered dimming in this model, but the very large residuals invalidate a precise exclusion claim. All four local fits leave structured positive and negative residuals around the bright source. The figures were inspected. The simple first-derivative model is inadequate; neither motion alone nor target plus motion explains the images well.

With motion terms, neighboring TIC469309967 ranks first in both whole-image stacks, all four local-region fits, six of eight sector9 event-omission stacks and all eight sector36 event-omission stacks. This is more consistent than the source-only fits, but still not reliable physical attribution: even its whole-image chi-square is179/115 and872/115, and local residuals remain substantial. Two sector9 omissions favor other sources. No new planet is assigned to the neighbor.

An independent QR solver reproduces 988 hypothesis fits (joint, source-only and motion-only comparisons). Raw-image and PRF hashes are checked. Matched-template synthetic additions recover the inserted target coefficient, showing numerical identifiability under the assumed templates; they do not test real PRF mismatch, completeness or source accuracy. The model uses the same already-opened discovery pixels and unchanged photometric clock. Sectors63/64 remain unopened.

TIC469309982 stays deprioritized as a likely on-target planet. Retain its approximately140-ppm photometric dip and possible secondary together with these negative source diagnostics. Its physical cause remains unresolved, and other planets around the star are not excluded.

Subsequent known-planet calibration: [Kepler-93 b](../prf-137151335-20261011/ASSESSMENT.md) also yields inconsistent source rankings with poor residuals. Consequently these image diagnostics alone cannot reject a shallow planet. This signal remains unresolved with its separate photometric concerns; no physical false-positive label or exclusion is established.

Later reserved-sector evidence changes the current priority to **unresolved / continued review**: [sector64 follow-up](../followup-469309982-20261011/ASSESSMENT.md) retains a positive match among pre-saved timing alternatives but remains timing-inconclusive. Sector64 is now deliberately opened; historical cache-absence statements above describe the earlier stage.
