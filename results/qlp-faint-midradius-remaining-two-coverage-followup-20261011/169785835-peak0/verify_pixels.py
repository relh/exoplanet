from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[]
for s in (99,100):
 p=Path(f'results/tesscut-169785835-s{s}-20261011');c=read(p/'coverage.json');f=read(p/'files.json')[0]
 assert sha(Path(f['path']))==f['sha256']==c['raw_sha256']
 assert c['frozen_sha256']==sha(out/'frozen.json') and c['script_sha256']==sha(p/'audit_coverage.py')
 if s==99:
  assert not c['events'] and read(p/'status.json')['exit_code']==1 and 'Fewer than two' in (p/'stderr.txt').read_text()
  tc=read(p/'time_coverage.json');assert tc['script_sha256']==sha(p/'time_coverage.py') and tc['raw_sha256']==c['raw_sha256'] and tc['frozen_sha256']==c['frozen_sha256']
  assert all(r['nearest_exposure_distance_days']>tc['duration']/2 for r in tc['windows'])
 else:
  a=read(p/'analysis.json');assert a['source']['sha256']==c['raw_sha256'] and a['fit_sha256']==c['frozen_sha256']
  assert a['n_events']==2 and a['script_sha256']==sha(p/'analyze.py') and a['neighbor_sha256']==sha(Path('results/neighbors-169785835-20261011/neighbors.json'))
  assert all(e['inside']==e['inside_quality_zero'] for e in c['events'])
  i=read(p/'individual-events.json')
  for n,h in i['inputs'].items():assert sha(Path(n))==h
  assert i['script_sha256']==sha(p/'plot_events.py') and i['plot_sha256']==sha(p/'individual-events.png')
 q=Path(f'results/spoc-pixels-169785835-s{s}-20261011');assert read(q/'status.json')['exit_code']==1 and '404 Client Error' in (q/'stderr.txt').read_text()
 rows.append({'sector':s,'coverage_sha256':sha(p/'coverage.json'),'processed_error_sha256':sha(q/'stderr.txt')})
g=Path('results/gaia-169785835-neighbors-20261011');plan=read(g/'plan.json');assert plan['script_sha256']==sha(g/'query.py') and plan['neighbors_sha256']==sha(Path('results/neighbors-169785835-20261011/neighbors.json'))
assert read(g/'results.json')['status']=='complete'
for table in ('dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary'):
 src=read(g/f'{table}-source.json');assert sha(Path(f'data/catalogs/gaia-169785835-neighbors-{table}-20261011.csv'))==src['sha256']
save_json(out/'source_review.json',{'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(out/'frozen.json'),'rows':rows,'visual_review':'S100 stack and both individual maps inspected: recurring compact off-target feature near TIC169785532, with fainter unresolved neighbors. S99 predicted window falls in a gap.','limits':'Contamination favored over target-host transit; unique variable unresolved. Same photons as QLP. Moment and formal errors not calibrated PRF confidence. Gaia absence is not variability exclusion. Exact processed-product404 and raw coverage gap are not nondetections.','gaia_results_sha256':sha(g/'results.json')})
print('Source provenance, coverage, failures and catalog downloads verified.')
