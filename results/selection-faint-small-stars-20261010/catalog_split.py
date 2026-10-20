"""Same physical scope, four distance partitions after broad-query timeout."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,copy,traceback
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=json.loads((out/'request.json').read_text())['request'];bounds=[(0,30),(30,60),(60,90),(90,120)]
assert not (out/'split-run.json').exists()
run={'utc':now(),'status':'running','script_sha256':sha(Path(__file__)),'base_request_sha256':sha(out/'request.json'),'bounds':bounds,'policy':'Same cuts split only by distance for query performance. Inclusive endpoints deduplicated with row-consistency check. Every partition must be COMPLETE with exact server row count before pool preparation. No timeout-as-empty results.'};save_json(out/'split-run.json',run)
def work(pair):
 lo,hi=pair;req=copy.deepcopy(base);req['params']['filters'][2]['values']=[{'min':lo,'max':hi}]
 rec={'distance_min':lo,'distance_max':hi,'utc':now()}
 try:
  rows,meta=mast_query(req,Path(f'data/targeting/tic-faint-small-d{lo}-{hi}-20261010.json'));rec.update(status='complete',n_rows=len(rows),source=meta);return rec,rows
 except Exception as exc:rec.update(status='error',error=repr(exc),traceback=traceback.format_exc());return rec,[]
records=[];allrows={};duplicates=0
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(work,p) for p in bounds]
 for future in as_completed(futures):
  rec,rows=future.result();records.append(rec);save_json(out/f"distance-{rec['distance_min']}-{rec['distance_max']}.json",rec)
  for row in rows:
   tic=int(row['ID'])
   if tic in allrows:assert row==allrows[tic];duplicates+=1
   allrows[tic]=row
  save_json(out/'split-progress.json',records);print(rec['distance_min'],rec['distance_max'],rec['status'],rec.get('n_rows'),flush=True)
run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in records),n_rows=len(allrows),duplicates_at_boundaries=duplicates);save_json(out/'split-run.json',run)
if run['n_errors']==0:
 save_json(out/'catalog-rows.json',[allrows[k] for k in sorted(allrows)]);save_json(out/'catalog-sources.json',records)
else:raise RuntimeError('Incomplete partition queries; do not prepare target pool')
