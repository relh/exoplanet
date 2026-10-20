from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,read_curve
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());fp=Path(plan['frozen_path']);assert sha(fp)==plan['frozen_sha256'];assert sha(p/'run.py')==plan['script_sha256'];f=json.loads(fp.read_text());b=f['best'];raw=Path('data/lightcurves/s0020-362222987.fits');assert sha(raw)==r['source']['sha256'];assert plan['created_utc']<=r['source']['retrieved_utc']
t,y,e,star=read_curve(raw);t,y,e=flatten(t,y,e);z=np.load(p/'photometry.npz')
for key,a in [('t',t),('y',y),('e',e)]:np.testing.assert_allclose(z[key],a)
assert fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])==r['nominal'];np.testing.assert_allclose(prediction_spread(t,b,f['timing_ranges']),r['timing_spread_days']);assert len(r['profile'])==len(f['timing_ranges']['profile_timing_pairs'])
for row,(period,epoch) in zip(r['profile'],f['timing_ranges']['profile_timing_pairs']):
 epoch+=round((b['transit_time']-epoch)/period)*period;assert row['period']==period and row['epoch']==epoch;assert fixed_measure(t,y,e,period,epoch,b['duration'])['total']==row['total']
assert r['profile_max']==max([q for q in r['profile'] if q['total'] is not None],key=lambda q:q['total']['snr'])
save_json(p/'verification.json',dict(status='passed',profile_measurements_checked=len(r['profile']),nominal_reconstructed=True,input_hashes_verified=True,limits='Numerical reconstruction; not calibration of timing or profile-search significance.'));print(len(r['profile']))
