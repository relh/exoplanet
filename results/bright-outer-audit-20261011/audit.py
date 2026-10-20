"""Reconcile the scoped bright outer-distance pool and all completed searches."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
read=lambda p:json.loads(Path(p).read_text())
out=Path(__file__).parent;coverage=Path('results/qlp-bright-outer-coverage-20261011');poolp=Path('results/selection-bright-outer-small-20261011/pool.json');pool=read(poolp)
seen=set();counts=Counter();batches=[]
for selection,run in [('four','four'),('three','three'),('two','two'),('one','one'),('one-reserved','single-reserved')]:
 sp=coverage/f'selected-{selection}.json';targets=read(sp);ids={r['tic'] for r in targets}
 assert len(ids)==len(targets) and not ids&seen;seen.update(ids)
 folder=Path(f'results/qlp-bright-outer-{run}-pilot-20261011');plan=read(folder/'plan.json');rec=read(folder/'reconciliation.json')
 assert sha(sp)==plan['source_sha256'] and plan['targets']==targets and rec['n_completed']==len(ids)
 for name,digest in rec['terminal_hashes'].items():assert sha(Path(name))==digest
 assert len(rec['inventory'])==len(ids)
 for item in rec['inventory']:
  p=Path(item['path']);assert sha(p)==item['sha256'];r=read(p);assert r['status']=='screened' and r['tic'] in ids
  for ev in r['data']:assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
  assert all(not Path(f"data/qlp/{r['tic']}-s{s:04d}.fits").exists() for s in r['target']['heldout_sectors'])
  counts[r['disposition']]+=1
 assert not rec['followups']
 batches.append({'selection':str(sp),'selection_sha256':sha(sp),'n':len(ids),'reconciliation_sha256':sha(folder/'reconciliation.json')})
rawp=Path('data/qlp-coverage-bright-outer-20261011/chunk-0.json');q=read(coverage/'queries.json');assert len(q)==1 and sha(rawp)==q[0]['evidence']['sha256']
raw=read(rawp);assert len(raw['data'])==raw['paging']['rowsFiltered']
remaining=[]
for target in pool:
 if target['tic'] in seen:continue
 sectors=sorted({int(r['sequence_number']) for r in raw['data'] if int(r['target_name'])==target['tic']})
 assert len(sectors)==1
 assert not Path(f"data/qlp/{target['tic']}-s{sectors[0]:04d}.fits").exists()
 remaining.append({'tic':target['tic'],'sectors':sectors,'reason':'No separate QLP observing epoch in scoped metadata'})
assert len(seen)==13 and len(remaining)==2 and len(pool)==15
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'pool_sha256':sha(poolp),'n_pool':15,'n_selected':13,'n_usable':13,'counts':dict(counts),'batches':batches,'unsearched_single_epoch':remaining,'coverage_sha256':sha(rawp),'interpretation':'Scoped population and artifact accounting, not all-TESS coverage, completeness, novelty or proof of no planets. All reserved epochs remain unopened because no peak qualifies.'})
print('13 usable',dict(counts),'remaining',remaining)
