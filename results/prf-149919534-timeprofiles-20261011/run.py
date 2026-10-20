"""Posthoc time profiles, fixed scene and predeclared binning; no transit search."""
from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;base=Path('results/prf-149919534-astrometry-20261011');read=lambda p:json.loads(p.read_text())
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json');pixel=Path('data/pixels/149919534-s0075.fits');b=read(fp)['best'];r=read(base/'fits.json');controls=read(base/'control-summary.json')['windows'];z=np.load(base/'images.npz');ids=r['scene_ids'];ts=[z['template_'+i] for i in ids];gy,gx=np.gradient(z['scene_model']);templates=ts+[gx,gy]
chosen=[{'label':f'event{n}','kind':'event','center':b['transit_time']+n*b['period']} for n in [1,2]]
for label,selector in [('positive_control',max),('negative_control',min)]:
 c=selector(controls,key=lambda c:c['amplitudes']['149919534']);chosen.append({'label':label,'kind':'control','center':c['center_btjd'],'prior_event':c['event'],'prior_fraction':c['fraction']})
edges=np.linspace(-3,3,25)
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p):sha(p) for p in [fp,pixel,base/'fits.json',base/'images.npz',base/'control-summary.json']},'windows':chosen,'bin_edges_durations':edges.tolist(),'policy':'Posthoc morphology diagnostic on already-opened S75. Two frozen events plus highest/lowest target controls selected from previous fixed-model results, not new independent validation. No epoch/duration optimization. Quarter-duration bins, at least2 q0 exposures. Local baseline D<abs(dt)<3D, at least5; controls exclude all true windows within D. Fixed scene PRFs+derivatives+plane. Difference variance accounts for shared exposures between bin and baseline; correlations across bins and pixels not calibrated.'})
with fits.open(pixel) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(d['FLUX'][ok],float);err=np.asarray(d['FLUX_ERR'][ok],float);q=d['QUALITY'][ok]
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;rows=[];checks=[]
for window in chosen:
 dt=(t-window['center'])/b['duration'];valid=q==0
 if window['kind']=='control':valid=valid&(abs(phase)>b['duration'])
 baseline=valid&(abs(dt)>1)&(abs(dt)<3);no=int(baseline.sum());assert no>=5
 row=dict(window,baseline_exposures=no,bins=[])
 for left,right in zip(edges[:-1],edges[1:]):
  mask=valid&(dt>=left)&(dt<right);ni=int(mask.sum());entry={'left':float(left),'right':float(right),'mid':float((left+right)/2),'n':ni,'overlap_baseline':int((mask&baseline).sum())}
  if ni<2:entry['status']='insufficient_coverage';row['bins'].append(entry);continue
  # Same exposure contributes once with its net contrast coefficient.
  w=baseline.astype(float)/no-mask.astype(float)/ni;selected=w!=0
  im=np.nansum(w[selected,None,None]*flux[selected],axis=0);se=np.sqrt(np.nansum(w[selected,None,None]**2*err[selected]**2,axis=0))
  f=fit_templates(im,se,templates)
  entry.update(status='measured',amplitudes=dict(zip(ids,map(float,f['coefficients']))),gradient_coefficients=f['coefficients'][len(ids):len(ids)+2].tolist(),plane_coefficients=f['coefficients'][-3:].tolist(),chi2=f['chi2'],dof=f['dof'])
  # Propagate a deterministic box dip plus time-variable nuisance through the same contrast.
  box=(abs(dt)<.5).astype(float);expected=float(-3*np.dot(w,box));nuisance=float(np.dot(w,np.sin(dt)))
  synthetic=expected*ts[ids.index('149919534')]+nuisance*(.002*gx-.001*gy+2)
  inj=fit_templates(synthetic,se,templates);truth=np.zeros(len(ids));truth[ids.index('149919534')]=expected;delta=float(abs(inj['coefficients'][:len(ids)]-truth).max());assert delta<1e-8
  checks.append({'window':window['label'],'left':float(left),'expected_target':expected,'max_source_error':delta});row['bins'].append(entry)
 rows.append(row)
save_json(out/'results.json',{'rows':rows,'limits':'Conditional source flux, positive means fainter than the local baseline. Selected controls and data-dependent scene are posthoc. Bin errors are correlated via common baseline; fit statistics are not probabilities. No independent epoch or host validation.'})
save_json(out/'synthetic.json',{'checks':checks,'limits':'Exact-template noiseless box plus derivative/plane nuisance checks linear contrast/fit arithmetic only, not morphology reliability under real systematics.'})
print([(r['label'],r['baseline_exposures'],sum(x['status']=='measured' for x in r['bins'])) for r in rows])
