from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;audit=Path('results/solar-radius-lead-audit-20261011/audit.json');inventory=json.loads(audit.read_text());eligible=[]
for batch in inventory['batches']:
 for path in sorted((Path(batch['path'])/'targets').glob('*.json')):
  r=json.loads(path.read_text())
  if r.get('disposition')!='below_screen_threshold':continue
  early=[s for s in r['target']['sectors'] if s<=55];added=[s for s in early if s not in r['target']['training_sectors']]
  if len(added)<2 or len(early)>9:continue
  if any(Path(f"data/lightcurves/s{s:04d}-{r['tic']}.fits").exists() for s in added+r['target']['heldout_sectors']):continue
  eligible.append(dict(tic=r['tic'],original_path=str(path),original_sha256=sha(path),seed=r['best'],original_baseline_days=r['clean_baseline_days'],target={**r['target'],'training_sectors':early},original_training_sectors=r['target']['training_sectors'],added_sectors=added))
eligible.sort(key=lambda x:(-x['seed']['depth_snr'],x['tic']));selected=eligible[:8];assert len(selected)==8
save_json(p/'eligible.json',eligible);save_json(p/'selected.json',selected);save_json(p/'plan.json',dict(created_utc=now(),audit_sha256=sha(audit),selection_script_sha256=sha(Path(__file__)),selected_sha256=sha(p/'selected.json'),n_eligible=len(eligible),n_selected=len(selected),policy='Exploratory eight-star pilot from completed original below-threshold records only. Require at least2 unopened additional sectors<=55, at most9 total early sectors, and unopened original reserved sectors. Rank original maximum SNR descending then TIC. Use the original strongest peak as the sole local-refinement seed; add all early sectors with unchanged local refinement at1.5/2.5day detrending. Review flag only if both local formal SNR>=8, periods agree within0.5%, and neither profile hits its search boundary. This is NOT original full-gate passage, calibrated significance or blind full-domain rediscovery. Preserve failures; no reserved sector is opened.'))
print('eligible',len(eligible),[(x['tic'],x['seed']['depth_snr'],x['added_sectors']) for x in selected])
