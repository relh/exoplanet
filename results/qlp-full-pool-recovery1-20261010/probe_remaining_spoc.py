"""Check the second assigned SPOC sector when the first epoch was absent."""
from pathlib import Path
from functools import partial
import json
from exoplanet.campaign import process_target,load_training
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;run=json.loads((out/'run.json').read_text());records=[]
for row in json.loads((out/'progress.json').read_text()):
 if row['resolved']:continue
 t=next(r['target'] for r in run['items'] if r['target']['tic']==row['tic']);t=dict(t,training_sectors=t['training_sectors'][1:]);dest=out/str(t['tic'])/'spoc-second'
 (dest/'targets').mkdir(parents=True,exist_ok=False)
 save_json(dest/'plan.json',{'utc':now(),'target':t,'script_sha256':sha(Path(__file__)),'policy':'Second assigned training epoch only, because combined SPOC loader failed at first epoch404. No reserved epochs.'})
 d=process_target(t,Path('data'),dest,loader=partial(load_training,bin_minutes=10),max_baseline=120)
 records.append({'tic':t['tic'],'status':d['status'],'path':str(dest/'targets'/f'{t["tic"]}.json'),'error':d.get('error')})
save_json(out/'spoc-second-results.json',records)
