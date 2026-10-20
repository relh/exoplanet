from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[];n=0
for s in (74,75):
 raw=Path(f'results/tesscut-154570351-s{s}-20261011');proc=Path(f'results/spoc-pixels-154570351-s{s}-20261011');a=read(raw/'analysis.json');pp=Path(f'data/pixels/154570351-s{s:04d}.fits')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-154570351-20261011/neighbors.json'))
 with fits.open(pp) as h:assert h[0].header['TICID']==154570351 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(a['source']['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
 assert all(e['inside_quality_zero']==0 for e in c['events']);n+=sum(e['inside'] for e in c['events'])
 rows.append({'sector':s,'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'processed_raw_sha256':sha(pp),'processed_status_sha256':sha(proc/'status.json')})
assert n==313
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'processed_inside_exposures':n,'processed_quality_zero_inside':0,'visual_review':'Both raw stacked plots inspected: entirefieldnegative, S74relative target/neighbor structure and S75gradient. Moments cannot locate transit host.','limits':'Background/quality concern. All313processedinsidepointsflagged (312flag4096,one128); absenceofqualityzerocoverage not nondetection. No quality/eventgatesrelaxed. No Gaia inference frominvalidmoments; exact physicalcause unresolved.'})
print('Verified 313 processed in-event exposures, none quality zero.')
