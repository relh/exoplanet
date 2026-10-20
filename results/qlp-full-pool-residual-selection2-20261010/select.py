"""Freeze remaining bounded residual-search cohort before residual searches."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;assert not (out/'selected.json').exists()
assert json.loads(Path('results/campaign-qlp-full-pool-20261010/run.json').read_text())['status']=='complete'
prior=set(json.loads(Path('results/qlp-full-pool-residual-selection1-20261010/selected.json').read_text()))
rows=[]
for p in Path('results/campaign-qlp-full-pool-20261010/targets').glob('*.json'):
 if str(p) in prior:continue
 d=json.loads(p.read_text());b=d.get('best',{})
 if d['status']!='screened' or b.get('depth_snr',0)<8:continue
 if any(set(k['flags'])<={'crowding_or_missing_crowding'} for k in d.get('screened_peaks',[])):continue
 if 2*b['duration']/b['period']>.18:continue
 rows.append((d['median_scatter_floor_ppm'],d['tic'],p))
rows.sort();selected=rows[:300]
save_json(out/'selected.json',[str(p) for _,_,p in selected])
save_json(out/'plan.json',{'utc':now(),'n_eligible_snapshot':len(rows),'n_selected':len(selected),'selected':[{'tic':tic,'noise_ppm':noise,'path':str(p),'sha256':sha(p)} for noise,tic,p in selected],'policy':'Remaining eligible cohort after full-pool completion, excluding first300-star selection: dominant SNR>=8, no original crowding-only review peak, expected mask duty <=18%, sort by recorded scatter floor then TIC. At most2 rounds; enforce actual20% cumulative mask cap and200point minimum. Training only. Extra search trials and noise-based sample selection prevent completeness or false-alarm claims. No dominant feature is classified as instrumental or planetary by masking.'})
print('selected',len(selected),'eligible',len(rows))
