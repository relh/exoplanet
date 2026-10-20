from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
npth=Path('results/neighbors-332624792-20261011/neighbors.json')
for sector in [79,80]:
 folder=Path(f'results/tesscut-332624792-s{sector}-20261011');a=read(folder/'analysis.json')
 assert a['n_events']==2 and sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(npth) and a['script_sha256']==sha(folder/'analyze.py')
 with np.load(folder/'images.npz') as z:assert np.all(z['difference']>0) if sector==79 else np.all(z['difference']<0)
 q=Path(f'results/spoc-pixels-332624792-s{sector}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 rows.append({'sector':sector,'raw_sha256':a['source']['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(folder/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt'),'processed_status_sha256':sha(q/'status.json'),'visual_review':'Broad positive background dominates, no compact stellar dip.' if sector==79 else 'Entirely negative background residual, no dimming-source localization.'})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Both plots inspected. Same photons as QLP; no calibrated PRF fit or source attribution. Moments of broad or negative maps are not hosts. Missing requested processed pixel products are not nondetections.'})
print('Verified two raw maps and two retained HTTP404 failures')
