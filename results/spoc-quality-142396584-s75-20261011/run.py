"""Check the first frozen event in its same-epoch processed light curve."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now,fetch
from exoplanet.campaign import lightcurve_url
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent
p=Path('data/lightcurves/s0075-142396584.fits')
source=fetch(lightcurve_url(142396584,75),p)
assert sha(p)==source['sha256']
fp=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0/frozen.json')
f=json.loads(fp.read_text());b=f['best'];rows=[]
with fits.open(p) as h:
    integrity=verify_hdus(p,h)
    assert h[0].header['TICID']==142396584 and h[0].header['SECTOR']==75
    assert h[1].header['BJDREFI']==2457000 and h[1].header['TIMESYS']=='TDB'
    t=np.array(h[1].data['TIME']);q=np.array(h[1].data['QUALITY'])
    for ev in f['training_measurement']['events']:
        center=ev['center_btjd']
        if not np.nanmin(t)<=center<=np.nanmax(t):continue
        inside=np.isfinite(t)&(abs(t-center)<=b['duration']/2)
        vals,counts=np.unique(q[inside],return_counts=True)
        rows.append({'event':ev['event'],'center_btjd':center,'n_inside':int(inside.sum()),'n_quality_zero':int(sum(inside&(q==0))),'quality_counts':{str(int(v)):int(n) for v,n in zip(vals,counts)}})
save_json(out/'source.json',source)
save_json(out/'quality.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'source_sha256':sha(p),
    'frozen_sha256':sha(fp),'integrity':integrity,'events':rows,
    'quality_definition':'https://lightkurve.github.io/lightkurve/_modules/lightkurve/utils.html#TessQualityFlags',
    'limits':'Quality4096 is automatic stray-light flagging. Flagged exposures are not reliable independent transit confirmation; flags alone do not establish an exact physical cause. Same observing photons as QLP; not independent transit confirmation.'})
print(rows)
