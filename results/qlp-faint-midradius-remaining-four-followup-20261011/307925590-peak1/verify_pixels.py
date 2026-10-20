from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
for sector in [62,63,64,65]:
 p=Path(f'results/tesscut-307925590-s{sector}-20261011');a=read(p/'analysis.json')
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-307925590-20261011/neighbors.json'))
 q=Path(f'results/spoc-pixels-307925590-s{sector}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 assert read(q/'plan.json')['script_sha256']==sha(q/'run.py')
 rows.append({'sector':sector,'n_events':a['n_events'],'target_offset_pixels':a['offset_pixels'],'nearest_sources':a['neighbors'][:3],'analysis_sha256':sha(p/'analysis.json'),'plot_sha256':sha(p/'difference.png'),'processed_error_sha256':sha(q/'stderr.txt')})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All four raw plots inspected: S62entirely negative, S63positive/negative feature around bright TIC307925559, S64offset positive group near same neighbor, S65positive background plus positive/negative bright-neighbor structure. No repeatable isolated target source established. Raw moments invalid as unique host confidence. All four exact processed pixel requests HTTP404, not nondetections.'})
print('Verified raw images and retained processed-product errors.')
