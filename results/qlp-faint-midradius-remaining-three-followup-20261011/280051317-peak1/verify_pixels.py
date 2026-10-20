from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in [67,68,69]:
 p=Path(f'results/tesscut-280051317-s{s}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-280051317-20261011/neighbors.json'))
 assert read(p/'status.json')['exit_code']==0 and a['n_events']==2
 q=Path(f'results/spoc-pixels-280051317-s{s}-20261011');c=read(q/'coverage.json')
 assert read(q/'status.json')['exit_code']==1 and 'Fewer than two image events' in (q/'stderr.txt').read_text()
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 assert c['script_sha256']==sha(q/'audit_coverage.py') and c['frozen_sha256']==sha(out/'frozen.json')
 raw=Path(f'data/pixels/280051317-s00{s}.fits')
 assert sha(raw)==c['source']['sha256']
 assert all(r['n_inside_quality_zero']==0 and r['inside_quality_counts']=={'4096':r['n_inside']} for r in c['events'])
 rows.append({'sector':s,'n_raw_events':a['n_events'],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt'),'processed_coverage_sha256':sha(q/'coverage.json'),'n_flagged_inside':sum(r['n_inside'] for r in c['events'])})
assert sum(r['n_flagged_inside'] for r in rows)==432
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All three raw plots inspected. S67 field-wide positive structure, S68 field-wide positive gradient plus target/neighbor features, S69 large field-wide positive offset plus target/neighbor features. Moments do not localize a reliable variable source. All 432 processed in-event exposures flagged4096, zeroquality0; processed difference-image gate fails allthree. Background/quality artifact concern, no secure host. Flagged observations are not nondetections.'})
print('Verified all three raw images and processed quality failures.')
