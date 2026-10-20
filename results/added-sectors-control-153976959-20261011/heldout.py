from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json,sha,now,fetch,read_curve
from exoplanet.campaign import lightcurve_url
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
p=Path(__file__).parent;f=json.loads((p/'frozen.json').read_text());assert json.loads((p/'verification.json').read_text())['status']=='passed';b=f['best'];raw=Path('data/lightcurves/s0076-153976959.fits');assert f['heldout_sectors']==[76] and not raw.exists()
save_json(p/'heldout-plan.json',dict(created_utc=now(),frozen_sha256=sha(p/'frozen.json'),verification_sha256=sha(p/'verification.json'),script_sha256=sha(Path(__file__)),policy='Open original reserved sector76 only after expanded discovery clock is frozen and verified. Same fixed-clock measurements, timing-spread heuristic and conclusion rules as followup.py. Evaluate all previously saved profile pairs at frozen duration separately; no new period/epoch fit. Known-planet control, not a new discovery.'))
r=dict(sector=76,started_utc=now(),status='error')
try:
 r['source']=fetch(lightcurve_url(153976959,76),raw);t,y,e,star=read_curve(raw);assert star['ticid']==153976959 and star['sector']==76;t,y,e=flatten(t,y,e);m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,f['timing_ranges']);precise=spread<b['duration']/2 and not f['timing_ranges']['search_boundary_hit'] and f['training_measurement']['supported_events']>=3;total=m['total'];expected=None if total is None else b['depth']/total['error']
 if not precise:conclusion='timing_prediction_inconclusive'
 elif total is None:conclusion='insufficient_coverage'
 elif total['snr']>=5 and m['supported_events']>=2:conclusion='recovered_at_frozen_ephemeris_requires_further_vetting'
 elif expected>=5 and total['snr']<2:conclusion='not_recovered_despite_expected_sensitivity'
 else:conclusion='insufficient_evidence'
 rows=[]
 for period,epoch in f['timing_ranges']['profile_timing_pairs']:
  epoch+=round((b['transit_time']-epoch)/period)*period;rows.append(dict(period=period,epoch=epoch,measurement=fixed_measure(t,y,e,period,epoch,b['duration'])))
 best=max((x for x in rows if x['measurement']['total'] is not None),key=lambda x:x['measurement']['total']['snr']);r.update(status='measured',star=star,measurement=m,timing_spread_days=spread,timing_precise=precise,expected_formal_snr=expected,conclusion=conclusion,profile_rows=rows,profile_best=best,limits='Profile maximum is over correlated discovery alternatives, not calibrated significance. Timing model ignores red noise and shape mismatch. No epoch-floor offsets or new durations scanned.');np.savez_compressed(p/'heldout-photometry.npz',time=t,flux=y,error=e)
except Exception as exc:r.update(error=repr(exc));save_json(p/'heldout.json',r);raise
save_json(p/'heldout.json',r);print('nominal',m['total'],'spread',spread,'conclusion',conclusion,'profilemax',best['measurement']['total'])
