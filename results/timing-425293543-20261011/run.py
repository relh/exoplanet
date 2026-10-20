from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training,fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;fp=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/425293543-peak0/frozen.json');f=json.loads(fp.read_text());dp=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/425293543.json');d=json.loads(dp.read_text());seed=f['best'];groups={'early':[53,54],'training':[80,81],'joint':[53,54,80,81]}
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(fp),'discovery_sha256':sha(dp),'groups':groups,'seed':seed,'seed_baseline':d['clean_baseline_days'],'method':'Existing refine_training BLS with original discovery baseline controlling search width; existing preprocessing unchanged. All data already opened. Posthoc timing audit, no new validation or calibrated timing confidence.'})
rows={};curves={}
for name,sectors in groups.items():
 t,y,e,data=load_qlp(dict(d['target'],training_sectors=sectors),Path('data'),bin_minutes=0)
 best,ranges=refine_training(t,y,e,seed,seed_baseline=d['clean_baseline_days']);rows[name]={'best':best,'ranges':ranges,'data':data,'measurement':fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration'])};curves[name]=(t,y,e)
 save_json(out/'fits.json',rows);print(name,best,flush=True)
b=rows['joint']['best'];comparisons=[];fig,axes=plt.subplots(4,2,figsize=(12,12),constrained_layout=True)
for row,s in enumerate((53,54,80,81)):
 t,y,e,data=load_qlp(dict(d['target'],training_sectors=[s]),Path('data'),bin_minutes=0);item={'sector':s,'data':data}
 for col,(label,fit) in enumerate((('Original frozen',seed),('Exploratory joint',b))):
  phase=(t-fit['transit_time']+fit['period']/2)%fit['period']-fit['period']/2
  ax=axes[row,col];ax.scatter(phase,y,s=2,alpha=.4);ax.set_xlim(-.3,.3);ax.set_ylim(.75,1.1);ax.set_title(f'S{s}: {label}');ax.set_xlabel('Days from fitted eclipse center')
  item[label]=fixed_measure(t,y,e,fit['period'],fit['transit_time'],fit['duration'])
 comparisons.append(item)
fig.savefig(out/'comparison.png',dpi=140)
save_json(out/'comparison.json',{'rows':comparisons,'period_change_seconds':(b['period']-seed['period'])*86400,'fits_sha256':sha(out/'fits.json'),'plot_sha256':sha(out/'comparison.png'),'limits':'All-sector fitted comparison, not independent validation. BLS box-model/white-noise profile omits model mismatch, red noise and alias uncertainty. Cannot infer physical period variation or planetary nature.'})
