from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
from exoplanet.integrity import verify_hdus
O=Path(__file__).parent;FP=Path('results/expanded-96166003-20261012/frozen-for59.json');SECTORS=[19,43,44,59]
def main():
 assert not (O/'plan.json').exists();f=json.loads(FP.read_text());clocks=[dict(name=r['role'],best=r['best']) for r in f['rows']];paths=[Path(f'data/lightcurves/s{s:04d}-96166003.fits') for s in SECTORS];save_json(O/'plan.json',dict(created_utc=now(),clocks=clocks,sectors=SECTORS,windows=[1.5,2.5],reductions=['SAP','PDCSAP'],inputs={str(p):sha(p) for p in paths+[FP,Path(__file__),Path('src/exoplanet/search.py'),Path('src/exoplanet/followup.py')]},policy='Allsectorsalreadyopened. Cross bothpre59expandedclocks withbothdetrendingwindows/reductions. Fixednominalclocks,no search/refit. Commonqualityfinitepositiveinputmask, separatepersectorflatten. Retrospectivedescriptiveanalysis: clocksselectedbefore59 but thisfactorialanalysischosenafterseeingmixed59. Samephotons notindependentobservations.'))
 rows=[]
 for window in [1.5,2.5]:
  for kind in ['SAP','PDCSAP']:
   arrays=[];metadata=[]
   for sector,path in zip(SECTORS,paths):
    with fits.open(path,checksum=False) as h:
     integrity=verify_hdus(path,h);assert all(x['checksum']=='verified' for x in integrity);assert h[0].header['TICID']==96166003 and h[0].header['SECTOR']==sector;d=h[1].data;mask=(d['QUALITY']==0)&np.isfinite(d['TIME'])
     for key in ['SAP_FLUX','SAP_FLUX_ERR','PDCSAP_FLUX','PDCSAP_FLUX_ERR']:mask &= np.isfinite(d[key])&(d[key]>0)
     t,y,e=flatten(np.asarray(d['TIME'][mask],float),np.asarray(d[kind+'_FLUX'][mask],float),np.asarray(d[kind+'_FLUX_ERR'][mask],float),window=window);arrays.append((t,y,e));metadata.append(dict(sector=sector,path=str(path),raw_sha256=sha(path),common_input_points=int(mask.sum()),clean_points=len(t),integrity=integrity));np.savez_compressed(O/f'{kind}-{window}-s{sector}.npz',t=t,y=y,e=e)
   for clock in clocks:
    b=clock['best'];sectorrows=[dict(**meta,measurement=fixed_measure(*a,b['period'],b['transit_time'],b['duration'])) for meta,a in zip(metadata,arrays)];t,y,e=[np.concatenate([a[j] for a in arrays]) for j in range(3)];rows.append(dict(clock=clock['name'],best=b,window=window,kind=kind,sectors=sectorrows,measurement=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])))
 save_json(O/'results.json',dict(created_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows));print('8crossedcomparisons')
if __name__=='__main__':main()
