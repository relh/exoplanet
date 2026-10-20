from pathlib import Path
import json,math
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;d=json.loads((out/'results.json').read_text());assert sha(out/'run.py')==d['script_sha256']
for p,h in d['inputs'].items():assert sha(Path(p))==h
n=0
for target in d['rows']:
 for r in target['neighbors']:
  ratio=10**((target['target_Tmag']-r['Tmag'])/2.5);assert math.isclose(ratio,r['flux_ratio_equal_throughput'],rel_tol=1e-12)
  assert math.isclose(r['required_eclipse_fraction']*ratio/(1+ratio),target['depth'],rel_tol=1e-12)
  throughput=r['minimum_neighbor_to_target_throughput_ratio_for_total_eclipse'];assert math.isclose(throughput*ratio/(1+throughput*ratio),target['depth'],rel_tol=1e-12)
  assert r['viable_under_equal_throughput_two_star_assumption']==(r['required_eclipse_fraction']<=1);n+=1
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'n_neighbors':n,'status':'All input hashes and dilution/throughput inversion identities checked. Assumptions unmeasured; no actual source exclusion.'});print(n)
