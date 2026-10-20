from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text())
for path,digest in r['inputs'].items():assert sha(Path(path))==digest
z=np.load(p/'events.npz');t=np.load('results/prf-241928959-s92-20261011/s92-images.npz')
images,var,nums=z['images'],z['variances'],z['numbers'];ids=['241928959','241928961']
assert len(nums)==5 and [row['event'] for row in r['events']]==nums.tolist()
y,x=np.indices(images[0].shape,dtype=float);checked=0
for group in ['events','leave_one_out','chronological_halves']:
 for row in r[group]:
  if group=='events':inds=np.flatnonzero(nums==row['event'])
  elif group=='leave_one_out':inds=np.flatnonzero(nums!=row['excluded_event'])
  else:inds=np.flatnonzero(np.isin(nums,row['events']))
  weight=1/var[inds]; total=weight.sum(axis=0)
  image=(weight*images[inds]).sum(axis=0)/total; error=1/np.sqrt(total)
  chi={}
  for tic in ids:
   columns=np.array([t['template_'+tic],np.ones_like(x),x-x.mean(),y-y.mean()])
   a=(columns/error).reshape(4,-1).T;b=(image/error).ravel()
   coeff=np.linalg.lstsq(a,b,rcond=None)[0];chi[tic]=float(np.sum((a@coeff-b)**2))
   np.testing.assert_allclose(coeff[0],row['hypotheses'][tic]['amplitude'])
   np.testing.assert_allclose(chi[tic],row['hypotheses'][tic]['chi2']);checked+=1
  assert min(chi,key=chi.get)==row['winner']
  np.testing.assert_allclose(chi[ids[1]]-chi[ids[0]],row['neighbor_minus_target_chi2'])
controls={tic:{'correct':sum(c['correct'] for c in r['controls'] if c['injected_tic']==tic),'trials':sum(c['trials'] for c in r['controls'] if c['injected_tic']==tic)} for tic in ids}
assert all(v['trials']==100 for v in controls.values())
save_json(p/'verification.json',{'verified':True,'direct_linear_fits_reconstructed':checked,'controls':controls,'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name not in ['verification.json','ASSESSMENT.md']},'limits':'Numerical reconstruction, not physical validation. Control count audit does not independently rerun the injections.'})
print(checked,controls)
