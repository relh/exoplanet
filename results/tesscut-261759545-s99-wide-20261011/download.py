from pathlib import Path
import zipfile
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;p=Path('data/pixels/tesscut-261759545-s99-wide.zip')
params={'ra':193.684157176277,'dec':-54.0279449083524,'x':31,'y':31,'units':'px','sector':99}
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
