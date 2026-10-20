from pathlib import Path
import json
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;frozen=Path('results/qlp-faint-one-reserved-sector87-pilot-followup-20261010/291207362-peak0/frozen.json');b=json.loads(frozen.read_text())['best']
req={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':['291207358']},{'paramName':'provenance_name','values':['QLP']}]},'format':'json','pagesize':50000,'page':1}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'request':req,'frozen_sha256':sha(frozen),'script_sha256':sha(Path(__file__)),'sectors':[87,33],'policy':'Neighbor selected from Sector 87 difference image. Fixed target ephemeris and duration, plus half-phase check. No refitting; same image epochs, not independent observations.'})
try:
 rows,meta=mast_query(req,Path('data/catalogs/qlp-291207358-20261010.json'));save_json(out/'observations.json',rows);save_json(out/'source.json',meta)
 products={str(int(r['sequence_number'])):r for r in rows}
 results=[]
 for sector in [87,33]:
  r={'sector':sector}
  try:
   target={'tic':291207358,'training_sectors':[sector],'qlp_products':products,'estimate_missing_errors':True}
   t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0)
   r.update(status='measured',data=data,primary=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']),half_phase=fixed_measure(t,y,e,b['period'],b['transit_time']+b['period']/2,b['duration']))
  except Exception as exc:r.update(status='error',error=repr(exc))
  results.append(r);save_json(out/'results.json',results);print(sector,r['status'],r.get('primary',{}).get('total',r.get('error')),r.get('half_phase',{}).get('total'),flush=True)
except Exception as exc:save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
