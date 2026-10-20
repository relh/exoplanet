"""Audit failed discovery inputs without consuming reserved validation."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.integrity import verify_hdus
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;rows=[]
for tic in [3962839,119612415,457919551]:
 source=out/'targets'/f'{tic}.json';r=json.loads(source.read_text());raw=Path(f'data/qlp/{tic}-s0051.fits')
 assert r['status']=='error' and r['target']['heldout_sectors']==[50]
 with fits.open(raw) as h:
  integrity=verify_hdus(raw,h);assert h[0].header['TICID']==tic and h[0].header['SECTOR']==51
  d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
  t,y,e=[np.array(d[k],dtype=float) for k in ['TIME',fc,ec]]
  good=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)
  tt=np.sort(t[good]);dt=np.diff(tt);cad=np.median(dt[dt>0]) if np.any(dt>0) else None
  pairs=int(np.sum((dt>0)&(dt<1.5*cad))) if cad else 0
  counts={'total':len(t),'quality_zero':int(np.sum(d['QUALITY']==0)),'finite_positive_flux':int(np.sum(np.isfinite(y)&(y>0))),'usable_flux':int(good.sum()),'usable_published_errors':int(np.sum(good&np.isfinite(e)&(e>0))),'adjacent_pairs':pairs}
 assert pairs<100 and counts['usable_published_errors']==0
 assert not Path(f'data/qlp/{tic}-s0050.fits').exists()
 rows.append({'tic':tic,'source_sha256':sha(source),'raw_path':str(raw),'raw_sha256':sha(raw),'download_manifest':json.loads(Path(str(raw)+'.json').read_text()),'integrity':integrity,'counts':counts,'status':'unusable_discovery'})
 print(tic,counts)
save_json(out/'failure_check.json',{'utc':now(),'rows':rows,'interpretation':'Insufficient data for unchanged empirical-noise gate; unusable, not nondetections. Only other sector50 remains reserved; no replacement training can preserve validation.'})
