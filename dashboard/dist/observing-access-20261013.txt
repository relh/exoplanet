# Access to resolved photometric follow-up

**No telescope time is secured.** Three realistic access routes exist, but each requires a user decision or an external allocation. A paid reservation is the most direct route administratively; it does not guarantee the required measurement quality. Public documentation was checked on 13 October 2026. No accounts, contacts, applications, purchases or observations were made.

The initial experiment should prioritize **TIC 80387959 and neighbor TIC 80387965**, separated by 13.76 arcsec. Their saved T magnitudes are 10.52 and 13.62; the neighbor's conditional eclipse requirement is 1.10–1.39%, with an optimistic model variant of 0.56%. The provisional full track is approximately 5.6 hours. T magnitudes must not be substituted for the chosen instrument's filter magnitudes. These are copied planning inputs, not new measurements; see the [frozen packet](../followup-planning-20261013/ASSESSMENT.md).

## Routes and barriers

| Route | Access mechanism | Relevant capability | Exact unresolved dependency |
|---|---|---|---|
| **LCO science time** | Existing institutional allocation or reviewed Director's Discretionary Time proposal; worldwide DDT eligibility remains | Southern 1-m imaging at Chile, South Africa and Australia; northern sites for 402358350 | We have no allocation or established eligible institutional access. DDT merit and scheduling are unassessed; proposal submission needs authorization. |
| **iTelescope T17, Siding Spring** | Paid account, sufficient credit and reservation; public service rather than competitive science allocation | 432-mm telescope; currently listed CMOS camera; 0.531 arcsec/pixel at Bin2; 42.4 × 28.3 arcmin field | User budget/access choice, actual reservation slot, exposure and calibration feasibility, and continuous-track compatibility with local horizons. No quote or performance trial obtained. |
| **AAVSOnet / AAVSO observing collaboration** | Normally paid membership plus accepted telescope proposal; an independently arranged observer collaboration is a separate route | Network supplies calibrated photometric images; telescope assigned after review | Intensive overnight time series are explicitly less favored. No suitable southern instrument, allocation, or observer commitment has been established. |

LCO's **2027A ordinary call is not open to the entire astronomical community**. It is restricted to its eligible science family and agreement institutions, with an October 26, 2026 deadline and February–July 2027 semester. Earlier descriptions of general semester Open Access are now stale. This does not close worldwide DDT, but a pending call is not observing access. The current call also says NRES is unavailable. [Current call](https://lco.global/news/callforproposals2027a/)

LCO DDT accepts investigators worldwide and targets unforeseen opportunities or high-impact facility support. Award and expiry are discretionary; time ends with the semester. The Key Project route requires a previous letter of intent and invitation and is not an immediate small-program route. Nothing in our current evidence establishes that DDT would be awarded. [Allocation rules](https://lco.global/observatory/process/)

LCO Global Sky Partners supports organizations running educational projects. Education-user registration goes through a partner; it is not unrestricted free telescope access for an individual research request. Joining a suitable existing education project could be a future collaboration, but no such relationship or current partner allocation has been established. [Partner program](https://lco.global/education/partners/) · [Education access](https://lco.global/education/activities/preparing-an-observation-request-on-lco/)

The iTelescope terms require an active paid subscription and credit; reservations require an attached observing plan and depend on weather, equipment and competing reservations. Its free/demo or full-Moon sessions are too short for this 5.6-hour experiment; the advertised unlimited plan's live sessions are capped at four hours, so a reservation remains the relevant mechanism. The provider prohibits automated access to its LaunchPad/control UI: any later booking must use a permitted workflow. Images should be downloaded promptly because retention is limited. No booking or price quotation was attempted. [Terms](https://www.itelescope.net/terms-of-use) · [Reservation rules](https://support.itelescope.net/support/solutions/articles/143104-i-am-unable-to-create-a-reservation-what-can-i-do-)

The public iTelescope account-information page lists total active-reservation allowances from 8 to 20 hours, enough in aggregate for one 5.6-hour block. This is **not** verification of an available continuous slot or a target-specific rate; the same page labels its last rate review February 2022. [Published quotas](https://go.itelescope.net/info.aspx)

AAVSOnet normally requires membership in good standing, with rare nonmember exceptions. Proposal review chooses a telescope; it does not guarantee that every member can reserve one. Its guidance explicitly warns that full-night time series are less likely to be accepted because they displace other targets. It is therefore a possible collaboration/allocation route, not an immediate replacement for a dedicated reservation. [Network](https://archive.aavso.org/index.php/aavsonet) · [Proposal guidance](https://archive.aavso.org/index.php/how-write-aavsonet-proposal)

## Instrument constraints before selecting a track

**LCO 1-m/Sinistro:** the documented full-frame scale is 0.389 arcsec/pixel over 26.5 arcmin, with a 28-second readout/overhead. The central binned mode offers 0.778 arcsec/pixel over about 13 arcmin and under 9 seconds overhead, with a restricted calibrated-filter set. The page announces camera replacement during 2026/2027: verify the assigned camera rather than freezing today's specification for next year. Neither pixel scale nor aperture establishes attainable precision or close-neighbor extraction quality. [Sinistro specifications](https://lco.global/observatory/instruments/sinistro/)

The 1-m mount documentation lists a 15-degree altitude horizon and hour-angle limits of ±4.6 hours. Those mechanical bounds supplement any stricter scientific altitude, twilight, Moon and airmass requirements; a long track must satisfy all of them. [Mount specifications](https://lco.global/observatory/telescopes/1m0/1m-spec/)

**T17:** the current support page lists a ZWO ASI6200MM Pro CMOS sensor, Bin2 only, maximum 240-second unguided exposures, and available calibrated darks for 240 seconds. Its clear/LRGB and narrowband filters should not be assumed equivalent to TESS or standard Sloan filters. The documented approximate horizon is 20 degrees west, 35 north/south and 55 east. A generic Siding Spring altitude calculation does not by itself satisfy this asymmetric mask. The page was modified in June 2024, so confirm the operating configuration before committing time. [T17 specifications](https://support.itelescope.net/support/solutions/articles/231915-telescope-17)

For either instrument, a short calibration sequence or applicable prior performance data must establish unsaturated target exposures, usable neighbor counts, image separation, comparison-star stability and correlated noise. A longer exposure appropriate for T=16–18 neighbors may saturate the target; interleaved exposure lengths may be necessary and would need a frozen cadence plan. Defocusing to improve target precision can undermine neighbor discrimination. The 7–35 arcsec separations are promising geometrically, but actual PSFs and extraction leakage decide whether a source is resolved.

A non-detection is useful only if the full timing envelope is covered and injected eclipses at the predeclared threshold are recovered. A detected neighbor eclipse must quantitatively explain the TESS aperture decrement, including passband and dilution uncertainty. A target-only dip would still require constraints on unresolved stellar companions. These criteria follow the retained [planning assessment](../followup-planning-20261013/ASSESSMENT.md), not vendor specifications.

TIC 402358350 remains a separate timing-recovery task. Its current 17.5–18.5-hour expanded-profile windows cannot be treated as ordinary single-site overnight tracks. Northern telescopes or network handoffs may help once an experiment is designed, but no fixed short reservation is justified by the present ephemeris.

## Representative LCO geometry

These published site-center coordinates are suitable for preliminary visibility calculations, not final exposure timestamp corrections or a reservation. East longitude is positive. [Official site table](https://lco.global/observatory/sites/)

| Site | Latitude | Longitude | Height |
|---|---:|---:|---:|
| Cerro Tololo, LSC | −30.1674° | −70.8048° | 2198 m |
| Sutherland, CPT | −32.3800° | +20.8100° | 1760 m |
| Siding Spring, COJ | −31.2733° | +149.0710° | 1116 m |

The official T17 location differs slightly from LCO's COJ location: −31°16′24″, +149°04′11″, 1118 m. Do not label an LCO-site visibility calculation as a verified T17 schedule.

## Provenance and next decision

[sources.json](sources.json) records 14 public-page URLs, retrieval timestamps, HTTP status, local ignored raw paths and SHA-256 hashes. All returned HTTP 200; claims above were checked against retained HTML. [fetch_sources.py](fetch_sources.py) records the read-only retrieval method. The live process inventory showed no candidate-science process; unrelated jobs and the existing webpage server were left untouched.

The external dependency is **access to a suitable instrument and authorization for the access route**. The useful user inputs are existing telescope or network access, site/camera/filter details, or a budget and willingness to apply for time/contact observers. With an instrument selected, prepare its exposure/calibration trial and exact site-specific track before requesting approval to book. No new target flux was accessed, and neither candidate's classification changes.
