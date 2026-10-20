from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
npth=Path('results/neighbors-130291325-20261011/neighbors.json')
for sector in [87,88]:
 folder=Path(f'results/tesscut-130291325-s{sector}-20261011');a=read(folder/'analysis.json')
 assert a['n_events']==2 and sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(npth) and a['script_sha256']==sha(folder/'analyze.py')
 with np.load(folder/'images.npz') as z:assert np.all(z['difference']>0) if sector==87 else np.all(z['difference']<0)
 q=Path(f'results/spoc-quality-130291325-s{sector}-20261011');err=read(q/'error.json');assert '404' in err['error'] and err['script_sha256']==sha(q/'run.py')
 rows.append({'sector':sector,'raw_sha256':a['source']['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(folder/'difference.png'),'processed_error_sha256':sha(q/'error.json'),'visual_review':'Broad positive background dominates, no compact stellar dip.' if sector==87 else 'Entirely negative background residual, no dimming-source localization.'})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Both plots inspected. Same photons as QLP; no calibrated PRF fit or source attribution. Moments of broad or negative maps are not hosts. Missing requested processed light curves are not nondetections.'})
print('Verified two raw maps and two retained HTTP404 failures')
