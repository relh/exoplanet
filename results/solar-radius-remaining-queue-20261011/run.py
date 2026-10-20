from pathlib import Path
import json,sys,subprocess,shutil,collections
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());assert sha(Path(plan['source']))==plan['source_sha256'];eligible=json.loads(Path(plan['source']).read_text());state=dict(status='running',started_utc=now(),plan_sha256=sha(p/'plan.json'),script_sha256=sha(Path(__file__)),completed=[]);save_json(p/'execution.json',state)
for batch in plan['batches']:
 src=Path(batch['selection']);out=Path(batch['output']);assert sha(src)==batch['selection_sha256'];selected=json.loads(src.read_text());assert selected==eligible[batch['start']:batch['end']]
 if out.exists():raise RuntimeError(f'Output exists; inspect before any resume: {out}')
 if shutil.disk_usage('.').free<60*1024**3:raise RuntimeError('Less than60GiB free; stop queue without deleting evidence')
 for target in selected:
  for s in target['training_sectors']+target['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{target['tic']}.fits").exists()
 state['active']=batch;save_json(p/'execution.json',state)
 result=subprocess.run([sys.executable,'-m','exoplanet.campaign','--selection',str(src),'--output',str(out),'--limit',str(batch['n']),'--workers',str(plan['workers'])])
 if result.returncode:raise RuntimeError(f'Campaign returned{result.returncode}; preserve partial output for explicit recovery')
 run=json.loads((out/'run.json').read_text());rows=[json.loads(f.read_text()) for f in (out/'targets').glob('*.json')];assert run['status']=='complete' and len(rows)==batch['n'];assert {r['tic'] for r in rows}=={r['tic'] for r in selected};assert run['selection_sha256']==sha(src)
 for name,digest in run['source_sha256'].items():assert sha(out/'source'/name)==digest
 raw=0;lookup={r['tic']:r for r in selected};leads=[]
 for r in rows:
  assert r['target']==lookup[r['tic']]
  for d in r.get('data',[]):
   assert sha(Path(f"data/lightcurves/s{d['sector']:04d}-{r['tic']}.fits"))==d['source']['sha256'];assert d['star']['ticid']==r['tic'] and d['star']['sector']==d['sector'];raw+=1
  for s in r['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{r['tic']}.fits").exists()
  for i,peak in enumerate(r.get('screened_peaks',[])):
   if not peak['flags']:leads.append(dict(tic=r['tic'],peak_index=i,best=peak['best']))
 assert run['n_errors']==sum(r['status']=='error' for r in rows);assert run['n_followup']==sum(r.get('disposition')=='followup_priority' for r in rows)
 audit=dict(status='passed',verified_utc=now(),counts=dict(collections.Counter(r.get('disposition',r['status']) for r in rows)),raw_products_checked=raw,reserved_cache_absent=True,eligible_peaks=leads,queue_plan_sha256=sha(p/'plan.json'),verifier_sha256=sha(Path(__file__)));save_json(out/'verification.json',audit)
 state['completed'].append(dict(output=str(out),verification=audit));save_json(p/'execution.json',state);print('AUDITED',str(out),audit['counts'],flush=True)
state.update(status='complete',finished_utc=now(),active=None);save_json(p/'execution.json',state)
