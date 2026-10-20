import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text())['rows'];fig,axes=plt.subplots(2,3,figsize=(13,7),sharex=True)
for ax,row in zip(axes.flat,r):
 z=np.load(O/f"{row['name']}.npz");b=row['best'];p=b['period'];phase=(z['tt']-b['transit_time']+p/2)%p-p/2;edges=np.linspace(-.4,.4,41);centers=[];means=[];errors=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  m=(phase>=lo)&(phase<hi)
  if m.sum():
   w=1/z['ee'][m]**2;centers.append((lo+hi)/2);means.append((np.average(z['yy'][m],weights=w)-1)*1e6);errors.append(1/np.sqrt(w.sum())*1e6)
 ax.errorbar(centers,means,yerr=errors,fmt='.',ms=4,lw=.7);ax.axvspan(-b['duration']/2,b['duration']/2,color='orange',alpha=.12);ax.axhline(0,color='gray',lw=.6);ax.set_title(f"Omit {row['excluded']} · window {row['window']}d\nP={p:.7f}d, SNR={row['measurement']['total']['snr']:.2f}");ax.set_xlabel('Days from train-only prediction');ax.set_ylabel('Relative flux (ppm)')
fig.suptitle('TIC469309982: retrospective omitted-season folds; all data previously seen');fig.tight_layout();fig.savefig(O/'folds.png',dpi=160)
