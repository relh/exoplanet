from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json,sha,now,fetch,read_curve
from exoplanet.campaign import lightcurve_url
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;prior=Path('results/followup-469309982-20261011');f=json.loads((prior/'frozen.json').read_text());h=json.loads((prior/'heldout.json').read_text());assert json.loads((prior/'heldout-verification.json').read_text())['status']=='passed';raw=Path('data/lightcurves/s0063-469309982.fits');assert not raw.exists();chosen=h['profile_best'];b={**f['best'],'period':chosen['period'],'transit_time':chosen['epoch']};clocks=[dict(name='primary_selected_from_sector64',best=b),dict(name='secondary_original_nominal',best=f['best'])]
save_json(p/'plan.json',dict(created_utc=now(),prior_frozen_sha256=sha(prior/'frozen.json'),sector64_sha256=sha(prior/'heldout.json'),clocks=clocks,policy='Primary clock is strongest of nine discovery timing alternatives in sector64. Freeze it before opening still-unread sector63. Also report unchanged original nominal clock as secondary. No phase/period/duration search in63. Adjacent sectors can share systematics; source attribution remains unresolved.'))
source=fetch(lightcurve_url(469309982,63),raw);t,y,e,star=read_curve(raw);assert star['ticid']==469309982 and star['sector']==63;t,y,e=flatten(t,y,e);rows=[]
for c in clocks:
 b=c['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);total=m['total'];expected=None if total is None else b['depth']/total['error'];result='insufficient_coverage' if total is None else 'fixed_clock_recovery_requires_source_vetting' if total['snr']>=5 and m['supported_events']>=2 else 'not_recovered_despite_expected_sensitivity' if expected>=5 and total['snr']<2 else 'insufficient_evidence';rows.append(dict(**c,measurement=m,expected_formal_snr=expected,screening_result=result))
np.savez_compressed(p/'photometry.npz',time=t,flux=y,error=e);save_json(p/'results.json',dict(finished_utc=now(),source=source,star=star,rows=rows,limits='Conditional fixed-clock test, no revised timing-precision claim. Primary selection used63-adjacent64 data. No calibrated false-alarm probability or host confirmation.'));print([(r['name'],r['measurement']['total'],r['measurement']['supported_events']) for r in rows])
