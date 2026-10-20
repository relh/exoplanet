"""Reproduce the coverage failure and inspect traceback counts without changing gates."""
from pathlib import Path
import json
from astropy.io import fits
from exoplanet.integrity import verify_hdus
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=out/'targets/257531000.json';r=json.loads(source.read_text());raw=Path('data/qlp/257531000-s0026.fits')
with fits.open(raw) as h:
 integrity=verify_hdus(raw,h);assert h[0].header['TICID']==257531000 and h[0].header['SECTOR']==26
counts=[]
for window in [1.5,2.5]:
 try:load_qlp(r['target'],Path('data'),window=window)
 except ValueError as exc:
  tb=exc.__traceback__;frames=[]
  while tb:
   f=tb.tb_frame
   if f.f_code.co_name=='flatten':
    loc=f.f_locals;frames.append({'function':'flatten','input_cadences':len(loc['time']),'clean_cadences':len(loc['t']) if 't' in loc and 'y' in loc and 'dy' in loc else None})
   tb=tb.tb_next
  counts.append({'window':window,'error':str(exc),'frames':frames})
 else:raise AssertionError('Unexpected usable data')
assert counts[0]['error']=='Fewer than 200 clean cadences' and counts[0]['frames'][0]['clean_cadences']<200
assert not Path('data/qlp/257531000-s0025.fits').exists()
save_json(out/'failure_check.json',{'utc':now(),'source_sha256':sha(source),'raw_path':str(raw),'raw_sha256':sha(raw),'download_manifest':json.loads(Path(str(raw)+'.json').read_text()),'integrity':integrity,'checks':counts,'status':'unusable_discovery','interpretation':'Minimum clean-cadence gate preserved. No replacement training sector without consuming sole reserved25. No injections run because baseline loader is unusable; not a nondetection or sensitivity trial.'})
print(counts)
