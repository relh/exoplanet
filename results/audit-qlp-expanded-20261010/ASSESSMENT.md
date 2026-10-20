# QLP-expanded campaign:287 usable targets, no review pass

The288-star frozen selection reaches Sector104. Both the original campaign,
the separate empirical-error recovery, and the data-availability fallback runs
are terminal (process exit0). `final_audit.py` verifies exact selection coverage,
deduplicates all routes and preserves original failures.

| Route | Usable targets |
|---|---:|
|Original QLP training pair, published errors|231|
|Same QLP training pair, empirical errors in otherwise unusable-error sectors|53|
|SPOC reduction of the same training epochs|1|
|Single surviving preassigned QLP training sector|2|
|Total usable|287|

There are225 below-screen-threshold and62 flagged targets. None passes all
non-crowding checks. QLP aperture crowding remains unassessed regardless.

The original run had57 failures. Fifty-six entered the empirical recovery;
53 recovered, while three had no usable flux rather than just missing errors.
TIC101722368 had insufficient clean QLP cadences but its SPOC Sectors25/26 work.
TIC183597632 uses surviving Sector29; TIC350348591 uses surviving Sector46.
Their period ceilings are approximately8.94/9.67d (baseline/2.5), so their coverage
is not equivalent to a two-sector search extending toward20d. All these results
are below threshold. Originally reserved epochs remain unopened.

**TIC357307559 remains unsearched:** QLP discovery Sectors45/46 contain no usable
quality-zero flux/error pairs. Its reserved Sector72 was not repurposed as
validation after discovery. This failure is retained, not counted as a null.

Empirical errors estimate short-timescale scatter from adjacent flux differences;
they are not published uncertainties, a red-noise model, or calibrated detection
significance. The physical/crowding/brightness cuts, targeted metadata sample,
finite period grid and heuristic vetting limit completeness. No absence-of-planets
claim or new candidate claim follows from these negatives.
