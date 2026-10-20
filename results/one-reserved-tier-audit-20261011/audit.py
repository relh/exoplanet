"""Read-only reconciliation of the completed exploratory tier, preserving failures."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json, sha, now
out=Path(__file__).parent
inventory=Path('results/qlp-faint-one-reserved-after35-20261010/coverage.json')
d=json.loads(inventory.read_text())
assert d['n_remaining_distinct']==0
rows=[];seen=set();counts=Counter();missing=[];usable=0;followups=0
for name,digest in d['prior_selections'].items():
 if 'one-reserved-sector' not in name:continue
 p=Path(name);assert sha(p)==digest
 selected=json.loads(p.read_text());ids={t['tic'] for t in selected}
 assert len(ids)==len(selected) and not seen&ids
 seen.update(ids)
 folder=Path(str(p.parent).replace('-selection-','-pilot-'))
 rp=folder/'reconciliation.json'
 if not rp.exists():
  missing.append(str(rp));continue
 r=json.loads(rp.read_text())
 assert r['n_completed']==len(ids)
 actual=set()
 for item in r['inventory']:
  q=Path(item['path']);assert sha(q)==item['sha256']
  z=json.loads(q.read_text());actual.add(z['tic'])
 assert actual==ids
 for name,h in r['terminal_hashes'].items():assert sha(Path(name))==h
 for f in r['followups']:
  policy='pilot-followup' if f['policy']=='original' else 'pilot-coverage-followup'
  base=Path(str(folder).replace('-pilot-',f'-{policy}-'))/f"{f['tic']}-peak{f['peak_index']}"
  for name,h in f['artifacts'].items():assert sha(base/name)==h
 for rec in r.get('recoveries',[]):
  for name,h in rec['artifacts'].items():assert sha(Path(name))==h
 counts.update(r['counts']);usable+=r['n_distinct_usable_after_recovery'];followups+=len(r['followups'])
 rows.append({'sector_folder':str(folder),'n_selected':len(ids),'counts':r['counts'],'usable_after_recovery':r['n_distinct_usable_after_recovery'],'n_followup_peaks':len(r['followups']),'reconciliation_sha256':sha(rp)})
result={'utc':now(),'script_sha256':sha(Path(__file__)),'inventory_sha256':sha(inventory),'n_selected_distinct':len(seen),'n_reconciled_batches':len(rows),'counts':dict(counts),'usable_after_recovery':usable,'n_followup_peaks':followups,'missing_reconciliations':missing,'batches':rows,'limits':'Artifact-integrity audit, not re-execution or astrophysical validation. Discovery dispositions precede detailed vetting. Follow-up peaks are not distinct planets. No completeness or novelty claim.'}
save_json(out/'audit.json',result)
print({k:v for k,v in result.items() if k not in ['batches','limits']})
