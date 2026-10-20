from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,shutil
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import process_target
p=Path(__file__).parent
run=json.loads((p/'run.json').read_text());selection=Path(run['selection_path']);assert sha(selection)==run['selection_sha256']
for name,digest in run['source_sha256'].items():assert sha(Path('src/exoplanet')/name)==digest
selected=json.loads(selection.read_text());done={int(q.stem) for q in (p/'targets').glob('*.json')};missing=[r for r in selected if r['tic'] not in done]
assert not (p/'interruption.json').exists()
save_json(p/'interruption.json',dict(observed_utc=now(),original_session=68893,exit_code=143,original_run=run,completed=len(done),remaining_tics=[r['tic'] for r in missing],note='Original process confirmed terminal; no other campaign process present. Resume only missing records without changing selection or settings.'))
with ThreadPoolExecutor(4) as pool:
 for future in as_completed([pool.submit(process_target,t,Path('data'),p) for t in missing]):future.result()
rows=[json.loads(q.read_text()) for q in (p/'targets').glob('*.json')];assert len(rows)==512
run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in rows),n_followup=sum(r.get('disposition')=='followup_priority' for r in rows),resumed_after_exit=143)
save_json(p/'run.json',run)
ranking=sorted([r for r in rows if r['status']=='screened'],key=lambda r:r['best']['depth_snr'],reverse=True)
save_json(p/'ranking.json',[{'tic':r['tic'],'best':r['best'],'disposition':r['disposition'],'flags':[s['flags'] for s in r['screened_peaks']]} for r in ranking])
save_json(p/'progress.json',dict(updated_utc=now(),completed=len(rows),total=512,errors=run['n_errors']))
print('Completed resumed batch',flush=True)
