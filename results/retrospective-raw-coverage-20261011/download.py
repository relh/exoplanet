from pathlib import Path
import json,zipfile
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
assert not (out/'plan.json').exists()
jobs=[]
for tic,sectors in [(352831349,[16,17]),(258513090,[85,86])]:
 row=json.loads(Path(f'results/qlp-faint-expanded-20261010/targets/{tic}.json').read_text())
 for sector in sectors:jobs.append({'tic':tic,'sector':sector,'ra':row['target']['star']['ra'],'dec':row['target']['star']['dec']})
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'jobs':jobs,'policy':'Same discovery epochs only; raw coverage/background check at frozen ephemerides. Single-event maps cannot satisfy two-event localization gate; no host attribution.'})
rows=[]
for j in jobs:
 r={**j,'started_utc':now()}
 try:
  p=Path(f"data/pixels/retro-{j['tic']}-s{j['sector']}.zip")
  params={k:j[k] for k in ['ra','dec','sector']};params.update(x=11,y=11,units='px')
  r['source']=fetch('https://mast.stsci.edu/tesscut/api/v0.1/astrocut',p,params)
  files=[]
  with zipfile.ZipFile(p) as z:
   for name in z.namelist():
    if not name.endswith('.fits'):continue
    dest=Path('data/pixels')/Path(name).name
    assert not dest.exists()
    dest.write_bytes(z.read(name));files.append({'path':str(dest),'sha256':sha(dest)})
  assert len(files)==1
  r.update(status='complete',files=files)
 except Exception as exc:r.update(status='error',error=repr(exc))
 r['finished_utc']=now();rows.append(r);save_json(out/'progress.json',rows);print(j['tic'],j['sector'],r['status'],r.get('error',''),flush=True)
save_json(out/'downloads.json',rows)
