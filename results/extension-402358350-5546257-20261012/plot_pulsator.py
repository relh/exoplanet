from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;d=json.loads((p/'pulsator-results.json').read_text());fig,axs=plt.subplots(1,2,figsize=(12,5),constrained_layout=True);labels=[]
for i,(k,w) in enumerate([('SAP',1.5),('SAP',2.5),('PDCSAP',1.5),('PDCSAP',2.5)]):
 labels.append(f'{k} {w}d')
 for nuisance,color,offset in [(False,'tab:blue',-.1),(True,'tab:orange',.1)]:
  r=next(r for r in d['fits'] if r['kind']==k and r['window']==w and r['sector']=='all' and r['nuisance']==nuisance);axs[0].errorbar(i+offset,1e6*r['depth'],yerr=1e6*r['error'],fmt='o',color=color,label=('Event baselines only' if not nuisance else '+ fixed-frequency sine/cosine') if i==0 else None)
 vals=[r['depth_change']*1e6 for r in d['injections'] if r['kind']==k and r['window']==w];axs[1].scatter(np.full(len(vals),i),vals,s=20)
axs[0].legend();axs[0].set(ylabel='Combined fixed-clock depth, ppm');axs[1].axhline(0,color='gray');axs[1].set(ylabel='Injected change in sector depth, ppm',title='1000-ppm sinusoid; four phases per sector')
for a in axs:a.set_xticks(range(4),labels,rotation=15)
fig.savefig(p/'pulsator-tests.png',dpi=130)
