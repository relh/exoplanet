from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
npth=Path('results/neighbors-392005513-20261011/neighbors.json')
for sector in [71,72]:
 folder=Path(f'results/tesscut-392005513-s{sector}-20261011');a=read(folder/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(npth) and a['script_sha256']==sha(folder/'analyze.py')
 with np.load(folder/'images.npz') as z:
  if sector==71:assert np.all(z['difference']<0)
 proc=Path(f'results/spoc-pixels-392005513-s{sector}-20261011')
 assert read(proc/'status.json')['exit_code']==1 and '404' in (proc/'stderr.txt').read_text()
 rows.append({'sector':sector,'raw_sha256':a['source']['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(folder/'difference.png'),'processed_status_sha256':sha(proc/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt'),'visual_review':'Entirely negative residual dominated by background; not host localization.' if sector==71 else 'Compact positive feature near target and faint neighbors; descriptive moment0.65pixel off target does not uniquely resolve host.'})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Both raw plots inspected; same photons as QLP, no PRF fit or calibrated confidence. Requested processed pixel products unavailable (HTTP404), not nondetections. Sector71 negative image is not a valid dimming-source centroid.'})
print('Verified conflicting raw maps and retained processed-product failures')
