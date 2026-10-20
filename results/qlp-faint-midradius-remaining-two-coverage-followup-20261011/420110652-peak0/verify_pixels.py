from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (73,74):
 raw=Path(f'results/tesscut-420110652-s{s}-20261011');proc=Path(f'results/spoc-pixels-420110652-s{s}-20261011');f=read(raw/'files.json')[0];pp=Path(f'data/pixels/420110652-s{s:04d}.fits');assert sha(Path(f['path']))==f['sha256']
 with fits.open(pp) as h:assert h[0].header['TICID']==420110652 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(f['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
 if s==73:
  assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
  assert len(c['events'])==1 and c['events'][0]['inside_quality_zero']==93
 else:
  assert [v['quality_counts'] for v in c['events']]==[{'4096':93},{'4096':93}]
  a=read(raw/'analysis.json');assert a['source']['sha256']==f['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['n_events']==2 and a['script_sha256']==sha(raw/'analyze.py')
  assert a['neighbor_sha256']==sha(Path('results/neighbors-420110652-20261011/neighbors.json'))
 rows.append({'sector':s,'raw_file_sha256':f['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'analysis_sha256':sha(raw/'analysis.json'),'plot_sha256':sha(raw/'difference.png'),'visual_review':'RawS74stack inspected, entirely negative across field, target/neighbor negative structure; moment not valid host. S73noimageunderunchangedgate.','limits':'Background/quality and sparse coverage concerns. All186processedS74insidepoints4096flagged; noqualityzerodata not nondetection. Exact host/cause unresolved, no Gaia inference. IndividualrawS74images not reviewed here; competingpeak1stillopen.'})
print('Source provenance and flagged coverage verified.')
