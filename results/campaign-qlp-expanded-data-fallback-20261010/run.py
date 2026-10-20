"""Frozen data-availability fallbacks; preserve every original failure."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json,shutil
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import process_target,load_training,SETTINGS
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent
assert not (out/'run.json').exists()
items=[]
for tic,collection,sectors in [(101722368,'SPOC',[25,26]),(183597632,'QLP',[29]),(350348591,'QLP',[46]),(357307559,'QLP',[46])]:
 p=Path(f'results/campaign-qlp-expanded-20261010/targets/{tic}.json');d=json.loads(p.read_text());t=dict(d['target']);t['training_sectors']=sectors
 items.append({'target':t,'collection':collection,'original_sha256':sha(p),'original_training_sectors':d['target']['training_sectors']})
run={'utc':now(),'status':'running','n_selected':len(items),'items':items,'script_sha256':sha(Path(__file__)),'settings':SETTINGS,'policy':'Data-driven fallback frozen before loading replacement photometry. One SPOC reduction of same discovery epochs; three use only the surviving preassigned discovery sector. Original reserved sectors remain unopened. Single-sector searches have smaller period ceiling min(20,baseline/2.5), not equivalent coverage. Published errors only. Original failures preserved.'}
(out/'targets').mkdir();(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
run['source_sha256']={p.name:sha(p) for p in (out/'source').iterdir()};save_json(out/'run.json',run)
def f(item):
 loader=partial(load_training,bin_minutes=10) if item['collection']=='SPOC' else load_qlp
 return process_target(item['target'],Path('data'),out,loader=loader,max_baseline=120)
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(f,items))
review=[{'tic':r['tic'],'peak_index':i,'best':p['best'],'flags':p['flags']} for r in rows for i,p in enumerate(r.get('screened_peaks',[])) if set(p['flags'])<={'crowding_or_missing_crowding'}]
save_json(out/'review.json',review);run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in rows));save_json(out/'run.json',run)
print('terminal',run['n_errors'],'errors',review,flush=True)
