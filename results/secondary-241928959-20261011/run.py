from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent
fp=Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json');dp=Path('results/qlp-faint-midradius-single-remaining-20261011/targets/241928959.json')
b=json.loads(fp.read_text())['best'];target=json.loads(dp.read_text())['target']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',dict(inputs={str(p):sha(p) for p in [fp,dp,Path(__file__),Path('src/exoplanet/followup.py')]},windows=[1.5,2.5],duration_factors=[1,2],phase=.5,limits='Same opened sector. Fixed half-phase only, no eccentric-secondary search. Two durations and detrending windows are sensitivity checks, not independent evidence.'))
rows=[];fig,axes=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
for i,window in enumerate([1.5,2.5]):
 t,y,e,data=load_qlp(target,Path('data'),window=window,bin_minutes=0)
 for j,factor in enumerate([1,2]):
  epoch=b['transit_time']+b['period']/2;duration=b['duration']*factor
  m=fixed_measure(t,y,e,b['period'],epoch,duration)
  phase=(t-epoch+b['period']/2)%b['period']-b['period']/2
  rows.append(dict(window=window,duration_factor=factor,measurement=m,data=data))
  np.savez_compressed(out/f'w{window}-d{factor}.npz',t=t,y=y,e=e,phase=phase)
  ax=axes[i,j];mask=abs(phase)<.2;ax.scatter(phase[mask]*24,(y[mask]-1)*100,s=3,alpha=.4);ax.axvspan(-duration*12,duration*12,alpha=.15);ax.set_title(f'Window {window}d; duration {duration}d');ax.set_xlabel('Hours from half-phase');ax.set_ylabel('Flux residual (%)')
save_json(out/'results.json',dict(rows=rows));fig.savefig(out/'secondary.png',dpi=140)
print([(r['window'],r['duration_factor'],r['measurement']['total'],len(r['measurement']['events'])) for r in rows])
