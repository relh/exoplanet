# TIC 101404423: unresolved screening signal

Native refinement: P=2.433118486 days, duration=0.133056 days, box depth=0.00258635 ± 0.00020788 (formal). Training sectors [104]; 8 supported events. These are fitted diagnostic quantities, not physical size estimates or calibrated discovery probabilities.

The original-seed native discovery plot was inspected: Shallow rounded central depression with small positive shoulders and a gap in the time series. Eight supported training events; prioritize source images, but no independent recurrence or host attribution.

Reserved-sector timing tests: sector 13: timing_prediction_inconclusive, timing spread 4.435823 days; sector 27: timing_prediction_inconclusive, timing spread 3.772782 days. Timing uncertainty prevents interpreting a fixed-window absence as exclusion or confirmation.

Exploratory off-phase maximum formal SNR: 2.493091134738869. It is selected over phase/duration and is not a calibrated secondary-eclipse significance.

Original screening flags, cache-presence records, failed checks and timing profiles remain in the underlying files. Source attribution, catalog checks and physical vetting remain pending. No likely new planet claimed.

## Source-image and catalog assessment

The sector104 raw stack and all10 individual maps were inspected. Repeated compact positive differences lie near TIC101404439, roughly3.984pixels from the nominal target. Event2 has just two inside exposures and stronger field/edge structure; event0 and especially10 have positive background offsets. The other events consistently show the off-target feature. Contamination is strongly favored; no planet orbiting the nominal target is supported by these images. Ten usable image windows do not mean ten photometrically supported transits (the training fit supports eight).

Events0/1/3/4/6/7 have58 inside samples,8/9/10 have57, event2 has2; quality-zero baseline counts are221–230. Event5 has58 inside samples all flagged (20flag2048,38flag18432) and is excluded. Raw FFI and QLP use the same photons. Formal peak pixel SNR444.2 is not calibrated source confidence. The exact processed sector104 product request returnedHTTP404, retained with child exit1; other processed products are not ruled out.

The140-row neighbor query and all16 catalog sources within3pixels of the raw difference moment were queried in Gaia. Sixteen source rows, two classifier rows and one eclipsing-binary row returned. The latter maps to TIC101404439 (GaiaDR3 6666656178247953024), with frequency0.41154755746435456/day and period2.429852837days. This lies within the retained TESS range2.428895291–2.435230083days; the best TESS value is2.433118486days. The spatial and period agreement strongly favor contamination by this cataloged eclipsing-binary candidate, though unresolved nearby sources and exact epoch alignment remain untested. Catalog classification scores are not probabilities of being the TESS source. Coordinates were not proper-motion propagated.

The [Gaia column documentation](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_variability_tables/ssec_dm_vari_eclipsing_binary.html) specifies reciprocal-day frequency and a TCB-based reference epoch; no direct epoch comparison is claimed here. [Period arithmetic](../../gaia-101404423-scene-20261011/period-comparison.json), [stack](../../tesscut-101404423-s104-20261011/difference.png), and [individual maps](../../tesscut-101404423-s104-20261011/event-plots.json) are retained. Source/plot/coverage/catalog hashes verified. No new planet or novelty claim.
