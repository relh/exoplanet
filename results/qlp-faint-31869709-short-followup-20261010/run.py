"""Post-hoc harmonic model fitted only to original training, then frozen."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure,refine_training,prediction_spread
out=Path(__file__).parent
source=Path('results/qlp-faint-expanded-20261010/targets/31869709.json')
original=Path('results/qlp-faint-expanded-followup-20261010/31869709-peak2/frozen.json')
d=json.loads(source.read_text());old=json.loads(original.read_text());seed=dict(old['best']);seed['period']/=3
sectors=[13,61]
assert all(s in d['target']['heldout_sectors'] and s not in old['heldout_sectors'] for s in sectors)
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'source_sha256':sha(source),'original_sha256':sha(original),'script_sha256':sha(Path(__file__)),'seed':seed,'heldout_sectors':sectors,'policy':'Post-hoc shorter-period model from original training only. Existing refinement routine, original failed detrending gate retained. Select nearest reserved sector before and after training, excluding already opened1/2. Freeze before fetching heldout data. Original heldout checks remain distinct; no claim of novelty or source attribution.'})
t,y,e,data=load_qlp(d['target'],Path('data'),bin_minutes=0)
b,ranges=refine_training(t,y,e,seed)
f={'utc':now(),'best':b,'timing_ranges':ranges,'training_data':data,'training_measurement':fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']),'previously_cached':{str(s):Path(f'data/qlp/31869709-s{s:04d}.fits').exists() for s in sectors}}
save_json(out/'frozen.json',f);print('frozen',b,'cached',f['previously_cached'],flush=True)
rows=[]
for sector in sectors:
 row={'sector':sector,'started_utc':now()}
 try:
  t,y,e,data=load_qlp(dict(d['target'],training_sectors=[sector]),Path('data'),bin_minutes=0)
  m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,ranges)
  row.update(status='measured',data=data,measurement=m,timing_spread_days=spread,timing_precise=spread<b['duration']/2 and not ranges['search_boundary_hit'],expected_formal_snr=None if m['total'] is None else b['depth']/m['total']['error'])
 except Exception as exc:row.update(status='error',error=repr(exc))
 row['finished_utc']=now();rows.append(row);save_json(out/'progress.json',rows)
 print(sector,{k:v for k,v in row.items() if k not in ['data','measurement']},row.get('measurement',{}).get('total'),flush=True)
save_json(out/'results.json',rows)
