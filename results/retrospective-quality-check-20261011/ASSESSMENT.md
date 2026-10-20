# Five retrospective signals: processed quality comparison

Nine requested same-epoch products cover ten supported native events across
five stars. Five products succeeded; four returned HTTP404. All outcomes and
raw provenance are retained. This is not new independent observing coverage.

Both events for TIC288525984 and TIC394050941 carry only quality4096 in-event
samples. One of TIC298551568's events has that flag; its Sector79 event has
quality-zero samples but the frozen-timing SPOC depth is2326±1376ppm (formal
SNR1.69), compared with QLP4616±1522ppm. Same photons, different processing.

The processed products for TIC258513090 sectors85/86 and TIC352831349 sectors16/17
were unavailable at the requested URLs. No clean-data, astrophysical rejection
or absence-of-product-everywhere claim follows from those errors.

Quality4096 denotes automatic stray light in the TESS flag definitions:
https://lightkurve.github.io/lightkurve/_modules/lightkurve/utils.html .
Flags raise instrumental concerns, not proof of a particular physical cause.
All five remain diagnostic only. Raw-image checks for unavailable reductions
and source attribution remain outstanding.
