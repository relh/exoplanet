from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (74,75):
 raw=Path(f'results/tesscut-149919534-s{s}-20261011');proc=Path(f'results/spoc-pixels-149919534-s{s}-20261011');file=read(raw/'files.json')[0];pp=Path(f'data/pixels/149919534-s{s:04d}.fits')
 assert sha(Path(file['path']))==file['sha256']
 with fits.open(pp) as h:assert h[0].header['TICID']==149919534 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(file['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 rc=read(raw/'coverage.json');assert [e['inside_quality_zero'] for e in rc['events']]==([93,0] if s==74 else [93,93])
 assert [e['outside_quality_zero'] for e in rc['events']]==([187,0] if s==74 else [373,373])
 if s==74:
  for p in (raw,proc):assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  assert [e['quality_counts'] for e in c['events']]==[{'4096':93},{'4096':94}]
 else:
  assert [e['inside_quality_zero'] for e in c['events']]==[93,94] and [e['outside_quality_zero'] for e in c['events']]==[353,374]
  a=read(raw/'analysis.json');b=read(proc/'analysis/localization.json');assert a['n_events']==b['n_events']==2
  assert a['fit_sha256']==b['frozen_sha256']==sha(out/'frozen.json') and a['source']['sha256']==file['sha256'] and b['source']['sha256']==sha(pp)
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-149919534-20261011/neighbors.json'))
 rows.append({'sector':s,'raw_file_sha256':file['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
p=Path('results/tesscut-149919534-s75-20261011');i=read(p/'individual-events.json')
for path,h in i['inputs'].items():assert sha(Path(path))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
q=Path('results/spoc-pixels-149919534-s75-20261011');j=read(q/'individual-events.json')
for path,h in j['inputs'].items():assert sha(Path(path))==h
assert j['script_sha256']==sha(q/'plot_events.py') and j['plot_sha256']==sha(q/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'raw_analysis_sha256':sha(p/'analysis.json'),'raw_plot_sha256':sha(p/'difference.png'),'individual_plot_sha256':sha(p/'individual-events.png'),'processed_individual_manifest_sha256':sha(q/'individual-events.json'),'processed_analysis_sha256':sha(q/'analysis/localization.json'),'processed_plot_sha256':sha(Path('results/spoc-pixels-149919534-s75-20261011/analysis/difference.png')),'visual_review':'Raw/processed S75 stacks and both individual images in each processing inspected. Raw positive field-wide background; target-region relative positive features in both events, also seen in processed maps with mixed residuals and gradient. No secure host attribution. S74 has no image under unchanged gate.','limits':'Background/quality concern and tentative target-region residuals need further modeling. All187 processed S74 inside exposures flag4096; raw event0 all94 flag2048. Missing usable coverage is not nondetection. Same photons across processing, not independent confirmation. No Gaia attribution or gates relaxed.'})
print('Source provenance and coverage verified.')
