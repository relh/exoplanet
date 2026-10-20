from pathlib import Path
import json,csv
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'catalog-results.json').read_text());plan=json.loads((p/'catalog-plan.json').read_text());out=[]
for row in r:
 target=next(x for x in plan['targets'] if x['tic']==row['tic']);file=Path(row['path']);assert sha(file)==row['sha256'];actual=list(csv.DictReader(file.open()));assert actual==row['rows'];assert len(actual)==row['n_rows']<100
 sky=SkyCoord(*target['position'],unit='deg');objects=[]
 for obj in actual:
  point=SkyCoord(float(obj['ra'])*u.deg,float(obj['dec'])*u.deg);sep=float(sky.separation(point).arcsec);assert sep<=3
  objects.append({'oid':obj['oid'],'filter':obj['filtercode'],'separation_from_tic_arcsec':sep,'nobs_catalog':int(obj['nobs']),'ngoodobs_catalog':int(obj['ngoodobs']),'medianmag':float(obj['medianmag'])})
 out.append({'tic':row['tic'],'objects':objects,'catalog_nobs_sum':sum(x['nobs_catalog'] for x in objects)})
save_json(p/'catalog-audit.json',{'inputs':{n:sha(p/n) for n in ['catalog-plan.json','catalog-results.json','audit_catalog.py']},'rows':out,'limits':'Catalog entries are not independent astrophysical objects. Positions compared to unpropagated TIC coordinates only; no source attribution, epoch audit, transit detection or duplicate-exposure correction yet.'});print(out)
