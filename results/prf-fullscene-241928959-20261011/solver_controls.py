from pathlib import Path
import json
import numpy as np
from PRF import TESS_PRF
from solver import fit_templates,fit_shift
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent
r=json.loads((p/'fits.json').read_text())['sectors'][0];m=json.loads((p/'models.json').read_text())['sectors'][0]
prf=TESS_PRF(m['camera'],m['ccd'],m['sector'],m['col'],m['row'],localdatadir='data/prf/start_s0004')
pos=np.array(r['scene_positions']);z=np.load(p/'s92-images.npz');shape=z['scene'].shape
y,x=np.indices(shape);rng=np.random.default_rng(241928959);amp=rng.uniform(1,300,len(pos));rows=[]
for shift in [np.array([.08,-.11]),np.array([-.13,.09])]:
 templates=[prf.locate(*(q+shift),shape) for q in pos]
 synthetic=np.einsum('i,ijk->jk',amp,templates)+10+.2*(x-x.mean())-.3*(y-y.mean())
 fixed=fit_templates(synthetic,np.ones(shape),templates,nonnegative=True)
 recovered=fit_shift(synthetic,np.ones(shape),pos,prf.locate)
 np.testing.assert_allclose(fixed['coefficients'][:len(amp)],amp,rtol=1e-6,atol=1e-5)
 np.testing.assert_allclose(recovered['shift'],shift,atol=1e-5)
 assert not recovered['boundary']
 rows.append({'injected_shift':shift.tolist(),'recovered_shift':recovered['shift'].tolist(),'fixed_chi2':fixed['chi2'],'shift_chi2':recovered['chi2'],'max_fixed_amplitude_error':float(np.max(abs(fixed['coefficients'][:len(amp)]-amp)))})
save_json(p/'solver-controls.json',{'rows':rows,'scene_sources':len(pos),'inputs':{n:sha(p/n) for n in ['solver.py','solver_controls.py','fits.json','models.json']},'limits':'Noiseless matched-model solver checks, not empirical PRF accuracy or host probabilities.'});print(rows)
