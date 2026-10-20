from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text());rows=[]
for sector in [68,69]:
 folder=Path(f'results/tesscut-469939625-s{sector}-20261011');files=read(folder/'files.json');assert len(files)==1
 assert sha(Path(files[0]['path']))==files[0]['sha256']
 a=read(folder/'analysis.json');assert a['script_sha256']==sha(folder/'analyze.py') and len(a['rows'])==1
 r=a['rows'][0];assert r['frozen_sha256']==sha(out/'frozen.json') and r['pixel_sha256']==files[0]['sha256']
 assert r['n_inside']==79 and r['n_outside']==314
 rows.append({'sector':sector,'raw_sha256':files[0]['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(folder/r['plot']),'visual_review':'Broad positive residual across illuminated portion; target at cutout coverage boundary.' if sector==68 else 'Field-wide positive background difference with weak patchy structure; no repeatable compact stellar source.'})
qfolder=Path('results/spoc-quality-469939625-s69-20261011');q=read(qfolder/'quality.json')
assert q['source_sha256']==sha(Path('data/lightcurves/s0069-469939625.fits')) and q['frozen_sha256']==sha(out/'frozen.json')
assert q['script_sha256']==sha(qfolder/'run.py') and len(q['events'])==1 and q['events'][0]['quality_counts']=={'0':79}
errpath=Path('results/spoc-quality-469939625-s68-20261011/error.json');err=read(errpath)
assert '404' in err['error'] and err['script_sha256']==sha(errpath.parent/'run.py')
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'quality69_sha256':sha(qfolder/'quality.json'),'processed68_error_sha256':sha(errpath),'limits':'Both plots inspected. Single-event descriptive maps, no PRF fit or calibrated localization. Same photons as QLP. Sector69 quality-zero exposures do not validate a transit; Sector68 missing requested processed product is not nondetection.'})
print('Verified both raw maps and retained processed quality evidence/error')
