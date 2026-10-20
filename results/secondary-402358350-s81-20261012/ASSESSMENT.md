# TIC402358350: no half-phase eclipse detected in cached sector81

Sector81 shows no positive dimming at exactly half orbital phase. At the unchanged pre81 expanded-training clock, the half-phase depth is−136.77±98.52ppm (formal SNR−1.39) with1.5d detrending, and−168.06±100.30ppm (−1.68) with2.5d. Negative depth means a small apparent brightening, consistent with noise at this precision. This does not exclude a binary, an eclipse at another phase or a differently shaped secondary.

The primary remains634.63±72.23ppm and636.45±72.26ppm, respectively. This reproduces cached observations and is not a second independent confirmation. Only sector81 was reprocessed here;40/41/54 totals are copied from their hashed existing report for comparison without refitting.

The [frozen plan](plan.json) uses period11.769544332d (full precision retained in JSON), original expanded-primary duration and epoch. Only phase0 and0.5 were evaluated, identically for both detrending windows. No clock, phase, duration or additional observation search was performed. Sector81 was already opened before this retrospective diagnostic.

Only one half-phase event, at BTJD3528.753897, has in-window measurements:−148.49±100.30ppm under1.5d and−168.06±100.30ppm under2.5d. The slight difference between1.5d total and event depth arises because the total out-of-transit baseline also includes points from other cycles with no usable in-window observations. It is not an additional eclipse measurement.

Earlier half-phase sector totals were84±75,145±101,4±80ppm for40/41/54 under1.5d, and78±75,90±105,24±80ppm under2.5d. None establishes a secondary. The new sector adds no coherent positive half-phase evidence. Formal errors assume independent supplied errors and cannot justify calibrated binary-exclusion confidence.

[Verification](verification.json) independently reconstructs four total and six event depth/error measurements from hashed raw81 data using precision sums, with shared preprocessing. It checks exact identity, frozen clock and script provenance. Previous sector records are hash-linked and their clock checked equal, not independently reverified in this report. [comparison.png](comparison.png) was visually inspected.

Reproduce with `uv run python results/secondary-402358350-s81-20261012/verify.py`. No shared scientific code, docs, additional data or external submission changed.
