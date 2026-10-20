# Why the shallow injections were missed

All15 missed100ppm probes have formal local SNR below7 even at their exact injected period, epoch and duration. Their incremental local depth, measured by subtracting the uninjected baseline measurement from the injected measurement, retains76.3–99.9% of the nominal injected depth. This includes exposure smearing, sample masks and detrending effects; it is not a pure detrending transfer function.

The three recovered100ppm probes have true-clock local SNR7.20–7.45. All are the1.37-day,0.12-day-duration configuration. None of the missed100ppm probes reaches the matching blind-search top-three screening records, so later vetting gates are not the primary obstacle for these cases. At300ppm,14/18 reach matching top-three records and11 pass all gates; the other3 fail noise, inverted-signal or alternative-detrending checks.

This is a post-outcome diagnostic using known synthetic timing, not another blind search or a validation test on real candidates. It suggests additional coherent data, rather than relaxed late-stage gates, are needed for weak signals in these examples. It does not quantify population completeness or prove a particular longer-baseline design will succeed.

Reconstruction uses the same three original stars, quality-filtered flux, exposure-integrated box injections and1.5-day flattening. The36 baseline/injected true-clock measurements are saved with source hashes. `verify.py` reconciles input hashes, sample size, arithmetic and the stated missed-signal bound. It does not independently rerun the detrending algorithm. Reserved sectors remain unused.

Validation: all49 repository tests passed in28.93seconds.
