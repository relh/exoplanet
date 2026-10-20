"""Refine using four already-opened sectors; freeze two genuinely unopened ones."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
out=Path(__file__).parent
p=Path('results/campaign-qlp-full-pool-20261010/targets/240023401.json');row=json.loads(p.read_text())
f=Path('results/qlp-full-pool-followup-20261010/240023401-peak0/frozen.json');prior=json.loads(f.read_text())
new=dict(row);new['target']=dict(row['target'],training_sectors=[43,44,20,60],heldout_sectors=[71,72])
new['screened_peaks']=[{'best':prior['best']}]
new['expanded_training_policy']={'utc':now(),'original_discovery_sha256':sha(p),'prior_frozen_sha256':sha(f),'note':'No new blind-discovery claim:43/44/20/60 already opened. Original clean_baseline_days retained solely to set the seed period-refinement width, as in existing expanded-training workflow. New follow-up records actual expanded training provenance/times. Freeze before opening71/72;73 remains reserved.'}
for s in [71,72,73]:assert not Path(f'data/qlp/240023401-s{s:04d}.fits').exists()
save_json(out/'discovery.json',new)
checks=follow_qlp(out/'discovery.json',out/'followup',max_sectors=2)
for c in checks:print(c['sector'],c.get('conclusion',c.get('error')),c.get('measurement',{}).get('total'),c.get('timing_spread_days'),flush=True)
