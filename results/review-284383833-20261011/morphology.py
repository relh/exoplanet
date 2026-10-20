from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;r=json.loads((O/'discovery.json').read_text());target=r['target'];b=r['screened_peaks'][0]['best'];assert target['training_sectors']==[24,25]
for s in [51,78]:assert not Path(f'data/lightcurves/s{s:04d}-284383833.fits').exists()
for s in [24,25]:assert Path(f'data/lightcurves/s{s:04d}-284383833.fits.json').exists()
save_json(O/'plan.json',dict(created_utc=now(),discovery_sha256=sha(O/'discovery.json'),sectors=[24,25],windows=[1.5,2.5],clock=b,policy='Discovery-only fixed original winning clock. No additional/refined clocks, no additional sectors or photometry downloads. Local morphology and existing screening diagnostics, not validation.',source_hashes={str(p):sha(p) for p in [Path(__file__),Path('src/exoplanet/campaign.py'),Path('src/exoplanet/followup.py'),Path('src/exoplanet/search.py')]}))
fig,axes=plt.subplots(2,2,figsize=(12,7));rows=[]
for j,w in enumerate([1.5,2.5]):
 t,y,e,ev=load_training(target,Path('data'),window=w);m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);rows.append(dict(window=w,measurement=m,data=ev));np.savez_compressed(O/f'w{w}.npz',t=t,y=y,e=e)
 axes[j,0].plot(t,(y-1)*1e6,'.',ms=.6);axes[j,0].set_ylabel(f'{w}d detrend flux(ppm)');axes[j,0].set_xlabel('BTJD')
 for v in m['events']:axes[j,0].axvline(v['center_btjd'],color='orange',lw=.5)
 ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.6,.6,61);xs=[];ys=[];es=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  a=(ph>=lo)&(ph<hi)
  if a.any():ww=1/e[a]**2;xs.append((lo+hi)/2);ys.append((np.average(y[a],weights=ww)-1)*1e6);es.append(1/np.sqrt(ww.sum())*1e6)
 axes[j,1].errorbar(xs,ys,yerr=es,fmt='.',ms=4,lw=.6);axes[j,1].axvspan(-b['duration']/2,b['duration']/2,color='orange',alpha=.12);axes[j,1].set_xlabel('Days from original predicted center');axes[j,1].set_ylabel('Flux(ppm)')
fig.suptitle('TIC284383833: discovery sectors24/25 only, P=13.0788462d');fig.tight_layout();fig.savefig(O/'discovery.png',dpi=150);save_json(O/'morphology.json',dict(plan_sha256=sha(O/'plan.json'),rows=rows))
