from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
for sector in [34,35]:
 p=Path(f'results/tesscut-257984190-s{sector}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-257984190-20261011/neighbors.json'))
 q=Path(f'results/spoc-pixels-257984190-s{sector}-20261011');status=read(q/'status.json')
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 if sector==34:assert status['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 else:
  b=read(q/'analysis/localization.json');assert status['exit_code']==0 and b['frozen_sha256']==sha(out/'frozen.json')
  assert sha(Path('data/pixels/257984190-s0035.fits'))==b['source']['sha256']
 rows.append({'sector':sector,'raw_events':a['n_events'],'raw_artifacts':{str(x):sha(x) for x in p.iterdir() if x.is_file()},'processed_artifacts':{str(x):sha(x) for x in q.rglob('*') if x.is_file()}})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All three available plots inspected. Raw34 displaced positive feature near257984147/162/166; raw35 and processed35 dominated by strong positive/negative structure near bright edge group257984151/161/532292521. Different source patterns, no repeatable compact target localization. Edge/dipole moments cannot establish a host. No calibrated PRF fit; same photons across processing. Processed34 HTTP404 is not a nondetection.'})
print('Verified available maps and retained failed product request.')
