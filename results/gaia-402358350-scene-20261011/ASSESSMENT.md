# TIC402358350: Gaia scene catalogs do not resolve the host

Six explicitly selected TIC sources produce nine Gaia DR3 neighborhood candidates. The target and close image competitors have no returned Gaia variability-classifier or eclipsing-binary entries. The only classified variable is the already known48.1arcsec neighbor TIC402358249, classified DSCT|GDOR|SXPHE. These limited catalog results neither explain the11.77-day dips nor exclude unlisted eclipsing binaries or other variability. Keep the signal's existing unresolved assessment.

## Identity reconciliation

TIC's Gaia identifiers were treated as DR2 and queried through `gaiadr3.dr2_neighbourhood`. Every returned relationship was retained before querying all mapped DR3 IDs. The neighborhood table is not a unique crossmatch. Its angular-distance unit is **mas**, independently read from the Gaia TAP schema and retained in [metadata.json](metadata.json).

| TIC | DR2 ID | Returned DR3 candidates; neighborhood distance |
|---|---|---|
|402358350 (target)|4318715445843296256|same ID;0.206mas|
|402358383|4318715445801415040|same ID;0.075mas; also4318715445843287040 at1376.513mas|
|1918682446|4318715445801459200|4318715445843652864 at619.893mas and4318715445847541248 at1369.019mas; neither has proper-motion propagation|
|1918682563|4318715480203031936|same ID;0.292mas|
|1918682448|4318715445801475840|same ID;0.078mas; also4318715445801475968 at1454.498mas|
|402358249 (known nearby variable)|4318716236117290496|same ID;0.065mas|

The small-distance same-ID relationships are strong catalog associations; ambiguous extra relationships remain in the evidence rather than silently selecting a single match. TIC1918682446 in particular has no same-ID DR3 entry in the returned neighborhood and two alternatives. This may affect catalog-based scene assumptions, but this metadata-only review does not refit images or determine whether a faint entry is a physical companion, unrelated star or catalog artifact.

## Variability and source information

All nine mapped source records were returned successfully. The sole classifier result is Gaia4318716236117290496, DSCT|GDOR|SXPHE, classifier score0.46657. This agrees exactly with the previously saved VSX name and class for the48.1arcsec neighbor, not the target. The score is not an exoplanet probability. No eclipsing-binary rows were returned for any of the nine IDs, so this check supplies no Gaia binary period to compare with the TESS clock.

Target RUWE is0.9996; the close competing TIC1918682563 has RUWE2.9295. Such catalog fit diagnostics do not diagnose a binary or validate a single host. Missing source parameters for the faint alternatives remain missing. No nominal radius, distance or color is elevated to a validated stellar model here.

Only the known pulsator has `has_epoch_photometry=true` and `phot_variable_flag=VARIABLE`; the other eight have false/NOT_AVAILABLE. No epoch photometry was downloaded. NOT_AVAILABLE is absence of catalog variability information, not evidence of constant flux.

## Reproduction and scope

[plan.json](plan.json) preserves source selection, the full selected TIC records, parent-catalog hash and discovery image-assessment hashes. [query.py](query.py) records requests, URLs, timestamps and raw-response hashes for all four Gaia tables; raw CSVs remain in ignored `data/catalogs/gaia-402358350-scene-*`. [Verification](verification.json) reconciles raw hashes, CSV/JSON records, selection/identity joins and all9 returned DR3 records. The additional metadata and prior VSX identity checks are also reproduced by `uv run python results/gaia-402358350-scene-20261011/verify.py`.

This is a restricted check of explicitly selected image competitors and the known variable, not an exhaustive field/binary census. It does not validate source localization, statistical planet odds or novelty. No light curves, pixels or epoch flux were downloaded; concurrent photometric investigations own those observations separately.
