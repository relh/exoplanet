from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
for sector in [99,100,101]:
 p=Path(f'results/tesscut-429294074-s{sector}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-429294074-20261011/neighbors.json'))
 q=Path(f'results/spoc-pixels-429294074-s{sector}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 rows.append({'sector':sector,'n_events':a['n_events'],'target_offset_pixels':a['offset_pixels'],'nearest_sources':a['neighbors'][:3],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt')})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All three raw plots inspected: S99 compact offset positive feature; S100 entirely negative field with relative target-region enhancement; S101 field-wide positive background with target/neighbor structure. Raw moments do not establish a source. Wider background tests reported separately. Raw background unmodeled beyond temporal subtraction; formal moments are not PRF confidence. Processed product HTTP404 errors are not nondetections.'})
print('Verified raw images and retained processed-product errors.')
