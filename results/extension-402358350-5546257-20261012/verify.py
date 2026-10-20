from pathlib import Path
import json,csv,numpy as np
from scipy.linalg import solve_triangular
from astropy.time import Time
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());checks=[]
def ck(v,s):
 assert v,s
 checks.append(s)
for name,h in plan['inputs'].items():ck(sha(Path(name))==h,'frozen input hash')
src=json.loads((p/'epoch-source.json').read_text());ck(sha(Path(src['path']))==src['sha256'],'Gaia raw hash');ck(src['requested_utc']>plan['frozen_utc'],'plan before access');raw=list(csv.DictReader(Path(src['path']).open()));good=[]
for r in raw:
 ck(r['source_id']==plan['gaia_source_id'],'Gaia exact identity')
 if r['variability_flag_g_reject']=='false' and r['rejected_by_photometry']=='false' and all(r[k] and np.isfinite(float(r[k])) for k in ['g_transit_time','g_transit_mag','g_transit_flux','g_transit_flux_error']) and float(r['g_transit_flux'])>0 and float(r['g_transit_flux_error'])>0:good.append(r)
z=np.load(p/'gaia-arrays.npz');gr=json.loads((p/'gaia-results.json').read_text());ck(len(good)==gr['quality_count']==54,'Gaia quality count');tc=np.array([float(r['g_transit_time']) for r in good]);t=Time(2455197.5,tc,format='jd',scale='tcb').tdb.jd-2457000;ck(np.max(abs(t-z['t']))<1e-8,'two-part JD conversion');g=plan['gaia_model'];cycles=(tc-float(g['reference_time']))*float(g['frequency']);shape=np.zeros(len(tc))
for j in [1,2]:
 delta=cycles-float(g[f'geom_model_gaussian{j}_phase']);delta-=np.round(delta);shape+=float(g[f'geom_model_gaussian{j}_depth'])*np.exp(-delta**2/(2*float(g[f'geom_model_gaussian{j}_sigma'])**2))
ck(np.max(abs(shape-z['shape']))<1e-10,'periodic two-Gaussian shape');ck(abs(np.sum(((z['mag']-float(g['geom_model_reference_level'])-shape)/z['me'])**2)-gr['published_model_chi2'])<1e-7,'published model chi2')
for c,m in zip(plan['candidate554'],gr['candidate_fixed_tests']):
 b=c['best'];cy=np.round((t-b['transit_time'])/b['period']);distance=abs(t-b['transit_time']-cy*b['period']);i=distance<b['duration']/2;o=distance>1.5*b['duration'];ck(i.sum()==m['n_inside'] and o.sum()==m['n_outside'],'Gaia candidate masks');use=i|o;X=np.column_stack([np.ones(use.sum()),-i[use].astype(float)]);Q,R=np.linalg.qr(X/z['e'][use,None]);coef=solve_triangular(R,Q.T@(z['y'][use]/z['e'][use]));inv=np.linalg.inv(R);error=np.sqrt((inv@inv.T)[1,1]);ck(abs(coef[1]-m['depth'])<1e-10 and abs(error-m['formal_error'])<1e-10,'Gaia candidate QR depth')
 if c['ranges']:
  offsets=[]
  for per,ep in c['ranges']['profile_timing_pairs']:
   ep+=round((b['transit_time']-ep)/per)*per
   for tt in [min(t),max(t)]:offsets.append(abs(ep-b['transit_time']+round((tt-b['transit_time'])/b['period'])*(per-b['period'])))
  spread=max(offsets)+3*c['ranges']['conditional_epoch_floor_days'];ck(abs(spread-m['spread_days'])<1e-10,'Gaia clock propagation')
 else:ck(m['spread_days'] is None,'missing seed uncertainty explicit')
 ck(m['outcome']=='inconclusive','original timing gate preserved')
r=json.loads((p/'pulsator-results.json').read_text());b=plan['clock402']
for fit in r['fits']:
 a=np.load(p/f"fit-{fit['key']}.npz");X=a['X'];Q,R=np.linalg.qr(X/a['e'][:,None]);beta=solve_triangular(R,Q.T@(a['y']/a['e']));inv=np.linalg.inv(R);ck(np.max(abs(beta-fit['coef']))<1e-9,'pulsation fit QR coefficients');ck(abs(np.sqrt((inv@inv.T)[-1,-1])-fit['error'])<1e-10,'pulsation fit covariance');phase=a['t']-b['transit_time']-np.round((a['t']-b['transit_time'])/b['period'])*b['period'];ck(np.array_equal(-X[:,-1],abs(phase)<b['duration']/2),'fixed dip template')
for inj in r['injections']:
 a=np.load(p/f"inject-{inj['key']}.npz");t=a['t'];event=np.round((t-b['transit_time'])/b['period']);d=abs(t-b['transit_time']-event*b['period']);i=d<b['duration']/2;o=(d>b['duration'])&(d<3*b['duration']);w=1/a['e']**2;num=den=0.
 for n in np.unique(event[i|o]):
  use=(i|o)&(event==n);x=-i[use].astype(float);y=a['y1'][use]-a['y0'][use];x-=np.average(x,weights=w[use]);y-=np.average(y,weights=w[use]);num+=np.sum(w[use]*x*y);den+=np.sum(w[use]*x*x)
 ck(abs(num/den-inj['depth_change'])<1e-9,'independent event-demeaned injection change')
sup=json.loads((p/'gaia-supplement.json').read_text())
for row in sup['fixed_gaussians']:
 c=next(c for c in plan['candidate554'] if c['name']==row['clock']);b=c['best'];d=t if False else z['t']-b['transit_time']-np.rint((z['t']-b['transit_time'])/b['period'])*b['period'];shape=np.exp(-.5*(d/(b['duration']/row['sigma_duration_divisor']))**2);X=np.column_stack([np.ones(len(d)),shape]);Q,R=np.linalg.qr(X/z['me'][:,None]);coef=solve_triangular(R,Q.T@(z['mag']/z['me']));ck(abs(coef[1]-row['depth_mag'])<1e-9,'supplement fixed Gaussian QR');ck(abs(np.sum(((z['mag']-X@coef)/z['me'])**2)-row['chi2'])<1e-6,'supplement chi2')
for row in sup['profiles']:
 b=plan['candidate554'][1]['best'];n=np.round((z['t']-row['epoch'])/row['period']);inside=abs(z['t']-row['epoch']-n*row['period'])<b['duration']/2;ck(np.where(inside)[0].tolist()==row['indices'],'profile point memberships')
save_json(p/'verification.json',dict(status='passed',n_checks=len(checks),checks=checks,limits='Arithmetic/input verification; shared Astropy timescale and existing flatten. No astrophysicalvalidation.'));print('PASS',len(checks))
