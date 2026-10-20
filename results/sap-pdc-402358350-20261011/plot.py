from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());b=p['clock'];fig,axs=plt.subplots(2,4,figsize=(15,7),sharex=True)
for i,w in enumerate([1.5,2.5]):
 for j,s in enumerate(p['sectors']):
  ax=axs[i,j]
  for kind in ['SAP','PDCSAP']:
   z=np.load(O/f'{kind}-{w}-s{s}.npz');phase=(z['t']-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.4,.4,25);xx=[];yy=[];ee=[]
   for lo,hi in zip(edges[:-1],edges[1:]):
    m=(phase>=lo)&(phase<hi)
    if m.any():ww=1/z['e'][m]**2;xx.append((lo+hi)/2);yy.append((np.average(z['y'][m],weights=ww)-1)*1e6);ee.append(1/np.sqrt(ww.sum())*1e6)
   ax.errorbar(xx,yy,yerr=ee,fmt='.-',ms=3,lw=.6,label=kind,alpha=.8)
  ax.axvspan(-b['duration']/2,b['duration']/2,color='gray',alpha=.1);ax.set_title(f'Sector{s}, window{w}d');ax.set_xlabel('Days from unchanged clock');ax.set_ylabel('Flux(ppm)');ax.legend(fontsize=8)
fig.suptitle('TIC402358350: aperture and corrected flux; same photons, fixed expanded primary clock');fig.tight_layout();fig.savefig(O/'comparison.png',dpi=140)
