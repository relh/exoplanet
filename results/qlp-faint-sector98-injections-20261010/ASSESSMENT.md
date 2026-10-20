# Sector 98 injection checks

Twelve deterministic injections into the first three frozen pilot targets
completed without errors. All twelve recovered the injected period among
the top three peaks, and all matched within half the injected duration at
the three checked times. Eight passed screening gates apart from missing
crowding information. Four one-Earth-radius cases were too weak to pass;
all six two-Earth-radius cases passed those gates.

Signals were inserted into raw flux before binning and detrending, preserving
the existing noise and astrophysical signals. Each baseline loader matched
the original loader exactly at both detrending windows. The fixed grid was
periods 1.37 and 4.73 days, radii one and two Earth radii, duration 0.04 days,
and one phase fraction of 0.317. These are synthetic box-shaped signals;
only three stars and one duration/phase were tested. The checks do not
establish survey completeness, false-positive rates, or host attribution.

See [audit.json](audit.json) for every recovery, timing comparison, retained
flag and evidence hash. No held-out photometry was opened by this test.
