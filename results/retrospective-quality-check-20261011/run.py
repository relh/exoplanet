"""Frozen event quality comparison in same-epoch SPOC light curves."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import fetch,save_json,sha,now
from exoplanet.campaign import lightcurve_url
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent
assert not (out/'plan.json').exists()
jobs=[]
for p in sorted(Path('results/qlp-faint-retrospective-gap-followup-20261011').glob('*/frozen.json')):
 f=json.loads(p.read_text())
 if f['tic']==310128088:continue
 for sector in f['training_sectors']:
  with fits.open(f"data/qlp/{f['tic']}-s{sector:04d}.fits") as h:
   t=h[1].data['TIME'];lo=float(np.nanmin(t));hi=float(np.nanmax(t))
  events=[e for e in f['training_measurement']['events'] if e['snr']>=3 and lo<=e['center_btjd']<=hi]
  if events:jobs.append({'tic':f['tic'],'sector':sector,'frozen_path':str(p),'frozen_sha256':sha(p),'best':f['best'],'events':events})
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'jobs':jobs,'policy':'Same-epoch diagnostic for all5remaining retrospective signals. Choose sectors containing frozen native events with formal SNR>=3; no period retuning or independent confirmation. Retain HTTP failures, quality differences and raw provenance.'})
rows=[]
for j in jobs:
 r={**j,'started_utc':now()}
 try:
  p=Path(f"data/lightcurves/s{j['sector']:04d}-{j['tic']}.fits")
  source=fetch(lightcurve_url(j['tic'],j['sector']),p)
  with fits.open(p) as h:
   integrity=verify_hdus(p,h);d=h[1].data
   assert int(h[0].header['TICID'])==j['tic'] and int(h[0].header['SECTOR'])==j['sector']
   t=np.array(d['TIME']);q=np.array(d['QUALITY']);events=[]
   for ev in j['events']:
    dt=t-ev['center_btjd'];inside=np.isfinite(t)&(abs(dt)<j['best']['duration']/2)
    outside=np.isfinite(t)&(abs(dt)>j['best']['duration'])&(abs(dt)<3*j['best']['duration'])
    vals,counts=np.unique(q[inside],return_counts=True)
    events.append({'event':ev['event'],'center':ev['center_btjd'],'n_inside':int(inside.sum()),'n_inside_quality_zero':int(sum(inside&(q==0))),'n_outside_quality_zero':int(sum(outside&(q==0))),'quality_counts':{str(int(v)):int(n) for v,n in zip(vals,counts)},'n_straylight2':int(sum(inside&((q&4096)!=0))),'n_planet_search_exclude':int(sum(inside&((q&8192)!=0)))})
  r.update(status='complete',source=source,integrity=integrity,events_quality=events)
 except Exception as exc:r.update(status='error',error=repr(exc))
 r['finished_utc']=now();rows.append(r);save_json(out/'progress.json',rows);print(j['tic'],j['sector'],r['status'],r.get('events_quality',r.get('error')),flush=True)
save_json(out/'results.json',rows)
