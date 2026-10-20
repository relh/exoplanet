"""Metadata-only audit for untouched Sector98 targets with reserved epochs."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/qlp-faint-pool-coverage-20261010')
run=json.loads((base/'run.json').read_text());assert run['status']=='complete' and run['n_errors']==0
poolp=Path(run['pool_path']);assert sha(poolp)==run['pool_sha256'];pool=json.loads(poolp.read_text())
priorp=base/'selected-four.json';prior={x['tic'] for x in json.loads(priorp.read_text())}
obs={};sources=[]
for q in json.loads((base/'queries.json').read_text()):
 assert q['status']=='complete';p=Path(f"data/qlp-coverage-faint-20261010/chunk-{q['offset']}.json");assert sha(p)==q['evidence']['sha256'];r=json.loads(p.read_text());assert len(r['data'])==r['paging']['rowsFiltered'];sources.append({'path':str(p),'sha256':sha(p)})
 for row in r['data']:obs.setdefault(int(row['target_name']),{}).setdefault(int(row['sequence_number']),[]).append(row)
selected=[];counts=Counter()
for target in pool:
 tic=target['tic'];products=obs.get(tic,{})
 if tic in prior:counts['prior_four_sector_selection']+=1;continue
 if 98 not in products:counts['no_sector98']+=1;continue
 if any(len({r['dataURL'] for r in rs})!=1 for rs in products.values()):counts['ambiguous_product']+=1;continue
 held=sorted(s for s in products if abs(s-98)>=8)
 if len(held)<2:counts['fewer_than_two_reserved_sectors']+=1;continue
 if list(Path('data/qlp').glob(f'{tic}-s*.fits')) or list(Path('data/lightcurves').glob(f's*-{tic}.fits')):counts['previous_photometry_cache']+=1;continue
 selected.append(dict(target,sectors=sorted(products),training_sectors=[98],heldout_sectors=held,qlp_products={str(s):rs[0] for s,rs in products.items()},estimate_missing_errors=True))
save_json(out/'selected.json',selected)
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_sha256':sha(poolp),'prior_four_sector_sha256':sha(priorp),'n_pool':len(pool),'n_selected':len(selected),'exclusions':dict(counts),'sources':sources,'selected_sha256':sha(out/'selected.json'),'policy':'Metadata-only extension to Sector98. Exclude entire prior1945-star four-sector selection and any cached QLP/SPOC photometry. Require two reserved sectors>=8numbers away. Preserve pool radius/noise ordering and dated catalog exclusions. Availability is not evidence of novelty or underexploration. No photometry opened.'})
print('selected',len(selected),'excluded',dict(counts))
