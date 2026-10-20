"""Complete metadata-only coverage of the remaining untouched TIC pool."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,traceback
from exoplanet.archive import qlp_observations
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=Path('results/selection-qlp-only-20261010/pool.json');pool=json.loads(p.read_text())
prior=json.loads(Path('results/selection-qlp-only-20261010/query-targets.json').read_text());assert pool[:2000]==prior
assert not (out/'run.json').exists()
run={'utc':now(),'status':'running','pool_path':str(p),'pool_sha256':sha(p),'n_pool':len(pool),'already_queried_prefix':2000,'n_new_metadata_targets':len(pool)-2000,'script_sha256':sha(Path(__file__)),'policy':'Metadata only for every remaining target in the original29549-star untouched pool, not a new brightness-ranked subset. No new photometry opened until viable sector selection is frozen. Prior2000-target queries and288-target discovery scope retained separately. Errors remain explicit, not absence of products.'}
save_json(out/'run.json',run)
def query(offset):
 tics=[r['tic'] for r in pool[offset:offset+250]];r={'offset':offset,'n_targets':len(tics),'started_utc':now()}
 try:
  rows,meta=qlp_observations(tics,Path(f'data/qlp-coverage-untouched-20261010/chunk-{offset}.json'))
  r.update(status='complete',n_observations=len(rows),n_targets_with_qlp=len({x['target_name'] for x in rows}),evidence=meta)
 except Exception as exc:r.update(status='error',error=repr(exc),traceback=traceback.format_exc())
 r['finished_utc']=now();save_json(out/f'query-{offset}.json',r);print(offset,r['status'],r.get('n_observations'),r.get('error'),flush=True);return r
records=[]
with ThreadPoolExecutor(max_workers=2) as executor:
 futures=[executor.submit(query,k) for k in range(2000,len(pool),250)]
 for f in as_completed(futures):
  records.append(f.result());save_json(out/'progress.json',{'utc':now(),'completed_chunks':len(records),'total_chunks':len(futures),'errors':sum(r['status']=='error' for r in records)})
save_json(out/'queries.json',sorted(records,key=lambda r:r['offset']));run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in records));save_json(out/'run.json',run)
