from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());b=json.loads(Path('results/source-check-5540688-20261011/frozen.json').read_text())['best'];assert sha(p/'run.py')==plan['script_sha256']
for path,d in plan['inputs'].items():assert sha(Path(path))==d
count=0
for s in r['sectors']:
 z=np.load(p/f"s{s['sector']}-models.npz");shape=z['scene'].shape;yy,xx=np.indices(shape,dtype=float)
 def solve(im,error,cols):
  cols=cols+[np.ones(shape),xx-xx.mean(),yy-yy.mean()];good=np.isfinite(im)&np.isfinite(error)&(error>0);A=np.stack([c[good]/error[good] for c in cols],axis=1);Y=im[good]/error[good];c,_,rank,_=lstsq(A,Y,lapack_driver='gelsy');assert rank==len(cols);return c,float(np.sum((Y-A@c)**2))
 diff,dc=solve(z['difference'],z['error'],[z['neighbor_template']])
 for case,cols in zip(s['models'],[[z['scene_template']],[z['other_template'],z['neighbor_template']]]):
  coef,chi=solve(z['scene'],np.ones(shape),cols);nf=coef[0]*r['catalog_flux_ratio'] if len(cols)==1 else coef[1];np.testing.assert_allclose(coef,case['coefficients'],rtol=1e-8,atol=1e-7);np.testing.assert_allclose([chi,nf,diff[0]/nf],[case['chi2'],case['neighbor_flux_coefficient'],case['fractional_dip']],rtol=1e-8);assert nf>0
 assert sha(Path(s['raw_path']))==s['raw_sha256'];assert sha(Path(f"results/prf-5540688-20261011/s{s['sector']}-images.npz"))==s['parent_images_sha256']
 with fits.open(s['raw_path']) as h:
  assert h[0].header['TICID']==5540688 and h[0].header['SECTOR']==s['sector'];a=h[1].data;t=np.asarray(a['TIME'],float);ok=np.isfinite(t);t=t[ok];f=np.asarray(a['FLUX'][ok],float);e=np.asarray(a['FLUX_ERR'][ok],float);q=a['QUALITY'][ok]
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;event=np.rint((t-b['transit_time'])/b['period']).astype(int)
 for ap in s['apertures']:
  coords=np.array(ap['pixels']);mask=np.hypot(xx-s['neighbor_position'][0],yy-s['neighbor_position'][1])<=ap['radius_pixels'];assert np.array_equal(coords,np.argwhere(mask));flux=f[:,coords[:,0],coords[:,1]].sum(axis=1);variance=(e[:,coords[:,0],coords[:,1]]**2).sum(axis=1)
  for v in ap['events']:
   inside=(q==0)&(event==v['event'])&(abs(phase)<b['duration']/2);outside=(q==0)&(event==v['event'])&(abs(phase)>b['duration'])&(abs(phase)<3*b['duration']);m0=sum(flux[outside])/sum(outside);m1=sum(flux[inside])/sum(inside);v0=sum(variance[outside])/sum(outside)**2;v1=sum(variance[inside])/sum(inside)**2;depth=1-m1/m0;error=(v1/m0**2+m1**2*v0/m0**4)**.5;np.testing.assert_allclose([m0,m1,v0,v1,depth,error],[v['outside_mean'],v['inside_mean'],v['outside_variance'],v['inside_variance'],v['depth'],v['error']],rtol=1e-10);count+=1
  weights=[v['error']**-2 for v in ap['events']];mean=sum(w*v['depth'] for w,v in zip(weights,ap['events']))/sum(weights);np.testing.assert_allclose([mean,sum(weights)**-.5],[ap['weighted_depth'],ap['formal_error']],rtol=1e-10)
for sec in [35,36,62]:assert not Path(f'data/lightcurves/s{sec:04d}-5540688.fits').exists()
save_json(p/'verification.json',dict(status='passed',utc=now(),event_aperture_depths_verified=count,independent_qr_scene_models=4,independent_qr_difference_models=2,unopened=[35,36,62],limits='Conditional arithmetic and provenance; not validation of PRF/dilution/stellar-radius assumptions.',artifact_sha256={x.name:sha(x) for x in p.iterdir() if x.is_file() and x.name!='verification.json'}))
