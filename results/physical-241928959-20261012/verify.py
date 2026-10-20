from pathlib import Path
import json
import numpy as np
import batman
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json,read_curve,now
from exoplanet.search import flatten
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
O=Path(__file__).parent;plan=json.loads((O/'plan.json').read_text());rows=json.loads((O/'results.json').read_text());assert rows['plan_sha256']==sha(O/'plan.json')
for p,h in plan['hashes'].items():assert sha(Path(p))==h
fig,axes=plt.subplots(2,3,figsize=(15,8));checks=[]
for index,row in enumerate(rows['rows']):
 w=row['window'];fit=row['fit'];b=fit['best'];z=np.load(O/f'w{w}.npz');t,y,e=[z[k] for k in ['t','y','e']]
 with fits.open('data/qlp/241928959-s0092.fits') as hdus:
  assert hdus[0].header['TICID']==241928959 and hdus[0].header['SECTOR']==92;d=hdus[1].data;fc,ec,_=qlp_flux_columns(d.names);tt,ff,ee=[np.asarray(d[k],float) for k in ['TIME',fc,ec]];a=(d['QUALITY']==0)&np.isfinite(tt)&np.isfinite(ff)&(ff>0)&np.isfinite(ee)&(ee>0);tt,ff,ee=tt[a],ff[a],ee[a];o=np.argsort(tt);ar=flatten(tt[o],ff[o],ee[o],window=w)
 for actual,expected in zip([t,y,e],ar):np.testing.assert_array_equal(actual,expected)
 case=row['case'];y=1+(y-1)/case['fraction'];e=e/case['fraction']
 seed=plan['seed'];p=seed['period'];ep=seed['transit_time']+round((np.median(t)-seed['transit_time'])/p)*p;labels=np.rint((t-ep)/p).astype(int);dt=t-(ep+labels*p);take=abs(dt)<min(4*seed['duration'],.45*p);u,c=np.unique(labels[take],return_counts=True);take&=np.isin(labels,u[c>=8]);exposure=np.empty(len(t))
 for ii in np.split(np.arange(len(t)),np.flatnonzero(np.diff(t)>.3)+1):exposure[ii]=np.median(np.diff(t[ii]))
 tt=t[take];yy=y[take];ee=e[take];exp=exposure[take];lab=labels[take];model=np.empty(len(tt));par=batman.TransitParams();par.t0=b['transit_time']-ep;par.per=b['period'];par.rp=b['radius_ratio'];par.a=b['scaled_axis'];par.inc=np.degrees(np.arccos(b['impact']/b['scaled_axis']));par.ecc=0;par.w=90;par.u=[.4,.2];par.limb_dark='quadratic'
 for dur in np.unique(np.round(exp,6)):
  a=np.round(exp,6)==dur;model[a]=batman.TransitModel(par,tt[a]-ep,supersample_factor=11,exp_time=float(dur)).light_curve(par)
 residual=np.empty(len(tt));corrected=np.empty(len(tt))
 for event in np.unique(lab):
  a=lab==event;x=tt[a]-np.mean(tt[a]);X=np.column_stack([np.ones(a.sum()),x]);coef=np.linalg.lstsq(X/ee[a,None],(yy[a]-model[a])/ee[a],rcond=None)[0];residual[a]=(yy[a]-model[a]-X@coef)/ee[a];corrected[a]=yy[a]-X@coef
 chi=float(residual@residual);prior=0 if case['prior'] is None else (np.log(b['scaled_axis']/case['axis'])/case['prior'])**2
 np.testing.assert_allclose([chi,chi+prior],[fit['conditional_data_chi2'],fit['conditional_total_chi2']],rtol=1e-8,atol=1e-6)
 dof=len(tt)-5-2*len(np.unique(lab));checks.append(dict(window=w,case=case['name'],chi2=chi,dof=dof,reduced_chi2=chi/dof))
 ax=axes.flat[index];phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.08,.08,65)
 for lo,hi in zip(edges[:-1],edges[1:]):
  a=(phase>=lo)&(phase<hi)
  if a.any():weights=1/ee[a]**2;ax.errorbar((lo+hi)/2,(np.average(corrected[a],weights=weights)-1)*case['fraction']*1e6,case['fraction']/np.sqrt(weights.sum())*1e6,fmt='.',color='black')
 a=abs(phase)<.08;order=np.argsort(phase[a]);ax.plot(phase[a][order],(model[a][order]-1)*case['fraction']*1e6,'.',ms=1,color='orange');ax.set_title(f'{w}d, {case["name"]}, b={b["impact"]:.2f}');ax.set_xlabel('Days from fitted center');ax.set_ylabel('Local-baseline corrected ppm')
fig.tight_layout();fig.savefig(O/'fits.png',dpi=150)
save_json(O/'verification.json',dict(status='passed',utc=now(),script_sha256=sha(Path(__file__)),checks=checks,scope='Raw QLP hashes/preprocessing reconstructed; direct batman model with independent per-event weighted least-squares baseline reproduces chi-square and prior penalty. Same batman library, not independently implemented transit physics or optimizer convergence proof.'))
print(checks)
