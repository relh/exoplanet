from pathlib import Path
import importlib.util,json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.integrity import verify_hdus
from exoplanet.search import flatten
O=Path(__file__).parent;V=Path('results/expanded-96166003-20261012/verify.py');sp=importlib.util.spec_from_file_location('independent',V);iv=importlib.util.module_from_spec(sp);sp.loader.exec_module(iv)
p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());assert r['plan_sha256']==sha(O/'plan.json');assert p['created_utc']<=r['created_utc'];assert len(r['rows'])==8
for path,h in p['inputs'].items():assert sha(Path(path))==h
checks=[];integrity={}
for row in r['rows']:
 assert row['best']==next(c['best'] for c in p['clocks'] if c['name']==row['clock'])
 arrays=[]
 for sector in row['sectors']:
  path=Path(sector['path']);assert sha(path)==sector['raw_sha256']
  with fits.open(path,checksum=False) as h:
   integrity[str(path)]=verify_hdus(path,h);assert all(x['checksum']=='verified' for x in integrity[str(path)]);assert h[0].header['TICID']==96166003 and h[0].header['SECTOR']==sector['sector'];d=h[1].data;m=(d['QUALITY']==0)&np.isfinite(d['TIME'])
   for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:m &= np.isfinite(d[key])&(d[key]>0)
   assert int(m.sum())==sector['common_input_points'];t,y,e=flatten(np.asarray(d['TIME'][m],float),np.asarray(d[row['kind']+'_FLUX'][m],float),np.asarray(d[row['kind']+'_FLUX_ERR'][m],float),window=row['window']);assert len(t)==sector['clean_points'];z=np.load(O/f"{row['kind']}-{row['window']}-s{sector['sector']}.npz")
   for key,a in dict(t=t,y=y,e=e).items():np.testing.assert_array_equal(a,z[key])
   iv.measured(t,y,e,row['best'],sector['measurement']);arrays.append((t,y,e))
 t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];iv.measured(t,y,e,row['best'],row['measurement']);checks.append(dict(clock=row['clock'],kind=row['kind'],window=row['window'],sectors=[x['sector'] for x in row['sectors']]))
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),independent_helper_sha256=sha(V),checks=checks,raw_integrity=integrity,checksum_warning='Byte-level FITS checksum verification used; no checksum warning encountered in thisrun.',scope='Thirty-two raw/common-mask/detrending/array and per-sector total/event reconstructions plus eight combined measurements independently summed; fixedclock/hash/identity/byte-levelFITS integrity. Same preprocessing and photons; not independent discovery or source validation.'))
print('passed32sector+8combinedmeasurementsets')
