from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.campaign import load_training
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());f=json.loads((p/'frozen.json').read_text());o=json.loads(Path(plan['original_path']).read_text());matched=json.loads((p/'matched-original.json').read_text())['rows'][0]['best'];t,y,e,_=load_training(o['target'],Path('data'));expanded=np.load(p/'photometry.npz');held=np.load(p/'heldout-photometry.npz');fig,axes=plt.subplots(3,1,figsize=(11,10),constrained_layout=True)
for ax,tt,yy,b,title in zip(axes,[t,expanded['time'],held['time']],[y,expanded['flux'],held['flux']],[matched,f['best'],f['best']],['Original two sectors, local refinement','Six discovery sectors, local refinement','Reserved sector76 at unchanged expanded clock']):
 phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.15,.15,51);bx=[];by=[];inside=abs(phase)<.15
 for low,high in zip(edges[:-1],edges[1:]):
  ok=(phase>=low)&(phase<high)
  if ok.sum():bx.append((low+high)*12);by.append(np.median(yy[ok]-1)*1e6)
 ax.scatter(phase[inside]*24,(yy[inside]-1)*1e6,s=1,alpha=.14);ax.plot(bx,by,'k.-');ax.axvspan(-b['duration']*12,b['duration']*12,alpha=.1);ax.set_title(title);ax.set_xlabel('Hours from frozen/refined event');ax.set_ylabel('Flux residual (ppm)')
fig.suptitle('Known TOI-1435 b control: added-data signal and inconclusive reserved-sector check');fig.savefig(p/'comparison.png',dpi=120)
