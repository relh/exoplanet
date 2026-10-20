from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'wide-background-plan.json');rows=[]
assert plan['frozen_sha256']==sha(out/'frozen.json')
helper=Path(plan['background_helper']);assert sha(helper)==plan['background_helper_sha256']
for s,n in [(99,1),(100,1),(101,1)]:
 p=Path(f'results/tesscut-261759545-s{s}-wide-20261011');a=read(p/'analysis.json');b=read(p/'background.json')
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-261759545-wide-20261011/neighbors.json'))
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert sha(p/'background.py')==sha(helper)==b['script_sha256']
 assert b['analysis_sha256']==sha(p/'analysis.json') and b['images_sha256']==sha(p/'images.npz')
 assert [r['n_background_pixels'] for r in b['results']]==[n,0]
 assert all(r['status']=='insufficient_background_pixels' for r in b['results'])
 assert not (p/'background-r3.npz').exists() and not (p/'background-r2.npz').exists()
 for name in ['analyze','background']:assert read(p/f'{name}-status.json')['exit_code']==0
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'background_sha256':sha(p/'background.json'),'difference_plot_sha256':sha(p/'difference.png'),'background_plot_sha256':sha(p/'background.png'),'background_pixels':[n,0]})
save_json(out/'background_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'All six wide difference/background plots inspected. All masks fail: two-pixel masks leave one background pixel per sector, three-pixel masks zero. Raw wide maps show crowded-field structure, including a much stronger remote feature in S100; no background correction or calibrated host attribution follows. Failed masks retained without relaxation.'})
print('Verified wide background diagnostics and all six failed masks.')
