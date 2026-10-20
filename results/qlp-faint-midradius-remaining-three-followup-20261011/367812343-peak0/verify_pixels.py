from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
rows=[]
for s in [78,79]:
 p=Path(f'results/tesscut-367812343-s{s}-20261011');files=read(p/'files.json')
 for r in files:assert sha(Path(r['path']))==r['sha256']
 q=Path(f'results/spoc-pixels-367812343-s{s}-20261011');assert read(q/'status.json')['exit_code']==1
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 assert ('404 Client Error' if s==78 else 'Fewer than two image events') in (q/'stderr.txt').read_text()
 if s==78:
  assert read(p/'status.json')['exit_code']==1 and read(p/'status.json')['script_sha256']==sha(p/'analyze.py')
  assert 'Fewer than two image events' in (p/'stderr.txt').read_text()
 else:
  a=read(p/'analysis.json');assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
  assert a['neighbor_sha256']==sha(Path('results/neighbors-367812343-20261011/neighbors.json')) and a['n_events']==2
  with np.load(p/'images.npz') as z:assert np.all(z['difference']<0)
 rows.append({'sector':s,'raw_files':files,'raw_artifacts':{x.name:sha(x) for x in p.iterdir() if x.is_file()},'processed_artifacts':{x.name:sha(x) for x in q.iterdir() if x.is_file()}})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'S79 plot inspected: entirely negative residual, no valid dimming-source position. S78 failed fewer than two image events. Processed S78 HTTP404; S79 fewer than two image events. No host or planet conclusion.'})
print('Verified raw hashes, negative map and retained failures.')
