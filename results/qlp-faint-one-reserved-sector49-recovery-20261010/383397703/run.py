from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
from exoplanet.campaign import process_target,load_training
out=Path(__file__).parent;tic=int(out.name);orig=Path(f'results/qlp-faint-one-reserved-sector49-pilot-20261010/targets/{tic}.json');target=json.loads(orig.read_text())['target'];raw=Path(f'data/qlp/{tic}-s0049.fits')
with fits.open(raw) as h:
 integrity=verify_hdus(raw,h);d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);usable=(d['QUALITY']==0)&np.isfinite(d['TIME'])&np.isfinite(d[fc])&(d[fc]>0);counts={'rows':len(d),'quality_zero':int((d['QUALITY']==0).sum()),'usable_flux':int(usable.sum()),'valid_errors':int((np.isfinite(d[ec])&(d[ec]>0)).sum())}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'original_sha256':sha(orig),'failed_raw':str(raw),'failed_raw_sha256':sha(raw),'failed_raw_url':'https://mast.stsci.edu/api/v0.1/Download/file/?uri='+target['qlp_products']['49']['dataURL'],'counts':counts,'integrity':integrity,'target':target,'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Original QLP failure retained. All other sectors reserved. Separate same-epoch SPOC attempt with unchanged gates; do not consume reserved data.'});print(counts,flush=True)
(out/'targets').mkdir();r=process_target(target,Path('data'),out,load_training,120);save_json(out/'result.json',{'utc':now(),'original_sha256':sha(orig),'path':str(out/'targets'/f'{tic}.json'),'status':r['status'],'disposition':r.get('disposition'),'error':r.get('error')})
