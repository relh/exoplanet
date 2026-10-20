"""Post-hoc refinement of four already-opened epochs for source localization."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training,fixed_measure
out=Path(__file__).parent;p=Path('results/campaign-qlp-full-pool-20261010/targets/314649431.json');d=json.loads(p.read_text());f=Path('results/qlp-full-pool-followup-20261010/314649431-peak0/frozen.json');b=json.loads(f.read_text())['best']
target=dict(d['target'],training_sectors=[15,56,82,83],heldout_sectors=[])
save_json(out/'plan.json',{'utc':now(),'target':target,'discovery_sha256':sha(p),'original_frozen_sha256':sha(f),'script_sha256':sha(Path(__file__)),'policy':'All four QLP epochs already opened. Fit for localization only; no independent or blind validation. Original failed/inconclusive checks retained.'})
t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0);best,ranges=refine_training(t,y,e,b,seed_baseline=d['clean_baseline_days'])
save_json(out/'fit.json',{'utc':now(),'best':best,'timing_ranges':ranges,'data':data,'policy':'Post-hoc all-opened-epoch fit, not an independently validated ephemeris.'})
rows=[]
for s in target['training_sectors']:
 t,y,e,data=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0);rows.append({'sector':s,'data':data,'measurement':fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration'])})
save_json(out/'measurements.json',rows)
print(best,flush=True)
for r in rows:print(r['sector'],r['measurement']['total'],flush=True)
