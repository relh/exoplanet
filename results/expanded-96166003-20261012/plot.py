from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;old=json.loads((O/'sector19-original-predictions.json').read_text());new=json.loads((O/'frozen-for59.json').read_text());fig,axs=plt.subplots(2,2,figsize=(11,7))
for i,(a,b) in enumerate(zip(old['rows'],new['rows'])):
 for j,(name,clock,label) in enumerate([(f"sector19-w{a['window']}",a['clock'],'Sector19 at original43/44 prediction'),(f"expanded-w{b['window']}",b['best'],'19/43/44 at expanded training fit')]):
  z=np.load(O/f'{name}.npz');p=clock['period'];phase=(z['t']-clock['transit_time']+p/2)%p-p/2;edges=np.linspace(-.5,.5,51);xs=[];ys=[];es=[]
  for lo,hi in zip(edges[:-1],edges[1:]):
   m=(phase>=lo)&(phase<hi)
   if m.any():w=1/z['e'][m]**2;xs.append((lo+hi)/2);ys.append((np.average(z['y'][m],weights=w)-1)*1e6);es.append(1/np.sqrt(w.sum())*1e6)
  ax=axs[i,j];ax.errorbar(xs,ys,yerr=es,fmt='.',lw=.7);ax.axvspan(-clock['duration']/2,clock['duration']/2,color='orange',alpha=.15);ax.axhline(0,color='gray',lw=.5);ax.set_title(f"{label}\n{a['window']}day detrending");ax.set_xlabel('Days from predicted/fitted center');ax.set_ylabel('Relative flux(ppm)')
fig.suptitle('TIC96166003: sector19 evaluated, then explicitly used for training;59 unopened');fig.tight_layout();fig.savefig(O/'comparison.png',dpi=150)
