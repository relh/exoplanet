"""Audit archived follow-up records and identify unaccounted modern-gate peaks."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
a=json.loads(Path('results/two-reserved-tier-audit-20261011/audit.json').read_text())
known={str(Path(rs[0]['path']).resolve()) for rs in a['records'].values()}
rows=[];terminals=[];seen=set();issues=[];duplicates=[];conclusions=Counter()
for p in sorted(Path('results').glob('qlp-faint*followup*/terminal.json')):
 if 'one-reserved' in str(p):continue
 d=json.loads(p.read_text())
 terminals.append({'path':str(p),'sha256':sha(p),'status':d['status']})
 if d['status']!='complete':issues.append({'path':str(p),'issue':'not complete'})
 for r in d['records']:
  discovery=Path(r['discovery_path'])
  if str(discovery.resolve()) not in known:continue
  key=(str(discovery.resolve()),r['peak_index'])
  duplicate=key in seen
  if duplicate:duplicates.append({'path':str(p),'tic':r['tic'],'peak_index':r['peak_index'],'discovery_path':str(discovery)})
  seen.add(key)
  assert sha(discovery)==r['discovery_sha256']
  folder=p.parent/f"{r['tic']}-peak{r['peak_index']}"
  artifacts={}
  for name in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']:
   q=folder/name
   if q.exists():artifacts[name]=sha(q)
   else:issues.append({'path':str(q),'issue':'missing'})
  if 'frozen.json' in artifacts:
   frozen=json.loads((folder/'frozen.json').read_text())
   assert frozen['discovery_sha256']==r['discovery_sha256']
  if not duplicate:
   for h in r.get('heldout',[]):conclusions[h.get('conclusion',h.get('status','unknown'))]+=1
  rows.append({'tic':r['tic'],'peak_index':r['peak_index'],'discovery_path':str(discovery),'folder':str(folder),'status':r['status'],'artifacts':artifacts})
# Retrospective modern-gate comparison only; historical policies can differ.
base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'}
extra={'secondary_unmeasurable','fewer_than_3_supported_events'}
gaps=[]
for rs in a['records'].values():
 p=Path(rs[0]['path']);r=json.loads(p.read_text())
 for i,peak in enumerate(r.get('screened_peaks',[])):
  flags=set(peak['flags'])
  eligible=flags<=base or (flags<=base|extra and bool(flags&extra) and peak['diagnostics']['supported_events']>=2)
  if eligible and (str(p.resolve()),i) not in seen:gaps.append({'tic':r['tic'],'path':str(p),'peak_index':i,'flags':peak['flags']})
save_json(out/'followups.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'n_terminal_inventories':len(terminals),'n_unique_peaks':len(seen),'n_distinct_stars':len({r['tic'] for r in rows}),'heldout_conclusions':dict(conclusions),'issues':issues,'duplicate_records_retained_but_not_counted':duplicates,'modern_gate_unaccounted':gaps,'terminals':terminals,'rows':rows,'limits':'Artifact existence and discovery provenance, not astrophysical validation. Modern-gate comparison is retrospective and may differ from historical policies; gaps require review. Reserved-sector conclusions may be timing-inconclusive.'})
print('inventories',len(terminals),'peaks',len(seen),'stars',len({r['tic'] for r in rows}),'issues',len(issues),'modern gaps',len(gaps),'held',dict(conclusions))
