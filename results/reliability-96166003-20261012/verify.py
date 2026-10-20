from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,now,read_curve
from exoplanet.search import flatten
from exoplanet.followup import refine_training
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());obs=json.loads((O/'observed.json').read_text());rows=json.loads((O/'results.json').read_text());z=np.load(O/'input.npz');perms=np.load(O/'permutations.npz')['indices'];assert len(rows)==len(perms)==120
for path,h in p['inputs'].items():assert sha(Path(path))==h
for s in p['sectors']:
 t,y,e,meta=read_curve(Path(f'data/lightcurves/s{s:04d}-96166003.fits'));assert meta['ticid']==96166003 and meta['sector']==s;t,y,e=flatten(t,y,e,window=1.5);m=z['sector']==s
 for key,a in dict(t=t,y=y,e=e).items():np.testing.assert_array_equal(a,z[key][m])
for i,(r,ix) in enumerate(zip(rows,perms)):
 rng=np.random.default_rng(np.random.SeedSequence([20261012,96166003,int(r['block_days']*100),r['draw']]));expected=np.arange(len(ix))
 for s in p['sectors']:
  sector=np.flatnonzero(z['sector']==s);cuts=np.r_[0,np.flatnonzero(np.diff(z['t'][sector])>.3)+1,len(sector)]
  for lo,hi in zip(cuts[:-1],cuts[1:]):
   seg=sector[lo:hi]
   if len(seg)<2:continue
   size=max(2,int(round(r['block_days']/np.median(np.diff(z['t'][seg])))));blocks=[seg[j:j+size] for j in range(0,len(seg),size)];expected[seg]=np.concatenate([blocks[j] for j in rng.permutation(len(blocks))])
 np.testing.assert_array_equal(ix,expected);np.testing.assert_array_equal(np.sort(ix),np.arange(len(ix)));assert np.all(z['sector'][ix]==z['sector']);assert r['exceeds']==(r['best']['power']>=obs['observed']['power'])
 if r['draw'] in [0,19,39]:
  best,_=refine_training(z['t'],z['y'][ix],z['e'][ix],p['seed'],seed_baseline=p['seed_baseline']);assert best==r['best']
for inv,key in [(False,'observed'),(True,'inverted')]:
 best,_=refine_training(z['t'],2-z['y'] if inv else z['y'],z['e'],p['seed'],seed_baseline=p['seed_baseline']);assert best==obs[key]
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),permutations_reconstructed=120,null_searches_recomputed=9,observed_and_inverted_recomputed=True,scope='Rawidentity/hash/preprocessing and every random permutation independently reconstructed; sector preservation and bijection checked. Ninepredeclarednullsearches+observed/inversion rerunusing sharedBLS. Not nullmodelvalidation or globalFAP.'));print('passed')
