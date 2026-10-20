# Exploratory added-sector searches from weak discovery peaks

This pilot selects eight stars from 689 eligible completed below-threshold records before downloading any added photometry. It ranks original maximum SNR descending, then TIC, requires at least two unopened additional sectors <=55, and caps total early sectors at nine. The original reserved sector for each star stays unopened.

The sole seed is each original search's strongest peak. The existing local-refinement routine searches around it after adding every early sector, with both 1.5-day and 2.5-day detrending. A provisional review flag requires formal SNR >=8 in both windows, periods agreeing within 0.5%, and neither timing profile touching its search boundary. This is a limited local search and not a pass through the original full vetting pipeline. It does not calibrate the extra search trials, establish a planet, or replace the original below-threshold records.

The pilot is motivated by the separate TOI-1435 b control, where extra sectors strengthened the local signal but the reserved-sector check remained inconclusive. It is an experiment in extending the viable search, not a change to the running frozen campaign. All selected stars, errors and outcomes are retained. Completed results and audit scope follow.

## Completed pilot

All eight targets completed without errors. Three satisfy the frozen local review rule; none has yet passed full vetting or an independent reserved-sector test.

| TIC | Period (days) | Depths, two windows (ppm) | Formal SNR, two windows | Local review flag |
|---|---:|---:|---:|---|
| 160163644 | 11.51180385 | 219.9, 578.4 | 12.68, 31.00 | True |
| 165796775 | 6.07631717 | 87.0, 119.8 | 8.55, 11.65 | False |
| 306680120 | 0.72265717 | 113.9, 120.2 | 9.24, 9.14 | True |
| 346630628 | 10.55133948 | 130.1, 163.6 | 6.12, 5.93 | False |
| 366637784 | 2.79773280 | 58.6, 66.4 | 7.70, 8.10 | False |
| 394877426 | 9.35674481 | 292.3, 368.7 | 9.99, 11.93 | True |
| 398308221 | 1.24661363 | 29.9, 30.4 | 6.08, 5.89 | False |
| 443950840 | 3.27768371 | 72.1, 79.4 | 6.41, 5.87 | False |

TIC160163644 and TIC394877426 both choose the longest local duration (0.216 day); the former changes depth by a factor of 2.63 between detrending windows. TIC306680120 has a fitted duration of 0.1104 day over a 0.722657-day period (15.3% duty cycle). These are concerns requiring morphology, variability and contamination checks before any planet interpretation. The three are exploratory leads, not likely new planets. No planet radius is assigned.

The verifier reconstructs all 16 local refinements and fixed-clock measurements, checks raw hashes and FITS identities, selection/source hashes and download chronology, and confirms reserved-sector cache absence. This verifies reproducibility, not physical validity or significance.

Subsequent six-window diagnostics and exact catalog identity checks deprioritize all three local review flags. Their original strengths and selection outcomes remain above. See [follow-up evidence](../weak-seed-review-20261011/ASSESSMENT.md). Reserved sectors remain unopened.
