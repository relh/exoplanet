# TIC389918717: unusable sector retained; three-sector recovery

The original four-sector target task ended with an explicit data error. Sector37
contains1698rows but zero finite KSPSAP_FLUX values, including among the1399rows
with QUALITY=0. No uncertainty estimate can make this absent flux usable.
The missing-uncertainty fallback raised an insufficient-adjacent-samples error;
this is not a negative transit detection. Raw file hash and download provenance
are preserved in sector37-quality.json.

Sectors36,38and39 are usable. A separately frozen recovery plan searched those
three already-assigned training sectors with unchanged period and quality gates.
Its strongest peak has formal SNR5.52, below threshold. The original failed result
is retained in the running campaign, and recovery is stored separately here;
no reserved epochs were opened and the star must not be counted twice.

The recovery has narrower coverage than the planned four-sector search. It does
not establish equal sensitivity, exclude planets, or resolve unavailable data.
