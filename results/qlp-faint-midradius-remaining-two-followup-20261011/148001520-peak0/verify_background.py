"""Verify wider-cutout diagnostics and retain both background masks."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'wide-background-plan.json');rows=[]
assert plan['frozen_sha256']==sha(out/'frozen.json')
helper=Path(plan['background_helper']);assert sha(helper)==plan['background_helper_sha256']
m=read(out/'corrected-moments.json');assert m['script_sha256']==sha(out/'corrected_moments.py') and m['helper_sha256']==sha(Path('src/exoplanet/pixel_vet.py'))
for sector in [87,88]:
 p=Path(f'results/tesscut-148001520-s{sector}-wide-20261011');a=read(p/'analysis.json');b=read(p/'background.json')
 assert sha(p/'background.py')==sha(helper)==b['script_sha256']
 assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-148001520-wide-20261011/neighbors.json'))
 assert sha(Path(a['source']['path']))==a['source']['sha256']
 assert b['analysis_sha256']==sha(p/'analysis.json') and b['images_sha256']==sha(p/'images.npz')
 assert [r['n_background_pixels'] for r in b['results']]=={87:[211,25],88:[244,42]}[sector]
 for r in m['rows']:
  if r['sector']!=sector:continue
  source=p/f"background-r{r['radius_pixels']}.npz";assert sha(source)==r['source_sha256']
  assert r['analysis_sha256']==sha(p/'analysis.json')
  assert r['nearest'][0]['tic']==738285152
 for n in ['analyze','background']:assert read(p/f'{n}-status.json')['exit_code']==0
 rows.append({'sector':sector,'analysis_sha256':sha(p/'analysis.json'),'background_sha256':sha(p/'background.json'),'difference_plot_sha256':sha(p/'difference.png'),'background_plot_sha256':sha(p/'background.png'),'background_pixels':[r['n_background_pixels'] for r in b['results']]})
save_json(out/'background_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'corrected_moments_sha256':sha(out/'corrected-moments.json'),'corrected_plot_sha256':sha(out/'corrected-moments.png'),'visual_review':'All four wide difference/background plots and four-panel corrected local view inspected. Near-target offset feature survives both masks in both sectors. S87 has stronger edge residual; global maximum cannot be used as signal localization. Local moments remain about0.97/1.32pixels off target, toward unresolved faint group. Not calibrated host attribution or independent observations.'})
print('Verified wide background checks, both masks and corrected local moments.')
