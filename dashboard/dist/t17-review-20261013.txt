# Independent T17 feasibility review

**The numerical results and limited interpretation are supported.** All 47
retained TIC 80387959 windows have unchanged endpoints. Only event 696 on
28 March 2027 passes the full altitude/darkness requirements. It passes the
illustrative cardinal-interpolation horizon; no window passes the assumed
flat 55° horizon. Neither model establishes the operator's actual mask.

The [verifier](verify.py) passes [386 checks](verification.json), including
all 31,724 saved decision samples and input hashes. For the 678-point March 28
track, an alternative TETE/equinox frame and apparent sidereal time reproduce
altitude and azimuth within 0.000103° and 0.000313°, respectively. The author
uses CIRS/CIO coordinates and Earth rotation angle. Both calculations share
Astropy time/ephemeris inputs; this checks coordinate conventions and arithmetic,
not independent observational accuracy.

The report explicitly leaves mount limits, meridian-flip interruption, actual
horizon, access and photometric performance unresolved. It does not transfer
LCO's hour-angle limit. The approximately 5.64-hour track is a conditional
proposal, not secured or demonstrated observing capability. A trial or even
one target-localized dip would not establish a planetary companion. The second
candidate's timing problem remains unresolved.

The [unsent inquiry](../t17-access-inquiry-20261013/ASSESSMENT.md) uses the correct
finder coordinates and rounded UTC interval and requests the missing operating
information. It distinguishes TESS magnitudes from instrument passbands and
requests exposure/calibration checks. No network, flux access, external contact
or booking was performed in this review. Public provider descriptions alone
cannot demonstrate empirical sensitivity or authorize a purchase.

A wording correction was recommended: call TIC 80387965 the principal neighboring
source of interest, rather than a comparison star. Its possible eclipse is
under investigation, so it must not be assumed to be a stable calibration star.
No substantive scientific correction was required. Review the actual operator
response and freeze a trial protocol before any authorized observations.
