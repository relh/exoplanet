"""Reconcile alternate-sector recovery plans without changing archived results."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
rp=out/'recoveries.json';ap=out/'audit.json'
rec=json.loads(rp.read_text());audit=json.loads(ap.read_text());rows=[]
for tic,records in rec['records'].items():
 for item in records:
  if set(item['training_sectors'])<=set(item['original_training_sectors']):continue
  q=Path(item['path']);assert sha(q)==item['sha256']
  r=json.loads(q.read_text());pp=q.parent.parent/'plan.json';p=json.loads(pp.read_text())
  origp=Path(audit['records'][tic][0]['path']);original=json.loads(origp.read_text())
  assert p['target']==r['target'] and p['utc']<=r['started_utc']
  assert sha(Path(p['original_path']))==p['original_sha256']==sha(origp)
  assert r['target']['heldout_sectors']==original['target']['heldout_sectors']
  assert not set(r['target']['training_sectors'])&set(original['target']['heldout_sectors'])
  assert 'separate discovery attempt' in p['policy']
  assert sha(Path(p['failed_raw']))==p['failed_raw_sha256']
  raws=[]
  for ev in r.get('data',[]):
   raw=Path(f"data/qlp/{tic}-s{ev['sector']:04d}.fits")
   assert sha(raw)==ev['source']['sha256']
   raws.append({'path':str(raw),'sha256':sha(raw)})
  rows.append({'tic':int(tic),'plan':str(pp),'plan_sha256':sha(pp),'result':str(q),'result_sha256':sha(q),'original_sha256':sha(origp),'plan_utc':p['utc'],'result_started_utc':r['started_utc'],'original_training':original['target']['training_sectors'],'alternate_training':r['target']['training_sectors'],'unchanged_reserved':r['target']['heldout_sectors'],'status':r['status'],'disposition':r.get('disposition'),'policy':p['policy'],'raws':raws})
assert len(rows)==16
save_json(out/'recovery-plan-verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'recoveries_sha256':sha(rp),'n_changed_sector_records':len(rows),'counts':dict(Counter(r['disposition'] or r['status'] for r in rows)),'rows':rows,'limits':'Plans precede recorded processing and preserve original reserved lists with zero training overlap. This verifies recorded provenance, not an independent forensic proof of no earlier data access. Alternate searches do not repair original sectors or add distinct stars.'})
print(Counter(r['disposition'] or r['status'] for r in rows))
