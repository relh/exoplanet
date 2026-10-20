from pathlib import Path
import csv
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
q="SELECT pl_name,tic_id,pl_orbper,pl_orbpererr1,pl_orbpererr2,pl_tranmid,pl_tranmiderr1,pl_tranmiderr2,pl_trandur,pl_trandep,pl_refname FROM ps WHERE default_flag=1 AND pl_name IN ('TOI-1680 b','TOI-715 b','TOI-2120 b','TOI-2266 b')"
p=Path('data/catalogs/faint-control-transit-truth-20261010.csv');params={'query':q,'format':'csv'};save_json(out/'truth-request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__))})
try:
 m=fetch('https://exoplanetarchive.ipac.caltech.edu/TAP/sync',p,params);save_json(out/'truth-source.json',m);r=list(csv.DictReader(p.open()));assert len(r)==4;save_json(out/'truth.json',r);print(r,flush=True)
except Exception as exc:save_json(out/'truth-error.json',{'utc':now(),'error':repr(exc)});raise
