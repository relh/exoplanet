"""Fixed-TESS-ephemeris, per-object ZTF checks; no period/phase optimization."""
from pathlib import Path
import json,csv
import numpy as np
from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy.utils import iers
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
iers.conf.auto_download=False
out=Path(__file__).parent;raw=Path('data/catalogs/ztf-207468583-neighborhood-20261010.csv')
f=Path('results/qlp-faint-expanded-followup-20261010/207468582-peak0/frozen.json');b=json.loads(f.read_text())['best']
rows=list(csv.DictReader(raw.open()));assert rows and 'oid' in rows[0]
rows=[r for r in rows if int(r['catflags'])==0 and all(np.isfinite(float(r[k])) for k in ['mjd','mag','magerr']) and float(r['magerr'])>0]
groups={}
for r in rows:groups.setdefault(r['oid'],[]).append(r)
npth=Path('results/neighbors-207468582-20261010/neighbors.json');neighbors=json.loads(npth.read_text())
catalog=SkyCoord([r['ra'] for r in neighbors]*u.deg,[r['dec'] for r in neighbors]*u.deg)
site=EarthLocation.from_geodetic(-116.863*u.deg,33.3563*u.deg,1706*u.m)
results=[];processed={}
for oid,rr in groups.items():
 ra=float(np.median([float(r['ra']) for r in rr]));dec=float(np.median([float(r['dec']) for r in rr]));coord=SkyCoord(ra*u.deg,dec*u.deg)
 sep=coord.separation(catalog).arcsec;idx=int(np.argmin(sep))
 mjd=np.array([float(r['mjd']) for r in rr]);tm=Time(mjd,format='mjd',scale='utc',location=site)
 t=(tm.tdb+tm.light_travel_time(coord)).jd-2457000
 mag=np.array([float(r['mag']) for r in rr]);e=np.array([float(r['magerr']) for r in rr])
 phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 inside=abs(phase)<b['duration']/2;outside=(abs(phase)>b['duration'])&(abs(phase)<3*b['duration'])
 result={'oid':oid,'filter':rr[0]['filtercode'],'ra':ra,'dec':dec,'nearest_tic':int(neighbors[idx]['ID']),'separation_arcsec':float(sep[idx]),'n_total':len(rr),'n_inside':int(inside.sum()),'n_outside_local':int(outside.sum()),'median_mag':float(np.median(mag))}
 if inside.sum()>=3 and outside.sum()>=5:
  w=1/e**2;delta=np.average(mag[inside],weights=w[inside])-np.average(mag[outside],weights=w[outside]);error=np.sqrt(1/w[inside].sum()+1/w[outside].sum())
  result.update(delta_mag=float(delta),formal_error=float(error),formal_snr=float(delta/error),n_distinct_events=len(np.unique(np.rint((t[inside]-b['transit_time'])/b['period']).astype(int))))
 results.append(result);processed[oid]=(t,phase,mag,e)
results.sort(key=lambda r:r.get('formal_snr',-np.inf),reverse=True)
save_json(out/'analysis.json',{'utc':now(),'raw_sha256':sha(raw),'frozen_sha256':sha(f),'neighbor_sha256':sha(npth),'script_sha256':sha(Path(__file__)),'best':b,'objects':results,'policy':'Fixed TESS ephemeris, no period or phase optimization. ZTF midpoint MJD UTC -> BJD TDB with approximate P48 coordinates, builtin solar-system ephemeris and each object position. catflags=0. Each OID analyzed separately, local phase-sideband baseline. Formal errors ignore red noise and source-selection trials. Catalog association uses nearest TIC without proper-motion propagation; inspect separations.','timing_documentation':'https://web.ipac.caltech.edu/staff/fmasci/ztf/ztf_pipelines_deliverables.pdf section12; no extra half-exposure added'})
fig,axes=plt.subplots(min(4,len(results)),1,figsize=(10,3*min(4,len(results))),constrained_layout=True)
for ax,r in zip(np.atleast_1d(axes),results):
 t,phase,mag,e=processed[r['oid']];ax.errorbar(phase/b['period'],mag,yerr=e,fmt='.',alpha=.5,ms=3,lw=.4);ax.axvspan(-b['duration']/2/b['period'],b['duration']/2/b['period'],alpha=.15,color='red');ax.invert_yaxis();ax.set(title=f"OID {r['oid']}, {r['filter']}, nearest TIC{r['nearest_tic']} ({r['separation_arcsec']:.2f} arcsec)",xlabel='Phase from frozen TESS event',ylabel='Magnitude')
fig.savefig(out/'fixed-phase.png',dpi=140);plt.close(fig)
for r in results:print(r,flush=True)
