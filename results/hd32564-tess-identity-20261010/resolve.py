from pathlib import Path
from urllib.parse import urlencode
import csv,json
from exoplanet.pipeline import fetch,save_json,sha,now
from exoplanet.archive import mast_query
out=Path(__file__).parent
q="select basic.main_id,basic.ra,basic.dec,ident.id from basic join ident on basic.oid=ident.oidref where basic.oid in (select oidref from ident where id='HD 32564')"
u='https://simbad.cds.unistra.fr/simbad/sim-tap/sync?'+urlencode({'request':'doQuery','lang':'adql','format':'csv','query':q})
p=Path('data/rv/hd32564-simbad-20261010.csv')
try:
 meta=fetch(u,p);save_json(out/'simbad-source.json',meta);rows=list(csv.DictReader(p.open()));ids={r['id'] for r in rows};print('IDs',sorted(ids),flush=True)
 stars=json.loads((out/'cone/tic.json').read_text());matches=[s for s in stars if f'HIP {s.get("HIP")}' in ids or f'Gaia DR2 {s.get("GAIA")}' in ids or f'TIC {s["ID"]}' in ids]
 assert len(matches)==1,matches
 star=matches[0];save_json(out/'identity.json',{'utc':now(),'star':star,'simbad_ids':sorted(ids),'simbad_sha256':sha(p),'tic_source_sha256':sha(out/'cone/tic.json')});tic=int(star['ID'])
 request={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':[str(tic)]},{'paramName':'provenance_name','values':['QLP','SPOC','TESS-SPOC']}]},'format':'json','pagesize':50000,'page':1}
 obs,meta=mast_query(request,Path('data/rv/hd32564-tess-observations-20261010.json'));save_json(out/'observations.json',obs);save_json(out/'observations-source.json',meta);print('observations',[(r['sequence_number'],r['provenance_name']) for r in obs],flush=True)
except Exception as exc:
 save_json(out/'resolve-error.json',{'utc':now(),'error':repr(exc)});raise
