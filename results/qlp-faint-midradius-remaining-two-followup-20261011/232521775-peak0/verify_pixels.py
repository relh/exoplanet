from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (74,75):
 raw=Path(f'results/tesscut-232521775-s{s}-20261011');proc=Path(f'results/spoc-pixels-232521775-s{s}-20261011');f=read(raw/'files.json')[0];assert sha(Path(f['path']))==f['sha256']
 pp=Path(f'data/pixels/232521775-s{s:04d}.fits')
 with fits.open(pp) as h:assert h[0].header['TICID']==232521775 and h[0].header['SECTOR']==s
 c=read(proc/'coverage.json');assert c['raw_sha256']==sha(pp) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(proc/'audit_coverage.py')
 if s==74:
  a=read(raw/'analysis.json');b=read(proc/'analysis/localization.json')
  assert a['fit_sha256']==b['frozen_sha256']==sha(out/'frozen.json') and b['source']['sha256']==sha(pp)
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-232521775-20261011/neighbors.json'))
  assert a['n_events']==b['n_events']==2
 else:
  for p in (raw,proc):assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  a=read(raw/'coverage.json');assert a['raw_sha256']==f['sha256'] and a['frozen_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'audit_coverage.py')
  for v in (a,c):assert [e['inside_quality_zero'] for e in v['events']]==[78,0]
 rows.append({'sector':s,'raw_files_sha256':sha(raw/'files.json'),'processed_raw_sha256':sha(pp),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'S74raw and processed plots inspected. Rawfieldwidepositivebackground invalidmoment; processedmixedpositive/negative target-region structure, no clean isolated source. S75both fail unchanged minimum-two-event requirement.','limits':'Background/source-systematics concern, exact cause and host unresolved. Formal significance/moments not calibrated confidence. S75event2 remains accepted; event3 onlythree flagged exposures, not nondetection. No Gaia inference from unreliable moments; same photons across reductions.'})
print('Raw/processed identities, event coverage and evidence verified.')
