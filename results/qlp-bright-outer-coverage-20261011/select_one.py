"""Audit all remaining metadata and freeze discovery/holdout choices."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;run=json.loads((out/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0
poolp=Path(run['pool_path']);assert sha(poolp)==run['pool_sha256'];pool=json.loads(poolp.read_text());prior_four={t['tic'] for name in ['selected-four.json','selected-three.json','selected-two.json'] for t in json.loads((out/name).read_text())};remaining=[t for t in pool if t['tic'] not in prior_four];allowed={r['tic'] for r in pool}
queries=json.loads((out/'queries.json').read_text());assert {q['offset'] for q in queries}==set(range(0,len(pool),250))
obs={};sources=[]
for q in queries:
 assert q['status']=='complete'
 p=Path(f"data/qlp-coverage-bright-outer-20261011/chunk-{q['offset']}.json");assert sha(p)==q['evidence']['sha256']
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
  if not all(s+i in sectors for i in range(1)):continue
  held=[h for h in sectors if min(abs(h-(s+i)) for i in range(1))>=8]
  if len(held)>=2:options.append(([s],held))
 if not options:counts['no_single_sector_sectors_and_two_distant_reserved_sectors']+=1;continue
 training,held=options[-1]
 selected.append(dict(target,sectors=sectors,training_sectors=training,heldout_sectors=held,estimate_missing_errors=True,qlp_products={str(s):v[0] for s,v in products.items()}))
prior=set()
for p in [Path('results/selection-small-stars-20261009/eligible.json'),Path('results/selection-late-sectors-20261010/eligible.json'),Path('results/selection-qlp-only-20261010/selected.json'),Path('results/qlp-full-pool-coverage-20261010/selected.json')]:prior.update(t['tic'] for t in json.loads(p.read_text()))
assert not prior&{t['tic'] for t in selected}
save_json(out/'selected-one.json',selected)
save_json(out/'selection-one.json',{'utc':now(),'n_remaining_metadata_targets':len(remaining),'n_with_qlp':len(obs),'n_selected':len(selected),'exclusions':dict(counts),'sources':sources,'selected_sha256':sha(out/'selected-one.json'),'script_sha256':sha(Path(__file__)),'disjoint_from_prior_selections':True,'training_sector_counts':{'-'.join(map(str,sectors)):n for sectors,n in Counter(tuple(t['training_sectors']) for t in selected).items()},'rule':'All remaining untouched pool targets with latest single QLP sector and at least two reserved sectors each >=8 sector numbers away. Bright small stars120<d<=200pc,6<=Tmag<=12,.15<=radius<=.6,Teff<=4200,crowding<=.2 with dated exclusions from selection-bright-outer-small-20261011; metadata coverage complete, no completeness/novelty claim. No new discovery photometry opened before freezing. Shorter discovery baseline is exploratory and may reduce sensitivity; deterministic controls required on this sample. All top-three peaks need review; original quality gates retained. Actual training baseline must be <=120 days. Earlier and/or later reserved epochs allowed.'})
print('remaining',len(remaining),'with_qlp',len(obs),'selected',len(selected),'excluded',dict(counts))
