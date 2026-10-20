# T17 follow-up geometry

**One retained TIC 80387959 track is geometrically promising for T17, but its operational feasibility remains unverified.** The March 28, 2027 track passes the unchanged altitude and darkness requirements and an explicitly exploratory horizon model. This is preparation for independent source photometry, not evidence that either candidate is a planet. No telescope access, reservation or empirical precision has been established.

## Full-track result

All 47 existing windows were evaluated at T17’s own published location, retaining the timing envelope, transit duration and both one-hour baselines. The March 28 event is the only complete sky-gate pass; shortening other windows was not permitted. No LCO mount restriction was transferred to T17.

| Quantity | March 28, 2027, event 696 |
|---|---:|
| Approximate geocentric UTC track | 12:04:53–17:43:09 |
| Duration | 5.638 hours |
| Target altitude range | 32.33–72.51° |
| Azimuth range, north through east | 160.12–230.46° |
| Start altitude / azimuth | 71.05° / 160.12° |
| End altitude / azimuth | 32.33° / 228.94° |
| Highest Sun altitude | −32.32° |
| Minimum clearance above exploratory cardinal interpolation | 5.48° |

The [official T17 page](https://support.itelescope.net/support/solutions/articles/231915-telescope-17) gives approximate cardinal minimum elevations: north/south 35°, east 55°, west 20°. Its linked diagram, retained with [provenance](diagram-source.json), depicts an asymmetric horizon but supplies no numerical mask or operational guarantees. The page lists a Paramount PME mount. Its actual tracking limits, meridian behavior and permitted uninterrupted scheduling have not been established.

Two frozen sensitivity cases illustrate why the mask matters. Applying 55° at every azimuth rejects every full track; this assumes the largest published cardinal elevation is a global maximum and is not a verified bound. A periodic linear interpolation through the four cardinal values allows March 28 with 5.48° minimum clearance; it also passes the separately specified 1° sky/horizon margins. **The interpolation is an analyst’s model, not the operator’s horizon.** The diagram is qualitatively consistent with lower southwestern obstructions, but was not digitized or substituted for authoritative limits. Other unreported mechanical restrictions could still preclude the track.

## Exact remaining dependency

Before selecting this track, obtain the operator’s current numerical horizon and mount/meridian restrictions for the complete azimuth path, verify that a continuous 5.64-hour sequence is permitted, and establish an available authorized access route. An exposure/calibration trial must then demonstrate unsaturated target photometry, separate neighbor measurements, adequate counts and stable comparisons under the [source-attribution protocol](../decisive-observation-protocol-20261013/ASSESSMENT.md). A geometric pass supplies none of those capabilities. These are prerequisites to a concrete booking decision, not reasons to keep revising the same visibility calculation.

No account, LaunchPad automation, contact, booking, payment or new stellar flux was used. TIC 402358350 still needs reliable event timing; this instrument check does not resolve that dependency. A future target-localized dip would also leave unresolved stellar companions to be tested. Both scientific classifications remain unchanged.

## Reproducibility and limits

[plan.json](plan.json), frozen before calculation, records coordinates, gates, model definitions, input hashes and source metadata. [events.csv](events.csv) retains every success and failure; [geometry.csv](geometry.csv) records all 31,724 sampled points. The target coordinates and approximate geocentric UTC come unchanged from the prior packet. The timing profile is not a confidence interval.

Astropy uses zero refraction and disabled IERS downloads on a grid no coarser than 30 seconds, including endpoints. No warnings occurred. Independent spherical equations reproduce altitude and azimuth to maximum differences of 0.000114° and 0.000318°. [verify.py](verify.py) checks hashes, all tabulated decision rules and the passing track on a separate 17-second grid. These numerical checks do not validate the proposed horizon model, actual availability, weather, clock precision or observing performance. Actual observations require current topocentric timing and instrument configuration.

Reproduce with `uv run python results/t17-feasibility-20261013/build.py` and then `uv run python results/t17-feasibility-20261013/verify.py`. See [summary.json](summary.json), [provenance.json](provenance.json) and [verification.json](verification.json).
