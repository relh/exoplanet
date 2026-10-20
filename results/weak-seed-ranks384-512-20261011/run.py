from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,shutil
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());assert sha(p/'selected.json')==plan['selected_sha256'];audit=Path('results/solar-radius-lead-audit-20261011/audit.json');assert sha(audit)==plan['audit_sha256'];shutil.copyfile(audit,p/'source-audit.json');selected=json.loads((p/'selected.json').read_text());(p/'targets').mkdir(exist_ok=False);(p/'source').mkdir(exist_ok=False)
for q in Path('src/exoplanet').glob('*.py'):shutil.copyfile(q,p/'source'/q.name)
run=dict(status='running',started_utc=now(),plan_sha256=sha(p/'plan.json'),runner_sha256=sha(Path(__file__)),source_sha256={q.name:sha(q) for q in (p/'source').glob('*.py')},n_selected=len(selected),workers=2);save_json(p/'run.json',run)
def one(row):
 tic=row['tic'];target=row['target'];result=dict(tic=tic,status='error',started_utc=now(),selection=row,windows=[])
 try:
  assert sha(Path(row['original_path']))==row['original_sha256']
  for s in row['added_sectors']+target['heldout_sectors']:assert not Path(f'data/lightcurves/s{s:04d}-{tic}.fits').exists()
  for window in [1.5,2.5]:
   t,y,e,ev=load_training(target,Path('data'),window=window);best,ranges=refine_training(t,y,e,row['seed'],seed_baseline=row['original_baseline_days']);result['windows'].append(dict(window_days=window,best=best,timing_ranges=ranges,measurement=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']),training_data=ev));save_json(p/'targets'/f'{tic}.json',result)
  a,b=result['windows'];eligible=(a['best']['depth_snr']>=8 and b['best']['depth_snr']>=8 and abs(a['best']['period']/b['best']['period']-1)<.005 and not a['timing_ranges']['search_boundary_hit'] and not b['timing_ranges']['search_boundary_hit']);result.update(status='measured',local_review_flag=eligible)
 except Exception as exc:result.update(error=repr(exc))
 result['finished_utc']=now();save_json(p/'targets'/f'{tic}.json',result);print(tic,result['status'],result.get('local_review_flag'),[(x['best']['period'],x['best']['depth_snr']) for x in result['windows']],flush=True);return result
rows=[]
with ThreadPoolExecutor(max_workers=2) as pool:
 for f in as_completed([pool.submit(one,r) for r in selected]):
  rows.append(f.result());save_json(p/'progress.json',dict(completed=len(rows),total=len(selected),updated_utc=now()))
run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in rows),n_local_review_flags=sum(r.get('local_review_flag',False) for r in rows));save_json(p/'run.json',run)
