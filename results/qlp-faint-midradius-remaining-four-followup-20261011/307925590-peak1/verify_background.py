from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'wide-background-plan.json');rows=[]
assert plan['frozen_sha256']==sha(out/'frozen.json')
helper=Path(plan['background_helper']);assert sha(helper)==plan['background_helper_sha256']
base62=Path('results/tesscut-307925590-s62-wide-20261011')
assert read(base62/'analyze-status.json')['exit_code']==1 and 'No positive difference flux' in (base62/'analyze-stderr.txt').read_text()
u=base62/'uncentered';up=read(u/'plan.json')
assert up['original_failure_sha256']==sha(base62/'analyze-stderr.txt') and up['original_script_sha256']==sha(base62/'analyze.py')
assert sha(u/'files.json')==sha(base62/'files.json')
assert read(u/'analysis.json')['source_centroid_computed'] is False
assert 'difference_moment_xy' not in read(u/'analysis.json')
for s,counts in [(62,[87,15]),(63,[47,1]),(64,[75,6]),(65,[103,17])]:
 p=Path(f'results/tesscut-307925590-s{s}-wide-20261011')
 if s==62:p=p/'uncentered'
 a=read(p/'analysis.json');b=read(p/'background.json')
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-307925590-wide-20261011/neighbors.json'))
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert a['n_events']=={62:5,63:6,64:5,65:5}[s]
 assert sha(p/'background.py')==sha(helper)==b['script_sha256']
 assert b['analysis_sha256']==sha(p/'analysis.json') and b['images_sha256']==sha(p/'images.npz')
 assert [r['n_background_pixels'] for r in b['results']]==counts
 residuals={}
 for r in b['results']:
  file=p/f"background-r{r['mask_radius_pixels']:g}.npz"
  if r['n_background_pixels']<=10:
   assert r['status']=='insufficient_background_pixels' and not file.exists()
  else:residuals[str(r['mask_radius_pixels'])]=sha(file)
 for n in ['analyze','background']:assert read(p/f'{n}-status.json')['exit_code']==0
 rows.append({'sector':s,'path':str(p),'analysis_sha256':sha(p/'analysis.json'),'background_sha256':sha(p/'background.json'),'difference_plot_sha256':sha(p/'difference.png'),'background_plot_sha256':sha(p/'background.png'),'background_pixels':counts,'residual_sha256':residuals})
save_json(out/'background_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'original_s62_failure_sha256':sha(base62/'analyze-stderr.txt'),'visual_review':'All eight wide raw/background plots inspected, S62using separate no-centroid diagnostic with original failure retained. Positive/negative residual structure around bright neighbor persists after available plane fits; remote edge/source residuals not target localizations. Six masks fit, S63/S64three-pixel masks fail. No clean repeatable isolated target source or unique variable attribution established. No calibrated PRF confidence.'})
print('Verified four-sector background diagnostics, two mask failures and original centroid failure.')
