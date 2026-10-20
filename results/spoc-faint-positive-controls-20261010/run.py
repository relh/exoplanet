"""SPOC reductions of exactly the QLP control epochs, with failures retained."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
from exoplanet.campaign import process_target,load_training
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=Path('results/qlp-faint-positive-controls-20261010/search-plan.json');plan=json.loads(p.read_text());assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'items':plan['items'],'truth':plan['truth'],'parent_sha256':sha(p),'script_sha256':sha(Path(__file__)),'policy':'Exactly same assigned two-sector epochs, SPOC instead of QLP. Known controls; same photons, not independent observations.10minbinning,120daymaxbaseline,originalscreening. Missing products remain errors.'})
def work(item):
 dest=out/item['label'];(dest/'targets').mkdir(parents=True,exist_ok=True)
 r=process_target(item['target'],Path('data'),dest,partial(load_training,bin_minutes=10),120)
 return {'tic':r['tic'],'label':item['label'],'status':r['status'],'error':r.get('error'),'result_path':str(dest/'targets'/f'{r["tic"]}.json'),'matches':[{'planet':name,'peak':k} for k in r.get('peaks',[]) for name,period in plan['truth'][str(r['tic'])].items() if abs(k['period']/period-1)<.01]}
with ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(work,plan['items']))
save_json(out/'results.json',rows);print(rows,flush=True)
