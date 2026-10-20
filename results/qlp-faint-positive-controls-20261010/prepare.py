"""Metadata-only known-planet controls, distinct from discovery candidates."""
from pathlib import Path
import json,csv
from exoplanet.archive import mast_query,qlp_observations
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;ids=[259168516,271971130,389900760,8348911]
p=Path('results/selection-small-stars-20261009/catalog_confirmed.csv');known=[r for r in csv.DictReader(p.open()) if int(r['tic_id'].replace('TIC','').strip()) in ids]
save_json(out/'plan.json',{'utc':now(),'tics':ids,'known_rows':known,'catalog_sha256':sha(p),'script_sha256':sha(Path(__file__)),'policy':'Four known-planet systems proposed for fainter small-star controls. Verify TIC properties/QLP availability before sampling. These are controls, not discovery or independent confirmation.'})
req={'service':'Mast.Catalogs.Filtered.Tic.Rows','params':{'columns':'ID,ra,dec,Tmag,rad,Teff,d,contratio,disposition,duplicate_id','filters':[{'paramName':'ID','values':list(map(str,ids))}]},'format':'json','pagesize':100,'page':1}
try:
 rows,meta=mast_query(req,Path('data/catalogs/faint-positive-controls-tic-20261010.json'));assert {int(r['ID']) for r in rows}==set(ids);save_json(out/'stars.json',rows);save_json(out/'stars-source.json',meta)
 obs,meta=qlp_observations(ids,Path('data/catalogs/faint-positive-controls-qlp-20261010.json'));save_json(out/'observations.json',obs);save_json(out/'observations-source.json',meta)
 print([(r['ID'],r['Tmag'],r['rad']) for r in rows],flush=True)
except Exception as exc:save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
