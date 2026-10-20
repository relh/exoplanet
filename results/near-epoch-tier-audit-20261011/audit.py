"""Reconcile the entire frozen near-epoch tier, including failures and controls."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(Path(p).read_text())
initial=Path('results/qlp-near-epoch-inventory-20261011/eligible.json')
expected={r['tic'] for r in read(initial)};seen=set();counts=Counter();batches=[];controls=[];followups=[];failures=[]
last=read('results/qlp-near-epoch-after20-20261011/inventory.json')
assert last['n_eligible']==0
for name,digest in last['additional_prior_selections'].items():
 selection=Path(name);assert sha(selection)==digest
 targets=read(selection);ids={t['tic'] for t in targets}
 assert len(ids)==len(targets) and not seen&ids;seen.update(ids)
 folder=Path(str(selection.parent).replace('-selection-','-pilot-'))
 plan=read(folder/'plan.json');rec=read(folder/'reconciliation.json');terminal=read(folder/'results.json')
 assert plan['targets']==targets and sha(selection)==plan['source_sha256']
 assert {r['tic'] for r in terminal}==ids and len(terminal)==len(ids)==rec['n_completed']
 assert sha(folder/'reconcile.py')==rec['script_sha256']
 for name2,digest2 in rec['terminal_hashes'].items():assert sha(Path(name2))==digest2
 for item in rec['inventory']:
  p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p)
  assert r['tic'] in ids and r['target']==next(t for t in targets if t['tic']==r['tic'])
  counts[r.get('disposition') or r['status']]+=1
  if r['status']=='error':
   assert sha(folder/'failure_check.json')==rec['failure_check_sha256']
   failures.append({'tic':r['tic'],'error':r['error'],'review':str(folder/'failure_check.json'),'sha256':sha(folder/'failure_check.json')})
  else:
   assert r['status']=='screened'
   for ev in r['data']:assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
 for f in rec['followups']:
  parent=Path(str(folder).replace('-pilot-','-pilot-followup-' if f['policy']=='original' else '-pilot-coverage-followup-'))/f"{f['tic']}-peak{f['peak_index']}"
  for name2,digest2 in f['artifacts'].items():assert sha(parent/name2)==digest2
  followups.append(f)
 for suffix in ['injections','long-injections']:
  dest=Path(str(folder).replace('-pilot-',f'-{suffix}-'))
  if not (dest/'results.json').exists():
   assert len(ids)==1 and len([r for r in terminal if r['status']=='error'])==1 and (dest/'NOT_RUN.txt').exists()
   controls.append({'folder':str(dest),'status':'not_run_unusable_baseline'});continue
  a=read(dest/'audit.json');b=read(dest/'bounds.json');cp=read(dest/'plan.json')
  assert a['terminal'] and sha(dest/'results.json')==a['input_sha256'] and sha(dest/'audit.json')==b['audit_sha256']
  assert cp['targets']==targets[:3] and len(a['rows'])==len(cp['targets'])*4==len(b['rows'])
  for r in a['rows']:assert sha(Path(r['path']))==r['source_sha256']
  for r in b['rows']:assert r['result_sha256']==next(x['source_sha256'] for x in a['rows'] if (x['tic'],x['period'],x['radius_earth'])==(r['tic'],r['period'],r['radius_earth']))
  for t in cp['targets']:
   eq=read(dest/f"{t['tic']}-baseline-equivalence.json");assert eq['exact_arrays_equal'] and eq['windows']==[1.5,2.5]
  passing=[r for r in a['rows'] if r['noncrowding_screen_pass']]
  assert all(any(m['within_half_injected_duration_at_three_times'] for m in r['matches']) for r in passing)
  controls.append({'folder':str(dest),'status':'complete','n':len(a['rows']),'in_grid':sum(r['in_grid'] for r in b['rows']),'passes':len(passing),'earth_passes':sum(r['radius_earth']==1 for r in passing),'audit_sha256':sha(dest/'audit.json')})
 batches.append({'selection':str(selection),'n':len(ids),'selection_sha256':digest,'reconciliation':str(folder/'reconciliation.json'),'reconciliation_sha256':sha(folder/'reconciliation.json')})
assert seen==expected and len(seen)==271
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'n_selected':len(seen),'counts':dict(counts),'n_usable':len(seen)-len(failures),'batches':batches,'failures':failures,'followups':followups,'controls':controls,'initial_sha256':sha(initial),'final_inventory_sha256':sha(Path('results/qlp-near-epoch-after20-20261011/inventory.json')),'interpretation':'Scoped tier accounting and artifact integrity, not astrophysical confirmation, all-TESS coverage or completeness. Dependent controls with different sampling cannot be pooled into a survey recovery probability.'})
print('selected',len(seen),'usable',len(seen)-len(failures),'counts',dict(counts),'batches',len(batches),'followups',len(followups))
print('controls',sum(c.get('n',0) for c in controls),'in_grid',sum(c.get('in_grid',0) for c in controls),'passes',sum(c.get('passes',0) for c in controls),'earth_passes',sum(c.get('earth_passes',0) for c in controls))
