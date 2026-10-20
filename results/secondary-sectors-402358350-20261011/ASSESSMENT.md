# TIC402358350: no convincing half-phase secondary in opened training sectors

At the fixed expanded40/41/54 primary clock, exact half-phase measurements are:

| Sector | 1.5day detrending depth ± formal error(ppm) | Formal SNR | 2.5day depth ± formal error(ppm) | Formal SNR |
|---|---|---|---|---|
|40|84.5±75.4|1.12|78.4±75.2|1.04|
|41|144.7±101.0|1.43|90.2±105.3|0.86|
|54|4.3±79.8|0.05|24.1±80.0|0.30|

None provides convincing evidence of an eclipse exactly halfway between the primary dips. This is not a calibrated exclusion of a binary: unequal/eccentric eclipses, dilution, timing and noise uncertainty remain. No other secondary phases were searched. Both windows share photons. Primary measurements are retained with all secondary measurements in results.json.

This is a retrospective diagnostic on already-opened40/41/54, using a clock fitted to those same data. It is not independent validation. Both windows use the same expanded primary clock and0.144day duration; this differs from the window-specific timing comparison protocol. The larger fitted primary depth in54 is therefore not a replacement for the prior saved prediction test. Sector81 was not accessed by this analysis.

All12 total depth/error/SNR measurements independently reproduce by weighted sums from the three hashed FITS inputs. Preprocessing shares the existing implementation; event-level arithmetic was not independently checked here. Formal errors do not incorporate full correlated noise or model uncertainty. No host attribution or planet probability follows.
