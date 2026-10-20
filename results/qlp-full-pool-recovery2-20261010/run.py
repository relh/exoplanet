"""Recover a frozen snapshot of failed targets using assigned epochs only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from functools import partial
import json,shutil
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import process_target,load_training,SETTINGS
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent
assert not (out/'run.json').exists()
prior=json.loads(Path('results/qlp-full-pool-recovery1-20261010/run.json').read_text());excluded={r['target']['tic'] for r in prior['items']}
assert json.loads(Path('results/campaign-qlp-full-pool-20261010/run.json').read_text())['status']=='complete'
items=[]
for p in sorted(Path('results/campaign-qlp-full-pool-20261010/targets').glob('*.json')):
 d=json.loads(p.read_text())
 if d['status']=='error' and d['tic'] not in excluded:items.append({'target':d['target'],'original_path':str(p),'original_sha256':sha(p),'original_error':d['error']})
(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
run={'utc':now(),'status':'running','items':items,'script_sha256':sha(Path(__file__)),'source_sha256':{p.name:sha(p) for p in (out/'source').iterdir()},'settings':SETTINGS,'policy':'Remaining errors after main terminal state, excluding first frozen73-star recovery cohort. Probe each assigned QLP training sector independently; use surviving sectors if original combined load failed. If none survive, or rerun fails, try same assigned epochs in SPOC. Never load reserved epochs. Reduced sector searches have narrower period coverage. Original error estimates/published errors policy retained. Data-dependent recovery is not independent validation.'}
save_json(out/'run.json',run)
def work(item):
 t=item['target'];dest=out/str(t['tic']);dest.mkdir();checks=[];usable=[]
 for s in t['training_sectors']:
  try:
   tt,yy,ee,evidence=load_qlp(dict(t,training_sectors=[s]),Path('data'))
   checks.append({'sector':s,'status':'usable','n_clean':len(tt),'evidence':evidence});usable.append(s)
  except Exception as exc:checks.append({'sector':s,'status':'error','error':repr(exc)})
 save_json(dest/'sector-probes.json',checks)
 attempts=[]
 if usable and usable!=t['training_sectors']:
  d=dest/'qlp';(d/'targets').mkdir(parents=True)
  r=process_target(dict(t,training_sectors=usable),Path('data'),d,loader=load_qlp,max_baseline=120);attempts.append({'collection':'QLP','path':str(d/'targets'/f'{t["tic"]}.json'),'status':r['status']})
  if r['status']=='screened':return {'tic':t['tic'],'attempts':attempts,'resolved':True}
 d=dest/'spoc';(d/'targets').mkdir(parents=True)
 r=process_target(t,Path('data'),d,loader=partial(load_training,bin_minutes=10),max_baseline=120);attempts.append({'collection':'SPOC','path':str(d/'targets'/f'{t["tic"]}.json'),'status':r['status']})
 return {'tic':t['tic'],'attempts':attempts,'resolved':r['status']=='screened'}
rows=[]
with ThreadPoolExecutor(max_workers=2) as pool:
 futures=[pool.submit(work,item) for item in items]
 for future in as_completed(futures):rows.append(future.result());save_json(out/'progress.json',rows)
run.update(status='complete',finished_utc=now(),n_recovered=sum(r['resolved'] for r in rows));save_json(out/'run.json',run)
print('complete',len(rows),'attempted',run['n_recovered'],'recovered',flush=True)
