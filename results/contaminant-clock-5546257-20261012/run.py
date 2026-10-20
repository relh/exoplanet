from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.timeseries import BoxLeastSquares
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;fp=Path('results/followup-5546257-20261011/frozen.json');gp=Path('results/gaia-5546257-scene-20261011/vari_eclipsing_binary.json');b=json.loads(fp.read_text())['best'];g=json.loads(gp.read_text())[0];paths=[Path(f'data/lightcurves/s{s:04d}-5546257.fits') for s in [9,35,36,62]]
assert not (p/'plan.json').exists()
save_json(p/'plan.json',dict(created_utc=now(),clock=b,gaia_row=g,inputs={str(q):sha(q) for q in paths+[fp,gp,Path(__file__)]},policy='All four already-opened sectors only. No pixel/new observation access. Unchanged expanded candidate clock; exact Gaia frequency/reference and two eclipse phases converted TCB to TDB. Compare arithmetic harmonics1..8, daily aliases m*f+k for m1..8 k-2..2. Fixed Gaia eclipse timings using narrow candidate duration and published Gaia durations (broad depths detrending-dependent). Exploratory epoch-only BLS at Pgaia,Pgaia/2,Pgaia/4, candidate duration fixed; no period optimization. Both1.5/2.5d detrendings, SAP/PDCSAP common masks. Event centers are predicted candidate centers, not independently measured minima. Compare proximity of supported events to nominal and heuristic3sigma Gaia windows; frequency/phase covariance unavailable.'))
f=float(g['frequency']);sf=float(g['frequency_error']);pg=1/f;ref=float(g['reference_time'])+2455197.5
refT=Time(ref,format='jd',scale='tcb').tdb.jd-2457000;period=Time(ref+pg,format='jd',scale='tcb').tdb.jd-Time(ref,format='jd',scale='tcb').tdb.jd
clocks={};
for label in ['primary','secondary']:
 ph=float(g[f'derived_{label}_ecl_phase']);epoch=Time(ref+ph*pg,format='jd',scale='tcb').tdb.jd-2457000;dur=float(g[f'derived_{label}_ecl_duration'])*period
 clocks[label]=dict(period=period,epoch=epoch,duration=dur,phase=ph,phase_error=float(g[f'derived_{label}_ecl_phase_error']))
harm=[dict(n=n,period=period/n,period_difference=period/n-b['period'],relative_difference=(period/n-b['period'])/b['period'],drift_per_gaia_orbit=n*b['period']-period) for n in range(1,9)]
ali=[dict(m=m,k=k,frequency=abs(m/period+k),frequency_difference=abs(abs(m/period+k)-1/b['period'])) for m in range(1,9) for k in range(-2,3) if abs(m/period+k)>0];ali.sort(key=lambda x:x['frequency_difference'])
save_json(p/'clock-comparison.json',dict(gaia_period_tcb=pg,gaia_period_tdb=period,gaia_period_error_tcb=sf/f**2,reference_btjd_tdb=refT,eclipses=clocks,harmonics=harm,daily_aliases=ali,beat_days_near_fourth=1/abs(4/period-1/b['period'])))
rows=[]
for win in [1.5,2.5]:
 for kind in ['SAP','PDCSAP']:
  arrays=[]
  for s,path in zip([9,35,36,62],paths):
   with fits.open(path) as h:
    assert h[0].header['TICID']==5546257 and h[0].header['SECTOR']==s;a=h[1].data;ok=(a['QUALITY']==0)&np.isfinite(a['TIME'])
    for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:ok&=np.isfinite(a[key])&(a[key]>0)
    t,y,e=flatten(np.array(a['TIME'][ok],float),np.array(a[kind+'_FLUX'][ok],float),np.array(a[kind+'_FLUX_ERR'][ok],float),window=win)
   arrays.append((t,y,e,np.full(len(t),s)))
  t,y,e,sec=[np.concatenate([a[j] for a in arrays]) for j in range(4)];np.savez_compressed(p/f'{kind}-{win}.npz',t=t,y=y,e=e,sector=sec)
  hypotheses={'candidate':dict(period=b['period'],epoch=b['transit_time'],duration=b['duration'],epoch_fit=False)}
  for lab,c in clocks.items():
   hypotheses['gaia_'+lab+'_narrow']=dict(period=c['period'],epoch=c['epoch'],duration=b['duration'],epoch_fit=False)
   hypotheses['gaia_'+lab+'_published_width']=dict(period=c['period'],epoch=c['epoch'],duration=c['duration'],epoch_fit=False)
  bls=BoxLeastSquares(t,y,e)
  for div in [1,2,4]:
   z=bls.power([period/div],[b['duration']],objective='likelihood',oversample=50);hypotheses[f'gaia_div{div}_epoch_fitted']=dict(period=period/div,epoch=float(z.transit_time[0]),duration=b['duration'],epoch_fit=True,power=float(z.power[0]))
  measurements=[]
  for name,c in hypotheses.items():
   for sector in [0,9,35,36,62]:
    sel=np.ones(len(t),bool) if sector==0 else sec==sector;meas=fixed_measure(t[sel],y[sel],e[sel],c['period'],c['epoch'],c['duration']);measurements.append(dict(name=name,sector=sector,clock=c,measurement=meas))
  cand=next(m for m in measurements if m['name']=='candidate' and m['sector']==0)['measurement'];comparisons=[]
  for ev in cand['events']:
   center=ev['center_btjd'];matches=[]
   for lab,c in clocks.items():
    n=round((center-c['epoch'])/period);pred=c['epoch']+n*period;unc=np.hypot(c['phase_error']*period,abs(center-refT)*sf/f)
    dist=abs(center-pred);matches.append(dict(eclipse=lab,nearest_center=pred,offset_days=center-pred,heuristic_sigma_days=float(unc),nominal_window_overlap=bool(dist<(c['duration']+b['duration'])/2),three_sigma_window_overlap=bool(dist<(c['duration']+b['duration'])/2+3*unc)))
   comparisons.append(dict(event=ev['event'],center=center,snr=ev['snr'],depth=ev['depth'],matches=matches))
  rows.append(dict(window=win,kind=kind,hypotheses=measurements,candidate_event_gaia_comparison=comparisons));print(kind,win,[(m['name'],round(m['measurement']['total']['snr'],2)) for m in measurements if m['sector']==0],flush=True)
save_json(p/'results.json',dict(rows=rows,limits='Epoch-fitted alternatives are exploratory on all opened data; Gaia formal frequency propagation lacks covariance and astrophysical ephemeris evolution. Same-photon reductions and formal SNR not independent validation.'))
