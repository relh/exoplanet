from pathlib import Path
import json
from exoplanet.pipeline import sha,read_curve,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure
p=Path(__file__).parent
plan=json.loads((p/'plan.json').read_text());run=json.loads((p/'run.json').read_text());selected=json.loads((p/'selected.json').read_text())
assert sha(Path(plan['source']))==plan['source_sha256']
assert selected==json.loads(Path(plan['source']).read_text())[384:512]
assert run['status']=='complete' and sha(p/'plan.json')==run['plan_sha256']
assert sha(p/'selected.json')==plan['selected_sha256'] and sha(p/'source-audit.json')==plan['audit_sha256']
assert sha(p/'select.py')==plan['selection_script_sha256'] and sha(p/'run.py')==run['runner_sha256']
for name,digest in run['source_sha256'].items():assert sha(p/'source'/name)==digest==sha(Path('src/exoplanet')/name)
assert {q.stem for q in (p/'targets').glob('*.json')}=={str(r['tic']) for r in selected}
raws=set();flags=[]
for row in selected:
 r=json.loads((p/'targets'/f"{row['tic']}.json").read_text());assert r['selection']==row and r['status']=='measured'
 original=json.loads(Path(row['original_path']).read_text());assert sha(Path(row['original_path']))==row['original_sha256'] and row['seed']==original['best']
 for s in row['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{row['tic']}.fits").exists()
 for w in r['windows']:
  assert {v['sector'] for v in w['training_data']}==set(row['target']['training_sectors'])
  for v in w['training_data']:
   raw=Path(f"data/lightcurves/s{v['sector']:04d}-{row['tic']}.fits");assert sha(raw)==v['source']['sha256'];*_,star=read_curve(raw);assert star['ticid']==row['tic'] and star['sector']==v['sector'];raws.add(str(raw))
   if v['sector'] in row['added_sectors']:assert v['source']['retrieved_utc']>plan['created_utc']
  t,y,e,_=load_training(row['target'],Path('data'),window=w['window_days']);best,ranges=refine_training(t,y,e,row['seed'],seed_baseline=row['original_baseline_days']);assert best==w['best'] and ranges==w['timing_ranges'];assert fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration'])==w['measurement']
 a,b=r['windows'];flag=a['best']['depth_snr']>=8 and b['best']['depth_snr']>=8 and abs(a['best']['period']/b['best']['period']-1)<.005 and not a['timing_ranges']['search_boundary_hit'] and not b['timing_ranges']['search_boundary_hit'];assert flag==r['local_review_flag']
 if flag:flags.append(row['tic'])
assert len(flags)==run['n_local_review_flags'] and run['n_errors']==0
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_targets=len(selected),raw_products_checked=len(raws),local_refinements_reproduced=2*len(selected),local_review_flags=sorted(flags),reserved_caches_absent=True,limitations='Reproducibility and integrity only; local flags are not full screening passes or calibrated significance.'))
print('Verified',len(selected),'targets',len(raws),'products',flags)
