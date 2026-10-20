from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
for tic,sector in [(15820624,43)]:
 rp=out/'targets'/f'{tic}.json';r=json.loads(rp.read_text());assert r['status']=='error' and r['target']['training_sectors']==[sector]
 raw=Path(f'data/qlp/{tic}-s{sector:04d}.fits')
 with fits.open(raw) as h:
  d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);counts={'rows':len(d),'q0':int(sum(d['QUALITY']==0)),'finite_flux':int(np.isfinite(d[fc]).sum()),'finite_error':int(np.isfinite(d[ec]).sum())}
 assert counts['finite_flux']==0 and counts['finite_error']==0
 save_json(out/f'data-error-{tic}.json',{'script_sha256':sha(Path(__file__)),'result_sha256':sha(rp),'raw_path':str(raw),'raw_sha256':sha(raw),'product':r['target']['qlp_products'][str(sector)],'original_error':r['error'],'flux_column':fc,'error_column':ec,'counts':counts,'interpretation':'No finite selected training flux/errors. Data failure, not transit nondetection. No network retry or reserved-sector substitution.'})
 print(tic,fc,counts)
