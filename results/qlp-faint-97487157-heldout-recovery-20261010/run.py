from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
from exoplanet.archive import qlp_flux_columns
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
source=Path('results/qlp-faint-one-reserved-sector22-pilot-20261010/targets/97487157.json')
frozen=Path('results/qlp-faint-one-reserved-sector22-pilot-followup-20261010/97487157-peak0/frozen.json')
target=json.loads(source.read_text())['target'];b=json.loads(frozen.read_text())['best'];raw=Path('data/qlp/97487157-s0045.fits')
with fits.open(raw) as h:
 integrity=verify_hdus(raw,h);d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);good=(d['QUALITY']==0)&np.isfinite(d['TIME'])&np.isfinite(d[fc])&(d[fc]>0)
 counts={'rows':len(d),'quality_zero':int((d['QUALITY']==0).sum()),'usable_flux':int(good.sum()),'valid_errors':int((np.isfinite(d[ec])&(d[ec]>0)).sum())}
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'discovery_sha256':sha(source),'frozen_sha256':sha(frozen),'raw_sha256':sha(raw),'raw_path':str(raw),'raw_url':'https://mast.stsci.edu/api/v0.1/Download/file/?uri='+target['qlp_products']['45']['dataURL'],'integrity':integrity,'counts':counts,'policy':'Recover already attempted reserved Sector45 with SPOC at unchanged frozen ephemeris. No period/phase search; timing uncertainty from original frozen file remains binding.'})
try:
 t,y,e,ev=load_training(dict(target,training_sectors=[45]),Path('data'));m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);r={'status':'measured','data':ev,'measurement':m}
except Exception as exc:r={'status':'error','error':repr(exc)}
save_json(out/'result.json',dict(utc=now(),**r));print(counts,r)
