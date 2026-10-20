from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (24,25):
 raw=Path(f'results/tesscut-390173361-s{s}-20261011');proc=Path(f'results/spoc-pixels-390173361-s{s}-20261011');f=read(raw/'files.json')[0]
 for p,path in [(raw,Path(f['path'])),(proc,Path(f'data/pixels/390173361-s{s:04d}.fits'))]:
  c=read(p/'coverage.json');assert sha(path)==c['raw_sha256'] and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
  if s==25:assert not c['events']
  elif p==raw:assert [e['inside_quality_zero'] for e in c['events']]==[2,2]
  else:assert [e['quality_counts'] for e in c['events']]==[{'4096':2},{'32768':3}]
 assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
 if s==25:
  assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
  tc=read(raw/'time_coverage.json');assert tc['script_sha256']==sha(raw/'time_coverage.py') and tc['raw_sha256']==sha(Path(f['path'])) and tc['frozen_sha256']==sha(out/'frozen.json')
  assert all(r['nearest_exposure_distance_days']>tc['duration']/2 for r in tc['windows'])
 else:
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==sha(Path(f['path']))
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-390173361-20261011/neighbors.json'))
  i=read(raw/'individual-events.json');assert i['script_sha256']==sha(raw/'plot_events.py') and i['plot_sha256']==sha(raw/'individual-events.png')
  for n,h in i['inputs'].items():assert sha(Path(n))==h
 rows.append({'sector':s,'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'visual_review':'S24 stack and both individual maps inspected. Opposite-sign field-wide gradients, no isolated source. S25 has no exposures in predicted windows.','limits':'Sparse coverage/background concerns; no host/Gaia inference. Missing/flagged data not nondetection. Same QLP epochs, not independent recurrence.'})
print('Source and coverage provenance verified.')
