from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (80,81):
 p=Path(f'results/tesscut-358699700-s{s}-20261011');files=read(p/'files.json');assert len(files)==1 and sha(Path(files[0]['path']))==files[0]['sha256']
 c=read(p/'coverage.json');assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 q=Path(f'results/spoc-pixels-358699700-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 if s==80:
  assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  c=read(p/'coverage.json');assert c['raw_sha256']==files[0]['sha256'] and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
  assert len(c['events'])==1 and c['events'][0]['inside_quality_zero']==32 and c['events'][0]['outside_quality_zero']==127
 else:
  a=read(p/'analysis.json');assert a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(p/'analyze.py') and a['event_numbers']==[1,2]
  assert a['neighbor_sha256']==sha(Path('results/neighbors-358699700-20261011/neighbors.json'))
  i=read(p/'individual-events.json')
  for n,h in i['inputs'].items():assert sha(Path(n))==h
  assert i['plot_sha256']==sha(p/'individual-events.png') and i['script_sha256']==sha(p/'plot_events.py')
 rows.append({'sector':s,'files_sha256':sha(p/'files.json'),'status_sha256':sha(p/'status.json'),'processed_error_sha256':sha(q/'stderr.txt')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'sector81_analysis_sha256':sha(p/'analysis.json'),'individual_plot_sha256':sha(p/'individual-events.png'),'visual_review':'S81stack and both individual images inspected: compact positive feature consistently displaced from target near358699657 and faint blends358699670/1814674531; targetoffset3.078pixels nearest358699657 .197pixels. Other background changes present. S80hasoneeventonly, no image under unchanged two-event gate.','limits':'Likely neighboring-source contamination, exact variable and period unresolved. No calibrated PRF confidence. Alternatepeak0 remains untested. Processed exact-product404 not nondetection; same epochs as QLP.'})
print('Source provenance and minimum-event coverage verified.')
