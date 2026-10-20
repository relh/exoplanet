from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
for tic,sectors in [(96166003,[43,44]),(236317267,[24,25])]:
 out=Path(f'results/source-check-{tic}-20261011');f=json.loads((out/'frozen.json').read_text());assert sha(Path(f['source']))==f['source_sha256'];p,e,d=[f['best'][k] for k in ['period','transit_time','duration']];rows=[]
 for sector in sectors:
  o=Path(f'results/pixels-{tic}-s{sector}-20261011');r=json.loads((o/'localization.json').read_text());raw=Path(f'data/pixels/{tic}-s{sector:04d}.fits');assert sha(raw)==r['source']['sha256'];assert sha(out/'frozen.json')==r['frozen_sha256']
  with fits.open(raw) as h:
   a=h[1].data;t=np.asarray(a['TIME'],float);finite=np.isfinite(t);t=t[finite];flux=np.asarray(a['FLUX'][finite],float);err=np.asarray(a['FLUX_ERR'][finite],float);valid=a['QUALITY'][finite]==0
  ph=(t-e+p/2)%p-p/2;ev=np.rint((t-e)/p).astype(int);diffs=[];vs=[];nums=[]
  for n in np.unique(ev[valid&(abs(ph)<d/2)]):
   inside=valid&(ev==n)&(abs(ph)<d/2);base=valid&(ev==n)&(abs(ph)>d)&(abs(ph)<3*d)
   if inside.sum()<2 or base.sum()<5:continue
   diffs.append(np.nanmean(flux[base],axis=0)-np.nanmean(flux[inside],axis=0));vs.append(np.nansum(err[base]**2,axis=0)/base.sum()**2+np.nansum(err[inside]**2,axis=0)/inside.sum()**2);nums.append(int(n))
  diffs=np.array(diffs);v=np.array(vs);w=np.divide(1,v,out=np.zeros_like(v),where=v>0);wt=w.sum(axis=0);avg=np.divide((w*diffs).sum(axis=0),wt,out=np.zeros_like(wt),where=wt>0);sigma=np.sqrt(np.divide(1,wt,out=np.full_like(wt,np.inf),where=wt>0))
  saved=np.load(o/'images.npz');np.testing.assert_allclose(saved['event_differences'],diffs);np.testing.assert_allclose(saved['difference'],avg);np.testing.assert_allclose(saved['error'],sigma);assert nums==r['event_numbers'];rows.append(dict(sector=sector,events=len(nums),raw_sha256=sha(raw)))
 save_json(out/'verification.json',dict(verified_utc=now(),status='passed',script_sha256=sha(Path(__file__)),rows=rows,limits='Independent raw event/variance/stack arithmetic, same masks and estimator; not validation of localization or astrophysical origin.'))
 print(tic,rows)
