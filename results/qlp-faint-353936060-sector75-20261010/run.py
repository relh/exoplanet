"""Test a closer reserved epoch without refitting the existing ephemeris."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure,prediction_spread
out=Path(__file__).parent
discovery=Path('results/qlp-faint-expanded-20261010/targets/353936060.json')
frozen=Path('results/qlp-faint-expanded-followup-20261010/353936060-peak0/frozen.json')
d=json.loads(discovery.read_text());f=json.loads(frozen.read_text());b=f['best']
assert 75 in d['target']['heldout_sectors'] and 75 not in f['heldout_sectors']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'discovery_sha256':sha(discovery),'frozen_sha256':sha(frozen),'best':b,'sector':75,'previously_cached':Path('data/qlp/353936060-s0075.fits').exists(),'script_sha256':sha(Path(__file__)),'policy':'Closest available reserved sector selected after inconclusive first tests. Original ephemeris unchanged; no period or phase search. Record timing uncertainty and missing coverage; no planet claim.'})
r={'sector':75,'started_utc':now()}
try:
 t,y,e,data=load_qlp(dict(d['target'],training_sectors=[75]),Path('data'),bin_minutes=0)
 m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])
 spread=prediction_spread(t,b,f['timing_ranges'])
 precise=spread<b['duration']/2 and not f['timing_ranges']['search_boundary_hit']
 r.update(status='measured',data=data,measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=None if m['total'] is None else b['depth']/m['total']['error'])
except Exception as exc:r.update(status='error',error=repr(exc))
r['finished_utc']=now();save_json(out/'results.json',r)
print({k:v for k,v in r.items() if k!='data'},flush=True)
