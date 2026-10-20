"""Run the full frozen remaining QLP pool; label missing-error estimates."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,shutil,subprocess,importlib.metadata
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target,SETTINGS
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;selection=Path('results/qlp-full-pool-coverage-20261010/selected.json')
assert not (out/'run.json').exists(),'Do not overwrite an existing run'
targets=[dict(t,estimate_missing_errors=True) for t in json.loads(selection.read_text())];(out/'targets').mkdir();(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
for name in ['uv.lock','pyproject.toml']:shutil.copyfile(name,out/'source'/name)
run={'started_utc':now(),'status':'running','n_selected':len(targets),'selection_path':str(selection),'selection_sha256':sha(selection),'script_sha256':sha(Path(__file__)),'source_sha256':{p.name:sha(p) for p in (out/'source').iterdir()},'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','astropy']},'settings':{**SETTINGS,'bin_minutes':10,'max_training_baseline_days':120,'estimate_missing_errors':True},'selection_note':'All5619 viable targets from complete metadata coverage of remaining27549-star untouched pool; disjoint from original, late-sector and288-target QLP selections. Earliest adjacent training pair plus separate reserved epoch. Not necessarily absent from all SPOC products.','caution':'QLP aperture crowding unassessed; crowding-only flags require followup, never planet promotion. Published errors used where valid; if a sector has no usable error pairs, robust adjacent-difference estimates are explicitly labeled in per-sector evidence. Not calibrated red-noise errors, trial-corrected significance or completeness.'}
save_json(out/'run.json',run);rows=[]
with ThreadPoolExecutor(max_workers=8) as pool:
 futures=[pool.submit(process_target,t,Path('data'),out,load_qlp,120) for t in targets]
 for future in as_completed(futures):
  rows.append(future.result());save_json(out/'progress.json',{'utc':now(),'completed':len(rows),'total':len(targets),'errors':sum(r['status']=='error' for r in rows)})
review=[]
for r in rows:
 for i,p in enumerate(r.get('screened_peaks',[])):
  if set(p['flags'])<={'crowding_or_missing_crowding'}:review.append({'tic':r['tic'],'peak_index':i,'best':p['best'],'flags':p['flags']})
save_json(out/'review.json',review)
run.update(status='complete',finished_utc=now(),n_errors=sum(r['status']=='error' for r in rows),n_review_peaks=len(review));save_json(out/'run.json',run)
print('terminal',run['n_errors'],'errors',len(review),'review peaks',flush=True)
