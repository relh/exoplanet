"""Reconcile the completed pilot and its explicitly reviewed lead."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');results=read(out/'results.json')
assert len(results)==len(plan['targets'])==100
assert {r['tic'] for r in results}=={t['tic'] for t in plan['targets']}
checkpoint=read(out/'checkpoint-0100.json')
assert [(r['tic'],r['screened_peak_index']) for r in checkpoint['review']]==[(386739254,0),(386739254,1)]
for row in checkpoint['inventory']:assert sha(Path(row['path']))==row['sha256']
for target in plan['targets']:
 row=read(out/'targets'/f"{target['tic']}.json")
 assert row['target']==target and row['status']=='screened' and row['finished_utc']
 for ev in row['data']:
  raw=Path(f"data/qlp/{target['tic']}-s{ev['sector']:04d}.fits")
  assert sha(raw)==ev['source']['sha256'] and raw.stat().st_size==ev['source']['bytes']
for name,digest in plan['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==digest
original=Path('results/qlp-faint-sector91-pilot-followup-20261010')
coverage=Path('results/qlp-faint-sector91-pilot-coverage-followup-20261010')
r=read(original/'terminal.json');c=read(coverage/'terminal.json')
assert r['status']==c['status']=='complete' and not r['records']
assert [(x['tic'],x['peak_index'],x['status']) for x in c['records']]==[(386739254,0,'complete'),(386739254,1,'complete')]
artifacts={}
for rec in c['records']:
 dest=coverage/f"{rec['tic']}-peak{rec['peak_index']}"
 f=read(dest/'frozen.json');h=read(dest/'heldout.json')
 assert f['discovery_sha256']==sha(out/'targets/386739254.json')
 assert rec['discovery_sha256']==f['discovery_sha256']
 assert {x['sector'] for x in h}==set(f['heldout_sectors']) and all(x['started_utc']>=f['utc'] for x in h)
 artifacts[str(dest)]={name:sha(dest/name) for name in ['frozen.json','heldout.json','secondary.json','discovery.png','ASSESSMENT.md']}
save_json(out/'reconciliation.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'n_completed':100,'n_reviewed_leads':2,'checkpoint_sha256':sha(out/'checkpoint-0100.json'),'pilot_audit_sha256':sha(out/'audit.json'),'followup_artifacts':artifacts,'interpretation':'Integrity and explicit review inventory passed; not scientific validation or candidate promotion.'})
print('Pilot reconciled: 100 completed searches, two reviewed unresolved peaks')
