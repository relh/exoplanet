from pathlib import Path
import json
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;frozen=Path('results/qlp-faint-sector72-recovery-20261010/26587095/targets/26587095.json');b=json.loads(frozen.read_text())['screened_peaks'][0]['best'];b=dict(b,transit_time=b['transit_time']+3*b['period'],period=100.)
req={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':['26587084']},{'paramName':'provenance_name','values':['QLP']}]},'format':'json','pagesize':50000,'page':1}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'request':req,'frozen_sha256':sha(frozen),'script_sha256':sha(Path(__file__)),'sectors':[71],'policy':'Neighbor selected from Sector71 single-event image. Fixed observed event center and duration; artificial100day isolation period is not a physical period. No refitting; same image epochs, not independent observations.'})
try:
 rows,meta=mast_query(req,Path('data/catalogs/qlp-26587084-20261010.json'));save_json(out/'observations.json',rows);save_json(out/'source.json',meta)
 products={str(int(r['sequence_number'])):r for r in rows}
 results=[]
 for sector in [71]:
  r={'sector':sector}
  try:
   target={'tic':26587084,'training_sectors':[sector],'qlp_products':products,'estimate_missing_errors':True}
   t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0)
   r.update(status='measured',data=data,primary=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']),half_phase=fixed_measure(t,y,e,b['period'],b['transit_time']+b['period']/2,b['duration']))
  except Exception as exc:r.update(status='error',error=repr(exc))
  results.append(r);save_json(out/'results.json',results);print(sector,r['status'],r.get('primary',{}).get('total',r.get('error')),r.get('half_phase',{}).get('total'),flush=True)
except Exception as exc:save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
