from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (79,80):
 raw=Path(f'results/tesscut-9823113-peak1-s{s}-20261011');proc=Path(f'results/spoc-pixels-9823113-s{s}-20261011');f=read(raw/'files.json')[0];c=read(raw/'coverage.json')
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(raw/'audit_coverage.py')
 assert [e['inside_quality_zero'] for e in c['events']]==([0,0] if s==79 else [58,58])
 assert [e['outside_quality_zero'] for e in c['events']]==([0,115] if s==79 else [229,230])
 if s==79:
  assert [e['quality_counts'] for e in c['events']]==[{'2048':57},{'2048':57}]
  assert read(raw/'status.json')['exit_code']==1 and 'Fewer than two image events' in (raw/'stderr.txt').read_text()
 else:
  a=read(raw/'analysis.json');assert a['n_events']==2 and a['fit_sha256']==sha(out/'frozen.json') and a['source']['sha256']==f['sha256']
  assert a['script_sha256']==sha(raw/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-9823113-20261011/neighbors.json'))
 assert read(proc/'status.json')['exit_code']==1 and '404 Client Error' in (proc/'stderr.txt').read_text()
 rows.append({'sector':s,'file_sha256':f['sha256'],'coverage_sha256':sha(raw/'coverage.json'),'raw_status_sha256':sha(raw/'status.json'),'processed_error_sha256':sha(proc/'stderr.txt')})
p=Path('results/tesscut-9823113-peak1-s80-20261011');m=read(p/'individual-events.json')
for path,digest in m['inputs'].items():assert sha(Path(path))==digest
assert m['script_sha256']==sha(p/'plot_events.py') and m['plot_sha256']==sha(p/'individual-events.png')
h=read(out.parent/'9823113-peak0/held-coverage-audit.json');assert h['file_sha256']==sha(Path('data/qlp/9823113-s0026.fits')) and h['script_sha256']==sha(out.parent/'9823113-peak0/audit_held_coverage.py') and h['preprocessing_sha256']==sha(Path('src/exoplanet/search.py'))
assert h['total_exposures']==1148 and h['valid_flux_error_pairs']==406 and h['reproduced_error']=='Fewer than 200 clean cadences'
w=read(out/'window-overlap.json');assert w['script_sha256']==sha(out/'compare_windows.py')
assert w['rows'][1]['common_inside_count']==58 and w['rows'][1]['quality_zero_inside_counts']==[116,116]
assert w['frozen_sha256']==[sha(out.parent/f'9823113-peak{k}/frozen.json') for k in (0,1)]
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'window_overlap_sha256':sha(out/'window-overlap.json'),'individual_manifest_sha256':sha(p/'individual-events.json'),'held_audit_sha256':sha(out.parent/'9823113-peak0/held-coverage-audit.json'),'s80_analysis_sha256':sha(raw/'analysis.json'),'s80_plot_sha256':sha(raw/'difference.png'),'visual_review':'S80 stack and both individual raw maps inspected. Both events positive across field, event2 strong column pattern and event3 different relative target/neighbor structure. No consistent isolated source. S79 all inside exposures flagged; no source image.','limits':'Background/quality concerns, host unresolved; all114rawS79insideflag2048; raw flags do not ensure clean background. Exact-product404 is not nondetection. S26 original preprocessing failure reproduced, not a transient download issue. No Gaia attribution or selection gates relaxed.'})
print('Source and held-coverage provenance verified.')
