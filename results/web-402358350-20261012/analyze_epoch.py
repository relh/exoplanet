from pathlib import Path
import json,csv,numpy as np
from astropy.time import Time
from astropy.timeseries import LombScargle
from exoplanet.pipeline import sha,save_json,now
from exoplanet.followup import prediction_spread
p=Path(__file__).parent;plan=json.loads((p/'epoch-plan.json').read_text());src=json.loads((p/'epoch-source.json').read_text());raw=Path(src['path']);assert sha(raw)==src['sha256'];rows=list(csv.DictReader(raw.open()));assert all(r['source_id']==plan['source_id'] for r in rows)
keep=[r for r in rows if r['variability_flag_g_reject']=='false' and r['rejected_by_photometry']=='false' and all(r[k] and np.isfinite(float(r[k])) for k in ['g_transit_time','g_transit_flux','g_transit_flux_error']) and float(r['g_transit_flux'])>0 and float(r['g_transit_flux_error'])>0];t=Time(np.array([float(r['g_transit_time']) for r in keep])+2455197.5,format='jd',scale='tcb').tdb.jd-2457000;flux=np.array([float(r['g_transit_flux']) for r in keep]);err=np.array([float(r['g_transit_flux_error']) for r in keep]);median=np.median(flux);y=flux/median;e=err/median;out=[]
for c in plan['clocks']:
 b=c['best'];d=abs((t-b['transit_time']+b['period']/2)%b['period']-b['period']/2);inside=d<b['duration']/2;outside=d>1.5*b['duration'];cycles=np.unique(np.rint((t[inside]-b['transit_time'])/b['period']).astype(int));spread=prediction_spread(t,b,c['ranges']);m=dict(n_inside=int(inside.sum()),n_outside=int(outside.sum()),event_cycles=cycles.tolist(),timing_spread_days=spread,half_duration=b['duration']/2,outcome='inconclusive' if spread>=b['duration']/2 or len(cycles)<2 else 'timing_and_count_adequate_no_detection_claim')
 if inside.sum()>0 and outside.sum()>0:
  wi=1/e[inside]**2;wo=1/e[outside]**2;depth=np.average(y[outside],weights=wo)-np.average(y[inside],weights=wi);error=np.sqrt(1/wi.sum()+1/wo.sum());m.update(depth=depth,formal_error=error,snr=depth/error)
 out.append(dict(source=c['source'],window=c['window'],measurement=m))
explore=None
if len(t)>=30:
 periods=np.geomspace(.05,100,50000);power=LombScargle(t,y,e).power(1/periods);order=np.argsort(power)[::-1];peaks=[]
 for i in order:
  if all(abs(periods[i]/q['period']-1)>.02 for q in peaks):peaks.append(dict(period=float(periods[i]),power=float(power[i])))
  if len(peaks)==10:break
 explore=dict(peaks=peaks,policy='Predeclared exploratory single-sinusoid grid; no calibrated significance, no candidate-clock adjustment.');np.savez_compressed(p/'gaia-periodogram.npz',period=periods,power=power)
np.savez_compressed(p/'gaia-processed.npz',t=t,y=y,e=e)
save_json(p/'epoch-results.json',dict(created_utc=now(),raw_count=len(rows),quality_count=len(t),span_btjd=[float(t.min()),float(t.max())],normalized_flux_p05_p95=np.percentile(y,[5,95]).tolist(),median_formal_error=float(np.median(e)),normalized_std=float(np.std(y)),fixed_tests=out,exploratory=explore,limits='Neighbor photometry, not target; sparse sampling and timing uncertainty prevent transit exclusion. Variability flags/classifier not physical cause confirmation.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(11,4),constrained_layout=True);axs[0].errorbar(t,y,yerr=e,fmt='.');axs[0].set(xlabel='BTJD TDB',ylabel='Median-normalized Gaia G',title='Exact neighbor402358249')
if explore:axs[1].plot(periods,power);axs[1].set(xscale='log',xlabel='Exploratory sinusoid period, days',ylabel='LS power',title='Selected aliases; no confirmation')
fig.savefig(p/'gaia-diagnostic.png',dpi=120);print(len(rows),len(t),out,explore)
