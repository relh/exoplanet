from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());h=json.loads((p/'heldout.json').read_text());z=np.load(p/'heldout-photometry.npz');t,y,e=z['time'],z['flux'],z['error'];fig,axes=plt.subplots(2,1,figsize=(11,7),constrained_layout=True)
for ax,b,title in [(axes[0],f['best'],'Nominal frozen clock'),(axes[1],dict(period=h['profile_best']['period'],transit_time=h['profile_best']['epoch'],duration=f['best']['duration']),'Maximum of nine pre-saved timing alternatives')]:
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;lim=3*b['duration'];edges=np.linspace(-lim,lim,51);x=[];v=[];err=[]
 for lo,hi in zip(edges[:-1],edges[1:]):
  m=(phase>=lo)&(phase<hi)
  if m.any():x.append((lo+hi)*12);v.append(np.average(y[m]-1,weights=1/e[m]**2)*1e6);err.append(1e6/np.sqrt(np.sum(1/e[m]**2)))
 ax.plot(phase*24,(y-1)*1e6,'.',ms=1,alpha=.1);ax.errorbar(x,v,yerr=err,fmt='k.-');ax.axvspan(-b['duration']*12,b['duration']*12,alpha=.1);ax.set(xlim=(-lim*24,lim*24),ylim=(-600,600),xlabel='Hours from predicted dip',ylabel='Flux residual (ppm)',title=title)
fig.suptitle('TIC469309982 reserved sector64: correlated profile maximum is not calibrated significance');fig.savefig(p/'reserved-comparison.png',dpi=120)
