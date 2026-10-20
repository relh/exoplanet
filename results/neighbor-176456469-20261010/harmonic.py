"""Post-selection 2/3-period diagnostic, without refitting timing."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
f=Path('results/qlp-faint-sector103-followup-20261010/176456470-peak2/frozen.json')
b=json.loads(f.read_text())['best'];period=b['period']*2/3
obs=out/'observations.json';products={str(int(r['sequence_number'])):r for r in json.loads(obs.read_text())}
save_json(out/'harmonic-plan.json',{'utc':now(),'period':period,'epoch':b['transit_time'],'duration':b['duration'],'frozen_sha256':sha(f),'script_sha256':sha(Path(__file__)),'observations_sha256':sha(obs),'policy':'Post-selection 2/3 of frozen harmonic period, unchanged epoch/duration. Motivated by three dips and original odd/even flag. No refitting, no independent prediction or calibrated binary classification.'})
rows=[]
for sector in [103,65]:
 t,y,e,data=load_qlp({'tic':176456469,'training_sectors':[sector],'qlp_products':products,'estimate_missing_errors':True},Path('data'),bin_minutes=0)
 a=fixed_measure(t,y,e,period,b['transit_time'],b['duration']);c=fixed_measure(t,y,e,period,b['transit_time']+period/2,b['duration'])
 rows.append({'sector':sector,'data':data,'phase0':a,'phase_half':c});print(sector,a['total'],c['total'])
save_json(out/'harmonic-results.json',rows)
