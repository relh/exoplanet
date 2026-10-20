from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (24,25):
 p=Path(f'results/tesscut-29439764-peak1-s{s}-20261011');c=read(p/'coverage.json');f=read(p/'files.json')[0]
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 q=Path('results/spoc-pixels-29439764-peak1-s24-20261011') if s==24 else Path('results/spoc-pixels-29439764-s25-20261011');assert read(q/'status.json')['exit_code']==1
 if s==24:
  a=read(p/'analysis.json');assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py') and a['event_numbers']==[0,1]
  assert a['neighbor_sha256']==sha(Path('results/neighbors-29439764-20261011/neighbors.json'))
  assert 'Fewer than two image events' in (q/'stderr.txt').read_text()
  pp=Path('data/pixels/29439764-s0024.fits');pc=read(q/'coverage.json')
  with fits.open(pp) as h:assert h[0].header['TICID']==29439764 and h[0].header['SECTOR']==24
  assert pc['raw_sha256']==sha(pp) and pc['frozen_sha256']==sha(out/'frozen.json') and pc['script_sha256']==sha(q/'audit_coverage.py')
  assert [e['quality_counts'] for e in pc['events']]==[{'4096':3},{'4096':2}] and all(e['inside_quality_zero']==e['outside_quality_zero']==0 for e in pc['events'])
 else:
  assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  assert '404 Client Error' in (q/'stderr.txt').read_text()
  assert len(c['events'])==1 and c['events'][0]['inside_quality_zero']==2
 rows.append({'sector':s,'files_sha256':sha(p/'files.json'),'coverage_sha256':sha(p/'coverage.json'),'raw_status_sha256':sha(p/'status.json'),'processed_error_sha256':sha(q/'stderr.txt')})
p=Path('results/tesscut-29439764-peak1-s24-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'raw_analysis_sha256':sha(p/'analysis.json'),'stack_plot_sha256':sha(p/'difference.png'),'individual_plot_sha256':sha(p/'individual-events.png'),'processed_coverage_sha256':sha(Path('results/spoc-pixels-29439764-peak1-s24-20261011/coverage.json')),'visual_review':'S24stack and both individual maps inspected: event0entirefieldnegative, event1entirefieldpositive, scattered relative structure without isolated source; stack nearlyallnegative. S25oneeventonly; no image claimed.','limits':'Background/quality and sparse coverage concerns, exact cause unresolved. All5processedS24insideexposuresflag4096; noqualityzerocoverage not nondetection. S25exactproduct404 not proof allproducts absent. No gates relaxed or Gaia inference; both fits remain unresolved.'})
print('Image provenance, quality coverage and failures verified.')
