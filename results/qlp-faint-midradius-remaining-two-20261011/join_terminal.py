"""Join separate error reviews and unchanged retries once per original star."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text())
a=read(out/'checkpoint-4144.json');v=read(out/'terminal-verification.json')
assert sha(out/'checkpoint-4144.json')==v['checkpoint_sha256'] and sha(out/'results.json')==v['results_sha256']
checks_path=Path('results/qlp-faint-two-data-errors-20261011/verification.json');checks=read(checks_path);missing={r['tic']:r for r in checks['rows']}
for r in missing.values():
 assert sha(Path(r['original_path']))==r['original_sha256'] and sha(Path(r['result_path']))==r['result_sha256']
 assert read(Path(r['result_path']))['status']=='insufficient_training_coverage'
retry_path=Path('results/qlp-faint-network-retry-two-20261011/verification.json');retries={r['tic']:r for r in read(retry_path)['rows']}
assert set(missing).isdisjoint(retries)
errors={r['tic'] for r in a['inventory'] if r['status']=='error'};assert errors==set(missing)|set(retries)
rows=[]
for r in a['inventory']:
 p=Path(r['path']);assert sha(p)==r['sha256'];tic=r['tic']
 q=None if tic in missing else Path(retries[tic]['path']) if tic in retries else p
 if tic in retries:
  assert sha(q)==retries[tic]['sha256'];assert read(q)['target']==read(p)['target']
 rows.append({'tic':tic,'original_path':str(p),'original_sha256':sha(p),'usable_path':str(q) if q else None,'usable_sha256':sha(q) if q else None,'disposition':read(q)['disposition'] if q else 'insufficient_training_coverage'})
assert len(rows)==len({r['tic'] for r in rows})==4144
counts=dict(Counter(r['disposition'] for r in rows));assert counts=={'below_screen_threshold':3218,'flagged':886,'insufficient_training_coverage':40}
save_json(out/'joined-terminal.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'original_counts':a['counts'],'counts':counts,'n_distinct_stars':4144,'n_distinct_usable':4104,'rows':rows,'terminal_verification_sha256':sha(out/'terminal-verification.json'),'data_error_verification_sha256':sha(checks_path),'network_retry_verification_sha256':sha(retry_path),'limits':'Original42failures retained. Two unchanged network retries counted once, forty stars have insufficient assigned training coverage. All71 original eligible followups completed but scientific review remains incomplete. No planet-validation or all-TESS completeness claim.'})
print(counts)
