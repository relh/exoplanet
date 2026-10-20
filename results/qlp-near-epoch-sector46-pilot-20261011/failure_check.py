"""Audit unusable discovery data without opening the reserved epoch."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.integrity import verify_hdus
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
source=out/'targets/389347623.json';r=json.loads(source.read_text());raw=Path('data/qlp/389347623-s0046.fits')
with fits.open(raw) as h:
 integrity=verify_hdus(raw,h);assert h[0].header['TICID']==389347623 and h[0].header['SECTOR']==46
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
 t,y,e=[np.array(d[k],dtype=float) for k in ['TIME',fc,ec]]
 good=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)
 tt=np.sort(t[good]);dt=np.diff(tt);cad=np.median(dt[dt>0]) if np.any(dt>0) else None
 pairs=int(np.sum((dt>0)&(dt<1.5*cad))) if cad else 0
 counts={'total':len(t),'quality_zero':int(np.sum(d['QUALITY']==0)),'finite_positive_flux':int(np.sum(np.isfinite(y)&(y>0))),'usable_flux':int(good.sum()),'usable_published_errors':int(np.sum(good&np.isfinite(e)&(e>0))),'adjacent_pairs':pairs}
assert pairs<100 and counts['usable_published_errors']==0
assert not Path('data/qlp/389347623-s0049.fits').exists()
save_json(out/'failure_check.json',{'utc':now(),'tic':389347623,'source_sha256':sha(source),'raw_path':str(raw),'raw_sha256':sha(raw),'download_manifest':json.loads(Path(str(raw)+'.json').read_text()),'integrity':integrity,'counts':counts,'status':'unusable_discovery','interpretation':'Insufficient data for unchanged empirical-noise gate; retained as unusable, not a nondetection. Only other sector49 remains reserved and unopened; no training replacement available without consuming validation.'})
print(counts)
