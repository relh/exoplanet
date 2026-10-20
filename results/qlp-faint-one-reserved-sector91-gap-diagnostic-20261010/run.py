"""Post-selection fixed-ephemeris sensitivity to the visibly noisy gap-return interval."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
assert not (out/'plan.json').exists()
files=sorted(Path('results').glob('qlp-faint-one-reserved-sector91-pilot*followup-20261010/*/frozen.json'))
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'interval_btjd':[3787,3789],'frozen_hashes':{str(p):sha(p) for p in files},'policy':'Post-selection sensitivity diagnostic motivated by visual burst after large gap. Native cadence, fixed frozen ephemeris, no refit and no opening additional reserved data. This mask is not a preregistered rejection rule; lost event coverage must be considered. Independent epochs and source attribution still required.'})
rows=[]
for p in files:
 f=json.loads(p.read_text());b=f['best'];d=Path('results/qlp-faint-one-reserved-sector91-pilot-20261010/targets')/f"{f['tic']}.json"
 target=json.loads(d.read_text())['target'];t,y,e,ev=load_qlp(target,Path('data'),bin_minutes=0)
 keep=(t<3787)|(t>3789)
 full=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])
 cut=fixed_measure(t[keep],y[keep],e[keep],b['period'],b['transit_time'],b['duration'])
 row={'tic':f['tic'],'peak_index':f['peak_index'],'frozen':str(p),'ra':target['star']['ra'],'dec':target['star']['dec'],'n_full':len(t),'n_retained':int(keep.sum()),'data':ev,'full':full,'excluding_interval':cut}
 rows.append(row);save_json(out/'progress.json',rows)
 print(f['tic'],f['peak_index'],full['total'],cut['total'],'supported',full['supported_events'],cut['supported_events'],flush=True)
save_json(out/'results.json',rows)
