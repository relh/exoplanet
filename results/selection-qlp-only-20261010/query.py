"""Query metadata in bounded chunks; preserve errors as errors, not nonmatches."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,traceback
from exoplanet.archive import qlp_observations
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=out/'query-targets.json';targets=json.loads(p.read_text())
def run(offset):
 tics=[r['tic'] for r in targets[offset:offset+250]];rec={'offset':offset,'n_targets':len(tics),'started_utc':now(),'input_sha256':sha(p)}
 try:
  rows,evidence=qlp_observations(tics,Path(f'data/qlp-coverage-untouched-20261010/chunk-{offset}.json'))
  rec.update(status='complete',n_observations=len(rows),n_targets_with_qlp=len({r['target_name'] for r in rows}),evidence=evidence)
 except Exception as exc:rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
 rec['finished_utc']=now();save_json(out/f'query-{offset}.json',rec);print(offset,rec['status'],rec.get('n_observations'),rec.get('error'),flush=True)
 return rec
with ThreadPoolExecutor(max_workers=2) as pool:records=list(pool.map(run,range(0,len(targets),250)))
save_json(out/'queries.json',records)
