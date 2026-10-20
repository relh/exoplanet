from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.campaign import load_training,joint_scan
from exoplanet.null_controls import block_permutation
p=Path(__file__).parent;run=json.loads((p/'run.json').read_text());results=json.loads((p/'results.json').read_text());assert run['status']=='complete';src=Path('results/review-362222987-20261011/discovery.json');assert sha(src)==run['discovery_sha256'];row=json.loads(src.read_text());t,y,e,evidence=load_training(row['target'],Path('data'))
for name,digest in run['source_sha256'].items():assert sha(p/'source'/name)==digest
for d in run['data']:assert sha(Path(f"data/lightcurves/s{d['sector']:04d}-362222987.fits"))==d['source']['sha256']
assert len(results)==48 and len({(r['block_days'],r['draw']) for r in results})==48
assert joint_scan(t,y,e)[2]==run['observed'];reruns=0
for r in results:
 assert r['block_days'] in [.5,1,2] and 0<=r['draw']<16
 rng=np.random.default_rng(np.random.SeedSequence([run['seed'],run['tic'],int(r['block_days']*10),r['draw']]))
 ix=block_permutation(t,r['block_days'],rng);assert np.array_equal(np.sort(ix),np.arange(len(t)))
 assert r['exceeds_observed_power']==(r['best']['power']>=run['observed']['power'])
 if r['draw']==0:assert joint_scan(t,y[ix],e[ix])[2]==r['best'];reruns+=1
for summary in run['summary']:assert summary['exceedances']==sum(r['exceeds_observed_power'] for r in results if r['block_days']==summary['block_days'])
save_json(p/'verification.json',dict(status='passed',permutations_verified=48,observed_search_reproduced=True,null_searches_reproduced=reruns,raw_hashes_verified=True,limits='Three of48 null searches rerun; other outcome accounting reconciled. Conditional maximum-power diagnostic, not full screening or calibrated FAP.'))
print(run['summary'])
