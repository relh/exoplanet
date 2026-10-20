from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha
p=Path(__file__).parent;b=json.loads(Path('results/source-check-106583384-20261012/frozen.json').read_text())['best'];r=json.loads((p/'fits.json').read_text());count=0
for row in r['sectors']:
 s=row['sector'];z=np.load(p/f's{s}-images.npz')
 with fits.open(f'data/pixels/106583384-s{s:04d}.fits') as h:
  a=h[1].data;valid=np.isfinite(a['TIME']);t=np.array(a['TIME'][valid],float);f=np.array(a['FLUX'][valid],float);e=np.array(a['FLUX_ERR'][valid],float);q=a['QUALITY'][valid]
 phase=np.remainder(t-b['transit_time']+b['period']/2,b['period'])-b['period']/2;num=np.rint((t-b['transit_time'])/b['period']).astype(int);ds=[];vs=[]
 for i,event in enumerate(row['events']):
  n=event['event'];inside=(q==0)&(num==n)&(abs(phase)<b['duration']/2);outside=(q==0)&(num==n)&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration'])
  d=np.nansum(f[outside],axis=0)/np.isfinite(f[outside]).sum(axis=0)-np.nansum(f[inside],axis=0)/np.isfinite(f[inside]).sum(axis=0)
  v=np.nansum(e[outside]**2,axis=0)/outside.sum()**2+np.nansum(e[inside]**2,axis=0)/inside.sum()**2
  np.testing.assert_allclose(z['event_differences'][i],d,atol=1e-10);np.testing.assert_allclose(z['event_variances'][i],v);ds.append(d);vs.append(v);count+=1
 ds=np.array(ds);vs=np.array(vs);w=np.where(vs>0,1/vs,0);np.testing.assert_allclose(z['difference'],(ds*w).sum(axis=0)/w.sum(axis=0),atol=1e-10)
for s in [7,61]:
 assert not Path(f'data/pixels/106583384-s{s:04d}.fits').exists()
save_json(p/'event-verification.json',dict(status='passed',independent_raw_event_means_and_stacks=count,extra_and_reserved_pixels_absent=[7,61],script_sha256=sha(Path(__file__)),limits='Checks arithmetic and present cache state, not physical source-model accuracy.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(4,5,figsize=(15,12),constrained_layout=True)
for row,axrow in zip(r['sectors'],[axes[:2].ravel(),axes[2:].ravel()]):
 z=np.load(p/f"s{row['sector']}-images.npz");tar=np.array(row['positions']['106583384'])+row['alignment'];nei=np.array(row['positions']['780959515'])+row['alignment']
 for a,ev,im in zip(axrow,row['events'],z['event_differences']):
  lim=np.max(abs(im));a.imshow(im,origin='lower',cmap='RdBu_r',vmin=-lim,vmax=lim);a.plot(*tar,'kx');a.plot(*nei,'g+');a.set_title(f"S{row['sector']} event{ev['event']}")
fig.suptitle('Individual differences: black target, green neighbor; separate color scales');fig.savefig(p/'events.png',dpi=120)
