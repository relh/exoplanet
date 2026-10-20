from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
read=lambda p:json.loads(p.read_text());root=Path(__file__).parent.parent
for peak in (0,1):
 out=root/f'389659430-peak{peak}';rows=[]
 for s in (27,28):
  suffix='-peak1' if peak==1 and s==27 else '';raw=Path(f'results/tesscut-389659430-s{s}{suffix}-20261011');proc=Path(f'results/spoc-pixels-389659430-s{s}{suffix}-20261011');fp=out/'frozen.json';f=read(raw/'files.json')[0];pp=Path(f'data/pixels/389659430-s{s:04d}.fits')
  assert sha(Path(f['path']))==f['sha256']
  with fits.open(pp) as h:assert h[0].header['TICID']==389659430 and h[0].header['SECTOR']==s
  cn='coverage-peak1.json' if peak==1 and s==28 else 'coverage.json';sn='audit_peak1.py' if peak==1 and s==28 else 'audit_coverage.py'
  for p,path in ((raw,Path(f['path'])),(proc,pp)):
   c=read(p/cn);assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(fp) and c['script_sha256']==sha(p/sn)
  if s==27:
   a=read(raw/'analysis.json');b=read(proc/'analysis/localization.json');assert a['fit_sha256']==b['frozen_sha256']==sha(fp) and b['source']['sha256']==sha(pp) and a['n_events']==b['n_events']==2
   assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-389659430-20261011/neighbors.json'))
  elif peak==0:
   assert c['events']==[] and read(raw/cn)['events']==[]
   for p in (raw,proc):assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  else:assert c['events'][0]['quality_counts']=={'4096':4} and c['events'][0]['outside_quality_zero']==0
  rows.append({'sector':s,'raw_coverage_sha256':sha(raw/cn),'processed_coverage_sha256':sha(proc/cn),'raw_sha256':f['sha256'],'processed_sha256':sha(pp)})
 save_json(out/'source_review.json',{'verifier':str(Path(__file__)),'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'All four S27raw/processed plots across two fits inspected. Weak mixed scattered structure, no reliable isolated source. Peak0formalmaxraw.82processed2.49; peak1raw2.73processed1.89,uncalibrated.','limits':'Sparseevents and weak source evidence. Peak0S28noinwindowexposures;peak1S28fourprocessedinsideflag4096andzeroq0baseline. Missingcleancoverage not nondetection; noquality/eventgatechanges or Gaia attribution. Same photons across reductions.'})
print('Both fit image provenance and coverage verified.')
