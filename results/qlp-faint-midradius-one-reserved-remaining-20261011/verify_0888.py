from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());cp=out/'checkpoint-0888.json';c=read(cp);plan=read(out/'plan.json');expected={t['tic']:t for t in plan['targets']};counts=Counter()
assert c['n_completed']==888 and c['n_planned']==2810 and c['plan_sha256']==sha(out/'plan.json')
for item in c['inventory']:
 p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p);assert r['target']==expected[r['tic']];counts[r.get('disposition') or r['status']]+=1
assert dict(counts)==c['counts']
errors=[r for name in ['initial-errors.json','checkpoint-0888-new-errors.json'] for r in read(out/name)['rows']]
assert {r['tic'] for r in errors}=={r['tic'] for r in c['inventory'] if r['status']=='error'}
for r in errors:
 assert r['finite_selected_flux']==r['finite_selected_errors']==r['usable_positive_flux_q0']==0
 assert sha(out/'targets'/f"{r['tic']}.json")==r['result_sha256'] and sha(Path(f"data/qlp/{r['tic']}-s{r['sector']:04d}.fits"))==r['raw_sha256']
assert len(c['review'])==1 and c['review'][0]['tic']==26042880
case=Path('results/qlp-faint-midradius-one-reserved-remaining-followup-20261011/26042880-peak0');review=read(case/'review.json')
for name,h in review['artifacts'].items():assert sha(case/name)==h
for path,h in read(case/'source_review.json')['artifacts'].items():assert sha(Path(path))==h
f=read(case/'frozen.json');h=read(case/'heldout.json');assert f['heldout_sectors']==[51] and len(h)==1 and h[0]['conclusion']=='timing_prediction_inconclusive'
for d in h[0]['data']:assert sha(Path(f"data/qlp/26042880-s{d['sector']:04d}.fits"))==d['source']['sha256']
save_json(out/'checkpoint-0888-verification.json',{'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(cp),'counts':dict(counts),'review_sha256':sha(case/'review.json'),'error_audits':{name:sha(out/name) for name in ['initial-errors.json','checkpoint-0888-new-errors.json']},'status':'888 immutable target identities/counts, all four audited data failures, one completed source review and reserved raw timing evidence verified. Live search remains incomplete; no candidate promotion or completeness claim.'});print(dict(counts),'one reviewed contamination case; four unusable inputs')
