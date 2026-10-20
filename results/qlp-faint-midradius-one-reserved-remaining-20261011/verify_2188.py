from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());cp=out/'checkpoint-2188.json';c=read(cp);plan=read(out/'plan.json');expected={t['tic']:t for t in plan['targets']};counts=Counter()
assert c['n_completed']==2188 and c['n_planned']==2810 and c['plan_sha256']==sha(out/'plan.json')
for name,h in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==h
for item in c['inventory']:
 p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p);assert r['target']==expected[r['tic']];counts[r.get('disposition') or r['status']]+=1
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
assert dict(counts)==c['counts']
errors=read(out/'checkpoint-2188-errors.json')['rows']
assert {r['tic'] for r in errors}=={r['tic'] for r in c['inventory'] if r['status']=='error'}
for r in errors:
 assert r['finite_selected_flux']==r['finite_selected_errors']==r['usable_positive_flux_q0']==0
 assert sha(out/'targets'/f"{r['tic']}.json")==r['result_sha256'] and sha(Path(f"data/qlp/{r['tic']}-s{r['sector']:04d}.fits"))==r['raw_sha256']
assert len(c['review'])==4
reviews={}
for item in c['review']:
 tic=item['tic'];idx=item['screened_peak_index'];suffix='coverage-followup' if item['category']=='coverage_diagnostic' else 'followup'
 case=Path(f'results/qlp-faint-midradius-one-reserved-remaining-{suffix}-20261011/{tic}-peak{idx}');r=read(case/'review.json')
 for n,h in r['artifacts'].items():assert sha(case/n)==h
 f=read(case/'frozen.json');held=read(case/'heldout.json');assert len(held)==1 and held[0]['sector']==f['heldout_sectors'][0] and held[0]['conclusion']=='timing_prediction_inconclusive'
 for d in f['training_data']+held[0]['data']:assert sha(Path(f"data/qlp/{tic}-s{d['sector']:04d}.fits"))==d['source']['sha256']
 if (case/'source_review.json').exists():
  for path,h in read(case/'source_review.json')['artifacts'].items():assert sha(Path(path))==h
 reviews[str(case/'review.json')]=sha(case/'review.json')
save_json(out/'checkpoint-2188-verification.json',{'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(cp),'counts':dict(counts),'review_hashes':reviews,'error_audit_sha256':sha(out/'checkpoint-2188-errors.json'),'status':'2188 identities, source hashes and raw results; nine unusable inputs; four initial plot reviews and inconclusive reserved-sector tests verified. Snapshot only; source follow-up ongoing, no planet or completeness claim.'})
print(dict(counts),len(reviews),'reviews verified')
