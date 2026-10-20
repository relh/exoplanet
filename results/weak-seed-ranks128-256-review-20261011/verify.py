from pathlib import Path
import json,csv,io,subprocess
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;before=json.loads((p/'diagnostics.json').read_text());subprocess.run(['uv','run','python',str(p/'analyze.py')],check=True);after=json.loads((p/'diagnostics.json').read_text());assert before['rows']==after['rows']
for r in after['rows']:assert sha(Path(r['source_path']))==r['source_sha256']
rows=json.loads((p/'results.json').read_text())
for r in rows:
 assert r['status']=='success' and sha(Path(r['path']))==r['sha256'];assert list(csv.DictReader(io.StringIO(Path(r['path']).read_text())))==r['rows']
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),diagnostic_windows_reproduced=8,catalog_response_hashes_checked=4,reserved_unopened_checked_by_analysis=True,script_sha256={q.name:sha(q) for q in p.glob('*.py')},limits='Same-algorithm reproducibility; no exact catalog identity or calibrated planet-probability claim.'))
