from pathlib import Path
import json
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (23,24):
 raw=Path(f'results/tesscut-9038963-peak1-s{s}-20261011');proc=Path(f'results/spoc-pixels-9038963-peak1-s{s}-20261011');file=read(raw/'files.json')[0];pp=Path(f'data/pixels/9038963-s{s:04d}.fits')
 assert sha(Path(file['path']))==file['sha256']
 req=read(Path(f'results/tesscut-9038963-s{s}-20261011/request.json'))['params'];assert req['ra']==222.105939873631 and req['dec']==29.9979955655275 and req['sector']==s
 with fits.open(pp) as h:assert h[0].header['TICID']==9038963 and h[0].header['SECTOR']==s
 for p,path in ((raw,Path(file['path'])),(proc,pp)):
  c=read(p/'coverage.json');assert c['raw_sha256']==sha(path) and c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 rc=read(raw/'coverage.json');assert [e['inside_quality_zero'] for e in rc['events']]==([2] if s==23 else [3,3]) and all(e['outside_quality_zero']==9 for e in rc['events'])
 if s==23:
  for p in (raw,proc):assert read(p/'status.json')['exit_code']==1 and 'Fewer than two image events' in (p/'stderr.txt').read_text()
  assert c['events'][0]['quality_counts']=={'4096':2} and c['events'][0]['outside_quality_zero']==0
 else:
  assert [e['inside_quality_zero'] for e in c['events']]==[2,2] and all(e['outside_quality_zero']==9 for e in c['events'])
  a=read(raw/'analysis.json');b=read(proc/'analysis/localization.json');assert a['n_events']==b['n_events']==2
  assert a['fit_sha256']==b['frozen_sha256']==sha(out/'frozen.json') and a['source']['sha256']==file['sha256'] and b['source']['sha256']==sha(pp)
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-9038963-20261011/neighbors.json'))
 rows.append({'sector':s,'raw_file_sha256':file['sha256'],'processed_file_sha256':sha(pp),'raw_coverage_sha256':sha(raw/'coverage.json'),'processed_coverage_sha256':sha(proc/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_status_sha256':sha(proc/'status.json')})
p=Path('results/pixel-events-9038963-peak1-20261011');plan=read(p/'plan.json');m=read(p/'manifest.json')
assert plan['script_sha256']==sha(p/'run.py') and plan['module_sha256']==sha(Path('src/exoplanet/pixel_vet.py')) and plan['fit_sha256']==sha(out/'frozen.json')
assert m['plan_sha256']==sha(p/'plan.json') and m['images_sha256']==sha(p/'images.npz') and m['plot_sha256']==sha(p/'individual-events.png')
for r in m['rows']:assert sha(Path(r['input']['path']))==r['input']['sha256'] and r['event_numbers']==([0] if r['sector']==23 else [1,2])
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'individual_manifest_sha256':sha(p/'manifest.json'),'raw_analysis_sha256':sha(raw/'analysis.json'),'raw_plot_sha256':sha(raw/'difference.png'),'processed_analysis_sha256':sha(proc/'analysis/localization.json'),'processed_plot_sha256':sha(proc/'analysis/difference.png'),'visual_review':'Raw/processed S24 stacks and all three individual raw maps inspected. All raw maps negative across field; processed weak mixed residuals, no isolated source.','limits':'Background/quality and sparse exposure concerns; S23 processed window fully4096flagged. No usable coverage not nondetection. Corrected downloads reused; original erroneous requests excluded. Two fits are alternative hypotheses, not two planets. No Gaia inference or gate changes.'})
print('Source provenance and sparse coverage verified.')
