from pathlib import Path
import json
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,now
out=Path(__file__).parent/'cone';out.mkdir(exist_ok=True)
request={'service':'Mast.Catalogs.Tic.Cone','params':{'ra':76.027343,'dec':-.649175,'radius':.01},'format':'json','pagesize':10000,'page':1}
save_json(out/'request.json',{'utc':now(),'request':request,'reason':'Identify HD32564 using RVBank coordinates and HD identifier before selecting TESS data.'})
try:
 rows,meta=mast_query(request,Path('data/rv/hd32564-tic-cone-20261010.json'));save_json(out/'tic.json',rows);save_json(out/'tic-source.json',meta)
 matches=[r for r in rows if str(r.get('HD','')).strip()=='32564'];assert len(matches)==1,matches
 tic=int(matches[0]['ID']);save_json(out/'identity.json',matches[0]);print('identity',matches[0],flush=True)
 request={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':[str(tic)]},{'paramName':'provenance_name','values':['QLP','SPOC','TESS-SPOC']}]},'format':'json','pagesize':50000,'page':1}
 rows,meta=mast_query(request,Path('data/rv/hd32564-tess-observations-20261010.json'));save_json(out/'observations.json',rows);save_json(out/'observations-source.json',meta);print('observations',[(r['sequence_number'],r['provenance_name']) for r in rows],flush=True)
except Exception as exc:
 save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
