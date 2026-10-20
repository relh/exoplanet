"""Inventory identities, quality and timestamp coverage; no photometric inference."""
from pathlib import Path
import json,numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import save_json,sha
p=Path(__file__).parent;result=json.loads((p/'results.json').read_text());assert result['status']=='downloaded'
catalog=json.loads(Path('results/ztf-catalog-route-20261011/catalog-results.json').read_text());lookup={int(o['oid']):(r['tic'],o) for r in catalog for o in r['rows']};out=[]
assert len({r['objectid'] for r in result['objects']})==len(result['objects'])
for r in result['objects']:
 f=Path(r['path']);assert sha(f)==r['sha256'];obj=json.loads(f.read_text());oid=obj['objectid'];assert oid==r['objectid'];tic,cat=lookup[oid]
 assert obj['filterid']==int(cat['fid']);assert obj['nepochs']==len(obj['lightcurve'])==r['n_rows']
 sep=SkyCoord(obj['objra']*u.deg,obj['objdec']*u.deg).separation(SkyCoord(float(cat['ra'])*u.deg,float(cat['dec'])*u.deg)).arcsec
 rows=obj['lightcurve'];required={'hmjd','mag','magerr','catflags'};assert all(required<=set(x) for x in rows)
 good=[x for x in rows if x['catflags']==0 and all(x[k] is not None and np.isfinite(x[k]) for k in ['hmjd','mag','magerr']) and x['magerr']>0]
 times=[x['hmjd'] for x in good]
 out.append({'tic':tic,'objectid':oid,'filterid':obj['filterid'],'n_rows':len(rows),'catalog_nobs':int(cat['nobs']),'n_quality_zero_finite':len(good),'catalog_ngoodobs':int(cat['ngoodobs']),'catalog_position_separation_arcsec':float(sep),'hmjd_range':None if not times else [min(times),max(times)],'repeated_good_timestamps':len(times)-len(set(times)),'median_magerr':None if not good else float(np.median([x['magerr'] for x in good]))})
save_json(p/'audit.json',{'inputs':{n:sha(p/n) for n in ['plan.json','results.json','audit.py']},'objects':out,'missing_ids':result['missing_ids'],'limits':'HMJD retained unconverted. No phase folding, transit test, detection or nondetection. Catalog good-observation definition may differ from catflags==0. Cross-object duplicate exposures and blend identities need review.'});print(out)
