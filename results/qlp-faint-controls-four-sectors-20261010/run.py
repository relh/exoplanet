"""Four-sector QLP sensitivity controls before choosing faint discovery strategy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;parent=Path('results/qlp-faint-positive-controls-20261010');plan=json.loads((parent/'search-plan.json').read_text());items=[];seen=set()
for row in plan['items']:
 tic=row['target']['tic']
 if tic in seen:continue
 seen.add(tic);t=row['target'];sectors=t['sectors'];groups=[[s,s+1,s+2,s+3] for s in sectors if s+3<=96 and all(x in sectors for x in [s+1,s+2,s+3])]
 if not groups:continue
 for label,g in [('early4',groups[0]),('late4',groups[-1])]:
  if label=='late4' and g==groups[0]:continue
  items.append({'label':label,'target':dict(t,training_sectors=g)})
assert not (out/'plan.json').exists();save_json(out/'plan.json',{'utc':now(),'items':items,'truth':plan['truth'],'parent_sha256':sha(parent/'search-plan.json'),'script_sha256':sha(Path(__file__)),'policy':'Known controls, not discoveries. Earliest/latest available consecutive4sectors<=96, actualbaseline<=120days checked by same pipeline. Compare longer coverage; retain all failures and flags. No cutoff tuning.'})
def work(item):
 dest=out/item['label'];(dest/'targets').mkdir(parents=True,exist_ok=True);r=process_target(item['target'],Path('data'),dest,load_qlp,120)
 return {'tic':r['tic'],'label':item['label'],'status':r['status'],'result_path':str(dest/'targets'/f'{r["tic"]}.json'),'matches':[{'planet':name,'peak':p} for p in r.get('peaks',[]) for name,period in plan['truth'][str(r['tic'])].items() if abs(p['period']/period-1)<.01]}
with ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(work,items))
save_json(out/'results.json',rows);print(rows,flush=True)
