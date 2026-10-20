from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (49,50):
 raw=Path(f'results/tesscut-22741082-s{s}-20261011');proc=Path(f'results/spoc-pixels-22741082-s{s}-20261011');a=read(raw/'analysis.json');pp=Path(f'data/pixels/22741082-s{s:04d}.fits')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-22741082-20261011/neighbors.json'))
 with fits.open(pp) as h:assert h[0].header['TICID']==22741082 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(a['source']['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 if s==49:
  assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
  assert [e['quality_counts'] for e in c['events']]==[{'4096':26},{'0':26}]
 else:
  b=read(proc/'analysis/localization.json');assert b['source']['sha256']==sha(pp) and b['frozen_sha256']==sha(out/'frozen.json') and b['n_events']==2
 rows.append({'sector':s,'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'processed_raw_sha256':sha(pp),'processed_status_sha256':sha(proc/'status.json')})
p=Path('results/tesscut-22741082-s50-20261011');i=read(p/'individual-events.json')
for path,h in i['inputs'].items():assert sha(Path(path))==h
assert i['plot_sha256']==sha(p/'individual-events.png') and i['script_sha256']==sha(p/'plot_events.py')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'processed_plot_sha256':sha(Path('results/spoc-pixels-22741082-s50-20261011/analysis/difference.png')),'visual_review':'Both raw stacks, four individual raw maps and processedS50stack inspected. Alternating field backgrounds/column structure dominate raw; relative target features unresolved. ProcessedS50weakmixed residuals, no isolated source.','limits':'Background/quality concern; processedS49event0all26insideflag4096, event1availablebutminimumtwoeventgatefails. Missing coverage not nondetection; no Gaia inference or physicalcause certainty.'})
print('Source provenance, quality coverage and images verified.')
