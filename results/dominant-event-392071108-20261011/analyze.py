from pathlib import Path
import json,numpy as np
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json,now
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;source=Path('results/weak-seed-ranks256-384-20261011/targets/392071108.json');r=json.loads(source.read_text());rows=[]
for w in r['windows']:
 b=w['best'];t,y,e,_=load_training(r['selection']['target'],Path('data'),window=w['window_days']);event=np.rint((t-b['transit_time'])/b['period']).astype(int);dominant=int(np.rint((1860.2995-b['transit_time'])/b['period']));keep=event!=dominant;m=fixed_measure(t[keep],y[keep],e[keep],b['period'],b['transit_time'],b['duration']);rows.append(dict(window_days=w['window_days'],removed_event=dominant,n_removed=int((~keep).sum()),measurement_without_dominant_event=m))
raw=Path('data/lightcurves/s0020-392071108.fits')
with fits.open(raw) as h:
 assert h[0].header['TICID']==392071108 and h[0].header['SECTOR']==20
 d=h[1].data;use=np.isfinite(d['TIME'])&(abs(d['TIME']-1860.2995)<1);cols=['TIME','QUALITY','SAP_FLUX','PDCSAP_FLUX','SAP_BKG','MOM_CENTR1','MOM_CENTR2'];data={k:np.asarray(d[k][use]).tolist() for k in cols}
fig,axes=plt.subplots(4,1,figsize=(11,9),sharex=True,constrained_layout=True);t=np.asarray(data['TIME']);q=np.asarray(data['QUALITY'])
for ax,keys in zip(axes,[['SAP_FLUX','PDCSAP_FLUX'],['SAP_BKG'],['MOM_CENTR1','MOM_CENTR2'],['QUALITY']]):
 for k in keys:
  y=np.asarray(data[k]);y=y/np.nanmedian(y)-1 if k in ['SAP_FLUX','PDCSAP_FLUX'] else y-np.nanmedian(y) if k.startswith('MOM') else y;ax.plot(t,y,'.-',ms=3,label=k)
 ax.axvspan(1860.2995-r['windows'][0]['best']['duration']/2,1860.2995+r['windows'][0]['best']['duration']/2,alpha=.15,color='red');ax.legend();ax.grid(alpha=.2)
axes[-1].set_xlabel('BTJD');fig.suptitle('TIC392071108 dominant event: raw flux, background, centroids and quality');fig.savefig(p/'event.png',dpi=120);plt.close(fig)
assert not Path('data/lightcurves/s0072-392071108.fits').exists()
data={k:[v if np.isfinite(v) else None for v in values] for k,values in data.items()}
save_json(p/'diagnostic.json',dict(created_utc=now(),source_sha256=sha(source),raw_sha256=sha(raw),raw_columns=data,omission_tests=rows,policy='Posthoc omission of already-identified dominant event near BTJD1860.2995, with clock and duration unchanged; whole orbital event removed, no new fit. Raw telemetry shown without detrending; physical cause not inferred solely from correlation.'))
print([(x['window_days'],x['measurement_without_dominant_event']['total']) for x in rows])
