from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
tic=356743185;sectors=[74, 75]

for s in sectors:
 p=Path(f'results/tesscut-{tic}-s{s}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path(f'results/neighbors-{tic}-20261011/neighbors.json'))
 q=Path(f'results/spoc-pixels-{tic}-s{s}-20261011');assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 row={'sector':s,'n_events':a['n_events'],'raw_sha256':a['source']['sha256'],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png')}
 if tic==148001520:
  assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
  with np.load(p/'images.npz') as z:assert np.all(z['difference']>0)
  row['processed_error_sha256']=sha(q/'stderr.txt')
 elif s==74:
  assert read(q/'status.json')['exit_code']==1 and 'Fewer than two image events' in (q/'stderr.txt').read_text()
  with np.load(p/'images.npz') as z:assert np.all(z['difference']<0)
  c=read(q/'coverage.json');assert sha(Path('data/pixels/356743185-s0074.fits'))==c['source']['sha256']
  assert all(r['n_inside_quality_zero']==0 for r in c['events']) and sum(r['n_inside'] for r in c['events'])==115
  row['coverage_sha256']=sha(q/'coverage.json');row['processed_error_sha256']=sha(q/'stderr.txt')
 else:
  assert read(q/'status.json')['exit_code']==0;b=read(q/'analysis/localization.json')
  assert b['tic']==tic and b['sector']==s and b['n_events']==2
  assert b['frozen_sha256']==sha(out/'frozen.json')
  assert sha(Path(f'data/pixels/{tic}-s{s:04d}.fits'))==b['source']['sha256']
  row['processed_sha256']=sha(q/'analysis/localization.json');row['processed_plot_sha256']=sha(q/'analysis/difference.png')
 rows.append(row)
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'Three plots inspected: raw S74 entirely negative, S75 field-wide positive; processed S75 weak mixed residual. No reliable source moment. Processed S74 fails event gate; its coverage audit finds all115 in-event exposures flagged4096.'})
print('Verified source evidence and retained failures for',tic)
