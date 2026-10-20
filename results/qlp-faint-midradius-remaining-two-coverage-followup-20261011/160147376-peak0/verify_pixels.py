from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (73,74):
 for kind in ('tesscut','spoc-pixels'):
  p=Path(f'results/{kind}-160147376-peak0-s{s}-20261011');c=read(p/'coverage.json')
  path=Path(read(p/'files.json')[0]['path']) if kind=='tesscut' else Path(f'data/pixels/160147376-s{s:04d}.fits')
  assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
  with fits.open(path) as h:
   assert h[0].header['SECTOR']==s
   if kind=='spoc-pixels':assert h[0].header['TICID']==160147376
  if kind=='spoc-pixels' or s==73:
   assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  else:
   a=read(p/'analysis.json');assert a['source']['sha256']==sha(path) and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py') and a['n_events']==2
   assert a['neighbor_sha256']==sha(Path('results/neighbors-160147376-20261011/neighbors.json'))
  if s==73:assert len(c['events'])==1 and c['events'][0]['inside_quality_zero']==15
  if s==74 and kind=='spoc-pixels':assert [e['quality_counts'] for e in c['events']]==[{'4096':17},{'4096':17}]
  rows.append({'sector':s,'kind':kind,'raw_sha256':sha(path),'coverage_sha256':sha(p/'coverage.json'),'status_sha256':sha(p/'status.json'),'stderr_sha256':sha(p/'stderr.txt')})
p=Path('results/tesscut-160147376-peak0-s74-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'raw_analysis_sha256':sha(p/'analysis.json'),'stack_plot_sha256':sha(p/'difference.png'),'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'S74 stack and both individual images inspected. Event1 entirely negative and event2 entirely positive, with field structure and relative target/neighbor features; no reliable isolated source.','limits':'S73onlyonepredictedimageevent; processedS74all34insideexposures4096flagged. Missing usable coverage not nondetection. Background/quality concern; exact source/cause unresolved. No gates relaxed, no Gaia attribution or planet exclusion.'})
print('Verified alternate-fit source evidence and coverage failures.')
