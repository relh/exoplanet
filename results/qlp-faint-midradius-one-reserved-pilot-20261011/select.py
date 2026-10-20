"""Metadata-only fresh tier with one distant reserved sector instead of two."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());base=Path('results/qlp-faint-midradius-coverage-20261011');run=read(base/'run.json');pp=Path(run['pool_path']);assert sha(pp)==run['pool_sha256'];pool=read(pp);assert run['status']=='complete' and run['n_errors']==0
exclude=set();prior=[]
for p in sorted(Path('results').glob('*/selected*.json')):
 a=read(p)
 if isinstance(a,list) and all(isinstance(r,dict) and 'tic' in r for r in a):
  exclude.update(int(r['tic']) for r in a);prior.append({'path':str(p),'sha256':sha(p)})
cache=[]
for pat in ['data/qlp/*-s*.fits','data/lightcurves/s*-*.fits']:
 for p in Path('.').glob(pat):
  tic=int(p.stem.split('-s')[0]) if 'qlp/' in str(p) else int(p.stem.split('-')[1]);exclude.add(tic);cache.append({'path':str(p),'tic':tic})
obs={};sources=[];queries=read(base/'queries.json');assert {q['offset'] for q in queries}==set(range(0,len(pool),250))
for q in queries:
 assert q['status']=='complete';p=Path(f"data/qlp-coverage-faint-midradius-20261011/chunk-{q['offset']}.json");assert sha(p)==q['evidence']['sha256'];a=read(p);assert len(a['data'])==a['paging']['rowsFiltered'];sources.append({'path':str(p),'sha256':sha(p)})
 for r in a['data']:obs.setdefault(int(r['target_name']),{}).setdefault(int(r['sequence_number']),[]).append(r)
selected=[];counts=Counter()
for t in pool:
 if t['tic'] in exclude:counts['prior_selection_or_opened']+=1;continue
 products=obs.get(t['tic'],{});sectors=sorted(products)
 if any(len({r['dataURL'] for r in v})!=1 for v in products.values()):counts['ambiguous_products']+=1;continue
 options=[]
 for n in [4,3,2,1]:
  for s in sectors:
   train=list(range(s,s+n));held=[h for h in sectors if min(abs(h-x) for x in train)>=8]
   if all(x in sectors for x in train) and held:options.append((n,s,train,held))
 if not options:counts['no_distant_reserved_epoch']+=1;continue
 _,_,train,held=max(options);selected.append(dict(t,sectors=sectors,training_sectors=train,heldout_sectors=held,estimate_missing_errors=True,qlp_products={str(s):v[0] for s,v in products.items()}))
assert not (out/'selected.json').exists();pilot=selected[:16];assert len(pilot)==16
for t in pilot:
 assert all(not Path(f"data/qlp/{t['tic']}-s{s:04d}.fits").exists() for s in t['sectors'])
save_json(out/'eligible.json',selected);save_json(out/'selected.json',pilot)
save_json(out/'selection.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_path':str(pp),'pool_sha256':sha(pp),'prior_selection_sources':prior,'cache_inventory':cache,'coverage_sources':sources,'excluded_ids':sorted(exclude),'counts':dict(counts),'n_pool':len(pool),'n_eligible':len(selected),'n_pilot':len(pilot),'eligible_sha256':sha(out/'eligible.json'),'selected_sha256':sha(out/'selected.json'),'training_lengths':dict(Counter(len(t['training_sectors']) for t in selected)),'policy':'Preserve original metadata rank and dated catalog exclusions. Fresh targets only, longest available consecutive discovery block up to4 sectors, latest tie, at least1 reserved sector >=8 sector numbers away. First16 frozen before photometry. One-reserved evidence is weaker than two; original search quality gates unchanged. Actual discovery baseline limited120days; no reserved substitution on failure. Local cache absence is not proof of worldwide underexploration or novelty.'});print('eligible',len(selected),'pilot',len(pilot),'counts',dict(counts),'blocks',dict(Counter(len(t['training_sectors']) for t in pilot)))
