"""Preserve unusable Sector 76 evidence; search latest unreserved sector 77."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.integrity import verify_hdus
from exoplanet.pipeline import sha, save_json, now
from exoplanet.campaign import process_target
from exoplanet.qlp_campaign import load_qlp

out=Path(__file__).parent
original=Path('results/qlp-faint-sector76-expanded-20261010/targets/23849990.json')
row=json.loads(original.read_text());target=row['target']
assert row['status']=='error' and target['training_sectors']==[76]
raw=Path('data/qlp/23849990-s0076.fits')
with fits.open(raw) as h:
    integrity=verify_hdus(raw,h)
    assert h[0].header['TICID']==23849990 and h[0].header['SECTOR']==76
    d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
    t,y,e=[np.array(d[c],float) for c in ['TIME',fc,ec]]
    usable=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)
    counts={'rows':len(d),'finite_time':int(np.isfinite(t).sum()),
            'quality_zero':int((d['QUALITY']==0).sum()),
            'finite_positive_flux':int((np.isfinite(y)&(y>0)).sum()),
            'valid_errors':int((np.isfinite(e)&(e>0)).sum()),'usable_flux':int(usable.sum())}
remaining=sorted(set(target['sectors'])-set(target['training_sectors'])-set(target['heldout_sectors']))
assert remaining[-1]==77
replacement=dict(target,training_sectors=[77])
assert not Path('data/qlp/23849990-s0077.fits').exists()
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'original_path':str(original),'original_sha256':sha(original),
    'failed_raw':str(raw),'failed_raw_sha256':sha(raw),'failed_raw_url':'https://mast.stsci.edu/api/v0.1/Download/file/?uri='+target['qlp_products']['76']['dataURL'],
    'integrity':integrity,'counts':counts,'target':replacement,'script_sha256':sha(Path(__file__)),
    'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},
    'policy':'Original Sector76 failure retained. Latest available nonreserved sector77 is a separate discovery attempt chosen before opening its photometry. Same loader and gates. This does not repair the original run or add a distinct target; reserved epochs remain available only for later frozen tests.'})
(out/'targets').mkdir()
r=process_target(replacement,Path('data'),out,load_qlp,120)
save_json(out/'result.json',{'utc':now(),'original_sha256':sha(original),
    'path':str(out/'targets'/'23849990.json'),'status':r['status'],
    'disposition':r.get('disposition'),'error':r.get('error')})
