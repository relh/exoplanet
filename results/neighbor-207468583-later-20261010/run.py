from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure,prediction_spread
out=Path(__file__).parent;frozen=Path('results/qlp-faint-expanded-followup-20261010/207468582-peak0/frozen.json');f=json.loads(frozen.read_text());b=f['best']
obs=Path('results/neighbor-207468583-20261010/observations.json');products={str(int(x['sequence_number'])):x for x in json.loads(obs.read_text())}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'frozen_sha256':sha(frozen),'observations_sha256':sha(obs),'best':b,'sectors':[83,86],'previously_cached':{str(s):Path(f'data/qlp/207468583-s{s:04d}.fits').exists() for s in [83,86]},'script_sha256':sha(Path(__file__)),'policy':'Later neighbor epochs selected after pixel and deeper neighbor dip evidence. Fixed target ephemeris, no retuning. Same neighbor may itself be blended; no planet or host claim.'})
rows=[]
for s in [83,86]:
 r={'sector':s}
 try:
  t,y,e,data=load_qlp({'tic':207468583,'training_sectors':[s],'qlp_products':products,'estimate_missing_errors':True},Path('data'),bin_minutes=0)
  m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,f['timing_ranges'])
  r.update(status='measured',data=data,measurement=m,timing_spread_days=spread,timing_precise=spread<b['duration']/2 and not f['timing_ranges']['search_boundary_hit'])
 except Exception as exc:r.update(status='error',error=repr(exc))
 rows.append(r);save_json(out/'results.json',rows);print(s,{k:v for k,v in r.items() if k!='data'},flush=True)
