from pathlib import Path
from urllib.parse import urlencode
from exoplanet.archive import mast_query
from exoplanet.pipeline import fetch,save_json
out=Path(__file__).parent
request={'service':'Mast.Catalogs.Tic.Cone','params':{'ra':139.202343,'dec':-49.30149,'radius':.01},'format':'json','pagesize':10000,'page':1}
try:
 rows,meta=mast_query(request,Path('data/rv/hd297396-tic.json'));save_json(out/'tic.json',rows);save_json(out/'tic-source.json',meta);print([(r['ID'],r['Tmag'],r['ra'],r['dec'],r.get('GAIA')) for r in rows if (r.get('Tmag') or 99)<13],flush=True)
except Exception as e:save_json(out/'tic-error.json',{'error':str(e)})
q="select basic.main_id,basic.ra,basic.dec,ident.id from basic join ident on basic.oid=ident.oidref where basic.oid in (select oidref from ident where id='HD 297396')"
u='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?'+urlencode({'request':'doQuery','lang':'adql','format':'csv','query':q})
try:
 p=Path('data/rv/hd297396-simbad.csv');m=fetch(u,p);save_json(out/'simbad-source.json',m);print(p.read_text(),flush=True)
except Exception as e:save_json(out/'simbad-error.json',{'error':str(e)})
