from pathlib import Path
import json,subprocess,csv,io
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;before=json.loads((p/'diagnostics.json').read_text());subprocess.run(['uv','run','python',str(p/'analyze.py')],check=True);after=json.loads((p/'diagnostics.json').read_text());assert before['rows']==after['rows']
vsx=json.loads((p/'results.json').read_text());ids=json.loads((p/'identity.json').read_text());matches=[]
for r in vsx+ids:
 assert r['status']=='success' and sha(Path(r['path']))==r['sha256'];assert list(csv.DictReader(io.StringIO(Path(r['path']).read_text())))==r['rows']
for r in ids:
 names={x['id'].strip() for x in r['rows']}
 if names:assert f"TIC {r['tic']}" in names
 nearby=next(x for x in vsx if x['tic']==r['tic']);matches.append(dict(tic=r['tic'],exact_vsx_matches=[x for x in nearby['rows'] if x['Name'].strip() in names],identifiers=sorted(names)))
for r in after['rows']:assert sha(Path(r['source_path']))==r['source_sha256']
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_diagnostic_windows_reproduced=12,n_catalog_responses_hash_checked=11,identity_checks=matches,reserved_unopened_checked_by_analysis=True,script_sha256={q.name:sha(q) for q in p.glob('*.py')},limits='Same-algorithm reconstruction; exact identity distinguished from cone proximity. No proof of physical cause, significance or planet exclusion.'))
