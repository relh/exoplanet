from pathlib import Path
import json,math
from exoplanet.pipeline import sha,save_json
O=Path(__file__).parent;x=json.loads((O/'candidate-geometry.json').read_text());positions={}
for p,h in x['inputs'].items():
 assert sha(Path(p))==h
 for s in json.loads(Path(p).read_text())['sectors']:
  tic=80387959 if '80387959' in s['positions'] else 402358350;positions[(tic,s['sector'])]=s['positions']
for r in x['rows']:
 ps=positions[(r['tic'],r['sector'])];a=ps[str(r['tic'])];b=ps[r['neighbor']];rad=r['radius'];ma={(i,j) for i in range(11) for j in range(11) if math.hypot(i-a[0],j-a[1])<=rad};mb={(i,j) for i in range(11) for j in range(11) if math.hypot(i-b[0],j-b[1])<=rad};assert [len(ma-mb),len(mb-ma)]==r['exclusive_pixels'];assert (ma==mb)==r['identical_masks'];assert len(ma&mb)==r['shared_pixels'];assert bool(ma-mb and mb-ma)==r['contrast_constructible'];assert math.isclose(math.dist(a,b),r['separation_pixels'])
save_json(O/'geometry-verification.json',dict(status='passed',rows=len(x['rows']),method='Independent scalar Euclidean distances and pixel-set intersections using only catalog positions; input hashes.'))
