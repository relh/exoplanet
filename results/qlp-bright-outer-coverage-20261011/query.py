"""Complete metadata-only coverage of the remaining untouched TIC pool."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,traceback
from exoplanet.archive import qlp_observations
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=Path('results/selection-bright-outer-small-20261011/pool.json');pool=json.loads(p.read_text())
assert not (out/'run.json').exists()
run={'utc':now(),'status':'running','pool_path':str(p),'pool_sha256':sha(p),'n_pool':len(pool),'already_queried_prefix':0,'n_new_metadata_targets':len(pool),'script_sha256':sha(Path(__file__)),'policy':'Metadata only for all selected bright outer small stars. No photometry before viable sector selection frozen. Query failures remain errors, not absence of products.'}
save_json(out/'run.json',run)
def query(offset):
 tics=[r['tic'] for r in pool[offset:offset+250]];r={'offset':offset,'n_targets':len(tics),'started_utc':now()}
 try:
  rows,meta=qlp_observations(tics,Path(f'data/qlp-coverage-bright-outer-20261011/chunk-{offset}.json'))
  r.update(status='complete',n_observations=len(rows),n_targets_with_qlp=len({x['target_name'] for x in rows}),evidence=meta)
 except Exception as exc:r.update(status='error',error=repr(exc),traceback=traceback.format_exc())
 r['finished_utc']=now();save_json(out/f'query-{offset}.json',r);print(offset,r['status'],r.get('n_observations'),r.get('error'),flush=True);return r
records=[]
with ThreadPoolExecutor(max_workers=2) as executor:
 futures=[executor.submit(query,k) for k in range(0,len(pool),250)]
 for f in as_completed(futures):
  records.append(f.result());save_json(out/'progress.json',{'utc':now(),'completed_chunks':len(records),'total_chunks':len(futures),'errors':sum(r['status']=='error' for r in records)})
save_json(out/'queries.json',sorted(records,key=lambda r:r['offset']));run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in records));save_json(out/'run.json',run)
