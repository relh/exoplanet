"""Audit selected-target coverage directly without presuming successful searches."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
ip=Path('results/qlp-faint-one-reserved-after35-20261010/coverage.json')
d=json.loads(ip.read_text());selected={};sources={}
for name,h in d['prior_selections'].items():
 if 'one-reserved-sector' in name:continue
 p=Path(name);assert sha(p)==h
 sources[name]=h
 for t in json.loads(p.read_text()):
  assert t['tic'] not in selected
  selected[t['tic']]=t
found={};plans=[];mismatches=[]
for p in sorted(Path('results').glob('qlp-faint*/plan.json')):
 folder=p.parent
 if any(x in folder.name for x in ['one-reserved','injection','followup','recovery']):continue
 plan=json.loads(p.read_text())
 ts=plan.get('targets',[])
 if not isinstance(ts,list) or not ts:continue
 used=0
 for t in ts:
  if not isinstance(t,dict) or t.get('tic') not in selected:continue
  tic=t['tic'];q=folder/'targets'/f'{tic}.json'
  if not q.exists():continue
  r=json.loads(q.read_text())
  if r.get('target')!=t:
   mismatches.append(str(q));continue
  # A pilot may annotate its target; compare actual training/heldout sector identities.
  if t.get('training_sectors')!=selected[tic].get('training_sectors'):continue
  if t.get('heldout_sectors')!=selected[tic].get('heldout_sectors'):continue
  found.setdefault(tic,[]).append({'path':str(q),'sha256':sha(q),'status':r['status'],'disposition':r.get('disposition'),'error':r.get('error')})
  used+=1
 if used:plans.append({'path':str(p),'sha256':sha(p),'n_used':used})
counts=Counter();multi={};missing=[]
for tic in selected:
 rs=found.get(tic,[])
 if not rs:missing.append(tic);continue
 if len(rs)>1:multi[str(tic)]=rs
 # Count only unambiguous single records; do not silently prefer a favorable rerun.
 if len(rs)==1:counts[rs[0]['disposition'] or rs[0]['status']]+=1
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory_sha256':sha(ip),'selection_sources':sources,'n_selected':len(selected),'n_found_distinct':len(found),'counts_single_record':dict(counts),'missing_tics':missing,'multiple_records':multi,'target_plan_mismatches':mismatches,'plans':plans,'records':found,'limits':'Coverage audit before recovery. Multiple records and missing targets require review. Counts are not planet counts or completeness. Training and heldout sector identities checked against frozen selections.'})
print('selected',len(selected),'found',len(found),'missing',len(missing),'multiple',len(multi),'mismatch',len(mismatches),'single counts',dict(counts))
