"""Post-hoc dependent phase controls using the existing follow-up diagnostic."""
import json
from pathlib import Path
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
plan=json.loads((out/'plan.json').read_text());tic=320504102
p=Path(f'results/qlp-faint-expanded-20261010/targets/{tic}.json');target=json.loads(p.read_text())['target'];b=plan['best']
t,y,e,data=load_qlp(dict(target,training_sectors=[75]),Path('data'),bin_minutes=0)
controls=[]
for shift in np.arange(1,50)*b['period']/50:
 if min(shift,b['period']-shift)<2*b['duration']:continue
 m=fixed_measure(t,y,e,b['period'],b['transit_time']+shift,b['duration'])['total']
 if m is not None:controls.append({'phase_shift':float(shift/b['period']),'measurement':m})
save_json(out/'controls.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'data':data,'controls':controls,'policy':'Post-hoc same-period dependent phase controls after the fixed measurement; same diagnostic grid as standard follow-up. Not a survey false-alarm probability. No retuning of candidate ephemeris.'})
print(tic,'controls',len(controls),'maximum SNR',max(c['measurement']['snr'] for c in controls))
