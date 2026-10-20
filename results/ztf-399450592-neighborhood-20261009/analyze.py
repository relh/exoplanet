"""Exploratory, fixed-TESS-ephemeris ZTF comparison; no independent discovery claim."""
import csv,json
from pathlib import Path
import numpy as np
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now
iers.conf.auto_download=False
OUT=Path(__file__).parent
seed=Path('results/followup-399450592-expanded-20261009/frozen.json');best=json.loads(seed.read_text())['best']
# Approximate P48 geodetic position; positional error of <1 km gives <4 ms delay.
site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m)

def measure(t,mag,err,groups,period,epoch,duration):
 phase=(t-epoch+period/2)%period-period/2
 inside=abs(phase)<duration/2
 # Simultaneous group intercepts and common eclipse amplitude in magnitudes.
 cols=[(groups==g).astype(float) for g in np.unique(groups)]
 x=np.column_stack(cols+[inside.astype(float)]);w=1/err**2
 cov=np.linalg.pinv(x.T@(w[:,None]*x));coef=cov@(x.T@(w*mag))
 residual=mag-x@coef
 return {'delta_mag':float(coef[-1]),'formal_error':float(np.sqrt(cov[-1,-1])),'formal_snr':float(coef[-1]/np.sqrt(cov[-1,-1])),'n_inside':int(inside.sum()),'n_total':len(t),'distinct_event_numbers':sorted(set(np.rint((t[inside]-epoch)/period).astype(int).tolist())),'chi2':float(np.sum(w*residual**2)),'dof':len(t)-len(coef)}

# Deterministic injection: group offsets must not masquerade as eclipse depth.
test_t=np.arange(0,20,.013);test_g=np.where(test_t<10,'a','b');test_in=abs((test_t+.5)%1-.5)<.05
test=measure(test_t,17+(test_g=='b')*.2+test_in*.15,np.full(len(test_t),.02),test_g,1,0,.1)
assert abs(test['delta_mag']-.15)<1e-8
summary={'created_utc':now(),'seed_sha256':sha(seed),'script_sha256':sha(Path(__file__)),'best':best,'method':'Fixed TESS ephemeris. ZTF midpoint MJD UTC -> BJD TDB using approximate P48 position and builtin solar-system ephemeris. catflags=0, finite positive errors. Per-object median subtraction for plots; simultaneous per-object intercepts for measurements. No phase/period optimization. Formal errors not survey significance.','time_reference_source':'https://web.ipac.caltech.edu/staff/fmasci/ztf/ztf_pipelines_deliverables.pdf section 12 lightcurve schema; mjd is midpoint, so no half-exposure added','sources':{},'stars':{}}
fig,axes=plt.subplots(2,3,figsize=(15,7),constrained_layout=True)
for si,(name,file,ra,dec) in enumerate([('target','target',26.87167439156,65.84783471765),('neighbor','neighbor-retry',26.86886661863,65.84329254925)]):
 path=Path(f'data/targeting/ztf-399450592-{file}.csv');summary['sources'][name]={'path':str(path),'sha256':sha(path)}
 rows=list(csv.DictReader(path.open()));rows=[r for r in rows if int(r['catflags'])==0 and np.isfinite(float(r['mag'])) and np.isfinite(float(r['magerr'])) and float(r['magerr'])>0]
 mjd=np.array([float(r['mjd']) for r in rows]);tm=Time(mjd,format='mjd',scale='utc',location=site)
 t=(tm.tdb+tm.light_travel_time(SkyCoord(ra*u.deg,dec*u.deg))).jd-2457000
 mag=np.array([float(r['mag']) for r in rows]);err=np.array([float(r['magerr']) for r in rows]);groups=np.array([r['oid'] for r in rows]);bands=np.array([r['filtercode'] for r in rows])
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
 centered=mag.copy();object_info=[]
 for g in np.unique(groups):
  m=groups==g;centered[m]-=np.median(mag[m]);rr=[r for r in rows if r['oid']==g]
  object_info.append({'oid':g,'filter':rr[0]['filtercode'],'n':int(m.sum()),'median_mag':float(np.median(mag[m])),'median_ra':float(np.median([float(r['ra']) for r in rr])),'median_dec':float(np.median([float(r['dec']) for r in rr]))})
 summary['stars'][name]={'objects':object_info,'bands':{}}
 for bi,band in enumerate(['zg','zr','zi']):
  m=bands==band;ax=axes[si,bi];ax.set(title=f'{name}: {band}',xlabel='Phase relative to frozen TESS event',ylabel='Magnitude − object median')
  if not m.any():ax.text(.5,.5,'No quality-zero observations',transform=ax.transAxes,ha='center');continue
  ax.errorbar(phase[m]/best['period'],centered[m],yerr=err[m],fmt='.',alpha=.45,ms=3,lw=.4)
  ax.axvspan(-best['duration']/2/best['period'],best['duration']/2/best['period'],alpha=.15,color='red')
  summary['stars'][name]['bands'][band]=measure(t[m],mag[m],err[m],groups[m],best['period'],best['transit_time'],best['duration'])
  ax.invert_yaxis()
 np.savez_compressed(OUT/f'{name}-processed.npz',btjd=t,mag=mag,magerr=err,oid=groups,band=bands,centered_mag=centered)
fig.suptitle('ZTF at frozen TESS ephemeris: larger magnitude means dimming; exploratory diagnostics')
fig.savefig(OUT/'fixed-ephemeris.png',dpi=140);plt.close(fig)
save_json(OUT/'analysis.json',summary)
print(json.dumps(summary['stars'],indent=2))
