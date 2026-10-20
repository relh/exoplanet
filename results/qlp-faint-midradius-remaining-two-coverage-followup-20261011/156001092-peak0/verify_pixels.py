from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (68,69):
 raw=Path(f'results/tesscut-156001092-s{s}-20261011');proc=Path(f'results/spoc-pixels-156001092-s{s}-20261011');file=read(raw/'files.json')[0];pp=Path(f'data/pixels/156001092-s{s:04d}.fits')
 assert sha(Path(file['path']))==file['sha256']
 req=read(raw/'request.json')['params'];assert req['ra']==8.20533588283614 and req['dec']==-53.0746877757393 and req['sector']==s
 with fits.open(pp) as h:assert h[0].header['TICID']==156001092 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(file['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 rc=read(raw/'coverage.json');assert [e['inside_quality_zero'] for e in rc['events']]==([93,93] if s==68 else [93,94]) and [e['outside_quality_zero'] for e in rc['events']]==([372,372] if s==68 else [373,374])
 a=read(raw/'analysis.json');assert a['n_events']==2 and a['source']['sha256']==file['sha256'] and a['fit_sha256']==sha(out/'frozen.json')
 assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-156001092-20261011/neighbors.json'))
 if s==68:
  assert read(proc/'status.json')['exit_code']==1 and 'Fewer than two image events' in (proc/'stderr.txt').read_text()
  assert [e['quality_counts'] for e in c['events']]==[{'4096':93},{'4096':91,'32768':2}]
  assert [e['outside_quality_zero'] for e in c['events']]==[0,183]
 else:
  b=read(proc/'analysis/localization.json');assert b['n_events']==2 and b['source']['sha256']==sha(pp) and b['frozen_sha256']==sha(out/'frozen.json')
  assert [e['inside_quality_zero'] for e in c['events']]==[93,94] and [e['outside_quality_zero'] for e in c['events']]==[242,289]
 rows.append({'sector':s,'raw_file_sha256':file['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'processed_status_sha256':sha(proc/'status.json')})
for p in (raw,proc):
 m=read(p/'individual-events.json')
 for path,digest in m['inputs'].items():assert sha(Path(path))==digest
 assert m['script_sha256']==sha(p/'plot_events.py') and m['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'raw_individual_manifest_sha256':sha(raw/'individual-events.json'),'processed_individual_manifest_sha256':sha(proc/'individual-events.json'),'processed_analysis_sha256':sha(proc/'analysis/localization.json'),'processed_plot_sha256':sha(proc/'analysis/difference.png'),'visual_review':'Both raw stacks/all4raw individual maps plus S69 processed stack/bothindividual maps inspected. Raw positive field backgrounds/gradients; recurring S69 target-adjacent positive residual with concurrent positive/negative neighboring-star residuals. Tentative source structure, not reliable unique host.','limits':'Background/quality concerns; S68 all186processed inside flagged. No usable data not nondetection. Same photons across reductions not independent confirmation. More background/motion/source modeling needed for S69; no Gaia inference.'})
print('Source provenance and coverage verified.')
