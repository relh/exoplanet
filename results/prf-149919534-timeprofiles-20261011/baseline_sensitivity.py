"""Posthoc baseline-side sensitivity motivated by the archived time profiles."""
from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');base=Path('results/prf-149919534-astrometry-20261011');r=read(base/'fits.json');z=np.load(base/'images.npz');ids=r['scene_ids'];gy,gx=np.gradient(z['scene_model']);templates=[z['template_'+i] for i in ids]+[gx,gy];fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json');b=read(fp)['best'];pixel=Path('data/pixels/149919534-s0075.fits')
save_json(out/'baseline-plan.json',{'script_sha256':sha(Path(__file__)),'profile_plan_sha256':sha(out/'plan.json'),'profile_results_sha256':sha(out/'results.json'),'policy':'Posthoc after viewing profiles. Compare before-only, after-only and both-side baselines at D<abs(dt)<3D for all four archived windows, fixed central abs(dt)<D/2. All outcomes retained. Baseline choice not optimized; no significance or source probability.'})
with fits.open(pixel) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(d['FLUX'][ok],float);err=np.asarray(d['FLUX_ERR'][ok],float);q=d['QUALITY'][ok]
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;rows=[];checks=[]
for window in plan['windows']:
 dt=(t-window['center'])/b['duration'];valid=q==0
 if window['kind']=='control':valid &= abs(phase)>b['duration']
 inside=valid&(abs(dt)<.5);ni=int(inside.sum());row=dict(window,inside=ni,fits=[])
 for side in ['before','after','both']:
  baseline=valid&(abs(dt)>1)&(abs(dt)<3)
  if side=='before':baseline &= dt<0
  if side=='after':baseline &= dt>0
  no=int(baseline.sum());entry={'side':side,'baseline_exposures':no}
  if ni<2 or no<5:entry['status']='insufficient_coverage';row['fits'].append(entry);continue
  w=baseline.astype(float)/no-inside.astype(float)/ni;selected=w!=0
  im=np.nansum(w[selected,None,None]*flux[selected],axis=0);se=np.sqrt(np.nansum(w[selected,None,None]**2*err[selected]**2,axis=0));f=fit_templates(im,se,templates)
  entry.update(status='measured',amplitudes=dict(zip(ids,map(float,f['coefficients']))),chi2=f['chi2'],dof=f['dof']);row['fits'].append(entry)
  for slope in [0.,1.]:
   # A dimming box plus a linear target trend demonstrates baseline dependence.
   light=slope*dt-3*(abs(dt)<.5);expected=float(np.dot(w,light));im=expected*templates[ids.index('149919534')]+.002*gx-.001*gy+2
   sf=fit_templates(im,se,templates);truth=np.zeros(len(ids));truth[ids.index('149919534')]=expected;delta=float(abs(sf['coefficients'][:len(ids)]-truth).max());assert delta<1e-8;checks.append({'window':window['label'],'side':side,'linear_slope':slope,'expected_target':expected,'max_error':delta})
 rows.append(row)
save_json(out/'baseline-results.json',{'rows':rows,'synthetic_checks':checks,'limits':'Different local baselines expose variability/model dependence, not a unique detrending choice. Exact noiseless tests verify arithmetic only.'})
print([(x['label'],[(f['side'],f['amplitudes']['149919534'],f['amplitudes']['149919536']) for f in x['fits']]) for x in rows])
