from pathlib import Path
import json,numpy as np
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());m=read(out/'models.json')['sectors'][0];r=read(out/'fits.json')['sectors'][0];z=np.load(out/'s91-images.npz');prf=TESS_PRF(m['camera'],m['ccd'],91,m['col'],m['row'],localdatadir='data/prf/start_s0004');a=np.array(r['alignment']);pos={k:np.array(v) for k,v in r['positions'].items()};vec=pos['196683452']-pos['196681132'];unit=vec/np.linalg.norm(vec);rows=[]
for step in np.linspace(-.2,.2,17):
 shift=a+step*unit
 scene=fit_templates(z['scene'],np.ones(z['scene'].shape),[prf.locate(*(np.array(p)+shift),z['scene'].shape) for p in r['scene_positions']],nonnegative=True)
 fs={k:fit_templates(z['difference'],z['error'],[prf.locate(*(p+shift),z['scene'].shape)]) for k,p in pos.items()};chi={k:f['chi2'] for k,f in fs.items()}
 rows.append({'step_pixels_along_target_to_neighbor':float(step),'shift':shift.tolist(),'scene_unweighted_squared_residual':scene['chi2'],'scene_coefficients':scene['coefficients'].tolist(),'host_chi2':chi,'winner':min(chi,key=chi.get)})
save_json(out/'registration-sensitivity.json',{'script_sha256':sha(Path(__file__)),'inputs':{n:sha(out/n) for n in ['models.json','fits.json','s91-images.npz']},'rows':rows,'limits':'Posthoc fixed registration perturbations along close-pair direction; scene fluxes refit nonnegative. Unweighted scene residual is not likelihood or registration confidence interval. No exclusion of PRF mismatch or alternative scene models.'});print([(round(r['step_pixels_along_target_to_neighbor'],3),r['winner'],round(r['scene_unweighted_squared_residual'],2)) for r in rows])
