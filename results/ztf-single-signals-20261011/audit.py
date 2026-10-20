"""Inventory downloaded ZTF objects before any transit measurement."""
from pathlib import Path
from collections import defaultdict
import json,csv,numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');assert plan['script_sha256']==sha(out/'download.py');results=read(out/'results.json');assert {r['tic'] for r in results}=={t['tic'] for t in plan['targets']};summary=[]
for result in results:
 target=next(t for t in plan['targets'] if t['tic']==result['tic']);assert sha(Path(target['frozen_path']))==target['frozen_sha256']
 if result['status']=='error':summary.append({'tic':result['tic'],'status':'download_error','error':result['error']});continue
 p=Path(result['path']);assert sha(p)==result['source']['sha256'];reader=csv.DictReader(p.open());required={'oid','ra','dec','mjd','mag','magerr','catflags','filtercode'}
 if not required<=set(reader.fieldnames or []):summary.append({'tic':result['tic'],'status':'invalid_schema','columns':reader.fieldnames,'raw_sha256':sha(p)});continue
 rows=list(reader);assert len(rows)==result['n_rows'];groups=defaultdict(list)
 for r in rows:groups[r['oid']].append(r)
 objects=[]
 for oid,rs in groups.items():
  coord=SkyCoord(ra=float(np.median([float(r['ra']) for r in rs]))*u.deg,dec=float(np.median([float(r['dec']) for r in rs]))*u.deg);origin=SkyCoord(*target['position'],unit='deg');good=[r for r in rs if int(r['catflags'])==0 and all(np.isfinite(float(r[k])) for k in ['mjd','mag','magerr']) and float(r['magerr'])>0]
  objects.append({'oid':oid,'filters':sorted({r['filtercode'] for r in rs}),'n_rows':len(rs),'n_quality_zero_finite':len(good),'median_ra':float(coord.ra.deg),'median_dec':float(coord.dec.deg),'separation_from_tic_arcsec':float(origin.separation(coord).arcsec),'mjd_range':None if not good else [min(float(r['mjd']) for r in good),max(float(r['mjd']) for r in good)]})
 summary.append({'tic':result['tic'],'status':'metadata_audited','raw_sha256':sha(p),'n_rows':len(rows),'objects':objects})
save_json(out/'audit.json',{'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'results_sha256':sha(out/'results.json'),'rows':summary,'limits':'Inventory only. Positional agreement does not resolve blends; times not yet converted to TESS reference and no transit recovery tested. Error/invalid schema is not absence of observations.'});print(summary)
