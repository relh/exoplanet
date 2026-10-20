"""Verify both bounded residual cohorts and all review-pass follow-ups."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;ids=set();counts=Counter();rounds=0;passes=[];cohorts=[]
follow={}
for dirname in ['qlp-residual2-followup-20261010','qlp-residual2-followup2-20261010']:
 root=Path('results')/dirname
 for item in json.loads((root/'plan.json').read_text())['items']:
  key=(item['path'],item['peak_index']);assert key not in follow
  follow[key]=root/f"{item['tic']}-{item['round']}-peak{item['peak_index']}"
for i in [1,2]:
 root=Path(f'results/qlp-full-pool-residual{i}-20261010');run=json.loads((root/'run.json').read_text());assert run['status']=='complete'
 selected=json.loads(Path(run['selection_path']).read_text());rows=json.loads((root/'results.json').read_text());assert len(selected)==len(rows)==run['n_cases']
 for row in rows:
  assert row['tic'] not in ids;ids.add(row['tic'])
  for a in row['rounds']:
   p=Path(a['result_path']);d=json.loads(p.read_text());counts[d.get('disposition',d['status'])]+=1;rounds+=1
   assert a['removed_fraction']<=.2
   for j,k in enumerate(d.get('screened_peaks',[])):
    if set(k['flags'])<={'crowding_or_missing_crowding'}:
     dest=follow[(str(p),j)];assert (dest/'heldout.json').exists() and (dest/'ASSESSMENT.md').exists()
     passes.append({'tic':d['tic'],'path':str(p),'sha256':sha(p),'peak_index':j,'followup':str(dest),'heldout_sha256':sha(dest/'heldout.json'),'assessment_sha256':sha(dest/'ASSESSMENT.md')})
 cohorts.append({'directory':str(root),'n_cases':len(rows),'run_sha256':sha(root/'run.json'),'results_sha256':sha(root/'results.json')})
assert len(follow)==len(passes)
save_json(out/'audit.json',{'utc':now(),'n_unique_targets':len(ids),'n_rounds':rounds,'counts':dict(counts),'n_review_passes':len(passes),'review':passes,'cohorts':cohorts,'limits':'Selected534 previously searched stars; no additional unique discovery targets. Conditional residual trials and mask ephemerides uncalibrated. Inconclusive timing not planet exclusion; no likely planet or completeness claim.'})
print(len(ids),rounds,dict(counts),len(passes))
