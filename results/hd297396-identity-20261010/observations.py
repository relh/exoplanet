from pathlib import Path
from urllib.parse import urlencode
from exoplanet.archive import mast_query
from exoplanet.pipeline import fetch,save_json
out=Path(__file__).parent
q='select * from toi where tid=293547742'
u='https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urlencode({'query':q,'format':'csv'})
p=Path('data/rv/hd297396-toi-20261010.csv');m=fetch(u,p);save_json(out/'toi-source.json',m);print(p.read_text(),flush=True)
r={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':['293547742']},{'paramName':'provenance_name','values':['QLP','TESS-SPOC','SPOC']}]},'format':'json','pagesize':50000,'page':1}
rows,m=mast_query(r,Path('data/rv/hd297396-observations.json'));save_json(out/'observations.json',rows);save_json(out/'observations-source.json',m);print([(x['sequence_number'],x['provenance_name']) for x in rows],flush=True)
