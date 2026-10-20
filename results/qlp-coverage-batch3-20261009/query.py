import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from exoplanet.archive import qlp_observations
from exoplanet.pipeline import save_json,sha,now
out=Path('results/qlp-coverage-batch3-20261009');parent=Path('results/campaign-small-stars-batch3-20261009/run.json');tics=json.loads(parent.read_text())['target_tics']
meta={'status':'running','started_utc':now(),'target_tics':tics,'parent_sha256':sha(parent),'script_sha256':sha(out/'query.py'),'chunk_size':250,'chunks':[],'previous_attempt':{'status':'failed','error':'ReadTimeout after 180 seconds for one 1000-target request','terminal_session':57161}}
save_json(out/'run.json',meta);rows=[]
def get_chunk(i):
 subset=tics[i:i+250]
 try:
  data,evidence=qlp_observations(subset,Path(f'data/targeting/qlp-batch3-chunk-{i}.json'))
  return data,{'offset':i,'n_targets':len(subset),'status':'complete','source':evidence,'n_observations':len(data)}
 except Exception as exc:return [],{'offset':i,'n_targets':len(subset),'status':'error','error':f'{type(exc).__name__}: {exc}'}
with ThreadPoolExecutor(2) as pool:
 for future in as_completed([pool.submit(get_chunk,i) for i in range(0,len(tics),250)]):
  data,evidence=future.result();rows.extend(data);meta['chunks'].append(evidence);save_json(out/'run.json',meta)
  print(evidence['offset'],evidence['status'],len(data),flush=True)
meta.update(status='complete' if all(c['status']=='complete' for c in meta['chunks']) else 'incomplete',finished_utc=now(),n_observations=len(rows))
save_json(out/'observations.json',rows);save_json(out/'newer-sectors.json',[r for r in rows if r['sequence_number']>85]);save_json(out/'run.json',meta)
