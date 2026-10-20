from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import read_curve,sha,save_json,now
from exoplanet.search import flatten
p=Path(__file__).parent;r=json.loads((p/'discovery.json').read_text());b=r['best'];assert r['target']['training_sectors']==[33, 34]
plan=dict(created_utc=now(),discovery_sha256=sha(p/'discovery.json'),script_sha256=sha(Path(__file__)),sectors=[33, 34],unopened=[7, 61],windows=[1.5,2.5],clock=b,phase_bins_days=np.arange(-2,2.0001,.1).tolist(),note='Exploratory morphology only, fixed discovery clock, no added observations or parameter fitting')
assert not (p/'plan.json').exists();save_json(p/'plan.json',plan)
fig,axes=plt.subplots(3,2,figsize=(13,10));out=[];arrays={}
for col,s in enumerate(plan['sectors']):
 raw=Path(f'data/lightcurves/s{s:04d}-106583384.fits');d=next(x for x in r['data'] if x['sector']==s);assert sha(raw)==d['source']['sha256'];t,f,e,star=read_curve(raw);assert star['ticid']==r['tic'] and star['sector']==s
 axes[0,col].plot(t,1e6*(f/np.median(f)-1),'.',ms=1);axes[0,col].set_title(f'Sector{s} quality-filtered corrected flux');axes[0,col].set_xlabel('BTJD')
 for row,w in enumerate(plan['windows'],1):
  tt,y,dy=flatten(t,f,e,window=w);phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2;bins=[]
  for lo,hi in zip(plan['phase_bins_days'][:-1],plan['phase_bins_days'][1:]):
   mask=(phase>=lo)&(phase<hi);n=int(mask.sum())
   if n:
    weights=1/dy[mask]**2;bins.append(dict(lo=lo,hi=hi,n=n,flux=float(np.average(y[mask],weights=weights)),error=float(1/np.sqrt(weights.sum()))))
  ax=axes[row,col];mask=abs(phase)<2;ax.plot(phase[mask],1e6*(y[mask]-1),'.',ms=1,alpha=.3);ax.errorbar([(x['lo']+x['hi'])/2 for x in bins],[1e6*(x['flux']-1) for x in bins],yerr=[1e6*x['error'] for x in bins],fmt='o',ms=3);ax.axvspan(-b['duration']/2,b['duration']/2,color='red',alpha=.1);ax.set_title(f'{w}d detrending; fixed2.468147d clock');ax.set_xlabel('Days from box center')
  out.append(dict(sector=s,window=w,bins=bins));arrays[f's{s}w{w}']=np.array([tt,y,dy])
for ax in axes.flat:ax.set_ylabel('Relative flux ppm')
fig.tight_layout();fig.savefig(p/'morphology.png',dpi=150);np.savez_compressed(p/'photometry.npz',**arrays);save_json(p/'morphology.json',dict(created_utc=now(),profiles=out))
