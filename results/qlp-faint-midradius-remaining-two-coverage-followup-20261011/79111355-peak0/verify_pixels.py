from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
rows=[]
for sector in (94,95):
 raw=Path(f'results/tesscut-79111355-s{sector}-20261011');proc=Path(f'results/spoc-pixels-79111355-s{sector}-20261011')
 files=read(raw/'files.json');assert len(files)==1
 f=files[0];path=Path(f['path']);assert sha(path)==f['sha256']
 with fits.open(path) as h:assert h[0].header['SECTOR']==sector and h[1].header['TIMESYS']=='TDB' and h[1].header['BJDREFI']==2457000
 c=read(raw/'coverage.json');assert c['raw_sha256']==f['sha256'] and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
 assert len(c['events'])==1
 e=c['events'][0];assert e['event']==sector-94 and e['inside']==93
 assert e['quality_counts']==({'0':32,'128':61} if sector==94 else {'0':93})
 assert e['inside_quality_zero']==(32 if sector==94 else 93) and e['outside_quality_zero']==(313 if sector==94 else 373)
 assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
 assert read(raw/'status.json')['script_sha256']==sha(raw/'analyze.py')
 assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
 assert read(proc/'plan.json')['script_sha256']==sha(proc/'run.py')
 rows.append({'sector':sector,'pixel_sha256':sha(path),'coverage_sha256':sha(raw/'coverage.json'),'raw_failure_sha256':sha(raw/'stderr.txt'),'processed_failure_sha256':sha(proc/'stderr.txt'),'processed_plan_sha256':sha(proc/'plan.json')})
n=Path('results/neighbors-79111355-20261011');assert len(read(n/'neighbors.json'))==62
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'neighbors_sha256':sha(n/'neighbors.json'),'findings':'One raw event per sector; unchanged two-event gate fails in both. Requested processed products return HTTP404. No source image produced or visually reviewed.','limits':'Coverage/product availability is not nondetection. Host remains unresolved. Individual-event or aligned cross-sector modeling is still possible; no gates relaxed or Gaia attribution.'})
print('Coverage, input provenance and retained failures verified.')
