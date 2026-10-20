from pathlib import Path
import json
import numpy as np
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha
out=Path(__file__).parent;fp=out/'frozen.json';f=json.loads(fp.read_text());b=f['best'];dis=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/425293543.json');target=json.loads(dis.read_text())['target'];held=json.loads((out/'heldout.json').read_text());rows=[]
for s in (53,54):
 t,y,e,data=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0);controls=[]
 for k in range(1,50):
  shift=k*b['period']/50
  if min(shift,b['period']-shift)<2*b['duration']:continue
  m=fixed_measure(t,y,e,b['period'],b['transit_time']+shift,b['duration'])
  if m['total'] is not None:controls.append({'phase':k/50,'measurement':m})
 old=next(v for v in held if v['sector']==s)
 assert np.allclose([v['measurement']['total']['snr'] for v in controls],old['phase_control_snrs'])
 best=max(controls,key=lambda v:v['measurement']['total']['snr']);assert best['phase']==.1
 rows.append({'sector':s,'selected_control':best,'data':data})
save_json(out/'shift-measurement.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(fp),'heldout_sha256':sha(out/'heldout.json'),'rows':rows,'limits':'Reproduces already-opened phase controls; selected shift is post-hoc and cannot replace failed preregistered ephemeris validation. No period refit or physical-cause inference.'})
print([(v['sector'],v['selected_control']['measurement']['total']) for v in rows])
