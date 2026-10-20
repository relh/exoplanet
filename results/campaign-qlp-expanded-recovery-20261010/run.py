"""Wait for initial run, then separately retry missing-error QLP targets."""
import json,time,shutil,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import process_target,SETTINGS
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent;original=Path('results/campaign-qlp-expanded-20261010')
assert not (out/'run.json').exists()
save_json(out/'queued.json',{'utc':now(),'awaiting':str(original/'run.json'),'policy':'After initial run completes, retry only errors explicitly reporting no finite positive quality-zero QLP flux/error pairs. Enable existing empirical-errors fallback only where no published usable error pairs exist. Retain original failures. Uncalibrated exploratory recovery, not published-error equivalence.','script_sha256':sha(Path(__file__))})
while True:
 try:done=json.loads((original/'run.json').read_text())['status']=='complete'
 except json.JSONDecodeError:done=False
 if done:break
 time.sleep(15)
rows=[];inputs=[]
for p in sorted((original/'targets').glob('*.json')):
 d=json.loads(p.read_text())
 if d['status']=='error' and 'No finite positive quality-zero QLP flux/error pairs' in d['error']:
  rows.append(dict(d['target'],estimate_missing_errors=True));inputs.append({'path':str(p),'sha256':sha(p),'error':d['error']})
(out/'targets').mkdir();(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
for name in ['uv.lock','pyproject.toml']:shutil.copyfile(name,out/'source'/name)
save_json(out/'selected.json',rows)
run={'utc':now(),'status':'running','n_selected':len(rows),'original_run_sha256':sha(original/'run.json'),'original_failures':inputs,'selected_sha256':sha(out/'selected.json'),'source_sha256':{p.name:sha(p) for p in (out/'source').iterdir()},'settings':{**SETTINGS,'max_training_baseline_days':120,'bin_minutes':10,'estimate_missing_errors':True},'caution':'Some sector errors estimated from robust adjacent differences; no calibrated significance/completeness. Original failures retained. Published usable errors remain in use for other sectors.'}
save_json(out/'run.json',run);results=[]
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(process_target,t,Path('data'),out,load_qlp,120) for t in rows]
 for future in as_completed(futures):
  results.append(future.result());save_json(out/'progress.json',{'utc':now(),'completed':len(results),'total':len(rows),'errors':sum(r['status']=='error' for r in results)})
review=[]
for r in results:
 for i,p in enumerate(r.get('screened_peaks',[])):
  if set(p['flags'])<={'crowding_or_missing_crowding'}:review.append({'tic':r['tic'],'peak_index':i,'best':p['best'],'flags':p['flags']})
save_json(out/'review.json',review);run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in results),n_review_peaks=len(review));save_json(out/'run.json',run)
print('terminal',len(rows),'selected',run['n_errors'],'errors',len(review),'review peaks',flush=True)
