"""Compare already-measured event centers; no new signal selection or fitting."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
paths=[out/'frozen.json',out.parent/'85408605-peak1/frozen.json']
a,b=[json.loads(p.read_text()) for p in paths]
long=a['training_measurement']['events'];short=b['training_measurement']['events']
matched=[]
for x in long:
 y=min(short,key=lambda z:abs(z['center_btjd']-x['center_btjd']))
 matched.append({'long_event':x['event'],'short_event':y['event'],'center_difference_seconds':(y['center_btjd']-x['center_btjd'])*86400,'long_snr':x['snr'],'short_snr':y['snr']})
assert [r['short_event'] for r in matched]==[0,2,4]
assert all(abs(r['center_difference_seconds'])<90 for r in matched)
extra=[r for r in short if r['event'] not in [m['short_event'] for m in matched]]
assert len(extra)==1 and extra[0]['snr']<2
save_json(out/'alias-events.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_hashes':{str(p):sha(p) for p in paths},'period_ratio':a['best']['period']/b['best']['period'],'matched':matched,'additional_measured_short_period_events':extra,'limits':'The three supported events at both periods coincide within90seconds, compared with0.072day fitted duration. One additional measured short-period event is unsupported. Missing events are not nondetections; this is an alias diagnostic, not a unique-period or host identification.'})
print('Verified same three supported dips in the competing period fits.')
