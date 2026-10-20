"""Alternative extraction of already-opened Sector 58; no new holdouts."""
import json
from pathlib import Path
import numpy as np
from exoplanet.archive import qlp_observations
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now

out=Path('results/qlp-heldout-83968926-s58-20261009')
parent=Path('results/followup-83968926-expanded-20261009')
frozen=json.loads((parent/'frozen.json').read_text())
previous=json.loads((parent/'heldout.json').read_text())[0]
assert frozen['heldout_sectors']==[58] and previous['sector']==58
if (out/'run.json').exists():raise RuntimeError('Preserve existing result')
run={'status':'running','started_utc':now(),'frozen_sha256':sha(parent/'frozen.json'),
     'previous_spoc_check_sha256':sha(parent/'heldout.json'),'script_sha256':sha(out/'check.py'),
     'policy':'Reuse original frozen ephemeris. Sector 58 SPOC was already opened. Compare QLP fixed time and explicitly exploratory 161 epoch shifts across original timing spread. No period refit, no Sector 78/85 opened. Not calibrated exclusion or independent prediction.',
     'seed':frozen['best'],'timing_spread_days':previous['timing_spread_days']}
save_json(out/'run.json',run)
try:
    obs,evidence=qlp_observations([83968926],Path('data/qlp-observations/83968926.json'))
    product=next(o for o in obs if int(o['sequence_number'])==58)
    target={'tic':83968926,'training_sectors':[58],'qlp_products':{'58':product}}
    t,y,dy,data=load_qlp(target,Path('data'));b=frozen['best']
    fixed=fixed_measure(t,y,dy,b['period'],b['transit_time'],b['duration'])
    span=previous['timing_spread_days'];trials=[]
    for shift in np.linspace(-span,span,161):
        measure=fixed_measure(t,y,dy,b['period'],b['transit_time']+shift,b['duration'])
        trials.append({'epoch_shift_days':float(shift),'measurement':measure})
    valid=[r for r in trials if r['measurement']['total'] is not None]
    best=max(valid,key=lambda r:r['measurement']['total']['snr']) if valid else None
    save_json(out/'measurements.json',{'fixed':fixed,'exploratory_best':best,'trials':trials})
    run.update(status='complete',finished_utc=now(),data=data,observation_query=evidence)
    print('Fixed',fixed['total'],'Exploratory',best,flush=True)
except Exception as exc:
    run.update(status='error',finished_utc=now(),error=f'{type(exc).__name__}: {exc}')
    print(run['error'],flush=True)
save_json(out/'run.json',run)
