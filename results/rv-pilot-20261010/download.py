import csv,json,re
from pathlib import Path
from urllib.parse import urlencode,urljoin
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from bs4 import BeautifulSoup
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import fetch,save_json,now
out=Path(__file__).parent
url='https://exoplanetarchive.ipac.caltech.edu/TAP/sync?'+urlencode({'query':'select pl_name,hostname,ra,dec,pl_orbper from pscomppars','format':'csv'})
cat=Path('data/rv/known-planets-20261010.csv');source=fetch(url,cat)
known=list(csv.DictReader(cat.open()));assert len(known)>6000
coords=SkyCoord([float(r['ra']) for r in known]*u.deg,[float(r['dec']) for r in known]*u.deg)
s=BeautifulSoup(Path('data/rv/rvbank-index.html').read_text(),'html.parser');eligible=[]
for a in s.find_all('a'):
 href=str(a.get('href',''))
 if not (href.startswith('./Ver_02/') and href.endswith('_HARPS_RVBank_ver02.csv')):continue
 cells=a.find_parent('tr').find_all(['th','td'],recursive=False)
 if len(cells)!=12:continue
 fields=[c.get_text(' ',strip=True) for c in cells]
 try:
  name,ra,dec,sptype=fields[:4];teff=float(fields[4]);vmag=float(fields[6]);distance=float(fields[8])
  if not(4000<=teff<=6500 and vmag<10.5 and distance<100):continue
  position=SkyCoord(ra,dec,unit=(u.hourangle,u.deg));separation=position.separation(coords).arcsec
  if separation.min()<60:continue
  if name=='HD32564':continue
  eligible.append(dict(name=name,ra=float(position.ra.deg),dec=float(position.dec.deg),teff=teff,vmag=vmag,distance_pc=distance,url=urljoin('https://exo-restart.com/wp-content/uploads/Stellar_parameters/HARPS_RVBank.html',href)))
 except (ValueError,TypeError):continue
eligible=sorted({r['name']:r for r in eligible}.values(),key=lambda r:r['name'])
rng=np.random.default_rng(20261010);selected=[eligible[i] for i in rng.permutation(len(eligible))[:64]]
save_json(out/'selection.json',dict(created_utc=now(),eligible_count=len(eligible),selected=selected,known_planet_source=source,selection='Seeded 64-star pilot: 4000–6500 K, V<10.5, d<100 pc; exclude within60 arcsec of current pscomppars and external HD32564 lead. Not proof of underexploration or novelty.'))
def one(r):
 p=Path('data/rv/pilot')/(r['name']+'.csv')
 try:
  src=fetch(r['url'],p);rows=list(csv.DictReader(p.open()));assert 'RV_mlc_nzp' in rows[0]
  return dict(**r,path=str(p),source=src,n_rows=len(rows))
 except Exception as e:return dict(**r,error=f'{type(e).__name__}: {e}')
results=[]
with ThreadPoolExecutor(4) as pool:
 for result in pool.map(one,selected):
  results.append(result);save_json(out/'downloads.json',results)
  print(result['name'],result.get('n_rows',result.get('error')),flush=True)
