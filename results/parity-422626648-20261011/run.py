from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-single-review-20261011/422626648-peak0/frozen.json');dp=Path('results/qlp-faint-midradius-single-remaining-20261011/targets/422626648.json');b=json.loads(fp.read_text())['best'];target=json.loads(dp.read_text())['target'];assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(fp),'discovery_sha256':sha(dp),'clock':b,'windows':[1.5,2.5],'policy':'Fixed existing primary clock, partition nearest-cycle parity without retiming. Measure both families with existing fixed_measure at2P. All usable events retained. Two detrending windows; no independent data, calibrated model odds or classification.'})
fig,axes=plt.subplots(2,2,figsize=(11,8),constrained_layout=True);rows=[]
for j,window in enumerate([1.5,2.5]):
 t,y,e,data=load_qlp(target,Path('data'),window=window,bin_minutes=0);cycle=np.rint((t-b['transit_time'])/b['period']).astype(int);families=[]
 for parity in [0,1]:
  mask=cycle%2==parity;epoch=b['transit_time']+parity*b['period'];m=fixed_measure(t[mask],y[mask],e[mask],2*b['period'],epoch,b['duration']);families.append(m)
  phase=(t[mask]-epoch+b['period'])%(2*b['period'])-b['period'];ax=axes[j,parity];ax.scatter(phase*24,(y[mask]-1)*1e6,s=3,alpha=.25);ax.set_xlim(-2,2);ax.set_ylim(-60000,30000);ax.set_title(f'Window{window}d, parity{parity}');ax.set_xlabel('Hours from fixed center');ax.set_ylabel('Flux residual ppm')
  ev=m['events'];print(window,parity,len(ev),m['total'],m['event_scatter_error'])
 x,z=[f['total'] for f in families];delta=x['depth']-z['depth'];formal=float(np.hypot(x['error'],z['error']));scatter=None if any(f['event_scatter_error'] is None for f in families) else float(np.hypot(*[f['event_scatter_error'] for f in families]));rows.append({'window':window,'data':data,'families':families,'depth_difference':delta,'formal_error':formal,'formal_sigma':delta/formal,'event_scatter_error':scatter,'event_scatter_sigma':None if scatter is None else delta/scatter})
fig.savefig(out/'comparison.png',dpi=140);save_json(out/'results.json',{'rows':rows,'limits':'Conditional fixed-clock parity comparison. Formal errors omit correlated systematics; event scatter is descriptive, not a calibrated binary test. Equal depths cannot exclude a binary. Same opened data.'})
