from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text())
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
b=json.loads(Path('results/qlp-faint-midradius-single-review-20261011/241928959-peak0/frozen.json').read_text())['best'];checked=0
for row in r['rows']:
 z=np.load(p/f"w{row['window']}-d{row['duration_factor']}.npz");d=b['duration']*row['duration_factor'];inside=abs(z['phase'])<d/2;outside=(abs(z['phase'])>d)&(abs(z['phase'])<3*d);w=1/z['e']**2
 value=np.sum(z['y'][outside]*w[outside])/sum(w[outside])-np.sum(z['y'][inside]*w[inside])/sum(w[inside]);err=np.sqrt(1/sum(w[inside])+1/sum(w[outside]));m=row['measurement']['total']
 np.testing.assert_allclose([value,err],[m['depth'],m['error']]);assert inside.sum()==m['n']
 for depth in [.001,.01]:
  y=z['y'].copy();y[inside]-=depth
  inj=fixed_measure(z['t'],y,z['e'],b['period'],b['transit_time']+b['period']/2,d)
  np.testing.assert_allclose(inj['total']['depth']-m['depth'],depth,atol=1e-12)
 for raw in row['data']:assert sha(Path(f"data/qlp/241928959-s{raw['sector']:04d}.fits"))==raw['source']['sha256']
 checked+=1
save_json(p/'verification.json',dict(measurements_verified=checked,fixed_window_additive_controls=8,limits='Controls check arithmetic on already flattened data, not detrending completeness or correlated-noise significance.'))
print('Four measurements and eight arithmetic controls passed')
