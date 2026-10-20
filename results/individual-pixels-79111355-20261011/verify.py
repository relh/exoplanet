from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
from exoplanet.pixel_vet import difference_events
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');assert plan['module_sha256']==sha(Path('src/exoplanet/pixel_vet.py')) and plan['test_sha256']==sha(Path('tests/test_pixels.py'))
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/79111355-peak0/frozen.json');assert plan['frozen_sha256']==sha(fp)
rows=[]
for s in (94,95):
 p=out/f's{s}';a=read(p/'analysis.json');assert a['n_events']==1 and a['event_numbers']==[s-94]
 assert a['fit_sha256']==sha(fp) and a['script_sha256']==sha(p/'analyze.py')
 assert a['source']['sha256']==sha(Path(a['source']['path'])) and a['neighbor_sha256']==sha(Path('results/neighbors-79111355-20261011/neighbors.json'))
 original=Path(f'results/tesscut-79111355-s{s}-20261011');assert read(original/'status.json')['exit_code']==1
 rows.append({'sector':s,'analysis_sha256':sha(p/'analysis.json'),'images_sha256':sha(p/'images.npz'),'plot_sha256':sha(p/'difference.png'),'original_failure_sha256':sha(original/'stderr.txt')})
# Recompute an existing successful two-event case to check exact preservation.
p=Path('results/tesscut-149919534-s75-20261011');a=read(p/'analysis.json');source=Path(a['source']['path']);assert sha(source)==a['source']['sha256']
fit=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json');assert sha(fit)==a['fit_sha256']
with fits.open(source) as h:
 d=h[1].data;finite=np.isfinite(d['TIME']);args=[np.array(d[k][finite],float) for k in ('TIME','FLUX','FLUX_ERR')]
 diff,err,events,numbers=difference_events(*args,d['QUALITY'][finite],read(fit)['best'])
stored=np.load(p/'images.npz')
for value,key in ((diff,'difference'),(err,'error'),(events,'event_differences')):assert np.array_equal(value,stored[key],equal_nan=True)
assert numbers==a['event_numbers']
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'rows':rows,'aggregate_regression':{'reference_analysis_sha256':sha(p/'analysis.json'),'reference_images_sha256':sha(p/'images.npz'),'result':'Exact equality of aggregate difference, errors, event arrays and event numbers on existing two-event case.'},'visual_review':'Both single-event maps inspected. S94 target-adjacent positive and negative structure; S95 field-wide positive background. No consistent isolated source or reliable host moment.','limits':'Exploratory source diagnostics on opened QLP epochs, not blind confirmation; unchanged original two-event gate still fails. No Gaia attribution; catalog positions not motion propagated.'})
print('Individual provenance and exact aggregate regression verified.')
