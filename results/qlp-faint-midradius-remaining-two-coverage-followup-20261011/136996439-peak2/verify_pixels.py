from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (15,16):
 raw=Path(f'results/tesscut-136996439-s{s}-20261011');proc=Path(f'results/spoc-pixels-136996439-s{s}-20261011');a=read(raw/'analysis.json');pp=Path(f'data/pixels/136996439-s{s:04d}.fits')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-136996439-20261011/neighbors.json'))
 with fits.open(pp) as h:assert h[0].header['TICID']==136996439 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(a['source']['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 if s==15:
  b=read(proc/'analysis/localization.json');assert b['source']['sha256']==sha(pp) and b['frozen_sha256']==sha(out/'frozen.json') and b['n_events']==2
 else:
  assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
  assert c['events'][1]['quality_counts']=={'4096':7} and c['events'][1]['inside_quality_zero']==0
 rows.append({'sector':s,'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'processed_raw_sha256':sha(pp),'processed_status_sha256':sha(proc/'status.json')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'Both raw stacked images and processed S15 plot inspected. RawS15positivefieldgradient, rawS16negativefield; processedS15weakmixedbackground/edge maximum. No reliable host position.','limits':'Background/quality concern, exact cause unresolved. ProcessedS16event3 allsevenpointsflag4096; unavailablequality-zeroevent is not nondetection. Samephotons not independentconfirmation. No Gaia inference from unreliable moments, no gate relaxation.'})
print('Raw/processed identity, provenance and flagged event verified.')
