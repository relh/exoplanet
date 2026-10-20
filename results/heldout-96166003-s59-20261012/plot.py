from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;rows=json.loads((O/'results.json').read_text())['rows'];fig,axes=plt.subplots(2,2,figsize=(11,7))
for ax,row in zip(axes.flat,rows):
 z=np.load(O/f"w{row['window']}.npz");b=row['clock'];phase=(z['t']-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.5,.5,51);xx=[];yy=[];ee=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  m=(phase>=lo)&(phase<hi)
  if m.any():w=1/z['e'][m]**2;xx.append((lo+hi)/2);yy.append((np.average(z['y'][m],weights=w)-1)*1e6);ee.append(1/np.sqrt(w.sum())*1e6)
 ax.errorbar(xx,yy,yerr=ee,fmt='.',lw=.7);ax.axvspan(-b['duration']/2,b['duration']/2,color='orange',alpha=.15);ax.axhline(0,color='gray',lw=.5);ax.set_title(f"{row['family']} · {row['window']}day window\nNominal SNR{row['measurement']['total']['snr']:.2f}; timing-inconclusive");ax.set_xlabel('Days from frozen predicted center');ax.set_ylabel('Relative flux(ppm)')
fig.suptitle('TIC96166003 sector59: four prespecified clocks, no timing optimization');fig.tight_layout();fig.savefig(O/'comparison.png',dpi=150)
