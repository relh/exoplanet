from pathlib import Path
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json
out=Path(__file__).parent
q={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':['80387959','80387965','80387961']},{'paramName':'provenance_name','values':['TGLC']}]},'format':'json','pagesize':1000,'page':1}
try:
 rows,source=mast_query(q,Path('data/targeting/tglc-80387959-obs.json'));save_json(out/'observations.json',{'rows':rows,'source':source});print(rows)
except Exception as exc:save_json(out/'query-error.json',{'request':q,'error':repr(exc)})
