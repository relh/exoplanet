from pathlib import Path
import json
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,now,sha
out=Path(__file__).parent
s=json.loads(Path('results/qlp-faint-one-reserved-sector91-pilot-20261010/targets/101436430.json').read_text())['target']['star']
r={'service':'Mast.Catalogs.Tic.Cone','params':{'ra':s['ra'],'dec':s['dec'],'radius':.05},'format':'json','pagesize':10000,'page':1}
save_json(out/'request.json',{'utc':now(),'request':r,'script_sha256':sha(Path(__file__))})
try:
 rows,meta=mast_query(r,Path('data/catalogs/neighbors-101436430-20261010.json'));save_json(out/'neighbors.json',rows);save_json(out/'source.json',meta);print('neighbors',len(rows),flush=True)
except Exception as exc:save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
