# Remaining closely spaced-sector search

All123 frozen targets completed:102 below threshold,17 flagged and4 errors. Both unchanged follow-up policies completed with no eligible fits. No new planet candidate is established. Together with the pilot,139 targets produced117 below-threshold results,18 flagged results and4 errors.

Discovery/reserved splits and metadata order were frozen before the pilot. No reserved sectors were opened in this batch. Nearby reserved epochs would provide weaker temporal separation than the earlier distant-sector design. The pilot controls show poor sensitivity to Earth-radius injections; this search cannot establish their absence or survey completeness.

Raw failure audit: TIC72660236 and287033641 in sector51,301578140 in46 and139343242 in46 have no finite selected KSPSAP flux/errors. For139343242, sector45 has2794 usable positive-flux quality-zero rows; the failure in46 prevented loading47. This is an incomplete target, not a nondetection. Preserve the failed run; a separately labeled recovery can use valid discovery data while keeping the original reserved sector untouched. No raw values or gates were changed.

`checkpoint-123-verification.json` independently reconciles frozen targets, source/raw hashes, result summaries and both policy queues. `errors.json` records all downloaded discovery sectors of failed targets, including the absent sector47. The error auditor initially assumed one discovery sector, then attempted to open the unrequested47 file; it now records the actual multi-sector failure state explicitly. No scientific algorithm changed and no new pytest claim is made.

Next: recover usable discovery sectors of TIC139343242 under an explicit error-recovery manifest, retaining the original failed result and reserved data. Broader source/product selection remains open; these139 are only one scoped pool, not all TESS.
