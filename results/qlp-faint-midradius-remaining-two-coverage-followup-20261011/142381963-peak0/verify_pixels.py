from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (75,76):
 raw=Path(f'results/tesscut-142381963-s{s}-20261011');proc=Path(f'results/spoc-pixels-142381963-s{s}-20261011');file=read(raw/'files.json')[0];pp=Path(f'data/pixels/142381963-s{s:04d}.fits')
 assert sha(Path(file['path']))==file['sha256']
 with fits.open(pp) as h:assert h[0].header['TICID']==142381963 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(file['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 if s==75:
  for p in (raw,proc):assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  assert [e['quality_counts'] for e in c['events']]==[{'4096':46},{'4096':45}]
 else:
  a=read(raw/'analysis.json');b=read(proc/'analysis/localization.json');assert a['n_events']==b['n_events']==3
  assert a['fit_sha256']==b['frozen_sha256']==sha(out/'frozen.json') and a['source']['sha256']==file['sha256'] and b['source']['sha256']==sha(pp)
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-142381963-20261011/neighbors.json'))
 rows.append({'sector':s,'raw_file_sha256':file['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
p=Path('results/tesscut-142381963-s76-20261011');i=read(p/'individual-events.json')
for path,h in i['inputs'].items():assert sha(Path(path))==h
assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'raw_analysis_sha256':sha(p/'analysis.json'),'raw_plot_sha256':sha(p/'difference.png'),'individual_plot_sha256':sha(p/'individual-events.png'),'processed_plot_sha256':sha(Path('results/spoc-pixels-142381963-s76-20261011/analysis/difference.png')),'visual_review':'Raw/processedS76stacks and3rawindividuals inspected. Event2negativefield, events3/4mixed target-adjacent residuals; processed weakmixed residuals formalmax2.025, no consistently isolated source. S75noimageunderunchangedgate.','limits':'Background/quality concern, exact host/cause unresolved. All91processedS75insidepointsflag4096; rawevent0all46flag2048. Missing usablecoverage not nondetection. No Gaia inference or gates relaxed.'})
print('Source provenance and coverage verified.')
