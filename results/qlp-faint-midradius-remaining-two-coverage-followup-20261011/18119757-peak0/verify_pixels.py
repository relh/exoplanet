from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (79,80):
 raw=Path(f'results/tesscut-18119757-s{s}-20261011');proc=Path(f'results/spoc-pixels-18119757-s{s}-20261011');f=read(raw/'files.json')[0];c=read(raw/'coverage.json')
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
 assert [e['inside_quality_zero'] for e in c['events']]==([56,16] if s==79 else [93,94])
 assert [e['outside_quality_zero'] for e in c['events']]==([186,186] if s==79 else [373,374])
 if s==79:
  assert [e['quality_counts'] for e in c['events']]==[{'0':56,'2048':37},{'0':16,'2048':77}]
  assert read(raw/'status.json')['exit_code']==1 and 'No positive difference flux' in (raw/'stderr.txt').read_text()
 else:
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==f['sha256']
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-18119757-20261011/neighbors.json'))
 assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
 rows.append({'sector':s,'file_sha256':f['sha256'],'coverage_sha256':sha(raw/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt')})
p=Path('results/pixel-events-18119757-20261011');plan=read(p/'plan.json');m=read(p/'manifest.json')
assert plan['script_sha256']==sha(p/'run.py') and plan['module_sha256']==sha(Path('src/exoplanet/pixel_vet.py')) and plan['fit_sha256']==sha(out/'frozen.json')
assert m['plan_sha256']==sha(p/'plan.json') and m['images_sha256']==sha(p/'images.npz') and m['plot_sha256']==sha(p/'individual-events.png')
for r in m['rows']:assert sha(Path(r['input']['path']))==r['input']['sha256'] and r['event_numbers']==([0,1] if r['sector']==79 else [2,3])
h=read(out/'held-coverage-audit.json');assert h['file_sha256']==sha(Path('data/qlp/18119757-s0026.fits')) and h['script_sha256']==sha(out/'audit_held_coverage.py') and h['preprocessing_sha256']==sha(Path('src/exoplanet/search.py'))
assert h['total_exposures']==1148 and h['valid_flux_error_pairs']==406 and h['reproduced_error']=='Fewer than 200 clean cadences'
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'individual_manifest_sha256':sha(p/'manifest.json'),'held_audit_sha256':sha(out/'held-coverage-audit.json'),'s80_analysis_sha256':sha(raw/'analysis.json'),'s80_plot_sha256':sha(raw/'difference.png'),'visual_review':'S80 stack and all four raw individual maps inspected. All individual maps entirely negative across field, S79 stronger gradient; no consistent isolated source. S79 failed moment retained, diagnostic plot intentionally estimates no moment.','limits':'Background/quality concerns, host unresolved; raw flags do not ensure clean background. Exact-product404 is not nondetection. S26 original preprocessing failure reproduced, not a transient download issue. No Gaia attribution or selection gates relaxed.'})
print('Source and held-coverage provenance verified.')
