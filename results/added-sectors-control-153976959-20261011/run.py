from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.followup import refine_training,fixed_measure
p=Path(__file__).parent;src=Path('results/solar-radius-positive-controls-run-20261011/targets/153976959.json');r=json.loads(src.read_text());target=dict(r['target']);original=list(target['training_sectors']);target['training_sectors']=[s for s in target['sectors'] if s<=55];added=[s for s in target['training_sectors'] if s not in original]
assert added==[22,41,48,49]
for sector in added+target['heldout_sectors']:assert not Path(f'data/lightcurves/s{sector:04d}-153976959.fits').exists()
save_json(p/'plan.json',dict(created_utc=now(),original_path=str(src),original_sha256=sha(src),target=target,seed=r['best'],original_baseline_days=r['clean_baseline_days'],original_training_sectors=original,added_sectors=added,script_sha256=sha(Path(__file__)),source_sha256={q.name:sha(q) for q in Path('src/exoplanet').glob('*.py')},policy='Positive-control experiment selected after original below-threshold outcome. Expand to every <=55 sector; refine only original strongest unseeded-search peak with existing local refinement and original baseline setting. Catalog orbital period not supplied. No alternate peak chosen after outcome; no heldout data. A local seeded fit is not a full-domain discovery search or full-gate pass.'))
t,y,dy,evidence=load_training(target,Path('data'));best,ranges=refine_training(t,y,dy,r['best'],seed_baseline=r['clean_baseline_days'])
frozen=dict(frozen_utc=now(),discovery_sha256=sha(src),tic=153976959,training_data=evidence,original_training_sectors=original,expanded_training=True,training_sectors=target['training_sectors'],seed=r['best'],best=best,timing_ranges=ranges,training_measurement=fixed_measure(t,y,dy,best['period'],best['transit_time'],best['duration']),heldout_sectors=target['heldout_sectors'],source_sha256={q.name:sha(q) for q in Path('src/exoplanet').glob('*.py')});save_json(p/'frozen.json',frozen)
np.savez_compressed(p/'photometry.npz',time=t,flux=y,error=dy)
print(best,{k:v for k,v in ranges.items() if k!='profile_timing_pairs'},flush=True)
# Alternate detrending is fitted independently in the same original seed interval.
ta,ya,ea,ev=load_training(target,Path('data'),window=2.5);ba,ra=refine_training(ta,ya,ea,r['best'],seed_baseline=r['clean_baseline_days']);save_json(p/'alternative.json',dict(best=ba,timing_ranges=ra,measurement=fixed_measure(ta,ya,ea,ba['period'],ba['transit_time'],ba['duration']),data=ev));print('alternate',ba,flush=True)
