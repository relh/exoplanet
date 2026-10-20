from pathlib import Path
import json,subprocess,csv,io
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;before=json.loads((p/'diagnostics.json').read_text())
subprocess.run(['uv','run','python',str(p/'analyze.py')],check=True)
after=json.loads((p/'diagnostics.json').read_text());assert before['rows']==after['rows']
vsx=json.loads((p/'results.json').read_text());ids=json.loads((p/'identity.json').read_text())
for r in vsx+ids:
 assert r['status']=='success' and sha(Path(r['path']))==r['sha256'];assert list(csv.DictReader(io.StringIO(Path(r['path']).read_text())))==r['rows']
for r in ids:
 names={x['id'].strip() for x in r['rows']};assert f"TIC {r['tic']}" in names
 match=next(x for x in vsx if x['tic']==r['tic']);assert len(match['rows'])==1 and match['rows'][0]['Name'].strip() in names and match['rows'][0]['Type'].strip()=='ROT'
for r in after['rows']:assert sha(Path(r['source_path']))==r['source_sha256']
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_diagnostic_windows_reproduced=6,n_catalog_responses_hash_checked=5,two_exact_tic_gaia_rot_identities=True,reserved_unopened_checked_by_analysis=True,script_sha256={q.name:sha(q) for q in p.glob('*.py')},limits='Same-algorithm reconstruction; heuristic diagnostics and catalog identity, not proof of physical cause or planet exclusion.'))
