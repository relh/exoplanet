from pathlib import Path
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,now
out=Path(__file__).parent
save_json(out/'toi-error.json',dict(recorded_utc=now(),query='select * from toi where tid=293547742',error='HTTP504 Gateway Timeout; no fresh catalog result. Existing20261009TOI snapshot used explicitly.'))
r={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':['293547742']},{'paramName':'provenance_name','values':['QLP','TESS-SPOC','SPOC']}]},'format':'json','pagesize':50000,'page':1}
rows,m=mast_query(r,Path('data/rv/hd297396-observations.json'));save_json(out/'observations.json',rows);save_json(out/'observations-source.json',m);print([(x['sequence_number'],x['provenance_name']) for x in rows],flush=True)
