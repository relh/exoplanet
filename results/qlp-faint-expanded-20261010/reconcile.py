"""Reconcile completed target, recovery and follow-up inventories."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
def read(p):return json.loads(Path(p).read_text())
a=read(out/'audit.json');plan=read(out/'plan.json');terminal=read(out/'results.json')
assert a['terminal_results_present'] and len(terminal)==len(plan['targets'])==1845
expected={x['tic'] for x in plan['targets']};assert {x['tic'] for x in terminal}==expected
assert len({x['tic'] for x in terminal})==1845
rows={};inventory=[]
for x in a['inventory']:
 p=Path(x['path']);assert sha(p)==x['sha256'];r=read(p);assert r['finished_utc'];rows[r['tic']]=r;inventory.append({'path':str(p),'sha256':sha(p)})
assert set(rows)==expected
for x in terminal:
 r=rows[x['tic']];assert all(x.get(k)==r.get(k) for k in ['status','error','disposition'])
errors={tic for tic,r in rows.items() if r['status']=='error'}
recpath=Path('results/qlp-faint-expanded-recovery-20261010/terminal.json');rec=read(recpath);assert rec['status']=='complete'
assert {r['tic'] for r in rec['records']}|set(rec['prior_recovery_tics'])==errors
assert len(rec['records'])+len(rec['prior_recovery_tics'])==len(errors)
recoveries=[]
for r in rec['records']:
 assert sha(Path(r['original_path']))==r['original_sha256'] and r['finished_utc']
 if r['status']=='screened':
  recovered=read(r['result_path']);assert recovered['finished_utc'];assert recovered['disposition']==r['disposition'];assert not r['followups']
 recoveries.append({'tic':r['tic'],'status':r['status'],'disposition':r.get('disposition')})
p=Path('results/qlp-faint-recovery-389918717-20261010/result.json');r=read(p);assert rec['prior_recovery_tics']==[389918717];rr=read(r['path']);assert rr['finished_utc'] and rr['disposition']==r['disposition'];recoveries.append({'tic':389918717,'status':r['status'],'disposition':r['disposition']})
fpath=Path('results/qlp-faint-expanded-followup-20261010/terminal.json');f=read(fpath);assert f['status']=='complete'
assert {(r['tic'],r['peak_index']) for r in f['records']}=={(r['tic'],r['rank']) for r in a['review']}
assert len(f['records'])==len(a['review'])==17
followups=[]
for r in f['records']:
 assert r['status']=='complete' and r['finished_utc'];assert sha(Path(r['discovery_path']))==r['discovery_sha256']
 folder=fpath.parent/f"{r['tic']}-peak{r['peak_index']}"
 for name in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']:assert (folder/name).exists()
 followups.append({'tic':r['tic'],'peak_index':r['peak_index'],'diagnostic_only':r['diagnostic_only'],'assessment':str(folder/'ASSESSMENT.md')})
usable=len(rows)-len(errors)+sum(r['status']=='screened' for r in recoveries)
save_json(out/'reconciliation.json',{'utc':now(),'n_attempted':len(rows),'original_counts':dict(Counter(r.get('disposition',r['status']) for r in rows.values())),'n_usable_distinct_after_recovery':usable,'recoveries':recoveries,'followups':followups,'n_original_screen':sum(not r['diagnostic_only'] for r in followups),'n_diagnostic_only':sum(r['diagnostic_only'] for r in followups),'terminal_hashes':{str(p):sha(p) for p in [out/'results.json',recpath,fpath]},'inventory':inventory,'interpretation':'Inventory and completed-work reconciliation, not scientific validation, novelty, sensitivity or survey completeness. Original errors and diagnostic flags retained.'})
print('Reconciled',len(rows),'targets;',usable,'usable distinct;',len(followups),'follow-ups')
