from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.search import flatten
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;p=Path('data/qlp/9823113-s0026.fits');meta=json.loads(Path(str(p)+'.json').read_text());assert meta['sha256']==sha(p)
with fits.open(p) as h:
 assert h[0].header['TICID']==9823113 and h[0].header['SECTOR']==26
 d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);t,y,e=[np.array(d[k],float) for k in ('TIME',fc,ec)]
 keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)&np.isfinite(e)&(e>0)
 result={'source':meta,'file_sha256':sha(p),'total_exposures':len(t),'quality_zero':int((d['QUALITY']==0).sum()),'valid_flux_error_pairs':int(keep.sum()),'flux_column':fc,'error_column':ec}
 t,y,e=t[keep],y[keep],e[keep];order=np.argsort(t);t,y,e=t[order],y[order],e[order]
 try:flatten(t,y,e,window=1.5)
 except ValueError as exc:
  assert str(exc)=='Fewer than 200 clean cadences';result['reproduced_error']=str(exc)
 else:raise AssertionError('Expected original preprocessing failure')
result.update(script_sha256=sha(Path(__file__)),preprocessing_sha256=sha(Path('src/exoplanet/search.py')),limits='Cached valid product, not a transient download failure. Original 1.5-day preprocessing and 200-point gate unchanged. No flux measurement or nondetection inferred.')
save_json(out/'held-coverage-audit.json',result);print(result['total_exposures'],result['valid_flux_error_pairs'],result['reproduced_error'])
