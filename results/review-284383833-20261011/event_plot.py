from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import read_curve,sha,save_json,now
O=Path(__file__).parent;r=json.loads((O/'discovery.json').read_text());b=r['best']
fig,axes=plt.subplots(3,3,figsize=(13,9),sharex=True)
for j,n in enumerate([0,2,3]):
 center=b['transit_time']+n*b['period'];s=24 if n==0 else 25;p=Path(f'data/lightcurves/s{s:04d}-284383833.fits');t,f,e,_=read_curve(p);a=abs(t-center)<1.5
 axes[0,j].plot(t[a]-center,(f[a]/np.median(f[a])-1)*1e6,'.',ms=3);axes[0,j].set_title(f'Event{n}, sector{s}, raw quality flux')
 for i,w in enumerate([1.5,2.5],1):
  z=np.load(O/f'w{w}.npz');t,y,e=[z[k] for k in ['t','y','e']];a=abs(t-center)<1.5;axes[i,j].errorbar(t[a]-center,(y[a]-1)*1e6,e[a]*1e6,fmt='.',ms=3,lw=.4);axes[i,j].set_title(f'{w}d detrending')
 for i in range(3):axes[i,j].axvspan(-.09,.09,color='orange',alpha=.2);axes[i,j].set_ylabel('Relative flux(ppm)');axes[i,j].set_xlabel('Days from original center')
fig.tight_layout();fig.savefig(O/'events.png',dpi=150)
save_json(O/'plot-provenance.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),inputs={str(p):sha(p) for p in [O/'discovery.json',O/'w1.5.npz',O/'w2.5.npz']},purpose='Display existing original-clock discovery events only; raw quality-selected flux median-normalized separately in each display window. No timing fit.'))
