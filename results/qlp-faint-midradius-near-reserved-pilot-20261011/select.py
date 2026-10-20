from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());audit=Path('results/qlp-faint-midradius-unused-coverage-audit-20261011');a=read(audit/'audit.json');inventory=read(audit/'inventory.json');assert sha(audit/'inventory.json')==a['inventory_sha256'];old=read(Path('results/qlp-faint-midradius-one-reserved-pilot-20261011/selection.json'));poolpath=Path(old['pool_path']);assert sha(poolpath)==old['pool_sha256'];pool=read(poolpath);byid={r['tic']:r for r in pool};obs={}
for src in a['coverage_sources']:
 p=Path(src['path']);assert sha(p)==src['sha256']
 for r in read(p)['data']:obs.setdefault(int(r['target_name']),{}).setdefault(int(r['sequence_number']),[]).append(r)
cache={int(p.stem.split('-s')[0]) for p in Path('data/qlp').glob('*-s*.fits')};targets=[]
for row in inventory:
 if row['category']!='multiple_sectors_without_distant_reserve':continue
 tic=row['tic'];assert tic not in cache;sectors=row['sectors'];products=obs[tic];assert all(len({r['dataURL'] for r in v})==1 for v in products.values())
 options=[]
 for n in range(1,min(4,len(sectors)-1)+1):
  for start in sectors:
   train=list(range(start,start+n));held=[s for s in sectors if s not in train]
   if all(s in sectors for s in train) and held:options.append((n,start,train,held))
 _,_,train,held=max(options)
 held.sort(key=lambda s:(-min(abs(s-t) for t in train),s))
 targets.append(dict(byid[tic],sectors=sectors,training_sectors=train,heldout_sectors=held,estimate_missing_errors=True,qlp_products={str(s):products[s][0] for s in sectors}))
assert len(targets)==139
pilot=targets[:16];assert not (out/'selected.json').exists()
save_json(out/'eligible.json',targets);save_json(out/'selected.json',pilot)
save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inputs':{str(audit/'audit.json'):sha(audit/'audit.json'),str(audit/'inventory.json'):sha(audit/'inventory.json'),str(poolpath):sha(poolpath)},'n_eligible':139,'n_pilot':16,'eligible_sha256':sha(out/'eligible.json'),'selected_sha256':sha(out/'selected.json'),'training_lengths':dict(Counter(len(t['training_sectors']) for t in targets)),'policy':'Preserve audited metadata order. Longest consecutive training block up to4 sectors leaving at least1 distinct reserve; latest start on ties. Reserve ordered by decreasing distance from training, earliest on ties. No8-sector separation requirement. First16 frozen before photometry; controls first3 without replacement. Original scientific gates unchanged. Closely spaced sectors offer weaker replication and may share systematics; not all-sector completeness or novelty.'})
print('pilot',[(t['tic'],t['training_sectors'],t['heldout_sectors']) for t in pilot])
