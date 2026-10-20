from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json,now,fetch,read_curve
from exoplanet.campaign import lightcurve_url
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure,prediction_spread
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;fp=Path('results/solar-radius-next256-followup-20261011/396160833/frozen.json');f=json.loads(fp.read_text());b=f['best'];raw=Path('data/lightcurves/s0025-396160833.fits');assert not raw.exists()
save_json(p/'plan.json',dict(created_utc=now(),frozen_path=str(fp),frozen_sha256=sha(fp),sector=25,script_sha256=sha(Path(__file__)),policy='Post-sector79 choice of nearest unused epoch. Use frozen discovery clock unchanged. Fixed nominal and frozen-profile sensitivity only; profile maximum is selected after inspection, not confirmation.'))
source=fetch(lightcurve_url(396160833,25),raw);t,y,e,star=read_curve(raw);assert int(star['ticid'])==396160833 and int(star['sector'])==25;t,y,e=flatten(t,y,e)
nominal=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,f['timing_ranges'])
rows=[]
for period,epoch in f['timing_ranges']['profile_timing_pairs']:
 epoch+=round((b['transit_time']-epoch)/period)*period
 m=fixed_measure(t,y,e,period,epoch,b['duration'])
 rows.append(dict(period=period,epoch=epoch,total=m['total']))
valid=[r for r in rows if r['total'] is not None];best=max(valid,key=lambda r:r['total']['snr']) if valid else None
save_json(p/'results.json',dict(source=source,star=star,nominal=nominal,timing_spread_days=spread,duration_days=b['duration'],profile=rows,profile_max=best,limits='Profile scan omits extra epoch-floor offsets and searches same-sector noise. No calibrated FAP, no exclusion of all timing alternatives.'))
np.savez_compressed(p/'photometry.npz',t=t,y=y,e=e)
fig,axes=plt.subplots(2,1,figsize=(10,6),constrained_layout=True);axes[0].plot(t,(y-1)*1e6,'.',ms=2);axes[0].set_xlabel('BTJD');axes[0].set_ylabel('Flux residual ppm')
phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;axes[1].scatter(phase*24,(y-1)*1e6,s=5);axes[1].axvspan(-b['duration']*12,b['duration']*12,alpha=.2);axes[1].set_xlabel('Hours from nominal predicted center');axes[1].set_ylabel('Flux residual ppm');fig.savefig(p/'nominal.png',dpi=140)
print('nominal',nominal['total'],'spread',spread,'profile max',best)
