"""Freeze QLP discovery/holdout sectors before opening new photometry."""
from pathlib import Path
import json
from collections import Counter
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;targets=json.loads((out/'query-targets.json').read_text());queries=json.loads((out/'queries.json').read_text())
assert len(queries)==8 and all(q['status']=='complete' for q in queries)
obs={};sources=[]
for q in queries:
 p=Path(f"data/qlp-coverage-untouched-20261010/chunk-{q['offset']}.json")
 assert sha(p)==q['evidence']['sha256'];sources.append(q['evidence'])
 payload=json.loads(p.read_text());assert len(payload['data'])==payload['paging']['rowsFiltered']
 for r in payload['data']:
  tic=int(r['target_name']);s=int(r['sequence_number']);obs.setdefault(tic,{}).setdefault(s,[]).append(r)
selected=[];counts=Counter()
for t in targets:
 products=obs.get(t['tic'],{});sectors=sorted(products)
 if any(len({v['dataURL'] for v in values})>1 for values in products.values()):counts['ambiguous_products']+=1;continue
 options=[]
 for s in sectors:
  if s+1 not in sectors:continue
  held=[h for h in sectors if min(abs(h-s),abs(h-s-1))>=8]
  if held:options.append(([s,s+1],held))
 if not options:counts['no_adjacent_pair_and_separate_epoch']+=1;continue
 training,held=options[0]
 selected.append(dict(t,sectors=sectors,training_sectors=training,heldout_sectors=held,qlp_products={str(s):v[0] for s,v in products.items()}))
save_json(out/'selected.json',selected)
save_json(out/'selection.json',{'utc':now(),'n_metadata_targets':len(targets),'n_with_qlp':len(obs),'n_selected':len(selected),'excluded':dict(counts),'metadata_sources':sources,'script_sha256':sha(Path(__file__)),'selection_sha256':sha(out/'selected.json'),'rule':'Earliest adjacent QLP sector pair, with reserved sectors separated by >=8 sector numbers from either training sector. Metadata only before selection; photometry unopened. QLP expands coverage beyond SPOC-defined prior selections; not necessarily stars entirely absent from SPOC.','error_policy':'Published uncertainties only on initial run. Unusable errors explicitly recorded, never treated as a negative detection.'})
print('selected',len(selected),dict(counts),Counter(tuple(t['training_sectors']) for t in selected))
