# TIC 80387959: additional archival spectroscopy

**New, modest evidence against an obvious spectroscopic false positive on the bright target; no change to candidate grade or unresolved-host status.** RAVE DR6 supplies one historical target spectrum with a normal primary classification and RV consistent with Gaia's later aggregate. This does not test the neighboring eclipsing-star explanation, measure a planetary RV signal, or exclude a target-host binary. No calibrated probability follows.

| Newly checked evidence | Result | Consequence |
|---|---|---|
| RAVE DR6 observation `20100502_1050m50_094` | 2010-05-02; catalog RV **5.94 ± 0.87 km/s**, S/N 52.3 | Adds an independent survey/epoch, previously absent from our checked evidence |
| Comparison to existing Gaia DR3 | Gaia **7.0209656 ± 0.32064104 km/s**; difference **1.08097 ± 0.92721 km/s**, **1.166 formal sigma** | No significant discrepancy on quoted errors; cross-survey zero points and phase coverage are not modeled |
| RAVE spectral morphology | Primary `n`, weight **0.9437**; secondary `e`, **0.0563022**; tertiary blank | Predominantly normal morphology, with a small activity alternative; weights are neither binary-exclusion probabilities nor planet probabilities |
| RAVE repeat inventory | **One** observation; remaining 12 observation slots blank | No RAVE time series with which to test orbital RV variation |
| RAVE MADERA | Calibrated Teff **5144.8 K**, log g **4.394**, metallicity **−0.06445**; listed errors 76 K, 0.12 dex, 0.1 dex; quality flag 0 | Supports an ordinary dwarf interpretation. These pipeline errors do not include all systematics; no mass/radius recalibration performed |
| GALAH DR4 all-star exact identity and spatial fallback | No target Gaia/2MASS row. Rectangular neighborhood returned one unrelated source **71.108 arcsec** away, outside the 60-arcsec circle | No useful GALAH spectrum found in this release/query; no astrophysical exclusion |

## Identity and original sources

The [SIMBAD query record](identity.json) joins TIC 80387959, TYC 8203-2056-1, 2MASS J11011449-4836490, Gaia DR2/DR3 5362389543781401216 and **RAVE J110114.5-483649** to the same object (oid 7533309). The RAVE row lies 0.0773 arcsec from the SIMBAD J2000 coordinate. More decisively, the [RAVE release's own EDR3 crossmatch](rave-gaia-join.json) joins this exact observation ID to Gaia 5362389543781401216. The repeat and MADERA tables join by the same observation ID. Neighbor TIC 80387961 is a separate Gaia source; this association does not establish which object produces the TESS dip.

Original catalog results: [master/classification](rave-cone.json), [repeat inventory](rave-repeats.json), [MADERA](rave-madera.json). The [RAVE DR6 catalog documentation](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/III/283?format=html&tex=true) defines `n` as normal, `e` as chromospheric emission/activity, and `b` as binary; the listed weights describe spectral classification. The [survey paper](https://arxiv.org/abs/2002.04377) describes the intermediate-resolution survey and its radial velocities. An undetected/faint companion can escape spectral classification. The [GALAH DR4 paper](https://arxiv.org/abs/2409.19858) describes the independent survey searched here; its target nonmatch carries no novelty implication.

## Relation to prior evidence

The [Gaia RV-context assessment](../rv-context-80387959-20261011/ASSESSMENT.md) already found no strong Gaia RV variability flag. Its aggregate RV is reused, not counted as a new observation. Existing [TGLC](../tglc-80387959-20261009/ASSESSMENT.md), [NSC](../nsc-80387959-q3c-20261010/ASSESSMENT.md), and [SkyMapper](../skymapper-80387959-20261010/ASSESSMENT.md) checks leave blending/source attribution unresolved. The new RAVE normal classification concerns the bright source and cannot eliminate a faint eclipsing source in the TESS aperture. Agreement between one RAVE velocity and a Gaia aggregate is weak conditional evidence, since binary RVs can coincide at some phases and the aggregate suppresses phase information.

The next useful experiment remains resolved, timed in-transit photometry of the competing sources or suitable repeated spectroscopy. The RAVE spectrum itself is a potential archival lead for an explicitly scoped spectral review, but **no spectrum or new flux series was downloaded** in this task. No TESS data, epochs, ephemerides, or held-out observations were opened or changed.

## Search coverage, errors, and reproducibility

Exact web searches for `TIC 80387959`, `5362389543781401216`, `8203-2056-1`, `11011449-4836490`, `80387959 star planet`, `RAVE J110114.5-483649`, and `110114.5-483649` produced no useful target-specific paper. A preliminary incorrect Tycho-prefix search (`TYC 8204` plus `1101`) was discarded; it did not establish identity. These are search-engine results, not exhaustive literature or novelty checks. SIMBAD's exact identifiers supplied the substantive RAVE lead.

Official TAP metadata were inspected before interpreting the tables. Data Central's GALAH cone function returned **HTTP 500** ([retained error](galah-cone.json)); the successful explicit RA/Dec bounding box recovered the local neighborhood and independently checked separations. The initial VizieR table-name pattern returned zero because of quoting; a broader pattern recovered 19 tables. It is a metadata lookup limitation, not a missing-target result. ESO metadata are owned by the coordinator and were not queried here.

Every request record preserves URL/ADQL, UTC request time, HTTP status, raw path and SHA-256, including the failed cone response. [Document manifest](documents.json) retains primary-document bytes/hashes. Reproduce queries with `uv run python results/web-80387959-20261012/{query,spectroscopy,followup,join,final_queries,docs}.py` individually; these contact the network and may return newer data. To check saved evidence without new requests:

```sh
uv run python results/web-80387959-20261012/verify.py
```

[Independent verification](verification.json) passed 19 raw-file hashes, raw CSV versus report rows, exact identity/observation joins, empty repeat slots, independently computed spherical separations, and RV difference/error arithmetic. It also hashes the reused prior Gaia input. This task changes no scientific algorithm and therefore adds no shared algorithm tests.
