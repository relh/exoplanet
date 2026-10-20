from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[];counts=[]
for s in (73,74):
 raw=Path(f'results/tesscut-160147376-s{s}-20261011');proc=Path(f'results/spoc-pixels-160147376-s{s}-20261011');a=read(raw/'analysis.json');pp=Path(f'data/pixels/160147376-s{s:04d}.fits')
 assert sha(Path(a['source']['path']))==a['source']['sha256'] and a['fit_sha256']==sha(out/'frozen.json') and a['script_sha256']==sha(raw/'analyze.py')
 assert a['neighbor_sha256']==sha(Path('results/neighbors-160147376-20261011/neighbors.json')) and a['n_events']==2
 with fits.open(pp) as h:assert h[0].header['TICID']==160147376 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(a['source']['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
 counts.extend(c['events'])
 rows.append({'sector':s,'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'processed_raw_sha256':sha(pp),'processed_status_sha256':sha(proc/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt')})
assert [e['inside_quality_zero'] for e in counts]==[20,0,0,0]
assert [e['quality_counts'] for e in counts]==[{'0':20},{'4096':20},{'4096':21},{'4096':21}]
p=Path('results/tesscut-160147376-s74-20261011');i=read(p/'individual-events.json')
for n,h in i['inputs'].items():assert sha(Path(n))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'individual_plot_sha256':sha(p/'individual-events.png'),'processed_events':counts,'visual_review':'Both raw stacked plots and four individual images inspected: all positive across the field, with changing structure and relative target features; no consistently isolated source. Moments cannot establish host.','limits':'Background/quality concern, exact cause unresolved. Three processed windows have all62exposures flagged4096; remaining window20qualityzero exposures. Missing qualityzero coverage not nondetection. No gates relaxed or Gaia attribution. Competing peak0 not checked by these frozen-fit images.'})
print('Verified raw provenance and processed event coverage: 20 accepted, 62 flagged exposures.')
