from pathlib import Path
import json,hashlib,math
import numpy as np
from astropy.io import fits
R=Path('results/paper-host-vetting-20261012');p=json.loads((R/'plan.json').read_text());a=json.loads((R/'results.json').read_text());checks=0
for path,h in p['inputs'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h;checks+=1
assert a['plan_sha256']==hashlib.sha256((R/'plan.json').read_bytes()).hexdigest()
for m in a['measurements']:
 z=np.load(R/f"{m['tic']}-s{m['sector']}-sap.npz");X=z['design'];y=z['flux'];err=z['error'];A=X/err[:,None];b=y/err
 # Independent residualized-transit solution after nuisance projection.
 N=A[:,1:];q=np.linalg.qr(N,mode='reduced')[0];v=A[:,0]-q@(q.T@A[:,0]);coef=float(v@b/(v@v));assert abs(coef-z['beta'][0])<1e-12;checks+=1
 beta=np.linalg.solve(A.T@A,A.T@b);assert np.max(abs(beta-z['beta']))<1e-11;checks+=1
 cov=np.linalg.inv(A.T@A)*max(1,np.sum(((y-X@beta)/err)**2)/(len(y)-len(beta)));np.testing.assert_allclose(cov,z['covariance'],rtol=1e-8,atol=1e-20);checks+=1
 base=np.mean(beta[1::2]);g=np.zeros(len(beta));g[0]=1/base;g[1::2]=-coef/base**2/len(m['events']);assert abs(coef/base-m['depth'])<1e-12;assert abs(math.sqrt(g@cov@g)-m['error'])<1e-12;checks+=2
 with fits.open(m['raw_path']) as h:
  raw=h[1].data;mask=(raw['QUALITY']==0)&np.isfinite(raw['TIME'])&np.isfinite(raw['SAP_FLUX'])&np.isfinite(raw['SAP_FLUX_ERR'])&(raw['SAP_FLUX']>0)&(raw['SAP_FLUX_ERR']>0);tt=raw['TIME'][mask];yy=raw['SAP_FLUX'][mask].astype(float);ee=raw['SAP_FLUX_ERR'][mask].astype(float);norm=np.median(yy)
  cp=json.loads(Path('results/strongest-80387959-shape-20261012/plan.json' if m['tic']==80387959 else 'results/strongest-402358350-baselines-20261012/plan.json').read_text());clock=cp.get('best',cp.get('clock'));P=clock['period'];D=clock['duration'];T=clock['transit_time'];ev=np.rint((tt-T)/P).astype(int);dt=tt-T-ev*P
  good=[]
  for event in np.unique(ev):
   use=(ev==event)&(abs(dt)<3*D)
   if sum(use&(abs(dt)<D/2))>=2 and sum(use&(dt<-D/2))>=5 and sum(use&(dt>D/2))>=5:good.append(int(event))
  assert good==m['events'];sel=np.isin(ev,good)&(abs(dt)<3*D);np.testing.assert_array_equal(tt[sel],z['time']);np.testing.assert_allclose(yy[sel]/norm,y,rtol=0,atol=0);np.testing.assert_allclose(ee[sel]/norm,err,rtol=0,atol=0);assert h[1].header['CROWDSAP']==m['crowdsap'];assert h[1].header['FLFRCSAP']==m['flfrcsap'];checks+=7
  exp=np.median(np.diff(tt));ol=np.clip((np.minimum(dt[sel]+exp/2,D/2)-np.maximum(dt[sel]-exp/2,-D/2))/exp,0,1);np.testing.assert_allclose(-X[:,0],ol,atol=1e-10);checks+=1
 # Deterministic injected decrement in presence of arbitrary local slopes; no noise.
 truth=np.ones(X.shape[1]);truth[0]=.0008;truth[2::2]=np.linspace(-.001,.001,len(good));synthetic=X@truth;fit=np.linalg.lstsq(A,synthetic/err,rcond=None)[0];assert max(abs(fit-truth))<1e-11;checks+=1
measure={(m['tic'],m['sector']):m for m in a['measurements']}
for tic,path in [(80387959,'results/neighbors-80387959-20261009/tic-neighbors.json'),(402358350,'results/neighbors-402358350-20261011/neighbors.json')]:
 cat=json.loads(Path(path).read_text());target=next(z for z in cat if z['ID']==tic);selected={}
 for star in cat:
  dra=math.radians(star['ra']-target['ra']);da=math.radians(star['dec']);db=math.radians(target['dec']);sep=math.degrees(2*math.asin(math.sqrt(math.sin((da-db)/2)**2+math.cos(da)*math.cos(db)*math.sin(dra/2)**2)))*3600
  if sep<=150:selected[star['ID']]=(star,sep)
 for sector in [m['sector'] for m in a['measurements'] if m['tic']==tic]:
  rr=[r for r in a['neighbors'] if r['tic']==tic and r['sector']==sector];assert {r['neighbor'] for r in rr}==set(selected);assert len(rr)==len(selected);checks+=2
  for r in rr:
   star,sep=selected[r['neighbor']];assert abs(sep-r['separation_arcsec'])<1e-6;assert r['Tmag']==star.get('Tmag');assert r['e_Tmag']==star.get('e_Tmag');assert r['gaia_dr2']==star.get('GAIA');checks+=4

for r in a['neighbors']:
 if r['status']=='missing_Tmag':continue
 m=measure[r['tic'],r['sector']];c=m['crowdsap'];eta=m['flfrcsap'];ratio=10**((r['target_Tmag']-r['Tmag'])/2.5);d=m['depth'];target=r['tic']==r['neighbor']
 # Direct stellar photon accounting: target total flux=1, aperture target=eta,
 # total aperture flux=eta/c. Each source an alternative, never sum TIC rows.
 total=eta/c
 for g in r['q_grid']:
  neighbor_aperture=ratio*eta*g['q'];removed=neighbor_aperture*g['required_eclipse_fraction'];assert math.isclose(removed/total,d,rel_tol=1e-12);assert g['within_throughput_and_budget']==bool(g['q']<=min(r['q_upper_physical'],r['q_upper_contamination_budget'])*(1+1e-12));checks+=2
 max_flux=eta if target else min(ratio,total-eta)
 assert math.isclose(r['minimum_eclipse_fraction'],d*total/max_flux,rel_tol=1e-12);checks+=1
 assert math.isclose(r['q_min_total_eclipse'],d*total/(ratio*eta),rel_tol=1e-12);checks+=1
 sigma=math.hypot(r['e_Tmag'],r['target_e_Tmag']);bright=10**(-.4*((r['Tmag']-r['target_Tmag'])-3*sigma));low=max(0,d-3*m['error']);upper_c=min(1,c*1.1);lower_eta=max(.001,eta*.9);bound=low/upper_c if target else low*lower_eta/(upper_c*bright);assert math.isclose(bound,r['optimistic_lower_bound'],rel_tol=1e-12);checks+=1
 # Synthetic eclipse at candidate q recovers eclipse fraction by inverse formula.
 e=.2;q=.3 if not target else 1.;d_syn=e*(ratio*eta*q)/total;e_back=d_syn/(c*ratio*q);assert math.isclose(e_back,e,rel_tol=1e-12);checks+=1
out={'status':'passed','checks':checks,'measurements':len(a['measurements']),'source_sector_cases':len(a['neighbors']),'limitations':'Arithmetic, raw provenance, fit reconstruction and synthetic linear-flux transfer only. Does not verify catalog/PRF model accuracy, instrumental origin, or source identity.'};(R/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
