import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from astropy.io import fits
from exoplanet.pipeline import fetch,save_json,sha
out=Path(__file__).parent;rows=json.loads((out/'observations.json').read_text())['rows']
jobs=[]
for row in rows:
 for sector in [10,36,37]:
  if sector==10:camera,ccd=2,1
  else:
   with fits.open(f'data/pixels/80387959-s{sector:04d}.fits') as h:camera,ccd=h[0].header['CAMERA'],h[0].header['CCD']
  uri=row['dataURL'].replace('s0010',f's{sector:04d}').replace('cam2-ccd1',f'cam{camera}-ccd{ccd}')
  jobs.append({'tic':int(row['target_name']),'sector':sector,'uri':uri,'uri_policy':'Sector10 archive-query URL; sectors36/37 follow same documented naming/path structure with camera/CCD from downloaded SPOC pixels. Validate returned FITS identity.'})
def get(job):
 job={**job};path=Path(f'data/tglc/{job["tic"]}-s{job["sector"]:04d}.fits')
 try:job['source']=fetch('https://mast.stsci.edu/api/v0.1/Download/file/?uri='+job['uri'],path);job['path']=str(path);job['status']='downloaded'
 except Exception as exc:job['status']='error';job['error']=repr(exc)
 return job
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(get,jobs))
save_json(out/'downloads.json',results)
for r in results:print(r['tic'],r['sector'],r['status'],r.get('error'))
