from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fp=Path('results/refinement-362222987-20261011/frozen.json');b=json.loads(fp.read_text())['best'];paths=[Path(f'data/lightcurves/s{s:04d}-362222987.fits') for s in [17,18]]
save_json(p/'plan.json',dict(created_utc=now(),clock=b,inputs={str(q):sha(q) for q in paths+[fp,Path(__file__)]},policy='Existing discovery data only, fixed refined clock. Same quality/finite positive masks for SAP and PDCSAP before separate identical detrending. Windows1.5/2.5days. Shared photons, no independent validation.'))
rows=[];fig,axes=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
for i,window in enumerate([1.5,2.5]):
 for j,kind in enumerate(['SAP','PDCSAP']):
  arrays=[];counts=[]
  for path in paths:
   with fits.open(path) as h:
    d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
    for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[key])&(d[key]>0)
    t,y,e=flatten(np.asarray(d['TIME'][mask],float),np.asarray(d[kind+'_FLUX'][mask],float),np.asarray(d[kind+'_FLUX_ERR'][mask],float),window=window)
    arrays.append((t,y,e));counts.append(dict(path=str(path),common_input_points=int(mask.sum()),clean_points=len(t)))
  t,y,e=[np.concatenate([a[k] for a in arrays]) for k in range(3)]
  m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);rows.append(dict(window=window,kind=kind,counts=counts,measurement=m));np.savez_compressed(p/f'{kind}-{window}.npz',t=t,y=y,e=e)
  phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;mask=abs(phase)<.4;axes[i,j].scatter(phase[mask]*24,(y[mask]-1)*1e6,s=5,alpha=.5);axes[i,j].axvspan(-b['duration']*12,b['duration']*12,alpha=.1);axes[i,j].set_title(f'{kind}, window{window}d');axes[i,j].set_xlabel('Hours from fixed dip');axes[i,j].set_ylabel('Flux residual ppm')
save_json(p/'results.json',dict(rows=rows));fig.savefig(p/'comparison.png',dpi=140);print([(r['kind'],r['window'],r['measurement']['total']) for r in rows])
