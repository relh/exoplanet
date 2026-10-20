from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;m=json.loads(Path('results/prf-156001092-20261011/models.json').read_text())['sectors'][0];r=json.loads((out/'fits.json').read_text());z=np.load(out/'images.npz');ids=r['scene_ids'];ts=[z['template_'+i] for i in ids];gy,gx=np.gradient(z['scene_model']);fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/frozen.json');b=json.loads(fp.read_text())['best'];fractions=np.r_[np.linspace(-.9,-.1,9),np.linspace(.1,.9,9)].tolist()
save_json(out/'broader-controls-plan.json',{'script_sha256':sha(Path(__file__)),'images_sha256':sha(out/'images.npz'),'fits_sha256':sha(out/'fits.json'),'frozen_sha256':sha(fp),'fractions':fractions,'injected_target_amplitude':5.,'policy':'Expanded sensitivity after initial four usable controls: shift each event backward and forward by listed period fractions, exclude all true-event windows within one duration from inside and baseline. Retain insufficient windows. Fixed registered PRFs plus scene gradients and plane. Overlapping controls are not independent or false-alarm calibration.'})
with fits.open(m['pixel_path']) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(d['FLUX'][ok],float);err=np.asarray(d['FLUX_ERR'][ok],float);q=d['QUALITY'][ok]
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;valid=(q==0)&(abs(phase)>b['duration']);rows=[]
for observed in r['rows']:
 for fraction in fractions:
  center=b['transit_time']+(observed['event']+fraction)*b['period'];dt=abs(t-center);inside=valid&(dt<b['duration']/2);outside=valid&(dt>b['duration'])&(dt<3*b['duration']);row={'event':observed['event'],'fraction':fraction,'inside':int(inside.sum()),'outside':int(outside.sum())}
  if inside.sum()<2 or outside.sum()<5:row['status']='insufficient_coverage'
  else:
   im=np.nanmean(flux[outside],axis=0)-np.nanmean(flux[inside],axis=0);se=np.sqrt(np.nansum(err[outside]**2,axis=0)/outside.sum()**2+np.nansum(err[inside]**2,axis=0)/inside.sum()**2);f=fit_templates(im,se,ts+[gx,gy]);inj=fit_templates(im+5*ts[ids.index('156001092')],se,ts+[gx,gy]);amplitudes=dict(zip(ids,map(float,f['coefficients'])));added=inj['coefficients'][:len(ids)]-f['coefficients'][:len(ids)];truth=np.zeros(len(ids));truth[ids.index('156001092')]=5;assert abs(added-truth).max()<1e-6;row.update(status='measured',amplitudes=amplitudes,chi2=f['chi2'],dof=f['dof'],max_injection_difference_error=float(abs(added-truth).max()))
  rows.append(row)
save_json(out/'broader-controls.json',{'rows':rows,'plan_sha256':sha(out/'broader-controls-plan.json'),'limits':'Linear-model injection response on real windows is algebraically constrained; does not test incorrect PRF shape or registration. Small selected overlapping control set, no significance or false-positive probability.'});print([(r['event'],r['fraction'],r['status'],r.get('amplitudes',{}).get('156001092')) for r in rows])
