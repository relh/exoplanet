"""Follow four-sector faint midradius pilot pilot screen passes and explicitly labeled detrending diagnostics."""
from pathlib import Path
from functools import partial
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent;campaign=Path('results/qlp-faint-midradius-remaining-two-20261011')
plan=json.loads((out/'plan.json').read_text())
assert sha(campaign/'plan.json')==plan['campaign_run_sha256_at_start']
for name,h in plan['source_sha256'].items():assert sha(Path('src/exoplanet')/name)==h
records=json.loads((out/'progress.json').read_text())
assert records==json.loads((out/'pre-resume-progress.json').read_text())
seen={(r['tic'],r['peak_index']) for r in records}
assert len(seen)==len(records) and all(r['status']=='complete' for r in records)
assert {p.name for p in out.iterdir() if p.is_dir()}=={f'{tic}-peak{i}' for tic,i in seen}
for r in records:
 assert sha(Path(r['discovery_path']))==r['discovery_sha256']
 folder=out/f"{r['tic']}-peak{r['peak_index']}"
 assert all((folder/n).exists() for n in ['frozen.json','heldout.json','discovery.png','secondary.json'])
save_json(out/'resume-start.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'previous_exit_code':143,'n_preserved':len(records),'pre_resume_progress_sha256':sha(out/'pre-resume-progress.json'),'policy':'Previous handle terminal and process absent. Resume only remaining eligible peaks; preserve original plan and all completed artifacts.'})
def eligible():
 items=[]
 for p in (campaign/'targets').glob('*.json'):
  try:d=json.loads(p.read_text())
  except json.JSONDecodeError:continue
  for i,peak in enumerate(d.get('screened_peaks',[])):
   if set(peak['flags'])<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'} and (d['tic'],i) not in seen:items.append((p,d,i))
 return items
while True:
 for p,d,i in eligible():
  key=(d['tic'],i);seen.add(key);dest=out/f'{key[0]}-peak{key[1]}'
  rec={'tic':key[0],'peak_index':i,'discovery_path':str(p),'discovery_sha256':sha(p),'started_utc':now(),'original_flags':d['screened_peaks'][i]['flags'],'diagnostic_only':'alternative_detrending_prefers_other_period' in d['screened_peaks'][i]['flags']}
  try:
   checks=follow_qlp(p,dest,peak_index=i,max_sectors=2)
   rec['heldout']=[{'sector':x['sector'],'status':x['status'],'conclusion':x.get('conclusion',x.get('error'))} for x in checks]
   plot_discovery(p,dest/'discovery.png',peak_index=i,loader=partial(load_qlp,bin_minutes=0))
   t,y,e,evidence=load_qlp(d['target'],Path('data'))
   sec=scan_secondary(t,y,e,d['screened_peaks'][i]['best'])
   save_json(dest/'secondary.json',{'data':evidence,'diagnostic':sec,'policy':'Exploratory training-only off-phase scan; selected SNR not calibrated'})
   rec['status']='complete'
  except Exception as exc:rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
  rec['finished_utc']=now();records.append(rec);save_json(out/'progress.json',records);print(rec,flush=True)
 try:done=(campaign/'results.json').exists() and len(json.loads((campaign/'results.json').read_text()))==len(json.loads((campaign/'plan.json').read_text())['targets'])
 except json.JSONDecodeError:done=False
 # Re-scan once the discovery run is terminal to avoid missing final-written files.
 if done and not eligible():break
 time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records})
