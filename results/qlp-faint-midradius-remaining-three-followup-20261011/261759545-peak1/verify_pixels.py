from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
for sector in [99,100,101]:
 p=Path(f'results/tesscut-261759545-s{sector}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-261759545-20261011/neighbors.json'))
 q=Path(f'results/spoc-pixels-261759545-s{sector}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 rows.append({'sector':sector,'n_events':a['n_events'],'target_offset_pixels':a['offset_pixels'],'nearest_sources':a['neighbors'][:3],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt')})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All three raw plots inspected: compact near-target but offset feature in S99/S100 atop positive background; S101 near-target feature and strong structure around bright neighbors atop a field-wide positive offset. Raw moments do not establish a unique source; wide background tests reported separately. All three exact processed product requests HTTP404, not nondetections.'})
print('Verified raw images and retained processed-product errors.')
