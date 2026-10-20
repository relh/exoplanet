from pathlib import Path
import json,hashlib,numpy as np
from astropy.io import fits
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest();assert sha(O/'plan.json')==r['plan_sha256'];count=0;maxcoef=0.;maxraw=0.;maxinj=0.
for target in p['targets']:
 assert sha(target['seed_path'])==target['seed_sha256'];b=target['seed']
 for inp in target['inputs']:
  assert sha(inp['path'])==inp['sha256'];assert inp['sha256']==inp['provenance']['sha256']
for row in r['rows']:
 z=np.load(O/(row['name']+'.npz'));assert sha(O/(row['name']+'.npz'))==row['npz_sha256'];target=next(v for v in p['targets'] if v['tic']==row['tic']);inp=next(v for v in target['inputs'] if v['sector']==row['sector']);b=target['seed']
 with fits.open(inp['path']) as h:
  d=h[1].data;tt=np.asarray(d['TIME'],float);yy=np.asarray(d[row['column']],float);ix=np.flatnonzero((d['QUALITY']==0)&np.isfinite(tt)&np.isfinite(yy)&(yy>0));ix=ix[np.argsort(tt[ix])];tt,yy=tt[ix],yy[ix];yy=yy/np.median(yy)
  cyc=np.round((tt-b['transit_time'])/b['period']);dt=abs(tt-(b['transit_time']+cyc*b['period']));cyc2=np.round((tt-b['transit_time']-.5*b['period'])/b['period']);dt2=abs(tt-(b['transit_time']+(.5+cyc2)*b['period']));sel=(dt>1.5*b['duration'])&(dt2>1.5*b['duration']);tt,yy=tt[sel],yy[sel];bins=np.floor((tt-tt[0])*48).astype(int);ts=[];ys=[]
  for key in np.unique(bins):mask=bins==key;ts.append(np.mean(tt[mask]));ys.append(np.mean(yy[mask])-1)
  assert len(ts)==len(z['t']);maxraw=max(maxraw,float(np.max(abs(np.array(ts)-z['t']))),float(np.max(abs(np.array(ys)-z['y']))));assert np.allclose(ts,z['t'],rtol=0,atol=1e-10);assert np.allclose(ys,z['y'],rtol=0,atol=1e-12)
 X=z['X'];y=z['y'];coef=np.linalg.solve(X.T@X,X.T@y);diff=np.max(abs(coef-z['beta']));maxcoef=max(maxcoef,float(diff));assert diff<1e-9;assert np.linalg.matrix_rank(X)==row['n_parameters'];assert np.allclose(coef[-4:]*1e6,row['coefficients_ppm'],atol=1e-5)
 for j in row['orbit_omission']:
  m=z['cycles']!=j['omitted_cycle'];xx=X[m];bb=np.linalg.solve(xx.T@xx,xx.T@y[m]);assert np.allclose(bb[-4:]*1e6,j['coefficients_ppm'],atol=1e-4)
 inj=np.asarray(row['injection_recovered_coefficients_ppm']);delta=float(np.max(abs(inj-np.eye(4)*1000)));maxinj=max(maxinj,delta);assert delta<1e-5
 for boot in row['bootstrap']:
  cov=np.array(boot['coefficient_cov_ppm2']);assert np.allclose(np.diag(cov)**.5,boot['coefficient_sd_ppm']);assert np.linalg.eigvalsh(cov).min()>0
 count+=1
(O/'verification.json').write_text(json.dumps(dict(verified_models=count,raw_fits=5,max_raw_reconstruction_difference=maxraw,max_normal_equation_coefficient_difference=maxcoef,max_injected_coefficient_error_ppm=maxinj,scope='Raw masks/bins independently reconstructed; full fits and leave-orbit-out normal-equation verification; exact injectedbasis expectation; covariance internal consistency. Does not calibrate astrophysical errors, upstream transfer or FPP.'),indent=2)+'\n');print((O/'verification.json').read_text())
