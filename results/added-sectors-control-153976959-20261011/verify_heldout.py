from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,read_curve,save_json
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());h=json.loads((p/'heldout.json').read_text());plan=json.loads((p/'heldout-plan.json').read_text());b=f['best'];raw=Path('data/lightcurves/s0076-153976959.fits');assert sha(raw)==h['source']['sha256'];assert sha(p/'frozen.json')==plan['frozen_sha256'];assert sha(p/'verification.json')==plan['verification_sha256'];assert f['frozen_utc']<plan['created_utc']<=h['started_utc']<h['source']['retrieved_utc']
t,y,e,star=read_curve(raw);assert star['ticid']==153976959 and star['sector']==76;t,y,e=flatten(t,y,e);m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);assert m==h['measurement'];assert prediction_spread(t,b,f['timing_ranges'])==h['timing_spread_days'];assert h['timing_spread_days']>b['duration']/2 and h['conclusion']=='timing_prediction_inconclusive'
for saved,(period,epoch) in zip(h['profile_rows'],f['timing_ranges']['profile_timing_pairs']):
 epoch+=round((b['transit_time']-epoch)/period)*period;assert saved['period']==period and saved['epoch']==epoch;assert fixed_measure(t,y,e,period,epoch,b['duration'])==saved['measurement']
assert len(h['profile_rows'])==len(f['timing_ranges']['profile_timing_pairs']);assert max(h['profile_rows'],key=lambda q:q['measurement']['total']['snr'])==h['profile_best'];z=np.load(p/'heldout-photometry.npz');np.testing.assert_array_equal(t,z['time']);np.testing.assert_array_equal(y,z['flux']);np.testing.assert_array_equal(e,z['error'])
save_json(p/'heldout-verification.json',dict(status='passed',freeze_precedes_reserved_download=True,raw_hash_and_identity_checked=True,nominal_reconstructed=True,profile_pairs_checked=len(h['profile_rows']),limits='Reproducibility of conditional measurements; not independent confirmation or a physical timing posterior.'))
print(h['expected_formal_snr'],len(h['profile_rows']))
