# Faint-pilot injection checks — complete

These are synthetic controls, not discoveries. Twelve probes are frozen for the
first three targets in the pilot's pre-existing selection order: periods1.37 and
4.73days, radii1 and2Earth, duration0.04day, one deterministic phase. Depth is
computed using each catalog stellar radius. The signal is multiplied into
quality-selected native QLP flux before ten-minute binning and detrending, with
exposure-integrated box attenuation. Uncertainties scale with injected flux.

Before any injection for a target, the custom loader must reproduce the original
loader's time, flux and uncertainty arrays exactly for both detrending windows.
This baseline-equivalence result and original download evidence are saved.

All12probes completed without errors and recovered the injected period among
the top three peaks. All12 also match the injected phase within half the injected
duration at the start, middle and end timing checks. None has a qualifying
pre-existing baseline-period match. Ten pass the original signal-quality screen
apart from missing aperture crowding. The two failures are both on TIC231733039
at4.73days: the1Earth injection retains an alternate-detrending flag, and the
2Earth injection retains an inconsistent-event-depth flag. Both failures are
preserved; the screening threshold was not changed. These results support a
limited pilot expansion after its data-quality review, not a completeness claim.

This does not measure survey completeness: three stars, one phase and duration,
two periods, box shapes, catalog radius uncertainty ignored, and no contaminant
flux dilution or physical limb darkening. Training-only probes leave reserved
observations untouched. Known-planet controls remain separate evidence of
limited sensitivity in other faint datasets. No quality gates were changed.
