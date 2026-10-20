# ZTF timing coverage is too sparse for a clean fixed-window confirmation

Only104 of1903 quality-screened observations pass the existing conditional timing gate after allowing the UTC-versus-TDB ambiguity and one second for timestamp quantization. Two observations fall nominally within TIC196681132's transit windows, but neither remains inside across the full adopted timing range. No independent recovery or rejection follows.

| Target | Quality-screened observations | Pass timing gate | Nominally inside among passing | Inside throughout adopted range |
| --- | ---: | ---: | ---: | ---: |
| TIC196681132 | 658 | 76 | 2 | 0 |
| TIC422626648 | 466 | 24 | 0 | 0 |
| TIC241928959 | 779 | 4 | 0 | 0 |

Three of the timing-gated TIC196681132 observations could overlap a window under some offset in the heuristic range. The other two targets have zero such possible overlaps among the gated points. This is an observation-coverage assessment, not a photometric test: no magnitudes were compared with an eclipse model and no period or epoch was refitted.

The cloud schema confirms HMJD=HJD−2400000.5 at exposure midpoint, rounded to five decimal places. The locally cached [ZTF pipeline documentation](https://web.ipac.caltech.edu/staff/fmasci/ztf/ztf_pipelines_deliverables.pdf), section13 timing advisory and light-curve schema, likewise identifies midpoint timing and an approximate heliocentric correction. Neither checked passage explicitly establishes the underlying time scale. Both UTC-based and TDB-based HMJD interpretations are therefore retained as assumptions, not declared verified facts.

For each assumption, five fixed-point iterations remove the heliocentric light-travel delay, followed by barycentric correction and TDB conversion. The approximate Palomar location and Astropy builtin ephemeris are used; no extra half exposure is added. The two results differ by approximately69.18seconds. This sensitivity check is not an exhaustive bound on archive timing systematics.

At each observation, the existing frozen-TESS prediction_spread calculation supplies the conditional ephemeris spread. The gate requires spread plus the full UTC/TDB difference plus1second to be below half the frozen transit duration, with no profile-search boundary hit. The clock profile and floor are a heuristic, not a posterior or confidence interval; correlated noise and model mismatch are not fully propagated. Most older observations fail this gate due to the short TESS baseline. No nondetection exclusion can be made from them.

All1903 heliocentric inversion roundtrips close to the recorded numerical precision. Four deterministic synthetic controls (two positions, two assumed scales, each at two epochs) recover known barycentric times within0.1millisecond. verify.py checks input hashes and reconstructs the timing masks, scale margins and summarized counts. All49 repository tests passed in22.17seconds. These numerical checks do not establish the archive's time scale.

Source association checks and the unresolved cloud/catalog observation-count differences remain as previously documented. An exploratory search allowing timing changes would be a separate analysis, not validation at the original frozen ephemeris. The signal classifications remain unresolved.
