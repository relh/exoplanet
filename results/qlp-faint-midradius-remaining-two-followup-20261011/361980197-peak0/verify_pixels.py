from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
rows=[]
for sector in [46,47]:
 p=Path(f'results/tesscut-361980197-s{sector}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-361980197-20261011/neighbors.json'))
 assert a['n_events']==2
 q=Path(f'results/spoc-pixels-361980197-s{sector}-20261011')
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 row={'sector':sector,'n_events':a['n_events'],'target_offset_pixels':a['offset_pixels'],'nearest_sources':a['neighbors'][:4],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png')}
 if sector==46:
  assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
  row['processed_error_sha256']=sha(q/'stderr.txt')
 else:
  b=read(q/'analysis/localization.json');assert read(q/'status.json')['exit_code']==0
  assert b['tic']==361980197 and b['sector']==47 and b['n_events']==2
  assert sha(Path('data/pixels/361980197-s0047.fits'))==b['source']['sha256']
  assert b['frozen_sha256']==sha(out/'frozen.json')
  row['processed_target_offset_pixels']=b['offset_from_header_target_pixels']
  row['processed_sha256']=sha(q/'analysis/localization.json');row['processed_plot_sha256']=sha(q/'analysis/difference.png')
 rows.append(row)
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All three available plots inspected. Compact positive source in the neighboring blend, displaced from target in both sectors. S47 raw peak at stamp boundary; processed S47 supports displacement but is near edge too. Exact blend component unresolved; moments not calibrated astrometry. Same-sector processing shares photons. S46 processed HTTP404 is not a nondetection.'})
print('Verified raw and processed source evidence and retained HTTP404.')
