from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (74,75):
 raw=Path(f'results/tesscut-313485055-s{s}-20261011');proc=Path(f'results/spoc-pixels-313485055-s{s}-20261011');a=read(raw/'analysis.json');pp=Path(f'data/pixels/313485055-s{s:04d}.fits')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-313485055-20261011/neighbors.json'))
 with fits.open(pp) as h:assert h[0].header['TICID']==313485055 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(a['source']['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 if s==74:
  assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
  assert all(e['quality_counts']=={'4096':78} and e['inside_quality_zero']==0 for e in c['events'])
 else:
  b=read(proc/'analysis/localization.json');assert b['source']['sha256']==sha(pp) and b['frozen_sha256']==sha(out/'frozen.json') and b['n_events']==2
 rows.append({'sector':s,'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'processed_raw_sha256':sha(pp),'processed_status_sha256':sha(proc/'status.json')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'Both raw stacked plots and processedS75 inspected. RawS74entirefieldnegative; rawS75positivegradient; processedS75stronggradient/mixedtargetregion andedge maximum, no isolated source.','limits':'Background/quality concern, exact cause/host unresolved. All156processedS74insideexposuresflag4096; noqualityzerocoverage not nondetection. S75twoeventsavailable butgradient not reliablelocalization. NoGaiaattribution/gaterelaxation.'})
print('Image provenance and 156 flagged processed exposures verified.')
