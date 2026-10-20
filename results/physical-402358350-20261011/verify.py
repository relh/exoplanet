from pathlib import Path
import json
import numpy as np
import batman
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json,read_curve,now
from exoplanet.search import flatten
O=Path(__file__).parent;plan=json.loads((O/'plan.json').read_text());rows=json.loads((O/'results.json').read_text());assert rows['plan_sha256']==sha(O/'plan.json')
for p,h in {**plan['input_sha256'],**plan['raw_sha256']}.items():assert sha(Path(p))==h
fig,axes=plt.subplots(2,2,figsize=(11,8));checks=[]
for index,row in enumerate(rows['rows']):
 w=row['window'];fit=row['fit'];b=fit['best'];z=np.load(O/f'w{w}.npz');t,y,e=[z[k] for k in ['t','y','e']]
 arrays=[]
 for s in plan['sectors']:
  tt,ff,ee,meta=read_curve(Path(f'data/lightcurves/s{s:04d}-402358350.fits'));assert meta['ticid']==402358350;arrays.append(flatten(tt,ff,ee,window=w))
 ar=[np.concatenate([a[j] for a in arrays]) for j in range(3)];order=np.argsort(ar[0])
 for actual,expected in zip([t,y,e],ar):np.testing.assert_array_equal(actual,expected[order])
 seed=plan['seed'];p=seed['period'];ep=seed['transit_time']+round((np.median(t)-seed['transit_time'])/p)*p;labels=np.rint((t-ep)/p).astype(int);dt=t-(ep+labels*p);take=abs(dt)<min(4*seed['duration'],.45*p);u,c=np.unique(labels[take],return_counts=True);take&=np.isin(labels,u[c>=8]);exposure=np.empty(len(t))
 for ii in np.split(np.arange(len(t)),np.flatnonzero(np.diff(t)>.3)+1):exposure[ii]=np.median(np.diff(t[ii]))
 tt=t[take];yy=y[take];ee=e[take];exp=exposure[take];lab=labels[take];model=np.empty(len(tt));par=batman.TransitParams();par.t0=b['transit_time']-ep;par.per=b['period'];par.rp=b['radius_ratio'];par.a=b['scaled_axis'];par.inc=np.degrees(np.arccos(b['impact']/b['scaled_axis']));par.ecc=0;par.w=90;par.u=plan['limb'];par.limb_dark='quadratic'
 for dur in np.unique(np.round(exp,6)):
  a=np.round(exp,6)==dur;model[a]=batman.TransitModel(par,tt[a]-ep,supersample_factor=11,exp_time=float(dur)).light_curve(par)
 residual=np.empty(len(tt));corrected=np.empty(len(tt))
 for event in np.unique(lab):
  a=lab==event;x=tt[a]-np.mean(tt[a]);X=np.column_stack([np.ones(a.sum()),x]);coef=np.linalg.lstsq(X/ee[a,None],(yy[a]-model[a])/ee[a],rcond=None)[0];residual[a]=(yy[a]-model[a]-X@coef)/ee[a];corrected[a]=yy[a]-X@coef
 chi=float(residual@residual);prior=0 if row['prior'] is None else (np.log(b['scaled_axis']/plan['axis_guess'])/row['prior'])**2
 np.testing.assert_allclose([chi,chi+prior],[fit['conditional_data_chi2'],fit['conditional_total_chi2']],rtol=1e-8,atol=1e-6)
 dof=len(tt)-5-2*len(np.unique(lab));checks.append(dict(window=w,prior=row['prior'],chi2=chi,dof=dof,reduced_chi2=chi/dof))
 ax=axes.flat[index];phase=(tt-b['transit_time']+b['period']/2)%b['period']-b['period']/2;edges=np.linspace(-.4,.4,41)
 for lo,hi in zip(edges[:-1],edges[1:]):
  a=(phase>=lo)&(phase<hi)
  if a.any():weights=1/ee[a]**2;ax.errorbar((lo+hi)/2,(np.average(corrected[a],weights=weights)-1)*1e6,1/np.sqrt(weights.sum())*1e6,fmt='.',color='black')
 a=abs(phase)<.4;order=np.argsort(phase[a]);ax.plot(phase[a][order],(model[a][order]-1)*1e6,'.',ms=1,color='orange');ax.set_title(f'{w}d, log-axis prior {row["prior"]}, b={b["impact"]:.2f}');ax.set_xlabel('Days from fitted center');ax.set_ylabel('Local-baseline corrected ppm')
fig.tight_layout();fig.savefig(O/'fits.png',dpi=150)
save_json(O/'verification.json',dict(status='passed',utc=now(),script_sha256=sha(Path(__file__)),checks=checks,scope='Raw hashes/preprocessing reconstructed; direct batman model with independent per-event weighted least-squares baseline reproduces chi-square and prior penalty. Same batman library, not independently implemented transit physics or optimizer convergence proof.'))
print(checks)
