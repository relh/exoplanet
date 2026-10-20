"""Event-window matched controls at fixed templates; no calibrated probabilities."""
from pathlib import Path
from collections import Counter
import json
import numpy as np
from astropy.io import fits
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/prf-80387959-20261009')
mp=base/'models.json';bp=Path('results/followup-80387959-qlp90-100-20261009/frozen.json')
sp=Path('results/prf-80387959-event-stability-20261011/results.json')
meta=json.loads(mp.read_text());best=json.loads(bp.read_text())['best'];stability=json.loads(sp.read_text())
assert not (out/'plan.json').exists()
fractions=np.linspace(.1,.9,41)
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'models_sha256':sha(mp),'frozen_sha256':sha(bp),'stability_sha256':sha(sp),'sectors':[63,90],'fractions':fractions.tolist(),'policy':'All recorded events in two previously discordant sectors. Shift each event center by 0.1–0.9 periods; mask all true-event windows from control events and baselines. Fixed archived templates, no registration refit. Inject target PRF at observed conditional target-fit amplitude. Windows overlap; no false-alarm probabilities or model-mismatch calibration. No selection by control outcome.'})
rows=[]
for m in meta['sectors']:
 if m['sector'] not in [63,90]:continue
 sector=m['sector'];p=Path(m['pixel_path']);assert sha(p)==m['pixel_sha256']
 z=np.load(base/f's{sector}-images.npz');templates={k.removeprefix('template_'):z[k] for k in z.files if k.startswith('template_')}
 with fits.open(p) as h:
  d=h[1].data;t=np.asarray(d['TIME'],float);finite=np.isfinite(t);t=t[finite]
  flux=np.asarray(d['FLUX'][finite],float);err=np.asarray(d['FLUX_ERR'][finite],float);q=np.asarray(d['QUALITY'][finite])
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
 def window(center,control):
  valid=(q==0)
  if control:valid &= abs(phase)>=best['duration']
  dt=abs(t-center);inside=valid&(dt<best['duration']/2);outside=valid&(dt>best['duration'])&(dt<3*best['duration'])
  counts={'inside':int(inside.sum()),'outside':int(outside.sum())}
  if inside.sum()<2 or outside.sum()<5:return None,None,counts
  im=np.nanmean(flux[outside],axis=0)-np.nanmean(flux[inside],axis=0)
  var=np.nansum(err[outside]**2,axis=0)/outside.sum()**2+np.nansum(err[inside]**2,axis=0)/inside.sum()**2
  return im,np.sqrt(var),counts
 def fit(im,se):
  fs={tic:fit_templates(im,se,[v]) for tic,v in templates.items()}
  chi={tic:f['chi2'] for tic,f in fs.items()}
  return {'winner':min(chi,key=chi.get),'chi2':chi,'amplitudes':{tic:float(f['coefficients'][0]) for tic,f in fs.items()},'target_delta_chi2':chi['80387959']-min(chi.values())},fs
 old=next(r for r in stability if r['sector']==sector)
 for ev in old['individual']:
  n=ev['event'];center=best['transit_time']+n*best['period']
  im,se,counts=window(center,False);observed,fs=fit(im,se)
  for tic in templates:np.testing.assert_allclose(observed['chi2'][tic],ev['chi2'][tic],rtol=1e-8,atol=1e-8)
  amplitude=max(observed['amplitudes']['80387959'],0)
  controls=[]
  for fraction in fractions:
   c=center+fraction*best['period'];ci,ce,cc=window(c,True)
   row={'fraction':float(fraction),'center':float(c),**cc}
   if ci is None:row['status']='insufficient_coverage'
   else:
    raw,_=fit(ci,ce);inj,_=fit(ci+amplitude*templates['80387959'],ce)
    row.update(status='measured',raw=raw,target_injected=inj)
   controls.append(row)
  good=[r for r in controls if r['status']=='measured']
  result={'sector':sector,'event':n,'center':center,'pixel_sha256':sha(p),'counts':counts,'observed':observed,'target_injected_amplitude':amplitude,'n_controls':len(good),'target_injection_winners':dict(Counter(r['target_injected']['winner'] for r in good)),'controls_with_at_least_observed_target_disadvantage':sum(r['target_injected']['target_delta_chi2']>=observed['target_delta_chi2'] for r in good),'controls':controls}
  np.savez_compressed(out/f's{sector}-event{n}.npz',difference=im,error=se,**{f'model_{tic}':f['model'] for tic,f in fs.items()})
  rows.append(result);save_json(out/'results.json',rows);print(sector,n,observed['winner'],len(good),result['target_injection_winners'],flush=True)
