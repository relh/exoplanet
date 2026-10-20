from pathlib import Path
import zipfile
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;p=Path('data/pixels/tesscut-466895419-s55.zip')
params={'ra':311.250059144249,'dec':3.26044753841835,'x':11,'y':11,'units':'px','sector':55}
save_json(out/'request.json',{'params':params,'utc':now(),'script_sha256':sha(Path(__file__)),'doc':'https://mast.stsci.edu/tesscut/docs/getting_started.html'})
try:
 source=fetch('https://mast.stsci.edu/tesscut/api/v0.1/astrocut',p,params);save_json(out/'source.json',source)
 files=[]
 with zipfile.ZipFile(p) as z:
  for name in z.namelist():
   if not name.endswith('.fits'):continue
   dest=Path('data/pixels')/Path(name).name
   assert not dest.exists(),'Do not overwrite existing evidence'
   dest.write_bytes(z.read(name));files.append({'member':name,'path':str(dest),'sha256':sha(dest)})
 save_json(out/'files.json',files);print(files)
except Exception as exc:save_json(out/'error.json',{'error':repr(exc),'utc':now()});print(repr(exc))
