"""Fixed-clock descriptive SAP/PDC comparison of already-opened sectors."""
from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
O=Path(__file__).parent;FP=Path('results/expanded-402358350-20261011/frozen-for81.json');SECTORS=[40,41,54,81]
def main():
 assert not (O/'plan.json').exists(),'No overwrites';clock=json.loads(FP.read_text())['rows'][0]['best'];paths=[Path(f'data/lightcurves/s{s:04d}-402358350.fits') for s in SECTORS]
 for p in paths:assert p.exists()
 save_json(O/'plan.json',dict(created_utc=now(),clock=clock,clock_path=str(FP),sectors=SECTORS,windows=[1.5,2.5],reductions=['SAP','PDCSAP'],inputs={str(p):sha(p) for p in paths+[FP,Path(__file__),Path('src/exoplanet/search.py'),Path('src/exoplanet/followup.py')]},policy='All40/41/54/81 previously opened. Same expanded primaryclock for every sector/reduction/window; no refit. Common quality0+finitepositive masks for bothfluxes/errors before separate sectorlocal detrending. Different finalcleaning mayyield differing coverage; retain counts. Postselection descriptive comparison; reductions share photons, dilution/noise/corrections differ.'))
 rows=[]
 for w in [1.5,2.5]:
  for kind in ['SAP','PDCSAP']:
   arrays=[];sectorrows=[]
   for s,path in zip(SECTORS,paths):
    with fits.open(path,checksum=True) as h:
     assert h[0].header['TICID']==402358350 and h[0].header['SECTOR']==s;d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
     for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[key])&(d[key]>0)
     t,y,e=flatten(np.asarray(d['TIME'][mask],float),np.asarray(d[kind+'_FLUX'][mask],float),np.asarray(d[kind+'_FLUX_ERR'][mask],float),window=w);arrays.append((t,y,e));sectorrows.append(dict(sector=s,path=str(path),raw_sha256=sha(path),common_input_points=int(mask.sum()),clean_points=len(t),measurement=fixed_measure(t,y,e,clock['period'],clock['transit_time'],clock['duration'])));np.savez_compressed(O/f'{kind}-{w}-s{s}.npz',t=t,y=y,e=e)
   t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];rows.append(dict(window=w,kind=kind,sectors=sectorrows,measurement=fixed_measure(t,y,e,clock['period'],clock['transit_time'],clock['duration'])))
 save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows));print([(r['kind'],r['window'],r['measurement']['total']) for r in rows])
if __name__=='__main__':main()
