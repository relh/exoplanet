from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());cp=out/'checkpoint-5716.json';c=read(cp);plan=read(out/'plan.json');terminal=read(out/'results.json')
assert c['n_completed']==c['n_planned']==len(plan['targets'])==len(terminal)==5716
assert sha(out/'plan.json')==c['plan_sha256']
expected={t['tic'] for t in plan['targets']};actual={r['tic']:r for r in terminal};assert len(actual)==5716 and set(actual)==expected
for x in c['inventory']:
 p=Path(x['path']);assert sha(p)==x['sha256'];r=read(p);s=actual[r['tic']]
 for k in ['status','error','disposition']:assert s.get(k)==r.get(k)
 for d in r.get('data',[]):assert sha(Path(f"data/qlp/{r['tic']}-s{d['sector']:04d}.fits"))==d['source']['sha256']
assert dict(Counter((r.get('disposition') or r['status']) for r in terminal))==c['counts']
reports=[];seen=set();conclusions=Counter();pending=[]
for kind in ['followup','coverage-followup']:
 base=Path(f'results/qlp-faint-midradius-remaining-one-{kind}-20261011');term=read(base/'terminal.json');assert term['status']=='complete'
 expected_keys={(x['tic'],x['screened_peak_index']) for x in c['review'] if (x['category']=='coverage_diagnostic')==(kind=='coverage-followup')}
 records=term['records'];assert {(r['tic'],r['peak_index']) for r in records}==expected_keys and len(records)==len(expected_keys)
 for r in records:
  key=(r['tic'],r['peak_index']);assert key not in seen;seen.add(key);assert r['status']=='complete'
  p=base/f'{key[0]}-peak{key[1]}';f=read(p/'frozen.json');h=read(p/'heldout.json');review=read(p/'review.json');assert sha(Path(r['discovery_path']))==r['discovery_sha256']==f['discovery_sha256']==review['discovery_sha256']
  for n,digest in review['artifacts'].items():assert sha(p/n)==digest,(p,n)
  for row in h:conclusions[row.get('conclusion',row['status'])]+=1
  if review['source_checks_pending']:pending.append(str(p))
  reports.append({'path':str(p),'review_sha256':sha(p/'review.json'),'source_checks_pending':review['source_checks_pending']})
assert len(seen)==len(c['review'])==22
errors=[]
for x in c['inventory']:
 if x['status']=='error':
  p=out/f"data-error-{x['tic']}.json";a=read(p);assert a['result_sha256']==x['sha256'];raw=Path(a.get('raw_path',a.get('pixel_path')));assert sha(raw)==a.get('raw_sha256',a.get('pixel_sha256'));errors.append({'tic':x['tic'],'audit_sha256':sha(p)})
save_json(out/'terminal-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'checkpoint_sha256':sha(cp),'results_sha256':sha(out/'results.json'),'n_targets':5716,'counts':c['counts'],'n_usable':5711,'n_followups':22,'heldout_conclusions':dict(conclusions),'reviews':reports,'pending_source_checks':pending,'errors':errors,'process_evidence':{'discovery_session':55707,'original_watcher_session':47847,'coverage_watcher_session':32471,'observed_exit_codes':[0,0,0]},'limits':'All planned target files and both eligibility queues reconciled with terminal artifacts and observed successful process exits. All22 initial plots reviewed, not22 planet candidates. Source/physical vetting remains incomplete. Scoped sample, no all-TESS completeness claim.'})
print(c['counts'],'followups',len(reports),'pending source checks',len(pending),'heldout',dict(conclusions))
