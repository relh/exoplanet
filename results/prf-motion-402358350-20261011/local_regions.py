from pathlib import Path
import json,numpy as np
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;r=json.loads((p/'fits.json').read_text());rows=[]
save_json(p/'local-regions-plan.json',dict(created_utc=now(),fits_sha256=sha(p/'fits.json'),script_sha256=sha(Path(__file__)),radii_pixels=[2.5,3.5],policy='Posthoc diagnostic prompted by catastrophic whole-stamp residuals. Circular regions centered on registered catalog target; retain both outcomes, all catalog hypotheses and signed amplitudes. Same frozen clock, original differences and diagonal errors. No host probabilities.'))
for s in r['sectors']:
 z=np.load(p/f"s{s['sector']}-images.npz");target=np.array(s['positions']['402358350'])+s['alignment'];yy,xx=np.indices(z['difference'].shape);radius=np.hypot(xx-target[0],yy-target[1]);cases=[]
 for rad in [2.5,3.5]:
  error=np.where(radius<=rad,z['error'],np.inf);hyp=[]
  motiononly=fit_templates(z['difference'],error,[z['gradx'],z['grady']])
  for h in s['hypotheses']:
   k=h['tic'];temp=z['template_'+k];fit=fit_templates(z['difference'],error,[temp,z['gradx'],z['grady']]);plain=fit_templates(z['difference'],error,[temp]);hyp.append(dict(tic=k,chi2=fit['chi2'],dof=fit['dof'],amplitude=float(fit['coefficients'][0]),without_motion_chi2=plain['chi2'],without_motion_amplitude=float(plain['coefficients'][0])))
  hyp.sort(key=lambda h:h['chi2']);cases.append(dict(radius_pixels=rad,motion_only_chi2=motiononly['chi2'],hypotheses=hyp));print(s['sector'],rad,'best',hyp[0],'target',next(x for x in hyp if x['tic']=='402358350'),'motiononly',motiononly['chi2'])
 rows.append(dict(sector=s['sector'],cases=cases))
save_json(p/'local-regions.json',dict(sectors=rows))
