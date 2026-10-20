from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;b=json.loads((p/'plan.json').read_text())['clocks'][0]['best'];fig,axes=plt.subplots(2,1,figsize=(11,7),constrained_layout=True)
for ax,path,title in [(axes[0],Path('results/followup-469309982-20261011/heldout-photometry.npz'),'Sector64: used to select among saved timing alternatives'),(axes[1],p/'photometry.npz','Sector63: subsequently opened, same fixed clock')]:
 z=np.load(path);t,y,e=z['time'],z['flux'],z['error'];ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;lim=3*b['duration'];edges=np.linspace(-lim,lim,51);xx=[];yy=[];ee=[]
 for l,r in zip(edges[:-1],edges[1:]):
  m=(ph>=l)&(ph<r)
  if m.any():xx.append((l+r)*12);yy.append(np.average(y[m]-1,weights=1/e[m]**2)*1e6);ee.append(1e6/np.sqrt(np.sum(1/e[m]**2)))
 ax.plot(ph*24,(y-1)*1e6,'.',ms=1,alpha=.1);ax.errorbar(xx,yy,yerr=ee,fmt='k.-');ax.axvspan(-b['duration']*12,b['duration']*12,alpha=.1);ax.set(xlim=(-lim*24,lim*24),ylim=(-600,600),xlabel='Hours from fixed prediction',ylabel='Flux residual (ppm)',title=title)
fig.suptitle('TIC469309982: selection data and subsequent test; no new timing fit');fig.savefig(p/'comparison.png',dpi=120)
