from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,now,read_curve
from run import evaluate
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());rows=json.loads((O/'results.json').read_text());obs=json.loads((O/'observed.json').read_text());perms=np.load(O/'permutations.npz')['indices'];raw=[]
for path,h in p['inputs'].items():assert sha(Path(path))==h
for s in p['sectors']:
 t,y,e,meta=read_curve(Path(f'data/lightcurves/s{s:04d}-469309982.fits'));assert meta['ticid']==469309982 and meta['sector']==s;raw.append((t,y,e))
assert len(rows)==len(perms)==120
for row,ix in zip(rows,perms):
 rng=np.random.default_rng(np.random.SeedSequence([20261012,469309982,int(row['block_days']*100),row['draw']]));parts=[];shuffled=[];offset=0
 for t,y,e in raw:
  expected=np.arange(len(t));cuts=np.r_[0,np.flatnonzero(np.diff(t)>.3)+1,len(t)]
  for lo,hi in zip(cuts[:-1],cuts[1:]):
   seg=np.arange(lo,hi)
   if len(seg)<2:continue
   size=max(2,int(round(row['block_days']/np.median(np.diff(t[seg])))));blocks=[seg[j:j+size] for j in range(0,len(seg),size)];expected[seg]=np.concatenate([blocks[j] for j in rng.permutation(len(blocks))])
  parts.append(expected+offset);offset+=len(t);shuffled.append((t,y[expected],e[expected]))
 np.testing.assert_array_equal(ix,np.concatenate(parts));np.testing.assert_array_equal(np.sort(ix),np.arange(len(ix)))
 a,b=row['windows'];flag=a['best']['depth_snr']>=8 and b['best']['depth_snr']>=8 and abs(a['best']['period']/b['best']['period']-1)<.005 and not a['ranges']['search_boundary_hit'] and not b['ranges']['search_boundary_hit'];assert flag==row['eligible'];assert row['statistic']==min(a['best']['depth_snr'],b['best']['depth_snr']);assert row['exceeds']==(flag and row['statistic']>=obs['result']['statistic'])
 if row['draw'] in [0,19,39]:assert evaluate(shuffled,p['seed'],p['baseline'])=={k:row[k] for k in ['windows','eligible','statistic']}
assert evaluate(raw,p['seed'],p['baseline'])==obs['result'];source=json.loads(Path(p['source_path']).read_text())
for a,b in zip(obs['result']['windows'],source['windows']):assert a['best']==b['best'] and a['ranges']==b['timing_ranges']
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),permutations_rebuilt=120,two_window_null_refits=9,actual_saved_weak_seed_selection_reproduced=True,scope='Rawidentity/hash+archivedalgorithmhashes, everysector/gapblockpermutationindependentlyrebuilt, selection/statistic ruleschecked,9two-window searches andobservedrefit. Sharedflatten/BLS engine, notmodelcalibration.'));print('passed')
