"""Audit all remaining metadata and freeze discovery/holdout choices."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;run=json.loads((out/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0
poolp=Path(run['pool_path']);assert sha(poolp)==run['pool_sha256'];pool=json.loads(poolp.read_text());remaining=pool[2000:];allowed={r['tic'] for r in remaining}
queries=json.loads((out/'queries.json').read_text());assert {q['offset'] for q in queries}==set(range(2000,len(pool),250))
obs={};sources=[]
for q in queries:
 assert q['status']=='complete'
 p=Path(f"data/qlp-coverage-untouched-20261010/chunk-{q['offset']}.json");assert sha(p)==q['evidence']['sha256']
 payload=json.loads(p.read_text());assert len(payload['data'])==payload['paging']['rowsFiltered']
 sources.append({'path':str(p),'sha256':sha(p),'provenance_path':str(out/f"query-{q['offset']}.json")})
 for row in payload['data']:
  tic=int(row['target_name']);assert tic in allowed
  obs.setdefault(tic,{}).setdefault(int(row['sequence_number']),[]).append(row)
selected=[];counts=Counter()
for target in remaining:
 products=obs.get(target['tic'],{});sectors=sorted(products)
 if any(len({x['dataURL'] for x in v})>1 for v in products.values()):counts['ambiguous_products']+=1;continue
 options=[]
 for s in sectors:
  if s+1 not in sectors:continue
  held=[h for h in sectors if min(abs(h-s),abs(h-s-1))>=8]
  if held:options.append(([s,s+1],held))
 if not options:counts['no_adjacent_pair_and_separate_epoch']+=1;continue
 training,held=options[0]
 selected.append(dict(target,sectors=sectors,training_sectors=training,heldout_sectors=held,qlp_products={str(s):v[0] for s,v in products.items()}))
prior=set()
for p in [Path('results/selection-small-stars-20261009/eligible.json'),Path('results/selection-late-sectors-20261010/eligible.json'),Path('results/selection-qlp-only-20261010/selected.json')]:prior.update(t['tic'] for t in json.loads(p.read_text()))
assert not prior&{t['tic'] for t in selected}
save_json(out/'selected.json',selected)
save_json(out/'selection.json',{'utc':now(),'n_remaining_metadata_targets':len(remaining),'n_with_qlp':len(obs),'n_selected':len(selected),'exclusions':dict(counts),'sources':sources,'selected_sha256':sha(out/'selected.json'),'script_sha256':sha(Path(__file__)),'disjoint_from_prior_selections':True,'training_pair_counts':{f'{a}-{b}':n for (a,b),n in Counter(tuple(t['training_sectors']) for t in selected).items()},'rule':'All remaining untouched pool targets with earliest adjacent QLP pair and reserved sectors >=8 sector numbers away. Same physical cuts and dated catalog exclusions as original pool; metadata coverage complete, no completeness/novelty claim. No new photometry opened before freezing.'})
print('remaining',len(remaining),'with_qlp',len(obs),'selected',len(selected),'excluded',dict(counts))
