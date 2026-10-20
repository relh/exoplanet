"""Post-selection influence check; no refitting and no altered discovery result."""
from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
fp=Path('results/qlp-faint-sector97-coverage-followup-20261010/250389607-peak0/frozen.json');f=json.loads(fp.read_text());b=f['best']
dp=Path('results/qlp-faint-sector97-expanded-20261010/targets/250389607.json');target=json.loads(dp.read_text())['target']
t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0)
base=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])
np.testing.assert_allclose(base['total']['depth'],f['training_measurement']['total']['depth'],rtol=1e-12)
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
inside=np.flatnonzero(abs(phase)<b['duration']/2)
results=[]
for idx in inside:
 keep=np.arange(len(t))!=idx
 m=fixed_measure(t[keep],y[keep],e[keep],b['period'],b['transit_time'],b['duration'])
 results.append({'omitted_index':int(idx),'time_btjd':float(t[idx]),'flux':float(y[idx]),'error':float(e[idx]),'measurement':m})
save_json(out/'influence.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(fp),'discovery_sha256':sha(dp),'data':data,'baseline':base,'leave_one_in_window_point_out':results,'limits':'Post-selection diagnostic of every in-window point; no ephemeris/duration refitting. Does not justify editing the original light curve or establish a false-alarm probability.'})
r=min(results,key=lambda r:r['measurement']['total']['snr']);print('most influential',r)
