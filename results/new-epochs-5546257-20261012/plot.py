from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());fig,axs=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
for i,s in enumerate([89,99]):
 for j,c in enumerate(plan['clocks']):
  ax=axs[i,j];b=c['best']
  for w in plan['windows']:
   a=np.load(p/f's{s}-w{w}.npz');phase=(a['t']-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.5,.5,51);xs=[];ys=[];es=[]
   for lo,hi in zip(edges[:-1],edges[1:]):
    m=(phase>=lo)&(phase<hi)
    if m.any():xs.append((lo+hi)/2);ys.append(np.average(a['y'][m],weights=1/a['e'][m]**2));es.append(np.sqrt(1/np.sum(1/a['e'][m]**2)))
   ax.errorbar(xs,np.array(ys)*1e6-1e6,yerr=np.array(es)*1e6,fmt='.',label=f'{w}d detrend')
  ax.axvspan(-b['duration']/2,b['duration']/2,color='gray',alpha=.15);ax.set(title=f'Sector{s}: {c["name"]}',xlabel='Days from unchanged prediction',ylabel='Relative flux, ppm');ax.legend()
fig.savefig(p/'fixed-clocks.png',dpi=130)
