# Site visibility of the frozen follow-up windows

**Three TIC 80387959 windows pass a strict full-track sky-geometry screen at five representative sites. Only the first also passes the published LCO 1-meter hour-angle limit, and it is close to that mechanical boundary. No TIC 402358350 window passes the full-track screen, even when combining the five sites' sampled visibility.** These are planning calculations, not new observations or evidence for either candidate's planetary origin.

The calculation retains all 64 event windows from the [existing packet](../followup-planning-20261013/ASSESSMENT.md), including the entire timing envelope, transit duration and one-hour baselines. The five sites are Cerro Tololo, Sutherland, Siding Spring, McDonald and Haleakala, using coordinates and elevations from the [official LCO site list](https://lco.global/observatory/sites/). Neither the user nor this investigation has established access to a telescope at these sites.

## Single-site opportunities for TIC 80387959

The frozen sky gates require target altitude at least 30° and Sun altitude at most −18° throughout the track. All three passing tracks also meet a 1° conservative margin on both sky gates. UTC values below are approximate geocentric arrival times, rounded to the minute; use the unrounded CSV when planning.

| Site | UTC date and full track | Minimum target altitude | Maximum Sun altitude | Minimum Moon separation | LCO 1m hour-angle limit |
|---|---|---:|---:|---:|---|
| Cerro Tololo | 2027-03-20 02:52–08:30 | 35.82° | −29.83° | 60.28° | Pass, narrowly: 4.577 h |
| Siding Spring | 2027-03-28 12:05–17:43 | 32.33° | −32.32° | 73.02° | Fail: 5.010 h |
| Cerro Tololo | 2027-04-10 01:55–07:33 | 31.53° | −44.46° | 119.41° | Fail: 5.017 h |

LCO publishes an [hour-angle range of −4.6 to +4.6 hours for its 1-meter telescopes](https://lco.global/observatory/telescopes/1m0/). That constraint was separately frozen during calculation, before interpreting the geometry results, and applied without altering the original sky screen. The March 20 track approaches the limit to within 0.0227 hour, approximately 82 sidereal seconds. It fails a conservative 1° hour-angle margin. **There is therefore no comfortably margined full LCO 1m track in this particular frozen list.** March 20 is a nominal possibility needing scheduler and instrument confirmation, not a recommended or secured booking. The other two rows may suit other mounts only after checking their actual restrictions. In particular, a shared Siding Spring location does not transfer these results to iTelescope T17's asymmetric horizon.

There are no full single-site passes before March 20 under these gates. This does not mean earlier observations are impossible or useless. For example, the March 7 Siding Spring track covers 98.82% of sampled points under the sky gates but reaches Sun altitude −17.21° near its edge. Shorter baselines, a different site, multiple sites or a deliberately different experiment could provide useful data; such changes need a new explicit plan and must not silently be counted as meeting this screen.

## Network geometry and TIC 402358350

Ten TIC 80387959 windows have full *sampled* geometric coverage by the union of the five sites. This is not a coordinated observing plan: the union ignores each mount's limits, scheduler availability, calibration between telescopes, weather and overlap needed to connect baselines. No allocation or handoff has been arranged.

None of TIC 402358350's 17 saved 17.45–18.50-hour windows has complete coverage at a single tested site or in that five-site union. Its uncertain ephemeris remains the primary obstacle. These calculations do not exclude coverage by a different network or space telescope, and a partial-window non-detection would remain inconclusive. Recover the clock from discriminating observations before planning a short targeted non-detection test.

## Calculation and verification

[plan.json](plan.json) freezes gates and input hashes. [sites.json](sites.json) preserves the adopted site coordinates; the downloaded official page is retained under ignored `data/site-visibility-20261013/` with its URL and SHA-256 in [provenance.json](provenance.json). [site-events.csv](site-events.csv) contains all 320 site/event combinations; [network-coverage.json](network-coverage.json) retains the union screen. [instrument-amendment.json](instrument-amendment.json) and [instrument-screen.json](instrument-screen.json) preserve the additional mount constraint and its source hash.

Astropy 8.0.1 uses its built-in solar-system ephemeris with IERS auto-download disabled and zero atmospheric refraction. Every track includes both endpoints and points separated by at most two minutes. Moon separation is reported without an arbitrary exclusion threshold; its photometric effect is not modeled. No IERS/extrapolation warnings were emitted; the saved warning lists are empty. Using fixed J2027 finder positions and approximate geocentric UTC is adequate for this broad geometry screen, not precision transit timing. The site-versus-geocenter light-time correction is bounded by approximately 0.022 second, negligible here. Current Earth-orientation data and full topocentric timing should be used for an actual observation.

The main calculation checks 85,890 target altitudes against the independent spherical altitude relation using topocentric CIRS coordinates and Earth rotation angle: maximum disagreement 0.0001383°. Five synthetic zenith identities also pass. [verify.py](verify.py) checks source/output hashes and repeats all three passing tracks with a denser, independent 31-second grid; all remain passing, including the sky margins. The hour-angle screen samples each passing track at 1,001 points. These checks establish numerical consistency, not telescope performance or continuous weather availability. The 1° sky margin is larger than the maximum angular travel across a two-minute sample interval, providing a conservative sampling guard for the passing rows; no equivalent robust mount margin survives.

Reproduce with `uv run python results/site-visibility-20261013/build.py`, then `verify.py` and `instrument.py` in that directory. No new stellar flux, reserved TESS epoch, observation request, submission or external contact was made. The original completed investigations remain complete; the decisive-evidence goal remains unresolved.
