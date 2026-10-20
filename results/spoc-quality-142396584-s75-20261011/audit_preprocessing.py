"""Explain event availability through unchanged SPOC preprocessing, both sectors."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.search import flatten
from exoplanet.pipeline import sha, save_json
out=Path(__file__).parent
fp=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0/frozen.json')
b=json.loads(fp.read_text())['best']; rows=[]
for s in (75,76):
 p=Path(f'data/lightcurves/s{s:04d}-142396584.fits')
 with fits.open(p) as h:
  assert h[0].header['TICID']==142396584 and h[0].header['SECTOR']==s
  d=h[1].data;t=np.array(d['TIME']);quality=np.array(d['QUALITY'])
  for col in ('PDCSAP','SAP'):
   f=np.array(d[col+'_FLUX']);e=np.array(d[col+'_FLUX_ERR'])
   valid=(quality==0)&np.isfinite(t)&np.isfinite(f)&np.isfinite(e)&(f>0)&(e>0)
   tv=t[valid];fv=f[valid];ev=e[valid];order=np.argsort(tv);tv,fv,ev=tv[order],fv[order],ev[order]
   assert np.all(np.diff(tv)>0)
   flat=flatten(tv,fv,ev)[0]
   pieces=np.split(np.arange(len(tv)),np.where(np.diff(tv)>.3)[0]+1)
   for n in ((0,1) if s==75 else (2,3)):
    center=b['transit_time']+n*b['period'];inside=abs(t-center)<b['duration']/2
    segments=[]
    for idx in pieces:
     k=abs(tv[idx]-center)<b['duration']/2
     if not k.any():continue
     width=max(3,int(1.5/np.median(np.diff(tv[idx])))//2*2+1)
     edge=(tv[idx]>tv[idx[0]]+.75)&(tv[idx]<tv[idx[-1]]-.75)
     segments.append({'start':float(tv[idx[0]]),'end':float(tv[idx[-1]]),'length':len(idx),'required_width':width,'event_points':int(k.sum()),'event_points_after_edge_trim':int((k&edge).sum()),'segment_eligible':len(idx)>=max(30,width)})
    rows.append({'sector':s,'column':col,'event':n,'raw_inside':int(inside.sum()),'quality_zero_inside':int((inside&(quality==0)).sum()),'valid_inside':int((inside&valid).sum()),'flattened_inside':int((abs(flat-center)<b['duration']/2).sum()),'segments':segments,'raw_sha256':sha(p)})
result={'script_sha256':sha(Path(__file__)),'frozen_sha256':sha(fp),'rows':rows,'limits':'Availability audit only; unchanged finite positive quality-zero selection and 1.5-day detrending with 0.75-day edge trimming. Missing processed coverage is not a nondetection.'}
save_json(out/'preprocessing-audit.json',result)
print(json.dumps(rows,indent=2))
